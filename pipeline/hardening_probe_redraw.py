"""RP-06 A1 — 인지 프로브 재추첨 (frozen 프로토콜 무수정 재사용, 출력 경로만 분리).

소유자 지시 addendum(RP-06, decisions_log 2026-07-06)의 A1 실행부. 이 모듈은
`probe_runner.probe_case`를 그대로 호출한다 — 프로브 문언·스키마·페이로드 생성
(교란 변형, probes.md ①)·격리 구성(J13-c) 전부 frozen 코드 소관이며 여기서
아무것도 재정의하지 않는다. 유일한 차이는 출력 디렉토리: 기존
scoring/probe_results/recognition/ (읽기 전용 — draw 1)이 아니라
runs/hardening/probe_recognition/ (draw 2)에 쓴다.

  python pipeline/hardening_probe_redraw.py

멱등: 출력 존재+스키마 통과 = skip. 레이트 리밋 = 재개 명령 출력 후 중단.
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import cli_client
from probe_runner import probe_case

REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_FILE = REPO_ROOT / "scoring" / "perturbed_cases.json"
OUT_DIR = REPO_ROOT / "runs" / "hardening" / "probe_recognition"


def main() -> int:
    cli_client.assert_no_metered_credentials()
    cli_client.require_clean_tree()

    cases = json.loads(CASES_FILE.read_text(encoding="utf-8"))["cases"]
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = REPO_ROOT / "logs" / f"run_{ts}"

    failures = 0
    try:
        for case in cases:  # 순차 — frozen probe_runner와 동일 (8건, 동시성 불요)
            res = probe_case("recognition", case, OUT_DIR, log_dir)
            if res["status"].startswith("FAIL"):
                failures += 1
            print(f"[recognition redraw] {res['case_id']}: {res['status']}", flush=True)
    except cli_client.RateLimitedError as e:
        print(f"\nHALT — {e}", file=sys.stderr)
        print("재개 명령 (완료분 자동 skip):\n  python pipeline/hardening_probe_redraw.py")
        return 3
    print(f"완료: {len(cases)}건 중 FAIL {failures}건 (로그: {log_dir})")
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
