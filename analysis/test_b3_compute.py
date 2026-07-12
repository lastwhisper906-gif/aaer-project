"""test_b3_compute.py — B3 계약 테스트 (specs/B3_metasignal.md §10).

주의: 4게이트 pytest 명령은 pipeline/ tools/ scoring/ 만 순회 — 본 파일은
phase 경계에서 명시 실행한다 (스펙 §10-5):
  .venv/bin/python -m pytest analysis/test_b3_compute.py -q
픽스처: pipeline/fixtures/data/{B3T,B3H} (B3T = 윈도 경계·다중 item·이력 부족,
B3H = 8-K 빈도 발화·충분 이력).
"""
import datetime
from pathlib import Path

import pytest

from b3_compute import B3Error, b3_score

FIXTURES = Path(__file__).resolve().parents[1] / "pipeline" / "fixtures" / "data"
CUT_B3T = datetime.date(2015, 6, 30)
CUT_B3H = datetime.date(2020, 12, 31)


# §10-1 윈도 경계: == cutoff 포함 · == cutoff − window_days 제외

def test_window_upper_edge_inclusive_at_cutoff():
    r = b3_score("B3T", CUT_B3T, 365, data_dir=FIXTURES)
    assert r["indicators"]["b_402"] == 1  # 4.02 8-K가 정확히 cutoff 당일


def test_window_lower_edge_exclusive():
    r = b3_score("B3T", CUT_B3T, 365, data_dir=FIXTURES)
    # 4.01 8-K는 정확히 cutoff − 365 (2014-06-30) → 윈도 밖
    assert r["indicators"]["b_401"] == 0


# §10-2 다중 item 문자열 정확 토큰 매칭

def test_multi_item_string_exact_token():
    r = b3_score("B3T", CUT_B3T, 365, data_dir=FIXTURES)
    assert r["indicators"]["b_402"] == 1   # "4.02, 9.01" (공백 포함) 토큰 매칭
    # "2.02,9.01" 행이 4.01/4.02로 오인되지 않음 (b_401=0은 위에서 검증)


# §10-3 insufficient-history fail-closed

def test_insufficient_history_fail_closed():
    r = b3_score("B3T", CUT_B3T, 365, data_dir=FIXTURES)
    assert r["flags"]["insufficient_history"] is True
    assert r["indicators"]["b_8kfreq"] == 0


def test_8kfreq_fires_with_sufficient_history():
    r = b3_score("B3H", CUT_B3H, 365, data_dir=FIXTURES)
    assert r["flags"]["insufficient_history"] is False
    assert r["counts"]["eightk_current"] == 3
    assert r["counts"]["eightk_trailing"] == [1, 1, 2]  # 중위 1 → 3 > 1.5
    assert r["indicators"]["b_8kfreq"] == 1


# §10-4 비가중 합

def test_unweighted_sum():
    r = b3_score("B3T", CUT_B3T, 365, data_dir=FIXTURES)
    assert r["indicators"]["b_nt"] == 1          # NT 10-Q 2015-05-11
    assert r["indicators"]["b_ka"] == 0          # 10-K/A는 윈도 밖 (2014-05-01)
    assert r["score"] == sum(r["indicators"].values()) == 2


def test_missing_submissions_fail_closed():
    with pytest.raises(B3Error):
        b3_score("NOSUCH", CUT_B3T, 365, data_dir=FIXTURES)
