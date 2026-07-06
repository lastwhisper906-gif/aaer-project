"""채점자 러너 (Phase 3 — 채점 쪽 코드. 피평가자 자료 흐름과 단방향 분리).

채점자는 정답 키 + 피평가자 출력을 받는다; 피평가자는 채점자 자료를 절대 받지 않는다
(V7 — 이 모듈은 pipeline/ 이 아니라 scoring/ 에 있고, pipeline/ 은 scoring import가
정적 스캔으로 금지된다).

사용: python scoring/grader_runner.py --runs runs/main --out scoring/grades/main
모델: 채점자 = claude-fable-5, 폴백 claude-opus-4-8 (D6 — 폴백 발동은 로그).
채점은 1차일 뿐이다 — "채점: Claude 보조 + 인간 최종 확정" (§7).
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GRADER_PIN = "claude-fable-5"
GRADER_FALLBACK = "claude-opus-4-8"
LOG = REPO / "logs" / "api_run_log.jsonl"

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


def call_grader(client, user_payload: str):
    import anthropic
    for model in (GRADER_PIN, GRADER_FALLBACK):
        try:
            t0 = time.monotonic()
            resp = client.messages.create(
                model=model, max_tokens=4000, system=SYSTEM,
                output_config={"format": {"type": "json_schema", "schema": GRADE_SCHEMA}},
                messages=[{"role": "user", "content": user_payload}])
            if resp.stop_reason == "refusal":
                print(f"  {model} refusal — 폴백 시도", file=sys.stderr)
                continue
            return resp, model, time.monotonic() - t0
        except anthropic.BadRequestError as e:
            print(f"  {model} 사용 불가({e.status_code}) — 폴백 시도", file=sys.stderr)
            continue
    raise RuntimeError("채점자 핀·폴백 모두 실패")


def answer_key(original_id: str) -> dict:
    cands = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates.json").read_text(encoding="utf-8"))["candidates"]}
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    import anthropic
    client = anthropic.Anthropic()
    mapping = json.loads((REPO / "scoring/id_mapping.json").read_text(encoding="utf-8"))["mapping"]
    out_dir = REPO / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    for run_file in sorted((REPO / args.runs).glob("case_*.json")):
        output = json.loads(run_file.read_text(encoding="utf-8"))
        neutral = output["case_id"]
        key = answer_key(mapping[neutral])
        user_payload = json.dumps({"answer_key": key, "evaluatee_output": output},
                                  ensure_ascii=False)
        resp, used_model, wall = call_grader(client, user_payload)
        grade = json.loads(next(b.text for b in resp.content if b.type == "text"))
        grade["_meta"] = {
            "case_id": neutral, "original_id": mapping[neutral],
            "grader_model_reported": resp.model, "grader_pin_used": used_model,
            "fallback_used": used_model != GRADER_PIN,
            "request_id": getattr(resp, "_request_id", None),
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "human_finalized": False,
        }
        (out_dir / f"{neutral}.json").write_text(
            json.dumps(grade, ensure_ascii=False, indent=2), encoding="utf-8")
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": grade["_meta"]["ts"], "grader": used_model,
                                "case_id": neutral, "wall_seconds": round(wall, 1),
                                "input_tokens": resp.usage.input_tokens,
                                "output_tokens": resp.usage.output_tokens},
                               ensure_ascii=False) + "\n")
        print(f"{neutral} ({mapping[neutral]}): d1={grade['dim1_probability_band']} "
              f"d2={grade['dim2_mechanism']} d4={grade['dim4_evidence_quality']} "
              f"mem2={grade['memorization_suspect_condition2']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
