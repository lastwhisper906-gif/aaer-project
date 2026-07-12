"""test_date_shift.py — perturbation-v2 계약 테스트 (specs/perturb_v2.md §7)."""
import datetime
import json

from date_shift import offset_for_case, shift_date, shift_payload

# build_payload(perturb=True) 출력 형태의 픽스처 (스펙 §3 순서 계약 — 이동은
# 익명화·재스케일 이후 렌더 시점)
FIXTURE = {
    "variant": "perturbed",
    "case": {"case_id": "case_99", "ticker": "XX99", "company_name": "Company CASE_99",
             "cutoff_date": "2015-06-30"},
    "financial_series_point_in_time": {
        "Revenues": [
            {"start": "2014-01-01", "end": "2014-12-31", "period_type": "annual",
             "value": 123.0, "filed": "2015-02-10", "accession": "0000000001-15-000010",
             "form": "10-K"},
            {"start": "2015-01-01", "end": "2015-03-31", "period_type": "quarterly",
             "value": 45.0, "filed": "2015-05-01", "accession": "0000000001-15-000011",
             "form": "10-Q"},
        ],
        "Assets": [
            {"start": None, "end": "2015-03-31", "period_type": "instant",
             "value": 999.0, "filed": "2015-05-01", "accession": "0000000001-15-000011",
             "form": "10-Q"},
        ],
    },
    "filing_chronology": [
        {"form": "10-K", "filing_date": "2015-02-10"},
        {"form": "NT 10-Q", "filing_date": "2015-05-11"},
        {"form": "8-K", "filing_date": "2015-06-30"},
    ],
}


def _all_dates(payload):
    out = [payload["case"]["cutoff_date"]]
    for vals in payload["financial_series_point_in_time"].values():
        for v in vals:
            out += [d for d in (v.get("start"), v["end"], v["filed"]) if d]
    out += [r["filing_date"] for r in payload["filing_chronology"]]
    return out


# §7-1 결정론

def test_offset_deterministic_and_snapshot():
    a, b = offset_for_case("case_99"), offset_for_case("case_99")
    assert a == b
    assert a == offset_for_case("case_99")  # 3회째도 동일
    # 스냅샷 고정: 유도식(sha256+salt)이 바뀌면 여기서 깨진다
    assert a == 364


# §7-2 주 단위 속성 + 부호 양쪽 출현

def test_whole_week_and_range_and_both_signs():
    ids = [f"case_{i:02d}" for i in range(1, 74)] + [f"hc_{i:02d}" for i in range(1, 10)]
    offsets = [offset_for_case(cid) for cid in ids]
    for o in offsets:
        assert o % 7 == 0
        assert 182 <= abs(o) <= 546
    assert any(o > 0 for o in offsets) and any(o < 0 for o in offsets)


# §7-3 간격 보존 + 요일 보존

def test_interval_and_weekday_preservation():
    shifted = shift_payload(FIXTURE)
    orig, new = _all_dates(FIXTURE), _all_dates(shifted)
    assert len(orig) == len(new)
    d0 = datetime.date.fromisoformat
    # 모든 날짜쌍의 차가 동일 (균일 이동의 항등)
    for i in range(len(orig)):
        for j in range(i + 1, len(orig)):
            assert (d0(orig[i]) - d0(orig[j])) == (d0(new[i]) - d0(new[j]))
    for o, n in zip(orig, new):
        assert d0(o).weekday() == d0(n).weekday()


# §7-4 컷오프 비교 불변

def test_cutoff_comparison_invariance():
    shifted = shift_payload(FIXTURE)
    d0 = datetime.date.fromisoformat
    cut_o = d0(FIXTURE["case"]["cutoff_date"])
    cut_n = d0(shifted["case"]["cutoff_date"])
    for tag, vals in FIXTURE["financial_series_point_in_time"].items():
        for v, w in zip(vals, shifted["financial_series_point_in_time"][tag]):
            assert (d0(v["filed"]) <= cut_o) == (d0(w["filed"]) <= cut_n)
    for r, s in zip(FIXTURE["filing_chronology"], shifted["filing_chronology"]):
        assert (d0(r["filing_date"]) <= cut_o) == (d0(s["filing_date"]) <= cut_n)
    # == cutoff 경계(8-K 2015-06-30)가 이동 후에도 == cutoff
    assert shifted["filing_chronology"][-1]["filing_date"] == shifted["case"]["cutoff_date"]


# §7-5 no-true-date-leak 문자열 스캔 (원본 accession 부재 포함)
#
# 주의(구현 중 발견, Q-F05에 기록): 주-단위 오프셋이 원본 날짜쌍의 차와 정확히
# 일치하면(예: 364일 = 52주 = 역년 기간의 start↔end 간격) 이동된 날짜가 "다른"
# 원본 날짜 문자열 위에 착지하는 양성 충돌이 생긴다. 엄격 스캔은 그 전제
# (오프셋 ∉ 날짜쌍 차 집합)를 단정한 뒤 수행한다.

def _pairwise_diffs(dates):
    d0 = datetime.date.fromisoformat
    ds = sorted({d0(x) for x in dates})
    return {abs((a - b).days) for a in ds for b in ds if a != b}


def test_no_true_date_or_accession_leak_strict():
    offset = 203  # 29주 — 아래에서 충돌-부재 전제를 기계 단정
    assert offset % 7 == 0 and offset not in _pairwise_diffs(_all_dates(FIXTURE))
    shifted = shift_payload(FIXTURE, offset_days=offset)
    text = json.dumps(shifted, ensure_ascii=False)
    for d in set(_all_dates(FIXTURE)):
        assert d not in text, f"진짜 날짜 {d} 가 v2 렌더에 생존"
    assert "0000000001-15-000010" not in text and "0000000001-15-000011" not in text
    # 마스킹은 케이스 내 순차 중립 ID
    accs = {v["accession"] for vals in shifted["financial_series_point_in_time"].values()
            for v in vals}
    assert accs == {"acc-001", "acc-002"}


def test_collision_property_documented():
    """case_99의 기본 오프셋(+364 = 52주)은 역년 start(2014-01-01)를 같은 해
    end(2014-12-31) 문자열 위로 옮긴다 — 양성 충돌의 실증 (leak 아님: 원본
    위치의 값은 전부 이동됨). 미래 v2 위생 스캔은 이 전제를 케이스별로
    확인해야 한다 (Q-F05 등록)."""
    assert offset_for_case("case_99") == 364
    assert 364 in _pairwise_diffs(_all_dates(FIXTURE))
    shifted = shift_payload(FIXTURE)
    # 필드 단위로는 전부 이동됨 (원본 위치 잔존 0)
    for (tag, vals) in FIXTURE["financial_series_point_in_time"].items():
        for v, w in zip(vals, shifted["financial_series_point_in_time"][tag]):
            assert w["filed"] != v["filed"] and w["end"] != v["end"]


def test_original_payload_not_mutated():
    before = json.dumps(FIXTURE, sort_keys=True)
    shift_payload(FIXTURE)
    assert json.dumps(FIXTURE, sort_keys=True) == before


def test_shift_date_roundtrip():
    assert shift_date("2015-06-30", 7) == "2015-07-07"
    assert shift_date("2015-06-30", -7) == "2015-06-23"
