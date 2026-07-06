"""오염 프로브 기계 판정 (D7 분기 + 축어 회상 등급) — 결정론 Python.

These controls BOUND memorization risk; they do not eliminate it.

판정 규칙 (probes.md ①·③ — 이 파일의 커밋이 결과 판독에 선행해야 한다):
- 인지: company_guess ↔ 실제 사명 (당시 또는 통용) — 대소문자·법인 접미사 무시.
  정규화: 소문자화, 구두점 제거, 접미사 어휘 제거 후 완전 일치 또는 한쪽이
  다른 쪽의 어두 연속 토큰열(접두열)인 경우 일치로 판정. 'unknown'은 불일치.
  경계 사례는 guess 원문과 함께 RP-05에 전건 수록 (재량 판단은 J14+).
- D7 (사전 등록 9f0fb42): 인지 ≥3/8 → CONTAMINATED.
- 축어 회상: revenue·net_income 각각 point-in-time 실측 대비 ±2% 이내면 회상 성공
  (둘 다 성공 = 회상 성공 1건). known=false 는 실패.
- 잔여 위험 등급: HIGH = 인지∧회상 / MED = 하나 / LOW = 둘 다 실패.

사용: python scoring/probe_verdict.py            # 판정표 출력 (stdout)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))

SUFFIX_WORDS = {
    "inc", "incorporated", "corp", "corporation", "company", "co", "ltd",
    "limited", "plc", "nv", "sa", "ag", "llc", "lp", "international",
    "holdings", "holding", "group", "the",
}


def normalize(name: str) -> tuple[str, ...]:
    tokens = re.sub(r"[^a-z0-9 ]", " ", name.lower()).split()
    return tuple(t for t in tokens if t not in SUFFIX_WORDS)


def name_match(guess: str, truth: str) -> bool:
    g, t = normalize(guess), normalize(truth)
    if not g or not t:
        return False
    if g == t:
        return True
    # 어두 접두열 (통용 사명: 'Orthofix' vs 'Orthofix International N.V.')
    shorter, longer = (g, t) if len(g) <= len(t) else (t, g)
    return longer[:len(shorter)] == shorter


def within_2pct(claimed, actual) -> bool:
    if claimed is None or actual is None or actual == 0:
        return False
    try:
        return abs(float(claimed) - float(actual)) / abs(float(actual)) <= 0.02
    except (TypeError, ValueError):
        return False


def actual_fy_values(case: dict) -> dict:
    """컷오프 직전 회계연도의 실측 Revenue/NetIncome (point-in-time 표에서)."""
    import build_payload as bp
    series = bp.load_pit_series(case["ticker"],
                                __import__("datetime").date.fromisoformat(case["cutoff_date"]))
    out = {}
    for kind, tags in (("revenue", ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
                                    "SalesRevenueNet", "SalesRevenueGoodsNet", "SalesRevenueServicesNet"]),
                       ("net_income", ["NetIncomeLoss", "ProfitLoss"])):
        candidates = []
        for tag in tags:
            for v in series.get(tag, []):
                if v["period_type"] == "annual":
                    candidates.append(v)
        out[kind] = max(candidates, key=lambda v: v["end"])["value"] if candidates else None
    return out


def main() -> int:
    cases = {c["case_id"]: c for c in json.loads(
        (REPO / "scoring/perturbed_cases.json").read_text(encoding="utf-8"))["cases"]}
    rec_dir = REPO / "scoring/probe_results/recognition"
    ver_dir = REPO / "scoring/probe_results/verbatim"

    print("| case | 인지 guess (원문) | conf | 인지 | 회상 rev/ni (±2%) | 회상 | 잔여 위험 |")
    print("|---|---|---|---|---|---|---|")
    n_recog = 0
    rows = []
    for cid, case in sorted(cases.items()):
        rec = json.loads((rec_dir / f"{cid}.json").read_text(encoding="utf-8")) \
            if (rec_dir / f"{cid}.json").is_file() else None
        ver = json.loads((ver_dir / f"{cid}.json").read_text(encoding="utf-8")) \
            if (ver_dir / f"{cid}.json").is_file() else None
        recog = bool(rec) and rec["company_guess"].strip().lower() != "unknown" \
            and name_match(rec["company_guess"], case["company_name"])
        n_recog += recog
        recall = False
        rev_ok = ni_ok = None
        if ver and ver.get("known"):
            actual = actual_fy_values(case)
            rev_ok = within_2pct(ver.get("revenue"), actual["revenue"])
            ni_ok = within_2pct(ver.get("net_income"), actual["net_income"])
            recall = bool(rev_ok and ni_ok)
        risk = "HIGH" if (recog and recall) else ("MED" if (recog or recall) else "LOW")
        rows.append((cid, risk))
        print(f"| {cid} | {rec['company_guess'] if rec else '—'!r} | "
              f"{rec['confidence'] if rec else '—'} | {'O' if recog else 'X'} | "
              f"{rev_ok}/{ni_ok} | {'O' if recall else 'X'} | {risk} |")

    verdict = "CONTAMINATED" if n_recog >= 3 else "NOT-CONTAMINATED"
    print(f"\n인지 {n_recog}/8 → **D7 판정: {verdict}** (임계 ≥3, 사전 등록 9f0fb42)")
    if verdict == "CONTAMINATED":
        print("분기: 본 분석 = 교란 실행 전용, 원본 결과는 부록 상한, 전 보고서 헤드라인 명시")
    else:
        print("분기: 본 분석 = 원본 실행, 원본−교란 delta = 암기 기여 추정치")
    return 0


if __name__ == "__main__":
    sys.exit(main())
