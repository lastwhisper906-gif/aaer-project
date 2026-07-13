"""Q-F06-B median-of-3 병기 분석 (specs/draw_k3.md §3) — 무호출·결정론.

동결 draw-1 발행 수치는 불변 — median-of-3은 병기(co-report) 통계다.
grade 병합 금지: dims·채점은 draw-1 유지, 여기서는 misstatement 점수만.

draw 소스 (케이스별 발행 draw-1 프레임 그대로 복제 — 실측 run_id 근거):
  w1 treatment 8  : draw-1 runs/perturbed · draw-2/3 runs/hardening/draws/draw_{2,3} (옵션 B 재사용)
  w1 control  22  : draw-1 runs/rp09/scores(original) · draw-2/3 runs/draw_k3/w1_controls/draw_{2,3}
  wave-2      32  : draw-1 runs/wave2/scores(original) · draw-2/3 runs/draw_k3/wave2/draw_{2,3}

출력: analysis/draw_k3_results.json + analysis/DRAW_K3_REPORT.md
  - flip-rate 표 (draw-1 플래그 vs median-of-3 플래그가 다른 케이스 + 방향)
  - median 점수 분리 통계 (perm p·AUC) — 동결 draw-1 수치와 나란히 병기, 대체 금지
  - per-case min–max 밴드 (E5§7 표기)
"""
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
import stats  # noqa: E402

FLAG = 50
import random  # noqa: E402

SEED_K3 = 20260713


def p_of(path: Path) -> int:
    return json.loads(path.read_text(encoding="utf-8"))["misstatement_probability"]


def collect() -> list[dict]:
    rows = []
    w1t = json.loads((REPO / "scoring/perturbed_cases.json").read_text())["cases"]
    for c in w1t:
        cid = c["case_id"]
        rows.append({"case_id": cid, "tier": "wave1", "group": "treatment",
                     "draws": [p_of(REPO / "runs/perturbed" / f"{cid}.json"),
                               p_of(REPO / "runs/hardening/draws/draw_2" / f"{cid}.json"),
                               p_of(REPO / "runs/hardening/draws/draw_3" / f"{cid}.json")],
                     "draw23_source": "hardening 재사용 (Q-F06 옵션 B)"})
    w1c = json.loads((REPO / "data/evaluatee/cases_v2.json").read_text())["cases"]
    for c in w1c:
        cid = c["case_id"]
        rows.append({"case_id": cid, "tier": "wave1", "group": "control",
                     "draws": [p_of(REPO / "runs/rp09/scores" / f"{cid}.json"),
                               p_of(REPO / "runs/draw_k3/w1_controls/draw_2" / f"{cid}.json"),
                               p_of(REPO / "runs/draw_k3/w1_controls/draw_3" / f"{cid}.json")],
                     "draw23_source": "신규"})
    w2 = json.loads((REPO / "data/evaluatee/cases_wave2.json").read_text())["cases"]
    w2_treat = set(json.loads((REPO / "runs/wave2/fraud_case_ids.json")
                              .read_text())) if (REPO / "runs/wave2/fraud_case_ids.json").is_file() else None
    for c in w2:
        cid = c["case_id"]
        grp = ("treatment" if (w2_treat and cid in w2_treat) else
               "control" if w2_treat else "unknown")
        rows.append({"case_id": cid, "tier": "wave2", "group": grp,
                     "draws": [p_of(REPO / "runs/wave2/scores" / f"{cid}.json"),
                               p_of(REPO / "runs/draw_k3/wave2/draw_2" / f"{cid}.json"),
                               p_of(REPO / "runs/draw_k3/wave2/draw_3" / f"{cid}.json")],
                     "draw23_source": "신규"})
    for r in rows:
        d = r["draws"]
        r["median3"] = statistics.median(d)
        r["band_min_max"] = [min(d), max(d)]
        r["flag_draw1"] = d[0] >= FLAG
        r["flag_median3"] = r["median3"] >= FLAG
        r["flip"] = (None if r["flag_draw1"] == r["flag_median3"] else
                     "gained_flag" if r["flag_median3"] else "lost_flag")
    return rows


def tier_block(rows: list[dict], tier: str) -> dict:
    sub = [r for r in rows if r["tier"] == tier and r["group"] in ("treatment", "control")]
    flips = [r for r in sub if r["flip"]]
    blk = {"n": len(sub),
           "flip_rate": f"{len(flips)}/{len(sub)}",
           "flips": [{"case_id": r["case_id"], "direction": r["flip"],
                      "draws": r["draws"], "median3": r["median3"]} for r in flips]}
    treat = [r["median3"] for r in sub if r["group"] == "treatment"]
    ctrl = [r["median3"] for r in sub if r["group"] == "control"]
    if treat and ctrl:
        rng = random.Random(SEED_K3)
        p, obs = stats.perm_test_mean(treat, ctrl, rng)
        lo, hi = stats.boot_auc_ci(treat, ctrl, rng)
        blk["median3_stats_co_report"] = {
            "auc": round(stats.auc(treat, ctrl), 4),
            "auc_boot95": [round(lo, 3), round(hi, 3)],
            "perm_p_one_sided": round(p, 6), "mean_diff": round(obs, 4),
            "note": "병기 전용 — 동결 draw-1 발행 수치 대체 금지 (specs/draw_k3.md)"}
    return blk


def main() -> int:
    rows = collect()
    out = {"spec": "specs/draw_k3.md (Q-F06 옵션 B — owner 2026-07-13 야간 서면 승인)",
           "flag_threshold": FLAG, "seed": SEED_K3,
           "nondeterminism_note": ("temp=0이 배포 API에서 결정론을 보장하지 않으므로 "
                                   "median-of-k는 분산 완화이지 제거가 아니다 (스펙 §1 — "
                                   "발행 표면 인용 시 동반 의무)"),
           "tiers": {t: tier_block(rows, t) for t in ("wave1", "wave2")},
           "per_case": rows}
    (REPO / "analysis" / "draw_k3_results.json").write_text(
        json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
        encoding="utf-8")
    md = ["# DRAW_K3 리포트 — median-of-3 병기 (Q-F06-B, 동결 draw-1 불변)", "",
          "> " + out["nondeterminism_note"], "",
          "> 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).", ""]
    for t, blk in out["tiers"].items():
        md += [f"## {t} — flip-rate {blk['flip_rate']}", ""]
        for f in blk["flips"]:
            md.append(f"- {f['case_id']}: {f['direction']} (draws {f['draws']} → "
                      f"median {f['median3']})")
        if blk.get("median3_stats_co_report"):
            s = blk["median3_stats_co_report"]
            md.append(f"- median-of-3 AUC {s['auc']} CI {s['auc_boot95']} "
                      f"p={s['perm_p_one_sided']} — **병기 전용**")
        md.append("")
    (REPO / "analysis" / "DRAW_K3_REPORT.md").write_text("\n".join(md) + "\n",
                                                         encoding="utf-8")
    print("→ analysis/draw_k3_results.json · DRAW_K3_REPORT.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
