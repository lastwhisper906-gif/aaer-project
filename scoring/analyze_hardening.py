"""RP-06 A1/A3 결정론 분석 — post-hoc robustness analysis quantifying L-3.

RP-05 §1 사전 등록 판정은 불변(IMMUTABLE) — 이 스크립트는 그것을 재계산하지
않고, 그 판정에 부여할 **신뢰도**를 정량화한다 (소유자 지시 addendum RP-06).

- A1: 인지 프로브 재추첨(draw 2, runs/hardening/probe_recognition) 판정 —
  frozen probe_verdict.name_match 규칙 그대로 적용, draw 1
  (scoring/probe_results/recognition, 읽기 전용)과 병기.
- A3: k=5 표본 분산 — draw 1 = 본 분석 입력(교란 T8 + 원본 C8, J14 비대칭),
  draw 2~5 = runs/hardening/draws/draw_N/. 케이스별 mean·σ·min–max,
  실패 테스트 통계(p·분리·AUC)의 draw별 분포 + 케이스별 중위값 기준 재계산,
  RP-05 §3 delta와 표본 σ의 분해 대조.

출력: scoring/rp06_hardening_stats.json (+stdout 표).
tools/reproduce_analysis.py가 이 파일 스키마(per_draw_stats,
median_of_draws_stats, per_case{mean,sd})를 재계산 대조한다.

사용: python scoring/analyze_hardening.py
"""
from __future__ import annotations

import itertools
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scoring"))
from probe_verdict import name_match  # noqa: E402  (frozen 판정 규칙 재사용)

mapping = json.loads((REPO / "scoring/id_mapping.json").read_text(encoding="utf-8"))["mapping"]
cands = {c["case_id"]: c for c in json.loads(
    (REPO / "data/candidates/candidates.json").read_text(encoding="utf-8"))["candidates"]}
treat = sorted(n for n, o in mapping.items() if o.startswith("T"))
ctrl = sorted(n for n, o in mapping.items() if o.startswith("C"))
pert_cases = {c["case_id"]: c for c in json.loads(
    (REPO / "scoring/perturbed_cases.json").read_text(encoding="utf-8"))["cases"]}


def midranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def mann_whitney_exact(t_vals, c_vals):
    pooled = list(t_vals) + list(c_vals)
    ranks = midranks(pooled)
    n_t = len(t_vals)
    obs = sum(ranks[:n_t])
    count = total = 0
    for combo in itertools.combinations(range(len(pooled)), n_t):
        total += 1
        if sum(ranks[i] for i in combo) >= obs - 1e-9:
            count += 1
    return count / total, (obs - n_t * (n_t + 1) / 2) / (n_t * len(c_vals))


def stats_block(t_vals, c_vals):
    p, auc = mann_whitney_exact(t_vals, c_vals)
    allv = list(t_vals) + list(c_vals)
    brier = (sum((v / 100 - 1) ** 2 for v in t_vals) +
             sum((v / 100 - 0) ** 2 for v in c_vals)) / len(allv)
    return {"p": round(p, 4), "auc": round(auc, 4),
            "median_t": statistics.median(t_vals), "median_c": statistics.median(c_vals),
            "separation_pp": statistics.median(t_vals) - statistics.median(c_vals),
            "sd_all16": round(statistics.pstdev(allv), 2), "brier": round(brier, 4),
            "failure_b_triggers": {}}


def load_p(d):
    return {p.stem: json.loads(p.read_text(encoding="utf-8"))["misstatement_probability"]
            for p in sorted((REPO / d).glob("case_*.json"))}


def a1_recognition():
    rows = []
    n1 = n2 = 0
    for cid in sorted(pert_cases):
        truth = pert_cases[cid]["company_name"]
        out = {}
        for label, d in (("draw1", "scoring/probe_results/recognition"),
                         ("draw2", "runs/hardening/probe_recognition")):
            f = REPO / d / f"{cid}.json"
            if not f.is_file():
                out[label] = None
                continue
            rec = json.loads(f.read_text(encoding="utf-8"))
            hit = rec["company_guess"].strip().lower() != "unknown" and \
                name_match(rec["company_guess"], truth)
            out[label] = {"guess": rec["company_guess"], "confidence": rec["confidence"],
                          "recognized": hit}
        n1 += bool(out["draw1"] and out["draw1"]["recognized"])
        n2 += bool(out["draw2"] and out["draw2"]["recognized"])
        rows.append({"case_id": cid, "ticker": pert_cases[cid]["ticker"], **out})
    return {"per_case": rows, "recognized_draw1": n1, "recognized_draw2": n2,
            "d7_threshold": 3,
            "d7_would_fire_draw2": n2 >= 3,
            "union_recognized": sum(
                1 for r in rows
                if (r["draw1"] and r["draw1"]["recognized"]) or
                   (r["draw2"] and r["draw2"]["recognized"]))}


def a3_sampling():
    p_orig, p_pert = load_p("runs/main"), load_p("runs/perturbed")
    draw_p = {1: {**{n: p_pert[n] for n in treat}, **{n: p_orig[n] for n in ctrl}}}
    draws_root = REPO / "runs/hardening/draws"
    for i, dname in enumerate(sorted(d.name for d in draws_root.iterdir() if d.is_dir()),
                              start=2):
        dp = load_p(f"runs/hardening/draws/{dname}")
        missing = [n for n in mapping if n not in dp]
        if missing:
            raise SystemExit(f"draw {dname} 불완전 — 누락 {missing}")
        draw_p[i] = dp
    draws = sorted(draw_p)
    k = len(draws)

    per_case = {}
    for n in sorted(mapping):
        vals = [draw_p[d][n] for d in draws]
        per_case[n] = {
            "original_id": mapping[n], "ticker": cands[mapping[n]]["ticker"],
            "company": cands[mapping[n]]["company_name"],
            "group": cands[mapping[n]]["group"],
            "draws": vals, "mean": round(statistics.mean(vals), 1),
            "sd": round(statistics.pstdev(vals), 2),
            "min": min(vals), "max": max(vals), "range_pp": max(vals) - min(vals),
        }

    per_draw = [stats_block([draw_p[d][n] for n in treat], [draw_p[d][n] for n in ctrl])
                for d in draws]
    for blk in per_draw:
        blk["failure_b_triggers"] = {"p>=0.20": blk["p"] >= 0.20,
                                     "separation<10pp": blk["separation_pp"] < 10,
                                     "degenerate(sd<5pp)": blk["sd_all16"] < 5}
        blk["failure_b"] = any(blk["failure_b_triggers"].values())
    med = {n: statistics.median([draw_p[d][n] for d in draws]) for n in mapping}
    med_stats = stats_block([med[n] for n in treat], [med[n] for n in ctrl])

    # 분해: RP-05 §3 delta (원본−교란, draw1) vs 케이스 내 표본 σ (교란 k=5)
    decomposition = []
    for n in treat:
        delta = p_orig[n] - p_pert[n]
        sd = per_case[n]["sd"]
        decomposition.append({
            "case_id": n, "ticker": per_case[n]["ticker"],
            "delta_orig_minus_pert_draw1": delta,
            "sampling_sd_perturbed_k5": sd,
            # |delta| ≤ 2σ 이면 표본 잡음으로 설명 가능 범위 (초과 = 잡음 밖 신호 후보)
            "abs_delta_within_2sd": abs(delta) <= 2 * sd,
        })
    sds = [per_case[n]["sd"] for n in treat]
    pooled = {
        "treatment_sd_mean": round(statistics.mean(sds), 2),
        "treatment_sd_median": round(statistics.median(sds), 2),
        "control_sd_mean": round(statistics.mean([per_case[n]["sd"] for n in ctrl]), 2),
        "n_delta_beyond_2sd": sum(1 for d in decomposition if not d["abs_delta_within_2sd"]),
    }
    return {"k": k, "per_case": per_case, "per_draw_stats": per_draw,
            "median_of_draws_stats": med_stats,
            "p_range_across_draws": [min(b["p"] for b in per_draw),
                                     max(b["p"] for b in per_draw)],
            "auc_range_across_draws": [min(b["auc"] for b in per_draw),
                                       max(b["auc"] for b in per_draw)],
            "separation_range_across_draws": [min(b["separation_pp"] for b in per_draw),
                                              max(b["separation_pp"] for b in per_draw)],
            "any_draw_failure_b": any(b["failure_b"] for b in per_draw),
            "decomposition_vs_rp05_s3": decomposition,
            "decomposition_pooled": pooled}


def main() -> int:
    result = {"framing": "post-hoc robustness analysis quantifying L-3 — "
                         "RP-05 §1 pre-registered verdict stands unchanged regardless of outcome",
              "a1_recognition_redraw": a1_recognition()}
    if (REPO / "runs/hardening/draws").is_dir():
        result["a3_sampling"] = a3_sampling()
    out = REPO / "scoring/rp06_hardening_stats.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
