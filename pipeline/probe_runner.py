"""오염 프로브 러너 (Phase 3-2) — scoring/probes.md 설계의 실행부.

  python pipeline/probe_runner.py --recognition --cases <교란 대상 케이스 파일>
  python pipeline/probe_runner.py --verbatim   --cases <원본 케이스 파일>

출력: scoring/probe_results/{recognition,verbatim}/{case_id}.json + api_run_log.
판정(일치 여부)은 채점 쪽 스크립트가 수행 — 이 러너는 모델 응답 수집만.
헤더 의무: these controls BOUND memorization risk; they do not eliminate it.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
from pathlib import Path

import build_payload as bp
from runner import EVALUATEE_MODEL, freeze_state

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG = REPO_ROOT / "logs" / "api_run_log.jsonl"

RECOG_SCHEMA = {"type": "object", "additionalProperties": False,
                "required": ["company_guess", "confidence"],
                "properties": {"company_guess": {"type": "string"},
                               "confidence": {"type": "string", "enum": ["high", "medium", "low"]}}}
RECOG_TASK = ("Based on the structured filing data above, which specific company is this? "
              "Answer with the company's real name, or 'unknown'.")

VERBATIM_SCHEMA = {"type": "object", "additionalProperties": False,
                   "required": ["revenue", "net_income", "filing_date", "known"],
                   "properties": {"revenue": {"type": ["number", "null"]},
                                  "net_income": {"type": ["number", "null"]},
                                  "filing_date": {"type": ["string", "null"]},
                                  "known": {"type": "boolean"}}}
VERBATIM_TASK = ("Without any documents: state {company_name}'s exact reported total revenue "
                 "and net income (USD) for the fiscal year ending immediately before "
                 "{cutoff_date}, and the filing date of that annual report. "
                 "If you do not know, set known=false and use nulls.")


def call(client, system: str, user: str, schema: dict) -> tuple[dict, object, float]:
    t0 = time.monotonic()
    resp = client.messages.create(model=EVALUATEE_MODEL, max_tokens=2000, system=system,
                                  output_config={"format": {"type": "json_schema", "schema": schema}},
                                  messages=[{"role": "user", "content": user}])
    text = next(b.text for b in resp.content if b.type == "text")
    return json.loads(text), resp, time.monotonic() - t0


def log_row(kind, case_id, resp, wall):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "probe": kind, "case_id": case_id, "model_reported": resp.model,
            "request_id": getattr(resp, "_request_id", None),
            "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens,
            "wall_seconds": round(wall, 1), "freeze": freeze_state(),
        }, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--recognition", action="store_true")
    ap.add_argument("--verbatim", action="store_true")
    ap.add_argument("--cases", default=str(bp.EVALUATEE_CASES))
    args = ap.parse_args()

    import anthropic
    client = anthropic.Anthropic()
    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))["cases"]
    out_root = REPO_ROOT / "scoring" / "probe_results"

    if args.recognition:
        out = out_root / "recognition"
        out.mkdir(parents=True, exist_ok=True)
        for case in cases:
            payload = bp.build_payload(case, perturb=True)
            payload.pop("_k_internal")
            result, resp, wall = call(
                client, RECOG_TASK,
                json.dumps(payload, ensure_ascii=False), RECOG_SCHEMA)
            (out / f"{case['case_id']}.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            log_row("recognition", case["case_id"], resp, wall)
            print(f"{case['case_id']}: guess={result['company_guess']!r} ({result['confidence']})")

    if args.verbatim:
        out = out_root / "verbatim"
        out.mkdir(parents=True, exist_ok=True)
        for case in cases:
            task = VERBATIM_TASK.format(company_name=case["company_name"],
                                        cutoff_date=case["cutoff_date"])
            result, resp, wall = call(client, task, "Answer now.", VERBATIM_SCHEMA)
            (out / f"{case['case_id']}.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            log_row("verbatim", case["case_id"], resp, wall)
            print(f"{case['case_id']}: known={result['known']} rev={result['revenue']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
