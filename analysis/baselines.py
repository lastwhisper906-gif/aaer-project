"""RP-10 Phase 2.1: 동일 30사 기계 기준선 — Beneish M / Dechow F (PIT).

기존 동결 구현(scoring/baselines/screens.py — PIT: filed<=cutoff, 최신 filed 승리,
결측 침묵 대체 금지)을 30사 전체에 재사용한다. §8-6 허용 결정론 공식.

출력: analysis/baseline_table.csv (사별 1행: LLM 점수·M·F·그룹) +
      analysis/baseline_details.json (결측 비율·사유 전수)
사용: python analysis/baselines.py   (결정론 — 네트워크 없음)
"""
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scoring/baselines"))
from screens import run_case  # noqa: E402 (동결 PIT 구현 재사용)

TREAT_IDS = ["T07", "T11", "T12", "T13", "T16", "T17", "T21", "T28"]


def llm_scores() -> dict:
    """원본 프레임 LLM 점수 (1차) + 교란 실험군 점수 (2차 프레임용)."""
    out = {}
    m1 = json.loads((REPO / "scoring/id_mapping.json").read_text())["mapping"]
    for p in sorted((REPO / "runs/main").glob("case_*.json")):
        j = json.loads(p.read_text())
        out[m1[j["case_id"]]] = {"llm_original": j["misstatement_probability"]}
    for p in sorted((REPO / "runs/perturbed").glob("case_*.json")):
        j = json.loads(p.read_text())
        out[m1[j["case_id"]]]["llm_perturbed"] = j["misstatement_probability"]
    m2p = REPO / "scoring/id_mapping_v2.json"
    if m2p.exists():
        m2 = json.loads(m2p.read_text())["mapping"]
        for p in sorted((REPO / "runs/rp09/scores").glob("case_*.json")):
            j = json.loads(p.read_text())
            out[m2[j["case_id"]]] = {"llm_original": j["misstatement_probability"]}
    return out


def main() -> int:
    cands = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates.json").read_text())["candidates"]}
    firms = [dict(cands[t], group="fraud") for t in TREAT_IDS]
    v2 = json.loads((REPO / "data/candidates/candidates_v2_controls.json").read_text())
    firms += [dict(c, group="control") for c in v2["candidates"]]
    assert len(firms) == 30, len(firms)

    scores = llm_scores()
    rows, details = [], {}
    for c in firms:
        cid = c["case_id"]
        r = run_case(c)
        b, f = r.get("beneish", {}), r.get("dechow_f", {})
        details[cid] = {
            "ticker": r["ticker"], "error": r.get("error"),
            "beneish_missing": b.get("missing"), "dechow_missing": f.get("missing"),
            "notes": r.get("notes"), "fye_used": r.get("fiscal_year_ends_used"),
        }
        llm = scores.get(cid, {})
        rows.append({
            "case_id": cid, "ticker": r["ticker"], "group": c["group"],
            "llm_score": llm.get("llm_original"),
            "llm_perturbed": llm.get("llm_perturbed"),
            "m_score": b.get("m_score"),
            "m_flag_-1.78": b.get("flag_minus_1_78"),
            "m_flag_-2.22": b.get("flag_minus_2_22"),
            "f_score": f.get("f_score"), "f_flag_1": f.get("flag_1_0"),
            "m_missing_n": len(b.get("missing") or []),
            "f_missing_n": len(f.get("missing") or []),
        })
        print(f"{cid} {r['ticker']:5s} {c['group']:7s} LLM={llm.get('llm_original')} "
              f"M={b.get('m_score') and round(b['m_score'], 2)} "
              f"F={f.get('f_score') and round(f['f_score'], 2)}")

    out = REPO / "analysis/baseline_table.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    (REPO / "analysis/baseline_details.json").write_text(
        json.dumps(details, ensure_ascii=False, indent=1), encoding="utf-8")
    n_m = sum(1 for r in rows if r["m_score"] is not None)
    n_f = sum(1 for r in rows if r["f_score"] is not None)
    print(f"\n→ {out} (M 계산가능 {n_m}/30, F {n_f}/30 — 결측 사유는 details)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
