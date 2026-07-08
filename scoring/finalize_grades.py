"""finalize_grades.py — 채점 인간 최종 확정 도구 (§7 human-signs-last, 감사 D3/B1).

**이 도구는 Claude가 실행하지 않는다.** 소유자가 RP-13 워크벤치를 검토한 뒤
직접 실행한다. 안전 장치:
  1. 기본 = dry-run (무엇이 확정될지 목록만 출력, 아무것도 안 바꿈).
  2. --commit 은 게이트 토큰이 있어야 동작: scoring/overrides.md 에
     'RP-13-FINALIZE: YES' 줄 (소유자가 검토 완료 서명으로 추가).
  3. per-case 오버라이드(제안 처분 뒤집기)는 overrides.md 에 케이스ID·사유 수기 기록
     — 이 도구는 batch finalize이며 예외는 소유자가 overrides.md 로 명시한다.

대상(대기 57): scoring/grades_wave2(32) + grades_holdout(3) + grades_v2/controls(22).
동작: 각 grade 파일 _meta.human_finalized = true 로 설정(원자적 rewrite, verbatim 보존).
확정은 새 커밋으로 남고, 그 커밋이 채점의 인간 서명 증적이 된다(§7 불변조항 3).
"""
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GATE = "RP-13-FINALIZE: YES"
OVERRIDES = REPO / "scoring/overrides.md"
DIRS = ["scoring/grades_wave2", "scoring/grades_holdout", "scoring/grades_v2/controls"]


def gate_present() -> bool:
    return OVERRIDES.is_file() and GATE in OVERRIDES.read_text(encoding="utf-8")


def pending():
    out = []
    for d in DIRS:
        for p in sorted(glob.glob(str(REPO / d / "*.json"))):
            j = json.loads(Path(p).read_text(encoding="utf-8"))
            if not (j.get("_meta") or {}).get("human_finalized", False):
                out.append((d, Path(p)))
    return out


def main(commit: bool) -> int:
    pend = pending()
    by_dir = {}
    for d, _ in pend:
        by_dir[d] = by_dir.get(d, 0) + 1
    print(f"대기(human_finalized=false) {len(pend)}건:")
    for d, n in by_dir.items():
        print(f"  {d}: {n}")
    if not commit:
        print("\n[dry-run] 확정하려면: (1) RP-13 워크벤치 검토 → (2) overrides.md 에 "
              f"'{GATE}' 추가(서명) → (3) 이 도구 --commit.")
        return 0
    if not gate_present():
        print(f"\n거부 — 게이트 부재. scoring/overrides.md 에 '{GATE}' 줄이 없다. "
              "소유자 검토 서명 후 재실행. (Claude는 이 토큰을 대신 추가하지 않는다.)")
        return 2
    for d, p in pend:
        j = json.loads(p.read_text(encoding="utf-8"))
        j.setdefault("_meta", {})["human_finalized"] = True
        p.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n확정 완료: {len(pend)}건 human_finalized=true. 이 변경을 커밋해 서명 증적으로 남길 것 "
          "(per-case override는 overrides.md 에 별도 기록).")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", action="store_true", help="게이트 있을 때만 실제 확정 (없으면 dry-run)")
    raise SystemExit(main(ap.parse_args().commit))
