"""RP-09 Stage 3a: 대조군 v2 채점 — 단일 명령 런북 (발사는 소유자 YES 후에만).

사용:
  python3 tools/run_control_v2_scoring.py --plan     # 실행 계획·호출 회계만 출력 (호출 0)
  python3 tools/run_control_v2_scoring.py --launch   # 전 단계 실행 (게이트 통과 시)

게이트: scoring/overrides.md 에 리터럴 서명줄 `RP-09-FINAL: YES` 가 존재해야
--launch 가 진행된다 (소유자 §Final 결정의 기계 확인 — 없으면 즉시 중단).

단계 (전부 멱등 — 중단 시 같은 명령 재실행):
  1. stage-data   : v2 선정사 companyfacts/submissions를 ~/aaer-data/_rp08 캐시에서
                    피평가자 데이터 규약 경로(~/aaer-data/{TICKER}/{xbrl,edgar})로 복사
                    (네트워크 없음 — 캐시 부재 시 소리 나는 실패)
  2. build-inputs : data/evaluatee/cases_v2.json (중립 ID case_17.., 고정 시드 셔플)
                    + scoring/id_mapping_v2.json (V-ID) + data/candidates/
                    candidates_v2_controls.json (채점 정답 키 — group=control).
                    사명은 **컷오프 시점 사명** (submissions formerNames 재구성, OV-002)
  3. score        : pipeline/runner.py --cases data/evaluatee/cases_v2.json
                    --out runs/rp09/scores  (핀 sonnet-5, I1 가드, 동시성 3)
  4. probes       : pipeline/probe_runner.py --recognition (교란 페이로드 정체 프로브,
                    --out-root scoring/probe_results_v2 — I3: 기존 probe_results 불가침)
  5. grade        : scoring/grader_runner.py --runs runs/rp09/scores
                    --out scoring/grades_v2/controls --mapping scoring/id_mapping_v2.json
                    --candidates data/candidates/candidates_v2_controls.json
                    (I3: scoring/grades/ 동결 — v2는 grades_v2/)

I1/I2: 페이로드는 기존 build_payload 경유(유일 look-ahead 필터 + guard_payload) —
이 스크립트는 페이로드를 만들지 않는다. 컷오프 = 매칭 실험군 컷오프 복사 (GP-9 ①).
"""
import argparse
import datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BIG = Path.home() / "aaer-data/_rp08"
DATA = Path.home() / "aaer-data"
V2 = REPO / "runs/rp09/control_group_v2.json"
CASES_V2_DEST = REPO / "data/evaluatee/cases_v2.json"
MAPPING_DEST = REPO / "scoring/id_mapping_v2.json"
CAND_DEST = REPO / "data/candidates/candidates_v2_controls.json"
GATE_FILE = REPO / "scoring/overrides.md"
GATE_LINE = "RP-09-FINAL: YES"
NEUTRAL_ID_SEED_V2 = 20260707  # 사전 커밋 고정 (build_evaluatee_inputs 규약 승계)
NEUTRAL_ID_START = 17          # case_01~16은 동결 실험 집합 — 겹침 금지


def selected_controls() -> list:
    v2 = json.loads(V2.read_text(encoding="utf-8"))
    rows = []
    for tid in sorted(v2["selections"]):
        sel = v2["selections"][tid]
        for i, s in enumerate(sel["selected"], 1):
            rows.append({"matched_treatment": tid, "rank_in_case": i,
                         "cutoff_date": sel["treatment"]["cutoff"], **s})
    return rows


def name_at_cutoff(cik: str, cutoff: str, current_name: str) -> str:
    """submissions formerNames로 컷오프 시점 사명 재구성 (OV-002 — 후신 사명 차단)."""
    p = BIG / f"submissions/CIK{cik}.json"
    j = json.loads(p.read_text(encoding="utf-8"))
    spans = []
    for f in j.get("formerNames", []):
        frm = (f.get("from") or "")[:10]
        to = (f.get("to") or "")[:10]
        if frm and to and frm <= cutoff <= to:
            spans.append((to, f.get("name", "")))
    if spans:
        return min(spans)[1] or current_name  # 컷오프를 덮는 가장 이른 종료 구간
    return current_name


def stage_data(rows) -> None:
    for r in rows:
        cik, tick = r["cik"], (r["tickers"] or ["UNK"])[0].upper()
        r["ticker"] = tick
        x = DATA / tick / "xbrl"
        e = DATA / tick / "edgar"
        x.mkdir(parents=True, exist_ok=True)
        e.mkdir(parents=True, exist_ok=True)
        src_f = BIG / f"facts/CIK{cik}.json"
        if not src_f.exists():
            raise SystemExit(f"companyfacts 캐시 부재: {src_f} — control_v2.py fetch 재실행")
        shutil.copy2(src_f, x / f"CIK{cik}.json")
        subs = sorted(BIG.glob(f"submissions/CIK{cik}*.json"))
        if not subs:
            raise SystemExit(f"submissions 캐시 부재: CIK{cik}")
        for s in subs:
            shutil.copy2(s, e / s.name)
        print(f"  staged {tick} (CIK {cik})")


def build_inputs(rows) -> None:
    import random
    ordered = sorted(rows, key=lambda r: (r["matched_treatment"], r["rank_in_case"]))
    for i, r in enumerate(ordered, 1):
        r["v_id"] = f"V{i:02d}"
    shuffled = list(ordered)
    random.Random(NEUTRAL_ID_SEED_V2).shuffle(shuffled)
    cases, mapping, cands = [], {}, []
    for i, r in enumerate(shuffled, NEUTRAL_ID_START):
        nid = f"case_{i:02d}"
        mapping[nid] = r["v_id"]
        nm = name_at_cutoff(r["cik"], r["cutoff_date"], r["name"])
        cases.append({"case_id": nid, "ticker": r["ticker"],
                      "cik": r["cik"], "company_name": nm,
                      "cutoff_date": r["cutoff_date"]})
        cands.append({"case_id": r["v_id"], "group": "control",
                      "company_name": nm, "ticker": r["ticker"],
                      "cik": r["cik"], "cutoff_date": r["cutoff_date"],
                      "matched_treatment": r["matched_treatment"],
                      "sic": r.get("sic"), "rev_pit": r.get("rev_pit"),
                      "scheme_summary": None, "scheme_type": None,
                      "manipulation_period_start": None, "manipulation_period_end": None})
    CASES_V2_DEST.write_text(json.dumps({"_meta": {
        "contract": "schemas/evaluatee_input.json",
        "generated_by": "tools/run_control_v2_scoring.py (결정론 — seed "
                        f"{NEUTRAL_ID_SEED_V2})",
        "id_convention": f"중립 ID case_{NEUTRAL_ID_START}.. — 동결 16건과 비겹침",
        "name_convention": "컷오프 시점 사명 (formerNames 재구성, OV-002)"},
        "cases": cases}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MAPPING_DEST.write_text(json.dumps({"_meta": {
        "warning": "채점 전용 — 피평가자 노출 금지 (id_mapping.json과 동일 규약)"},
        "mapping": mapping}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    CAND_DEST.write_text(json.dumps({"_meta": {
        "warning": "채점 정답 키 (전원 group=control) — 피평가자 노출 금지",
        "source": "runs/rp09/control_group_v2.json"},
        "candidates": cands}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  inputs: {len(cases)} cases → {CASES_V2_DEST.name}, "
          f"{MAPPING_DEST.name}, {CAND_DEST.name}")


def run(cmd: list) -> None:
    print(f"\n$ {' '.join(cmd)}", flush=True)
    r = subprocess.run(cmd, cwd=REPO)
    if r.returncode != 0:
        raise SystemExit(f"단계 실패 (exit {r.returncode}) — 같은 명령 재실행으로 재개")


def commit_outputs(msg: str, regen_manifest: bool) -> None:
    """단계별 산출물 커밋 — 다음 단계 러너의 clean-tree 가드 충족 + I3 즉시 동결.

    runs/ 아래 산출물은 전역 매니페스트 재생성 후 커밋 (HANDOFF 규칙 — CI (d)).
    """
    if regen_manifest:
        run([sys.executable, "tools/verify_blindness.py", "--write-manifest"])
    subprocess.run(["git", "add", "-A"], cwd=REPO, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO).returncode == 0:
        return  # 변경 없음 (멱등 재실행)
    subprocess.run(["git", "commit", "-q", "-m", msg + "\n\nCo-Authored-By: "
                    "Claude Fable 5 <noreply@anthropic.com>"], cwd=REPO, check=True)
    print(f"  [커밋] {msg}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--plan", action="store_true")
    g.add_argument("--launch", action="store_true")
    args = ap.parse_args()

    rows = selected_controls()
    n = len(rows)
    plan = {
        "controls": n,
        "evaluatee_calls": {"scoring(original)": n, "recognition_probe(perturbed)": n},
        "grader_calls": n,
        "wall_clock_estimate": {
            "scoring": f"~{round(n * 2.2 / 3 * 3)}min (동시성 3, 케이스당 ~6.5min/3)",
            "probes": f"~{round(n * 0.8)}min (동시성 3)",
            "grading": f"~{round(n * 2.5)}min (순차 — 채점자 케이스당 ~2.5min)",
        },
        "outputs": ["runs/rp09/scores/", "scoring/probe_results_v2/recognition/",
                    "scoring/grades_v2/controls/"],
    }
    print(json.dumps(plan, ensure_ascii=False, indent=1))
    if args.plan:
        return 0

    gate = GATE_FILE.read_text(encoding="utf-8") if GATE_FILE.exists() else ""
    if GATE_LINE not in gate:
        print(f"\nBLOCKED — 게이트 미충족: scoring/overrides.md 에 '{GATE_LINE}' "
              f"서명줄이 없습니다. 소유자 §Final 결정(YES) 기록 후 재실행.",
              file=sys.stderr)
        return 4

    print(f"\n[1/5] stage-data ({datetime.datetime.now().isoformat(timespec='seconds')})")
    stage_data(rows)
    print("[2/5] build-inputs")
    build_inputs(rows)
    py = sys.executable
    commit_outputs("RP-10 발사 전 입력 스테이징 (멱등 재생성분)", regen_manifest=False)
    print("[3/5] score")
    run([py, "pipeline/runner.py", "--cases", "data/evaluatee/cases_v2.json",
         "--out", "runs/rp09/scores"])
    commit_outputs("RP-10 Phase 1: 대조군 v2 채점 원시 출력 22 (runs/rp09/scores) — I3 즉시 동결",
                   regen_manifest=True)
    print("[4/5] probes")
    run([py, "pipeline/probe_runner.py", "--recognition",
         "--cases", "data/evaluatee/cases_v2.json",
         "--out-root", "scoring/probe_results_v2"])
    commit_outputs("RP-10 Phase 1: 대조군 v2 인지 프로브 22 (scoring/probe_results_v2)",
                   regen_manifest=False)
    print("[5/5] grade")
    run([py, "scoring/grader_runner.py", "--runs", "runs/rp09/scores",
         "--out", "scoring/grades_v2/controls",
         "--mapping", "scoring/id_mapping_v2.json",
         "--candidates", "data/candidates/candidates_v2_controls.json"])
    commit_outputs("RP-10 Phase 1: 대조군 v2 채점자 출력 22 (scoring/grades_v2/controls)",
                   regen_manifest=False)
    print("\n완료 — 다음: analysis/ (Phase 2 통계)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
