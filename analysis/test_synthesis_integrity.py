import json

import pytest

import synthesis


def _write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _holdout_repo(tmp_path):
    candidates = []
    for case_id, ticker in (("C1", "TRUE"), ("C2", "FALSE"), ("C3", "MISSING")):
        candidates.append({"case_id": case_id, "ticker": ticker})
        _write_json(
            tmp_path / f"runs/holdout/scores/{case_id}.json",
            {"misstatement_probability": 50},
        )
    _write_json(
        tmp_path / "data/candidates/candidates_holdout.json",
        {"candidates": candidates},
    )
    _write_json(tmp_path / "runs/holdout/recognition/TRUE.json", {"knows_event": True})
    _write_json(tmp_path / "runs/holdout/recognition/FALSE.json", {"knows_event": False})


def test_holdout_recognition_and_row_shape(tmp_path, monkeypatch):
    _holdout_repo(tmp_path)
    monkeypatch.setattr(synthesis, "run_case", lambda candidate: {})
    exclusions = []

    rows = synthesis.rows_holdout(exclusions, repo=tmp_path)

    assert [row["recognized"] for row in rows] == [True, False, None]
    assert len(set(row["recognized"] for row in rows)) == 3
    assert exclusions == [{
        "case_id": "C3",
        "ticker": "MISSING",
        "stage": "holdout_recognition",
        "exception_class": "FileNotFoundError",
        "message": str(tmp_path / "runs/holdout/recognition/MISSING.json"),
        "classification": "data_missing",
    }]
    assert set(rows[0]) == {
        "wave", "case_id", "ticker", "group", "llm_score", "flag", "llm_perturbed",
        "perturb_delta", "recognized", "m_score", "m_flag", "f_score", "f_flag",
    }


def test_baseline_records_data_failure_and_propagates_code_failure(monkeypatch):
    exclusions = []

    def missing(_candidate):
        raise FileNotFoundError("fixture absent")

    monkeypatch.setattr(synthesis, "run_case", missing)
    assert synthesis.baseline_mf({"case_id": "C1", "ticker": "ABC"}, exclusions) == (None, None)
    assert exclusions[0] == {
        "case_id": "C1",
        "ticker": "ABC",
        "stage": "baseline_mf",
        "exception_class": "FileNotFoundError",
        "message": "fixture absent",
        "classification": "data_missing",
    }

    def bug(_candidate):
        raise RuntimeError("bug")

    monkeypatch.setattr(synthesis, "run_case", bug)
    with pytest.raises(RuntimeError, match="bug"):
        synthesis.baseline_mf({"case_id": "C2", "ticker": "XYZ"}, exclusions)


def test_main_writes_exclusion_artifact(tmp_path, monkeypatch):
    record = {"stage": "fixture", "classification": "data_missing"}
    monkeypatch.setattr(synthesis, "rows_wave1", lambda exclusions, repo: [])
    monkeypatch.setattr(synthesis, "rows_wave2", lambda exclusions, repo: [])
    monkeypatch.setattr(
        synthesis,
        "separation",
        lambda rows, rng: {"auc": 0.5, "auc_ci": [0.5, 0.5]},
    )
    monkeypatch.setattr(synthesis, "name_id_rate", lambda rows: 0.0)

    def holdout(exclusions, repo):
        exclusions.append(record)
        return []

    monkeypatch.setattr(synthesis, "rows_holdout", holdout)
    out_dir = tmp_path / "generated"
    out_dir.mkdir()

    assert synthesis.main(repo=tmp_path, out_dir=out_dir) == 0
    artifact = json.loads((out_dir / "out/synthesis_exclusions.json").read_text(encoding="utf-8"))
    assert artifact == {
        "generated_by": "analysis/synthesis.py",
        "excluded_n": 1,
        "records": [record],
    }
