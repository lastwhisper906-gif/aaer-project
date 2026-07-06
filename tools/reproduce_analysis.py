"""RP-05 발행 수치 제3자 재현 검증기 (RP-06 B2) — 결정론, API 호출 0.

커밋된 원시 산출물(runs/ · scoring/grades/ · scoring/baselines/results/ ·
scoring/id_mapping.json)만으로 RP-05 §1~§5의 발행 수치 전부(p, 분리, σ, AUC,
Brier, delta, 베이스라인 비교, §7-2 민감도)를 재계산하고, 아래에 하드코딩된
**발행값**(RP-05 문서 원문 전사)과 PASS/FAIL 대조를 출력한다.

- 발행값을 rp05_stats.json에서 읽지 않고 이 파일에 전사해 두는 이유: 검증
  대상은 "발행된 주장"이지 "생성된 중간 파일"이 아니다. rp05_stats.json과의
  정합은 별도 항목으로 추가 대조한다.
- A3 확장 (RP-06): scoring/rp06_hardening_stats.json이 존재하면
  runs/hardening/draws/에서 k=5 통계를 재계산해 그 파일과 대조한다.
- CI: 이 검증기는 커밋 산출물에만 의존하므로 f4f8f73 schema-only 관행의
  skip 대상이 **아니다** — 코퍼스(~/aaer-data) 없이 항상 전체 실행된다.

사용: python tools/reproduce_analysis.py   (실패 시 exit 1)
"""
from __future__ import annotations

import itertools
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# ---------------- 발행값 (RP-05_results.md 원문 전사 — 수정 금지) ----------------
PUBLISHED = {
    "primary": {"p": 0.0226, "separation_pp": 19.0, "median_t": 50.0, "median_c": 31.0,
                "sd_all16": 13.18, "auc": 0.797, "brier": 0.191,
                "failure_b": False},
    "appendix": {"p": 0.0094, "separation_pp": 26.5, "auc": 0.844, "brier": 0.177},
    "failure_a_dim4zero_primary_n": 0,
    "mem2_flags_n": 0,
    # §2 케이스별 p (중립 ID → (원본, 교란|None)) — RP-05 표 전사
    "per_case_p": {
        "case_01": (55, 45), "case_02": (60, 45), "case_03": (42, 45),
        "case_04": (25, None), "case_05": (48, None), "case_06": (28, 58),
        "case_07": (25, None), "case_08": (78, 55), "case_09": (65, 55),
        "case_10": (58, None), "case_11": (45, None), "case_12": (68, 68),
        "case_13": (55, 42), "case_14": (32, None), "case_15": (22, None),
        "case_16": (30, None),
    },
    # §3 교란 delta
    "delta_mean": 4.8, "delta_median": 10.0, "delta_range": [-30, 23],
    # §5 베이스라인 AUC
    "baselines": {"M": 0.571, "F": 0.542, "C": 0.571, "Sloan_abs": 0.589},
    # §7-2 민감도 (ICON/case_09 ↔ PERY/case_05 값 교환)
    "sensitivity_swap": {"p": 0.0347, "auc": 0.773},
}

# ---------------- 재계산 (frozen spec §5 정의 — 정확 Mann-Whitney, midrank) ----------------


def midranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def mann_whitney_exact(t_vals, c_vals):
    pooled = list(t_vals) + list(c_vals)
    ranks = midranks(pooled)
    n_t = len(t_vals)
    obs = sum(ranks[:n_t])
    count = total = 0
    for combo in itertools.combinations(range(len(pooled)), n_t):
        total += 1
        if sum(ranks[i] for i in combo) >= obs - 1e-9:
            count += 1
    u = obs - n_t * (n_t + 1) / 2
    return count / total, u / (n_t * len(c_vals))


def stats_block(t_vals, c_vals):
    p, auc = mann_whitney_exact(t_vals, c_vals)
    all16 = list(t_vals) + list(c_vals)
    brier = (sum((v / 100 - 1) ** 2 for v in t_vals) +
             sum((v / 100 - 0) ** 2 for v in c_vals)) / len(all16)
    return {"p": round(p, 4), "auc": round(auc, 4),
            "median_t": statistics.median(t_vals), "median_c": statistics.median(c_vals),
            "separation_pp": statistics.median(t_vals) - statistics.median(c_vals),
            "sd_all16": round(statistics.pstdev(all16), 2), "brier": round(brier, 4)}


def load_p(d):
    return {p.stem: json.loads(p.read_text(encoding="utf-8"))["misstatement_probability"]
            for p in sorted((REPO / d).glob("case_*.json"))}


def load_grades(d):
    return {p.stem: json.loads(p.read_text(encoding="utf-8"))
            for p in sorted((REPO / d).glob("case_*.json"))}


CHECKS = []


def check(name, got, want, tol=0.0006):
    if isinstance(want, (int, float)) and isinstance(got, (int, float)):
        ok = abs(got - want) <= tol
    else:
        ok = got == want
    CHECKS.append((name, got, want, ok))
    return ok


def main() -> int:
    mapping = json.loads((REPO / "scoring/id_mapping.json").read_text(encoding="utf-8"))["mapping"]
    treat = sorted(n for n, o in mapping.items() if o.startswith("T"))
    ctrl = sorted(n for n, o in mapping.items() if o.startswith("C"))
    p_orig, p_pert = load_p("runs/main"), load_p("runs/perturbed")
    g_main, g_pert = load_grades("scoring/grades/main"), load_grades("scoring/grades/perturbed")

    # §2 케이스별 p 전사 대조
    for n, (po, pp) in PUBLISHED["per_case_p"].items():
        check(f"§2 {n} p_original", p_orig[n], po)
        if pp is not None:
            check(f"§2 {n} p_perturbed", p_pert[n], pp)

    # §1 본 분석 / 부록
    pri = stats_block([p_pert[n] for n in treat], [p_orig[n] for n in ctrl])
    app = stats_block([p_orig[n] for n in treat], [p_orig[n] for n in ctrl])
    for k, want in PUBLISHED["primary"].items():
        if k == "failure_b":
            fb = pri["p"] >= 0.20 or pri["separation_pp"] < 10 or pri["sd_all16"] < 5
            check("§1 primary failure_b", fb, want)
        else:
            check(f"§1 primary {k}", pri[k], want)
    for k, want in PUBLISHED["appendix"].items():
        check(f"§1 appendix {k}", app[k], want)

    # 실패 기준 (a)/(c) 입력
    d4z = [n for n in treat if g_pert[n]["dim4_evidence_quality"] == 0] + \
          [n for n in ctrl if g_main[n]["dim4_evidence_quality"] == 0]
    mem2 = [n for n in mapping if g_main[n]["memorization_suspect_condition2"]] + \
           [n for n in treat if g_pert[n]["memorization_suspect_condition2"]]
    check("§1 failure_a dim4=0 count (primary)", len(d4z), PUBLISHED["failure_a_dim4zero_primary_n"])
    check("§0 mem2 flag count", len(mem2), PUBLISHED["mem2_flags_n"])

    # §3 delta
    deltas = [p_orig[n] - p_pert[n] for n in treat]
    check("§3 delta mean", round(statistics.mean(deltas), 1), PUBLISHED["delta_mean"])
    check("§3 delta median", statistics.median(deltas), PUBLISHED["delta_median"])
    check("§3 delta range", [min(deltas), max(deltas)], PUBLISHED["delta_range"])

    # §5 베이스라인 AUC (analyze_rp05와 동일 정의 — 값 존재 케이스만, 동률 0.5)
    cands = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates.json").read_text(encoding="utf-8"))["candidates"]}
    tvals = {n: json.loads((REPO / f"scoring/baselines/results/{mapping[n]}.json")
                           .read_text(encoding="utf-8")) for n in treat}
    import re

    def first_word(s):
        toks = [t for t in re.sub(r"[^a-z0-9 ]", " ", s.lower()).split() if t != "the"]
        return toks[0] if toks else ""

    by_cand = {}
    for pth in (REPO / "scoring/baselines/results/controls").glob("*.json"):
        d = json.loads(pth.read_text(encoding="utf-8"))
        by_cand[first_word(d["candidate"])] = d

    def screen(n, key):
        if n in tvals:
            d = tvals[n]
            return {"M": d["beneish"]["m_score"], "F": d["dechow_f"]["f_score"],
                    "C": d["montier_c"]["c_score"], "Sloan": d["sloan_accruals"]["value"]}[key]
        d = by_cand.get(first_word(cands[mapping[n]]["company_name"]))
        return None if d is None else {"M": d["beneish_m"], "F": d["dechow_f"],
                                       "C": d["montier_c"], "Sloan": d["sloan"]}[key]

    def auc_defined(key, transform=lambda x: x):
        t = [transform(screen(n, key)) for n in treat if screen(n, key) is not None]
        c = [transform(screen(n, key)) for n in ctrl if screen(n, key) is not None]
        wins = sum((1.0 if a > b else 0.5 if a == b else 0.0) for a in t for b in c)
        return round(wins / (len(t) * len(c)), 3)

    check("§5 AUC Beneish M", auc_defined("M"), PUBLISHED["baselines"]["M"])
    check("§5 AUC Dechow F", auc_defined("F"), PUBLISHED["baselines"]["F"])
    check("§5 AUC Montier C", auc_defined("C"), PUBLISHED["baselines"]["C"])
    check("§5 AUC Sloan |값|", auc_defined("Sloan", abs), PUBLISHED["baselines"]["Sloan_abs"])

    # §7-2 민감도: case_09(교란 55) ↔ case_05(원본 48) 값 교환
    t_swap = [(48 if n == "case_09" else p_pert[n]) for n in treat]
    c_swap = [(55 if n == "case_05" else p_orig[n]) for n in ctrl]
    p_s, auc_s = mann_whitney_exact(t_swap, c_swap)
    check("§7-2 swap p", round(p_s, 4), PUBLISHED["sensitivity_swap"]["p"])
    check("§7-2 swap AUC", round(auc_s, 3), PUBLISHED["sensitivity_swap"]["auc"])

    # rp05_stats.json 정합 (생성 파일 ↔ 재계산)
    stats = json.loads((REPO / "scoring/rp05_stats.json").read_text(encoding="utf-8"))
    check("stats.json primary p", stats["primary"]["p_one_sided_exact"], pri["p"])
    check("stats.json primary auc", stats["primary"]["auc"], pri["auc"])
    check("stats.json appendix p", stats["appendix"]["p_one_sided_exact"], app["p"])

    # ---- A3 확장 (RP-06): 통계 파일이 존재할 때만 — 부재는 실패가 아님 ----
    rp06 = REPO / "scoring/rp06_hardening_stats.json"
    if rp06.is_file():
        pub6 = json.loads(rp06.read_text(encoding="utf-8"))
        draws_root = REPO / "runs/hardening/draws"
        draw_p = {1: {**{n: p_pert[n] for n in treat}, **{n: p_orig[n] for n in ctrl}}}
        for i, dname in enumerate(sorted(d.name for d in draws_root.iterdir() if d.is_dir()), start=2):
            draw_p[i] = load_p(f"runs/hardening/draws/{dname}")
        for d, want in zip(sorted(draw_p), pub6["per_draw_stats"]):
            got = stats_block([draw_p[d][n] for n in treat], [draw_p[d][n] for n in ctrl])
            check(f"A3 draw{d} p", got["p"], want["p"])
            check(f"A3 draw{d} auc", got["auc"], want["auc"])
            check(f"A3 draw{d} separation", got["separation_pp"], want["separation_pp"])
        med = {n: statistics.median([draw_p[d][n] for d in sorted(draw_p)]) for n in mapping}
        got_med = stats_block([med[n] for n in treat], [med[n] for n in ctrl])
        for k in ("p", "auc", "separation_pp"):
            check(f"A3 per-case-median {k}", got_med[k], pub6["median_of_draws_stats"][k])
        for n in sorted(mapping):
            vals = [draw_p[d][n] for d in sorted(draw_p)]
            check(f"A3 {n} mean", round(statistics.mean(vals), 1), pub6["per_case"][n]["mean"])
            check(f"A3 {n} sd", round(statistics.pstdev(vals), 2), pub6["per_case"][n]["sd"])
    else:
        print("A3 통계 파일 부재 — RP-05 검증만 수행 (A3 확장은 파일 생성 후 자동 활성)")

    # ---- 보고 ----
    fails = [c for c in CHECKS if not c[3]]
    for name, got, want, ok in CHECKS:
        if not ok:
            print(f"FAIL {name}: 재계산={got!r} 발행={want!r}")
    print(f"\n{'PASS' if not fails else 'FAIL'} — {len(CHECKS) - len(fails)}/{len(CHECKS)} 항목 일치"
          f" (발행 수치 ↔ 커밋 산출물 재계산)")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
