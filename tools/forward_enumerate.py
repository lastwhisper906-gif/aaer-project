"""forward 유니버스 결정론 열거 (UNIVERSE_SELECTION.md §1–§3·§5·§6, D100).

usage: python tools/forward_enumerate.py --out forward/cycle_001/universe.json
재실행(결정론 검증): 동일 명령 — 동일 T₀ 스냅샷( data/candidates/universe/ )이
있으면 네트워크 없이 재계산한다 (--offline 강제 가능).

권한: governance/DECISION_FORWARD_UNIVERSE.md §5 (owner plan 2026-07-20
§4.4/§8 서면 위임). 원시 응답 전건 보존 + provenance(질의 URL·시각) 기록.
네트워크는 EDGAR 공개 API만 (무료) · 모델 호출 0 · 레이트 ≤4 req/s.

기계 판독 주석 (§1-3): "companyfacts에 XBRL 사실이 있는 제출"은 EDGAR
submissions의 공식 isXBRL 플래그로 판독한다 (companyfacts 전건 fetch 대비
등가·경량 — 방법은 universe.json.method에 기록).
"""
import argparse
import datetime
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_common import (REPO, SEC_UA, UNIVERSE_SIZE, assert_subscription_only,
                            write_json, read_json)

SIC_SET = ["3571", "3572", "3576", "3577", "3585", "3612", "3613", "3621",
           "3661", "3663", "3669", "3672", "3674", "4911"]  # §6 (A) — 정렬 고정
SNAP = REPO / "data/candidates/universe"
T0 = "2026-07-20"                      # 열거 시점 (서명 후 첫 실행일 — D95→plan 위임)
TRAIL_START = "2024-07-20"             # T₀ − 24개월 (§1-1)
FLOAT_MIN = 1e9

_provenance = []


def fetch(url: str, dest: Path, offline: bool) -> bytes | None:
    if dest.exists():
        return dest.read_bytes()
    if offline:
        return None
    req = urllib.request.Request(url, headers=SEC_UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
    except Exception as e:  # 404 등 — 결측 기록 (fail-closed)
        _provenance.append({"url": url, "retrieved_at": _now(), "error": str(e)[:120]})
        dest.with_suffix(dest.suffix + ".missing").write_text(str(e)[:200], encoding="utf-8")
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    _provenance.append({"url": url, "retrieved_at": _now(), "file": str(dest.relative_to(REPO))})
    time.sleep(0.3)  # SEC fair-access <5 req/s
    return data


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def browse_ciks(sic: str, offline: bool) -> list[tuple[str, str]]:
    """SIC별 활동 등록사 (트레일링 24개월 내 10-K 제출 필터) — (cik, name)."""
    out, start = [], 0
    while True:
        url = ("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany"
               f"&SIC={sic}&type=10-K&datea={TRAIL_START.replace('-', '')}"
               f"&owner=include&count=100&start={start}&output=atom")
        data = fetch(url, SNAP / f"sic_{sic}_p{start // 100}.xml", offline)
        if data is None:
            break
        text = data.decode("utf-8", "replace")
        # company-list atom: 항목당 <cik>NNNNNNNNNN</cik> (사명은 submissions에서)
        ciks = re.findall(r"<cik>(\d+)</cik>", text)
        out.extend((c.zfill(10), "") for c in ciks)
        if len(ciks) < 100:
            break
        start += 100
    return out


def cycle1_ciks() -> set[str]:
    """자기 오염 제외 (§2-2): Cycle-1 케이스 세트 전건의 CIK."""
    ciks = set()
    for f in ["cases.json", "cases_wave2.json", "cases_holdout.json",
              "cases_holdout_controls.json"]:
        p = REPO / "data/evaluatee" / f
        if p.exists():
            for c in read_json(p).get("cases", []):
                if c.get("cik"):
                    ciks.add(str(c["cik"]).zfill(10))
    return ciks


def check_candidate(cik: str, offline: bool) -> tuple[str, dict | None]:
    """(사유 | 'ok', 상세) — §1·§2 기계 판정."""
    data = fetch(f"https://data.sec.gov/submissions/CIK{cik}.json",
                 SNAP / f"submissions_CIK{cik}.json", offline)
    if data is None:
        return "missing_data", None
    sub = json.loads(data)
    recent = sub.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    items = recent.get("items", [""] * len(forms))
    xbrl = recent.get("isXBRL", [0] * len(forms))

    if any(f in ("20-F", "40-F", "6-K") for f in forms):
        return "foreign_filer", None
    in_trail = [i for i, d in enumerate(dates) if d >= TRAIL_START]
    k_recent = sum(1 for i in in_trail if forms[i] == "10-K")
    q_recent = sum(1 for i in in_trail if forms[i] == "10-Q")
    if k_recent < 1 or q_recent < 2:
        return "form_requirement", None
    if any(forms[i] == "8-K" and "4.02" in (items[i] or "") for i in in_trail):
        return "contamination_402_posthoc_track", None
    xb_all = [i for i, f in enumerate(forms) if f in ("10-K", "10-Q") and xbrl[i]]
    xb_k = sum(1 for i in xb_all if forms[i] == "10-K")
    if len(xb_all) < 8 or xb_k < 2:
        return "xbrl_history", None

    fdata = fetch(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/dei/EntityPublicFloat.json",
                  SNAP / f"float_CIK{cik}.json", offline)
    if fdata is None:
        return "missing_data", None
    try:
        facts = [u for u in json.loads(fdata)["units"]["USD"] if u.get("end") <= T0]
        latest = max(facts, key=lambda u: u["end"])
    except (KeyError, ValueError):
        return "missing_data", None
    if latest["val"] < FLOAT_MIN:
        return "float_below_1b", None
    return "ok", {"float_usd": latest["val"], "float_asof": latest["end"],
                  "sic": str(sub.get("sic", "")), "name": sub.get("name", ""),
                  "ticker": (sub.get("tickers") or [""])[0]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="forward/cycle_001/universe.json")
    ap.add_argument("--offline", action="store_true",
                    help="스냅샷만으로 재계산 (결정론 검증)")
    args = ap.parse_args()
    assert_subscription_only()
    SNAP.mkdir(parents=True, exist_ok=True)

    burned = cycle1_ciks()
    seen, buckets, excluded = set(), {s: [] for s in SIC_SET}, {}
    candidates = 0
    for sic in SIC_SET:
        for cik, _name in browse_ciks(sic, args.offline):
            if cik in seen:
                continue
            seen.add(cik)
            candidates += 1
            if cik in burned:
                excluded["cycle1_self_contamination"] = excluded.get(
                    "cycle1_self_contamination", 0) + 1
                continue
            reason, info = check_candidate(cik, args.offline)
            if reason != "ok":
                excluded[reason] = excluded.get(reason, 0) + 1
                continue
            buckets[sic].append({"cik": cik, **info, "browse_sic": sic})

    for sic in SIC_SET:  # float 내림차순 · 동률 CIK 오름차순 (§3)
        buckets[sic].sort(key=lambda r: (-r["float_usd"], r["cik"]))
    order = []            # 버킷 라운드로빈 (SIC 오름차순 고정)
    rank = 0
    while any(buckets.values()):
        for sic in SIC_SET:
            if buckets[sic]:
                r = buckets[sic].pop(0)
                rank += 1
                r["selection_rank"] = rank
                order.append(r)
    selected = order[:UNIVERSE_SIZE]
    for i, r in enumerate(selected, 1):
        r["record_id"] = f"fw001-r{i:02d}"
    alternates = order[UNIVERSE_SIZE:]

    universe = {
        "rule_ref": "docs/UNIVERSE_SELECTION.md#§6",
        "decision_ref": "governance/DECISION_FORWARD_UNIVERSE.md",
        "enumerated_at": T0,
        "trailing_window_start": TRAIL_START,
        "candidate_count": candidates,
        "excluded_by_reason": excluded,
        "selected": selected,
        "alternates": alternates,
        "method": {
            "browse": "browse-edgar SIC + type=10-K + datea=trailing-24mo (활동 필터)",
            "xbrl_history": "submissions.isXBRL 플래그 판독 (§1-3 기계 판독 주석)",
            "float": "companyconcept dei/EntityPublicFloat 최신(end ≤ T0)",
            "rerun": "python tools/forward_enumerate.py --offline (스냅샷 결정론 재계산)",
        },
    }
    write_json(REPO / args.out, universe)
    if _provenance:
        prov_path = SNAP / "provenance.json"
        old = read_json(prov_path) if prov_path.exists() else []
        write_json(prov_path, old + _provenance)
    print(f"OK — candidates {candidates} · selected {len(selected)} · "
          f"alternates {len(alternates)} · excluded {excluded}")
    print("selected:", ", ".join(f"{r['ticker'] or r['cik']}({r['browse_sic']})"
                                 for r in selected))
    return 0 if len(selected) == UNIVERSE_SIZE else 1


if __name__ == "__main__":
    sys.exit(main())
