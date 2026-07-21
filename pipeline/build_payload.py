"""피평가자 페이로드 빌더 (Phase 3 — 피평가자 쪽 코드, 결정론·오프라인).

입력: data/evaluatee/cases.json (유일 허용 케이스 메타) + 로컬 corpus의 {ticker}/
  {edgar,xbrl}/ 로컬 사본. 후보 레지스트리(정답지)·scoring/ 접근 금지 (정적 스캔 강제).
출력: 케이스당 페이로드 dict —
  1. case fields (evaluatee_input v1.1의 5필드)
  2. 구조화 재무 시계열: point-in-time XBRL 개념표 (연차 + 분기, filed <= cutoff,
     같은 (태그, 기간)은 컷오프 전 최신 filed 승리) + provenance(accession/filed)
  3. 제출물 연대기: 컷오프 전 EDGAR 제출 인덱스 (form, filingDate)
교란 변형(D8): perturb=True — 사명/티커 익명화 + 화폐값 상수배 재스케일 (케이스별
  결정론 k, 날짜 불변).

look-ahead 통제: 모든 corpus 읽기는 cutoff_guard 벌크 로더를 경유해 레지스트리
컷오프, accession filingDate 대조, 접근 로그를 적용한다. 두 정적 강제 테스트가
우회를 검출하며 fixture 레지스트리는 실제 corpus에 사용할 수 없다.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import math
from pathlib import Path

import cutoff_guard

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALUATEE_CASES = REPO_ROOT / "data" / "evaluatee" / "cases.json"
DATA_DIR = cutoff_guard.DEFAULT_EDGAR_DATA

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


def _case_and_registry(case_or_ticker, cutoff):
    if isinstance(case_or_ticker, dict):
        matches = []
        for path in sorted(EVALUATEE_CASES.parent.glob("cases*.json")):
            cases = json.loads(path.read_text(encoding="utf-8")).get("cases", [])
            if any(case == case_or_ticker for case in cases):
                matches.append(path)
        if len(matches) != 1:
            raise cutoff_guard.CutoffGuardError(
                f"case={case_or_ticker.get('case_id')!r}: 정확히 한 레지스트리에 속하지 않음")
        return case_or_ticker, matches[0]
    raw = json.loads(EVALUATEE_CASES.read_text(encoding="utf-8"))["cases"]
    matches = [case for case in raw if case.get("ticker") == case_or_ticker]
    if len(matches) != 1:
        raise cutoff_guard.CutoffGuardError(f"ticker={case_or_ticker!r}: 정확히 한 케이스가 아님")
    case = matches[0]
    if _iso(case["cutoff_date"]) != _iso(cutoff):
        raise cutoff_guard.CutoffGuardError("호출자 cutoff_date가 레지스트리와 불일치")
    return case, EVALUATEE_CASES


def load_pit_series(case_or_ticker, cutoff: datetime.date, *, data_dir=None,
                    registry_path=None) -> dict:
    """point-in-time XBRL 시계열: filed <= cutoff, (태그, 기간) 최신 filed 승리."""
    data_dir = DATA_DIR if data_dir is None else data_dir
    if isinstance(case_or_ticker, dict) and Path(data_dir).resolve() != cutoff_guard.DEFAULT_EDGAR_DATA.resolve():
        case, default_registry = case_or_ticker, {"cases": [case_or_ticker]}
    else:
        case, default_registry = _case_and_registry(case_or_ticker, cutoff)
    registry_path = ({"cases": [case]} if registry_path is None and
                     Path(data_dir).resolve() != cutoff_guard.DEFAULT_EDGAR_DATA.resolve()
                     else default_registry if registry_path is None else registry_path)
    table: dict[str, dict] = {}
    facts, _ = cutoff_guard.load_xbrl_facts(case["case_id"], case["ticker"], cutoff,
                                             data_dir=data_dir, registry_path=registry_path)
    for row in facts:
        if row["namespace"] == "us-gaap" and row["tag"] in PAYLOAD_TAGS and row["unit"] == MONEY_UNIT:
                tag, f = row["tag"], row["fact"]
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


def load_filing_chronology(case_or_ticker, cutoff: datetime.date, *, data_dir=None,
                           registry_path=None) -> list[dict]:
    """컷오프 전 EDGAR 제출 인덱스 (form, filingDate) — T2 메타신호 채널."""
    data_dir = DATA_DIR if data_dir is None else data_dir
    if isinstance(case_or_ticker, dict) and Path(data_dir).resolve() != cutoff_guard.DEFAULT_EDGAR_DATA.resolve():
        case, default_registry = case_or_ticker, {"cases": [case_or_ticker]}
    else:
        case, default_registry = _case_and_registry(case_or_ticker, cutoff)
    registry_path = ({"cases": [case]} if registry_path is None and
                     Path(data_dir).resolve() != cutoff_guard.DEFAULT_EDGAR_DATA.resolve()
                     else default_registry if registry_path is None else registry_path)
    loaded, _ = cutoff_guard.load_edgar_chronology(case["case_id"], case["ticker"], cutoff,
                                                     data_dir=data_dir, registry_path=registry_path)
    rows = [{"form": r["form"], "filing_date": r["filingDate"]} for r in loaded]
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
    series = load_pit_series(case, cutoff)
    chronology = load_filing_chronology(case, cutoff)
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
