"""RP-06 A2 — 교차 패밀리 채점 스팟체크 (claude-opus-4-8, 6호출).

소유자 지시 addendum(RP-06, decisions_log 2026-07-06)의 A2 실행부.
채점 페이로드 구성(answer_key + evaluatee_output)·시스템 프롬프트·스키마는
frozen `grader_runner`에서 그대로 import — 유일한 차이는 (i) 모델이 설계상
claude-opus-4-8 고정, (ii) 출력이 scoring/grades/ 가 아니라
runs/hardening/regrade_opus/ 에 SPOT-CHECK 라벨로 격리된다는 것.
**이 출력은 절대 scoring/grades/ 에 병합하지 않는다** — 소유자 확정 단계의
참고 증거 전용.

대상 6건 (지시문 A2):
  - RP-05 §6 MODEL 귀속 5건: case_01/02/03/12 (본 분석 = 교란 채점 →
    runs/perturbed 출력), case_10 (대조군 → runs/main 출력).
  - 비플래그 1건: RP-05 §6 오류 표에 등장하지 않는 9건 중 RNG 무작위 선택 —
    시드 20260706 (본 사이클 중립 ID 셔플 시드와 동일 관례), 선택 결과 로그.

  python scoring/regrade_spotcheck.py
"""
from __future__ import annotations

import datetime
import json
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
sys.path.insert(0, str(REPO / "scoring"))
import cli_client  # noqa: E402
import grader_runner  # noqa: E402  (frozen 채점 페이로드·프롬프트·스키마 재사용)

SPOT_MODEL = "claude-opus-4-8"  # A2 설계 고정 (지시문 PRE-AUTHORIZATION)
OUT_DIR = REPO / "runs" / "hardening" / "regrade_opus"
RNG_SEED = 20260706

# RP-05 §6 MODEL 귀속 5건 — 본 분석 채점과 동일 변형 (실험군=교란, 대조군=원본)
MODEL_ATTRIBUTED = [
    ("case_01", "runs/perturbed"),
    ("case_02", "runs/perturbed"),
    ("case_03", "runs/perturbed"),
    ("case_12", "runs/perturbed"),
    ("case_10", "runs/main"),
]
# RP-05 §6 오류 표(케이스 단위)에 등장하지 않는 케이스 전수 (플래그 = 01,02,03,06,10,12,13)
NON_FLAGGED_POOL = ["case_04", "case_05", "case_07", "case_08", "case_09",
                    "case_11", "case_14", "case_15", "case_16"]


def spot_targets() -> list[tuple[str, str]]:
    treat = {c["case_id"] for c in json.loads(
        (REPO / "scoring/perturbed_cases.json").read_text(encoding="utf-8"))["cases"]}
    pick = random.Random(RNG_SEED).choice(sorted(NON_FLAGGED_POOL))
    variant = "runs/perturbed" if pick in treat else "runs/main"
    print(f"비플래그 무작위 선택: {pick} (seed={RNG_SEED}, pool={len(NON_FLAGGED_POOL)}건, "
          f"변형={variant})", flush=True)
    return MODEL_ATTRIBUTED + [(pick, variant)]


def regrade_one(neutral: str, runs_dir: str, mapping: dict, log_dir: Path) -> str:
    out_path = OUT_DIR / f"{neutral}.json"
    if grader_runner._existing_grade_valid(out_path):
        return "skip (멱등)"
    output = json.loads((REPO / runs_dir / f"{neutral}.json").read_text(encoding="utf-8"))
    original_id = mapping[neutral]
    key = grader_runner.answer_key(original_id)
    # frozen grader_runner.grade_one과 동일한 페이로드 구성 (바이트 동일 규약)
    user_payload = json.dumps({"answer_key": key, "evaluatee_output": output},
                              ensure_ascii=False)
    r = cli_client.call_model(SPOT_MODEL, grader_runner.SYSTEM, user_payload,
                              grader_runner.GRADE_SCHEMA,
                              log_dir=log_dir, log_name=f"regrade_{SPOT_MODEL}_{neutral}")
    if not r.ok:
        return f"FAIL ({r.fail_reason})"
    grade = dict(r.structured)
    grade["_meta"] = {
        "label": "SPOT-CHECK — cross-family grader agreement (RP-06 A2). "
                 "NEVER merge into scoring/grades/.",
        "case_id": neutral, "original_id": original_id,
        "variant_graded": runs_dir,
        "grader_model_reported": (r.served_models or [SPOT_MODEL])[0],
        "grader_pin_used": SPOT_MODEL,
        "rng_seed_nonflagged": RNG_SEED,
        "session_id": r.session_id,
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "human_finalized": False,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(grade, ensure_ascii=False, indent=2), encoding="utf-8")
    return (f"OK d1={grade['dim1_probability_band']} d2={grade['dim2_mechanism']} "
            f"d4={grade['dim4_evidence_quality']} mem2={grade['memorization_suspect_condition2']}")


def main() -> int:
    cli_client.assert_no_metered_credentials()
    cli_client.require_clean_tree()

    mapping = json.loads((REPO / "scoring/id_mapping.json").read_text(encoding="utf-8"))["mapping"]
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = REPO / "logs" / f"run_{ts}"

    failures = 0
    try:
        for neutral, runs_dir in spot_targets():
            status = regrade_one(neutral, runs_dir, mapping, log_dir)
            if status.startswith("FAIL"):
                failures += 1
            print(f"{neutral}: {status}", flush=True)
    except cli_client.RateLimitedError as e:
        print(f"\nHALT — {e}", file=sys.stderr)
        print("재개 명령 (완료분 자동 skip):\n  python scoring/regrade_spotcheck.py")
        return 3
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
