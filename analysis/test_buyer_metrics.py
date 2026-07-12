"""buyer_metrics_build 픽스처 테스트 — 합성 E2-형 데이터 4지표 + fail-closed (D52)."""
import json

import pytest

import buyer_metrics_build as bm


def _case(cid, group, points):
    return {"case_id": cid, "ticker": cid.upper(), "group": group,
            "snapshots": [{"j": j, "cutoff": f"2026-0{j+1}-01",
                           "quarters_to_revelation": t, "llm_p": p, "b3_score": b}
                          for j, t, p, b in points]}


TRAJ = {
    "flag_threshold_llm": 50, "flag_threshold_b3": 2,
    "cases": [
        # 실험군 3: LLM lead 3/3/1 → 중위 3, B3 lead 1/0/1 → 중위 1
        _case("t0", "treatment", [(0, 1, 80, 2), (1, 2, 70, 1), (2, 3, 60, 0),
                                  (3, 4, 30, 0), (4, 5, 20, 0), (5, 6, 10, 0),
                                  (6, 7, 10, 0), (7, 8, 10, 0)]),
        _case("t1", "treatment", [(0, 1, 75, 0), (1, 2, 65, 1), (2, 3, 55, 1),
                                  (3, 4, 40, 1), (4, 5, 30, 0), (5, 6, 20, 0),
                                  (6, 7, 10, 0), (7, 8, 10, 0)]),
        _case("t2", "treatment", [(0, 1, 90, 3), (1, 2, 40, 1)]),  # 깊이 2 (절단)
        # 대조군 4: 1건만 LLM 오탐 (s에서 55), B3 오탐 0
        _case("c0", "control", [(0, 1, 30, 0), (1, 2, 55, 1)]),
        _case("c1", "control", [(0, 1, 20, 0), (1, 2, 25, 0)]),
        _case("c2", "control", [(0, 1, 10, 1), (1, 2, 15, 0)]),
        _case("c3", "control", [(0, 1, 40, 0), (1, 2, 35, 1)]),
    ],
}


@pytest.fixture()
def logs_dir(tmp_path):
    d = tmp_path / "logs"
    d.mkdir()
    for i, (tin, tout) in enumerate([(9000, 900), (11000, 1100), (10000, 1000)]):
        (d / f"call_{i}.json").write_text(json.dumps(
            {"usage": {"input_tokens": tin, "output_tokens": tout}}))
    (d / "no_usage.json").write_text(json.dumps({"ok": True}))  # usage 없는 로그는 무시
    return d


def test_four_metrics(logs_dir):
    v = bm.compute(TRAJ, logs_dir, price_in=3.0, price_out=15.0)
    # 1. 리드타임 — 엔진 판정과 동일 산식
    assert v["lead_llm_median"] == 3 and v["lead_b3_median"] == 1
    assert v["lead_llm_range"] == "1–3"
    # 2. FPR@임계 + CP95 (동결 clopper_pearson 재사용)
    assert v["fpr_llm"] == "1/4 = 25.0%" and v["fpr_b3"] == "0/4 = 0.0%"
    assert v["fpr_llm_ci"].startswith("[0.6%")   # CP(1,4) 하한 0.63%
    assert v["fpr_b3_ci"] == "[0.0%, 60.2%]"     # CP(0,4) — N 소표본 정직 상한
    # 3. 비용 — 평균 10000 in / 1000 out, $3/$15 per MTok
    assert v["tokens_in_mean"] == 10000 and v["n_calls_measured"] == 3
    assert v["cost_per_screen"] == "$0.0450"
    # 4. 커버리지
    assert v["n_treatment"] == 3 and v["n_control"] == 4
    assert "t2" in v["coverage_truncation"]


def test_render_fills_every_placeholder(logs_dir):
    text = bm.render(bm.compute(TRAJ, logs_dir, 3.0, 15.0))
    assert "{" not in text.replace("{placeholder}", "")  # 템플릿 잔여 placeholder 0
    assert "**3**" in text and "$0.0450" in text
    assert "수기 편집 금지" in text


def test_price_optional_but_explicit(logs_dir):
    v = bm.compute(TRAJ, logs_dir, None, None)
    assert "단가 미입력" in v["cost_per_screen"]  # 지어낸 단가 금지 — 명시 문구


def test_fail_closed():
    with pytest.raises(bm.BuyerMetricsError):  # 빈 대조군
        bm.compute({"flag_threshold_llm": 50, "flag_threshold_b3": 2,
                    "cases": [_case("t0", "treatment", [(0, 1, 80, 2)])]}, None, None, None)


def test_fail_closed_empty_logs(tmp_path):
    d = tmp_path / "empty_logs"
    d.mkdir()
    (d / "x.json").write_text(json.dumps({"no": "usage"}))
    with pytest.raises(bm.BuyerMetricsError, match="usage 실측 로그 0건"):
        bm.compute(TRAJ, d, 3.0, 15.0)
