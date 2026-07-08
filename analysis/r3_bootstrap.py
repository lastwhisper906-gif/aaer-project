"""r3_bootstrap.py — DRAFT (감사 B7). R3 '암기 우세' 5/8 경계의 견고성 정량화.

동결 재추첨(k=5, rp07_stats.per_case)만 사용 — 재채점 아님, 캐시·API 불요, 결정론.
R3 계수 규칙(stats.py와 동일): 케이스가 산입되려면 denom<=0 이거나
|delta_mean| >= 0.5*denom (denom = 본실행 orig_score - control_median).
delta_mean = mean(orig_draws) - mean(pert_draws).

부트스트랩: 케이스별 orig/pert 5-draw를 복원추출해 delta_mean*을 다시 만들고,
8케이스의 산입 수를 세어 P(count>=5)와 분포를 낸다. → 5/8 헤드라인이 추첨 잡음에
얼마나 견고한지. **초안: 소유자 검토 후 서술 반영(발행 아님).**
"""
import json
import random
import statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEED = 20260708
B = 20000
FIRE_FRAC = 0.5


def main():
    rp07 = json.loads((REPO / "scoring/rp07_stats.json").read_text())["per_case"]  # {case_id: {...}}
    stats = json.loads((REPO / "analysis/results_stats.json").read_text())
    med_c = stats["primary"]["median_control"]
    # 본실행 orig_score = runs/main/{case}.json (case_NN 키 = rp07 키와 일치)
    orig_score = {}
    for cid in rp07:
        f = REPO / "runs" / "main" / f"{cid}.json"
        if f.is_file():
            orig_score[cid] = json.loads(f.read_text())["misstatement_probability"]

    cases = []
    for cid, pc in rp07.items():
        denom = orig_score.get(cid, 0) - med_c
        cases.append((cid, pc["ticker"], pc["orig_draws"], pc["pert_draws"], denom))

    def fires(delta_mean, denom):
        return denom <= 0 or abs(delta_mean) >= FIRE_FRAC * denom

    # 관측(점추정) 산입
    obs_count = 0
    per_case_obs = []
    for cid, tk, od, pd, denom in cases:
        dm = st.mean(od) - st.mean(pd)
        f = fires(dm, denom)
        obs_count += f
        thr = "auto(denom<=0)" if denom <= 0 else round(FIRE_FRAC * denom, 1)
        per_case_obs.append((tk, round(dm, 1), thr, f))

    # 부트스트랩
    rng = random.Random(SEED)
    counts = []
    fire_freq = {c[0]: 0 for c in cases}
    for _ in range(B):
        cnt = 0
        for cid, tk, od, pd, denom in cases:
            od_s = [od[rng.randrange(len(od))] for _ in od]
            pd_s = [pd[rng.randrange(len(pd))] for _ in pd]
            dm = st.mean(od_s) - st.mean(pd_s)
            if fires(dm, denom):
                cnt += 1
                fire_freq[cid] += 1
        counts.append(cnt)
    p_ge5 = sum(1 for c in counts if c >= 5) / B
    dist = {k: round(counts.count(k) / B, 3) for k in range(3, 9)}

    print(f"관측 R3 산입: {obs_count}/8  (발동 임계 >=5 → {'발동' if obs_count>=5 else '미발동'})")
    for tk, dm, thr, f in per_case_obs:
        print(f"  {tk:5s} delta_mean={dm:+6.1f}  임계={thr}  산입={'O' if f else 'X'}")
    print(f"\n부트스트랩 (k=5 복원추출 x{B}, seed {SEED}):")
    print(f"  P(count >= 5) = {p_ge5:.3f}")
    print(f"  count 분포: {dist}")
    print("  케이스별 산입 빈도:")
    for cid, tk, *_ in cases:
        print(f"    {tk:5s} {fire_freq[cid]/B:.2f}")
    return {"obs_count": obs_count, "p_ge5": p_ge5, "dist": dist,
            "fire_freq": {c[1]: round(fire_freq[c[0]]/B, 3) for c in cases}}


if __name__ == "__main__":
    main()
