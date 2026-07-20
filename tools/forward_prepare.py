"""forward 사이클 골격 생성 + 유니버스 내부 정합 검증 (spec §9, D100).

usage: python tools/forward_prepare.py --cycle forward/cycle_001

- 골격: evidence/ · outcome_updates.jsonl · PROTOCOL.md (모델 핀·동결 파일
  해시 스냅샷).
- universe.json이 이미 있으면 내부 정합(선정 수·중복 CIK·필수 필드)을
  검증한다. 없으면 골격만 만들고 열거 필요를 보고한다.
- 네트워크 0 · 모델 호출 0.
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_common import (REPO, UNIVERSE_SIZE, SCREENING_CUTOFF,
                            assert_subscription_only, read_json, sha256_file, fail)

PIN_SOURCES = [
    "pipeline/runner.py", "pipeline/cli_client.py", "pipeline/build_payload.py",
    "schemas/llm_output.json", "specs/FORWARD_WATCHLIST_V1.md",
    "specs/RISK_SCORE_SEMANTICS.md", "docs/UNIVERSE_SELECTION.md",
]


def evaluatee_model() -> str:
    m = re.search(r'EVALUATEE_MODEL\s*=\s*"([^"]+)"',
                  (REPO / "pipeline/runner.py").read_text(encoding="utf-8"))
    return m.group(1) if m else "UNRESOLVED"


def check_universe(u: dict) -> list[str]:
    errs = []
    sel = u.get("selected", [])
    if len(sel) != UNIVERSE_SIZE:
        errs.append(f"selected {len(sel)} ≠ {UNIVERSE_SIZE}")
    ciks = [r.get("cik") for r in sel]
    if len(set(ciks)) != len(ciks):
        errs.append("selected 내 중복 CIK")
    for r in sel:
        missing = [k for k in ("cik", "ticker", "name", "sic", "float_usd", "record_id")
                   if r.get(k) in (None, "")]
        if missing:
            errs.append(f"{r.get('cik', '?')}: 필수 필드 결측 {missing}")
    for r in sel:
        if not isinstance(r.get("float_usd"), (int, float)) or r["float_usd"] < 1e9:
            errs.append(f"{r.get('ticker', '?')}: float_usd < $1B 또는 비수치 — 규칙 위반")
    alt = u.get("alternates", [])
    if len({r.get("cik") for r in alt} & set(ciks)):
        errs.append("alternates와 selected 교집합 존재")
    if u.get("rule_ref") != "docs/UNIVERSE_SELECTION.md#§6":
        errs.append("rule_ref 부재/불일치 (docs/UNIVERSE_SELECTION.md#§6)")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True)
    args = ap.parse_args()
    assert_subscription_only()

    cycle = REPO / args.cycle
    (cycle / "evidence").mkdir(parents=True, exist_ok=True)
    outcomes = cycle / "outcome_updates.jsonl"
    if not outcomes.exists():
        outcomes.write_text("", encoding="utf-8")

    pins = {p: sha256_file(REPO / p) for p in PIN_SOURCES if (REPO / p).exists()}
    proto = cycle / "PROTOCOL.md"
    proto.write_text(
        "# PROTOCOL.md — cycle_001 동결 프로토콜 스냅샷\n\n"
        f"- generated: {datetime.date.today().isoformat()} (tools/forward_prepare.py)\n"
        f"- spec: specs/FORWARD_WATCHLIST_V1.md (규범 원문)\n"
        f"- screening_cutoff: {SCREENING_CUTOFF} (ET, EDGAR acceptance)\n"
        f"- evaluatee_model (pin): `{evaluatee_model()}`\n"
        "- execution path: subscription OAuth only — `claude -p` + "
        "`CLAUDE_CODE_OAUTH_TOKEN` via `pipeline/cli_client.py` (INVARIANT 4)\n"
        "- draws: k=1 · retry ≤2 · decision cuts: ≥70 flag / 40–69 review / "
        "<40 no_flag / insufficient→abstain (사전 등록 서수 컷)\n\n"
        "## 동결 파일 해시 (준비 시점)\n\n"
        + "\n".join(f"- `{p}` sha256 `{h}`" for p, h in sorted(pins.items()))
        + "\n\n모델 승계 조항·중단 규칙: spec §5·§3. 봉인 후 본 파일 수정 금지.\n",
        encoding="utf-8")
    print(f"OK — 골격+PROTOCOL.md 생성: {cycle}")

    upath = cycle / "universe.json"
    if not upath.exists():
        print("NOTE — universe.json 부재: tools/forward_enumerate.py 실행 필요 "
              "(governance/DECISION_FORWARD_UNIVERSE.md §5 권한 기록 참조)")
        return 0
    errs = check_universe(read_json(upath))
    if errs:
        fail("universe.json 정합 위반:\n  " + "\n  ".join(errs))
    print(f"OK — universe.json 정합 (selected {UNIVERSE_SIZE})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
