"""E4 교차모델 실행 하네스 (analysis/CROSSMODEL_PLAN.md, EXPLORATORY) — 18호출.

  .venv/bin/python tools/e4_runner.py            # dry-run: 로스터·완료 현황
  .venv/bin/python tools/e4_runner.py --execute  # 발사 (하네스, 개정 #4)
  .venv/bin/python tools/e4_runner.py --only case_71   # 케이스 경계 실행 (PLAN §4)

설계 (PLAN §2): 피평가자 시스템 프롬프트·스키마·격리 플래그 완전 동일 — 모델
ID만 claude-opus-4-8로 교체. 동결 runner.run_case를 그대로 사용하되 모듈 전역
EVALUATEE_MODEL을 실행 시점에 교체한다 (요청 모델·핀 검증·로그가 일관되게
opus-4-8; runner.py 파일 무수정 — §8-3 보존). 프레임 = 각 케이스의 원 채점과
동일 (전 18건 original — runs/holdout/scores·controls/scores·wave2/scores
run_id 'original-*-r1' 실측).

로스터 (PLAN §1 사전 고정, §4 순서 = 홀드아웃 → wave-2 → E1 대조군, 그룹 내
ticker 알파벳): 3 + 6 + 9 = 18. EXPLORATORY — 각주 전용, 헤드라인 금지.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))

import cli_client  # noqa: E402
import runner  # noqa: E402 (동결 — 파일 무수정, 전역 모델만 실행 시점 교체)

E4_MODEL = "claude-opus-4-8"  # PLAN §2 사전 등록 (fable-5/haiku 기각 사유 동봉)
OUT_DIR = REPO / "runs" / "e4" / "scores"

# (표시 순서, 케이스 파일, case_id) — PLAN §1/§4 사전 고정
ROSTER: list[tuple[str, str, str]] = [
    # 홀드아웃 3 (ticker 알파벳: GNE·HUBG·WMK)
    ("holdout", "data/evaluatee/cases_holdout.json", "case_73"),  # GNE
    ("holdout", "data/evaluatee/cases_holdout.json", "case_71"),  # HUBG
    ("holdout", "data/evaluatee/cases_holdout.json", "case_72"),  # WMK
    # wave-2 6 (ADAM·CGI·CSC·IOVA·MDXG·WFT)
    ("wave2", "data/evaluatee/cases_wave2.json", "case_44"),      # ADAM
    ("wave2", "data/evaluatee/cases_wave2.json", "case_61"),      # CGI
    ("wave2", "data/evaluatee/cases_wave2.json", "case_52"),      # CSC
    ("wave2", "data/evaluatee/cases_wave2.json", "case_49"),      # IOVA
    ("wave2", "data/evaluatee/cases_wave2.json", "case_60"),      # MDXG
    ("wave2", "data/evaluatee/cases_wave2.json", "case_65"),      # WFT
    # E1 대조군 9 (BCO·GO·GRDX·RXO·SFM·UTL·VIASP·VLGEA·XPO)
    ("e1_control", "data/evaluatee/cases_holdout_controls.json", "hc_05"),  # BCO
    ("e1_control", "data/evaluatee/cases_holdout_controls.json", "hc_07"),  # GO
    ("e1_control", "data/evaluatee/cases_holdout_controls.json", "hc_03"),  # GRDX
    ("e1_control", "data/evaluatee/cases_holdout_controls.json", "hc_04"),  # RXO
    ("e1_control", "data/evaluatee/cases_holdout_controls.json", "hc_08"),  # SFM
    ("e1_control", "data/evaluatee/cases_holdout_controls.json", "hc_02"),  # UTL
    ("e1_control", "data/evaluatee/cases_holdout_controls.json", "hc_01"),  # VIASP
    ("e1_control", "data/evaluatee/cases_holdout_controls.json", "hc_09"),  # VLGEA
    ("e1_control", "data/evaluatee/cases_holdout_controls.json", "hc_06"),  # XPO
]
BUDGET = len(ROSTER)  # 18 ≤ PLAN §5 cap ~20


class E4RunError(Exception):
    pass


def load_cases() -> list[tuple[str, dict]]:
    files: dict[str, dict] = {}
    out = []
    for grp, fpath, cid in ROSTER:
        if fpath not in files:
            files[fpath] = {c["case_id"]: c
                            for c in json.loads((REPO / fpath).read_text(
                                encoding="utf-8"))["cases"]}
        out.append((grp, files[fpath][cid]))
    return out


def done(case: dict) -> bool:
    return cli_client.output_is_valid(OUT_DIR / f"{case['case_id']}.json",
                                      runner.FULL_OUTPUT_SCHEMA)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--only", nargs="*", help="특정 case_id만 (케이스 경계 커밋용)")
    args = ap.parse_args()
    cases = load_cases()
    if args.only:
        cases = [(g, c) for g, c in cases if c["case_id"] in set(args.only)]
    todo = [(g, c) for g, c in cases if not done(c)]
    print(f"E4 로스터 {len(cases)} · 완료 {len(cases) - len(todo)} · 잔여 {len(todo)} "
          f"· model={E4_MODEL} · 프레임 original (원 채점 동일)")
    if not args.execute:
        print("dry-run — 발사는 --execute")
        return 0
    cli_client.assert_no_metered_credentials()
    cli_client.require_clean_tree()
    if len(todo) > BUDGET:
        raise E4RunError(f"지출 가드: 잔여 {len(todo)} > 예산 {BUDGET}")
    runner.EVALUATEE_MODEL = E4_MODEL  # 실행 시점 교체 — 요청 모델·핀 검증 일관
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = REPO / "logs" / f"run_e4_{ts}"
    failures = 0
    try:
        for grp, case in todo:
            res = runner.run_case(case, False, OUT_DIR, log_dir)
            print(f"[{grp}] {res['case_id']}: {res['status']}", flush=True)
            if res["status"].startswith("FAIL"):
                failures += 1
    except cli_client.RateLimitedError as e:
        print(f"E4 HALT (레이트 리밋, 멱등) — {e}", file=sys.stderr)
        print("재개: .venv/bin/python tools/e4_runner.py --execute")
        return 3
    print(f"E4 완료: FAIL {failures} · 다음: .venv/bin/python analysis/e4_crossmodel.py")
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
