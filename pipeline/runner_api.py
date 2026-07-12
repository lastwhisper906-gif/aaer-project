"""피평가자 러너 — raw API 병렬 변형 (freeze 개정 #3 스캐폴드, D38 — 미배선).

동결 `runner.py`와의 차이는 호출 클라이언트뿐 (api_client.call_model_api).
TASK·MODEL_SCHEMA·build_payload·출력 형식·멱등 skip 전부 동결 모듈 import.
실행은 개정 #3 발효 후에만 (api_client의 이중 안전장치가 차단).

사용 (발효 후):
  AAER_RAW_API_APPROVED=1 python pipeline/runner_api.py --cases <cases.json> --out <dir> \
      [--perturbed] [--only case_NN ...] [--temperature 0]
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

import build_payload as bp
import cli_client
from api_client import assert_raw_api_approved, call_model_api
from cli_client import EVALUATEE_FORBIDDEN_MARKERS, freeze_state
from runner import EVALUATEE_MODEL, FULL_OUTPUT_SCHEMA, MODEL_SCHEMA, TASK

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_case_api(case: dict, perturb: bool, out_dir: Path, log_dir: Path,
                 temperature: float | None) -> dict:
    cid = case["case_id"]
    out_path = out_dir / f"{cid}.json"
    if cli_client.output_is_valid(out_path, FULL_OUTPUT_SCHEMA):
        return {"case_id": cid, "status": "skip (멱등)"}
    payload = bp.build_payload(case, perturb=perturb)
    k = payload.pop("_k_internal")
    cik_part = f", CIK {case['cik']}" if not perturb else ""
    task = TASK.format(company_name=payload["case"]["company_name"],
                       ticker=payload["case"]["ticker"], cik_part=cik_part,
                       cutoff_date=case["cutoff_date"])
    user_payload = json.dumps({k2: v for k2, v in payload.items()
                               if not k2.startswith("_")}, ensure_ascii=False)
    variant = "perturbed" if perturb else "original"
    r = call_model_api(EVALUATEE_MODEL, task, user_payload, MODEL_SCHEMA,
                       log_dir=log_dir, log_name=f"evaluatee_api_{variant}_{cid}",
                       forbid_markers=EVALUATEE_FORBIDDEN_MARKERS,
                       temperature=temperature)
    if not r.ok:
        return {"case_id": cid, "status": f"FAIL ({r.fail_reason})"}
    accessions = {}
    for tag, vals in payload["financial_series_point_in_time"].items():
        for v in vals:
            if v.get("accession"):
                accessions[v["accession"]] = {"accession_no": v["accession"],
                                              "form_type": v.get("form") or "unknown",
                                              "filing_date": v["filed"]}
    full = {"case_id": cid, "run_id": f"api-{variant}-{cid}-r1",
            "model": (r.served_models or [EVALUATEE_MODEL])[0],
            "pipeline_version": freeze_state()["head"],
            "run_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "documents_used": sorted(accessions.values(), key=lambda d: d["accession_no"]),
            **r.structured}
    out_dir.mkdir(parents=True, exist_ok=True)
    # 원자적 기록 (D67): 크래시 시 부분 파일이 '완료'로 오인되지 않도록 tmp→replace
    tmp = out_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(out_path)
    return {"case_id": cid,
            "status": f"OK p={full['misstatement_probability']} (perturb_k={k if perturb else None})"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--perturbed", action="store_true")
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--temperature", type=float, default=None)
    args = ap.parse_args()

    assert_raw_api_approved()      # 소유자 스위치 + 키 (개정 #3 발효 전 즉시 예외)
    cli_client.require_clean_tree()

    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))["cases"]
    if args.only:
        cases = [c for c in cases if c["case_id"] in set(args.only)]
    out_dir = REPO_ROOT / args.out
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = REPO_ROOT / "logs" / f"run_{ts}"
    failures = 0
    try:
        for c in cases:  # 순차 — 동치성 테스트 규모(소수 케이스)에 충분
            res = run_case_api(c, args.perturbed, out_dir, log_dir, args.temperature)
            print(f"{res['case_id']}: {res['status']}", flush=True)
            if res["status"].startswith("FAIL"):
                failures += 1
    except cli_client.RateLimitedError as e:
        print(f"HALT — {e} (재개 = 동일 명령, 멱등)", file=sys.stderr)
        return 3
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
