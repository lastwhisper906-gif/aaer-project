"""P2 교차-웨이브 종합 — 결정론·시드 고정. `python analysis/synthesis.py`.

동결 함수만 재사용(재해석·재채점 없음):
  scoring/probe_verdict.name_match · scoring/baselines/screens.run_case ·
  analysis/stats.{auc,boot_auc_ci}.
입력: baseline_table.csv(wave-1) · runs/{wave2,holdout}/scores · runs/wave2/perturbed ·
      scoring/probe_results_wave2/recognition · name_probe_results.json(wave-1) ·
      candidates_{,wave2,holdout}.json · id_mapping_wave2.json · fraud_case_ids.json.
출력: analysis/unified_table.csv · analysis/synthesis.json ·
      analysis/fig_memorization_doseresponse.png.
캡션 주의: 세 표본은 시대·유명도·라벨 tier가 달라 통제 실험이 아니라 gradient 판독.
"""
import csv
import json
import random
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scoring"))
sys.path.insert(0, str(REPO / "scoring/baselines"))
sys.path.insert(0, str(REPO / "analysis"))
from probe_verdict import name_match  # noqa: E402 (동결 판정)
from screens import run_case  # noqa: E402 (동결 기준선)
from stats import auc, boot_auc_ci  # noqa: E402 (동결 통계)

SEED = 20260708
M_FLAG, F_FLAG = -1.78, 1.0
FRAUD_W2 = ["T02", "T04", "T19", "T20", "T22", "T23", "T24", "T26", "T29"]


def load(p, repo=REPO):
    return json.load(open(repo / p, encoding="utf-8"))


def baseline_mf(cand_rec, exclusions):
    try:
        r = run_case(cand_rec)
    except (FileNotFoundError, KeyError, ValueError, ZeroDivisionError) as exc:
        exclusions.append({
            "case_id": cand_rec.get("case_id"),
            "ticker": cand_rec.get("ticker"),
            "stage": "baseline_mf",
            "exception_class": type(exc).__name__,
            "message": str(exc),
            "classification": (
                "data_missing" if isinstance(exc, (FileNotFoundError, KeyError)) else "code_error"
            ),
        })
        return None, None
    return r.get("beneish", {}).get("m_score"), r.get("dechow_f", {}).get("f_score")


def rows_wave1(exclusions, repo=REPO):
    npr = {r["truth_ticker"]: r["recognized"] for r in load("analysis/name_probe_results.json", repo)["rows"]}
    out = []
    for r in csv.DictReader(open(repo / "analysis/baseline_table.csv", encoding="utf-8")):
        p = float(r["llm_score"]) if r["llm_score"] not in ("", "None") else None
        pert = float(r["llm_perturbed"]) if r["llm_perturbed"] not in ("", "None") else None
        m = float(r["m_score"]) if r["m_score"] not in ("", "None") else None
        f = float(r["f_score"]) if r["f_score"] not in ("", "None") else None
        out.append(dict(wave="wave1", case_id=r["case_id"], ticker=r["ticker"], group=r["group"],
                        llm_score=p, flag=int(p >= 50) if p is not None else None,
                        llm_perturbed=pert,
                        perturb_delta=round(pert - p, 1) if (pert is not None and p is not None) else None,
                        recognized=npr.get(r["ticker"].split("/")[0]),
                        m_score=m, m_flag=int(m <= M_FLAG) if m is not None else None,
                        f_score=f, f_flag=int(f >= F_FLAG) if f is not None else None))
    return out


def rows_wave2(exclusions, repo=REPO):
    idmap = load("scoring/id_mapping_wave2.json", repo)["mapping"]
    frauds = set(load("runs/wave2/fraud_case_ids.json", repo))
    cw = {c["case_id"]: c for c in load("data/candidates/candidates_wave2.json", repo)["candidates"]}
    out = []
    for case, code in sorted(idmap.items()):
        sp = repo / f"runs/wave2/scores/{case}.json"
        if not sp.exists():
            continue
        s = json.load(open(sp, encoding="utf-8"))
        p = s.get("misstatement_probability")
        grp = "fraud" if case in frauds else "control"
        c = cw[code]
        pert = None
        pp = repo / f"runs/wave2/perturbed/{case}.json"
        if pp.exists():
            pert = json.load(open(pp, encoding="utf-8")).get("misstatement_probability")
        rec = None
        rp = repo / f"scoring/probe_results_wave2/recognition/{case}.json"
        if rp.exists():
            g = json.load(open(rp, encoding="utf-8")).get("company_guess", "")
            rec = bool(name_match(g, c["company_name"]))
        m, f = baseline_mf(dict(c, group=grp), exclusions)
        out.append(dict(wave="wave2", case_id=case, ticker=c["ticker"], group=grp,
                        llm_score=p, flag=int((p or 0) >= 50),
                        llm_perturbed=pert,
                        perturb_delta=round(pert - p, 1) if (pert is not None and p is not None) else None,
                        recognized=rec,
                        m_score=round(m, 3) if m is not None else None,
                        m_flag=int(m <= M_FLAG) if m is not None else None,
                        f_score=round(f, 3) if f is not None else None,
                        f_flag=int(f >= F_FLAG) if f is not None else None))
    return out


def rows_holdout(exclusions, repo=REPO):
    ch = {c["case_id"]: c for c in load("data/candidates/candidates_holdout.json", repo)["candidates"]}
    out = []
    for case in sorted(ch):
        sp = repo / f"runs/holdout/scores/{case}.json"
        if not sp.exists():
            continue
        p = json.load(open(sp, encoding="utf-8")).get("misstatement_probability")
        c = ch[case]
        m, f = baseline_mf(dict(c, group="fraud"), exclusions)
        rp = repo / f"runs/holdout/recognition/{c['ticker']}.json"
        if rp.exists():
            recognized = bool(json.load(open(rp, encoding="utf-8"))["knows_event"])
        else:
            recognized = None
            exclusions.append({
                "case_id": case,
                "ticker": c["ticker"],
                "stage": "holdout_recognition",
                "exception_class": "FileNotFoundError",
                "message": str(rp),
                "classification": "data_missing",
            })
        out.append(dict(wave="holdout", case_id=case, ticker=c["ticker"], group="fraud",
                        llm_score=p, flag=int((p or 0) >= 50), llm_perturbed=None,
                        perturb_delta=None,
                        recognized=recognized,
                        m_score=round(m, 3) if m is not None else None,
                        m_flag=int(m <= M_FLAG) if m is not None else None,
                        f_score=round(f, 3) if f is not None else None,
                        f_flag=int(f >= F_FLAG) if f is not None else None))
    return out


def separation(rows, rng):
    fr = [r["llm_score"] for r in rows if r["group"] == "fraud" and r["llm_score"] is not None]
    ct = [r["llm_score"] for r in rows if r["group"] == "control" and r["llm_score"] is not None]
    d = dict(n_fraud=len(fr), n_control=len(ct),
             fraud_median=round(sorted(fr)[len(fr) // 2], 1) if fr else None,
             control_median=round(sorted(ct)[len(ct) // 2], 1) if ct else None)
    if fr and ct and len(ct) >= 2:
        d["auc"] = round(auc(fr, ct), 3)
        lo, hi = boot_auc_ci(fr, ct, rng)
        d["auc_ci"] = [round(lo, 3), round(hi, 3)]
    else:
        d["auc"] = None
        d["auc_ci"] = None
        d["per_case_fraud_scores"] = sorted(fr, reverse=True)
    return d


def name_id_rate(rows):
    """동결 name_match 규칙 기준 name-ID rate. (rule-vs-human 경계 DAR는 §reconcile 참조.)"""
    rec = [r["recognized"] for r in rows if r["recognized"] is not None]
    return round(100 * sum(rec) / len(rec), 1) if rec else None


def main(repo=REPO, out_dir=None):
    if out_dir is None:
        out_dir = repo / "analysis"
    rng = random.Random(SEED)
    exclusions = []
    w1 = rows_wave1(exclusions, repo)
    w2 = rows_wave2(exclusions, repo)
    ho = rows_holdout(exclusions, repo)
    allrows = w1 + w2 + ho

    cols = ["wave", "case_id", "ticker", "group", "llm_score", "flag", "llm_perturbed",
            "perturb_delta", "recognized", "m_score", "m_flag", "f_score", "f_flag"]
    with open(out_dir / "unified_table.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in allrows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})

    # 시드 재사용 순서 고정: wave1 → wave2 (holdout는 AUC 없음)
    sep = {"wave1": separation(w1, rng), "wave2": separation(w2, rng), "holdout": separation(ho, rng)}
    dose = [
        {"tier": "wave1 (famous)", "name_id_pct": name_id_rate(w1), "auc": sep["wave1"]["auc"],
         "auc_ci": sep["wave1"]["auc_ci"], "rule": "R3 (memorization-entangled)"},
        {"tier": "wave2 (less-famous)", "name_id_pct": name_id_rate(w2), "auc": sep["wave2"]["auc"],
         "auc_ci": sep["wave2"]["auc_ci"], "rule": "R4 (residual capability)"},
        {"tier": "holdout (post-cutoff, unmemorizable)", "name_id_pct": name_id_rate(ho),
         "auc": sep["holdout"]["auc"], "auc_ci": None,
         "per_case": {r["ticker"]: r["llm_score"] for r in ho}, "rule": "H2 (per-case, N=3)"},
    ]
    out = {
        "seed": SEED,
        "generated_by": "analysis/synthesis.py (deterministic)",
        "separation_by_wave": sep,
        "memorization_dose_response": dose,
        "dose_response_reading": ("name-ID(암기 대리지표) 50%→25%→~0%로 하락해도 분리 AUC는 "
                                  "0.824→0.829로 사실상 불변(wave1→wave2), 홀드아웃은 HUBG=70으로 "
                                  "탐지 잔존 → 분리는 암기로 설명되지 않음(R4/H2 residual). "
                                  "단 세 표본은 시대·유명도·라벨 tier 상이 = gradient 판독, 통제실험 아님."),
        "per_wave_rule": {"wave1": "R3", "wave2": "R4 (E3 재추첨 확증)", "holdout": "H2 (N=3, per-case)"},
        "note": ("E3(wave-2 교란 재추첨, 2026-07-08) 완료: median-delta dominance 4/9 < 5 → "
                 "R4 유지(R3 미발동), per-case σ 3.2pp. e3_results.json 참조. wave2 rule 확정 R4."),
        "wave2_name_id_reconcile": {
            "frozen_rule_pct": 21.9, "frozen_rule_count": "7/32 (fraud 3/9, control 4/23)",
            "human_read_pct": 25.0, "human_read_count": "8/32 (fraud 3/9, control 5/23)",
            "single_boundary_case": "DAR (Darling Ingredients): probe guess "
                "'Darling International Inc. (now Darling Ingredients Inc.)' — 명백한 정체 "
                "인식이나 동결 name_match는 구명(舊名 'Darling International') 미처리로 False. "
                "wave2_summary.md 산문 '25%'는 DAR를 사람이 인식으로 계수(8/32); 동결 규칙은 "
                "21.9%(7/32).",
            "resolution": "본 synthesis는 방법론(동결 판정 규칙 재해석 금지, name_probes.py "
                "헤더)에 따라 frozen_rule 21.9%를 1차값으로 보고하고 human_read 25%를 병기. "
                "산문 25% 무단 수정 안 함(재채점 금지) — 발행 규약 선택은 OWNER_QUEUE Q-E02.",
            "qualitative_invariant": "어느 쪽이든 50%→~22–25%→0%의 반감 서사는 불변.",
        },
    }
    (out_dir / "synthesis.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    exclusion_path = out_dir / "out/synthesis_exclusions.json"
    exclusion_path.parent.mkdir(parents=True, exist_ok=True)
    exclusion_path.write_text(json.dumps({
        "generated_by": "analysis/synthesis.py",
        "excluded_n": len(exclusions),
        "records": exclusions,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # dose-response figure
    xs = [d["name_id_pct"] for d in dose]
    ys = [d["auc"] if d["auc"] is not None else None for d in dose]
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    for d in dose[:2]:
        lo, hi = d["auc_ci"]
        ax.errorbar(d["name_id_pct"], d["auc"], yerr=[[d["auc"] - lo], [hi - d["auc"]]],
                    fmt="o", ms=9, capsize=5, color="#2f5fa8")
        ax.annotate(f"{d['tier'].split(' ')[0]}\nAUC={d['auc']}",
                    (d["name_id_pct"], d["auc"]), textcoords="offset points",
                    xytext=(8, 8), fontsize=9)
    ho_d = dose[2]
    ax.scatter([ho_d["name_id_pct"]], [0.5], marker="s", s=80, color="#b45309", zorder=5)
    ax.annotate("holdout N=3 (AUC 불가)\nHUBG=70·GNE=42·WMK=32",
                (ho_d["name_id_pct"], 0.5), textcoords="offset points", xytext=(8, -28), fontsize=8)
    ax.set_xlabel("name-ID rate (memorization proxy, %) — 낮을수록 암기 약함")
    ax.set_ylabel("separation AUC (fraud vs control)")
    ax.set_title("Memorization dose-response: 암기 하락에도 분리 유지 (gradient, 통제실험 아님)")
    ax.set_xlim(-5, 60)
    ax.set_ylim(0.45, 1.0)
    ax.axhline(0.5, ls=":", c="#9ca3af", lw=1)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "fig_memorization_doseresponse.png", dpi=140)

    print(f"unified_table.csv: {len(allrows)} rows (w1={len(w1)} w2={len(w2)} ho={len(ho)})")
    print(f"dose-response name-ID: w1={xs[0]}% w2={xs[1]}% ho={xs[2]}% | AUC w1={ys[0]} w2={ys[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
