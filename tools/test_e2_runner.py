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


def test_crash_tmp_artifact_not_treated_as_done(sandbox):
    """원자 기록의 반대면: 크래시가 남긴 .tmp 부분 파일은 '완료'가 아니다 —
    재실행이 해당 스냅샷을 다시 (정확히 1회) 지출한다."""
    rows = er.buildable_rows(sandbox)
    victim = rows[0]
    p = er.out_path(victim)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.with_suffix(".json.tmp").write_text('{"misstatement_prob')  # 부분 파일
    calls = []
    er.execute(sandbox, is_done=fake_done, run_one=make_run_one(calls))
    assert calls.count(victim["snapshot_id"]) == 1
    assert p.is_file()                           # 정본 존재
    assert not p.with_suffix(".json.tmp").exists()  # 부분 파일은 rename으로 소거
    assert len(calls) == 4                       # 전 스냅샷 정확 1회


# ---------------------------------------------------------------- D69 --client harness


def test_client_mode_selection():
    assert er._default_run_one("harness") is er._run_one_harness
    assert er._default_run_one("api") is er._run_one_api
    with pytest.raises(er.E2RunError, match="알 수 없는"):
        er._default_run_one("sdk")


def test_harness_run_one_delegates_to_frozen_runner(sandbox, monkeypatch):
    """하네스 run_one은 동결 runner.run_case에 (entry, perturb=True, 출력 디렉토리,
    log_dir) 그대로 위임한다 — runner.py 무수정 계약 (§8-3)."""
    import runner
    seen = {}

    def fake_run_case(case, perturb, out_dir, log_dir):
        seen.update(case=case, perturb=perturb, out_dir=out_dir, log_dir=log_dir)
        return {"case_id": case["case_id"], "status": "OK p=50"}

    monkeypatch.setattr(runner, "run_case", fake_run_case)
    row = er.buildable_rows(sandbox)[0]
    entry = {"case_id": row["base_case_id"]}
    res = er._run_one_harness(row, entry, Path("/tmp/logs"))
    assert res["status"].startswith("OK")
    assert seen["case"] is entry and seen["perturb"] is True
    assert seen["out_dir"] == er.out_path(row).parent
    assert seen["log_dir"] == Path("/tmp/logs")


def test_harness_preflight_blocks_metered_key(monkeypatch):
    """개정 #4 가드: 하네스 모드에서 ANTHROPIC_API_KEY 존재 = 즉시 예외 (INVARIANT 4)."""
    import cli_client
    monkeypatch.setattr(cli_client, "require_clean_tree", lambda: None)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        er.client_preflight("harness")


def test_harness_preflight_skips_raw_latch(monkeypatch):
    """하네스 모드는 raw 승인 래치를 참조하지 않는다 (개정 #3은 보류) —
    AAER_RAW_API_APPROVED 부재·키 부재에서 통과, clean-tree 가드는 호출된다."""
    import cli_client
    called = []
    monkeypatch.setattr(cli_client, "require_clean_tree", lambda: called.append(1))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("AAER_RAW_API_APPROVED", raising=False)
    er.client_preflight("harness")          # 예외 없음
    assert called == [1]


def test_api_preflight_still_requires_latch(monkeypatch):
    """api 모드 가드는 D67 원형 그대로 — 래치 부재 시 즉시 예외."""
    monkeypatch.delenv("AAER_RAW_API_APPROVED", raising=False)
    with pytest.raises(RuntimeError, match="raw API"):
        er.client_preflight("api")


def test_temp_pin_na_in_harness_mode(sandbox, monkeypatch):
    """온도 핀 assert는 raw 전용 — 하네스 모드는 핀 부재가 N/A (개정 #4 §3, L-3).
    api 모드에서는 상수 변조가 여전히 정지를 일으킨다."""
    monkeypatch.setattr(er, "TEMPERATURE_PIN", 0.7)
    calls = []
    er.execute(sandbox, is_done=fake_done, run_one=make_run_one(calls),
               client="harness")            # 하네스: 예외 없음
    assert len(calls) == 4
    with pytest.raises(AssertionError):
        er.execute(sandbox, is_done=fake_done, run_one=make_run_one([]),
                   client="api")


def test_crash_resume_idempotent_harness_client(sandbox):
    """크래시-재개 멱등은 client 인자와 무관하게 유지 — harness 경로로 명시 실행."""
    calls = []
    with pytest.raises(RuntimeError, match="simulated crash"):
        er.execute(sandbox, is_done=fake_done,
                   run_one=make_run_one(calls, crash_after=2), client="harness")
    assert len(calls) == 2
    er.execute(sandbox, is_done=fake_done, run_one=make_run_one(calls),
               client="harness")
    assert sorted(calls) == sorted(set(calls)) and len(calls) == 4
