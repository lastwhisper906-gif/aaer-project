"""B4 아카이브 단계 — FINRA Consolidated Short Interest 파일 수집 (D52 스펙 §1).

로스터의 각 케이스에서 필요한 결제일 창의 합집합을 ~/aaer-data/short_interest/에
원본 그대로 보관한다 (재개 가능 — 기존 파일 스킵, sha256은 checksums.log).
수집 후 매니페스트 재생성·커밋은 별도 단계:
  .venv/bin/python tools/verify_manifest.py --write

창 산술 (스펙 §3): t_last ≈ cutoff−14일, slope 4보고(~45일), trailing 중앙값 365일,
반월 여유 30일 → range = [cutoff − 454 − 30, cutoff], 하한은 DATA_FLOOR로 클램프.
cutoff < DATA_FLOOR + 14 인 케이스는 사용 가능 보고서가 존재할 수 없어 스킵 (기록).
"""
import datetime
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
sys.path.insert(0, str(REPO / "analysis" / "vendor"))
sys.path.insert(0, str(REPO / "pipeline"))

import short_interest as si_core  # noqa: E402
from b3_compute import load_rosters  # noqa: E402

UA = "chaeper lastwhisper906@gmail.com"  # fetch_primary_sources.py와 동일 규약
SI_DIR = Path.home() / "aaer-data" / "short_interest"
LOOKBACK_DAYS = 484  # 14(lag) + 45(slope 4보고) + 365(trailing) + 30(반월 여유) + 30(버퍼)


def needed_ranges() -> tuple[list[tuple[datetime.date, datetime.date]], list[str]]:
    ranges, skipped = [], []
    for tier, roster in load_rosters().items():
        for case in roster:
            cutoff = case["cutoff"]
            if cutoff < si_core.DATA_FLOOR + datetime.timedelta(days=si_core.LAG_DAYS):
                skipped.append(f"{tier}:{case['case_id']}({case['ticker']}) {cutoff}")
                continue
            start = max(cutoff - datetime.timedelta(days=LOOKBACK_DAYS),
                        si_core.DATA_FLOOR)
            ranges.append((start, cutoff))
    merged: list[tuple[datetime.date, datetime.date]] = []
    for s, e in sorted(ranges):
        if merged and s <= merged[-1][1] + datetime.timedelta(days=16):
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return merged, skipped


def main() -> int:
    merged, skipped = needed_ranges()
    print(f"skip (데이터 하한 이전 cutoff): {len(skipped)}건")
    total_found, total_missing = [], []
    for s, e in merged:
        print(f"range {s} .. {e}")
        r = si_core.download_range(s, e, SI_DIR, UA)
        total_found += r["found"]
        total_missing += r["missing_halfmonths"]
    print(f"archived: {len(set(total_found))} files → {SI_DIR}")
    if total_missing:
        print(f"MISSING half-months (조용한 스킵 아님, 기록): {total_missing}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
