"""3-arm 정체 실험 — arm (b) 가공 사명 러너 (IDENTITY_3ARM_PLAN §3, D36).

arm (a) 익명 = 동결 runs/wave2/perturbed (재실행 없음)
arm (b) 가공 사명 = 본 러너 — 동결 build_payload(perturb=True) 페이로드에
        data/evaluatee/fict_names_wave2.json의 가공 사명·티커만 중첩 (그 외 동일:
        동일 k 재스케일·동일 시계열·동일 연대기·동일 TASK/스키마/가드)
arm (c) 실명 = 동결 runs/wave2/scores (재실행 없음)

신규 호출은 (b)의 9건뿐. 출력 runs/wave2/identity_arm_b/{case_id}.json —
runner.run_case와 동일 출력 형식. 멱등 (기존 유효 출력 skip).
동결 pipeline/ 모듈 무수정 — import 재사용만.
"""
import datetime
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
import build_payload as bp  # noqa: E402
import cli_client  # noqa: E402
from cli_client import EVALUATEE_FORBIDDEN_MARKERS, freeze_state  # noqa: E402
from runner import EVALUATEE_MODEL, FULL_OUTPUT_SCHEMA, MODEL_SCHEMA, TASK  # noqa: E402

FICT = json.loads((REPO / "data/evaluatee/fict_names_wave2.json").read_text())["names"]
CASES = {c["case_id"]: c for c in json.loads(
    (REPO / "data/evaluatee/cases_wave2.json").read_text())["cases"]}
FRAUD_IDS = json.loads((REPO / "runs/wave2/fraud_case_ids.json").read_text())
OUT_DIR = REPO / "runs/wave2/identity_arm_b"


def run_arm_b(cid: str, log_dir: Path) -> dict:
    out_path = OUT_DIR / f"{cid}.json"
    if cli_client.output_is_valid(out_path, FULL_OUTPUT_SCHEMA):
        return {"case_id": cid, "status": "skip (멱등)"}
    case = CASES[cid]
    payload = bp.build_payload(case, perturb=True)  # 동결 함수 — k·시계열 동일
    k = payload.pop("_k_internal")
    fict = FICT[cid]
    payload["case"]["company_name"] = fict["company_name"]  # 정체 토큰만 중첩
    payload["case"]["ticker"] = fict["ticker"]
    task = TASK.format(company_name=fict["company_name"], ticker=fict["ticker"],
                       cik_part="", cutoff_date=case["cutoff_date"])
    user_payload = json.dumps({k2: v for k2, v in payload.items()
                               if not k2.startswith("_")}, ensure_ascii=False)
    r = cli_client.call_model(
        EVALUATEE_MODEL, task, user_payload, MODEL_SCHEMA,
        log_dir=log_dir, log_name=f"evaluatee_armb_{cid}",
        forbid_markers=EVALUATEE_FORBIDDEN_MARKERS)
    meta = {"case_id": cid, "variant": f"armb-{cid}-r1", "perturb_factor": k,
            "fict_name": fict["company_name"], "fail_reason": r.fail_reason,
            "served_models": r.served_models}
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / f"runmeta_armb_{cid}.json").write_text(
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
    full = {"case_id": cid, "run_id": f"armb-{cid}-r1",
            "model": (r.served_models or [EVALUATEE_MODEL])[0],
            "pipeline_version": freeze_state()["head"],
            "run_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "documents_used": sorted(accessions.values(), key=lambda d: d["accession_no"]),
            **r.structured}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(full, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"case_id": cid,
            "status": f"OK p={full['misstatement_probability']} tier={full['overall']['risk_tier']}"}


def main() -> int:
    cli_client.assert_no_metered_credentials()
    cli_client.require_clean_tree()
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = REPO / "logs" / f"run_{ts}"
    only = sys.argv[1:] or sorted(FRAUD_IDS)
    failures = 0
    for cid in only:
        res = run_arm_b(cid, log_dir)
        print(f"{res['case_id']}: {res['status']}", flush=True)
        if res["status"].startswith("FAIL"):
            failures += 1
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
