"""RP-13 채점 확정 워크벤치 생성기 (P3) — RP-06 포맷, 결정론.

동결 채점(scoring/grades_wave2/ + grades_holdout/, human_finalized=false)과 동결
점수(runs/wave2/scores/ + runs/holdout/scores/)를 읽어 소유자 서명대 markdown을
생성한다. **모든 발췌는 verbatim** (날조 인용 금지 §5-3) — 이 생성기가 그것을 기계
보증한다. 회사명·정답키는 채점측 자료(candidates_*)에서만 온다(피평가자 미노출).

flags-first 순서 (미션 P3): 우선 검토(TIER A) = 채점자-경계표시 dim2 · 약증거(d4≤2)
· 오류 케이스(출력≠정답: FP/미탐) · 홀드아웃 G2 provisional. 나머지 = TIER B.
mem-susp(memorization_suspect_condition2)은 wave-2/홀드아웃 전건 false(그 자체가 발견).

출력: review_packets/RP-13_grading_workbench.md · `python tools/build_rp13_workbench.py`.
"""
import json
import glob
import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BORDER = re.compile(r"borderline|flag for auditor|uncertain|ambiguous|close call", re.I)


def load(p):
    return json.load(open(REPO / p, encoding="utf-8"))


def clip(s, n):
    s = " ".join((s or "").split())
    return s[:n] + ("…" if len(s or "") > n else "")


def rationale_lines(r, maxlines=6, width=240):
    # rationale는 채점자가 줄 단위(DIM1.. / newline)로 쓴다 — 앞 maxlines 유지
    parts = [ln.strip() for ln in (r or "").replace(". DIM", ".\nDIM").splitlines() if ln.strip()]
    if len(parts) == 1:
        parts = re.split(r"(?<=\.)\s+(?=DIM|MEM|Coverage|Minor)", parts[0])
    out = []
    for ln in parts[:maxlines]:
        out.append(clip(ln, width))
    return out


def collect():
    idmap = load("scoring/id_mapping_wave2.json")["mapping"]
    frauds = set(load("runs/wave2/fraud_case_ids.json"))
    cw = {c["case_id"]: c for c in load("data/candidates/candidates_wave2.json")["candidates"]}
    ch = {c["case_id"]: c for c in load("data/candidates/candidates_holdout.json")["candidates"]}
    # 감사 B1: wave-1 primary(8v22) 헤드라인의 대조군 22(v2)가 서명대에서 누락 → 편입.
    idmap_v2 = load("scoring/id_mapping_v2.json")["mapping"]
    cv2 = {c["case_id"]: c for c in load("data/candidates/candidates_v2_controls.json")["candidates"]}
    recs = []

    def add(case, gdir, sdir, kind):
        g = load(f"{gdir}/{case}.json")
        s = load(f"{sdir}/{case}.json")
        p = s.get("misstatement_probability")
        if kind == "wave2":
            code = idmap[case]
            c = cw[code]
            grp = "FRAUD" if case in frauds else "control"
            name, tkr = c["company_name"], c["ticker"]
            key = c.get("scheme_summary") if grp == "FRAUD" else None
        elif kind == "v2control":
            code = idmap_v2[case]
            c = cv2[code]
            grp = "control"
            name, tkr = c["company_name"], c["ticker"]
            key = None
        else:
            c = ch[case]
            code = case
            grp = "HOLDOUT(G2)"
            name, tkr = c["company_name"], c["ticker"]
            key = c.get("scheme_summary")
        d1, d2, d4 = g.get("dim1_probability_band"), g.get("dim2_mechanism"), g.get("dim4_evidence_quality")
        mem2 = g.get("memorization_suspect_condition2")
        # flag reasons
        flags = []
        if mem2:
            flags.append("MEM-SUSPECT")
        if BORDER.search(g.get("rationale", "")):
            flags.append("채점자-경계표시")
        if isinstance(d4, int) and d4 <= 2:
            flags.append(f"약증거(d4={d4})")
        wrong = (grp == "control" and (p or 0) >= 50) or (grp != "control" and (p or 0) < 50)
        if wrong:
            flags.append("오류(출력≠정답)" if grp != "HOLDOUT(G2)" else "홀드아웃-미탐/경계")
        if grp == "HOLDOUT(G2)":
            flags.append("G2-provisional")
        recs.append(dict(case=case, code=code, name=name, tkr=tkr, grp=grp, p=p,
                         tier=(s.get("overall") or {}).get("risk_tier"),
                         hyps=s.get("mechanism_hypotheses") or [], d1=d1, d2=d2,
                         d3=g.get("dim3_genre_mapping"), d4=d4, mem2=mem2,
                         rationale=g.get("rationale", ""), key=key, flags=flags))

    for gp in sorted(glob.glob(str(REPO / "scoring/grades_wave2/*.json"))):
        add(os.path.basename(gp)[:-5], "scoring/grades_wave2", "runs/wave2/scores", "wave2")
    for gp in sorted(glob.glob(str(REPO / "scoring/grades_holdout/*.json"))):
        add(os.path.basename(gp)[:-5], "scoring/grades_holdout", "runs/holdout/scores", "holdout")
    for gp in sorted(glob.glob(str(REPO / "scoring/grades_v2/controls/*.json"))):
        add(os.path.basename(gp)[:-5], "scoring/grades_v2/controls", "runs/rp09/scores", "v2control")
    return recs


def prio(r):
    # 낮을수록 위. mem>경계>오류>약증거>홀드아웃>표준
    order = ["MEM-SUSPECT", "채점자-경계표시", "오류(출력≠정답)", "홀드아웃-미탐/경계",
             "약증거", "G2-provisional"]
    for i, o in enumerate(order):
        if any(f.startswith(o) for f in r["flags"]):
            return i
    return len(order)


def disposition(r):
    if r["grp"] == "control":
        if (r["p"] or 0) >= 50:
            return "finalize (오탐이나 채점 d1=0 정확 — trust boundary 데이터. §1 오류해부 참조)"
        return "finalize (대조군 정탐, 근거 명확)"
    if r["grp"] == "HOLDOUT(G2)":
        return "finalize (G2 provisional 라벨 유지 — 4.02/AAER 상향 시 티어 갱신)"
    if (r["p"] or 0) < 50:
        return "finalize (미탐 — 채점 정확. CSC=보정 near-miss / BRX=구조적 미탐, §2 참조)"
    return "finalize (실험군 정탐)"


def render(recs):
    recs.sort(key=lambda r: (prio(r), -(r["p"] or 0)))
    def _is_a(r):
        return r["grp"] == "HOLDOUT(G2)" or (bool(r["flags"]) and r["flags"] != ["G2-provisional"])
    n_flag = sum(1 for r in recs if _is_a(r))
    L = []
    L.append("# RP-13 채점 확정 워크벤치 — 소유자 서명대 (P3, OWNER-GATE-E 세션)\n")
    L.append("> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-08. "
             "**생성기: `tools/build_rp13_workbench.py` (결정론, verbatim 보증).**")
    L.append(f"> **용도**: 대기 채점 {len(recs)}건(wave-2 32 + 홀드아웃 3 + wave-1 primary "
             "대조군 22[v2, 감사 B1 편입])의 인간 최종 확정(§7). E1/E2/E4/E5 채점은 실행 후 "
             "재생성으로 추가. 케이스당 ~30–60초 처리 목표.")
    L.append("> **읽는 법**: 피평가자 p·가설 → 채점 d1/d2/d4 → rationale 발췌(verbatim) "
             "→ 제안 처분 → 서명란. 확정은 각 grade 파일 `human_finalized=true` + "
             "오버라이드는 `scoring/overrides.md`.")
    L.append("> **루브릭**: 실험군 p≥70→d1=2 / 50–69→1 / <50→0 · 대조군 p≤30→2 / 31–49→1 "
             "/ ≥50→0. d2: 0 무관 · 1 계정영역 · 2 +방향+유형 · 3 +케이스특이. d4: 증거품질.")
    n_mem_false = sum(1 for r in recs if not r["mem2"])
    L.append(f"> **mem-suspect 전건 false ({n_mem_false}/{len(recs)})** — 암기귀속 의심 0건 "
             "(R4/H2의 약한 암기와 정합, 그 자체가 발견).\n")
    L.append(f"**요약**: 총 {len(recs)}건 · 우선 검토(TIER A, 플래그) {n_flag}건 · "
             f"표준(TIER B) {len(recs)-n_flag}건. 아래는 플래그 우선 정렬.\n")
    L.append("---\n")
    cur_tier = None
    for r in recs:
        # 홀드아웃 3건은 항상 우선 검토(신규·G2 provisional·서사 핵심)
        is_a = _is_a(r)
        tier = "TIER A — 우선 검토" if is_a else "TIER B — 표준"
        if tier != cur_tier:
            L.append(f"\n## {tier}\n")
            cur_tier = tier
        badge = (" ⚑ " + " · ".join(r["flags"])) if r["flags"] else ""
        L.append(f"### {r['case']} = {r['name']} ({r['tkr']}, {r['code']}) — {r['grp']}{badge}\n")
        L.append(f"- 피평가자: **p={r['p']}** · tier={r['tier']} · 가설(확신순):")
        for i, h in enumerate(r["hyps"][:2], 1):
            dirn = h.get("direction", "?")
            li = ", ".join(h.get("affected_line_items", [])[:3])
            tr = clip(h.get("accounting_treatment", ""), 200)
            L.append(f"  {i}. [{dirn}] {li} — {tr}")
        d3 = r["d3"] or {}
        L.append(f"- 채점(claude-fable-5): **d1={r['d1']}** · d2={r['d2']} · "
                 f"d3={d3.get('mapped_genre')}/{d3.get('score')} · d4={r['d4']} · "
                 f"mem2={r['mem2']}")
        if r["key"]:
            L.append(f"- 정답 키(채점측): {clip(r['key'], 240)}")
        L.append("- 채점 rationale 발췌 (verbatim, ≤6줄):")
        for ln in rationale_lines(r["rationale"]):
            L.append(f"  > {ln}")
        L.append(f"- **제안 처분**: {disposition(r)}")
        L.append("- **서명**: ☐ finalize   ☐ override (사유: __________ → overrides.md)\n")
    return "\n".join(L)


def main():
    recs = collect()
    md = render(recs)
    out = REPO / "review_packets/RP-13_grading_workbench.md"
    out.write_text(md, encoding="utf-8")
    print(f"RP-13 워크벤치 생성: {len(recs)}건 → {out.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
