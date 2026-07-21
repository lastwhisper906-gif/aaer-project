"""Canonical Wave-2 conclusion rules from ANALYSIS_PLAN_WAVE2 section 4."""

import math


def r1_fires(perm_p, alpha=0.05):
    return perm_p >= alpha


def r2_fires(rho, resid_perm_p, rho_high=0.7, alpha=0.05):
    return (
        rho is not None
        and rho >= rho_high
        and resid_perm_p is not None
        and resid_perm_p >= alpha
    )


def r3_case_counts(delta_mean, orig_score, control_median):
    denominator = orig_score - control_median
    return denominator <= 0 or abs(delta_mean) >= 0.5 * denominator


def r3_fires(n_counting, n_treatment):
    return n_counting >= math.floor(n_treatment / 2) + 1


def fired_rule(r1, r2, r3):
    if r1:
        return "R1"
    if r3:
        return "R3"
    if r2:
        return "R2"
    return "R4"
