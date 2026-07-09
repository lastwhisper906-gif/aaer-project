"""wave-2 outcome-recognition 결정론 분석 (OUTCOME_RECOGNITION_PLAN §3 — 무분기).

입력: runs/wave2/outcome_recognition/{TICKER}.json (32사, knows_event) +
      data/candidates/candidates_wave2.json (roster) +
      analysis/unified_table.csv (동결 name-ID `recognized` 열)
출력: analysis/outcome_recognition_results.json —
      그룹별 인지율 + Clopper-Pearson 95% CI + name-ID 4분면 reconcile.
어떤 임계도 R/H 판정을 변경하지 않는다 (branchless — §1).
"""
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
from holdout_controls_analyze import clopper_pearson  # noqa: E402 (동결 CP 재사용)

RUN_DIR = REPO / "runs/wave2/outcome_recognition"
OUT = REPO / "analysis/outcome_recognition_results.json"


def roster():
    d = json.loads((REPO / "data/candidates/candidates_wave2.json").read_text(encoding="utf-8"))
    rows = [c for c in d["candidates"] if c.get("case_id", "").startswith(("T", "W"))]
    w2_tickers = {r["ticker"] for r in csv.DictReader(
        open(REPO / "analysis/unified_table.csv", encoding="utf-8")) if r["wave"] == "wave2"}
    return sorted([c for c in rows if c["ticker"] in w2_tickers],
                  key=lambda c: c["ticker"])


def name_id_flags():
    return {r["ticker"]: r["recognized"] == "True"
            for r in csv.DictReader(open(REPO / "analysis/unified_table.csv", encoding="utf-8"))
            if r["wave"] == "wave2"}


def main() -> int:
    ros = roster()
    if len(ros) != 32:
        print(f"FAIL — roster 32 기대, {len(ros)} 발견"); return 1
    missing = [c["ticker"] for c in ros if not (RUN_DIR / f"{c['ticker']}.json").exists()]
    if missing:
        print(f"FAIL — transcript 미완 {len(missing)}: {missing} (판정은 전량 존재 시에만)")
        return 1

    nid = name_id_flags()
    per, groups = [], {"treatment": [], "control": []}
    for c in ros:
        t = c["ticker"]
        rec = json.loads((RUN_DIR / f"{t}.json").read_text(encoding="utf-8"))
        ke = bool(rec["knows_event"])
        grp = "treatment" if c["group"] in ("treatment", "fraud") else "control"
        groups[grp].append(ke)
        per.append({"ticker": t, "case_id": c["case_id"], "group": grp,
                    "knows_event": ke, "confidence": rec.get("confidence"),
                    "name_id_recognized_frozen": nid.get(t)})

    result = {"plan": "analysis/OUTCOME_RECOGNITION_PLAN.md (D34)",
              "branchless": "R/H 판정 입력 아님 — 병기 전용",
              "per_company": per, "rates": {}, "reconcile": {}}
    for g, vals in groups.items():
        k, n = sum(vals), len(vals)
        lo, hi = clopper_pearson(k, n)
        result["rates"][g] = {"knows_event_true": k, "n": n,
                              "rate": round(k / n, 4),
                              "cp95": [round(lo, 4), round(hi, 4)]}
    quad = {"both": [], "name_only": [], "event_only": [], "neither": []}
    for p in per:
        key = ("both" if p["name_id_recognized_frozen"] and p["knows_event"]
               else "name_only" if p["name_id_recognized_frozen"]
               else "event_only" if p["knows_event"] else "neither")
        quad[key].append(p["ticker"])
    result["reconcile"] = {k: {"n": len(v), "tickers": v} for k, v in quad.items()}
    result["reconcile"]["note"] = (
        "name-ID는 익명 페이로드에서 이름 지목(동결 name_match) — 대리 지표; "
        "knows_event는 실명 노출 하 사건 인지 — 직접 지표. event_only = 이름은 "
        "페이로드에서 상기 불능이나 사건은 아는 케이스 (name-ID의 거짓음성 방향 실증).")

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for g in ("treatment", "control"):
        r = result["rates"][g]
        print(f"{g}: knows_event {r['knows_event_true']}/{r['n']} = {r['rate']:.1%} "
              f"CP95 [{r['cp95'][0]:.1%}, {r['cp95'][1]:.1%}]")
    print("reconcile:", {k: v["n"] for k, v in result["reconcile"].items() if k != "note"})
    return 0


if __name__ == "__main__":
    sys.exit(main())
