import math
import random

from aaer_eval.statistics import (
    auc,
    boot_auc_ci,
    cliffs_delta,
    fisher_one_sided,
    fpr_bound,
    median,
    perm_test_mean,
    residuals,
    spearman,
)


def test_spearman_is_tie_aware():
    x = [1, 1, 2, 3]
    y = [1, 2, 2, 3]

    def naive_distinct_ranks(values):
        ranks = [0] * len(values)
        for rank, index in enumerate(sorted(range(len(values)), key=values.__getitem__), 1):
            ranks[index] = rank
        return ranks

    naive = spearman(naive_distinct_ranks(x), naive_distinct_ranks(y))
    tied = spearman(x, y)
    assert tied == 5 / 6
    assert tied != naive


def test_spearman_degenerate_inputs():
    assert spearman([1, 1, 1], [1, 2, 3]) is None
    assert spearman([1], [2]) is None


def test_permutation_is_deterministic_and_one_sided():
    a, b = [10, 11, 12, 13], [0, 1, 2, 3]
    first = perm_test_mean(a, b, random.Random(7), n=5_000)
    second = perm_test_mean(a, b, random.Random(7), n=5_000)
    assert first == second
    assert first[0] < 0.05
    assert perm_test_mean([1, 2, 3], [1, 2, 3], random.Random(8), n=1_000)[0] > 0.4


def test_fisher_matches_independent_hypergeometric_sum():
    tp, fn, fp, tn = 7, 2, 5, 18
    total, row1, col1 = tp + fn + fp + tn, tp + fn, tp + fp
    expected = sum(
        math.comb(row1, x) * math.comb(total - row1, col1 - x) / math.comb(total, col1)
        for x in range(tp, min(row1, col1) + 1)
    )
    assert math.isclose(fisher_one_sided(tp, fn, fp, tn), expected)


def test_auc_ties_and_basic_wrappers():
    assert auc([2, 1], [1, 0]) == 0.875
    assert cliffs_delta([2, 1], [1, 0]) == 0.75
    assert median([3, 1, 2]) == 2


def test_boot_auc_ci_is_deterministic_and_contains_auc():
    a, b = [4, 5, 6, 7], [0, 1, 2, 3]
    first = boot_auc_ci(a, b, random.Random(9), n=1_000)
    second = boot_auc_ci(a, b, random.Random(9), n=1_000)
    assert first == second
    assert first[0] <= auc(a, b) <= first[1]


def test_fpr_bounds_match_published_values():
    assert fpr_bound(0, 22) == {
        "fp": 0, "n": 22, "rule": "rule-of-three", "upper95_pct": 13.6
    }
    bound = fpr_bound(5, 23)
    assert bound["lo_pct"] == 7.5
    assert bound["upper95_pct"] == 43.7


def test_residuals_linear_and_degenerate_x():
    assert residuals([3, 5, 7], [1, 2, 3]) == [0.0, 0.0, 0.0]
    assert residuals([1, 2, 6], [4, 4, 4]) == [-2.0, -1.0, 3.0]
