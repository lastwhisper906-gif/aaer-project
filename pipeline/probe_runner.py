"""오염 프로브 러너 (freeze 개정 #2 — 구독 헤드리스 경로) — scoring/probes.md 설계의 실행부.

  python pipeline/probe_runner.py --recognition --cases <교란 대상 케이스 파일>
  python pipeline/probe_runner.py --verbatim   --cases <원본 케이스 파일>

출력: scoring/probe_results/{recognition,verbatim}/{case_id}.json + logs/run_<ts>/.
판정(일치 여부)은 채점 쪽 스크립트가 수행 — 이 러너는 모델 응답 수집만.
헤더 의무: these controls BOUND memorization risk; they do not eliminate it.
멱등: 출력 존재+스키마 통과 = skip. 레이트 리밋 = 재개 명령 출력 후 중단.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import json
import shlex
import sys
from pathlib import Path

import build_payload as bp
import cli_client
from runner import EVALUATEE_MODEL

REPO_ROOT = Path(__file__).resolve().parent.parent

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


def probe_case(kind: str, case: dict, out: Path, log_dir: Path) -> dict:
    cid = case["case_id"]
    out_path = out / f"{cid}.json"
    schema = RECOG_SCHEMA if kind == "recognition" else VERBATIM_SCHEMA
    if cli_client.output_is_valid(out_path, schema):
        return {"case_id": cid, "status": "skip (멱등)"}

    if kind == "recognition":
        payload = bp.build_payload(case, perturb=True)
        payload.pop("_k_internal")
        system, user = RECOG_TASK, json.dumps(payload, ensure_ascii=False)
        markers = cli_client.EVALUATEE_FORBIDDEN_MARKERS
    else:
        system = VERBATIM_TASK.format(company_name=case["company_name"],
                                      cutoff_date=case["cutoff_date"])
        user = "Answer now."
        markers = cli_client.EVALUATEE_FORBIDDEN_MARKERS

    r = cli_client.call_model(EVALUATEE_MODEL, system, user, schema,
                              log_dir=log_dir, log_name=f"probe_{kind}_{cid}",
                              forbid_markers=markers)
    if not r.ok:
        return {"case_id": cid, "status": f"FAIL ({r.fail_reason})"}
    out.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(r.structured, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    if kind == "recognition":
        return {"case_id": cid, "status": f"OK guess={r.structured['company_guess']!r} "
                f"({r.structured['confidence']})"}
    return {"case_id": cid, "status": f"OK known={r.structured['known']} "
            f"rev={r.structured['revenue']}"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--recognition", action="store_true")
    ap.add_argument("--verbatim", action="store_true")
    ap.add_argument("--cases", default=str(bp.EVALUATEE_CASES))
    ap.add_argument("--concurrency", type=int, default=3,
                    help="RP-09 3d: 대조군 16-24건 확장 대비 — runner.py와 동일 패턴")
    ap.add_argument("--out-root", default=str(REPO_ROOT / "scoring" / "probe_results"),
                    help="RP-09 3b: v2 대조군 프로브는 별도 루트 (I3 — 기존 "
                         "probe_results 동결 경로에 추가 기입 금지)")
    args = ap.parse_args()

    cli_client.assert_no_metered_credentials()
    cli_client.require_clean_tree()

    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))["cases"]
    out_root = Path(args.out_root)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = REPO_ROOT / "logs" / f"run_{ts}"
    resume_cmd = "python pipeline/probe_runner.py " + " ".join(
        shlex.quote(a) for a in sys.argv[1:])

    kinds = [k for k, on in (("recognition", args.recognition),
                             ("verbatim", args.verbatim)) if on]
    failures = 0
    try:
        for kind in kinds:
            out = out_root / kind
            # RP-09 3d: 병렬화 (runner.py와 동일 ThreadPool 패턴 — 호출 격리는
            # cli_client가 호출 단위로 보장, 케이스 간 상태 공유 없음)
            with concurrent.futures.ThreadPoolExecutor(
                    max_workers=args.concurrency) as pool:
                futs = {pool.submit(probe_case, kind, case, out, log_dir): case
                        for case in cases}
                for fut in concurrent.futures.as_completed(futs):
                    res = fut.result()
                    if res["status"].startswith("FAIL"):
                        failures += 1
                    print(f"[{kind}] {res['case_id']}: {res['status']}", flush=True)
    except cli_client.RateLimitedError as e:
        print(f"\nHALT — {e}", file=sys.stderr)
        print(f"재개 명령 (완료분 자동 skip):\n  {resume_cmd}")
        return 3
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
