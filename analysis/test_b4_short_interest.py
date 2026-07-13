"""B4 테스트 계약 (specs/B4_short_interest.md §10).

코어 산술(PIT 경계·중앙값·slope·분모 밴드·파서)의 정본 테스트는 screener
tests/test_short_interest.py — 여기는 aaer-evals 측 계약만:
vendored 스냅샷 무결성, b4_score 래퍼의 fail-closed 계약, precision@k 산술.
4게이트 pytest 경로가 analysis/를 순회하지 않으므로 phase boundary에서 명시 실행
(B3 §10-5와 동일 규약): .venv/bin/python -m pytest analysis/ -q
"""
import datetime
import hashlib
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

from b4_short_interest import b4_score, precision_at_k  # noqa: E402


def test_vendor_integrity():
    """스냅샷 sha256 == PROVENANCE.md 기록 (수정은 원본 screener에서만)."""
    prov = (REPO / "analysis/vendor/PROVENANCE.md").read_text(encoding="utf-8")
    recorded = re.search(r"`short_interest\.py`.*`([0-9a-f]{64})`", prov).group(1)
    actual = hashlib.sha256(
        (REPO / "analysis/vendor/short_interest.py").read_bytes()).hexdigest()
    assert actual == recorded


def test_b4_score_missing_facts_flags_not_raises(tmp_path):
    """분모 소스(companyfacts) 부재 → 예외가 아니라 플래그 (E2 루프 보존)."""
    header = ("accountingYearMonthNumber|symbolCode|issueName|"
              "issuerServicesGroupExchangeCode|marketClassCode|"
              "currentShortPositionQuantity|previousShortPositionQuantity|"
              "stockSplitFlag|averageDailyVolumeQuantity|daysToCoverQuantity|"
              "revisionFlag|changePercent|changePreviousNumber|settlementDate")
    (tmp_path / "si").mkdir()
    (tmp_path / "si" / "shrt20200115.csv").write_text(
        header + "\n20200115|ZZZT|T|R|NNM|100|0||0|0.0||0|0|2020-01-15\n",
        encoding="utf-8")
    out = b4_score("ZZZT", datetime.date(2020, 6, 1),
                   data_dir=tmp_path / "si", facts_dir=tmp_path / "empty")
    assert out["score_level"] is None
    assert out["flags"]["no_shares_denominator"]


def test_precision_at_k_arithmetic_and_tiebreak():
    scored = [("c1", "treatment", 3.0), ("c2", "control", 2.0),
              ("c3", "treatment", 2.0), ("c4", "control", 1.0)]
    pk = precision_at_k(scored, k=2)
    # 동률(2.0)은 case_id 사전순 → c2가 c3보다 앞 (중립 결정론)
    assert pk["top_k_case_ids"] == ["c1", "c2"]
    assert pk["hits"] == 1 and pk["precision"] == 0.5


def test_dissemination_map_plumbing(monkeypatch):
    """§14 (D77): b4_score 기본 = 실측 매핑 전달, None 명시 = LAG 규칙(D66 관할)."""
    import datetime
    import b4_short_interest as b4m
    import short_interest as si_core
    seen = []
    monkeypatch.setattr(si_core, "b4_from_facts",
                        lambda t, c, d, f, dissemination_map=None:
                        seen.append(dissemination_map) or {"flags": {}})
    monkeypatch.setattr(b4m, "extract_share_facts", lambda *a: ({}, None))
    b4m.b4_score("TK", datetime.date(2020, 1, 1))
    b4m.b4_score("TK", datetime.date(2020, 1, 1), dissemination_map=None)
    assert seen[0] is b4m.DISSEMINATION_MAP and len(seen[0]) == 223
    assert seen[1] is None


def test_dissemination_map_covers_archive():
    """§14: 현 SI 아카이브 결제일 전수가 매핑에 존재 (D72 검증 4의 소비자측 재확인)."""
    from pathlib import Path
    import b4_short_interest as b4m
    missing = [p.stem[4:] for p in sorted(
        (Path.home() / "aaer-data" / "short_interest").glob("shrt*.csv"))
        if f"{p.stem[4:8]}-{p.stem[8:10]}-{p.stem[10:12]}" not in b4m.DISSEMINATION_MAP]
    assert missing == []
