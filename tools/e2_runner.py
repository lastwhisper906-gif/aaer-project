"""E2 실행 하네스 (D67) — 146호출 세션의 안전 레일. tools/ 소재 (채점측 오케스트레이션).

  .venv/bin/python tools/e2_runner.py            # dry-run: 계획·드리프트·잔여 출력만
  AAER_RAW_API_APPROVED=1 .venv/bin/python tools/e2_runner.py --execute   # 발사
  .venv/bin/python tools/e2_runner.py --postrun-only                      # 후처리 재실행

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


def execute(manifest: dict, is_done=None, run_one=None) -> dict:
    """호출 루프 — is_done/run_one 주입 가능 (테스트), 기본 = 실물."""
    is_done = is_done or _is_done
    if run_one is None:
        from runner_api import run_case_api

        def run_one(row, entry, log_dir):
            return run_case_api(entry, True, out_path(row).parent, log_dir,
                                TEMPERATURE_PIN)
    rows = buildable_rows(manifest)
    done = [r for r in rows if is_done(out_path(r))]
    todo = [r for r in rows if not is_done(out_path(r))]
    if len(done) + len(todo) != manifest["totals"]["buildable"]:
        raise E2RunError(f"지출 가드: 완료 {len(done)} + 잔여 {len(todo)} != "
                         f"buildable {manifest['totals']['buildable']}")
    assert TEMPERATURE_PIN == 0.0  # 온도 핀 (상수 변조 방지 이중 확인)
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


def _s0_score(base_case_id: str, tier: str) -> int:
    p = (REPO / "runs/perturbed" / f"{base_case_id}.json" if tier == "wave1"
         else REPO / "runs/wave2/perturbed" / f"{base_case_id}.json")
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
            b4s0 = b4m.b4_score(row["ticker"], datetime.date.fromisoformat(base_cut))
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
    return {"flag_threshold_llm": FLAG_LLM, "flag_threshold_b3": FLAG_B3,
            "cases": [cases[k] for k in sorted(cases)],
            "_adapter": "tools/e2_runner.py (D66/D67 — q=floor(days/91), s0=동결 perturbed)"}


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
    args = ap.parse_args()
    manifest = load_manifest()
    try:
        drift_check(manifest)
        if args.postrun_only:
            print(f"후처리 → {postrun(manifest)}")
            return 0
        rows = buildable_rows(manifest)
        todo = [r for r in rows if not _is_done(out_path(r))]
        print(f"계획: buildable {len(rows)} · 완료 {len(rows) - len(todo)} · "
              f"잔여 {len(todo)} · temp={TEMPERATURE_PIN} · 예산 {manifest['budget_of_record']}")
        if not args.execute:
            print("dry-run — 발사는 --execute (AAER_RAW_API_APPROVED=1 + 키 필요, "
                  "스모크 래치 §6-3 선행)")
            return 0
        from api_client import assert_raw_api_approved
        assert_raw_api_approved()
        r = execute(manifest)
        print(f"실행 완료: 시도 {r['attempted']} · FAIL {r['failures']}")
        if r["failures"] == 0 and all(_is_done(out_path(x)) for x in rows):
            print(f"후처리 → {postrun(manifest)}")
        return 0 if r["failures"] == 0 else 2
    except E2RunError as e:
        print(f"E2 HALT — {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
