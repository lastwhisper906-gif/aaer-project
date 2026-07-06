"""피평가자 페이로드 빌더 (Phase 3 — 피평가자 쪽 코드, 결정론·오프라인).

입력: data/evaluatee/cases.json (유일 허용 케이스 메타) + ~/aaer-data/{ticker}/
  {edgar,xbrl}/ 로컬 사본. 후보 레지스트리(정답지)·scoring/ 접근 금지 (정적 스캔 강제).
출력: 케이스당 페이로드 dict —
  1. case fields (evaluatee_input v1.1의 5필드)
  2. 구조화 재무 시계열: point-in-time XBRL 개념표 (연차 + 분기, filed <= cutoff,
     같은 (태그, 기간)은 컷오프 전 최신 filed 승리) + provenance(accession/filed)
  3. 제출물 연대기: 컷오프 전 EDGAR 제출 인덱스 (form, filingDate)
교란 변형(D8): perturb=True — 사명/티커 익명화 + 화폐값 상수배 재스케일 (케이스별
  결정론 k, 날짜 불변).

look-ahead 통제: 모든 시간 필터는 이 모듈의 cutoff 비교 한 곳으로 수렴하며,
test_build_payload.py가 컷오프 후 항목의 부재를 기계 검증한다.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import math
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALUATEE_CASES = REPO_ROOT / "data" / "evaluatee" / "cases.json"
DATA_DIR = Path.home() / "aaer-data"

# 페이로드에 싣는 us-gaap 태그 (원시 값 — 파생 지표·스크린 점수 금지).
PAYLOAD_TAGS = [
    "Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet",
    "SalesRevenueGoodsNet", "SalesRevenueServicesNet", "CostOfGoodsAndServicesSold",
    "CostOfRevenue", "CostOfGoodsSold", "CostOfServices", "GrossProfit",
    "OperatingIncomeLoss", "NetIncomeLoss", "ProfitLoss",
    "IncomeLossFromContinuingOperationsNetOfTax",
    "NetIncomeLossAvailableToCommonStockholdersBasic",
    "SellingGeneralAndAdministrativeExpense", "GeneralAndAdministrativeExpense",
    "ResearchAndDevelopmentExpense", "InterestExpense",
    "DepreciationDepletionAndAmortization", "Depreciation", "DepreciationAndAmortization",
    "Assets", "AssetsCurrent", "CashAndCashEquivalentsAtCarryingValue",
    "CashAndCashEquivalentsAtCarryingValueIncludingDiscontinuedOperations",
    "ShortTermInvestments", "MarketableSecuritiesCurrent",
    "AccountsReceivableNetCurrent", "ReceivablesNetCurrent", "AccountsReceivableNet",
    "AccountsNotesAndLoansReceivableNetCurrent", "InventoryNet",
    "PropertyPlantAndEquipmentNet", "PropertyPlantAndEquipmentGross",
    "Goodwill", "IntangibleAssetsNetExcludingGoodwill", "OtherAssetsNoncurrent",
    "Liabilities", "LiabilitiesCurrent", "AccountsPayableCurrent",
    "AccruedLiabilitiesCurrent", "DeferredRevenueCurrent", "ContractWithCustomerLiabilityCurrent",
    "LongTermDebtNoncurrent", "LongTermDebt", "LongTermDebtCurrent", "DebtCurrent",
    "SecuredLongTermDebt", "DebtAndCapitalLeaseObligations", "StockholdersEquity",
    "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
    "NetCashProvidedByUsedInOperatingActivities",
    "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
    "NetCashProvidedByUsedInInvestingActivities",
    "NetCashProvidedByUsedInFinancingActivities",
    "PaymentsToAcquirePropertyPlantAndEquipment",
    "ProceedsFromIssuanceOfCommonStock", "ProceedsFromIssuanceOfLongTermDebt",
    "AllowanceForDoubtfulAccountsReceivableCurrent",
    "ProductWarrantyAccrualClassifiedCurrent", "StandardProductWarrantyAccrual",
]
# 화폐 재스케일 제외 대상 (비화폐·주식수 등은 애초에 USD 단위가 아니라 미포함)

MONEY_UNIT = "USD"
ANNUAL_DAYS = (340, 400)
QUARTER_DAYS = (75, 100)


def _iso(s):
    return datetime.date.fromisoformat(str(s))


def perturb_factor(case_id: str) -> float:
    """케이스별 결정론 재스케일 상수 k ∈ [0.4, 2.5] 로그균등 (D8)."""
    h = hashlib.sha256(f"{case_id}perturb-v1".encode()).digest()
    u = int.from_bytes(h[:4], "big") / 0xFFFFFFFF
    lo, hi = math.log(0.4), math.log(2.5)
    return math.exp(lo + u * (hi - lo))


def load_pit_series(ticker: str, cutoff: datetime.date) -> dict:
    """point-in-time XBRL 시계열: filed <= cutoff, (태그, 기간) 최신 filed 승리."""
    xbrl_dir = DATA_DIR / ticker / "xbrl"
    files = sorted(xbrl_dir.glob("*CIK*.json"))
    if not files:
        raise FileNotFoundError(f"{xbrl_dir}: companyfacts 없음")
    table: dict[str, dict] = {}
    for path in files:
        gaap = json.loads(path.read_text(encoding="utf-8")).get("facts", {}).get("us-gaap", {})
        for tag in PAYLOAD_TAGS:
            for f in gaap.get(tag, {}).get("units", {}).get(MONEY_UNIT, []):
                if _iso(f["filed"]) > cutoff:
                    continue  # 유일한 look-ahead 필터 지점
                start = f.get("start")
                if start:
                    span = (_iso(f["end"]) - _iso(start)).days
                    if ANNUAL_DAYS[0] <= span <= ANNUAL_DAYS[1]:
                        ptype = "annual"
                    elif QUARTER_DAYS[0] <= span <= QUARTER_DAYS[1]:
                        ptype = "quarterly"
                    else:
                        continue
                else:
                    ptype = "instant"
                key = (f.get("start") or "") + "|" + f["end"]
                slot = table.setdefault(tag, {})
                prev = slot.get(key)
                cand = {"start": f.get("start"), "end": f["end"], "period_type": ptype,
                        "value": f["val"], "filed": f["filed"], "accession": f.get("accn"),
                        "form": f.get("form")}
                if prev is None or (cand["filed"], cand["accession"] or "") > (prev["filed"], prev["accession"] or ""):
                    slot[key] = cand
    return {tag: sorted(vals.values(), key=lambda v: (v["end"], v["start"] or ""))
            for tag, vals in sorted(table.items())}


def load_filing_chronology(ticker: str, cutoff: datetime.date) -> list[dict]:
    """컷오프 전 EDGAR 제출 인덱스 (form, filingDate) — T2 메타신호 채널."""
    edgar_dir = DATA_DIR / ticker / "edgar"
    chunks = sorted(edgar_dir.glob("CIK*.json"))
    if not chunks:
        raise FileNotFoundError(f"{edgar_dir}: submissions 없음")
    rows = []
    for chunk in chunks:
        j = json.loads(chunk.read_text(encoding="utf-8"))
        blocks = [j["filings"]["recent"]] if "filings" in j else [j]
        for b in blocks:
            for form, date in zip(b.get("form", []), b.get("filingDate", [])):
                if _iso(date) <= cutoff:
                    rows.append({"form": form, "filing_date": date})
    rows.sort(key=lambda r: (r["filing_date"], r["form"]))
    # 동일 (form, date) 중복 제거 (다중 CIK 청크 병합 시)
    dedup, seen = [], set()
    for r in rows:
        k = (r["form"], r["filing_date"])
        if k not in seen:
            seen.add(k)
            dedup.append(r)
    return dedup


def build_payload(case: dict, perturb: bool = False) -> dict:
    cutoff = _iso(case["cutoff_date"])
    series = load_pit_series(case["ticker"], cutoff)
    chronology = load_filing_chronology(case["ticker"], cutoff)
    fields = dict(case)
    k = 1.0
    if perturb:
        k = perturb_factor(case["case_id"])
        fields = {
            "case_id": case["case_id"],
            "ticker": f"XX{case['case_id'][-2:]}",
            "company_name": f"Company {case['case_id'].upper()}",
            "cutoff_date": case["cutoff_date"],
            # cik 제공하지 않음 (probes.md ② 규칙 1)
        }
        series = {tag: [{**v, "value": (round(v["value"] * k, 2)
                                        if isinstance(v["value"], (int, float)) else v["value"])}
                        for v in vals] for tag, vals in series.items()}
    return {
        "variant": "perturbed" if perturb else "original",
        "perturb_factor_recorded_scoring_side_only": None,  # k는 페이로드에 싣지 않는다
        "case": fields,
        "financial_series_point_in_time": series,
        "filing_chronology": chronology,
        "_k_internal": k,  # 러너가 채점 로그에만 기록 후 페이로드에서 제거
    }


def build_all(perturb: bool = False) -> list[dict]:
    cases = json.loads(EVALUATEE_CASES.read_text(encoding="utf-8"))["cases"]
    return [build_payload(c, perturb=perturb) for c in cases]
