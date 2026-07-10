"""3-arm 정체 실험 결정론 판독 (IDENTITY_3ARM_PLAN §3 — 기계 적용, 재해석 없음).

a = 동결 교란(llm_perturbed, unified_table) · b = runs/wave2/identity_arm_b ·
c = 동결 원본(llm_score, unified_table). paired delta 케이스별 + median +
정확 이항 부호 검정(동률 제외, 병기 전용). 분류 임계 = 사전 등록 10pp.
출력: analysis/identity_3arm_results.json. N=9 방향 증거 — R/H 판정 입력 아님.
"""
import csv
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ARM_B = REPO / "runs/wave2/identity_arm_b"
OUT = REPO / "analysis/identity_3arm_results.json"
BAR = 10.0  # 사전 등록 임계 (pp)


def sign_test(deltas):
    """정확 이항 부호 검정 (양측, 동률 제외)."""
    pos = sum(1 for d in deltas if d > 0)
    neg = sum(1 for d in deltas if d < 0)
    n = pos + neg
    if n == 0:
        return {"n_nonzero": 0, "pos": 0, "neg": 0, "p_two_sided": 1.0}
    k = min(pos, neg)
    p = min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)
    return {"n_nonzero": n, "pos": pos, "neg": neg, "p_two_sided": round(p, 5)}


def median(xs):
    s = sorted(xs)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def main() -> int:
    cases = {c["case_id"]: c for c in json.loads(
        (REPO / "data/evaluatee/cases_wave2.json").read_text())["cases"]}
    fraud_ids = sorted(json.loads((REPO / "runs/wave2/fraud_case_ids.json").read_text()))
    frozen = {r["ticker"]: r for r in csv.DictReader(
        open(REPO / "analysis/unified_table.csv", encoding="utf-8"))
        if r["wave"] == "wave2" and r["group"] == "fraud"}
    fict = json.loads((REPO / "data/evaluatee/fict_names_wave2.json").read_text())["names"]

    missing = [cid for cid in fraud_ids if not (ARM_B / f"{cid}.json").exists()]
    if missing:
        print(f"FAIL — arm(b) 미완 {missing} (판정은 전량 존재 시에만)"); return 1

    per, d_ba, d_cb = [], [], []
    for cid in fraud_ids:
        tk = cases[cid]["ticker"]
        fz = frozen[tk]
        a, c = float(fz["llm_perturbed"]), float(fz["llm_score"])
        b = float(json.loads((ARM_B / f"{cid}.json").read_text())["misstatement_probability"])
        d_ba.append(b - a); d_cb.append(c - b)
        per.append({"case_id": cid, "ticker": tk, "fict_name": fict[cid]["company_name"],
                    "a_perturbed_frozen": a, "b_fict_name": b, "c_original_frozen": c,
                    "delta_b_minus_a": b - a, "delta_c_minus_b": c - b})

    med_ba, med_cb = median(d_ba), median(d_cb)
    if abs(med_ba) < BAR and med_cb >= BAR:
        cls, stmt = "i", ("실명 토큰이 점수를 끌어올린다는 방향 증거 — 암기 기여가 "
                          "이름 채널에 실린다 (b≈a, c만 상승). N=9 방향 증거.")
    elif abs(med_ba) < BAR and abs(med_cb) < BAR:
        cls, stmt = "ii", "암기의 점수 기여가 작다는 방향 증거 (a≈b≈c). N=9 방향 증거."
    else:
        cls, stmt = "iii", ("해석 보류 + 기록 — 사전 문장으로 덮이지 않는 패턴. "
                            "수치만 병기, 소유자 검토 이관.")

    result = {"plan": "analysis/IDENTITY_3ARM_PLAN.md (D36)", "bar_pp": BAR,
              "per_case": per,
              "median_b_minus_a": med_ba, "median_c_minus_b": med_cb,
              "sign_test_b_minus_a": sign_test(d_ba),
              "sign_test_c_minus_b": sign_test(d_cb),
              "classification": cls, "interpretation_preregistered": stmt,
              "framing": "N=9 directional evidence — 인과 확정 서술 금지; R/H 판정 불변"}
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for p in per:
        print(f"{p['ticker']}: a={p['a_perturbed_frozen']:.0f} b={p['b_fict_name']:.0f} "
              f"c={p['c_original_frozen']:.0f}  (b−a={p['delta_b_minus_a']:+.0f}, "
              f"c−b={p['delta_c_minus_b']:+.0f})")
    print(f"median(b−a)={med_ba:+.1f} · median(c−b)={med_cb:+.1f} → 분류 ({cls})")
    print(stmt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
