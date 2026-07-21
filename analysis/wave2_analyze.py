"""Wave-2 rev2 analysis, writing a new JSON artifact only."""

import glob
import json
import random
import statistics
import sys
from pathlib import Path

from aaer_eval.statistics import (
    auc,
    boot_auc_ci,
    cliffs_delta,
    fisher_one_sided,
    fpr_bound,
    perm_test_mean,
    residuals,
    spearman,
)
from aaer_eval.verdict import fired_rule, r1_fires, r2_fires, r3_case_counts, r3_fires

sys.path.insert(0, "scoring/baselines")
from screens import run_case


def _items(values, prefix):
    if isinstance(values, dict):
        return list(values.items())
    return [(f"{prefix}{i}", value) for i, value in enumerate(values)]


def _baseline_result(pairs, seed, n_perm):
    usable = [(llm, baseline, group) for llm, baseline, group in pairs
              if llm is not None and baseline is not None]
    rho = spearman([x[0] for x in usable], [x[1] for x in usable]) if len(usable) >= 2 else None
    resid_p = None
    fraud_groups = {"fraud", "treatment"}
    if (usable and any(x[2] in fraud_groups for x in usable)
            and any(x[2] == "control" for x in usable)):
        values = residuals([x[0] for x in usable], [x[1] for x in usable])
        fraud_resid = [v for v, x in zip(values, usable) if x[2] in fraud_groups]
        control_resid = [v for v, x in zip(values, usable) if x[2] == "control"]
        resid_p, _ = perm_test_mean(
            fraud_resid, control_resid, random.Random(seed), n=n_perm
        )
    return {"rho": rho, "residual_perm_p": resid_p, "n": len(usable)}


def compute_results(fraud, control, perturbed, m_pairs, f_pairs,
                    seed=20260707, n_perm=100_000, n_boot=10_000,
                    wave1_fraud=(), wave1_control=()):
    fraud_items = _items(fraud, "fraud-")
    control_items = _items(control, "control-")
    fraud_complete = [v for _, v in fraud_items if v is not None]
    control_complete = [v for _, v in control_items if v is not None]
    perm_p, mean_diff = perm_test_mean(
        fraud_complete, control_complete, random.Random(seed), n=n_perm
    )
    original = {
        "perm_p": perm_p,
        "mean_diff": mean_diff,
        "cliff": cliffs_delta(fraud_complete, control_complete),
        "auc": auc(fraud_complete, control_complete),
        "auc_ci": list(boot_auc_ci(
            fraud_complete, control_complete, random.Random(seed), n=n_boot
        )),
        "fraud_median": statistics.median(fraud_complete),
        "control_median": statistics.median(control_complete),
    }

    perturbed_items = dict(_items(perturbed, "fraud-"))
    perturbed_complete = [
        perturbed_items[case_id]
        for case_id, _ in fraud_items
        if case_id in perturbed_items and perturbed_items[case_id] is not None
    ]
    perturbed_frame = {"n_perturbed": len(perturbed_complete), "available": False}
    if perturbed_complete:
        perturbed_p, perturbed_diff = perm_test_mean(
            perturbed_complete, control_complete, random.Random(seed), n=n_perm
        )
        perturbed_frame.update({
            "available": True,
            "perm_p": perturbed_p,
            "mean_diff": perturbed_diff,
            "auc": auc(perturbed_complete, control_complete),
        })

    tp = sum(v >= 50 for v in fraud_complete)
    fn = len(fraud_complete) - tp
    fp = sum(v >= 50 for v in control_complete)
    tn = len(control_complete) - fp
    fisher = {"tp": tp, "fn": fn, "fp": fp, "tn": tn,
              "one_sided_p": fisher_one_sided(tp, fn, fp, tn)}

    incomplete = sum(v is None for _, v in fraud_items + control_items)
    worst_fraud = [0 if v is None else v for _, v in fraud_items]
    worst_control = [100 if v is None else v for _, v in control_items]
    worst_p, worst_diff = perm_test_mean(
        worst_fraud, worst_control, random.Random(seed), n=n_perm
    )
    baseline_results = {
        "beneish_m": _baseline_result(m_pairs, seed, n_perm),
        "dechow_f": _baseline_result(f_pairs, seed, n_perm),
    }

    case_results = []
    for case_id, score in fraud_items:
        if score is None or case_id not in perturbed_items or perturbed_items[case_id] is None:
            continue
        delta = score - perturbed_items[case_id]
        case_results.append({
            "case_id": case_id,
            "delta_mean": delta,
            "counts": r3_case_counts(delta, score, original["control_median"]),
        })
    n_counting = sum(case["counts"] for case in case_results)
    r3 = r3_fires(n_counting, len(fraud_items))
    r2 = any(r2_fires(v["rho"], v["residual_perm_p"])
             for v in baseline_results.values())
    r1 = r1_fires(perm_p)

    pooled_fraud = fraud_complete + list(wave1_fraud)
    pooled_control = control_complete + list(wave1_control)
    pooled_p, pooled_diff = perm_test_mean(
        pooled_fraud, pooled_control, random.Random(seed), n=n_perm
    )

    return {
        "original": original,
        "perturbed_frame": perturbed_frame,
        "fisher_2x2": fisher,
        "fpr": fpr_bound(fp, len(control_complete)),
        "worst_case_substitution": {
            "n_incomplete": incomplete, "perm_p": worst_p, "mean_diff": worst_diff
        },
        "baselines": baseline_results,
        "R3_memorization": {
            "cases": case_results, "n_counting": n_counting,
            "n_treatment": len(fraud_items), "fires": r3,
        },
        "conclusion_rule_standalone": {
            "r1": r1, "r2": r2, "r3": r3,
            "fired": fired_rule(r1, r2, r3),
        },
        "pooled_secondary": {
            "n_fraud": len(pooled_fraud), "n_control": len(pooled_control),
            "mean_diff": pooled_diff, "perm_p": pooled_p,
            "auc": auc(pooled_fraud, pooled_control),
            "note": "SECONDARY ONLY; frozen wave-1 scores reused unchanged",
        },
    }


def load_scores(directory, mapping_path):
    mapping = json.loads(Path(mapping_path).read_text())["mapping"]
    scores = {}
    for filename in glob.glob(f"{directory}/*.json"):
        record = json.loads(Path(filename).read_text())
        scores[mapping[record["case_id"]]] = record.get("misstatement_probability")
    return scores


def load_wave1_scores():
    mapping = json.loads(Path("scoring/id_mapping.json").read_text())["mapping"]
    fraud_ids = {"T07", "T11", "T12", "T13", "T16", "T17", "T21", "T28"}
    fraud = []
    for filename in glob.glob("runs/main/case_*.json"):
        record = json.loads(Path(filename).read_text())
        if mapping[record["case_id"]] in fraud_ids:
            fraud.append(record["misstatement_probability"])
    control = [
        json.loads(Path(filename).read_text())["misstatement_probability"]
        for filename in glob.glob("runs/rp09/scores/case_*.json")
    ]
    return fraud, control


def main():
    candidates_w2 = {
        c["case_id"]: c
        for c in json.loads(Path("data/candidates/candidates_wave2.json").read_text())["candidates"]
    }
    scores = load_scores("runs/wave2/scores", "scoring/id_mapping_wave2.json")
    perturbed = load_scores("runs/wave2/perturbed", "scoring/id_mapping_wave2.json")
    fraud = {case_id: score for case_id, score in scores.items()
             if candidates_w2[case_id]["group"] == "treatment"}
    control = {case_id: score for case_id, score in scores.items()
               if candidates_w2[case_id]["group"] == "control"}

    candidates_w1 = {
        c["case_id"]: c
        for c in json.loads(Path("data/candidates/candidates.json").read_text())["candidates"]
    }
    firms = [dict(candidates_w1[t], group="fraud")
             for t in ["T02", "T04", "T19", "T20", "T22", "T23", "T24", "T26", "T29"]]
    firms += [dict(c, group="control") for c in candidates_w2.values()
              if c["group"] == "control"]
    m_pairs, f_pairs, exclusions = [], [], []
    for firm in firms:
        llm = scores.get(firm["case_id"])
        if llm is None:
            continue
        try:
            baseline = run_case(firm)
        except Exception as exc:
            exclusions.append({"case_id": firm["case_id"],
                               "exception_class": type(exc).__name__, "message": str(exc)})
            continue
        group = firm["group"]
        m_pairs.append((llm, baseline.get("beneish", {}).get("m_score"), group))
        f_pairs.append((llm, baseline.get("dechow_f", {}).get("f_score"), group))

    wave1_fraud, wave1_control = load_wave1_scores()
    results = compute_results(
        fraud, control, perturbed, m_pairs, f_pairs,
        wave1_fraud=wave1_fraud, wave1_control=wave1_control,
    )
    results["exclusions"] = exclusions
    output = Path("analysis/out/wave2_rev2/wave2_results_rev2.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
