import copy
import hashlib
import json
from types import SimpleNamespace

import runner


CASE = {"case_id": "case_99", "company_name": "Example", "ticker": "EX",
        "cik": "1", "cutoff_date": "2020-01-01"}
PAYLOAD = {
    "_k_internal": 1.0,
    "case": {"company_name": "Example", "ticker": "EX"},
    "financial_series_point_in_time": {
        "Revenue": [{"accession": "a", "form": "10-K", "filed": "2020-01-01"}]
    },
}
MODEL_OUTPUT = {
    "checklist": [{
        "item_id": "CL1", "question": "q", "finding": "no_flag", "confidence": "low",
        "evidence": [{"quote": "Revenue=1 (FY2020)", "source_accession_no": "a",
                      "location": "Revenue FY2020"}],
    }],
    "misstatement_probability": 20,
    "mechanism_hypotheses": [],
    "overall": {"risk_tier": "clear", "top_signals": []},
}


def _setup(monkeypatch):
    monkeypatch.setattr(runner.bp, "build_payload",
                        lambda case, perturb: copy.deepcopy(PAYLOAD))
    monkeypatch.setattr(runner, "freeze_state", lambda: {"head": "a" * 40})
    monkeypatch.setattr(runner, "get_harness_version", lambda: "claude-test")


def _call_result():
    return SimpleNamespace(ok=True, structured=copy.deepcopy(MODEL_OUTPUT), fail_reason=None,
                           served_models=[runner.EVALUATEE_MODEL])


def _run(monkeypatch, tmp_path, call_model=None):
    _setup(monkeypatch)
    monkeypatch.setattr(runner.cli_client, "call_model", call_model or (lambda *a, **k: _call_result()))
    out_dir = tmp_path / "runs"
    log_dir = tmp_path / "logs"
    log_dir.mkdir(exist_ok=True)
    result = runner.run_case(CASE, False, out_dir, log_dir)
    return result, out_dir


def _never_called(*args, **kwargs):
    raise AssertionError("call_model must not be called")


def test_identical_fingerprint_skips(monkeypatch, tmp_path):
    _, out_dir = _run(monkeypatch, tmp_path)
    result, _ = _run(monkeypatch, tmp_path, _never_called)
    assert result["status"].startswith("skip")


def test_changed_prompt_writes_versioned_sibling_without_touching_original(monkeypatch, tmp_path):
    _, out_dir = _run(monkeypatch, tmp_path)
    original = out_dir / "case_99.json"
    original_bytes = original.read_bytes()
    monkeypatch.setattr(runner, "TASK", runner.TASK + "\nChanged instruction.")

    result, _ = _run(monkeypatch, tmp_path)

    assert "stale-superseding" in result["status"]
    assert original.read_bytes() == original_bytes
    siblings = list(out_dir.glob("case_99.fp-*.json"))
    assert len(siblings) == 1
    assert json.loads(siblings[0].read_text())["fingerprint"]["system_prompt_sha256"] != \
        json.loads(original.read_text())["fingerprint"]["system_prompt_sha256"]


def test_legacy_valid_output_skips(monkeypatch, tmp_path):
    _, out_dir = _run(monkeypatch, tmp_path)
    path = out_dir / "case_99.json"
    legacy = json.loads(path.read_text())
    legacy.pop("fingerprint")
    path.write_text(json.dumps(legacy), encoding="utf-8")

    result, _ = _run(monkeypatch, tmp_path, _never_called)
    assert "legacy" in result["status"]


def test_new_output_embeds_computed_fingerprint(monkeypatch, tmp_path):
    result, out_dir = _run(monkeypatch, tmp_path)
    assert result["status"].startswith("OK")
    record = json.loads((out_dir / "case_99.json").read_text())
    payload = copy.deepcopy(PAYLOAD)
    payload.pop("_k_internal")
    user_payload = json.dumps(payload, ensure_ascii=False)
    task = runner.TASK.format(company_name="Example", ticker="EX", cik_part=", CIK 1",
                              cutoff_date="2020-01-01")
    assert record["fingerprint"] == runner.compute_fingerprint(CASE, task, user_payload)


def test_stale_versioned_path_is_deterministic(monkeypatch, tmp_path):
    _, out_dir = _run(monkeypatch, tmp_path)
    original = out_dir / "case_99.json"
    record = json.loads(original.read_text())
    record["fingerprint"]["model_requested"] = "old-model"
    original.write_text(json.dumps(record), encoding="utf-8")

    _run(monkeypatch, tmp_path)
    sibling = next(out_dir.glob("case_99.fp-*.json"))
    first = json.loads(sibling.read_text())
    _run(monkeypatch, tmp_path)
    siblings = list(out_dir.glob("case_99.fp-*.json"))
    second = json.loads(siblings[0].read_text())

    assert len(siblings) == 1
    first.pop("run_timestamp")
    second.pop("run_timestamp")
    assert first == second
    canonical = json.dumps(second["fingerprint"], sort_keys=True, ensure_ascii=False)
    assert sibling.name == f"case_99.fp-{hashlib.sha256(canonical.encode()).hexdigest()[:8]}.json"
