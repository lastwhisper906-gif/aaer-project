"""b3_compute.py — B3 결정론 메타신호 기준선 (WS-2/F-1, specs/B3_metasignal.md).

스펙 사전 등록 커밋(053e780)이 본 파일보다 선행한다 — 임계·윈도·집계식은
계산 전 고정. 출력: analysis/results_b3.json + analysis/B3_REPORT.md.

결정론: SEED_B3 = 20260712 (스펙 §6 선언). (tier, window) 블록마다
random.Random(SEED_B3)을 새로 시드 — 계산 순서와 무관하게 재현 동일.
LLM AUC는 재계산하지 않는다 — 동결 산출물에서 읽는다 (스펙 §6).

E2 통합 계약 (스펙 §8): b3_score(ticker, cutoff, window_days) 순수 함수.

사용: .venv/bin/python analysis/b3_compute.py
"""
from __future__ import annotations

import csv
import datetime
import json
import random
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
sys.path.insert(0, str(REPO / "analysis"))
from payload_v2_extract import parse_items  # WS-1 공유 파서 (스펙 §4)
import stats  # 동결 분석과 동일 의미론의 auc/boot/perm (스펙 §6)

DATA_DIR = Path.home() / "aaer-data"
SEED_B3 = 20260712
W4, W8 = 365, 730
WINDOWS = {"W4": W4, "W8": W8}
PRIMARY_WINDOW = "W8"
EIGHTK_ITEM_FORMS = ("8-K", "8-K/A")
OLD_ITEM_REGIME_END = datetime.date(2004, 8, 23)  # 신형 item 번호 발효

# 동결 LLM AUC (스펙 §6 — 재계산 금지, 값 출처 주석)
FROZEN_LLM_AUC = {
    "wave1": 0.8239,   # analysis/results_stats.json primary.auc
    "wave2": 0.829,    # analysis/wave2_results.json original.auc
    "holdout": None,   # 동결 AUC 부재 (N=3 per-case 프레임) — 귀속비 미계산
}
FROZEN_B_AUC = {  # analysis/results_stats.json baselines.*.own_separation.auc
    "wave1": {"B1_beneish_m": 0.5104, "B2_dechow_f": 0.5729},
    "wave2": {"B1_beneish_m": None, "B2_dechow_f": None},   # 동결 AUC 없음 (rho만 존재)
    "holdout": {"B1_beneish_m": None, "B2_dechow_f": None},
}


class B3Error(Exception):
    """fail-closed: 파싱 불가 날짜·파일 부재 — 조용한 skip 금지."""


def _iso(value, field: str) -> datetime.date:
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError as e:
        raise B3Error(f"{field}={value!r}: ISO 날짜가 아님 — fail-closed") from e


def _load_filings(ticker: str, data_dir: Path) -> list[dict]:
    """submissions 전 청크 → [{form, date, items_raw, accession}] (accession dedup)."""
    edgar_dir = data_dir / ticker / "edgar"
    paths = sorted(edgar_dir.glob("CIK*.json"))
    if not paths:
        raise B3Error(f"{edgar_dir}: submissions JSON 없음 — fail-closed (fetch 금지)")
    rows, seen = [], set()
    for path in paths:
        j = json.loads(path.read_text(encoding="utf-8"))
        blocks = [j["filings"]["recent"]] if "filings" in j else [j]
        for b in blocks:
            forms = b.get("form", [])
            dates = b.get("filingDate", [])
            accs = b.get("accessionNumber", [])
            items = b.get("items", [""] * len(forms))
            for i, form in enumerate(forms):
                acc = accs[i]
                if acc in seen:
                    continue
                seen.add(acc)
                rows.append({"form": form, "date": _iso(dates[i], "filingDate"),
                             "items_raw": items[i] if i < len(items) else "",
                             "accession": acc})
    return rows


def _in_window(d: datetime.date, cutoff: datetime.date, window_days: int, k: int = 0) -> bool:
    """윈도 k (k=0 현재): cutoff−(k+1)·w < d <= cutoff−k·w (스펙 §3)."""
    hi = cutoff - datetime.timedelta(days=k * window_days)
    lo = cutoff - datetime.timedelta(days=(k + 1) * window_days)
    return lo < d <= hi


def b3_score(ticker: str, cutoff: datetime.date, window_days: int,
             data_dir: Path = DATA_DIR) -> dict:
    """스펙 §4 지표 6종 + §5 비가중 합. E2 통합 계약 (스펙 §8) — 순수 함수."""
    filings = _load_filings(ticker, data_dir)
    cur = [f for f in filings if _in_window(f["date"], cutoff, window_days)]

    b_nt = int(any(f["form"].startswith(("NT 10-K", "NT 10-Q")) for f in cur))
    b_ka = int(any(f["form"] == "10-K/A" for f in cur))
    b_qa = int(any(f["form"] == "10-Q/A" for f in cur))
    b_401 = int(any(f["form"] in EIGHTK_ITEM_FORMS and "4.01" in parse_items(f["items_raw"])
                    for f in cur))
    b_402 = int(any(f["form"] in EIGHTK_ITEM_FORMS and "4.02" in parse_items(f["items_raw"])
                    for f in cur))

    eightk_current = sum(1 for f in cur if f["form"] == "8-K")
    earliest = min((f["date"] for f in filings), default=None)
    history_floor = cutoff - datetime.timedelta(days=4 * window_days)
    insufficient = earliest is None or earliest > history_floor
    trailing = [sum(1 for f in filings
                    if f["form"] == "8-K" and _in_window(f["date"], cutoff, window_days, k))
                for k in (1, 2, 3)]
    if insufficient:
        b_8kfreq = 0  # fail-closed (스펙 §4)
    else:
        b_8kfreq = int(eightk_current > 1.5 * statistics.median(trailing))

    indicators = {"b_nt": b_nt, "b_ka": b_ka, "b_qa": b_qa,
                  "b_401": b_401, "b_402": b_402, "b_8kfreq": b_8kfreq}
    return {"score": sum(indicators.values()), "indicators": indicators,
            "flags": {"insufficient_history": bool(insufficient)},
            "counts": {"eightk_current": eightk_current, "eightk_trailing": trailing},
            "window_start": str(cutoff - datetime.timedelta(days=window_days)),
            "cutoff": str(cutoff)}


# ── 로스터 (스펙 §2 — 커밋된 동결 산출물에서만) ────────────────────────────

def _registry(path: Path) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    cands = raw["candidates"] if isinstance(raw, dict) else raw
    return {c["case_id"]: c for c in cands}


def load_rosters() -> dict:
    cand_dir = REPO / "data" / "candidates"
    main_reg = _registry(cand_dir / "candidates.json")
    v2_reg = _registry(cand_dir / "candidates_v2_controls.json")
    rosters = {"wave1": [], "wave2": [], "holdout": []}

    for r in csv.DictReader(open(REPO / "analysis/baseline_table.csv", encoding="utf-8")):
        reg = main_reg if r["case_id"].startswith("T") else v2_reg
        if r["case_id"] not in reg:
            raise B3Error(f"wave-1 로스터 {r['case_id']}: 레지스트리 미발견 — fail-closed")
        c = reg[r["case_id"]]
        rosters["wave1"].append({"case_id": r["case_id"], "ticker": r["ticker"],
                                 "group": "treatment" if r["group"] == "fraud" else "control",
                                 "cutoff": _iso(c["cutoff_date"], "cutoff_date")})
    for c in _registry(cand_dir / "candidates_wave2.json").values():
        rosters["wave2"].append({"case_id": c["case_id"], "ticker": c["ticker"],
                                 "group": c["group"],
                                 "cutoff": _iso(c["cutoff_date"], "cutoff_date")})
    for name in ("candidates_holdout.json", "candidates_holdout_controls.json"):
        for c in _registry(cand_dir / name).values():
            rosters["holdout"].append({"case_id": c["case_id"], "ticker": c["ticker"],
                                       "group": c["group"],
                                       "cutoff": _iso(c["cutoff_date"], "cutoff_date")})
    return rosters


def tier_stats(treat: list[int], ctrl: list[int]) -> dict:
    rng = random.Random(SEED_B3)  # 블록별 재시드 — 순서 독립 결정론
    p, obs = stats.perm_test_mean(treat, ctrl, rng)
    a = stats.auc(treat, ctrl)
    lo, hi = stats.boot_auc_ci(treat, ctrl, rng)
    return {"n_treatment": len(treat), "n_control": len(ctrl),
            "treatment_scores": sorted(treat), "control_scores": sorted(ctrl),
            "mean_diff": round(obs, 3),
            "median_treatment": statistics.median(treat),
            "median_control": statistics.median(ctrl),
            "auc": round(a, 4), "auc_boot95": [round(lo, 3), round(hi, 3)],
            "perm_p_one_sided": round(p, 6)}


def main() -> int:
    rosters = load_rosters()
    out = {"spec": "specs/B3_metasignal.md", "spec_commit": "053e780",
           "seed": SEED_B3, "n_perm": stats.N_PERM, "n_boot": stats.N_BOOT,
           "primary_window": PRIMARY_WINDOW,
           "frozen_llm_auc": FROZEN_LLM_AUC, "frozen_baseline_auc": FROZEN_B_AUC,
           "tiers": {}}
    earliest_window_start = None

    for tier, roster in rosters.items():
        tier_out = {"coverage": None, "windows": {}}
        per_case = {}
        missing = []
        for case in roster:
            try:
                per_case[case["case_id"]] = {
                    w: b3_score(case["ticker"], case["cutoff"], days)
                    for w, days in WINDOWS.items()}
            except B3Error as e:
                missing.append({"case_id": case["case_id"], "ticker": case["ticker"],
                                "reason": str(e)})
        covered = [c for c in roster if c["case_id"] in per_case]
        tier_out["coverage"] = f"{len(covered)}/{len(roster)}"
        tier_out["missing"] = missing
        for w, days in WINDOWS.items():
            treat = [per_case[c["case_id"]][w]["score"] for c in covered if c["group"] == "treatment"]
            ctrl = [per_case[c["case_id"]][w]["score"] for c in covered if c["group"] == "control"]
            st = tier_stats(treat, ctrl)
            st["insufficient_history_n"] = sum(
                1 for c in covered if per_case[c["case_id"]][w]["flags"]["insufficient_history"])
            gap_src = FROZEN_LLM_AUC[tier]
            if gap_src is not None:
                st["attribution_ratio_vs_frozen_llm"] = round((st["auc"] - 0.5) / (gap_src - 0.5), 4)
            tier_out["windows"][w] = st
            for c in covered:
                ws = _iso(per_case[c["case_id"]][w]["window_start"], "window_start")
                if earliest_window_start is None or ws < earliest_window_start:
                    earliest_window_start = ws
        tier_out["per_case"] = {cid: per_case[cid] for cid in sorted(per_case)}
        out["tiers"][tier] = tier_out

    # 스펙 §4: item 매칭 윈도가 전부 신형 번호 체계(2004-08-23) 이후인지 확인·기록
    out["item_regime_check"] = {
        "earliest_current_window_start": str(earliest_window_start),
        "all_post_2004_regime": earliest_window_start > OLD_ITEM_REGIME_END}
    if not out["item_regime_check"]["all_post_2004_regime"]:
        raise B3Error("현재 윈도가 2004-08 이전 item 체계와 겹침 — 스펙 §4 전제 위반")

    # 스펙 §7 해석 규칙 — wave-2 W8 판정
    ratio = out["tiers"]["wave2"]["windows"][PRIMARY_WINDOW]["attribution_ratio_vs_frozen_llm"]
    if ratio >= 0.5:
        branch = ("majority_attribution", "메타신호가 분리의 과반을 설명 — 능력 해석 완화 diff 제안 의무")
    elif ratio <= 0.2:
        branch = ("non_trivial", "분리는 사소한 연대기 규칙에 귀속되지 않음 — 비자명성 강화, 병기만")
    else:
        branch = ("partial_attribution", "부분 귀속 — 어느 방향으로도 주장 변경 없음")
    out["interpretation"] = {"decision_tier": "wave2", "decision_window": PRIMARY_WINDOW,
                             "attribution_ratio": ratio, "branch": branch[0], "reading": branch[1]}

    (REPO / "analysis/results_b3.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── B3_REPORT.md ──
    md = ["# B3_REPORT — 결정론 메타신호 기준선 (specs/B3_metasignal.md 사전 등록 이행)",
          "",
          f"- 사전 등록: 스펙 커밋 `053e780` (컴퓨트 코드 선행). seed {SEED_B3}, "
          f"perm {stats.N_PERM:,}, boot {stats.N_BOOT:,}. 1차 윈도 = {PRIMARY_WINDOW}.",
          "- B3 = 6지표 비가중 합 (0–6): NT 10-K/Q · 10-K/A · 10-Q/A · 8-K item 4.01 · "
          "item 4.02 · 8-K 빈도 (>1.5× 선행 3윈도 중위).",
          "- LLM/B1/B2 AUC는 동결 산출물 인용 (재계산 0) — 부재 tier는 '동결값 없음'.",
          ""]
    tier_names = {"wave1": "wave-1 (8v22)", "wave2": "wave-2 (9v23)", "holdout": "holdout (3v9)"}
    for tier in ("wave1", "wave2", "holdout"):
        t = out["tiers"][tier]
        md += [f"## {tier_names[tier]} — coverage {t['coverage']}", "",
               "| 지표 | " + " | ".join(WINDOWS) + " |", "|---|---|---|"]
        for label, get in [
            ("B3 AUC [boot95]", lambda s: f"{s['auc']} {s['auc_boot95']}"),
            ("B3 순열 p (단측)", lambda s: f"{s['perm_p_one_sided']}"),
            ("B3 평균차 (t−c)", lambda s: f"{s['mean_diff']}"),
            ("B3 중위 (t / c)", lambda s: f"{s['median_treatment']} / {s['median_control']}"),
            ("insufficient_history", lambda s: f"{s['insufficient_history_n']}건"),
            ("귀속비 (AUC_B3−0.5)/(AUC_LLM−0.5)",
             lambda s: f"{s.get('attribution_ratio_vs_frozen_llm', '— (동결 LLM AUC 없음)')}"),
        ]:
            md.append(f"| {label} | " + " | ".join(get(t["windows"][w]) for w in WINDOWS) + " |")
        b1 = FROZEN_B_AUC[tier]["B1_beneish_m"]
        b2 = FROZEN_B_AUC[tier]["B2_dechow_f"]
        llm = FROZEN_LLM_AUC[tier]
        md += ["",
               f"동결 병렬: B1 Beneish M AUC = {b1 if b1 is not None else '동결값 없음'} · "
               f"B2 Dechow F AUC = {b2 if b2 is not None else '동결값 없음'} · "
               f"LLM AUC = {llm if llm is not None else '동결값 없음 (N=3 per-case 프레임)'}",
               ""]
    it = out["interpretation"]
    w1_ratio = out["tiers"]["wave1"]["windows"][PRIMARY_WINDOW]["attribution_ratio_vs_frozen_llm"]
    md += ["## 사전 등록 해석 규칙 판정 (스펙 §7)", "",
           f"- 판정 tier/윈도: **{it['decision_tier']} · {it['decision_window']}** · "
           f"귀속비 = **{it['attribution_ratio']}** (경계 0.2 / 0.5)",
           f"- 발화 브랜치: **{it['branch']}** — {it['reading']}", "",
           "### 판독 노트 (산술 사실 병기 — 서사 사용은 소유자 서명 대상)", "",
           f"- 참고 tier 비대칭: wave-1 {PRIMARY_WINDOW} 귀속비 **{w1_ratio}** vs "
           f"wave-2 **{it['attribution_ratio']}** — 사소한 연대기 규칙이 wave-1 분리의"
           " 대부분에 도달하지만 wave-2에서는 그렇지 않다는 산술. 판정 tier는 스펙이"
           " 계산 전에 wave-2로 고정했다 (§7 — 암기 교란이 덜한 tier가 귀속 문제의"
           " 실체). 이 비대칭의 원인 서술(암기·대조군 매칭 품질·시대 차 등)은 사전"
           " 등록 문장 밖 — 세션은 서술하지 않는다.", "",
           "## 한계", "",
           "- B3는 상한 탐사가 아니라 사전 등록 6지표의 단일 조합이다 — 지표 선택 자체가"
           " 문헌 기반이며, 계산 후 조정은 없었다 (스펙 커밋이 증거).",
           "- holdout tier는 동결 LLM AUC가 없어 귀속비를 계산하지 않는다 (N=3).",
           "- 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).", ""]
    (REPO / "analysis/B3_REPORT.md").write_text("\n".join(md), encoding="utf-8")
    print(f"B3: wave2 {PRIMARY_WINDOW} 귀속비 {ratio} → {branch[0]}")
    for tier in out["tiers"]:
        for w in WINDOWS:
            s = out["tiers"][tier]["windows"][w]
            print(f"  {tier} {w}: AUC {s['auc']} {s['auc_boot95']} p={s['perm_p_one_sided']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
