"""engine_verdict.py — 엔진 판정 기계 계산 (specs/ENGINE_DECISION.md, D51).

스펙 사전 등록 커밋이 본 파일보다 선행한다. 판정은 §4의 순서 고정·전역 완전
규칙 그대로 — 이 스크립트 밖의 어떤 서사도 판정에 개입하지 못한다.

입력: analysis/e2_trajectories.json (스펙 §1 스키마 — E2 완료 후 어댑터가 조립)
출력: analysis/engine_verdict.json (판정 + 중간값 + 케이스별 lead 전수 표)

사용: .venv/bin/python analysis/engine_verdict.py [--in PATH] [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
from stats import auc  # noqa: E402 (동결 tie-aware AUC 의미론 — 스펙 §3)

DEFAULT_IN = REPO / "analysis" / "e2_trajectories.json"
DEFAULT_OUT = REPO / "analysis" / "engine_verdict.json"
B3_SENSITIVITY = (1, 3)  # 스펙 §2 — 병기 전용, 판정 무가중


class VerdictError(Exception):
    """fail-closed: 스키마 위반·빈 그룹 — 조용한 기본값 금지."""


def case_lead(snapshots: list[dict], score_key: str, threshold: int) -> int:
    """스펙 §3: 임계 돌파 스냅샷 중 최대 quarters_to_revelation, 없으면 0."""
    crossed = [s["quarters_to_revelation"] for s in snapshots
               if s[score_key] is not None and s[score_key] >= threshold]
    return max(crossed, default=0)


def _snapshot0(case: dict, score_key: str):
    j0 = [s for s in case["snapshots"] if s["j"] == 0]
    if len(j0) != 1:
        raise VerdictError(f"{case['case_id']}: 스냅샷 j=0이 정확히 1개여야 함 ({len(j0)}개)")
    return j0[0][score_key]


def compute(traj: dict) -> dict:
    thr_llm = traj["flag_threshold_llm"]
    thr_b3 = traj["flag_threshold_b3"]
    if (thr_llm, thr_b3) != (50, 2):
        raise VerdictError(f"임계 ({thr_llm},{thr_b3}) ≠ 사전 등록 (50,2) — 스펙 §2 위반")
    treat = [c for c in traj["cases"] if c["group"] == "treatment"]
    ctrl = [c for c in traj["cases"] if c["group"] == "control"]
    if not treat or not ctrl:
        raise VerdictError("실험군/대조군 중 빈 그룹 — 판정 불능 (fail-closed)")

    leads = [{"case_id": c["case_id"], "ticker": c["ticker"],
              "lead_llm": case_lead(c["snapshots"], "llm_p", thr_llm),
              "lead_b3": case_lead(c["snapshots"], "b3_score", thr_b3),
              **{f"lead_b3_ge{t}": case_lead(c["snapshots"], "b3_score", t)
                 for t in B3_SENSITIVITY}}
             for c in treat]
    med_llm = statistics.median(l["lead_llm"] for l in leads)
    med_b3 = statistics.median(l["lead_b3"] for l in leads)

    auc_llm = auc([_snapshot0(c, "llm_p") for c in treat],
                  [_snapshot0(c, "llm_p") for c in ctrl])
    auc_b3 = auc([_snapshot0(c, "b3_score") for c in treat],
                 [_snapshot0(c, "b3_score") for c in ctrl])

    # 스펙 §4 — 순서 고정, 첫 일치가 판정
    if med_llm <= 1 and med_b3 <= 1:
        branch, reading = "c_terminated", ("어느 쪽도 폭로 직전 분기를 넘는 선행 신호 없음 — "
                                           "도구 경로 종료, screener 아카이브, stage-2 없음")
    elif med_llm >= med_b3 + 1:
        branch, reading = "a_llm_engine", "LLM lead ≥ B3+1분기 — stage-2 활성"
    else:
        branch, reading = "b_rules_engine", ("규칙 엔진 — stage-2 제거, LLM은 리포트 초안 "
                                             "보조로 강등")
    sub = None
    if branch == "b_rules_engine":
        sub = "b_strict" if (med_b3 >= med_llm and auc_b3 >= auc_llm) else "b_residual"

    return {"spec": "specs/ENGINE_DECISION.md", "spec_decision": "D51",
            "thresholds": {"llm_p": thr_llm, "b3_score": thr_b3},
            "median_lead_llm_quarters": med_llm,
            "median_lead_b3_quarters": med_b3,
            "auc_snapshot0": {"llm": round(auc_llm, 4), "b3": round(auc_b3, 4)},
            "n_treatment": len(treat), "n_control": len(ctrl),
            "branch": branch, "b_subcase": sub, "reading": reading,
            "per_case_leads": sorted(leads, key=lambda l: l["case_id"]),
            "note": "판정은 스펙 §4 기계 규칙 — 본 결과는 Claude 기반 단일 파이프라인에 한정 (§5-5)"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="inp", default=str(DEFAULT_IN))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()
    verdict = compute(json.loads(Path(args.inp).read_text(encoding="utf-8")))
    Path(args.out).write_text(json.dumps(verdict, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8")
    print(f"engine verdict: {verdict['branch']}"
          + (f" ({verdict['b_subcase']})" if verdict["b_subcase"] else "")
          + f" — lead LLM {verdict['median_lead_llm_quarters']}q vs "
            f"B3 {verdict['median_lead_b3_quarters']}q")
    return 0


if __name__ == "__main__":
    sys.exit(main())
