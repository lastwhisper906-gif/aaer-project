"""RP-10 Phase 2.2: 사전 커밋 계획(analysis/ANALYSIS_PLAN.md)의 기계 실행.

출력: analysis/results_stats.json + analysis/results_summary.md
결정론: seed 20260707 고정, 네트워크 없음. 사용: python analysis/stats.py
"""
import csv
import json
import math
import random
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEED = 20260707
N_PERM = 100_000
N_BOOT = 10_000
ALPHA = 0.05
FLAG = 50          # 동결 루브릭 임계 (plan §1)
RHO_HIGH = 0.7     # R2 (plan §4)


def load_table():
    rows = list(csv.DictReader(open(REPO / "analysis/baseline_table.csv", encoding="utf-8")))
    for r in rows:
        for k in ("llm_score", "llm_perturbed", "m_score", "f_score"):
            r[k] = float(r[k]) if r[k] not in ("", "None", None) else None
    return rows


def perm_test_mean(a, b, rng, n=N_PERM):
    """단측 (mean(a) > mean(b)) 순열 p."""
    obs = statistics.mean(a) - statistics.mean(b)
    pooled = list(a) + list(b)
    na = len(a)
    ge = 0
    for _ in range(n):
        rng.shuffle(pooled)
        if statistics.mean(pooled[:na]) - statistics.mean(pooled[na:]) >= obs - 1e-12:
            ge += 1
    return (ge + 1) / (n + 1), obs


def fisher_one_sided(tp, fn, fp, tn):
    """단측 Fisher exact (초기하 — 양성군에 플래그가 더 몰릴 확률)."""
    def c(n, k):
        return math.comb(n, k)
    n = tp + fn + fp + tn
    row1 = tp + fn
    col1 = tp + fp
    p = 0.0
    for x in range(tp, min(row1, col1) + 1):
        p += c(row1, x) * c(n - row1, col1 - x) / c(n, col1)
    return p


def cliffs_delta(a, b):
    gt = lt = 0
    for x in a:
        for y in b:
            gt += x > y
            lt += x < y
    return (gt - lt) / (len(a) * len(b))


def auc(a, b):
    gt = eq = 0
    for x in a:
        for y in b:
            gt += x > y
            eq += x == y
    return (gt + 0.5 * eq) / (len(a) * len(b))


def boot_auc_ci(a, b, rng):
    vals = []
    for _ in range(N_BOOT):
        ra = [a[rng.randrange(len(a))] for _ in a]
        rb = [b[rng.randrange(len(b))] for _ in b]
        vals.append(auc(ra, rb))
    vals.sort()
    return vals[int(0.025 * N_BOOT)], vals[int(0.975 * N_BOOT)]


def spearman(x, y):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = ranks(x), ranks(y)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else None


def residuals(y, x):
    """OLS y~x 잔차 (plan §4 R2)."""
    mx, my = statistics.mean(x), statistics.mean(y)
    den = sum((a - mx) ** 2 for a in x)
    beta = sum((a - mx) * (b - my) for a, b in zip(x, y)) / den if den else 0.0
    alpha = my - beta * mx
    return [b - (alpha + beta * a) for a, b in zip(x, y)]


def fpr_bound(fp, n):
    if fp == 0:
        return {"fp": 0, "n": n, "rule": "rule-of-three", "upper95_pct": round(300 / n, 1)}
    # Clopper-Pearson 정확 구간 (이항, 95% 양측)
    def beta_inv(p, a, b):  # 이분법
        lo, hi = 0.0, 1.0
        from math import lgamma, exp, log

        def betacdf(x):
            # 수치 적분 (단순, N=30 규모에 충분)
            n_steps = 20000
            s = 0.0
            for i in range(1, n_steps + 1):
                t = x * (i - 0.5) / n_steps
                s += exp((a - 1) * log(max(t, 1e-12)) + (b - 1) * log(max(1 - t, 1e-12)))
            s *= x / n_steps
            norm = exp(lgamma(a) + lgamma(b) - lgamma(a + b))
            return s / norm
        for _ in range(60):
            mid = (lo + hi) / 2
            if betacdf(mid) < p:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    lo = 0.0 if fp == 0 else beta_inv(0.025, fp, n - fp + 1)
    hi = beta_inv(0.975, fp + 1, n - fp)
    return {"fp": fp, "n": n, "rule": "Clopper-Pearson 95%",
            "lo_pct": round(100 * lo, 1), "upper95_pct": round(100 * hi, 1)}


def frame_stats(fraud, ctrl, rng, label):
    p, obs = perm_test_mean(fraud, ctrl, rng)
    fp = sum(1 for v in ctrl if v >= FLAG)
    tp = sum(1 for v in fraud if v >= FLAG)
    lo, hi = boot_auc_ci(fraud, ctrl, rng)
    return {
        "frame": label, "n_fraud": len(fraud), "n_control": len(ctrl),
        "fraud_scores": fraud, "control_scores": ctrl,
        "mean_diff": round(obs, 2),
        "median_fraud": statistics.median(fraud), "median_control": statistics.median(ctrl),
        "perm_p_one_sided": round(p, 6),
        "fisher_2x2": {"tp": tp, "fn": len(fraud) - tp, "fp": fp,
                       "tn": len(ctrl) - fp, "threshold": FLAG,
                       "p_one_sided": round(fisher_one_sided(
                           tp, len(fraud) - tp, fp, len(ctrl) - fp), 6)},
        "cliffs_delta": round(cliffs_delta(fraud, ctrl), 3),
        "rank_biserial_note": "rank-biserial = Cliff's delta (동치)",
        "auc": round(auc(fraud, ctrl), 4),
        "auc_boot95": [round(lo, 3), round(hi, 3)],
        "auc_stability_label": "UNSTABLE at N=30 — 점 플롯이 1차 시각화",
        "fpr": fpr_bound(fp, len(ctrl)),
    }


def main() -> int:
    rows = load_table()
    fraud = [r for r in rows if r["group"] == "fraud"]
    ctrl = [r for r in rows if r["group"] == "control"]
    incomplete = [r["case_id"] for r in rows if r["llm_score"] is None]
    fraud_s = [r["llm_score"] for r in fraud if r["llm_score"] is not None]
    ctrl_s = [r["llm_score"] for r in ctrl if r["llm_score"] is not None]

    rng = random.Random(SEED)
    primary = frame_stats(fraud_s, ctrl_s, rng, "primary: original(8) vs original(22)")
    fraud_pert = [r["llm_perturbed"] for r in fraud if r["llm_perturbed"] is not None]
    secondary = frame_stats(fraud_pert, ctrl_s, rng,
                            "secondary: perturbed-fraud vs original-control (J14)")

    # 기준선: 각자 동일 분리 검정 + LLM과의 Spearman + R2 잔차 검정
    baselines = {}
    for key, col in (("beneish_m", "m_score"), ("dechow_f", "f_score")):
        sub = [r for r in rows if r[col] is not None and r["llm_score"] is not None]
        bf = [r[col] for r in sub if r["group"] == "fraud"]
        bc = [r[col] for r in sub if r["group"] == "control"]
        p_b, obs_b = perm_test_mean(bf, bc, rng)
        rho = spearman([r["llm_score"] for r in sub], [r[col] for r in sub])
        res = residuals([r["llm_score"] for r in sub], [r[col] for r in sub])
        rf = [e for e, r in zip(res, sub) if r["group"] == "fraud"]
        rc = [e for e, r in zip(res, sub) if r["group"] == "control"]
        p_res, obs_res = perm_test_mean(rf, rc, rng)
        baselines[key] = {
            "n_computable": len(sub), "n_fraud": len(bf), "n_control": len(bc),
            "own_separation": {"mean_diff": round(obs_b, 3), "perm_p": round(p_b, 6),
                               "auc": round(auc(bf, bc), 4)},
            "spearman_rho_vs_llm": round(rho, 3) if rho is not None else None,
            "r2_residual_test": {"resid_mean_diff": round(obs_res, 2),
                                 "perm_p": round(p_res, 6)},
            "r2_fires": (rho is not None and rho >= RHO_HIGH and p_res >= ALPHA),
        }

    # R3: RP-07 완결 delta (동결 산출물)
    rp07 = json.loads((REPO / "scoring/rp07_stats.json").read_text())
    med_c = primary["median_control"]
    r3_cases = []
    for d in rp07["delta_decomposition_completed"]:
        base = [r for r in fraud if r["case_id"] ==
                json.loads((REPO / "scoring/id_mapping.json").read_text())["mapping"][d["case_id"]]]
        orig_score = base[0]["llm_score"] if base else None
        denom = (orig_score - med_c) if orig_score is not None else None
        fires = (denom is None or denom <= 0
                 or abs(d["delta_mean_orig_minus_pert"]) >= 0.5 * denom)
        r3_cases.append({"ticker": d["ticker"], "delta_mean": d["delta_mean_orig_minus_pert"],
                         "orig_minus_ctrl_median": denom, "counts_toward_r3": bool(fires)})
    r3_n = sum(1 for c in r3_cases if c["counts_toward_r3"])

    # 결론 규칙 판정 (양 프레임 — 보수 쪽 승리, 우선순위 R1>R3>R2)
    def rules(frame, mark):
        r1 = frame["perm_p_one_sided"] >= ALPHA
        r2 = any(b["r2_fires"] for b in baselines.values())
        r3 = r3_n >= 5
        fired = "R1" if r1 else ("R3" if r3 else ("R2" if r2 else "R4"))
        return {"frame": mark, "R1_null": r1, "R2_mechanical": r2,
                "R3_memorization": r3, "fired": fired}
    verdicts = [rules(primary, "primary"), rules(secondary, "secondary")]
    order = {"R1": 0, "R3": 1, "R2": 2, "R4": 3}
    headline = min((v["fired"] for v in verdicts), key=lambda f: order[f])

    out = {
        "plan": "analysis/ANALYSIS_PLAN.md (사전 커밋)", "seed": SEED,
        "incomplete_cases": incomplete,
        "primary": primary, "secondary": secondary,
        "baselines": baselines,
        "r3_decomposition": {"cases": r3_cases, "n_counting": r3_n,
                             "fires_at": ">=5/8"},
        "conclusion_rules": {"per_frame": verdicts,
                             "headline_rule_fired": headline},
    }
    (REPO / "analysis/results_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    md = ["# results_summary — RP-10 Phase 2 (기계 생성, 계획 사전 커밋본 준수)", ""]
    for fr in (primary, secondary):
        md += [f"## {fr['frame']}",
               f"- fraud {fr['n_fraud']} vs control {fr['n_control']} · 평균차 "
               f"{fr['mean_diff']}pp · 중위 {fr['median_fraud']} vs {fr['median_control']}",
               f"- 순열 p(단측) = **{fr['perm_p_one_sided']}** · Fisher p = "
               f"{fr['fisher_2x2']['p_one_sided']} (플래그 p≥{FLAG}: TP {fr['fisher_2x2']['tp']}/"
               f"{fr['n_fraud']}, FP {fr['fisher_2x2']['fp']}/{fr['n_control']})",
               f"- Cliff's δ = {fr['cliffs_delta']} · AUC = {fr['auc']} "
               f"(부트스트랩 95% {fr['auc_boot95']} — {fr['auc_stability_label']})",
               f"- FPR: {fr['fpr']}", ""]
    md += ["## 기준선 (동일 30사 PIT)"]
    for k, b in baselines.items():
        md += [f"- **{k}** (계산가능 {b['n_computable']}/30): 자체 분리 p="
               f"{b['own_separation']['perm_p']}, AUC={b['own_separation']['auc']} · "
               f"Spearman ρ(LLM)={b['spearman_rho_vs_llm']} · R2 잔차 p="
               f"{b['r2_residual_test']['perm_p']} → R2 발동={b['r2_fires']}"]
    md += ["", f"## R3 암기 분해: {r3_n}/8 케이스 산입 (발동 임계 ≥5)",
           "", f"## 결론 규칙 발동: **{headline}** (프레임별: "
           + ", ".join(f"{v['frame']}={v['fired']}" for v in verdicts) + ")"]
    (REPO / "analysis/results_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
