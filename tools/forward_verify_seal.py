"""봉인 후 무결성 재검증 (spec §9, D100).

usage: python tools/forward_verify_seal.py --cycle forward/cycle_001

MANIFEST.sha256 대비 현재 파일 해시를 전건 재계산 — 불일치·누락·추가를
보고하고 외부 검증 절차를 안내한다. 네트워크 0.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_common import REPO, manifest_text, sha256_text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True)
    args = ap.parse_args()
    cycle = REPO / args.cycle
    manifest = cycle / "MANIFEST.sha256"
    if not manifest.exists():
        print("FAIL — MANIFEST.sha256 부재 (미봉인 사이클)")
        return 1

    recorded = manifest.read_text(encoding="utf-8")
    current = manifest_text(cycle)
    if recorded != current:
        rec = dict(line.split("  ", 1)[::-1] for line in recorded.splitlines() if "  " in line)
        cur = dict(line.split("  ", 1)[::-1] for line in current.splitlines() if "  " in line)
        print("FAIL — 봉인 무결성 위반:")
        for name in sorted(set(rec) | set(cur)):
            if name not in cur:
                print(f"  삭제됨: {name}")
            elif name not in rec:
                print(f"  봉인 후 추가됨: {name}")
            elif rec[name] != cur[name]:
                print(f"  변조됨: {name}")
        return 1

    print(f"PASS — 봉인 무결성 (manifest sha256 {sha256_text(recorded)})")
    ots = manifest.with_suffix(".sha256.ots")
    print("외부 검증: SEAL_RECORD.md §외부 검증 방법 — GitHub tag API 서버 시각 + "
          + (f"`ots verify {ots}`" if ots.exists()
             else "OTS 앵커 pending (ots stamp 후 커밋 필요)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
