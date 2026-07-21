"""피평가자 러너 (freeze 개정 #2 — 구독 헤드리스 경로) — 케이스별 독립 호출, 페이로드 규약 강제.

사용:
  python pipeline/runner.py --cases data/evaluatee/cases.json --out runs/main
  python pipeline/runner.py --cases scoring/perturbed_cases.json --perturbed --out runs/perturbed
  python pipeline/runner.py --cases pilot/cases_pilot.json --out pilot/runs

규약 (GP-6 3조항 + V4/V7 + 개정 #2):
  - 호출당 컨텍스트 = 시스템 프롬프트(TASK) + 페이로드 JSON 하나. 저장소 문서·
    다른 케이스·채점 자료 일절 미포함 — cli_client가 격리 임시 디렉토리에서
    `claude -p` (도구 차단, CLAUDE_CONFIG_DIR 격리)로 강제.
  - 이 모듈은 scoring/ 를 import하지 않는다 (정적 스캔).
  - 멱등: legacy 유효 출력 또는 현재 실행 fingerprint와 일치하는 출력만 skip.
  - 실행 순서 = 케이스 파일의 셔플된 중립 ID 순서 고정, 동시성 3.
  - 2연속 실패 = 해당 케이스 FAIL 기록 후 계속. 레이트 리밋 = 재개 명령 출력 후 중단.
  - 모델 핀: 피평가자 = claude-sonnet-5 (D6) — 폴백 없음. 서빙 모델 핀 불일치 = FAIL.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import hashlib
import json
import shlex
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import build_payload as bp
import cli_client
import jsonschema
from cli_client import EVALUATEE_FORBIDDEN_MARKERS, freeze_state

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALUATEE_MODEL = "claude-sonnet-5"  # D6 pin (사유는 채점 쪽 문서)
FULL_OUTPUT_SCHEMA = json.loads(
    (REPO_ROOT / "schemas" / "llm_output.json").read_text(encoding="utf-8"))
CANARY_MARKERS = ("9fa11f98", "a2d69cfe")
_HARNESS_VERSION: str | None = None


def get_harness_version() -> str:
    """Return the CLI version once per runner process."""
    global _HARNESS_VERSION
    if _HARNESS_VERSION is None:
        try:
            result = subprocess.run(
                ["claude", "--version"], capture_output=True, text=True, check=True)
            _HARNESS_VERSION = result.stdout.splitlines()[0] if result.stdout else "UNAVAILABLE"
        except (FileNotFoundError, OSError):
            _HARNESS_VERSION = "UNAVAILABLE"
    return _HARNESS_VERSION


def compute_fingerprint(case: dict, task: str, user_payload: str) -> dict:
    """Compute the complete configuration identity before a model call."""
    schema_bytes = (REPO_ROOT / "schemas" / "llm_output.json").read_bytes()
    case_json = json.dumps(case, sort_keys=True, ensure_ascii=False)
    return {
        "case_input_sha256": hashlib.sha256(case_json.encode("utf-8")).hexdigest(),
        "payload_sha256": hashlib.sha256(user_payload.encode("utf-8")).hexdigest(),
        "system_prompt_sha256": hashlib.sha256(task.encode("utf-8")).hexdigest(),
        "schema_sha256": hashlib.sha256(schema_bytes).hexdigest(),
        "model_requested": EVALUATEE_MODEL,
        "harness_version_actual": get_harness_version(),
        "pipeline_commit": freeze_state()["head"],
    }


def derive_model_schema(full_schema: dict) -> dict:
    """Return the canonical model subset as a standalone Draft 7 schema."""
    model_schema = deepcopy(full_schema["$defs"]["model_output"])
    model_schema["$schema"] = full_schema["$schema"]
    return model_schema


MODEL_SCHEMA = derive_model_schema(FULL_OUTPUT_SCHEMA)

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

def run_case(case: dict, perturb: bool, out_dir: Path, log_dir: Path) -> dict:
    """케이스 1건 실행 — 반환: 상태 요약 dict (FAIL 포함, 예외는 레이트 리밋만)."""
    cid = case["case_id"]
    out_path = out_dir / f"{cid}.json"
    existing = None
    if out_path.exists():
        try:
            existing = json.loads(out_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
        if (cli_client.output_is_valid(out_path, FULL_OUTPUT_SCHEMA)
                and isinstance(existing, dict) and "fingerprint" not in existing):
            return {"case_id": cid,
                    "status": "skip (legacy output — fingerprint 없음, 재실행 안 함)"}

    payload = bp.build_payload(case, perturb=perturb)
    k = payload.pop("_k_internal")
    cik_part = f", CIK {case['cik']}" if not perturb else ""
    task = TASK.format(company_name=payload["case"]["company_name"],
                       ticker=payload["case"]["ticker"], cik_part=cik_part,
                       cutoff_date=case["cutoff_date"])
    user_payload = json.dumps({k2: v for k2, v in payload.items() if not k2.startswith("_")},
                              ensure_ascii=False)
    fingerprint = compute_fingerprint(case, task, user_payload)
    write_path = out_path
    stale_superseding = False
    if out_path.exists():
        if isinstance(existing, dict) and existing.get("fingerprint") == fingerprint:
            return {"case_id": cid, "status": "skip (멱등 — fingerprint 일치)"}
        canonical = json.dumps(fingerprint, sort_keys=True, ensure_ascii=False)
        suffix = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:8]
        write_path = out_dir / f"{cid}.fp-{suffix}.json"
        stale_superseding = True

    variant = "perturbed" if perturb else "original"
    r = cli_client.call_model(
        EVALUATEE_MODEL, task, user_payload, MODEL_SCHEMA,
        log_dir=log_dir, log_name=f"evaluatee_{variant}_{cid}",
        forbid_markers=EVALUATEE_FORBIDDEN_MARKERS)

    canary_hit = any(m in json.dumps(r.structured or {}).lower() for m in CANARY_MARKERS)
    meta = {"case_id": cid, "variant": f"{variant}-{cid}-r1",
            "perturb_factor": k if perturb else None, "canary_hit": canary_hit,
            "fail_reason": r.fail_reason, "served_models": r.served_models}
    (log_dir / f"runmeta_{variant}_{cid}.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    if not r.ok:
        return {"case_id": cid, "status": f"FAIL ({r.fail_reason})"}

    accessions = {}
    for tag, vals in payload["financial_series_point_in_time"].items():
        for v in vals:
            if v.get("accession"):
                accessions[v["accession"]] = {"accession_no": v["accession"],
                                              "form_type": v.get("form") or "unknown",
                                              "filing_date": v["filed"]}
    full = {
        "case_id": cid,
        "run_id": f"{variant}-{cid}-r1",
        "model": (r.served_models or [EVALUATEE_MODEL])[0],
        "pipeline_version": freeze_state()["head"],
        "run_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "documents_used": sorted(accessions.values(), key=lambda d: d["accession_no"]),
        "fingerprint": fingerprint,
        **r.structured,
    }
    errors = list(jsonschema.Draft7Validator(FULL_OUTPUT_SCHEMA).iter_errors(full))
    if errors:
        path = ".".join(str(part) for part in errors[0].absolute_path) or "<root>"
        reason = f"schema_violation: {path}"
        meta["fail_reason"] = reason
        log_dir.mkdir(parents=True, exist_ok=True)
        (log_dir / f"runmeta_{variant}_{cid}.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"case_id": cid, "status": f"FAIL ({reason})"}
    out_dir.mkdir(parents=True, exist_ok=True)
    write_path.write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")
    status_prefix = "OK stale-superseding" if stale_superseding else "OK"
    return {"case_id": cid, "status": f"{status_prefix} p={full['misstatement_probability']} "
            f"tier={full['overall']['risk_tier']} hyps={len(full['mechanism_hypotheses'])}"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=str(bp.EVALUATEE_CASES))
    ap.add_argument("--perturbed", action="store_true")
    ap.add_argument("--out", required=True, help="출력 디렉토리 (예: runs/main, pilot/runs)")
    ap.add_argument("--only", nargs="*", help="특정 case_id만")
    ap.add_argument("--concurrency", type=int, default=3)
    args = ap.parse_args()

    cli_client.assert_no_metered_credentials()
    cli_client.require_clean_tree()

    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))["cases"]
    if args.only:
        cases = [c for c in cases if c["case_id"] in set(args.only)]
    out_dir = REPO_ROOT / args.out
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = REPO_ROOT / "logs" / f"run_{ts}"

    resume_cmd = "python pipeline/runner.py " + " ".join(
        shlex.quote(a) for a in sys.argv[1:])
    failures = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futs = {pool.submit(run_case, c, args.perturbed, out_dir, log_dir): c
                for c in cases}  # 제출 순서 = 케이스 파일의 셔플된 중립 ID 순서 (고정)
        try:
            for fut in concurrent.futures.as_completed(futs):
                res = fut.result()
                if res["status"].startswith("FAIL"):
                    failures += 1
                print(f"{res['case_id']}: {res['status']}", flush=True)
        except cli_client.RateLimitedError as e:
            pool.shutdown(cancel_futures=True)
            print(f"\nHALT — {e}", file=sys.stderr)
            print(f"재개 명령 (완료분 자동 skip):\n  {resume_cmd}")
            return 3
    print(f"완료: {len(cases)}건 중 FAIL {failures}건 (로그: {log_dir})")
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
