"""V1 부분 탈익명화(partial de-identification) 공개의 회귀 테스트 (2026-07-20, D99).

두 층위를 분리해 고정한다:

1. **특성화(characterization)** — v1 `build_payload(perturb=True)`는 원본
   accession 번호·원본 제출일 연대기를 유지한다. 이것은 결함 수리가 아니라
   *사실의 고정*이다: v1 동결 산출물은 재실행하지 않으며(계획 §0.1), 이
   테스트는 v1 교란 프레임이 "부분 탈익명화"로만 서술되어야 하는 근거를
   기계로 재확인한다 (analysis/V1_PARTIAL_DEIDENTIFICATION_AUDIT.md).
   이 테스트가 깨지면 = 누군가 동결 빌더를 소급 수정했다는 뜻이다.

2. **회귀 가드(regression)** — 앞으로 "identity-masked / identifier-removed"
   급으로 서술되는 어떤 페이로드도 원본 accession 번호·원본 CIK·회사명·
   티커를 포함할 수 없다. 현재 그 서술 등급에 해당하는 유일한 경로는
   v2 date-shift(`date_shift.shift_payload` — accession 중립 ID 치환 포함)다.
   미래 변형은 `assert_fully_deidentified`를 통과해야 같은 서술을 쓸 수 있다.

데이터 의존: data/evaluatee/cases*.json 헤더 + ~/aaer-data 코퍼스(시리즈 원천).
코퍼스 부재 시(CI 러너) skip — test_build_payload.py와 동일 규약 (강제 지점은
로컬 실행 게이트).
"""
import json
import re
from pathlib import Path

import pytest

import build_payload as bp
import date_shift

pytestmark = pytest.mark.skipif(
    not bp.DATA_DIR.exists(),
    reason="~/aaer-data 코퍼스 부재 (CI runner) — 로컬 실행 게이트에서 강제")

REPO = Path(__file__).resolve().parent.parent
ACCESSION_RE = re.compile(r"\d{10}-\d{2}-\d{6}")

CASE_FILES = [
    REPO / "data/evaluatee/cases.json",        # wave-1
    REPO / "data/evaluatee/cases_wave2.json",  # wave-2
]


def _first_case(path):
    return json.loads(path.read_text(encoding="utf-8"))["cases"][0]


def _original_accessions(case):
    """원본(비교란) 페이로드에 등장하는 모든 원본 accession 번호.

    케이스 입력 JSON은 헤더뿐이고 시리즈는 코퍼스에서 빌드되므로,
    원본 accession 집합은 perturb=False 페이로드에서 취한다.
    """
    original = bp.build_payload(case, perturb=False)
    return set(ACCESSION_RE.findall(json.dumps(original, ensure_ascii=False)))


def assert_fully_deidentified(payload, case):
    """'identifier_removed / identity-masked' 서술 등급의 기계 정의.

    미래의 어떤 페이로드 변형이든 이 서술을 쓰려면 이 함수를 통과해야 한다
    (계획 §1.4). 구조적 지문(비율·추세·연대기 형태)은 검사 대상이 아니다 —
    그것은 의도적으로 보존되는 축이다 (docs/CLAIM_HIERARCHY.md·§5 정책).
    """
    blob = json.dumps(payload, ensure_ascii=False)
    # 원본 accession 번호 (접두부는 제출 filer CIK, 중간부는 제출 연도 인코딩)
    leaked = _original_accessions(case) & set(ACCESSION_RE.findall(blob))
    assert not leaked, f"원본 accession 잔존: {sorted(leaked)[:3]}"
    # 원본 CIK (제로패딩/비패딩 양쪽)
    cik = str(case.get("cik", "")).lstrip("0")
    if cik:
        assert not re.search(rf"\b0*{cik}\b", blob), "원본 CIK 잔존"
    # 회사명·티커
    name = case.get("company_name", "")
    if name:
        assert name not in blob, "원본 회사명 잔존"
        # 법인 접미사 제거한 핵심 명칭도 검사 (예: 'Comscore, Inc.' → 'Comscore')
        core = re.sub(r",?\s+(Inc|Corp|Co|Ltd|LLC|Trust)\.?$", "", name, flags=re.I).strip()
        if len(core) >= 4:
            assert core.lower() not in blob.lower(), f"회사명 핵심부 잔존: {core}"
    ticker = case.get("ticker", "")
    if ticker and len(ticker) >= 2:
        assert not re.search(rf'"\s*{re.escape(ticker)}\s*"', blob), "원본 티커 잔존"


# ── 1. 특성화: v1 perturbed 프레임은 부분 탈익명화다 ──────────────────────

def test_v1_perturbed_retains_accessions_and_dates_characterization():
    for cases_file in CASE_FILES:
        case = _first_case(cases_file)
        payload = bp.build_payload(case, perturb=True)
        blob = json.dumps(payload, ensure_ascii=False)
        retained = _original_accessions(case) & set(ACCESSION_RE.findall(blob))
        # v1 동결 동작: accession 유지 (부분 탈익명화의 근거 — 소급 수정 금지)
        assert retained, (
            f"{cases_file.name}: v1 perturbed 프레임에서 accession이 사라졌다 — "
            "동결 빌더가 소급 수정되었는지 확인하라 (v1 서술·감사 문서와 불일치)")
        # v1이 실제로 제거한 것: 헤더의 회사명·티커·CIK
        hdr = payload["case"]
        assert "cik" not in hdr
        assert hdr["company_name"].startswith("Company ")
        assert hdr["ticker"].startswith("XX")


# ── 2. 회귀 가드: identity-masked 급 서술은 완전 탈익명화를 통과해야 한다 ──

def test_v2ds_payload_is_fully_deidentified():
    for cases_file in CASE_FILES:
        case = _first_case(cases_file)
        payload = bp.build_payload(case, perturb=True)
        shifted = date_shift.shift_payload(payload, date_shift.offset_for_case(case["case_id"]))
        assert_fully_deidentified(shifted, case)


def test_v2ds_uses_neutral_accession_ids():
    case = _first_case(CASE_FILES[0])
    payload = bp.build_payload(case, perturb=True)
    shifted = date_shift.shift_payload(payload, date_shift.offset_for_case(case["case_id"]))
    blob = json.dumps(shifted, ensure_ascii=False)
    assert re.search(r"acc-\d{3}", blob), "중립 accession ID(acc-NNN) 부재"
