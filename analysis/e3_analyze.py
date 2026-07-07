"""E3 분석 — wave-2 교란 재추첨 dominance 재계산 (결정론). `python analysis/e3_analyze.py`.

동결 R3 정의(`wave2_analyze.py`) 그대로 재사용 — 재해석 금지:
  delta = fr[s] − pt[s] · contrib = 0.5(fr[s] − cmed) · cross iff abs(delta)≥contrib or contrib≤0.
  dominance fires iff cross ≥ 5 of 9.
identity(fr)·control median(cmed)은 동결 main 점수. pt = draw별 교란 점수.
median-delta: 케이스별 median(pt1,pt2,pt3) → delta → cross.
결론 규칙(사전 등록 W2_PERTURB_REDRAW_PLAN §3): median-dominance ≥5/9 → R3가 R4
supersede; ≤4/9 → R4 유지 + 안정성 밴드.
출력: analysis/e3_results.json.
"""
import json
import statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FRAUDS = ["case_39", "case_40", "case_52", "case_59", "case_60", "case_61",
          "case_65", "case_66", "case_67"]


def load_p(path):
    p = REPO / path
    return json.load(open(p, encoding="utf-8"))["misstatement_probability"] if p.exists() else None


def main():
    idmap = json.load(open(REPO / "scoring/id_mapping_wave2.json", encoding="utf-8"))["mapping"]
    allcases = list(idmap)
    ctrl = [load_p(f"runs/wave2/scores/{c}.json") for c in allcases if c not in FRAUDS]
    cmed = st.median(ctrl)

    fr, draws = {}, {1: {}, 2: {}, 3: {}}
    for c in FRAUDS:
        fr[c] = load_p(f"runs/wave2/scores/{c}.json")
        draws[1][c] = load_p(f"runs/wave2/perturbed/{c}.json")
        draws[2][c] = load_p(f"runs/wave2/perturbed_redraw/draw_2/{c}.json")
        draws[3][c] = load_p(f"runs/wave2/perturbed_redraw/draw_3/{c}.json")

    def crossed(pt):
        cs = []
        for c in FRAUDS:
            if pt.get(c) is None:
                continue
            delta = fr[c] - pt[c]
            contrib = 0.5 * (fr[c] - cmed)
            if abs(delta) >= contrib or contrib <= 0:
                cs.append(idmap[c])
        return cs

    per_draw = {}
    for d in (1, 2, 3):
        if all(draws[d].get(c) is not None for c in FRAUDS):
            cs = crossed(draws[d])
            per_draw[f"draw_{d}"] = {"crossed": len(cs), "cases": cs, "fires_R3": len(cs) >= 5}

    # median-delta (draw별 존재분만; 최소 draw-1+2)
    median_pt, sigma = {}, {}
    ready = [d for d in (1, 2, 3) if all(draws[d].get(c) is not None for c in FRAUDS)]
    for c in FRAUDS:
        vals = [draws[d][c] for d in ready]
        median_pt[c] = st.median(vals)
        sigma[c] = round(st.pstdev(vals), 1) if len(vals) > 1 else 0.0
    med_cross = crossed(median_pt)
    med_fires = len(med_cross) >= 5

    verdict = ("R3 supersedes R4 (median-dominance ≥5/9) — 모든 드래프트 갱신 필요"
               if med_fires else
               "R4 유지 (median-dominance ≤4/9) + 재추첨 안정성 밴드 보고")

    out = {
        "draws_used": ready,
        "control_median_cmed": cmed,
        "identity_scores_fr": {idmap[c]: fr[c] for c in FRAUDS},
        "perturbed_by_draw": {f"draw_{d}": {idmap[c]: draws[d].get(c) for c in FRAUDS}
                              for d in (1, 2, 3)},
        "per_draw_dominance": per_draw,
        "median_perturbed": {idmap[c]: median_pt[c] for c in FRAUDS},
        "per_case_sigma_pp": {idmap[c]: sigma[c] for c in FRAUDS},
        "median_delta_dominance": {"crossed": len(med_cross), "cases": med_cross,
                                   "fires_R3": med_fires, "n": 9},
        "mean_sigma_pp": round(st.mean(sigma.values()), 1),
        "conclusion_rule": "median-dominance ≥5/9 → R3 supersede; ≤4/9 → R4 (W2_PERTURB_REDRAW_PLAN §3)",
        "verdict": verdict,
        "note": ("점수 기반 재계산, 채점자 0. identity·cmed 동결 main. wave-1 draw σ≈12pp 참조 "
                 "— per-case σ 밴드 병기. draw-1 published 불변(E3=안정성/규칙 재판정)."),
    }
    (REPO / "analysis/e3_results.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"draws_used={ready} | per-draw dominance="
          f"{ {k: v['crossed'] for k, v in per_draw.items()} } | "
          f"median-delta dominance={len(med_cross)}/9 fires_R3={med_fires} | mean σ={out['mean_sigma_pp']}pp")
    print("VERDICT:", verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
