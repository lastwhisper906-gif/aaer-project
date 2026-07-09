"""RP-13 확정 적용기 (P7) — 서명된 워크벤치를 grade 파일에 반영한다.

입력 (둘 중 하나):
  (a) 소유자가 체크한 review_packets/RP-13_grading_workbench.md
      — `☑ finalize` 또는 `☑ override (사유: <텍스트> → overrides.md)`
      (☑ 외에 ✓, [x] 표기도 인정. 미체크 케이스는 건너뛰고 --partial 없이는 실패.)
  (b) --decisions <json>: [{"case":"case_39","action":"finalize"|"override",
      "reason":"...","fields":{"dim2_mechanism":2}}, ...]

동작:
  - 각 케이스 grade 파일의 `_meta.human_finalized = true` 설정
    (+ `_meta.finalized_date`, `_meta.finalized_via`).
  - override: fields를 grade에 적용하고 scoring/overrides.md에 OV-NNN 블록 추가
    (기록 형식 §7 — 대상/Claude 1차/오버라이드/사유/사후 확인).
  - 멱등: 이미 true인 파일은 건너뛴다. 미지의 case id는 거부.
  - --also <dir>: 추가 grade 디렉터리 일괄 확정 (예: scoring/grades_v2/controls,
    RP-09/RP-10 검토 패킷 기반 — decisions_log 항목과 함께 사용).

주의: 이 스크립트 실행 전 워크벤치를 재생성하지 말 것 —
tools/build_rp13_workbench.py 는 무조건 덮어써 체크 표시를 파괴한다.

사용:  python tools/apply_rp13_finalization.py [--workbench <md>] [--decisions <json>]
       [--also scoring/grades_v2/controls] [--partial] [--dry-run] [--date YYYY-MM-DD]
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORKBENCH = REPO / "review_packets/RP-13_grading_workbench.md"
OVERRIDES = REPO / "scoring/overrides.md"
GRADE_DIRS = ["scoring/grades_wave2", "scoring/grades_holdout"]  # RP-13 대상 35건

CASE_HDR = re.compile(r"^### (case_\d+) = (.+?) \((\S+), (\S+)\) — (\S+)")
TICK = r"(?:☑|✓|\[x\]|\[X\])"
SIG_FINAL = re.compile(rf"^\- \*\*서명\*\*:\s*{TICK}\s*finalize", re.M)
SIG_OVER = re.compile(rf"{TICK}\s*override\s*\(사유:\s*(.*?)\s*→\s*overrides\.md\)")
UNTICKED = re.compile(r"^\- \*\*서명\*\*:\s*☐\s*finalize\s+☐\s*override")


def grade_path(case):
    for d in GRADE_DIRS:
        p = REPO / d / f"{case}.json"
        if p.exists():
            return p
    return None


def parse_workbench(path):
    """서명된 워크벤치 → [{case, action, reason}] (미체크는 action=None)."""
    text = Path(path).read_text(encoding="utf-8")
    decisions, case = [], None
    for block in text.split("\n### ")[1:]:
        block = "### " + block
        m = CASE_HDR.match(block)
        if not m:
            continue
        case = m.group(1)
        sig = next((ln for ln in block.splitlines() if ln.startswith("- **서명**")), "")
        if SIG_FINAL.search(sig):
            decisions.append(dict(case=case, action="finalize", reason=None, fields=None))
        elif SIG_OVER.search(sig):
            reason = SIG_OVER.search(sig).group(1)
            if not reason or set(reason) <= {"_", " "}:
                sys.exit(f"[FAIL] {case}: override 체크됐으나 사유가 비어 있음 — 사유 필수")
            decisions.append(dict(case=case, action="override", reason=reason, fields=None))
        else:
            decisions.append(dict(case=case, action=None, reason=None, fields=None))
    return decisions


def next_ov_number():
    nums = [int(m.group(1)) for m in
            re.finditer(r"^## OV-(\d+) —", OVERRIDES.read_text(encoding="utf-8"), re.M)]
    return max(nums, default=0) + 1


def append_override(case, grade, reason, fields, date, dry):
    n = next_ov_number()
    first_claude = ", ".join(
        f"{k}={grade.get(k)}" for k in
        ("dim1_probability_band", "dim2_mechanism", "dim4_evidence_quality"))
    changed = ", ".join(f"{k}: {grade.get(k)} → {v}" for k, v in (fields or {}).items()) \
        or "(필드 변경 없음 — 판단 기록만)"
    block = (
        f"\n## OV-{n:03d} — {date}\n"
        f"- 대상: `{grade_path(case).relative_to(REPO)}` / {case}\n"
        f"- Claude 1차: {first_claude} · rationale 발췌: "
        f"{' '.join(grade.get('rationale', '').split())[:200]}…\n"
        f"- 오버라이드: {changed}\n"
        f"- 사유: {reason}\n"
        f"- 사후 확인: (Week 3+ 기입) 옳았던 쪽 = 미확정\n")
    if not dry:
        with open(OVERRIDES, "a", encoding="utf-8") as f:
            f.write(block)
    return f"OV-{n:03d}"


def finalize_file(path, date, via, fields, dry):
    g = json.loads(path.read_text(encoding="utf-8"))
    meta = g.setdefault("_meta", {})
    if meta.get("human_finalized") is True:
        return g, "skip(already)"
    for k, v in (fields or {}).items():
        if k not in g:
            sys.exit(f"[FAIL] {path.name}: 미지 필드 {k}")
        g[k] = v
    meta["human_finalized"] = True
    meta["finalized_date"] = date
    meta["finalized_via"] = via
    if not dry:
        path.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    return g, "finalized"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workbench", default=str(WORKBENCH))
    ap.add_argument("--decisions", help="decisions JSON (워크벤치 대신)")
    ap.add_argument("--also", action="append", default=[],
                    help="추가 일괄 확정 디렉터리 (예: scoring/grades_v2/controls)")
    ap.add_argument("--partial", action="store_true",
                    help="미체크 케이스 잔존 허용 (기본: 전건 서명 요구)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    args = ap.parse_args()

    if args.decisions:
        decisions = json.loads(Path(args.decisions).read_text(encoding="utf-8"))
        via = f"decisions JSON ({os.path.basename(args.decisions)})"
    else:
        decisions = parse_workbench(args.workbench)
        via = "RP-13 workbench"

    unticked = [d["case"] for d in decisions if d["action"] is None]
    if unticked and not args.partial:
        sys.exit(f"[FAIL] 미서명 {len(unticked)}건: {', '.join(unticked)} "
                 f"(부분 적용은 --partial)")

    counts = {"finalized": 0, "override": 0, "skip(already)": 0}
    for d in decisions:
        if d["action"] is None:
            continue
        p = grade_path(d["case"])
        if p is None:
            sys.exit(f"[FAIL] 미지 케이스 {d['case']} — grade 파일 없음")
        if d["action"] == "override":
            g = json.loads(p.read_text(encoding="utf-8"))
            ov = append_override(d["case"], g, d["reason"], d.get("fields"),
                                 args.date, args.dry_run)
            _, st = finalize_file(p, args.date, f"{via} + {ov}",
                                  d.get("fields"), args.dry_run)
            counts["override"] += 1
            print(f"{d['case']}: override → {ov} ({st})")
        else:
            _, st = finalize_file(p, args.date, via, None, args.dry_run)
            counts[st] += 1
            print(f"{d['case']}: {st}")

    for extra in args.also:
        for gp in sorted(glob.glob(str(REPO / extra / "*.json"))):
            _, st = finalize_file(Path(gp), args.date,
                                  f"blanket ({extra}, decisions_log 참조)",
                                  None, args.dry_run)
            counts[st] += 1
            print(f"{extra}/{os.path.basename(gp)}: {st}")

    remaining = [str(Path(gp).relative_to(REPO)) for d in GRADE_DIRS
                 for gp in sorted(glob.glob(str(REPO / d / "*.json")))
                 if json.loads(Path(gp).read_text(encoding="utf-8"))
                 .get("_meta", {}).get("human_finalized") is not True]
    tag = "[DRY-RUN] " if args.dry_run else ""
    print(f"\n{tag}적용: finalize {counts['finalized']} · override {counts['override']} "
          f"· 기확정 skip {counts['skip(already)']} · 미확정 잔존 {len(remaining)}")
    if remaining and not args.partial and not args.dry_run:
        sys.exit(f"[FAIL] human_finalized=false 잔존: {', '.join(remaining)}")
    if counts["override"] == 0 and counts["finalized"] >= 30:
        print("[NOTE] 오버라이드 0건 — Issue #0 고무도장 기준(§9) 해당 여부를 "
              "소유자가 명시적으로 확인할 것 (overrides.md 서두 참조).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
