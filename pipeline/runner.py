"""피평가자 러너 (Phase 3-3/3-4) — 케이스별 독립 API 호출, 페이로드 규약 강제.

사용:
  python pipeline/runner.py --pilot            # pilot/ 격리 (T18/T25 상당 케이스는
                                               #  실험 16 밖 — 별도 케이스 파일 지정)
  python pipeline/runner.py --main             # 원본 16
  python pipeline/runner.py --perturbed        # 교란 8 (실험군만 — 러너는 그룹을
                                               #  모르므로 케이스 목록은 채점 쪽이
                                               #  파일로 제공: --cases <json>)
  공통: --cases <evaluatee-format json> 로 케이스 파일 대체 가능.

규약 (GP-6 3조항 + V4/V7):
  - 호출당 컨텍스트 = 시스템 프롬프트(아래 TASK) + 페이로드 JSON 하나. 저장소 문서·
    다른 케이스·채점 자료 일절 미포함.
  - 이 모듈은 scoring/ 를 import하지 않는다 (정적 스캔).
  - run log: response.model(서버 보고 문자열)·request id·타임스탬프·토큰·freeze 해시.
  - 모델 핀: 피평가자 = claude-sonnet-5 (scoring/decisions_log.md D6 — 문자열만 여기 복제).
"""
from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys
import time
from pathlib import Path

import build_payload as bp

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALUATEE_MODEL = "claude-sonnet-5"  # D6 pin (사유는 채점 쪽 문서)
OUTPUT_SCHEMA_PATH = REPO_ROOT / "schemas" / "llm_output.json"

TASK = """You are analyzing the financial reporting quality of {company_name} ({ticker}{cik_part}) \
using only the structured data provided below, which reflects public filings available on or \
before {cutoff_date}. Do not use any knowledge of events after {cutoff_date}. Complete the \
checklist, then: (a) estimate the probability (0-100) that the company's financial statements \
contain, or have contained during the periods covered by the available filings, a material \
misstatement; (b) if you estimate this probability at 40 or above, describe the most likely \
mechanism(s), most confident first (at most 3): which financial statement line items are \
affected, in which direction, and through what accounting treatment. Every finding must cite \
the specific data points provided, in the form 'concept=value (period)'. If the data is \
insufficient for an item, say so - do not guess.

Checklist items (answer each with finding flag/no_flag/insufficient_data + evidence):
CL1 Did receivables grow materially faster than revenue across consecutive periods?
CL2 Did non-current 'soft' assets (intangibles, other assets, capitalized items) grow materially faster than the business overall?
CL3 Is there a persistent divergence between net income and operating cash flow?
CL4 Do inventory levels or gross margins show trends inconsistent with revenue?
CL5 Is the earnings trajectory unusually smooth relative to the volatility of revenue and cash flow?
CL6 Did liability, allowance, or reserve balances decline (or fail to grow) despite growing business activity?
CL7 Does the filing chronology show irregularities (late filings/NT forms, amendments, unusual 8-K frequency)?
CL8 Is the provided data sufficient in coverage and length for the above assessments?"""

# 모델이 채우는 부분만의 스키마 (구조화 출력용 — 파이프라인 메타 필드는 러너가 채움)
MODEL_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["checklist", "misstatement_probability", "mechanism_hypotheses", "overall"],
    "properties": {
        "checklist": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["item_id", "question", "finding", "confidence", "evidence"],
            "properties": {
                "item_id": {"type": "string"},
                "question": {"type": "string"},
                "finding": {"type": "string", "enum": ["flag", "no_flag", "insufficient_data"]},
                "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                "evidence": {"type": "array", "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["quote", "source_accession_no", "location"],
                    "properties": {"quote": {"type": "string"},
                                   "source_accession_no": {"type": "string"},
                                   "location": {"type": "string"}}}},
            }}},
        "misstatement_probability": {"type": "integer"},
        "mechanism_hypotheses": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["affected_line_items", "direction", "accounting_treatment", "rationale_evidence"],
            "properties": {
                "affected_line_items": {"type": "array", "items": {"type": "string"}},
                "direction": {"type": "string", "enum": ["overstated", "understated", "timing_shift"]},
                "accounting_treatment": {"type": "string"},
                "rationale_evidence": {"type": "array", "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["quote", "source_accession_no", "location"],
                    "properties": {"quote": {"type": "string"},
                                   "source_accession_no": {"type": "string"},
                                   "location": {"type": "string"}}}},
            }}},
        "overall": {"type": "object", "additionalProperties": False,
                    "required": ["risk_tier", "top_signals"],
                    "properties": {"risk_tier": {"type": "string", "enum": ["elevated", "watch", "clear"]},
                                   "top_signals": {"type": "array", "items": {"type": "string"}}}},
    },
}


def freeze_state() -> dict:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_ROOT,
                           capture_output=True, text=True, check=True).stdout.strip()
    return {"head": head, "clean_tree": not dirty}


def run_case(client, case: dict, perturb: bool, out_dir: Path, log_path: Path) -> dict:
    payload = bp.build_payload(case, perturb=perturb)
    k = payload.pop("_k_internal")
    cik_part = f", CIK {case['cik']}" if not perturb else ""
    task = TASK.format(company_name=payload["case"]["company_name"],
                       ticker=payload["case"]["ticker"], cik_part=cik_part,
                       cutoff_date=case["cutoff_date"])
    t0 = time.monotonic()
    resp = client.messages.create(
        model=EVALUATEE_MODEL,
        max_tokens=16000,
        system=task,
        output_config={"format": {"type": "json_schema", "schema": MODEL_SCHEMA}},
        messages=[{"role": "user", "content": json.dumps(
            {k2: v for k2, v in payload.items() if not k2.startswith("_")},
            ensure_ascii=False)}],
    )
    wall = time.monotonic() - t0
    if resp.stop_reason == "refusal":
        raise RuntimeError(f"{case['case_id']}: evaluatee refusal — run log 확인")
    text = next(b.text for b in resp.content if b.type == "text")
    model_out = json.loads(text)
    # 파이프라인 메타 필드 채움 (llm_output v1.2 완성)
    accessions = {}
    for tag, vals in payload["financial_series_point_in_time"].items():
        for v in vals:
            if v.get("accession"):
                accessions[v["accession"]] = {"accession_no": v["accession"],
                                              "form_type": v.get("form") or "unknown",
                                              "filing_date": v["filed"]}
    full = {
        "case_id": case["case_id"],
        "run_id": f"{'perturbed' if perturb else 'original'}-{case['case_id']}-r1",
        "model": resp.model,
        "pipeline_version": freeze_state()["head"],
        "run_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "documents_used": sorted(accessions.values(), key=lambda d: d["accession_no"]),
        **model_out,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{case['case_id']}.json").write_text(
        json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": full["run_timestamp"], "case_id": case["case_id"],
            "variant": full["run_id"], "model_reported": resp.model,
            "request_id": getattr(resp, "_request_id", None),
            "stop_reason": resp.stop_reason,
            "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens,
            "wall_seconds": round(wall, 1), "freeze": freeze_state(),
            "perturb_factor": k if perturb else None,
        }, ensure_ascii=False) + "\n")
    return full


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=str(bp.EVALUATEE_CASES))
    ap.add_argument("--perturbed", action="store_true")
    ap.add_argument("--out", required=True, help="출력 디렉토리 (예: runs/main, pilot/runs)")
    ap.add_argument("--only", nargs="*", help="특정 case_id만")
    args = ap.parse_args()

    fs = freeze_state()
    if not fs["clean_tree"]:
        print("FAIL: 작업 트리가 깨끗하지 않음 — freeze-commit-then-run 위반", file=sys.stderr)
        return 1

    import anthropic  # 지연 import — CI에는 SDK가 없다
    client = anthropic.Anthropic()

    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))["cases"]
    if args.only:
        cases = [c for c in cases if c["case_id"] in set(args.only)]
    out_dir = REPO_ROOT / args.out
    log_path = REPO_ROOT / "logs" / "api_run_log.jsonl"
    for case in cases:
        full = run_case(client, case, args.perturbed, out_dir, log_path)
        print(f"{case['case_id']}: p={full['misstatement_probability']} "
              f"tier={full['overall']['risk_tier']} hyps={len(full['mechanism_hypotheses'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
