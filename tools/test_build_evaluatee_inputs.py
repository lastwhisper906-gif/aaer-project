"""피평가자 입력 파일의 오염 차단 강제 테스트.

4중 방어: ① 커밋본 = 재생성본 (드리프트 차단) ② 스키마 additionalProperties:false
③ 금지 필드 명시 목록 (스키마가 실수로 완화되어도 여기서 깨짐)
④ 값 수준 누출 스캔 (2026-07-05 표본 점검 교훈 — ①~③은 어떤 '필드'가
   존재하는지만 보고 필드 '값'의 내용은 보지 않았다. OV-001/OV-002).
"""
import json
import re
from pathlib import Path

import pytest
from jsonschema import Draft7Validator, FormatChecker

from build_evaluatee_inputs import DEST, MAPPING_DEST, build

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

NEUTRAL_ID = re.compile(r"^case_[0-9]{2}$")
GROUP_ENCODING_ID = re.compile(r"^[TC]\d+")  # 원본 T/C 접두사 — 그룹 소속 인코딩

# 케이스 필드 값 어디에도 나타나면 안 되는 부분열 (소문자 대조).
# 후신 사명(사후 정보), 정답지 어휘, 집행 절차 어휘 — 필요 시 확장.
FORBIDDEN_VALUE_SUBSTRINGS = [
    "n/k/a", "n.k.a", "now known as", "(now ", "; now ",
    "aaer", "sec v.", "sec vs",
    "fraud", "restatement", "restated", "manipulat", "scheme",
    "enforcement", "litigation", "complaint", "investigation",
    "short seller", "short-seller", "whistleblower", "delist",
]


@pytest.fixture(scope="module")
def committed():
    assert DEST.is_file(), f"{DEST} 없음 — tools/build_evaluatee_inputs.py 실행 후 커밋할 것"
    return json.loads(DEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def committed_mapping():
    assert MAPPING_DEST.is_file(), f"{MAPPING_DEST} 없음 — 빌더 실행 후 커밋할 것"
    return json.loads(MAPPING_DEST.read_text(encoding="utf-8"))


def test_committed_file_matches_regeneration(committed, committed_mapping):
    payload, mapping_payload = build()
    assert committed == payload, (
        "data/evaluatee/cases.json이 candidates.json과 불일치 — "
        "tools/build_evaluatee_inputs.py로 재생성해 함께 커밋할 것"
    )
    assert committed_mapping == mapping_payload, "id_mapping.json 드리프트 — 재생성해 커밋할 것"


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


# ---- 방어 ④: 값 수준 누출 스캔 (필드가 아니라 값을 본다) ----

def test_case_ids_are_neutral(committed):
    for case in committed["cases"]:
        cid = case["case_id"]
        assert NEUTRAL_ID.fullmatch(cid), f"중립 ID 형식 위반: {cid!r}"
        assert not GROUP_ENCODING_ID.match(cid), f"그룹 인코딩 ID 잔존: {cid!r}"


def test_no_forbidden_substring_in_any_value(committed):
    for case in committed["cases"]:
        for field, value in case.items():
            if not isinstance(value, str):
                continue
            low = value.lower()
            for sub in FORBIDDEN_VALUE_SUBSTRINGS:
                assert sub not in low, (
                    f"{case['case_id']}.{field}: 금지 부분열 {sub!r} — 값 수준 누출 "
                    f"(value={value!r})"
                )


def test_ticker_is_single_primary(committed):
    for case in committed["cases"]:
        assert "/" not in case["ticker"], f"{case['case_id']}: 복합 티커 {case['ticker']!r}"


def test_id_mapping_bijection_and_shuffle(committed, committed_mapping):
    mapping = committed_mapping["mapping"]
    n = len(committed["cases"])
    # 전단사: 중립 ID n개 ↔ 원본 ID n개, 파일의 case_id와 정확히 일치
    assert len(mapping) == n and len(set(mapping.values())) == n
    assert set(mapping) == {c["case_id"] for c in committed["cases"]}
    # 셔플 실효성: 중립 순번이 원본 정렬 순서를 그대로 따르면 순번이 곧 원본 ID
    in_neutral_order = [mapping[k] for k in sorted(mapping)]
    assert in_neutral_order != sorted(mapping.values()), (
        "중립 순번 = 원본 정렬 순서 — 셔플이 무력화됨 (순번-그룹 상관 차단 실패)"
    )


def test_id_mapping_lives_outside_evaluatee_path():
    assert "evaluatee" not in MAPPING_DEST.parts, (
        f"매핑 파일이 피평가자 경로 안에 있음: {MAPPING_DEST}"
    )
    # 피평가자 파일 쪽에도 원본 ID가 새어 있지 않아야 한다
    text = DEST.read_text(encoding="utf-8")
    assert not re.search(r'"[TC]\d{2}"', text), "피평가자 파일에 원본 T/C ID 문자열 존재"
