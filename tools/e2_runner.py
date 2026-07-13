"""E2 실행 하네스 (D67, D69 --client) — 146호출 세션의 안전 레일. tools/ 소재 (채점측 오케스트레이션).

  .venv/bin/python tools/e2_runner.py            # dry-run: 계획·드리프트·잔여 출력만
  .venv/bin/python tools/e2_runner.py --client harness --execute          # 발사 (개정 #4 — 구독 하네스)
  AAER_RAW_API_APPROVED=1 .venv/bin/python tools/e2_runner.py --execute   # 발사 (개정 #3 raw — 보류 중)
  .venv/bin/python tools/e2_runner.py --postrun-only                      # 후처리 재실행

클라이언트 경로 (freeze 개정 #4, docs/FREEZE_REV4_HARNESS_E2.md):
  --client harness = 동결 runner.run_case / cli_client.call_model (구독, 전 발행
    tier와 동일 경로). 가드 = assert_no_metered_credentials + require_clean_tree
    (raw 승인 래치·스모크 래치는 raw 경로와 한 몸으로 보류). 온도 핀은 하네스에
    없음 — TEMPERATURE_PIN assert는 이 모드에서 N/A (L-3 미해소, 개정 #4 §3).
  --client api (기본) = D67 원형 그대로 (runner_api.run_case_api, 개정 #3 래치).

안전 레일 (전부 호출 전 평가):
  1. 매니페스트 드리프트 정지 — 커밋된 data/e2/E2_MANIFEST.json ≠ 현재 재생성
     (smoke_rev3와 동일 패턴, fail-closed exit 2).
  2. 지출 가드 — 완료+잔여 == buildable 회계 불일치 시 정지; 런타임 시도 카운터가
     잔여를 넘으면 즉시 정지 (이중 안전).
  3. 온도 핀 — TEMPERATURE_PIN=0.0 상수, 플래그로 변경 불가 (FREEZE_REV3).
  4. INVARIANT 4 — 출력 기록 직후 API 키 문자열 스캔, 발견 시 파일 삭제+정지.
  5. 재개 멱등 — runner_api의 output_is_valid 스킵 + 원자적 기록(tmp→replace):
     크래시 후 같은 명령 재실행 = 미완분만, 중복 지출 0.

후처리 (전 스냅샷 완료 시 자동): 어댑터 → analysis/e2_trajectories.json →
engine_verdict (b4_comparison.valid=false 자기 기록 포함, D61 예측) →
runs/e2/E2_SUMMARY.md. buyer_metrics는 가격 인자가 필요해 명령만 안내.

어댑터 규약 (D66): quarters_to_revelation = floor((기저컷오프+1 − 스냅샷컷오프)/91일).
s0 = 동결 본실행 perturbed 점수 재사용 (runs/perturbed·runs/wave2/perturbed).
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "pipeline"))
sys.path.insert(0, str(REPO / "analysis"))
sys.path.insert(0, str(REPO / "analysis" / "vendor"))

import e2_generate_cases as gen  # noqa: E402

E2_DIR = REPO / "data" / "e2"
RUNS = REPO / "runs" / "e2"
TRAJ_OUT = REPO / "analysis" / "e2_trajectories.json"
TEMPERATURE_PIN = 0.0  # FREEZE_REV3 — 상수, 인자로 바꿀 수 없다
FLAG_LLM, FLAG_B3 = 50, 2  # ENGINE_DECISION §2 (동결 재사용)


class E2RunError(Exception):
    pass


def load_manifest() -> dict:
    return json.loads((E2_DIR / "E2_MANIFEST.json").read_text(encoding="utf-8"))


def drift_check(manifest: dict) -> None:
    """커밋 매니페스트 ≠ 재생성 산술 → 정지 (smoke_rev3 패턴)."""
    regen = gen.compute_manifest(gen.derive_roster())
    if [dict(r) for r in regen["rows"]] != [
            {k: v for k, v in r.items()} for r in manifest["rows"]]:
        raise E2RunError("드리프트: 커밋된 E2_MANIFEST ≠ 재생성 산술 — fail-closed. "
                         "생성기 재실행·재커밋 후 발사하라")


def buildable_rows(manifest: dict) -> list[dict]:
    rows = [r for r in manifest["rows"] if r["status"] == "buildable"]
    return sorted(rows, key=lambda r: (r["ticker"], r["j"]))  # PLAN §5 순서


def out_path(row: dict) -> Path:
    return RUNS / f"s{row['j']}" / f"{row['base_case_id']}.json"


def _is_done(path: Path) -> bool:
    import cli_client
    from runner import FULL_OUTPUT_SCHEMA
    return cli_client.output_is_valid(path, FULL_OUTPUT_SCHEMA)


def _batch_entry(row: dict) -> dict:
    batch = json.loads((E2_DIR / f"cases_e2_s{row['j']}.json").read_text(encoding="utf-8"))
    for c in batch["cases"]:
        if c["case_id"] == row["base_case_id"]:
            return c
    raise E2RunError(f"배치 s{row['j']}에 {row['base_case_id']} 없음")


def scrub_check(path: Path) -> None:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key and path.is_file() and key in path.read_text(encoding="utf-8"):
        path.unlink()
        raise E2RunError(f"INVARIANT 4 위반: 출력에 API 키 문자열 — {path} 삭제·정지")


def _snap_log_dir(row, log_dir: Path) -> Path:
    """스냅샷별 로그 격리 (D70) — 러너의 log_name이 기저 case_id로만 구성되어
    같은 케이스의 s{j}들이 로그 파일을 상호 덮어씀 (D67 잠복 결함, 실사격 발견).
    동결 runner.py는 무수정 — run_one이 제어하는 log_dir을 s{j}로 분기해 해소."""
    return log_dir / f"s{row['j']}"


def _run_one_api(row, entry, log_dir):
    from runner_api import run_case_api
    return run_case_api(entry, True, out_path(row).parent,
                        _snap_log_dir(row, log_dir), TEMPERATURE_PIN)


def _run_one_harness(row, entry, log_dir):
    from runner import run_case  # 동결 모듈 — 무수정 (§8-3), 출력 형식·멱등 skip 동일
    return run_case(entry, True, out_path(row).parent, _snap_log_dir(row, log_dir))


def _default_run_one(client: str):
    if client == "harness":
        return _run_one_harness
    if client == "api":
        return _run_one_api
    raise E2RunError(f"알 수 없는 --client: {client}")


def client_preflight(client: str) -> None:
    """발사 직전 경로별 가드 — harness(개정 #4) vs api(개정 #3 래치)."""
    import cli_client
    if client == "harness":
        cli_client.assert_no_metered_credentials()  # INVARIANT 4 — 키 존재 = 즉시 예외
        cli_client.require_clean_tree()             # freeze-commit-then-run (runner.py main 동형)
    elif client == "api":
        from api_client import assert_raw_api_approved
        assert_raw_api_approved()
    else:
        raise E2RunError(f"알 수 없는 --client: {client}")


def execute(manifest: dict, is_done=None, run_one=None, client: str = "api") -> dict:
    """호출 루프 — is_done/run_one 주입 가능 (테스트), 기본 = client 경로 실물."""
    is_done = is_done or _is_done
    if run_one is None:
        run_one = _default_run_one(client)
    rows = buildable_rows(manifest)
    done = [r for r in rows if is_done(out_path(r))]
    todo = [r for r in rows if not is_done(out_path(r))]
    if len(done) + len(todo) != manifest["totals"]["buildable"]:
        raise E2RunError(f"지출 가드: 완료 {len(done)} + 잔여 {len(todo)} != "
                         f"buildable {manifest['totals']['buildable']}")
    if client == "api":
        assert TEMPERATURE_PIN == 0.0  # 온도 핀 (raw 전용 — 하네스는 핀 부재 N/A, 개정 #4 §3)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = REPO / "logs" / f"run_e2_{ts}"
    attempted, failures = 0, 0
    for row in todo:
        attempted += 1
        if attempted > len(todo):
            raise E2RunError("지출 가드: 시도 횟수가 잔여를 초과 — 즉시 정지")
        res = run_one(row, _batch_entry(row), log_dir)
        scrub_check(out_path(row))
        print(f"{row['snapshot_id']}: {res['status']}", flush=True)
        if str(res.get("status", "")).startswith("FAIL"):
            failures += 1
    return {"done_before": len(done), "attempted": attempted, "failures": failures}


# ---------------------------------------------------------------- post-run

def _q_to_rev(base_cutoff: str, snap_cutoff: str) -> int:
    rev = datetime.date.fromisoformat(base_cutoff) + datetime.timedelta(days=1)
    return max(0, (rev - datetime.date.fromisoformat(snap_cutoff)).days // 91)


def _s0_score(base_case_id: str, tier: str) -> int | None:
    """동결 perturbed draw-1 점수 (j=0 재사용). RP-01 v1 대조군은 perturbed
    프레임 미채점(동결 점수가 원본 프레임에만 존재) — 파일 부재 시 None
    (llm_p null), ENGINE_DECISION §3 주석(D71)의 fail-closed 규약."""
    p = (REPO / "runs/perturbed" / f"{base_case_id}.json" if tier == "wave1"
         else REPO / "runs/wave2/perturbed" / f"{base_case_id}.json")
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))["misstatement_probability"]


def build_trajectories(manifest: dict, runs_dir: Path = RUNS) -> dict:
    """어댑터 — E2 출력 + 생성 기록(동반 점수) + s0 동결 점수 → ENGINE §1 스키마."""
    import b3_compute
    import b4_short_interest as b4m
    cases: dict[str, dict] = {}
    for row in buildable_rows(manifest):
        cid = row["base_case_id"]
        if cid not in cases:
            base_cut = json.loads((E2_DIR / f"{row['snapshot_id']}.json")
                                  .read_text(encoding="utf-8"))["base_cutoff"]
            b3s0 = b3_compute.b3_score(row["ticker"],
                                       datetime.date.fromisoformat(base_cut), 730)
            # §14 관할 명시 (D77): E2 궤적의 b4는 D66 규칙(LAG=14)으로 동결 —
            # 사이드카(s1+)와 규칙 일관성 유지를 위해 실측 매핑을 명시적 비적용
            b4s0 = b4m.b4_score(row["ticker"], datetime.date.fromisoformat(base_cut),
                                dissemination_map=None)
            cases[cid] = {"case_id": cid, "ticker": row["ticker"],
                          "group": row["group"], "_base_cutoff": base_cut,
                          "snapshots": [{
                              "j": 0, "cutoff": base_cut,
                              "quarters_to_revelation": _q_to_rev(base_cut, base_cut),
                              "llm_p": _s0_score(cid, row["tier"]),
                              "b3_score": b3s0["score"],
                              "b4_slope_aug": b4s0["score_slope_aug"]}]}
        rec = json.loads((E2_DIR / f"{row['snapshot_id']}.json").read_text(encoding="utf-8"))
        out = json.loads(out_path(row).read_text(encoding="utf-8"))
        cases[cid]["snapshots"].append({
            "j": row["j"], "cutoff": row["cutoff"],
            "quarters_to_revelation": _q_to_rev(cases[cid]["_base_cutoff"], row["cutoff"]),
            "llm_p": out["misstatement_probability"],
            "b3_score": rec["b3_W8"]["score"],
            "b4_slope_aug": rec["b4"].get("score_slope_aug")})
    for c in cases.values():
        c.pop("_base_cutoff")
        c["snapshots"].sort(key=lambda s: s["j"])
    s0_null = sorted(cid for cid, c in cases.items()
                     if any(s["j"] == 0 and s["llm_p"] is None for s in c["snapshots"]))
    return {"flag_threshold_llm": FLAG_LLM, "flag_threshold_b3": FLAG_B3,
            "cases": [cases[k] for k in sorted(cases)],
            "_s0_llm_unavailable": s0_null,
            "_adapter": ("tools/e2_runner.py (D66/D67/D71 — q=floor(days/91), "
                         "s0=동결 perturbed; RP-01 v1 대조군 perturbed 미채점 → llm_p null)")}


def postrun(manifest: dict, runs_dir: Path = RUNS) -> Path:
    import engine_verdict as ev
    traj = build_trajectories(manifest, runs_dir)
    TRAJ_OUT.write_text(json.dumps(traj, ensure_ascii=False, sort_keys=True, indent=1)
                        + "\n", encoding="utf-8")
    verdict = ev.compute({k: v for k, v in traj.items() if not k.startswith("_")})
    (REPO / "analysis" / "engine_verdict.json").write_text(
        json.dumps(verdict, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
        encoding="utf-8")
    b4c = verdict.get("b4_comparison", {})
    summary = REPO / "runs" / "e2" / "E2_SUMMARY.md"
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text("\n".join([
        "# E2_SUMMARY — 자동 후처리 (tools/e2_runner.py, D67)", "",
        f"- 판정 브랜치: **{verdict['branch']}** (b_subcase={verdict.get('b_subcase')})",
        f"- median lead — LLM {verdict.get('median_lead_llm_quarters')}분기 · "
        f"B3 {verdict.get('median_lead_b3_quarters')}분기",
        f"- b4_comparison.valid = **{b4c.get('valid')}**"
        + (f" — 사유: {b4c.get('reason')}" if not b4c.get("valid") else ""),
        "- (D60/D61 사전 예측: 커버리지 미달로 valid=false — 무료 신호 대결은 seal 관할)",
        "- 다음: buyer_metrics — `.venv/bin/python analysis/buyer_metrics_build.py "
        "--logs-dir logs/<run_e2_*> --price-in <USD/MTok> --price-out <USD/MTok>`",
        "- 판정 결과의 원장 기록(D-엔트리)·commit·push는 발사 세션 마무리 절차.", "",
    ]), encoding="utf-8")
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--execute", action="store_true", help="실호출 (기본: dry-run)")
    ap.add_argument("--postrun-only", action="store_true")
    ap.add_argument("--client", choices=("api", "harness"), default="api",
                    help="호출 경로: api(개정 #3 raw, 래치 필요) / harness(개정 #4 구독)")
    args = ap.parse_args()
    manifest = load_manifest()
    temp_desc = TEMPERATURE_PIN if args.client == "api" else "N/A(harness, L-3)"
    resume_cmd = (".venv/bin/python tools/e2_runner.py "
                  + " ".join(a for a in sys.argv[1:]))
    import cli_client
    try:
        drift_check(manifest)
        if args.postrun_only:
            print(f"후처리 → {postrun(manifest)}")
            return 0
        rows = buildable_rows(manifest)
        todo = [r for r in rows if not _is_done(out_path(r))]
        print(f"계획: buildable {len(rows)} · 완료 {len(rows) - len(todo)} · "
              f"잔여 {len(todo)} · client={args.client} · temp={temp_desc} · "
              f"예산 {manifest['budget_of_record']}")
        if not args.execute:
            print("dry-run — 발사는 --execute (--client harness = 개정 #4 구독 경로 / "
                  "--client api = 개정 #3 raw, AAER_RAW_API_APPROVED=1 + 키 + 스모크 래치 §6-3)")
            return 0
        client_preflight(args.client)
        r = execute(manifest, client=args.client)
        print(f"실행 완료: 시도 {r['attempted']} · FAIL {r['failures']}")
        if r["failures"] == 0 and all(_is_done(out_path(x)) for x in rows):
            print(f"후처리 → {postrun(manifest)}")
        return 0 if r["failures"] == 0 else 2
    except cli_client.RateLimitedError as e:
        print(f"E2 HALT (레이트 리밋, 멱등 — 완료분 자동 skip) — {e}", file=sys.stderr)
        print(f"재개 명령:\n  {resume_cmd}")
        return 3
    except E2RunError as e:
        print(f"E2 HALT — {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
