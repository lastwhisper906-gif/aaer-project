"""피평가자 입력 파일의 오염 차단 강제 테스트.

3중 방어: ① 커밋본 = 재생성본 (드리프트 차단) ② 스키마 additionalProperties:false
③ 금지 필드 명시 목록 (스키마가 실수로 완화되어도 여기서 깨짐).
"""
import json
from pathlib import Path

import pytest
from jsonschema import Draft7Validator, FormatChecker

from build_evaluatee_inputs import DEST, build

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "evaluatee_input.json").read_text(encoding="utf-8"))

# ground truth로 간주되는 필드 — 하나라도 생성물에 나타나면 백테스트 오염
FORBIDDEN_FIELDS = {
    "group", "scheme_type", "scheme_summary", "matched_case_id",
    "aaer_no", "aaer_date", "aaer_url",
    "manipulation_period_start", "manipulation_period_end",
    "first_revelation_date", "revelation_source",
    "ab_classification", "ab_signed_off",
    "pre_revelation_quarters_available", "xbrl_available", "notes",
}


@pytest.fixture(scope="module")
def committed():
    assert DEST.is_file(), f"{DEST} 없음 — tools/build_evaluatee_inputs.py 실행 후 커밋할 것"
    return json.loads(DEST.read_text(encoding="utf-8"))


def test_committed_file_matches_regeneration(committed):
    assert committed == build(), (
        "data/evaluatee/cases.json이 candidates.json과 불일치 — "
        "tools/build_evaluatee_inputs.py로 재생성해 함께 커밋할 것"
    )


def test_every_case_passes_evaluatee_schema(committed):
    validator = Draft7Validator(SCHEMA, format_checker=FormatChecker())
    for case in committed["cases"]:
        errors = list(validator.iter_errors(case))
        assert not errors, f"{case.get('case_id')}: {[e.message for e in errors]}"


def test_no_ground_truth_field_present(committed):
    for case in committed["cases"]:
        leaked = FORBIDDEN_FIELDS & set(case)
        assert not leaked, f"{case.get('case_id')}: ground truth 필드 누출 {sorted(leaked)}"


def test_no_ground_truth_text_leaks_into_file():
    # 필드명 밖 누출(예: _meta에 요약 문자열)도 차단 — 금지 키워드의 파일 전체 스캔
    text = DEST.read_text(encoding="utf-8")
    for token in ("aaer", "scheme", "revelation", "manipulation", "fraud"):
        # _meta의 계약 설명에 쓰는 단어와 겹치지 않도록 금지 토큰은 소문자 필드명 계열로 한정
        assert f'"{token}' not in text.lower(), f"금지 토큰 {token!r}이 생성물에 존재"
