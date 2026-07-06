"""페이로드 빌더의 방법론 규율 테스트 (컷오프·누출·교란 결정론)."""
import datetime
import json
from pathlib import Path

import build_payload as bp

REPO = Path(__file__).resolve().parent.parent
FORBIDDEN_PAYLOAD_SUBSTRINGS = [
    "aaer", "fraud", "manipulat", "scheme_summary", "matched_case",
    "m_score", "beneish", "dechow", "montier", "sloan", "piotroski",
    "9FA11F98", "A2D69CFE",  # 카나리 GUID — 페이로드 반입 즉시 누출
]


def _cases():
    return json.loads(bp.EVALUATEE_CASES.read_text(encoding="utf-8"))["cases"]


def test_all_series_and_chronology_respect_cutoff():
    for case in _cases():
        cutoff = datetime.date.fromisoformat(case["cutoff_date"])
        p = bp.build_payload(case)
        for tag, vals in p["financial_series_point_in_time"].items():
            for v in vals:
                assert datetime.date.fromisoformat(v["filed"]) <= cutoff, \
                    f"{case['case_id']} {tag}: filed {v['filed']} > cutoff"
        for r in p["filing_chronology"]:
            assert datetime.date.fromisoformat(r["filing_date"]) <= cutoff, \
                f"{case['case_id']}: chronology {r} > cutoff"


def test_payload_has_no_ground_truth_or_baseline_markers():
    for case in _cases()[:4]:  # 값 스캔은 표본으로 충분 (구조 동일)
        text = json.dumps(bp.build_payload(case), ensure_ascii=False).lower()
        leaked = [s for s in FORBIDDEN_PAYLOAD_SUBSTRINGS if s.lower() in text]
        assert not leaked, f"{case['case_id']}: 페이로드 누출 마커 {leaked}"


def test_perturbation_is_deterministic_and_ratio_preserving():
    case = _cases()[0]
    p1, p2 = bp.build_payload(case, perturb=True), bp.build_payload(case, perturb=True)
    assert p1 == p2, "교란 변형이 비결정론"
    k = p1["_k_internal"]
    assert 0.4 <= k <= 2.5
    orig = bp.build_payload(case)
    for tag, vals in orig["financial_series_point_in_time"].items():
        for v, vp in zip(vals, p1["financial_series_point_in_time"][tag]):
            if isinstance(v["value"], (int, float)) and abs(v["value"]) > 1:
                assert abs(vp["value"] / v["value"] - k) < 1e-6, f"{tag} 재스케일 불일치"


def test_perturbed_variant_hides_identity_but_keeps_dates():
    case = _cases()[0]
    p = bp.build_payload(case, perturb=True)
    f = p["case"]
    assert "cik" not in f, "교란 변형에 CIK 잔존"
    assert f["ticker"].startswith("XX") and f["company_name"].startswith("Company ")
    assert f["cutoff_date"] == case["cutoff_date"], "D8: 날짜는 불변이어야 함"
    orig = bp.build_payload(case)
    assert p["filing_chronology"] == orig["filing_chronology"], "연대기 날짜 변형 금지 (D8)"
