"""E2 통합 인터페이스 계약 — b3_score와 b4_score 병행 호출 가능성 (스펙 §8).

동결 E2 계획(EARLINESS_PLAN.md)의 스냅샷 루프가 무수정으로 두 기준선을 함께
계산할 수 있음을 기계로 보증한다: 동일 (ticker, cutoff) 호출 형태, dict 반환,
결측은 예외가 아니라 플래그(B4) — 스냅샷 하나의 데이터 구멍이 궤적 전체를
죽이지 않는다.
"""
import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

from b3_compute import b3_score  # noqa: E402
from b4_short_interest import b4_score  # noqa: E402

FIXTURES = REPO / "pipeline" / "fixtures" / "data"  # TST: edgar + xbrl 동반
CUTOFF = datetime.date(2015, 8, 1)
SPEC_KEYS = {"score_level", "score_slope_aug", "sir_last", "abnormal_sir_last",
             "slope4", "n_reports_trailing12m", "last_settlement", "flags", "cutoff",
             "shares_source"}  # shares_source = §13/D56 개정의 §8 반환 확장
SPEC_FLAGS = {"insufficient_history", "no_si_file", "no_shares_denominator",
              "slope_unavailable", "revision_seen_diagnostic"}


def test_side_by_side_snapshot_call(tmp_path):
    """E2 루프 형태 그대로: 스냅샷 컷오프 하나에 두 점수를 연달아 계산."""
    si_dir = tmp_path / "si"
    si_dir.mkdir()  # 아카이브 디렉토리 부재 = raise (인프라 오류) / 빈 아카이브 = 플래그
    b3 = b3_score("TST", CUTOFF, 730, data_dir=FIXTURES)
    b4 = b4_score("TST", CUTOFF, data_dir=si_dir, facts_dir=FIXTURES)
    assert isinstance(b3, dict) and isinstance(b4, dict)
    assert b3["cutoff"] == b4["cutoff"] == str(CUTOFF)
    assert isinstance(b3["score"], int)
    # SI 아카이브가 없는 스냅샷: B4는 예외가 아니라 None+플래그 (E2 루프 보존)
    assert b4["score_slope_aug"] is None and b4["flags"]["no_si_file"]


def test_b4_return_shape_matches_spec_contract(tmp_path):
    (tmp_path / "si").mkdir()
    b4 = b4_score("TST", CUTOFF, data_dir=tmp_path / "si", facts_dir=FIXTURES)
    assert set(b4) == SPEC_KEYS, f"스펙 §8 반환 키 불일치: {set(b4) ^ SPEC_KEYS}"
    assert set(b4["flags"]) == SPEC_FLAGS


def test_both_deterministic(tmp_path):
    args3 = ("TST", CUTOFF, 730)
    assert b3_score(*args3, data_dir=FIXTURES) == b3_score(*args3, data_dir=FIXTURES)
    si = tmp_path / "si"
    si.mkdir()
    assert (b4_score("TST", CUTOFF, data_dir=si, facts_dir=FIXTURES)
            == b4_score("TST", CUTOFF, data_dir=si, facts_dir=FIXTURES))
