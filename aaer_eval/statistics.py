"""Single canonical statistics module for AAER evaluation.

``analysis/stats.py`` is the frozen wave-1 executor and is intentionally
left untouched. New and rev2 analysis code MUST import statistics helpers
from this module. Beneish/Dechow baseline computation deliberately remains
in ``scoring/baselines/screens.py`` as its single source; copying it here
would recreate the duplication this module exists to eliminate.
"""

import math
import statistics


def spearman(x, y):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r

    rx, ry = ranks(x), ranks(y)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(
        sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)
    )
    return num / den if den else None


def perm_test_mean(a, b, rng, n=100_000):
    """One-sided permutation p-value for mean(a) > mean(b)."""
    obs = statistics.mean(a) - statistics.mean(b)
    pooled = list(a) + list(b)
    na = len(a)
    ge = 0
    for _ in range(n):
        rng.shuffle(pooled)
        if statistics.mean(pooled[:na]) - statistics.mean(pooled[na:]) >= obs - 1e-12:
            ge += 1
    return (ge + 1) / (n + 1), obs


def fisher_one_sided(tp, fn, fp, tn):
    """One-sided Fisher exact probability via the hypergeometric law."""
    n = tp + fn + fp + tn
    row1 = tp + fn
    col1 = tp + fp
    p = 0.0
    for x in range(tp, min(row1, col1) + 1):
        p += math.comb(row1, x) * math.comb(n - row1, col1 - x) / math.comb(n, col1)
    return p


def cliffs_delta(a, b):
    gt = lt = 0
    for x in a:
        for y in b:
            gt += x > y
            lt += x < y
    return (gt - lt) / (len(a) * len(b))


def auc(a, b):
    gt = eq = 0
    for x in a:
        for y in b:
            gt += x > y
            eq += x == y
    return (gt + 0.5 * eq) / (len(a) * len(b))


def boot_auc_ci(a, b, rng, n=10_000):
    vals = []
    for _ in range(n):
        ra = [a[rng.randrange(len(a))] for _ in a]
        rb = [b[rng.randrange(len(b))] for _ in b]
        vals.append(auc(ra, rb))
    vals.sort()
    return vals[int(0.025 * n)], vals[int(0.975 * n)]


def residuals(y, x):
    """Return OLS residuals for y ~ x."""
    mx, my = statistics.mean(x), statistics.mean(y)
    den = sum((a - mx) ** 2 for a in x)
    beta = sum((a - mx) * (b - my) for a, b in zip(x, y)) / den if den else 0.0
    alpha = my - beta * mx
    return [b - (alpha + beta * a) for a, b in zip(x, y)]


def fpr_bound(fp, n):
    if fp == 0:
        return {"fp": 0, "n": n, "rule": "rule-of-three", "upper95_pct": round(300 / n, 1)}

    def beta_inv(p, a, b):
        lo, hi = 0.0, 1.0
        from math import exp, lgamma, log

        def betacdf(x):
            n_steps = 20000
            s = 0.0
            for i in range(1, n_steps + 1):
                t = x * (i - 0.5) / n_steps
                s += exp(
                    (a - 1) * log(max(t, 1e-12))
                    + (b - 1) * log(max(1 - t, 1e-12))
                )
            s *= x / n_steps
            norm = exp(lgamma(a) + lgamma(b) - lgamma(a + b))
            return s / norm

        for _ in range(60):
            mid = (lo + hi) / 2
            if betacdf(mid) < p:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    lo = beta_inv(0.025, fp, n - fp + 1)
    hi = beta_inv(0.975, fp + 1, n - fp)
    return {
        "fp": fp,
        "n": n,
        "rule": "Clopper-Pearson 95%",
        "lo_pct": round(100 * lo, 1),
        "upper95_pct": round(100 * hi, 1),
    }


def median(xs):
    return statistics.median(xs)
