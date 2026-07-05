"""피평가자 입력 파일 생성 (ground truth 오염 차단 — schemas/evaluatee_input.json 계약).

candidates.json(정답지 포함)에서 화이트리스트 필드만 추출해
data/evaluatee/cases.json을 생성한다. 물리적 분리가 방어의 핵심:
피평가자 코드는 candidates.json을 열 일이 없고(pipeline/test_no_guard_bypass.py가
직독을 금지), 이 생성물에 금지 필드가 없는지는 tools/test_build_evaluatee_inputs.py가
스키마(additionalProperties: false) + 재생성 대조로 강제한다.

출력은 결정론적(타임스탬프 없음, case_id 정렬) — 커밋본과 재생성본의
바이트 대조가 CI에서 가능하다.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CANDIDATES = REPO / "data" / "candidates" / "candidates.json"
DEST = REPO / "data" / "evaluatee" / "cases.json"

# schemas/evaluatee_input.json required와 1:1 — 여기 필드를 늘리려면 스키마 개정(=서명) 필요
WHITELIST = ["case_id", "ticker", "cik", "company_name", "cutoff_date"]


def build() -> dict:
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))["candidates"]
    cases = [
        {field: c[field] for field in WHITELIST}
        for c in sorted(candidates, key=lambda c: c["case_id"])
    ]
    return {
        "_meta": {
            "contract": "schemas/evaluatee_input.json",
            "warning": "피평가자에게는 이 파일 외의 케이스 메타데이터를 제공하지 않는다 "
                       "(candidates.json은 ground truth — PROJECT.md §7 역할 분리)",
            "generated_by": "tools/build_evaluatee_inputs.py (결정론 — 재생성 대조는 CI)",
        },
        "cases": cases,
    }


def main() -> int:
    payload = build()
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {DEST} ({len(payload['cases'])} cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
