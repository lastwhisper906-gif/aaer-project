"""B4 — 비정상 공매도 잔고 기준선 (specs/B4_short_interest.md, D55).

정본 계산 코어는 screener/ingest/short_interest.py — 여기서는
analysis/vendor/short_interest.py (문자 그대로 스냅샷, PROVENANCE.md)를 import.
스펙 커밋(4753824)이 이 파일보다 git 이력에서 선행한다 (freeze-commit-then-run).

실행: .venv/bin/python analysis/b4_short_interest.py
  → analysis/results_b4.json + analysis/B4_REPORT.md
네트워크 0 (아카이브 사전 단계는 tools/fetch_short_interest.py), LLM 호출 0.
"""
import datetime
import json
import math
import random
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
sys.path.insert(0, str(REPO / "analysis" / "vendor"))
sys.path.insert(0, str(REPO / "pipeline"))

import short_interest as si_core  # noqa: E402 — vendored snapshot
import stats  # noqa: E402
from b3_compute import B3Error, load_rosters  # noqa: E402
from payload_v2_extract import PayloadV2Error, extract_share_facts  # noqa: E402

DATA_DIR = Path.home() / "aaer-data"
SI_DATA_DIR = DATA_DIR / "short_interest"
SEED_B4 = 20260713  # 스펙 §5 신규 선언 (B3 20260712와 별도)
SPEC = "specs/B4_short_interest.md"
SPEC_COMMIT = "4753824"
COVERAGE_HEADLINE_FLOOR = 0.70  # 스펙 §6: 미달 tier는 서술 전용

FROZEN_LLM_AUC = {"wave1": 0.8239, "wave2": 0.829, "holdout": None}  # 재계산 금지
FROZEN_B_AUC = {"wave1": {"B1_beneish_m": 0.5104, "B2_dechow_f": 0.5729}}
RESULTS_B3 = REPO / "analysis" / "results_b3.json"
OUT_JSON = REPO / "analysis" / "results_b4.json"
OUT_MD = REPO / "analysis" / "B4_REPORT.md"


def b4_score(ticker: str, cutoff: datetime.date,
             data_dir: Path = SI_DATA_DIR, facts_dir: Path = DATA_DIR) -> dict:
    """스펙 §8 E2 통합 계약 — b3_score와 동형의 import 가능한 순수 함수.
    사용 가능 보고서/분모 없음 = None 점수 + 플래그 (E2 루프 보존)."""
    try:
        share_facts, _ = extract_share_facts(ticker, cutoff, facts_dir)
    except PayloadV2Error:
        share_facts = {}  # 분모 소스 부재 → no_shares_denominator 플래그로 귀결
    return si_core.b4_from_facts(ticker, cutoff, data_dir, share_facts)


def tier_stats_b4(treat: list[float], ctrl: list[float]) -> dict:
    rng = random.Random(SEED_B4)  # (tier, score) 블록별 재시드 — 순서 독립 결정론
    p, obs = stats.perm_test_mean(treat, ctrl, rng)
    a = stats.auc(treat, ctrl)
    lo, hi = stats.boot_auc_ci(treat, ctrl, rng)
    return {"n_treatment": len(treat), "n_control": len(ctrl),
            "mean_diff": round(obs, 6),
            "median_treatment": round(statistics.median(treat), 6),
            "median_control": round(statistics.median(ctrl), 6),
            "auc": round(a, 4), "auc_boot95": [round(lo, 3), round(hi, 3)],
            "perm_p_one_sided": round(p, 6)}


def precision_at_k(scored: list[tuple[str, str, float]], k: int) -> dict:
    """scored: [(case_id, group, score)] 커버 케이스만. 동률은 case_id 사전순
    (중립 결정론 tie-break). 스펙 §5: 농축 표본 — 유니버스 precision@30과 비교 불가."""
    ranked = sorted(scored, key=lambda x: (-x[2], x[0]))[:k]
    hits = sum(1 for _, g, _ in ranked if g == "treatment")
    return {"k": k, "hits": hits,
            "precision": round(hits / k, 4) if k else None,
            "top_k_case_ids": [c for c, _, _ in ranked]}


def main() -> int:
    rosters = load_rosters()
    b3 = json.loads(RESULTS_B3.read_text(encoding="utf-8")) if RESULTS_B3.is_file() else None
    out = {"spec": SPEC, "spec_commit": SPEC_COMMIT, "seed": SEED_B4,
           "n_perm": stats.N_PERM, "n_boot": stats.N_BOOT,
           "primary_score": "score_slope_aug",
           "lag_days": si_core.LAG_DAYS, "data_floor": str(si_core.DATA_FLOOR),
           "frozen_llm_auc": FROZEN_LLM_AUC, "frozen_baseline_auc": FROZEN_B_AUC,
           "tiers": {}, "interpretation": None}

    for tier, roster in rosters.items():
        per_case, missing = {}, []
        for case in sorted(roster, key=lambda c: c["case_id"]):
            r = b4_score(case["ticker"], case["cutoff"])
            per_case[case["case_id"]] = {"ticker": case["ticker"],
                                         "group": case["group"], **r}
            if r["score_slope_aug"] is None and r["score_level"] is None:
                missing.append(case["case_id"])
        n_total = len(roster)
        tier_out = {"n_total": n_total, "missing": missing, "scores": {},
                    "per_case": per_case}
        for score_key in ("score_level", "score_slope_aug"):
            treat = [(cid, v[score_key]) for cid, v in per_case.items()
                     if v["group"] == "treatment" and v[score_key] is not None]
            ctrl = [(cid, v[score_key]) for cid, v in per_case.items()
                    if v["group"] == "control" and v[score_key] is not None]
            covered = len(treat) + len(ctrl)
            cov = covered / n_total
            blk = {"coverage": f"{covered}/{n_total}", "coverage_ratio": round(cov, 4),
                   "headline_eligible": cov >= COVERAGE_HEADLINE_FLOOR,
                   "stats": None, "precision_at_k": None}
            if treat and ctrl:
                blk["stats"] = tier_stats_b4([s for _, s in treat],
                                             [s for _, s in ctrl])
                scored = ([(c, "treatment", s) for c, s in treat]
                          + [(c, "control", s) for c, s in ctrl])
                blk["precision_at_k"] = precision_at_k(
                    scored, k=math.ceil(n_total / 10))
            tier_out["scores"][score_key] = blk
        out["tiers"][tier] = tier_out

    # 스펙 §7 — 비교 성립 조건 판정 (커버리지 >= 70% AND 동결 LLM AUC 존재)
    eligible = [t for t in out["tiers"]
                if out["tiers"][t]["scores"]["score_slope_aug"]["headline_eligible"]
                and FROZEN_LLM_AUC.get(t) is not None]
    out["interpretation"] = {
        "comparison_established_tiers": eligible,
        "reading": ("비교 성립 tier 없음 — wave-1/2는 커버리지 미달(<70%), holdout은 "
                    "동결 LLM AUC 부재(N=3). 무료 신호 벤치마크는 전향 비교(E2 스냅샷·"
                    "sealed 분기)에서 성립한다." if not eligible else
                    "성립 tier에서 LLM<=B4이면 엔진 결정 입력 (스펙 §7 결합 조항)."),
        "engine_coupling": ("비교 성립 조건 충족 미래 시점에서 LLM(또는 워치리스트) "
                            "성능 <= B4 성능이면 E2 평결과 동일 가중치로 엔진 결정 "
                            "입력에 들어간다 — 완화 금지 (specs/B4_short_interest.md §7)")}

    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8")
    OUT_MD.write_text(report_md(out, b3), encoding="utf-8")
    print(f"wrote {OUT_JSON.relative_to(REPO)}, {OUT_MD.relative_to(REPO)}")
    return 0


def _b3_auc(b3: dict | None, tier: str) -> str:
    if not b3:
        return "—"
    try:
        return f"{b3['tiers'][tier]['windows']['W8']['auc']:.4f}"
    except KeyError:
        return "—"


def report_md(out: dict, b3: dict | None) -> str:
    L = ["# B4 리포트 — 비정상 공매도 잔고 기준선 (D55)", "",
         f"- 스펙: {out['spec']} (커밋 {out['spec_commit']}, 계산 전 동결)",
         f"- 데이터: FINRA Consolidated Short Interest, 하한 {out['data_floor']}, "
         f"PIT LAG {out['lag_days']}일",
         f"- 시드 {out['seed']} · perm {out['n_perm']:,} · boot {out['n_boot']:,} · "
         "1차 점수 = slope-augmented", "",
         "> 본 결과는 Claude 기반 단일 파이프라인의 보조 기준선 문서에 한정된다"
         " (PROJECT.md §5-5). LLM/B1/B2/B3 값은 동결 인용 — 재계산 0.", "",
         "## 5열 표 (tier별, pooled 없음)", "",
         "| tier | B1 (M) | B2 (F) | B3 (W8) | **B4 (slope-aug)** | LLM | B4 커버리지 |",
         "|---|---|---|---|---|---|---|"]
    for tier, t in out["tiers"].items():
        blk = t["scores"]["score_slope_aug"]
        b4auc = (f"{blk['stats']['auc']:.4f}" if blk["stats"] else "계산 불가")
        if not blk["headline_eligible"]:
            b4auc += " ⚠️coverage-limited"
        b1 = f"{FROZEN_B_AUC.get(tier, {}).get('B1_beneish_m', 0):.4f}" if tier in FROZEN_B_AUC else "동결값 없음"
        b2 = f"{FROZEN_B_AUC.get(tier, {}).get('B2_dechow_f', 0):.4f}" if tier in FROZEN_B_AUC else "동결값 없음"
        llm = FROZEN_LLM_AUC.get(tier)
        L.append(f"| {tier} | {b1} | {b2} | {_b3_auc(b3, tier)} | {b4auc} | "
                 f"{llm if llm is not None else '없음(N=3)'} | {blk['coverage']} |")
    L += ["", "⚠️coverage-limited = 커버리지 <70% (스펙 §6) — **서술 전용, 헤드라인 "
          "주장 금지**. FINRA 무료 데이터 하한(2017-12-29)이 원인이며 사전 등록된 "
          "산술 그대로다.", "",
          "**결정 관련성 (한 문장)**: 회고 tier의 B4 수치는 어느 것도 판정에 쓰이지 "
          "않는다 — **결정에 관련된 B4 수치는 holdout과 모든 미래 seal이다** (스펙 §7 "
          "결합 조항이 정의하는 전향 비교의 관할).", "",
          ]
    ho = out["tiers"].get("holdout", {}).get("scores", {}).get("score_slope_aug", {})
    if ho and not ho.get("headline_eligible"):
        L += ["**holdout 커버리지 미달의 정직 기록**: 스펙 §6의 사전 산술 기대는 12/12"
              f"였으나 실측 {ho['coverage']} — **holdout조차 70% 바를 미달**해 서술 "
              "전용이다. 원인 진단 (커밋 287a92a): SIR 분모가 "
              "dei:EntityCommonStockSharesOutstanding 단일 태그인데 다중 클래스 "
              "발행사에서 companyfacts가 차원(클래스별) 사실을 비평탄화해 체계적 결측. "
              "교정(분모 폴백 규칙)은 스펙 §3 변경이므로 신규 D-엔트리 스펙 개정으로만 "
              "가능 — **OWNER_QUEUE Q-M03** (첫 seal 전 해소 권장: 같은 분모가 "
              "워치리스트 b4 필드에도 쓰인다).", ""]
    for tier, t in out["tiers"].items():
        L += [f"## {tier}", ""]
        for key in ("score_level", "score_slope_aug"):
            blk = t["scores"][key]
            L.append(f"- **{key}**: coverage {blk['coverage']}"
                     + (f", AUC {blk['stats']['auc']} CI {blk['stats']['auc_boot95']}"
                        f" p={blk['stats']['perm_p_one_sided']}" if blk["stats"] else
                        " — 통계 계산 불가(커버 처치/대조 부족)"))
            if blk["precision_at_k"]:
                pk = blk["precision_at_k"]
                L.append(f"  - precision@{pk['k']} = {pk['precision']} "
                         f"({pk['hits']}/{pk['k']}) — 농축 표본, 유니버스 "
                         "precision@30과 수치 비교 불가 (스펙 §5)")
        if t["missing"]:
            L.append(f"- 결측 케이스 (fail-closed): {', '.join(t['missing'])}")
        L.append("")
    itp = out["interpretation"]
    L += ["## 해석 (스펙 §7 사전 등록 규칙)", "",
          f"- 비교 성립 tier: {itp['comparison_established_tiers'] or '없음'}",
          f"- {itp['reading']}", f"- 결합 조항: {itp['engine_coupling']}", ""]
    return "\n".join(L)


if __name__ == "__main__":
    sys.exit(main())
