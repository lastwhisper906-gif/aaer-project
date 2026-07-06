"""RP-08 공통 상수·스크린 로직 (CONTROL_CRITERIA_v1.md의 코드 미러).

fetch_control_pool_rp08.py(수집)와 select_control_group_rp08.py(선정)가 같은
판정 함수를 쓰도록 분리 — 두 스크립트 간 로직 드리프트 방지. 모든 수치 상수는
criteria 문서 §1~§4와 1:1 대응하며, 문서 수정 없이 이 파일만 바꾸는 것은 금지.
"""
import datetime
import hashlib
import json
import math
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RAW_DIR = REPO / "runs/rp08/control_pool_raw"
BIG_DIR = Path.home() / "aaer-data/_rp08"  # 대용량 원문 (git 밖, data/README 규약)
PROVENANCE = RAW_DIR / "provenance.jsonl"
MANIFEST = RAW_DIR / "MANIFEST.sha256"

# ── criteria §1: 실험군 매칭 대상 (고정 상수) ─────────────────────────────
CASES = {
    "T07": {"ticker": "MON", "cik": "0001110783", "cutoff": "2011-06-28",
            "fye_month": 8, "rev_pit": 10_502_000_000, "assets_pit": 19_649_000_000,
            "sic_primary": ["2870"], "sic_supp": ["2800", "2810", "2820", "2860", "2890"]},
    "T11": {"ticker": "OFIX", "cik": "0000884624", "cutoff": "2013-07-28",
            "fye_month": 12, "rev_pit": 462_320_000, "assets_pit": 503_380_000,
            "sic_primary": ["3841"], "sic_supp": ["3842", "3845"]},
    "T12": {"ticker": "LOGI", "cik": "0001032975", "cutoff": "2013-08-06",
            "fye_month": 3, "rev_pit": 2_099_883_000, "assets_pit": 1_374_111_000,
            "sic_primary": ["3577"], "sic_supp": ["3651", "3661", "3812", "3576"]},
    "T13": {"ticker": "HTZ", "cik": "0001657853", "cutoff": "2014-05-12",
            "fye_month": 12, "rev_pit": 10_771_900_000, "assets_pit": 24_588_400_000,
            "sic_primary": ["7510"], "sic_supp": ["7500", "7359"]},
    "T16": {"ticker": "ICON", "cik": "0000857737", "cutoff": "2015-08-09",
            "fye_month": 12, "rev_pit": 461_243_000, "assets_pit": 3_021_902_000,
            "sic_primary": ["6794", "3140"], "sic_supp": ["2300", "2320", "2330", "5136", "5137"]},
    "T17": {"ticker": "MRVL", "cik": "0001058057", "cutoff": "2015-09-10",
            "fye_month": 1, "rev_pit": 3_706_963_000, "assets_pit": 5_842_049_000,
            "sic_primary": ["3674"], "sic_supp": ["3672", "3576"]},
    "T21": {"ticker": "SCOR", "cik": "0001158172", "cutoff": "2016-02-28",
            "fye_month": 12, "rev_pit": 329_151_000, "assets_pit": 545_648_000,
            "sic_primary": ["7389"], "sic_supp": ["8732", "7375"]},
    "T28": {"ticker": "KHC", "cik": "0001637459", "cutoff": "2019-02-20",
            "fye_month": 12, "rev_pit": 26_232_000_000, "assets_pit": 119_730_000_000,
            "sic_primary": ["2030"], "sic_supp": ["2000", "2040", "2013", "2052", "2090"]},
}

# ── criteria §3/§4: 스크린 임계 ───────────────────────────────────────────
MIN_10K = 3               # E1
MIN_10Q = 8               # E1
ACTIVE_MONTHS = 18        # E3
RESTATE_BACK_Y = 5        # E5: 컷오프 −5년
RESTATE_FWD_Y = 3         # E5: 컷오프 +3년
HISTORY_Y = 3             # E6a: 최초 계상 제출 ≤ 컷오프 −3년
COARSE_BAND = math.log(6)  # S0 frames 조잡 게이트
SIZE_BAND = math.log(4)    # S1
TIE_DELTA = 0.05           # S2
N_PIT = 25                 # S0 companyfacts 조회 상한 (케이스당)
N_ALT = 3                  # S3 대안 순위 기록 수
MIN_ELIGIBLE = 5           # §2 보충 SIC 발동 임계

ANNUAL = {"10-K", "10-K405", "10-KT"}
QUARTER = {"10-Q", "10-QT"}
SALES_TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
              "SalesRevenueNet", "SalesRevenueGoodsNet", "SalesRevenueServicesNet"]
FRAME_TAGS = ["Revenues", "SalesRevenueNet",
              "RevenueFromContractWithCustomerExcludingAssessedTax"]

# E8: RP-01 §2 실격 승계 (J5 — 증거는 RP-01에 1차 소스로 확정)
RP01_DISQUALIFIED_CIKS = {
    "0000844161": "Cherokee/Apex Global Brands — AAER-4199",
    "0000749251": "Gartner — AAER-4411",
    "0000723612": "Avis Budget = Cendant CIK — AAER-1272/1276",
    "0001067701": "United Rentals — 2008 SEC 회계사기 화해 (PR 2008-190)",
}

_SUFFIXES = {"the", "co", "corp", "inc", "ltd", "llc", "plc", "company",
             "corporation", "holdings", "holding", "group", "international",
             "incorporated", "limited", "nv", "sa", "ag"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def name_key(name: str) -> str:
    """AAER 색인 대조 키: 법인 접미·관사 제거 후 첫 토큰 (criteria E4)."""
    tokens = re.sub(r"[^A-Za-z ]", " ", name or "").lower().split()
    core = [t for t in tokens if t not in _SUFFIXES]
    return (core or tokens or [""])[0]


def aaer_hits(names: list, index_entries: list) -> list:
    """현재 사명 + formerNames 전체에 대한 색인 적중 (E4)."""
    hits = []
    for nm in names:
        key = name_key(nm)
        if len(key) < 3:  # 한 글자·관사 잔여 키는 대조 불능 — 기록만
            continue
        for e in index_entries:
            if key in e["respondents"].lower():
                hits.append({"name_checked": nm, "key": key,
                             "aaer_no": e["aaer_no"],
                             "respondents": e["respondents"][:80]})
    return hits


def screen_submissions(blocks: list, meta: dict, cutoff: datetime.date) -> dict:
    """submissions JSON(전 청크) → E1/E3/E5/E6a 판정 필드 (기계 전수).

    blocks: [recent, older...] 각각 form/filingDate/isXBRL/items 병렬 배열.
    """
    ann = q = 0
    xbrl = False
    first_counted = None
    last_in_window = None
    r402 = []
    active_floor = cutoff - datetime.timedelta(days=ACTIVE_MONTHS * 30)
    rs = cutoff - datetime.timedelta(days=RESTATE_BACK_Y * 365)
    re_ = cutoff + datetime.timedelta(days=RESTATE_FWD_Y * 365)
    fpi = 0
    for b in blocks:
        forms = b["form"]
        n = len(forms)
        items_arr = b.get("items", [""] * n)
        isx = b.get("isXBRL", [0] * n)
        for i in range(n):
            d = datetime.date.fromisoformat(b["filingDate"][i])
            form = forms[i]
            if form in ("20-F", "40-F"):
                fpi += 1
            if form.startswith("8-K") and "4.02" in (items_arr[i] or ""):
                if rs <= d <= re_:
                    r402.append(b["filingDate"][i])
            if d > cutoff:
                continue
            if form in ANNUAL:
                ann += 1
            elif form in QUARTER:
                q += 1
            else:
                continue
            if isx[i]:
                xbrl = True
            if first_counted is None or d < first_counted:
                first_counted = d
            if d >= active_floor:
                last_in_window = max(last_in_window or d, d)
    return {
        "pre_cutoff_10K": ann, "pre_cutoff_10Q": q,
        "xbrl_pre_cutoff": xbrl,
        "first_counted": first_counted.isoformat() if first_counted else None,
        "active_in_window": last_in_window is not None,
        "item_402_in_window": sorted(r402),
        "fpi_forms": fpi,
        "sic": meta.get("sic"), "sic_desc": meta.get("sicDescription"),
        "name": meta.get("name"), "fye": meta.get("fiscalYearEnd"),
        "former_names": [f.get("name", "") for f in meta.get("formerNames", [])],
    }


def eligibility(rec: dict, cutoff: datetime.date, e4_hits: list,
                overrides: dict) -> tuple:
    """하드 스크린 E1~E8 (규모 제외) → (eligible, fail_codes, discretionary)."""
    fails, disc = [], []
    if rec["pre_cutoff_10K"] < MIN_10K or rec["pre_cutoff_10Q"] < MIN_10Q:
        fails.append(f"E1 filing history 10-K={rec['pre_cutoff_10K']} 10-Q={rec['pre_cutoff_10Q']}")
    if rec["fpi_forms"] > 0 and rec["pre_cutoff_10K"] == 0:
        fails.append("E1 FPI(20-F/40-F 전용)")
    if not rec["xbrl_pre_cutoff"]:
        fails.append("E2 XBRL 부재(pre-cutoff)")
    if not rec["active_in_window"]:
        fails.append("E3 비활동(18개월)")
    if e4_hits:
        ov = overrides.get(rec["cik"])
        if ov and ov.get("pass"):
            disc.append({"flag": "E4-동명이인 수기 통과", "evidence": ov.get("evidence"),
                         "hits": e4_hits[:3]})
        else:
            fails.append(f"E4 AAER 색인 적중 {len(e4_hits)}건 (예: AAER-{e4_hits[0]['aaer_no']})")
    if rec["item_402_in_window"]:
        fails.append(f"E5 Item 4.02 재작성 {rec['item_402_in_window']}")
    if rec["first_counted"] is None or datetime.date.fromisoformat(
            rec["first_counted"]) > cutoff - datetime.timedelta(days=HISTORY_Y * 365):
        fails.append("E6a 제출 이력 <3년")
    if rec["cik"] in RP01_DISQUALIFIED_CIKS:
        fails.append(f"E8 RP-01 실격 승계: {RP01_DISQUALIFIED_CIKS[rec['cik']]}")
    return (not fails), fails, disc


def pit_size(companyfacts: dict, cutoff: datetime.date) -> tuple:
    """PIT 매출·총자산 (filed ≤ cutoff, 전 태그 합집합, 최신 기말·최신 filed).

    criteria §1 각주의 재계산 규약과 동일 — treatment_targets 검증에도 사용.
    """
    gaap = companyfacts.get("facts", {}).get("us-gaap", {})

    def best(tags, dur):
        cand = {}
        for tag in tags:
            for f in gaap.get(tag, {}).get("units", {}).get("USD", []):
                if datetime.date.fromisoformat(f["filed"]) > cutoff:
                    continue
                has_start = bool(f.get("start"))
                if dur:
                    if not has_start:
                        continue
                    span = (datetime.date.fromisoformat(f["end"])
                            - datetime.date.fromisoformat(f["start"])).days
                    if not (340 <= span <= 400):
                        continue
                elif has_start:
                    continue
                prev = cand.get(f["end"])
                if prev is None or f["filed"] > prev[1]:
                    cand[f["end"]] = (f["val"], f["filed"])
        if not cand:
            return None
        return cand[max(cand)][0]

    return best(SALES_TAGS, True), best(["Assets"], False)


def fye_month_dist(fye_field: str, target_month: int):
    """FYE 월 원형 거리 0~6 (S2). fye_field 예: '1231'."""
    if not fye_field or len(fye_field) != 4 or not fye_field.isdigit():
        return None
    m = int(fye_field[:2])
    if not 1 <= m <= 12:
        return None
    d = abs(m - target_month)
    return min(d, 12 - d)


def treatment_ciks() -> set:
    """E7: 실험군 30 후보 풀 전체 CIK."""
    cands = json.loads((REPO / "data/candidates/candidates.json").read_text())
    return {c["cik"] for c in cands["candidates"]
            if c.get("cik") and c.get("group") == "treatment"}
