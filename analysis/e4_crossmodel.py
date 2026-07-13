"""E4 교차모델 분석 (analysis/CROSSMODEL_PLAN.md §3, EXPLORATORY) — 무호출·결정론.

지표 (사전 지정): Spearman 순위 상관 · 플래그(p>=50) 일치율 + Cohen's κ ·
per-case 표 + 불일치 열거. 주장 상한: "두 Claude 모델의 순위가 얼마나
겹치는가" — 성능 비교·벤치마크 금지, truth 없음 (둘 다 피평가자).

입력: runs/e4/scores/ (opus-4-8) + 동결 원 채점 (sonnet-5, 재계산 0):
      runs/holdout/scores · runs/holdout/controls/scores · runs/wave2/scores
출력: analysis/e4_crossmodel.json + analysis/E4_CROSSMODEL.md (EXPLORATORY 배너)
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
import stats  # noqa: E402 (동결 spearman)

FLAG = 50
BASE_DIRS = {  # 동결 draw-1 원 채점 위치 (전 18건 original 프레임)
    "case_71": "runs/holdout/scores", "case_72": "runs/holdout/scores",
    "case_73": "runs/holdout/scores",
    **{cid: "runs/wave2/scores" for cid in
       ("case_44", "case_49", "case_52", "case_60", "case_61", "case_65")},
    **{f"hc_{i:02d}": "runs/holdout/controls/scores" for i in range(1, 10)},
}
GROUPS = {"case_71": "holdout", "case_72": "holdout", "case_73": "holdout",
          **{c: "wave2" for c in ("case_44", "case_49", "case_52",
                                  "case_60", "case_61", "case_65")},
          **{f"hc_{i:02d}": "e1_control" for i in range(1, 10)}}


def cohen_kappa(pairs: list[tuple[bool, bool]]) -> float | None:
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    pa = sum(a for a, _ in pairs) / n
    pb = sum(b for _, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else round((po - pe) / (1 - pe), 4)


def main() -> int:
    rows = []
    for cid, base_dir in sorted(BASE_DIRS.items()):
        a = json.loads((REPO / base_dir / f"{cid}.json").read_text(encoding="utf-8"))
        bp = REPO / "runs" / "e4" / "scores" / f"{cid}.json"
        if not bp.is_file():
            raise SystemExit(f"{cid}: E4 출력 부재 — 러너 미완 (분석 보류)")
        b = json.loads(bp.read_text(encoding="utf-8"))
        rows.append({"case_id": cid, "group": GROUPS[cid],
                     "p_sonnet5": a["misstatement_probability"],
                     "p_opus48": b["misstatement_probability"],
                     "model_served_e4": b.get("model"),
                     "flag_sonnet5": a["misstatement_probability"] >= FLAG,
                     "flag_opus48": b["misstatement_probability"] >= FLAG})
    xs = [r["p_sonnet5"] for r in rows]
    ys = [r["p_opus48"] for r in rows]
    rho = round(stats.spearman(xs, ys), 4)
    pairs = [(r["flag_sonnet5"], r["flag_opus48"]) for r in rows]
    agree = sum(a == b for a, b in pairs)
    kappa = cohen_kappa(pairs)
    disagreements = [r["case_id"] for r in rows if r["flag_sonnet5"] != r["flag_opus48"]]
    out = {"label": "EXPLORATORY — 각주 전용, 헤드라인 금지 (CROSSMODEL_PLAN §6)",
           "n": len(rows), "spearman_rho": rho,
           "flag_agreement": f"{agree}/{len(rows)}",
           "cohen_kappa": kappa, "flag_threshold": FLAG,
           "disagreement_cases": disagreements, "rows": rows,
           "claim_ceiling": ("'두 Claude 모델(claude-sonnet-5 vs claude-opus-4-8)의 "
                             "순위가 얼마나 겹치는가' 이상 주장 금지 — truth 없음, "
                             "N=18 단일 프롬프트 (PLAN §3)")}
    (REPO / "analysis" / "e4_crossmodel.json").write_text(
        json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
        encoding="utf-8")
    md = ["# E4 교차모델 점검 — **EXPLORATORY** (각주 전용, 발행 금지 게이트)", "",
          "> 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).",
          "> 성능 비교·벤치마크 아님 — 순위 중첩도 측정만 (CROSSMODEL_PLAN §0/§3).", "",
          f"- N = {len(rows)} (홀드아웃 3 + wave-2 6 + E1 대조군 9) · 프레임 = 원 채점 동일(original)",
          f"- **Spearman ρ = {rho}** · 플래그(p≥{FLAG}) 일치 {agree}/{len(rows)}"
          f" · Cohen κ = {kappa}",
          f"- 불일치 케이스: {', '.join(disagreements) or '없음'}", "",
          "| case | group | sonnet-5 p | opus-4-8 p | flag 일치 |", "|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['case_id']} | {r['group']} | {r['p_sonnet5']} | "
                  f"{r['p_opus48']} | {'✓' if r['flag_sonnet5'] == r['flag_opus48'] else '✗'} |")
    (REPO / "analysis" / "E4_CROSSMODEL.md").write_text("\n".join(md) + "\n",
                                                        encoding="utf-8")
    print(f"E4: ρ={rho} · flag {agree}/{len(rows)} · κ={kappa} → analysis/e4_crossmodel.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
