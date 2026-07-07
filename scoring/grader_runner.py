"""채점자 러너 (freeze 개정 #2 — 구독 헤드리스 경로. 피평가자 자료 흐름과 단방향 분리).

채점자는 정답 키 + 피평가자 출력을 받는다; 피평가자는 채점자 자료를 절대 받지 않는다
(V7 — 이 모듈은 pipeline/ 이 아니라 scoring/ 에 있고, pipeline/ 은 scoring import가
정적 스캔으로 금지된다. scoring→pipeline 방향의 cli_client 공유는 규약 위반이 아니다).

사용: python scoring/grader_runner.py --runs runs/main --out scoring/grades/main
모델: 채점자 = claude-fable-5, 폴백 claude-opus-4-8 (D6 — 발동 사유·케이스 ID 로그).
채점은 1차일 뿐이다 — "채점: Claude 보조 + 인간 최종 확정" (§7).
stdout은 중립 ID만 출력한다 (원본 ID 노출 금지 — 라벨 결합은 Phase 6).
멱등: 채점 파일 존재+스키마 통과 = skip. 레이트 리밋 = 재개 명령 출력 후 중단.
"""
from __future__ import annotations

import argparse
import datetime
import json
import shlex
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
import cli_client  # noqa: E402  (scoring→pipeline 방향 — V7 허용 방향)

GRADER_PIN = "claude-fable-5"
GRADER_FALLBACK = "claude-opus-4-8"
FALLBACK_REASONS = {"error", "refusal", "empty", "schema_failure"}  # 접근불능·거부·절단

GRADE_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["dim1_probability_band", "dim2_mechanism", "dim3_genre_mapping",
                 "dim4_evidence_quality", "memorization_suspect_condition2",
                 "rationale"],
    "properties": {
        "dim1_probability_band": {"type": "integer", "enum": [0, 1, 2]},
        "dim2_mechanism": {"type": ["integer", "null"], "enum": [0, 1, 2, 3, None]},
        "dim3_genre_mapping": {
            "type": "object", "additionalProperties": False,
            "required": ["mapped_genre", "score"],
            "properties": {"mapped_genre": {"type": ["string", "null"],
                                            "enum": ["active", "omission-estimate", "mixed", None]},
                           "score": {"type": ["integer", "null"], "enum": [0, 1, 2, None]}}},
        "dim4_evidence_quality": {"type": "integer", "enum": [0, 1, 2, 3]},
        "memorization_suspect_condition2": {"type": "boolean"},
        "rationale": {"type": "string"},
    },
}

SYSTEM = """You are grading one output of a financial-analysis pipeline against ground truth, \
using a fixed 4-dimension rubric. Apply the rubric mechanically; every score must be justified \
in 'rationale' by pointing at specific parts of the output and the answer key. You are the \
first-pass grader; a human auditor finalizes all grades. Do not reward confident language - \
only evidence. Rubric (fixed at freeze):
- dim1 (probability band): treatment case: p>=70 -> 2, 50<=p<70 -> 1, p<50 -> 0. \
control case: p<=30 -> 2, 30<p<50 -> 1, p>=50 -> 0.
- dim2 (mechanism, treatment only, TOP-RANKED hypothesis only; control -> null): \
0 = no hypothesis (required if p>=40) or unrelated accounts; 1 = correct account area; \
2 = account + direction + treatment type substantially match the enforcement-order description; \
3 = additionally names at least one case-specific fact pinpointed in the answer key. \
Multi-mechanism truth: grade best match, note coverage in rationale.
- dim3 (genre mapping, treatment only; control -> nulls): map the top-ranked hypothesis \
narrative to active / omission-estimate / mixed, then score against the answer-key genre: \
exact 2; one-sided-vs-mixed 1; wrong 0.
- dim4 (evidence quality, all cases): 0 fabricated/irrelevant citations; 1 generic; \
2 specific provided data points genuinely support the claims (including any mechanism \
assertions on control cases); 3 = 2 plus coherent multi-year/multi-point combination. \
Cap at 1 if risk_tier contradicts the declared consistency rule \
(p>=70 => elevated; 40<=p<70 => watch/elevated; p<40 => clear/watch).
- memorization_suspect_condition2 (mechanical, L-1): true iff the output's reasoning \
(a) lists documents without pointing at any concrete provided data content, or \
(b) mentions facts only public after the cutoff (revelation, enforcement, outcome)."""


def answer_key(original_id: str, candidates_path: str = "data/candidates/candidates.json") -> dict:
    cands = {c["case_id"]: c for c in json.loads(
        (REPO / candidates_path).read_text(encoding="utf-8"))["candidates"]}
    c = cands[original_id]
    genre = None
    genre_table = (REPO / "scoring/genre_tags.md").read_text(encoding="utf-8")
    for line in genre_table.splitlines():
        if line.startswith(f"| {original_id} "):
            genre = line
            break
    return {
        "group": c["group"],
        "scheme_summary": c.get("scheme_summary"),
        "scheme_type": c.get("scheme_type"),
        "manipulation_period": [c.get("manipulation_period_start"), c.get("manipulation_period_end")],
        "genre_tag_row": genre,
    }


def _existing_grade_valid(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    body = {k: v for k, v in data.items() if k != "_meta"}
    import jsonschema
    return not list(jsonschema.Draft7Validator(GRADE_SCHEMA).iter_errors(body))


def grade_one(neutral: str, original_id: str, output: dict,
              out_dir: Path, log_dir: Path, mapping_path_note: str,
              candidates_path: str = "data/candidates/candidates.json") -> str:
    out_path = out_dir / f"{neutral}.json"
    if _existing_grade_valid(out_path):
        return "skip (멱등)"
    key = answer_key(original_id, candidates_path)
    user_payload = json.dumps({"answer_key": key, "evaluatee_output": output},
                              ensure_ascii=False)
    used_model, r = GRADER_PIN, None
    for model in (GRADER_PIN, GRADER_FALLBACK):
        r = cli_client.call_model(model, SYSTEM, user_payload, GRADE_SCHEMA,
                                  log_dir=log_dir, log_name=f"grader_{model}_{neutral}")
        used_model = model
        if r.ok:
            break
        if r.fail_reason in FALLBACK_REASONS and model == GRADER_PIN:
            print(f"  {neutral}: {model} 실패({r.fail_reason}) — 폴백 {GRADER_FALLBACK} "
                  f"(D6 폴백 발동 기록)", file=sys.stderr, flush=True)
            continue
        break
    if not r.ok:
        return f"FAIL ({r.fail_reason})"

    grade = dict(r.structured)
    grade["_meta"] = {
        "case_id": neutral, "original_id": original_id,
        "grader_model_reported": (r.served_models or [used_model])[0],
        "grader_pin_used": used_model,
        "fallback_used": used_model != GRADER_PIN,
        "session_id": r.session_id,
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "human_finalized": False,
        "mapping_access_note": mapping_path_note,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(grade, ensure_ascii=False, indent=2), encoding="utf-8")
    return (f"OK d1={grade['dim1_probability_band']} d2={grade['dim2_mechanism']} "
            f"d4={grade['dim4_evidence_quality']} mem2={grade['memorization_suspect_condition2']}"
            + (" [fallback]" if grade["_meta"]["fallback_used"] else ""))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--candidates", default="data/candidates/candidates.json",
                    help="RP-09: v2 대조군은 data/candidates/candidates_v2_controls.json")
    ap.add_argument("--mapping", default="scoring/id_mapping.json",
                    help="파일럿은 scoring/id_mapping_pilot.json")
    args = ap.parse_args()

    cli_client.assert_no_metered_credentials()
    cli_client.require_clean_tree()

    mapping = json.loads((REPO / args.mapping).read_text(encoding="utf-8"))["mapping"]
    out_dir = REPO / args.out
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = REPO / "logs" / f"run_{ts}"
    note = (f"{args.mapping} opened mechanically by grader_runner for answer-key join; "
            f"neutral IDs only on stdout (label-joining deferred to Phase 6)")
    resume_cmd = "python scoring/grader_runner.py " + " ".join(
        shlex.quote(a) for a in sys.argv[1:])

    failures = 0
    try:
        for run_file in sorted((REPO / args.runs).glob("case_*.json")):
            output = json.loads(run_file.read_text(encoding="utf-8"))
            neutral = output["case_id"]
            status = grade_one(neutral, mapping[neutral], output, out_dir, log_dir, note,
                               candidates_path=args.candidates)
            if status.startswith("FAIL"):
                failures += 1
            print(f"{neutral}: {status}", flush=True)
    except cli_client.RateLimitedError as e:
        print(f"\nHALT — {e}", file=sys.stderr)
        print(f"재개 명령 (완료분 자동 skip):\n  {resume_cmd}")
        return 3
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
