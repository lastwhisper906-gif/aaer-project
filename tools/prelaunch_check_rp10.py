"""RP-10 Phase 0.5: 발사 전 불변량 검사 — 전 항목 PASS 아니면 abort (exit 1).

호출 없음. stage-data + build-inputs를 선실행(멱등)한 뒤 22개 대조군 페이로드를
실제 빌더로 구성해 검사한다:
  BLINDNESS — case 필드 = evaluatee_input 계약 화이트리스트만 · guard_payload
    (정답 어휘·카나리) 통과 · 페이로드 직렬화에 AAER/answer/treatment/control
    라벨 문자열 부재
  CUTOFF — financial_series 전 사실 filed ≤ cutoff · chronology 전 항목 ≤ cutoff
  IMMUTABILITY — 동결 경로 diff (f3b76f7..HEAD) 0줄 · verify_manifest PASS ·
    pytest 전체 PASS (호출자가 별도 실행 — 본 스크립트는 diff만)
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(REPO / "pipeline"))

import run_control_v2_scoring as rb  # noqa: E402
import build_payload as bp  # noqa: E402
import cli_client  # noqa: E402

WHITELIST = {"case_id", "ticker", "cik", "company_name", "cutoff_date"}
# 부분문자열 오탐 주의: 'control'은 NoncontrollingInterest 태그에 걸림 — 라벨
# 누출은 guard_payload(정답 어휘)와 아래 명시 키로만 검사
FORBIDDEN_STRINGS = ("aaer", "answer_key", "\"group\"", "scheme_", "fraud")
FROZEN = ["runs/main", "runs/perturbed", "runs/hardening", "scoring/grades",
          "pilot/grades", "scoring/probe_results",
          "review_packets/RP-05_results.md", "review_packets/RP-06_hardening.md",
          "scoring/rp05_stats.json", "scoring/rp06_hardening_stats.json"]


def main() -> int:
    fails = []
    rows = rb.selected_controls()
    print(f"[0] stage-data + build-inputs ({len(rows)} controls, 멱등)")
    rb.stage_data(rows)
    rb.build_inputs(rows)

    cases = json.loads(rb.CASES_V2_DEST.read_text(encoding="utf-8"))["cases"]
    assert len(cases) == len(rows)
    for case in cases:
        cid = case["case_id"]
        if set(case) != WHITELIST:
            fails.append(f"{cid}: case 필드 위반 {set(case) ^ WHITELIST}")
        payload = bp.build_payload(case, perturb=False)
        payload.pop("_k_internal")
        js = json.dumps(payload, ensure_ascii=False)
        # BLINDNESS: guard (정답 어휘·카나리)
        try:
            cli_client.guard_payload(js, cli_client.EVALUATEE_FORBIDDEN_MARKERS)
        except Exception as e:  # noqa: BLE001
            fails.append(f"{cid}: guard_payload FAIL {e}")
        low = js.lower()
        for s in FORBIDDEN_STRINGS:
            if s in low:
                fails.append(f"{cid}: 금지 문자열 '{s}' 페이로드 출현")
        # CUTOFF
        cut = case["cutoff_date"]
        for tag, vals in payload["financial_series_point_in_time"].items():
            for v in vals:
                if v["filed"] > cut:
                    fails.append(f"{cid}: {tag} filed {v['filed']} > cutoff {cut}")
        for r in payload["filing_chronology"]:
            if r["filing_date"] > cut:
                fails.append(f"{cid}: chronology {r['filing_date']} > cutoff {cut}")
        n_facts = sum(len(v) for v in payload["financial_series_point_in_time"].values())
        print(f"  {cid} {case['ticker']:5s} facts={n_facts} chron={len(payload['filing_chronology'])} OK")

    # IMMUTABILITY
    d = subprocess.run(["git", "diff", "f3b76f7..HEAD", "--"] + FROZEN,
                       capture_output=True, text=True, cwd=REPO)
    if d.stdout.strip():
        fails.append("동결 경로 diff 비공백 (f3b76f7..HEAD)")

    if fails:
        print("\nABORT — 검사 실패:")
        for f in fails:
            print("  FAIL", f)
        return 1
    print(f"\nPASS — BLINDNESS/CUTOFF ({len(cases)} payloads) + IMMUTABILITY diff 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
