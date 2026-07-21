from pathlib import Path

from aaer_eval.verdict import fired_rule, r1_fires, r2_fires, r3_case_counts, r3_fires
from analysis.wave2_analyze import compute_results


def fixture(incomplete=False):
    fraud = {"f1": 90, "f2": 80, "f3": None if incomplete else 70}
    control = {"c1": 10, "c2": 20, "c3": 30}
    perturbed = {"f1": 40, "f2": 75, "f3": 60}
    m_pairs = [(90, 3, "fraud"), (80, 2, "fraud"),
               (10, -2, "control"), (20, -1, "control")]
    f_pairs = [(90, 1.5, "fraud"), (80, 1.2, "fraud"),
               (10, 0.2, "control"), (20, 0.4, "control")]
    return compute_results(
        fraud, control, perturbed, m_pairs, f_pairs,
        seed=17, n_perm=2_000, n_boot=500,
    )


def test_r2_requires_positive_rho():
    assert not r2_fires(-0.8, 0.9)


def test_r2_requires_residual_null():
    assert not r2_fires(0.9, 0.01)
    assert r2_fires(0.9, 0.5)


def test_r1_null_on_nonsignificance():
    assert r1_fires(0.05)
    assert not r1_fires(0.049)


def test_r3_memorization_blocks_capability_claim():
    assert fired_rule(False, False, True) == "R3"
    assert fired_rule(True, False, True) == "R1"


def test_r3_denominator_auto_count():
    assert r3_case_counts(0, 20, 20)
    assert r3_case_counts(0, 19, 20)


def test_r3_requires_strict_majority():
    assert r3_fires(5, 9)
    assert r3_fires(5, 8)
    assert not r3_fires(4, 8)


def test_r4_conditions():
    assert fired_rule(False, False, False) == "R4"


def test_output_contains_fisher_exact():
    block = fixture()["fisher_2x2"]
    assert set(block) == {"tp", "fn", "fp", "tn", "one_sided_p"}
    assert 0 <= block["one_sided_p"] <= 1


def test_output_contains_cp_interval():
    block = fixture()["fpr"]
    assert block["rule"] == "rule-of-three"
    assert block["upper95_pct"] > 0


def test_output_contains_worst_case_substitution():
    block = fixture()["worst_case_substitution"]
    assert block["n_incomplete"] == 0
    assert block["perm_p"] == fixture()["original"]["perm_p"]


def test_output_contains_residual_test():
    baselines = fixture()["baselines"]
    for block in baselines.values():
        assert "rho" in block
        assert 0 <= block["residual_perm_p"] <= 1


def test_output_contains_perturbed_frame():
    block = fixture()["perturbed_frame"]
    assert block["available"]
    assert block["n_perturbed"] == 3
    assert 0 <= block["perm_p"] <= 1


def test_worst_case_substitution_moves_p():
    result = fixture(incomplete=True)
    assert result["worst_case_substitution"]["n_incomplete"] == 1
    assert result["worst_case_substitution"]["perm_p"] >= result["original"]["perm_p"]


def test_rev2_never_writes_v1_paths():
    source = Path("analysis/wave2_analyze.py").read_text()
    assert "wave2_results.json" not in source
    assert "wave2_summary.md" not in source
