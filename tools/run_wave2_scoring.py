"""Wave-2 채점 런북 — 실험군 9(신규) + 대조군(wave2 선정) 채점·프로브·채점자.

owner가 이 세션에서 발사 승인 (RP-11 §6 재개). 동결 파이프라인 재사용 —
build_payload(유일 look-ahead 필터) / runner / probe_runner / grader_runner 무수정.
I3: 출력은 runs/wave2/ · scoring/*_wave2/ (동결 rp09 경로 불가침).

단계 (전부 멱등):
  1 stage-data  : 대조군 companyfacts/submissions _rp08 캐시 → ~/aaer-data/{T}/ (D23-safe).
                  실험군 9는 이미 ~/aaer-data/{T}/ 스테이지됨.
  2 build-inputs: cases_wave2.json (실험군9+대조군, 중립ID 셔플[블라인드], 파일순=티커
                  알파벳[발사순=시간절단 결과독립], 컷오프 시점 사명) + id_mapping_wave2
                  + candidates_wave2 (정답키: 실험군 group=treatment+scheme, 대조군 control).
  3 score       : runner --cases cases_wave2.json --out runs/wave2/scores
  4 perturb     : runner --only <실험군9> --perturbed --out runs/wave2/perturbed (교란 draw 1회)
  5 probes      : probe_runner --recognition + --verbatim --out-root scoring/probe_results_wave2
  6 grade       : grader_runner --out scoring/grades_wave2 (human_finalized=false)

사용: python3 tools/run_wave2_scoring.py {build|score|perturb|probes|grade|all}
"""
import argparse, json, random, shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BIG = Path.home() / "aaer-data/_rp08"
DATA = Path.home() / "aaer-data"
V2 = REPO / "runs/wave2/control_group_v2.json"
CASES_DEST = REPO / "data/evaluatee/cases_wave2.json"
MAP_DEST = REPO / "scoring/id_mapping_wave2.json"
CAND_DEST = REPO / "data/candidates/candidates_wave2.json"
SEED = 20260707
NEUTRAL_START = 39  # case_01-16 실험 + case_17-38 rp09 대조 뒤 — 비겹침
FRAUDS = {"T02":"CSC","T04":"WFT","T19":"OSIR","T20":"BRX","T22":"TNGO",
          "T23":"HAIN","T24":"CGI","T26":"MDXG","T29":"UAA"}


def _cutoff_name(cik, cutoff, current, subs_paths):
    """컷오프 시점 사명 = formerNames로 재구성 (OV-002 후신 사명 차단)."""
    for p in subs_paths:
        if not p.exists():
            continue
        j = json.loads(p.read_text(encoding="utf-8"))
        spans = []
        for f in j.get("formerNames", []):
            frm, to = (f.get("from") or "")[:10], (f.get("to") or "")[:10]
            if frm and to and frm <= cutoff <= to:
                spans.append((to, f.get("name", "")))
        if spans:
            return min(spans)[1] or current
        # 후신 사명 제거 (n/k/a) — build_evaluatee_inputs 규약 (paren + tail 양형)
        break
    import re
    s = re.sub(r"\s*\(\s*(?:n/k/a|now(?:\s+known\s+as)?)\s+[^)]*\)", "", current, flags=re.I)
    s = re.sub(r"\s*;\s*(?:n/k/a|now(?:\s+known\s+as)?)\s+.*$", "", s, flags=re.I)
    return s.strip()


def fraud_rows():
    cand = {c["case_id"]: c for c in json.loads(
        (REPO/"data/candidates/candidates.json").read_text())["candidates"]}
    rows = []
    for tid, tk in FRAUDS.items():
        c = cand[tid]; cik = c["cik"]
        subs = sorted((DATA/tk/"edgar").glob(f"CIK{cik}*.json")) + \
               sorted((DATA/tk/"edgar").glob(f"CIK{cik.zfill(10)}*.json"))
        nm = _cutoff_name(cik, c["cutoff_date"], c["company_name"], subs)
        rows.append({"stable_id": tid, "group": "treatment", "ticker": tk,
                     "cik": cik, "cutoff_date": c["cutoff_date"], "company_name": nm,
                     "scheme_summary": c.get("scheme_summary"), "scheme_type": c.get("scheme_type"),
                     "manipulation_period_start": c.get("manipulation_period_start"),
                     "manipulation_period_end": c.get("manipulation_period_end"),
                     "matched_treatment": tid, "sic": None, "rev_pit": None})
    return rows


def control_rows():
    v2 = json.loads(V2.read_text(encoding="utf-8"))
    rows, vi = [], 0
    for tid in sorted(v2["selections"]):
        sel = v2["selections"][tid]
        for s in sel["selected"]:
            vi += 1
            tk = (s.get("tickers") or ["UNK"])[0].upper()
            cutoff = sel["treatment"]["cutoff"]
            subs = sorted(BIG.glob(f"submissions/CIK{s['cik']}*.json"))
            nm = _cutoff_name(s["cik"], cutoff, s.get("name") or "", subs)
            rows.append({"stable_id": f"W{vi:02d}", "group": "control", "ticker": tk,
                         "cik": s["cik"], "cutoff_date": cutoff,
                         "company_name": nm,
                         "scheme_summary": None, "scheme_type": None,
                         "manipulation_period_start": None, "manipulation_period_end": None,
                         "matched_treatment": tid, "sic": s.get("sic"), "rev_pit": s.get("rev_pit")})
    return rows


def stage_controls(rows):
    for r in rows:
        cik, tk = r["cik"], r["ticker"]
        x, e = DATA/tk/"xbrl", DATA/tk/"edgar"
        x.mkdir(parents=True, exist_ok=True); e.mkdir(parents=True, exist_ok=True)
        src = BIG/f"facts/CIK{cik}.json"
        if not src.exists():
            raise SystemExit(f"companyfacts 캐시 부재: {src}")
        dst = x/f"CIK{cik}.json"
        if not dst.exists():  # D23: 기존 동결 아카이브 덮어쓰기 금지
            shutil.copy2(src, dst)
        subs = sorted(BIG.glob(f"submissions/CIK{cik}*.json"))
        if not subs:
            raise SystemExit(f"submissions 캐시 부재: CIK{cik}")
        for s in subs:
            if not (e/s.name).exists():
                shutil.copy2(s, e/s.name)


def build_inputs():
    frauds, controls = fraud_rows(), control_rows()
    stage_controls(controls)
    allrows = frauds + controls
    # 파일 순서 = 티커 알파벳 (발사순 = 시간절단 결과독립, ANALYSIS_PLAN_WAVE2 §7)
    allrows.sort(key=lambda r: r["ticker"])
    # 중립 ID = 셔플 풀 (블라인드 — case 번호가 그룹/순서를 인코딩하지 않음)
    ids = list(range(NEUTRAL_START, NEUTRAL_START + len(allrows)))
    random.Random(SEED).shuffle(ids)
    cases, mapping, cands = [], {}, []
    for r, num in zip(allrows, ids):
        nid = f"case_{num:02d}"
        mapping[nid] = r["stable_id"]
        cases.append({"case_id": nid, "ticker": r["ticker"], "cik": r["cik"],
                      "company_name": r["company_name"], "cutoff_date": r["cutoff_date"]})
        cands.append({"case_id": r["stable_id"], "group": r["group"],
                      "company_name": r["company_name"], "ticker": r["ticker"], "cik": r["cik"],
                      "cutoff_date": r["cutoff_date"], "matched_treatment": r["matched_treatment"],
                      "sic": r["sic"], "rev_pit": r["rev_pit"],
                      "scheme_summary": r["scheme_summary"], "scheme_type": r["scheme_type"],
                      "manipulation_period_start": r["manipulation_period_start"],
                      "manipulation_period_end": r["manipulation_period_end"]})
    CASES_DEST.write_text(json.dumps({"_meta": {
        "contract": "schemas/evaluatee_input.json",
        "generated_by": f"tools/run_wave2_scoring.py (결정론 seed {SEED})",
        "id_convention": f"중립 ID case_{NEUTRAL_START}.. 셔플 — 동결 1-38과 비겹침",
        "order_convention": "파일 순서 = 티커 알파벳 (발사순 = 시간절단 결과독립)",
        "name_convention": "컷오프 시점 사명 (formerNames/후신 제거)"},
        "cases": cases}, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    MAP_DEST.write_text(json.dumps({"_meta": {"warning": "채점 전용 — 피평가자 노출 금지"},
        "mapping": mapping}, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    CAND_DEST.write_text(json.dumps({"_meta": {
        "warning": "채점 정답 키 — 피평가자 노출 금지", "source": "runs/wave2/control_group_v2.json + candidates.json"},
        "candidates": cands}, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    fraud_ids = [c["case_id"] for c in cases if mapping[c["case_id"]] in FRAUDS]
    (REPO/"runs/wave2").mkdir(parents=True, exist_ok=True)
    (REPO/"runs/wave2/fraud_case_ids.json").write_text(json.dumps(sorted(fraud_ids)))
    print(f"  build: {len(frauds)} frauds + {len(controls)} controls = {len(cases)} cases "
          f"→ {CASES_DEST.name}; fraud ids={sorted(fraud_ids)}")


def run(cmd):
    print(f"\n$ {' '.join(cmd)}", flush=True)
    r = subprocess.run(cmd, cwd=REPO)
    # 0 = 전건 OK · 2 = 일부 케이스 FAIL(재시도 후) = INCOMPLETE 허용, 계속 진행
    # (사전 고정 알파벳 순서라 결과 독립) · 3 = 레이트 리밋 → 중단·재개
    if r.returncode == 2:
        print(f"  ⚠ 일부 케이스 FAIL (exit 2) — INCOMPLETE 표기, 다음 단계 진행", flush=True)
        return
    if r.returncode not in (0,):
        raise SystemExit(f"단계 exit {r.returncode} (레이트리밋/오류) — 같은 명령 재실행으로 재개")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["build","score","perturb","probes","grade","all"])
    a = ap.parse_args()
    py = sys.executable
    if a.stage in ("build","all"):
        build_inputs()
    if a.stage in ("score","all"):
        run([py,"pipeline/runner.py","--cases","data/evaluatee/cases_wave2.json","--out","runs/wave2/scores"])
    if a.stage in ("perturb","all"):
        fids = json.loads((REPO/"runs/wave2/fraud_case_ids.json").read_text())
        run([py,"pipeline/runner.py","--cases","data/evaluatee/cases_wave2.json",
             "--only",*fids,"--perturbed","--out","runs/wave2/perturbed"])
    if a.stage in ("probes","all"):
        for kind in ("--recognition","--verbatim"):
            run([py,"pipeline/probe_runner.py",kind,"--cases","data/evaluatee/cases_wave2.json",
                 "--out-root","scoring/probe_results_wave2"])
    if a.stage in ("grade","all"):
        run([py,"scoring/grader_runner.py","--runs","runs/wave2/scores","--out","scoring/grades_wave2",
             "--mapping","scoring/id_mapping_wave2.json","--candidates","data/candidates/candidates_wave2.json"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
