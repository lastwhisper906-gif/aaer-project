"""buyer_metrics_build.py — E2 완료 후 구매자 지표 4종 자동 채움 (D52).

입력: analysis/e2_trajectories.json (specs/ENGINE_DECISION.md §1 스키마 —
      엔진 판정과 동일 파일, 동일 산식) + E2 호출 로그 디렉토리 (usage 실측).
출력: analysis/BUYER_METRICS.md (BUYER_METRICS.template.md의 placeholder 채움).

E2 동결 스펙(EARLINESS_PLAN.md)은 무변경 소비 — 본 스크립트는 어댑터가 조립한
trajectories와 로그만 읽는다. 손 계산 금지: 전 수치가 이 스크립트 산출.

사용: .venv/bin/python analysis/buyer_metrics_build.py \
        [--traj PATH] [--logs-dir DIR] [--price-in USD/MTok --price-out USD/MTok]
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
from engine_verdict import case_lead  # noqa: E402 (D51 판정과 동일 산식)
from holdout_controls_analyze import clopper_pearson  # noqa: E402 (동결 CP 재사용)

TEMPLATE = REPO / "analysis" / "BUYER_METRICS.template.md"
DEFAULT_TRAJ = REPO / "analysis" / "e2_trajectories.json"
DEFAULT_OUT = REPO / "analysis" / "BUYER_METRICS.md"
STAGE2_UNIVERSE = 300  # docs 퍼널 stage-2 규모 (screener/docs/FUNNEL.md §2)


class BuyerMetricsError(Exception):
    """fail-closed: 빈 그룹·로그 usage 부재 — 조용한 0 금지."""


def _pct(k: int, n: int) -> str:
    return f"{k}/{n} = {100 * k / n:.1f}%"


def _ci(k: int, n: int) -> str:
    lo, hi = clopper_pearson(k, n)
    return f"[{100 * lo:.1f}%, {100 * hi:.1f}%]"


def compute(traj: dict, logs_dir: Path | None,
            price_in: float | None, price_out: float | None) -> dict:
    thr_llm, thr_b3 = traj["flag_threshold_llm"], traj["flag_threshold_b3"]
    treat = [c for c in traj["cases"] if c["group"] == "treatment"]
    ctrl = [c for c in traj["cases"] if c["group"] == "control"]
    if not treat or not ctrl:
        raise BuyerMetricsError("실험군/대조군 중 빈 그룹 — 지표 정의 불능")

    # 1. 리드타임 (엔진 판정과 동일 산식 — case_lead import)
    leads_llm = [case_lead(c["snapshots"], "llm_p", thr_llm) for c in treat]
    leads_b3 = [case_lead(c["snapshots"], "b3_score", thr_b3) for c in treat]

    # 2. FPR@임계 — 대조군: 어느 스냅샷이든 돌파 = 오탐 (운영 semantics)
    fp_llm = sum(1 for c in ctrl
                 if any(s["llm_p"] is not None and s["llm_p"] >= thr_llm
                        for s in c["snapshots"]))
    fp_b3 = sum(1 for c in ctrl
                if any(s["b3_score"] is not None and s["b3_score"] >= thr_b3
                       for s in c["snapshots"]))

    # 3. 비용 — E2 로그 usage 실측
    tokens_in, tokens_out = [], []
    if logs_dir is not None:
        for p in sorted(Path(logs_dir).rglob("*.json")):
            u = json.loads(p.read_text(encoding="utf-8")).get("usage")
            if u and u.get("input_tokens") is not None:
                tokens_in.append(u["input_tokens"])
                tokens_out.append(u["output_tokens"])
        if not tokens_in:
            raise BuyerMetricsError(f"{logs_dir}: usage 실측 로그 0건 — 비용 지표 계산 불능")
    have_price = price_in is not None and price_out is not None
    if tokens_in:
        in_mean = statistics.mean(tokens_in)
        out_mean = statistics.mean(tokens_out)
        cost = (in_mean * price_in + out_mean * price_out) / 1e6 if have_price else None
    else:
        in_mean = out_mean = cost = None

    depth = [len(c["snapshots"]) for c in traj["cases"]]
    truncated = [c["case_id"] for c in traj["cases"] if len(c["snapshots"]) < 8]
    return {
        "lead_llm_median": statistics.median(leads_llm),
        "lead_b3_median": statistics.median(leads_b3),
        "lead_llm_range": f"{min(leads_llm)}–{max(leads_llm)}",
        "lead_b3_range": f"{min(leads_b3)}–{max(leads_b3)}",
        "n_treatment": len(treat), "n_control": len(ctrl),
        "fpr_llm": _pct(fp_llm, len(ctrl)), "fpr_llm_ci": _ci(fp_llm, len(ctrl)),
        "fpr_b3": _pct(fp_b3, len(ctrl)), "fpr_b3_ci": _ci(fp_b3, len(ctrl)),
        "tokens_in_mean": round(in_mean) if in_mean is not None else "로그 미지정",
        "tokens_out_mean": round(out_mean) if out_mean is not None else "로그 미지정",
        "n_calls_measured": len(tokens_in),
        "cost_per_screen": f"${cost:.4f}" if cost is not None
                           else "단가 미입력 (--price-in/--price-out)",
        "cost_stage2_pass": f"${cost * STAGE2_UNIVERSE:,.2f} (~{STAGE2_UNIVERSE}건)"
                            if cost is not None else "단가 미입력",
        "pricing_note": (f"입력 ${price_in}/MTok · 출력 ${price_out}/MTok (소유자 입력)"
                         if have_price else "단가 미입력 — 소유자가 실행 시점 공식 단가로 지정"),
        "coverage_treatment": f"E2 적격 detected fraud {len(treat)}건 (EARLINESS_PLAN §1)",
        "coverage_control": f"RP-01 확정 대조군 {len(ctrl)}건 (동일 그리드, EARLINESS_PLAN §4)",
        "coverage_depth": f"케이스당 스냅샷 중위 {statistics.median(depth)} (상한 8)",
        "coverage_truncation": (f"깊이 8 미만 {len(truncated)}건: {', '.join(truncated)}"
                                if truncated else "절단 없음 (전 케이스 깊이 8)"),
    }


def render(values: dict) -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("(E2 완료 후 자동 채움, D52)", "(자동 생성 — 수기 편집 금지)")
    for key, val in values.items():
        text = text.replace("{" + key + "}", str(val))
    leftover = [w for w in text.split() if w.startswith("{") and w.rstrip(".,)").endswith("}")]
    if leftover:
        raise BuyerMetricsError(f"미채움 placeholder: {leftover} — 템플릿/빌더 불일치")
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--traj", default=str(DEFAULT_TRAJ))
    ap.add_argument("--logs-dir", default=None)
    ap.add_argument("--price-in", type=float, default=None)
    ap.add_argument("--price-out", type=float, default=None)
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()
    values = compute(json.loads(Path(args.traj).read_text(encoding="utf-8")),
                     Path(args.logs_dir) if args.logs_dir else None,
                     args.price_in, args.price_out)
    Path(args.out).write_text(render(values), encoding="utf-8")
    print(f"buyer metrics -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
