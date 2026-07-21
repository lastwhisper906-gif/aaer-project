import copy
import json
from pathlib import Path
from types import SimpleNamespace

import jsonschema
import pytest

import runner


REPO_ROOT = Path(__file__).resolve().parent.parent


def _evidence():
    return {"quote": "Revenue=1 (FY2020)", "source_accession_no": "a", "location": "Revenue FY2020"}


def _hypothesis():
    return {
        "affected_line_items": ["Revenue"],
        "direction": "overstated",
        "accounting_treatment": "recognition timing",
        "rationale_evidence": [_evidence()],
    }


def _model_output():
    return {
        "checklist": [{
            "item_id": "CL1", "question": "q", "finding": "no_flag", "confidence": "low",
            "evidence": [_evidence()],
        }],
        "misstatement_probability": 20,
        "mechanism_hypotheses": [_hypothesis()],
        "overall": {"risk_tier": "clear", "top_signals": []},
    }


def _full_output(model_output):
    return {
        "case_id": "case_99", "run_id": "original-case_99-r1", "model": "claude-sonnet-5",
        "pipeline_version": "a" * 40, "run_timestamp": "2026-07-21T00:00:00+00:00",
        "documents_used": [{"accession_no": "a", "form_type": "10-K", "filing_date": "2020-01-01"}],
        **model_output,
    }


@pytest.fixture(params=["probability", "empty_evidence", "four_hypotheses", "conditional"])
def invalid_model_output(request):
    output = _model_output()
    if request.param == "probability":
        output["misstatement_probability"] = 130
    elif request.param == "empty_evidence":
        output["checklist"][0]["evidence"] = []
    elif request.param == "four_hypotheses":
        output["mechanism_hypotheses"] = [_hypothesis() for _ in range(4)]
    else:
        output["misstatement_probability"] = 55
        output["mechanism_hypotheses"] = []
    return output


def test_invalid_outputs_rejected_by_model_and_full_schemas(invalid_model_output):
    assert list(jsonschema.Draft7Validator(runner.MODEL_SCHEMA).iter_errors(invalid_model_output))
    assert list(jsonschema.Draft7Validator(runner.FULL_OUTPUT_SCHEMA).iter_errors(
        _full_output(invalid_model_output)))


def test_model_schema_is_derived_with_all_constraints():
    schema = runner.derive_model_schema(runner.FULL_OUTPUT_SCHEMA)
    properties = schema["properties"]
    assert properties["misstatement_probability"]["minimum"] == 0
    assert properties["misstatement_probability"]["maximum"] == 100
    assert properties["mechanism_hypotheses"]["maxItems"] == 3
    assert properties["checklist"]["minItems"] == 1
    assert properties["checklist"]["items"]["properties"]["evidence"]["minItems"] == 1
    assert properties["mechanism_hypotheses"]["items"]["properties"]["rationale_evidence"]["minItems"] == 1
    assert schema["allOf"][0]["if"]["properties"]["misstatement_probability"]["minimum"] == 40
    assert schema["allOf"][0]["then"]["properties"]["mechanism_hypotheses"]["minItems"] == 1


def test_run_case_revalidates_before_write(monkeypatch, tmp_path):
    invalid = _model_output()
    invalid["misstatement_probability"] = 130
    payload = {
        "_k_internal": 1.0,
        "case": {"company_name": "Example", "ticker": "EX"},
        "financial_series_point_in_time": {
            "Revenue": [{"accession": "a", "form": "10-K", "filed": "2020-01-01"}]
        },
    }
    monkeypatch.setattr(runner.bp, "build_payload", lambda case, perturb: copy.deepcopy(payload))
    monkeypatch.setattr(runner.cli_client, "call_model", lambda *args, **kwargs: SimpleNamespace(
        ok=True, structured=invalid, fail_reason=None, served_models=[runner.EVALUATEE_MODEL]))
    monkeypatch.setattr(runner, "freeze_state", lambda: {"head": "a" * 40})
    out_dir = tmp_path / "runs"
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    case = {"case_id": "case_99", "company_name": "Example", "ticker": "EX",
            "cik": "1", "cutoff_date": "2020-01-01"}

    result = runner.run_case(case, False, out_dir, log_dir)

    assert result["status"] == "FAIL (schema_violation: misstatement_probability)"
    assert not (out_dir / "case_99.json").exists()
    meta = json.loads((log_dir / "runmeta_original_case_99.json").read_text(encoding="utf-8"))
    assert meta["fail_reason"] == "schema_violation: misstatement_probability"


def test_all_committed_run_outputs_validate():
    patterns = (
        "runs/*/case_*.json", "runs/*/scores/*.json", "runs/wave2/perturbed/*.json",
        "pilot/runs/case_*.json",
    )
    paths = sorted({path for pattern in patterns for path in REPO_ROOT.glob(pattern)})
    assert paths
    validator = jsonschema.Draft7Validator(runner.FULL_OUTPUT_SCHEMA)
    failures = []
    for path in paths:
        errors = list(validator.iter_errors(json.loads(path.read_text(encoding="utf-8"))))
        if errors:
            failures.append(f"{path.relative_to(REPO_ROOT)}: {errors[0].message}")
    assert not failures, "\n".join(failures)
