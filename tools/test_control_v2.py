"""CONTROL_CRITERIA_v2 규칙 고정 테스트 (RP-09 Stage 2 — 개정 방향성의 기계 증거).

실행: .venv/bin/python -m pytest tools/test_control_v2.py -q
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from control_v2 import (CASES_V2, aaer_hits_v2, name_tokens_v2, sic_tier,
                        N_PIT_V2, N_SELECT)

IDX = [
    {"aaer_no": "4515", "respondents": "General Electric Company"},
    {"aaer_no": "1001", "respondents": "General Cable Corporation"},
    {"aaer_no": "2652", "respondents": "ConAgra Foods, Inc."},
    {"aaer_no": "3841", "respondents": "Kraft Foods Inc. n/k/a Mondelez Global LLC"},
    {"aaer_no": "9001", "respondents": "Clete D. Madden, CPA, and David L. Huffman, CPA"},
    {"aaer_no": "9002", "respondents": "Steven A. Fishman and John Doe"},
    {"aaer_no": "9003", "respondents": "Douglas Campbell and Associates LLP"},
    {"aaer_no": "9004", "respondents": "Campbell Soup Company"},
    {"aaer_no": "9005", "respondents": "Mills Manufacturing General Partner"},
]


# ── (iii) E4-v2: 다토큰 구문 규칙 ────────────────────────────────────────
def test_general_mills_not_hit_by_general_token():
    """v1.1 실탈락 재현 케이스: 'general' 단독 토큰은 비적중이어야 한다."""
    hits = aaer_hits_v2(["GENERAL MILLS INC"], IDX[:2])
    assert hits == []


def test_general_mills_hits_when_both_words_present():
    """다토큰 전 단어 공존이면 적중 (미탐 방향 보호 — 순서 무관 보수 규칙)."""
    hits = aaer_hits_v2(["GENERAL MILLS INC"],
                        [{"aaer_no": "x", "respondents": "General Mills, Inc."}])
    assert len(hits) == 1
    # 두 단어가 다른 맥락으로 공존해도 적중 = 보수(과잉 배제) 방향으로만 오차
    assert aaer_hits_v2(["GENERAL MILLS INC"], [IDX[8]])


def test_steven_madden_not_hit():
    """Madden 모호성의 규칙 해소: 'steven'·'madden' 단독 인명은 비적중."""
    assert aaer_hits_v2(["STEVEN MADDEN, LTD."], IDX) == []


def test_real_exposures_still_hit():
    """실제 AAER 노출(ConAgra, 구 Kraft Foods 계보)은 v2에서도 적중 유지."""
    assert aaer_hits_v2(["CONAGRA BRANDS, INC.", "ConAgra Foods Inc"], IDX)
    assert aaer_hits_v2(["Mondelez International, Inc.", "KRAFT FOODS INC"], IDX)


def test_single_token_needs_corporate_suffix_adjacency():
    """단일 토큰 이름: 인명('Douglas Campbell ... LLP' — 직후 2단어 밖) 비적중,
    법인 표기('Campbell Soup Company')는 적중... 단 'soup'가 접미가 아니므로
    직후 2단어 규칙 내 'company' 포함 → 적중."""
    camp = [{"aaer_no": "9003", "respondents": "Douglas Campbell and Associates LLP"}]
    assert aaer_hits_v2(["CAMPBELL'S CO"], camp) == []
    assert aaer_hits_v2(["CAMPBELL'S CO"], [IDX[7]])


def test_tokenizer_drops_suffixes_and_short():
    assert name_tokens_v2("The Campbell's Company") == ["campbell"]
    assert name_tokens_v2("AIR PRODUCTS & CHEMICALS, INC.") == ["air", "products", "chemicals"]


# ── (i) 무조건 확장 + T21 SIC 정정 ───────────────────────────────────────
def test_t21_sic_correction():
    assert CASES_V2["T21"]["sic_supp"] == ["8732", "7375", "8700", "8742"]
    # 그 외 케이스 선언 무변경
    from rp08_common import CASES
    for tid in CASES:
        if tid != "T21":
            assert CASES_V2[tid]["sic_supp"] == CASES[tid]["sic_supp"]


def test_fetch_plan_has_no_early_break():
    """순서 버그 회귀 방지: cmd_fetch 소스에 확장 조기 탈출(break) 조건 부재."""
    src = (Path(__file__).parent / "control_v2.py").read_text(encoding="utf-8")
    assert "MIN_ELIGIBLE" not in src.split("def cmd_fetch")[1].split("def cmd_validate")[0]


# ── (ii) S2-v2 전순서 ────────────────────────────────────────────────────
def test_sic_tier_ordering():
    spec = CASES_V2["T12"]
    assert sic_tier(spec, "3577") == 0          # 1차
    assert sic_tier(spec, "3651") == 1          # 보충 1순위
    assert sic_tier(spec, "3576") == 4          # 보충 4순위
    assert N_SELECT == 3 and N_PIT_V2 == 40


# ── (3d) 프로브 러너 병렬화 회귀 방지 ────────────────────────────────────
def test_probe_runner_is_concurrent():
    src = (Path(__file__).parents[1] / "pipeline/probe_runner.py").read_text(encoding="utf-8")
    assert "ThreadPoolExecutor" in src and "--concurrency" in src


def test_s0_gate_has_no_exclusion_power():
    """S0-v2 개정 회귀 방지: 조잡 게이트가 eligible을 끄는 코드 부재 (우선순위 전용)."""
    src = (Path(__file__).parent / "control_v2.py").read_text(encoding="utf-8")
    fetch_c = src.split("def cmd_fetch")[1].split("def cmd_validate")[0]
    assert "조잡 게이트 |log|" not in fetch_c
    assert "COARSE_BAND" not in src


def test_e8b_owner_confirmed_enforcement_exclusion():
    """A1 규칙화 회귀 방지: ADI CIK가 E8b 테이블에 있고 eligibility가 이를 거른다."""
    import datetime
    from control_v2 import OWNER_CONFIRMED_ENFORCEMENT_CIKS, eligibility_v2
    assert "0000006281" in OWNER_CONFIRMED_ENFORCEMENT_CIKS
    rec = {"cik": "0000006281", "pre_cutoff_10K": 20, "pre_cutoff_10Q": 60,
           "fpi_forms": 0, "xbrl_pre_cutoff": True, "active_in_window": True,
           "item_402_in_window": [], "first_counted": "1995-01-01",
           "tickers": ["ADI"]}
    ok, fails = eligibility_v2(rec, datetime.date(2015, 9, 10), [])
    assert not ok and any("E8b" in f for f in fails)
