"""E2 러너 안전 레일 테스트 (D67) — 전부 오프라인, 실호출 0.

크래시-재개, 지출 가드, 드리프트 정지, 온도 핀, 키 스크럽, 후처리 체인.
"""
import copy
import json
import os
from pathlib import Path

import pytest

import e2_runner as er


def mini_manifest(tmp_path, n_cases=2, n_snaps=2):
    rows = []
    for c in range(n_cases):
        for j in range(1, n_snaps + 1):
            rows.append({"snapshot_id": f"case_9{c}_s{j}", "base_case_id": f"case_9{c}",
                         "ticker": f"TK{c}", "tier": "wave1",
                         "group": "treatment" if c == 0 else "control",
                         "j": j, "status": "buildable", "cutoff": f"2015-0{j}-15"})
    return {"rows": rows, "totals": {"buildable": len(rows), "grid_ineligible": 0,
                                     "build_failed": 0},
            "budget_of_record": {"evaluatee_calls": len(rows), "grader_calls": 0}}


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    monkeypatch.setattr(er, "RUNS", tmp_path / "runs")
    monkeypatch.setattr(er, "E2_DIR", tmp_path / "e2")
    (tmp_path / "e2").mkdir()
    m = mini_manifest(tmp_path)
    for j in (1, 2):
        (tmp_path / "e2" / f"cases_e2_s{j}.json").write_text(json.dumps(
            {"cases": [{"case_id": f"case_9{c}", "ticker": f"TK{c}",
                        "cik": "0", "company_name": f"Co{c}",
                        "cutoff_date": f"2015-0{j}-15"} for c in (0, 1)]}))
    return m


def fake_done(path: Path) -> bool:
    return path.is_file()


def make_run_one(call_log, crash_after=None):
    def run_one(row, entry, log_dir):
        if crash_after is not None and len(call_log) >= crash_after:
            raise RuntimeError("simulated crash")
        call_log.append(row["snapshot_id"])
        p = er.out_path(row)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps({"misstatement_probability": 40 + row["j"]}))
        tmp.replace(p)
        return {"case_id": row["base_case_id"], "status": "OK"}
    return run_one


def test_crash_resume_no_respend_no_gaps(sandbox):
    calls = []
    with pytest.raises(RuntimeError, match="simulated crash"):
        er.execute(sandbox, is_done=fake_done, run_one=make_run_one(calls, crash_after=1))
    assert len(calls) == 1                       # 크래시 전 1건만 지출
    er.execute(sandbox, is_done=fake_done, run_one=make_run_one(calls))
    assert sorted(calls) == sorted(set(calls))   # 중복 지출 0
    assert len(calls) == 4                       # 갭 0 (전 스냅샷 정확 1회)
    r = er.execute(sandbox, is_done=fake_done, run_one=make_run_one(calls))
    assert r["attempted"] == 0                   # 3차 실행 = 전부 스킵


def test_spend_guard_accounting_halt(sandbox):
    bad = copy.deepcopy(sandbox)
    bad["totals"]["buildable"] = 3               # 회계 불일치 조작
    with pytest.raises(er.E2RunError, match="지출 가드"):
        er.execute(bad, is_done=fake_done, run_one=make_run_one([]))


def test_drift_check_halts_on_mismatch(monkeypatch, sandbox):
    monkeypatch.setattr(er.gen, "derive_roster", lambda: [])
    monkeypatch.setattr(er.gen, "compute_manifest",
                        lambda roster: {"rows": [{"other": 1}]})
    with pytest.raises(er.E2RunError, match="드리프트"):
        er.drift_check(sandbox)


def test_temperature_pin_is_constant():
    assert er.TEMPERATURE_PIN == 0.0             # FREEZE_REV3 핀 — 플래그 부재가 계약


def test_key_scrub_deletes_and_halts(tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-SECRET-123")
    p = tmp_path / "out.json"
    p.write_text(json.dumps({"debug": "leaked sk-test-SECRET-123"}))
    with pytest.raises(er.E2RunError, match="INVARIANT 4"):
        er.scrub_check(p)
    assert not p.exists()                        # 오염 출력은 남지 않는다


def test_postrun_chain_end_to_end(sandbox, tmp_path, monkeypatch):
    """합성 출력 → 어댑터 → 실제 engine_verdict → E2_SUMMARY (valid=false 라인)."""
    er.execute(sandbox, is_done=fake_done, run_one=make_run_one([]))
    for row in er.buildable_rows(sandbox):       # 생성 기록 사이드카 합성
        (er.E2_DIR / f"{row['snapshot_id']}.json").write_text(json.dumps(
            {"base_cutoff": "2015-06-30", "b3_W8": {"score": row["j"] % 3},
             "b4": {"state": "not_computable"}}))
    monkeypatch.setattr(er, "_s0_score", lambda cid, tier: 60)
    monkeypatch.setattr(er, "TRAJ_OUT", tmp_path / "traj.json")
    import b3_compute, b4_short_interest
    monkeypatch.setattr(b3_compute, "b3_score", lambda *a, **k: {
        "score": 1, "indicators": {}, "flags": {}})
    monkeypatch.setattr(b4_short_interest, "b4_score", lambda *a, **k: {
        "score_slope_aug": None, "score_level": None, "flags": {}})
    monkeypatch.setattr(er, "REPO", tmp_path)    # verdict/summary도 샌드박스에
    (tmp_path / "analysis").mkdir()
    summary = er.postrun(sandbox)
    text = summary.read_text(encoding="utf-8")
    assert "b4_comparison.valid = **False**" in text
    assert "판정 브랜치" in text
    traj = json.loads((tmp_path / "traj.json").read_text())
    case = traj["cases"][0]
    assert [s["j"] for s in case["snapshots"]] == [0, 1, 2]   # s0 + 신규 정렬
    assert traj["flag_threshold_llm"] == 50 and traj["flag_threshold_b3"] == 2
