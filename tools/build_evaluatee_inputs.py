"""피평가자 입력 파일 생성 (ground truth 오염 차단 — schemas/evaluatee_input.json 계약).

candidates.json(정답지 포함)에서 화이트리스트 필드만 추출해
data/evaluatee/cases.json을 생성한다. 물리적 분리가 방어의 핵심:
피평가자 코드는 candidates.json을 열 일이 없고(pipeline/test_no_guard_bypass.py가
직독을 금지), 이 생성물에 금지 필드가 없는지는 tools/test_build_evaluatee_inputs.py가
스키마(additionalProperties: false) + 재생성 대조 + 값 수준 스캔으로 강제한다.

2026-07-05 표본 점검(§7)이 잡은 값 수준 누출 2건의 정정 (OV-001/OV-002,
서명 결정 — scoring/overrides.md):
  1. case_id의 T/C 접두사가 그룹 소속(=정답)을 인코딩 → 중립 ID(case_NN)로
     치환 + 고정 시드 셔플(순번-그룹 상관 차단). 원본 매핑은 채점 전용
     data/scoring/id_mapping.json (피평가자 경로 밖).
  2. company_name의 후신 사명(n/k/a, "now …")은 정의상 컷오프 이후 정보(§5-1
     위반이 필드 값 안에) → 컷오프 시점 사명만 남긴다. f/k/a(과거 정보)는 유지.
  부수 정정: 복합 티커("UAA/UA")는 주 상장 티커만 ("A/B" → "A").

출력은 결정론적(고정 시드, 타임스탬프 없음) — 커밋본과 재생성본의
바이트 대조가 CI에서 가능하다.
"""
import json
import random
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CANDIDATES = REPO / "data" / "candidates" / "candidates.json"
DEST = REPO / "data" / "evaluatee" / "cases.json"
MAPPING_DEST = REPO / "data" / "scoring" / "id_mapping.json"

# schemas/evaluatee_input.json required와 1:1 — 여기 필드를 늘리려면 스키마 개정(=서명) 필요
WHITELIST = ["case_id", "ticker", "cik", "company_name", "cutoff_date"]

# 중립 ID 셔플 시드 — 고정값이어야 재생성 대조가 성립한다. 시드 자체는 비밀이
# 아니다(매핑 파일이 이미 채점 전용 경로에 평문으로 존재): 방어선은 시드의
# 은닉이 아니라 피평가자에게 매핑·candidates.json을 주지 않는 물리적 분리다.
NEUTRAL_ID_SEED = 20260705

# 컷오프 이후 정보(후신 사명) 제거 — "(n/k/a …)", "(now …)", "; n/k/a …" 꼴.
# f/k/a(개명 '이전' 사명 = 과거 정보)는 서명 결정대로 유지.
_POST_CUTOFF_PAREN = re.compile(r"\s*\(\s*(?:n/k/a|now(?:\s+known\s+as)?)\s+[^)]*\)", re.I)
_POST_CUTOFF_TAIL = re.compile(r"\s*;\s*(?:n/k/a|now(?:\s+known\s+as)?)\s+.*$", re.I)


def name_as_of_cutoff(name: str) -> str:
    return _POST_CUTOFF_TAIL.sub("", _POST_CUTOFF_PAREN.sub("", name)).strip()


def primary_ticker(ticker: str) -> str:
    return ticker.split("/")[0]


def build() -> tuple[dict, dict]:
    """(피평가자 파일 payload, 채점용 ID 매핑 payload)를 반환. 둘 다 결정론."""
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))["candidates"]
    ordered = sorted(candidates, key=lambda c: c["case_id"])
    random.Random(NEUTRAL_ID_SEED).shuffle(ordered)

    cases, mapping = [], {}
    for i, c in enumerate(ordered, start=1):
        neutral_id = f"case_{i:02d}"
        mapping[neutral_id] = c["case_id"]
        cases.append({
            "case_id": neutral_id,
            "ticker": primary_ticker(c["ticker"]),
            "cik": c["cik"],
            "company_name": name_as_of_cutoff(c["company_name"]),
            "cutoff_date": c["cutoff_date"],
        })

    payload = {
        "_meta": {
            "contract": "schemas/evaluatee_input.json",
            "warning": "피평가자에게는 이 파일 외의 케이스 메타데이터를 제공하지 않는다 "
                       "(candidates.json은 ground truth — PROJECT.md §7 역할 분리)",
            "generated_by": "tools/build_evaluatee_inputs.py (결정론 — 재생성 대조는 CI)",
            "id_convention": "중립 ID(case_NN), 고정 시드 셔플 — 원본 매핑은 채점 전용 "
                             "data/scoring/id_mapping.json (OV-001)",
            "name_convention": "company_name은 컷오프 시점 사명만 — 후신 사명(n/k/a 등) "
                               "제거, f/k/a 유지 (OV-002)",
            "ticker_convention": "복합 티커는 주 상장 티커만 ('A/B' → 'A')",
        },
        "cases": cases,
    }
    mapping_payload = {
        "_meta": {
            "warning": "채점 시에만 사용 — 피평가자(파이프라인)에 절대 제공·노출 금지. "
                       "pipeline/test_no_guard_bypass.py가 pipeline/ 내 참조를 금지한다",
            "generated_by": "tools/build_evaluatee_inputs.py (NEUTRAL_ID_SEED 고정)",
        },
        "mapping": mapping,
    }
    return payload, mapping_payload


def main() -> int:
    payload, mapping_payload = build()
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    MAPPING_DEST.parent.mkdir(parents=True, exist_ok=True)
    MAPPING_DEST.write_text(
        json.dumps(mapping_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"wrote {DEST} ({len(payload['cases'])} cases)")
    print(f"wrote {MAPPING_DEST} ({len(mapping_payload['mapping'])} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
