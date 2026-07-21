import json
from pathlib import Path

import verify_blindness as vb


def write_json(root: Path, relative: str, value) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def registry(*, perturbed=None, aux=None) -> dict:
    return {"experiments": [{
        "name": "wave_test", "score_commit": "UNKNOWN",
        "label_join_commit": "UNKNOWN", "analysis_commit": "UNKNOWN",
        "output_globs": [], "perturbed_globs": perturbed or [],
        "aux_globs": aux or [],
        "perturbed_treatment_ids": "ids.json",
        "names_mapping": "mapping.json", "names_candidates": "candidates.json",
    }]}


def identity_files(root: Path, candidates=None, mapping=None) -> None:
    write_json(root, "ids.json", {"cases": [{"case_id": "case_01"}]})
    write_json(root, "mapping.json", {"mapping": mapping or {"case_01": "T01"}})
    if candidates is None:
        candidates = [{"case_id": "T01", "company_name": "Zebra Corp", "ticker": "ZBRA"}]
    write_json(root, "candidates.json", {"candidates": candidates})


def semantic_failures(root: Path, reg: dict) -> list[str]:
    vb.FAILS.clear()
    vb.WARNS.clear()
    vb.check_semantic_scans(root, reg)
    return list(vb.FAILS)


def test_synthetic_real_name_leak(tmp_path):
    reg = registry(perturbed=["runs/wave_test/**/*.json"])
    identity_files(tmp_path)
    write_json(tmp_path, "runs/wave_test/case_01.json", {"text": "Zebra Corp"})
    assert any("실명" in failure for failure in semantic_failures(tmp_path, reg))


def test_unregistered_surface_fails(tmp_path):
    write_json(tmp_path, "runs/rogue/case_01.json", {})
    assert any("unregistered output surface" in failure
               for failure in semantic_failures(tmp_path, {"experiments": []}))


def test_derivation_missing_mapping_fails_closed(tmp_path):
    reg = registry(perturbed=["runs/wave_test/**/*.json"])
    identity_files(tmp_path, mapping={"different": "T01"})
    write_json(tmp_path, "runs/wave_test/case_01.json", {})
    assert any("이름 파생 실패" in failure for failure in semantic_failures(tmp_path, reg))


def test_derivation_empty_candidates_fails_closed(tmp_path):
    reg = registry(perturbed=["runs/wave_test/**/*.json"])
    identity_files(tmp_path, candidates=[])
    write_json(tmp_path, "runs/wave_test/case_01.json", {})
    assert any("이름 파생 실패" in failure for failure in semantic_failures(tmp_path, reg))


def test_wave1_distinctive_name_variants():
    real_registry = vb.load_registry(vb.REPO)
    wave1 = next(exp for exp in real_registry["experiments"] if exp["name"] == "wave1")
    patterns = vb.derive_treatment_patterns(vb.REPO, wave1)
    assert patterns is not None
    for name in ("comscore", "orthofix", "logitech", "monsanto", "hertz",
                 "iconix", "kraft heinz", "marvell"):
        assert patterns[0].search(name), name


def test_registered_clean_perturbed_passes_semantic_scan(tmp_path):
    reg = registry(perturbed=["runs/wave_test/**/*.json"])
    identity_files(tmp_path)
    write_json(tmp_path, "runs/wave_test/case_01.json", {"text": "clean output"})
    assert semantic_failures(tmp_path, reg) == []


def test_perturbed_precedes_aux(tmp_path):
    reg = registry(perturbed=["runs/wave_test/**/*.json"],
                   aux=["runs/**/*.json"])
    identity_files(tmp_path)
    write_json(tmp_path, "runs/wave_test/case_01.json", {"text": "Zebra"})
    assert any("실명" in failure for failure in semantic_failures(tmp_path, reg))
