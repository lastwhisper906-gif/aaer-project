"""E2 생성기 계약 테스트 (D66) — 합성 픽스처, 네트워크 0, 호출 0.

느린 실데이터 검증(146 전수·이중 생성 바이트 동일)은 생성 세션이 1회 수행하고
D-엔트리에 기록 — 여기는 규칙 단위의 빠른 계약만.
"""
import copy
import datetime
import json
from pathlib import Path

import pytest

import cutoff_guard
import e2_generate_cases as gen

TICKER = "E2T"
CUTOFF = "2016-02-28"


def seed_ticker(root: Path, n_filings: int, first_10k_every: int = 4,
                start_year: int = 2011, all_xbrl: bool = True):
    """분기 간격 합성 제출 이력 + 최소 companyfacts."""
    forms, dates, accs, isx = [], [], [], []
    y, m = start_year, 2
    for i in range(n_filings):
        forms.append("10-K" if i % first_10k_every == 0 else "10-Q")
        dates.append(f"{y:04d}-{m:02d}-15")
        accs.append(f"{1000000000+i:010d}-{y % 100:02d}-{i:06d}")
        isx.append(1 if all_xbrl else 0)
        m += 3
        if m > 12:
            m -= 12; y += 1
    edgar = root / TICKER / "edgar"; edgar.mkdir(parents=True)
    edgar.joinpath("CIK0000000001.json").write_text(json.dumps(
        {"filings": {"recent": {"form": forms, "filingDate": dates,
                                "accessionNumber": accs, "isXBRL": isx}}}))
    xbrl = root / TICKER / "xbrl"; xbrl.mkdir(parents=True)
    facts = {"us-gaap": {"Assets": {"units": {"USD": [
        {"start": None, "end": d, "val": 100.0 + i, "accn": a, "filed": d,
         "form": f, "fy": 2015, "fp": "Q1"}
        for i, (d, a, f) in enumerate(zip(dates, accs, forms))]}}}}
    xbrl.joinpath("CIK0000000001.json").write_text(json.dumps({"facts": facts}))
    return dates


# ---------------------------------------------------------------- grid rule

def test_grid_eligibility_rules(tmp_path):
    dates = seed_ticker(tmp_path, 8)  # k=8 → 잔존>=6 은 j<=3
    fs = gen.xbrl_filings(TICKER, "2020-01-01", data_dir=tmp_path)
    assert len(fs) == 8 and fs[0]["filed"] == dates[-1]
    grid = gen.snapshot_grid(fs)
    assert [g["eligible"] for g in grid] == [True, True, True] + [False] * 5
    assert grid[3]["reason"] == "insufficient_remaining"
    # 컷오프 = filed + 1일
    assert grid[0]["cutoff"] == str(
        datetime.date.fromisoformat(dates[-1]) + datetime.timedelta(days=1))


def test_grid_requires_10k_in_remaining(tmp_path):
    # 10-K가 최신 1건뿐 → j=2부터 잔존에 10-K 없음
    seed_ticker(tmp_path, 8, first_10k_every=8)
    fs = gen.xbrl_filings(TICKER, "2020-01-01", data_dir=tmp_path)
    tenk_pos = [i for i, d in enumerate(fs) if d["form"] == "10-K"]
    grid = gen.snapshot_grid(fs)
    for g in grid:
        if g["eligible"]:
            assert any(d["form"] == "10-K" for d in fs[g["j"] - 1:])


def test_non_xbrl_filings_excluded(tmp_path):
    seed_ticker(tmp_path, 8, all_xbrl=False)
    assert gen.xbrl_filings(TICKER, "2020-01-01", data_dir=tmp_path) == []


# ---------------------------------------------------------------- roster (실저장소, 읽기 전용)

def test_roster_equals_plan_rule_output():
    roster = gen.derive_roster()
    treat = sorted(c["base_case"]["ticker"] for c in roster if c["group"] == "treatment")
    assert treat == sorted(["OFIX", "HTZ", "ICON", "MRVL", "SCOR", "KHC",
                            "WFT", "CGI", "MDXG", "HAIN", "OSIR", "TNGO", "UAA"])
    assert len([c for c in roster if c["group"] == "control"]) == 8
    # 규칙에 의한 자동 탈락 — 명시 제외 목록이 없음을 확인
    assert not {"MON", "CSC", "BRX"} & set(treat)


# ---------------------------------------------------------------- anti-leak

def test_antileak_detects_injected_future_fact():
    payload = {"financial_series_point_in_time":
               {"us-gaap:Assets": [{"filed": "2016-03-01", "value": 1}]},
               "filing_chronology": []}
    with pytest.raises(gen.E2GenError, match="LEAK"):
        gen.assert_no_leak(payload, CUTOFF)


def test_antileak_detects_future_chronology():
    payload = {"financial_series_point_in_time": {},
               "filing_chronology": [{"form": "8-K", "filing_date": "2016-02-29"}]}
    with pytest.raises(gen.E2GenError, match="LEAK"):
        gen.assert_no_leak(payload, CUTOFF)


# ---------------------------------------------------------------- guard integration

def test_guard_blocks_post_cutoff_document(tmp_path):
    reg = tmp_path / "reg.json"
    reg.write_text(json.dumps({"candidates": [
        {"case_id": "case_99_s1", "ticker": TICKER, "cutoff_date": CUTOFF}]}))
    payload = {"financial_series_point_in_time":
               {"t": [{"filed": "2016-03-01", "accession": None, "form": "10-K",
                       "value": 1}]},
               "filing_chronology": []}
    with pytest.raises(cutoff_guard.CutoffViolationError):
        gen.guard_pass("case_99_s1", TICKER, payload, reg,
                       data_dir=tmp_path)


def test_guard_blocks_unknown_snapshot_id(tmp_path):
    reg = tmp_path / "reg.json"
    reg.write_text(json.dumps({"candidates": []}))
    payload = {"financial_series_point_in_time":
               {"t": [{"filed": "2016-01-01", "accession": None, "form": "10-K",
                       "value": 1}]},
               "filing_chronology": []}
    with pytest.raises(cutoff_guard.CutoffGuardError):
        gen.guard_pass("case_98_s1", TICKER, payload, reg, data_dir=tmp_path)


# ---------------------------------------------------------------- end-to-end (픽스처)

def _fixture_roster(tmp_path, n_filings=14):
    seed_ticker(tmp_path / "data", n_filings)
    return [{"tier": "wave1", "group": "treatment", "reg_id": "T99",
             "base_case": {"case_id": "case_99", "ticker": TICKER,
                           "cik": "0000000001", "company_name": "E2 Test Co",
                           "cutoff_date": "2020-01-01"},
             "base_cutoff": "2020-01-01"}]


def test_generation_deterministic_and_accounted(tmp_path, monkeypatch):
    roster = _fixture_roster(tmp_path)
    monkeypatch.setattr(gen, "derive_roster", lambda repo=None: roster)
    monkeypatch.setattr(gen.bp, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(gen, "b3_score", lambda *a, **k: {
        "score": 0, "indicators": {}, "flags": {"insufficient_history": True}})
    monkeypatch.setattr(gen, "b4_score", lambda *a, **k: {
        "score_slope_aug": None, "score_level": None, "flags": {"no_si_file": True}})
    outs = []
    for run in ("a", "b"):
        out = tmp_path / run
        m = gen.generate(out_root=out, data_dir=tmp_path / "data", repo=REPO_STUB)
        files = {p.name: p.read_bytes() for p in sorted(out.iterdir())}
        outs.append((m, files))
    assert outs[0][1] == outs[1][1]                      # 바이트 동일 (결정론)
    m = outs[0][0]
    # 회계: k=14 → 잔존>=6 은 j<=8 전부(14-7=7>=6... j=8 잔존 7), buildable 8
    assert m["totals"]["buildable"] == 8
    assert m["totals"]["buildable"] + m["totals"]["grid_ineligible"] == 8  # cap 행 전수
    assert m["budget_of_record"] == {"evaluatee_calls": 8, "grader_calls": 0,
                                     "cite": "D65 주석 2"}
    # 기록 파일: b4 not_computable 상태가 생략되지 않고 기록됨 (D61)
    rec = json.loads((tmp_path / "a" / "case_99_s1.json").read_text())
    assert rec["b4"]["state"] == "not_computable"
    assert rec["payload_sha256"] == json.loads(
        (tmp_path / "b" / "case_99_s1.json").read_text())["payload_sha256"]
    # 러너 배치는 evaluatee 5필드만
    batch = json.loads((tmp_path / "a" / "cases_e2_s1.json").read_text())
    assert set(batch["cases"][0]) == {"case_id", "ticker", "cik",
                                      "company_name", "cutoff_date"}


REPO_STUB = None  # derive_roster가 monkeypatch되므로 미사용
