"""RP-09 Stage 3c: 검정력 사전 계산 — 대조군 v2 점수 존재 전 커밋 (결정론, seed 고정).

질문 (RP-09 원문): 8 실험군 vs 16-24 대조군에서 사전 등록 임계로 분해 가능한
분리/AUC/오탐율 차이는 무엇이며, 9.0pp급 사건이 설계 분해능 안인가 밖인가.

입력 (전부 동결 산출물, 읽기 전용):
  - 실험군 원본 점수 8 (runs/main — RP-05 §1 불변) — 관측 분포로 사용
  - inside-noise σ 추정 (scoring/rp07_stats.json — 원본 재추첨 k=5)
  - RP-01 대조군 관측 분포 (runs/main C8) — 대조군 시나리오 모수의 근거
출력: scoring/rp09_power.json
"""
import itertools
import json
import random
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

SEED = 20260707  # 사전 커밋 고정 시드
TREAT = ["case_01", "case_02", "case_03", "case_06",
         "case_08", "case_09", "case_12", "case_13"]
CTRL_RP01 = ["case_04", "case_05", "case_07", "case_10",
             "case_11", "case_14", "case_15", "case_16"]
ALPHA = 0.05          # 사전 등록 유의 임계 (RP-05)
SEP_THRESHOLD = 10.0  # 사전 등록 분리 임계 (pp)


def load_p(rel):
    out = {}
    for p in sorted((REPO / rel).glob("case_*.json")):
        j = json.loads(p.read_text(encoding="utf-8"))
        out[j["case_id"]] = j["misstatement_probability"]
    return out


def mc_power(t_obs, ctrl_mu, ctrl_sd, inside_sd, n_c, n_sim, rng):
    """대조군 시나리오 + 양측 inside-noise 하에서 p<ALPHA / 분리<10pp 확률."""
    sig = below = 0
    seps = []
    for _ in range(n_sim):
        tv = [max(0, min(100, x + rng.gauss(0, inside_sd))) for x in t_obs]
        cv = [max(0, min(100, rng.gauss(ctrl_mu, ctrl_sd))) for _ in range(n_c)]
        p, _ = mann_whitney_exact_fast(tv, cv, rng)
        sep = statistics.median(tv) - statistics.median(cv)
        seps.append(sep)
        sig += p < ALPHA
        below += sep < SEP_THRESHOLD
    return {"p_lt_alpha_rate": round(sig / n_sim, 3),
            "sep_below_10pp_rate": round(below / n_sim, 3),
            "sep_mean": round(statistics.mean(seps), 1),
            "sep_sd": round(statistics.stdev(seps), 2)}


def mann_whitney_exact_fast(tv, cv, rng, n_perm=2000):
    """8 vs 16-24는 전수 조합이 큼 — 몬테카를로 순열 p (시드 고정, 사전 계산 전용)."""
    pooled = tv + cv
    n_t = len(tv)
    # midranks
    order = sorted(range(len(pooled)), key=lambda i: pooled[i])
    ranks = [0.0] * len(pooled)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and pooled[order[j + 1]] == pooled[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k2 in range(i, j + 1):
            ranks[order[k2]] = r
        i = j + 1
    obs = sum(ranks[:n_t])
    idx = list(range(len(pooled)))
    ge = 0
    for _ in range(n_perm):
        samp = rng.sample(idx, n_t)
        if sum(ranks[i2] for i2 in samp) >= obs - 1e-9:
            ge += 1
    auc = (obs - n_t * (n_t + 1) / 2) / (n_t * len(cv))
    return (ge + 1) / (n_perm + 1), auc


def main() -> int:
    rng = random.Random(SEED)
    p_main = load_p("runs/main")
    t_obs = [p_main[n] for n in TREAT]
    c_rp01 = [p_main[n] for n in CTRL_RP01]
    rp07 = json.loads((REPO / "scoring/rp07_stats.json").read_text())
    inside_sds = [d["inside_noise_sd_orig"]
                  for d in rp07["delta_decomposition_completed"]]
    inside_sd = statistics.median(inside_sds)

    # 최소 달성 가능 p (동률 없다는 최선 배치): 8 vs n_c 초기하 1/C(n,8)
    import math
    min_p = {str(n_c): 1 / math.comb(8 + n_c, 8) for n_c in (8, 16, 20, 24)}

    # FPR 분해능: 대조군 n으로 추정 가능한 오탐율 눈금 + 정확 이항 95% CI (0오탐 시)
    fpr = {}
    for n_c in (8, 16, 20, 24):
        fpr[str(n_c)] = {"granularity_pct": round(100 / n_c, 1),
                         "ci95_upper_if_zero_fp_pct": round(100 * (1 - 0.05 ** (1 / n_c)), 1)}

    # 시나리오: RP-01 대조군 관측 (median/sd) ± 보수/낙관
    mu_obs = statistics.median(c_rp01)
    sd_obs = statistics.stdev(c_rp01)
    scenarios = {
        "rp01_observed": (mu_obs, sd_obs),
        "conservative_noisier_controls": (mu_obs + 5, sd_obs + 5),
        "clean_controls": (mu_obs - 5, max(5.0, sd_obs - 5)),
    }
    power = {}
    for name, (mu, sd) in scenarios.items():
        power[name] = {"ctrl_mu": mu, "ctrl_sd": round(sd, 2)}
        for n_c in (8, 16, 24):
            power[name][f"n_c={n_c}"] = mc_power(t_obs, mu, sd, inside_sd,
                                                 n_c, 400, rng)

    out = {
        "committed_before_any_v2_control_scores": True,
        "seed": SEED,
        "alpha": ALPHA, "sep_threshold_pp": SEP_THRESHOLD,
        "treatment_scores_frozen": dict(zip(TREAT, t_obs)),
        "rp01_control_observed": {"median": mu_obs, "sd": round(sd_obs, 2)},
        "inside_noise_sd_used": round(inside_sd, 2),
        "min_achievable_p_8_vs_nc": {k: f"{v:.2e}" for k, v in min_p.items()},
        "fpr_resolution": fpr,
        "monte_carlo_power": power,
        "note": "mann_whitney_exact_fast = 몬테카를로 순열 (n_perm=2000, seed 고정) — "
                "실채점 검정은 동결 mann_whitney_exact(전수)를 그대로 사용",
    }
    dest = REPO / "scoring/rp09_power.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("min_achievable_p_8_vs_nc", "fpr_resolution",
                                          "inside_noise_sd_used")}, indent=1))
    for name, blk in power.items():
        print(name, {k: v for k, v in blk.items() if k.startswith("n_c")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
