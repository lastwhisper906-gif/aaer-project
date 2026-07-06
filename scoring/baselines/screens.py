"""정량 베이스라인 4종 스크린 (Phase 1 — 채점 쪽 산출물, 피평가자 페이로드 금지).

Beneish M-Score(8변수, 임계 -1.78/-2.22 병기) / Dechow F-Score(Model 1, 임계 1.0/1.4)
/ Montier C-Score(6플래그) / Sloan 발생액.

컷오프 규율 (§5-1, 베이스라인에도 동일 적용):
  - 입력은 data.sec.gov companyfacts 아카이브(~/aaer-data/{ticker}/xbrl/)이며,
    개별 fact는 자신을 보고한 제출물의 filed 날짜를 갖는다.
  - **point-in-time**: filed <= cutoff_date인 fact만 사용한다. 같은 (개념, 기말)의
    값이 여러 제출물에 있으면 컷오프 이전의 '최신 filed'를 취한다 — 시장이 컷오프
    시점에 알고 있던 값(컷오프 전 정정 포함, 컷오프 후 재작성 배제).
  - 결정론: 네트워크 접근·현재 시각 사용 없음. 같은 입력 → 같은 출력.

결측 처리: 유사 태그 폴백 후에도 없으면 해당 변수/스크린을 None + 사유로 보고
(값을 지어내지 않는다). 선택적 구성요소(증권, 우선주 등)만 0 폴백 + 노트.

사용: python scoring/baselines/screens.py T07 T11 ...  (결과: results/{case_id}.json)
"""
from __future__ import annotations

import datetime
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA_DIR = Path.home() / "aaer-data"
RESULTS_DIR = Path(__file__).resolve().parent / "results"
CANDIDATES = REPO / "data" / "candidates" / "candidates.json"

ANNUAL_FORMS = {"10-K", "10-K/A", "10-K405", "10-KT"}

# 개념 → us-gaap 태그 폴백 목록 (앞이 우선). optional=True는 0 폴백 허용.
CONCEPTS = {
    "sales": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
              "SalesRevenueNet", "SalesRevenueGoodsNet", "SalesRevenueServicesNet",
              "RevenueFromContractWithCustomerIncludingAssessedTax"],
    "cogs": ["CostOfGoodsAndServicesSold", "CostOfRevenue", "CostOfGoodsSold",
             "CostOfServices", "CostOfGoodsSoldExcludingDepreciationDepletionAndAmortization"],
    "receivables": ["AccountsReceivableNetCurrent", "ReceivablesNetCurrent",
                    "AccountsNotesAndLoansReceivableNetCurrent", "AccountsReceivableNet"],
    "inventory": ["InventoryNet", "InventoryFinishedGoodsNetOfReserves"],
    "current_assets": ["AssetsCurrent"],
    "total_assets": ["Assets"],
    "ppe_net": ["PropertyPlantAndEquipmentNet"],
    "ppe_gross": ["PropertyPlantAndEquipmentGross"],
    "securities": ["LongTermInvestments", "MarketableSecuritiesNoncurrent",
                   "AvailableForSaleSecuritiesNoncurrent", "OtherLongTermInvestments"],
    "depreciation": ["DepreciationDepletionAndAmortization",
                     "DepreciationAmortizationAndAccretionNet", "Depreciation",
                     "DepreciationAndAmortization"],
    "sga": ["SellingGeneralAndAdministrativeExpense",
            "GeneralAndAdministrativeExpense"],
    "current_liabilities": ["LiabilitiesCurrent"],
    "total_liabilities": ["Liabilities"],
    "lt_debt": ["LongTermDebtNoncurrent", "LongTermDebt",
                "LongTermDebtAndCapitalLeaseObligations", "SecuredLongTermDebt",
                "DebtAndCapitalLeaseObligations"],
    "st_debt": ["LongTermDebtCurrent", "DebtCurrent", "ShortTermBorrowings",
                "LongTermDebtAndCapitalLeaseObligationsCurrent"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue",
             "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
             "CashAndCashEquivalentsAtCarryingValueIncludingDiscontinuedOperations"],
    "st_investments": ["ShortTermInvestments", "MarketableSecuritiesCurrent",
                       "AvailableForSaleSecuritiesCurrent"],
    "preferred": ["PreferredStockValue"],
    "ni": ["NetIncomeLoss", "ProfitLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"],
    "ibx": ["IncomeLossFromContinuingOperationsNetOfTax",
            "IncomeLossFromContinuingOperations", "NetIncomeLoss", "ProfitLoss",
            "NetIncomeLossAvailableToCommonStockholdersBasic"],
    "cfo": ["NetCashProvidedByUsedInOperatingActivities",
            "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
    "issue_stock": ["ProceedsFromIssuanceOfCommonStock",
                    "StockIssuedDuringPeriodValueNewIssues"],
    "issue_debt": ["ProceedsFromIssuanceOfLongTermDebt",
                   "ProceedsFromIssuanceOfDebt", "ProceedsFromNotesPayable"],
}
OPTIONAL_ZERO = {"securities", "st_investments", "preferred", "st_debt",
                 "issue_stock", "issue_debt", "inventory", "lt_debt"}
INSTANT = {"receivables", "inventory", "current_assets", "total_assets", "ppe_net",
           "ppe_gross", "securities", "current_liabilities", "total_liabilities",
           "lt_debt", "st_debt", "cash", "st_investments", "preferred"}


def _iso(s):
    return datetime.date.fromisoformat(s)


def load_facts(ticker: str, cutoff: datetime.date):
    """companyfacts JSON들(다중 CIK 합산) → point-in-time fact 테이블.

    반환: {tag: {end_date: {"val": v, "filed": d, "accn": a, "form": f, "start": s}}}
    같은 (tag, end)는 filed <= cutoff 중 최신 filed 승리 (tie: accn 사전순 최대).
    """
    xbrl_dir = DATA_DIR / ticker / "xbrl"
    files = sorted(xbrl_dir.glob("CIK*.json"))
    if not files:
        raise FileNotFoundError(f"{xbrl_dir}: companyfacts 없음 — tools/fetch_xbrl_facts.py 실행")
    table: dict[str, dict] = {}
    for path in files:
        j = json.loads(path.read_text(encoding="utf-8"))
        gaap = j.get("facts", {}).get("us-gaap", {})
        for tag, body in gaap.items():
            for unit, facts in body.get("units", {}).items():
                if unit != "USD":
                    continue
                for f in facts:
                    filed = _iso(f["filed"])
                    if filed > cutoff:
                        continue  # point-in-time: 컷오프 후 제출분 배제
                    end = _iso(f["end"])
                    start = _iso(f["start"]) if f.get("start") else None
                    # 연차 duration(340~400일) 또는 instant만 채택
                    if start is not None and not (340 <= (end - start).days <= 400):
                        continue
                    slot = table.setdefault(tag, {})
                    prev = slot.get(end)
                    cand = {"val": f["val"], "filed": str(filed), "accn": f.get("accn"),
                            "form": f.get("form"), "start": str(start) if start else None}
                    if prev is None or (cand["filed"], cand["accn"] or "") > (prev["filed"], prev["accn"] or ""):
                        slot[end] = cand
    return table


def fiscal_year_ends(table, cutoff: datetime.date, n=3):
    """연차 기말 후보: 매출/순익 연차 duration의 end들 (최신 n개, 내림차순)."""
    ends = set()
    for concept in ("sales", "ni", "ibx"):
        for tag in CONCEPTS[concept]:
            for end, f in table.get(tag, {}).items():
                if f["start"] is not None:
                    ends.add(end)
    return sorted(ends, reverse=True)[:n]


def get(table, concept, end, prov):
    """개념값 point-in-time 조회. 폴백 태그 순회, 발견 시 provenance 기록."""
    for tag in CONCEPTS[concept]:
        f = table.get(tag, {}).get(end)
        if f is not None:
            prov.setdefault(f"{concept}@{end}", {"tag": tag, **f})
            return float(f["val"])
    if concept in OPTIONAL_ZERO:
        prov.setdefault(f"{concept}@{end}", {"tag": None, "note": "optional missing → 0"})
        return 0.0
    return None


def _div(a, b):
    if a is None or b is None or b == 0:
        return None
    return a / b


def beneish(v_t, v_p, notes):
    """v_t/v_p: 연도 t/t-1 변수 dict. 반환 (변수 dict, M, 결측 목록)."""
    miss = []

    def idx(name, num, den):
        r = _div(num, den)
        if r is None:
            miss.append(name)
        return r

    gm_t = _div((v_t["sales"] - v_t["cogs"]) if None not in (v_t["sales"], v_t["cogs"]) else None, v_t["sales"])
    gm_p = _div((v_p["sales"] - v_p["cogs"]) if None not in (v_p["sales"], v_p["cogs"]) else None, v_p["sales"])
    aq = {}
    for k, v in (("t", v_t), ("p", v_p)):
        if None in (v["current_assets"], v["ppe_net"], v["total_assets"]):
            aq[k] = None
        else:
            aq[k] = 1 - (v["current_assets"] + v["ppe_net"] + v["securities"]) / v["total_assets"]
    ppe_t = v_t["ppe_gross"] if v_t["ppe_gross"] is not None else v_t["ppe_net"]
    ppe_p = v_p["ppe_gross"] if v_p["ppe_gross"] is not None else v_p["ppe_net"]
    if v_t["ppe_gross"] is None or v_p["ppe_gross"] is None:
        notes.append("DEPI: PP&E gross 미보고 → net 대체")
    dep_rate_t = _div(v_t["depreciation"], (v_t["depreciation"] + ppe_t) if None not in (v_t["depreciation"], ppe_t) else None)
    dep_rate_p = _div(v_p["depreciation"], (v_p["depreciation"] + ppe_p) if None not in (v_p["depreciation"], ppe_p) else None)
    lv = {}
    for k, v in (("t", v_t), ("p", v_p)):
        if None in (v["lt_debt"], v["current_liabilities"], v["total_assets"]):
            lv[k] = None
        else:
            lv[k] = (v["lt_debt"] + v["current_liabilities"]) / v["total_assets"]

    variables = {
        "DSRI": idx("DSRI", _div(v_t["receivables"], v_t["sales"]), _div(v_p["receivables"], v_p["sales"])),
        "GMI": idx("GMI", gm_p, gm_t),
        "AQI": idx("AQI", aq["t"], aq["p"]),
        "SGI": idx("SGI", v_t["sales"], v_p["sales"]),
        "DEPI": idx("DEPI", dep_rate_p, dep_rate_t),
        "SGAI": idx("SGAI", _div(v_t["sga"], v_t["sales"]), _div(v_p["sga"], v_p["sales"])),
        "LVGI": idx("LVGI", lv["t"], lv["p"]),
        "TATA": _div((v_t["ibx"] - v_t["cfo"]) if None not in (v_t["ibx"], v_t["cfo"]) else None, v_t["total_assets"]),
    }
    if variables["TATA"] is None:
        miss.append("TATA")
    if miss:
        return variables, None, miss
    m = (-4.84 + 0.920 * variables["DSRI"] + 0.528 * variables["GMI"]
         + 0.404 * variables["AQI"] + 0.892 * variables["SGI"] + 0.115 * variables["DEPI"]
         - 0.172 * variables["SGAI"] + 4.679 * variables["TATA"] - 0.327 * variables["LVGI"])
    return variables, m, miss


def _wc(v):
    if None in (v["current_assets"], v["current_liabilities"]):
        return None
    return (v["current_assets"] - v["cash"] - v["st_investments"]) - (v["current_liabilities"] - v["st_debt"])


def _nco(v):
    if None in (v["total_assets"], v["current_assets"], v["total_liabilities"], v["current_liabilities"]):
        return None
    return ((v["total_assets"] - v["current_assets"] - v["securities"])
            - (v["total_liabilities"] - v["current_liabilities"] - (v["lt_debt"] or 0)))


def _fin(v):
    if v["lt_debt"] is None:
        return None
    return (v["st_investments"] + v["securities"]) - (v["lt_debt"] + v["st_debt"] + v["preferred"])


def dechow_f(v_t, v_p, v_pp, notes):
    """Dechow et al. (2011) Model 1. v_pp(t-2)는 avg assets 계산용 — 없으면 근사+노트."""
    miss = []
    ta_t, ta_p = v_t["total_assets"], v_p["total_assets"]
    ta_pp = v_pp["total_assets"] if v_pp else None
    if None in (ta_t, ta_p):
        return None, None, ["total_assets"]
    avg_t = (ta_t + ta_p) / 2
    if ta_pp is not None:
        avg_p = (ta_p + ta_pp) / 2
    else:
        avg_p = ta_p
        notes.append("F-score: t-2 총자산 결측 → avg assets(t-1) = TA(t-1) 근사")

    def delta(f):
        a, b = f(v_t), f(v_p)
        return None if None in (a, b) else a - b

    rsst_num = None
    d_wc, d_nco, d_fin = delta(_wc), delta(_nco), delta(_fin)
    if None not in (d_wc, d_nco, d_fin):
        rsst_num = d_wc + d_nco + d_fin
    variables = {
        "rsst_acc": _div(rsst_num, avg_t),
        "ch_rec": _div((v_t["receivables"] - v_p["receivables"]) if None not in (v_t["receivables"], v_p["receivables"]) else None, avg_t),
        "ch_inv": _div((v_t["inventory"] - v_p["inventory"]), avg_t),
        "soft_assets": _div((ta_t - (v_t["ppe_net"] or 0) - (v_t["cash"] or 0)), ta_t) if v_t["ppe_net"] is not None and v_t["cash"] is not None else None,
        "ch_cs": None,
        "ch_roa": None,
        "issue": 1.0 if (v_t["issue_stock"] or v_t["issue_debt"]) else 0.0,
    }
    cs_t = (v_t["sales"] - (v_t["receivables"] - v_p["receivables"])) if None not in (v_t["sales"], v_t["receivables"], v_p["receivables"]) else None
    # 현금매출 변화율: t-1 현금매출은 ΔAR(t-1) 필요 → t-2 AR. 결측 시 매출 근사.
    if v_pp and None not in (v_p["sales"], v_p["receivables"]) and v_pp.get("receivables") is not None:
        cs_p = v_p["sales"] - (v_p["receivables"] - v_pp["receivables"])
    elif v_p["sales"] is not None:
        cs_p = v_p["sales"]
        notes.append("F-score: t-2 AR 결측 → t-1 현금매출 = 매출 근사")
    else:
        cs_p = None
    variables["ch_cs"] = _div((cs_t - cs_p) if None not in (cs_t, cs_p) else None, cs_p)
    roa_t = _div(v_t["ibx"], avg_t)
    roa_p = _div(v_p["ibx"], avg_p)
    if None not in (roa_t, roa_p):
        variables["ch_roa"] = roa_t - roa_p
    miss = [k for k, v in variables.items() if v is None]
    if miss:
        return variables, None, miss
    pv = (-7.893 + 0.790 * variables["rsst_acc"] + 2.518 * variables["ch_rec"]
          + 1.191 * variables["ch_inv"] + 1.979 * variables["soft_assets"]
          + 0.171 * variables["ch_cs"] - 0.932 * variables["ch_roa"] + 1.029 * variables["issue"])
    prob = math.exp(pv) / (1 + math.exp(pv))
    return variables, prob / 0.0037, miss  # 무조건부 확률 0.37%로 정규화한 F-score


def montier_c(v_t, v_p):
    """6플래그 합. 판정 불능 플래그는 None(합산 제외)로 보고."""
    def flag(cond):
        return None if cond is None else int(cond)

    def cmp_ratio(num_t, den_t, num_p, den_p, direction=1):
        r_t, r_p = _div(num_t, den_t), _div(num_p, den_p)
        if None in (r_t, r_p):
            return None
        return (r_t > r_p) if direction == 1 else (r_t < r_p)

    ni_cfo_t = _div((v_t["ni"] - v_t["cfo"]) if None not in (v_t["ni"], v_t["cfo"]) else None, v_t["total_assets"])
    ni_cfo_p = _div((v_p["ni"] - v_p["cfo"]) if None not in (v_p["ni"], v_p["cfo"]) else None, v_p["total_assets"])
    oca_t = (v_t["current_assets"] - (v_t["receivables"] or 0) - (v_t["inventory"] or 0) - (v_t["cash"] or 0)) if v_t["current_assets"] is not None else None
    oca_p = (v_p["current_assets"] - (v_p["receivables"] or 0) - (v_p["inventory"] or 0) - (v_p["cash"] or 0)) if v_p["current_assets"] is not None else None
    ppe_t = v_t["ppe_gross"] if v_t["ppe_gross"] is not None else v_t["ppe_net"]
    ppe_p = v_p["ppe_gross"] if v_p["ppe_gross"] is not None else v_p["ppe_net"]
    growth = _div(v_t["total_assets"], v_p["total_assets"])
    flags = {
        "c1_ni_cfo_divergence": flag(None if None in (ni_cfo_t, ni_cfo_p) else ni_cfo_t > ni_cfo_p),
        "c2_dso_up": flag(cmp_ratio(v_t["receivables"], v_t["sales"], v_p["receivables"], v_p["sales"])),
        "c3_dsi_up": flag(cmp_ratio(v_t["inventory"], v_t["sales"], v_p["inventory"], v_p["sales"])),
        "c4_oca_up": flag(cmp_ratio(oca_t, v_t["sales"], oca_p, v_p["sales"])),
        "c5_dep_down": flag(cmp_ratio(v_t["depreciation"], ppe_t, v_p["depreciation"], ppe_p, direction=-1)),
        "c6_asset_growth": flag(None if growth is None else growth - 1 > 0.10),
    }
    known = [v for v in flags.values() if v is not None]
    return flags, (sum(known) if known else None), [k for k, v in flags.items() if v is None]


def sloan(v_t, v_p):
    if None in (v_t["ni"], v_t["cfo"], v_t["total_assets"], v_p["total_assets"]):
        return None
    return (v_t["ni"] - v_t["cfo"]) / ((v_t["total_assets"] + v_p["total_assets"]) / 2)


def run_case(case: dict) -> dict:
    ticker = case["ticker"].split("/")[0]
    cutoff = _iso(case["cutoff_date"])
    notes: list[str] = []
    prov: dict = {}
    table = load_facts(ticker, cutoff)
    ends = fiscal_year_ends(table, cutoff)
    result = {
        "case_id": case["case_id"], "ticker": ticker, "cutoff_date": str(cutoff),
        "fiscal_year_ends_used": [str(e) for e in ends],
        "point_in_time_rule": "facts with filed <= cutoff only; latest filed wins per (tag, period-end)",
    }
    if len(ends) < 2:
        result["error"] = f"컷오프 전 연차 XBRL 기간 {len(ends)}개 — 스크린 계산 불능 (연차 2개 필요)"
        result["notes"] = notes
        return result
    years = []
    for end in ends[:3]:
        years.append({c: get(table, c, end, prov) for c in CONCEPTS})
    v_t, v_p = years[0], years[1]
    v_pp = years[2] if len(years) > 2 else None

    b_vars, m, b_miss = beneish(v_t, v_p, notes)
    f_vars, f, f_miss = dechow_f(v_t, v_p, v_pp, notes)
    c_flags, c, c_miss = montier_c(v_t, v_p)
    s = sloan(v_t, v_p)

    result.update({
        "beneish": {"variables": b_vars, "m_score": m, "missing": b_miss,
                    "flag_minus_1_78": None if m is None else m > -1.78,
                    "flag_minus_2_22": None if m is None else m > -2.22},
        "dechow_f": {"variables": f_vars, "f_score": f, "missing": f_miss,
                     "flag_1_0": None if f is None else f > 1.0,
                     "flag_1_4": None if f is None else f > 1.4},
        "montier_c": {"flags": c_flags, "c_score": c, "undetermined": c_miss,
                      "flag_ge_4": None if c is None else c >= 4},
        "sloan_accruals": {"value": s,
                           "flag_gt_0_10": None if s is None else abs(s) > 0.10,
                           "convention": "|accruals/avgTA| > 0.10 (상위 십분위 관행 근사)"},
        "notes": notes,
        "provenance": prov,
    })
    return result


def main() -> int:
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))["candidates"]
    by_id = {c["case_id"]: c for c in candidates}
    ids = sys.argv[1:] or sorted(by_id)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    for cid in ids:
        if cid not in by_id:
            print(f"{cid}: 미등록")
            continue
        try:
            r = run_case(by_id[cid])
        except FileNotFoundError as e:
            print(f"{cid}: {e}")
            continue
        (RESULTS_DIR / f"{cid}.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        m = r.get("beneish", {}).get("m_score")
        f = r.get("dechow_f", {}).get("f_score")
        c = r.get("montier_c", {}).get("c_score")
        s = r.get("sloan_accruals", {}).get("value")
        fmt = lambda x, p=3: "N/A" if x is None else f"{x:.{p}f}"  # noqa: E731
        print(f"{cid} {r['ticker']:5s} M={fmt(m)} F={fmt(f,2)} C={c if c is not None else 'N/A'} "
              f"Sloan={fmt(s)} ends={r.get('fiscal_year_ends_used', [])[:2]} "
              f"{'ERROR: ' + r['error'] if 'error' in r else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
