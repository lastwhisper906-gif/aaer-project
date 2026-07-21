"""CI-safe payload tests against the committed synthetic SEC corpus."""
import datetime
import json
from pathlib import Path

import pytest

import build_payload as bp
from test_build_payload import FORBIDDEN_PAYLOAD_SUBSTRINGS


FIXTURES = Path(__file__).resolve().parent / "fixtures"
CORPUS = FIXTURES / "synthetic_corpus"
CASES = json.loads(
    (FIXTURES / "synthetic_cases.json").read_text(encoding="utf-8"))["cases"]


@pytest.fixture(autouse=True)
def synthetic_data_dir(monkeypatch):
    monkeypatch.setattr(bp, "DATA_DIR", CORPUS)


def _case(ticker):
    return next(case for case in CASES if case["ticker"] == ticker)


def _numeric_values(payload):
    for values in payload["financial_series_point_in_time"].values():
        for value in values:
            if isinstance(value["value"], (int, float)):
                yield value, value["value"]


def test_point_in_time_edges_and_duplicate_amendment_resolution():
    alpha = bp.build_payload(_case("SYNA"))
    alpha_values = alpha["financial_series_point_in_time"]["Revenues"]
    assert [(v["filed"], v["value"]) for v in alpha_values] == [
        ("2020-03-15", 1000000)]

    beta = bp.build_payload(_case("SYNB"))
    assert beta["financial_series_point_in_time"]["Assets"][0]["value"] == 3500000

    gamma = bp.build_payload(_case("SYNC"))
    survivor = gamma["financial_series_point_in_time"]["NetIncomeLoss"][0]
    assert survivor["value"] == 4750000
    assert survivor["accession"] == "0000000001-22-000003"
    assert {row["form"] for row in gamma["filing_chronology"]} == {"10-K", "10-K/A"}


def test_multi_submission_chronology_is_merged_sorted_and_deduped():
    payload = bp.build_payload(_case("SYND"))
    assert payload["filing_chronology"] == [
        {"form": "10-K", "filing_date": "2023-02-01"},
        {"form": "10-Q", "filing_date": "2023-05-01"},
    ]


def test_all_cases_respect_cutoff_and_have_no_leakage_markers():
    for case in CASES:
        payload = bp.build_payload(case)
        cutoff = datetime.date.fromisoformat(case["cutoff_date"])
        assert all(
            datetime.date.fromisoformat(value["filed"]) <= cutoff
            for values in payload["financial_series_point_in_time"].values()
            for value in values)
        text = json.dumps(payload, ensure_ascii=False).lower()
        assert not [marker for marker in FORBIDDEN_PAYLOAD_SUBSTRINGS
                    if marker.lower() in text]


def test_all_cases_perturb_deterministically_and_preserve_ratios_and_identity():
    for case in CASES:
        original = bp.build_payload(case)
        first = bp.build_payload(case, perturb=True)
        second = bp.build_payload(case, perturb=True)
        assert first == second
        k = first["_k_internal"]
        assert 0.4 <= k <= 2.5
        perturbed_values = list(_numeric_values(first))
        original_values = list(_numeric_values(original))
        assert len(perturbed_values) == len(original_values)
        for ((before_meta, before), (after_meta, after)) in zip(
                original_values, perturbed_values):
            assert after / before == pytest.approx(k, abs=1e-6)
            assert (after_meta["start"], after_meta["end"], after_meta["filed"]) == (
                before_meta["start"], before_meta["end"], before_meta["filed"])
        masked = first["case"]
        assert masked["ticker"].startswith("XX")
        assert masked["company_name"].startswith("Company ")
        assert "cik" not in masked
        assert masked["cutoff_date"] == case["cutoff_date"]
        assert first["filing_chronology"] == original["filing_chronology"]
