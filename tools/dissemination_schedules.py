"""FINRA 공표일(dissemination/publication date) 실측 재구성 — Q-M02 구현 (D71).

analysis/DISSEMINATION_DATES_MEMO.md §3 계획의 실행체. 두 하위 명령:

  .venv/bin/python tools/dissemination_schedules.py fetch   # Wayback 스냅샷 → ~/aaer-data/finra_schedules/ (체크섬 로그)
  .venv/bin/python tools/dissemination_schedules.py build   # 아카이브 HTML → data/finra_dissemination/dissemination_dates.json

결정론: build는 아카이브 파일 집합이 같으면 출력 바이트 동일 (타임스탬프 0).
검증 4중:
  (1) 셀 요일명 == 추론 날짜의 실제 요일 (연도 추론 체크섬)
  (2) 스냅샷 간 중복 연도 테이블 cross-check (전 행 대조)
  (3) 산술 가드: settlement < publication ≤ settlement+30일
  (4) 커버리지 대조: ~/aaer-data/short_interest/shrt*.csv 결제일 전수 매핑 존재

불일치 해소 규칙 (전부 2026-07-13 실측 사례로 사전 등록 — 재량 0):
  규칙 1 (weekday_typo_outvoted): 요일 체크섬 실패 행은 같은 결제일의
    self-consistent 행이 있으면 그 행이 정본 (실증: 2025-04-15 공표일
    'April 25 (Thursday)' → 후속 스냅샷 'April 25 (Friday)' 교정 — 날짜 정본).
  규칙 2 (revision_latest_wins): self-consistent 행 간 공표일 충돌은 최신
    스냅샷 우선 — 사건 후 스냅샷 = 실현된 일정 (실증: 2021-12-15 공표
    12-24(휴장일) → 12-27 연중 개정).
  규칙 3 (weekday_typo_all_sources_plus7): 전 스냅샷이 동일 오탈 요일이면
    날짜 만장일치 AND due+7일==publication 패턴일 때만 날짜 채택 (실증:
    2026-12-31 행 — 요일 라벨이 전년 행 복제, 날짜는 패턴 정합).
  그 외 전부: 정지 (exit 2) — 수동 검토 없이 진행 불가.

네트워크는 fetch만 (web.archive.org) — build·소비 경로는 네트워크 0.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import html as ht
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ARCHIVE_DIR = Path.home() / "aaer-data" / "finra_schedules"
OUT_JSON = REPO / "data" / "finra_dissemination" / "dissemination_dates.json"
SI_DIR = Path.home() / "aaer-data" / "short_interest"

MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
            "Saturday", "Sunday"]

# 스냅샷 정본 목록 (사전 등록 — 추가는 신규 D-엔트리). 연도별 전체 테이블 +
# 중복 연도 cross-check + 오탈 다수결용 동년 추가 스냅샷.
SNAPSHOTS = {
    "20180111_si.html": "https://web.archive.org/web/20180111063824/http://www.finra.org/industry/short-interest/short-interest-reporting-due-dates",
    "20190121_si.html": "https://web.archive.org/web/20190121104853/http://www.finra.org/industry/short-interest/short-interest-reporting-due-dates",
    "20200718_si.html": "https://web.archive.org/web/20200718232030/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest",
    "20210116_si.html": "https://web.archive.org/web/20210116171648/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest",
    "20220317_si.html": "https://web.archive.org/web/20220317120000/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest",
    "20230127_si.html": "https://web.archive.org/web/20230127120000/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest",
    "20240320_si.html": "https://web.archive.org/web/20240320120000/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest",
    "20250114_si.html": "https://web.archive.org/web/20250114120000/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest",
    "20250601_si.html": "https://web.archive.org/web/20250601120000/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest",
    "20251001_si.html": "https://web.archive.org/web/20251001120000/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest",
    "20260118_si.html": "https://web.archive.org/web/20260118120000/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest",
    "20260401_si.html": "https://web.archive.org/web/20260401120000/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest",
    "20260701_si.html": "https://web.archive.org/web/20260701120000/https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest",
}
MAX_DELAY_DAYS = 30  # 산술 가드 상한 (관측 9~12일의 여유 배수)


class DisseminationError(Exception):
    """fail-closed: 파싱 불능·해소 불능 불일치·커버리지 구멍."""


# ---------------------------------------------------------------- fetch

def fetch(archive_dir: Path = ARCHIVE_DIR) -> dict:
    """스냅샷 아카이브 — 멱등 (기존 파일 유지), 체크섬 로그 append."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    got, skipped = [], []
    for fname, url in sorted(SNAPSHOTS.items()):
        path = archive_dir / fname
        if path.is_file():
            skipped.append(fname)
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "aaer-evals research (Q-M02/D71)"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        if b"Settlement" not in data:
            raise DisseminationError(f"{fname}: 일정표 마커 부재 — 스냅샷 검증 실패")
        tmp = path.with_suffix(".html.part")
        tmp.write_bytes(data)
        tmp.rename(path)
        rec = {"file": fname, "url": url, "bytes": len(data),
               "sha256": hashlib.sha256(data).hexdigest()}
        with (archive_dir / "checksums.log").open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        got.append(fname)
    return {"fetched": got, "kept": skipped}


# ---------------------------------------------------------------- parse

def _cell_texts(fragment: str) -> list[str]:
    cells = re.findall(r"<t[dh].*?</t[dh]>", fragment, re.S)
    return [ht.unescape(re.sub(r"<[^>]+>", "", c)).replace("\xa0", " ").strip()
            for c in cells]


def _parse_cell(text: str):
    """'September 29\\n\\tFriday' → (month, day, weekday|None). 시각 표기 제거."""
    text = re.sub(r"–.*?p\.m\.", "", text)
    m = re.search(r"([A-Z][a-z]+)\s+(\d{1,2})", text)
    if not m or m.group(1) not in MONTHS:
        return None
    wd = next((w for w in WEEKDAYS if w in text), None)
    return MONTHS[m.group(1)], int(m.group(2)), wd


def _infer_date(month, day, weekday, table_year, anchor_month):
    """테이블 연도 + 12월→1월 롤오버. 반환 (date, weekday_ok) — 요일은 체크섬."""
    year = table_year + 1 if (anchor_month == 12 and month == 1) else table_year
    d = datetime.date(year, month, day)
    ok = (weekday is None) or (WEEKDAYS[d.weekday()] == weekday)
    return d, ok


def parse_snapshot(path: Path) -> dict[str, list[dict]]:
    """스냅샷 1개 → {settlement_iso: [후보 행]} — 연도 헤딩('YYYY Short Interest
    Reporting Dates')이 지배, 헤딩 없는 테이블은 무시."""
    h = path.read_text(encoding="utf-8", errors="replace")
    out: dict[str, list[dict]] = {}
    current_year = None
    for m in re.finditer(r"(<h[1-4][^>]*>.*?</h[1-4]>)|(<table.*?</table>)", h, re.S):
        if m.group(1):
            txt = ht.unescape(re.sub(r"<[^>]+>", "", m.group(1))).replace("\xa0", " ")
            ym = re.search(r"(20\d\d)\s*Short Interest Reporting Dates", txt)
            if ym:
                current_year = int(ym.group(1))
            continue
        if current_year is None:
            continue
        rows = re.findall(r"<tr.*?</tr>", m.group(2), re.S)
        if not rows or not any("Settlement" in c for c in _cell_texts(rows[0])):
            continue
        for r in rows[1:]:
            cells = _cell_texts(r)
            if len(cells) != 3:
                continue
            ps, pd_, pp = (_parse_cell(c) for c in cells)
            if not (ps and pp):
                continue
            settle, s_ok = _infer_date(ps[0], ps[1], ps[2], current_year, anchor_month=0)
            due, d_ok = (_infer_date(pd_[0], pd_[1], pd_[2], current_year,
                                     anchor_month=ps[0]) if pd_ else (None, True))
            pub, p_ok = _infer_date(pp[0], pp[1], pp[2], current_year, anchor_month=ps[0])
            if pub <= settle or (pub - settle).days > MAX_DELAY_DAYS:
                raise DisseminationError(f"산술 가드: {settle} → {pub} ({path.name})")
            out.setdefault(settle.isoformat(), []).append({
                "publication": pub.isoformat(),
                "due": due.isoformat() if due else None,
                "table_year": current_year,
                "source": path.name,
                "weekday_ok": s_ok and d_ok and p_ok,
            })
    return out


def merge(candidates: dict[str, list[dict]]):
    """규칙 1~3 병합 — 해소 불능은 예외 (fail-closed)."""
    merged, discrepancies, conflicts = {}, [], []
    for k in sorted(candidates):
        vs = candidates[k]
        good = [v for v in vs if v["weekday_ok"]]
        bad = [v for v in vs if not v["weekday_ok"]]
        if good:
            pubs = sorted({v["publication"] for v in good})
            if len(pubs) > 1:
                latest = max(good, key=lambda v: v["source"])  # 규칙 2
                discrepancies.append({
                    "settlement": k, "rule": "revision_latest_wins",
                    "resolved_publication": latest["publication"],
                    "superseded_publications": sorted(
                        {v["publication"] for v in good
                         if v["publication"] != latest["publication"]}),
                    "sources": sorted({v["source"] for v in good})})
                pool = [latest]
            else:
                pool = good
            rec = dict(pool[0])
            rec["cross_checked_by"] = sorted({v["source"] for v in pool})
            if bad:  # 규칙 1
                rec["weekday_typo_in"] = sorted({v["source"] for v in bad})
                discrepancies.append({
                    "settlement": k, "rule": "weekday_typo_outvoted",
                    "resolved_publication": rec["publication"],
                    "typo_sources": rec["weekday_typo_in"],
                    "typo_publications": sorted({v["publication"] for v in bad})})
        else:  # 규칙 3
            pubs = sorted({v["publication"] for v in vs})
            dues = sorted({v["due"] for v in vs if v["due"]})
            plus7 = (len(pubs) == 1 and len(dues) == 1
                     and (datetime.date.fromisoformat(pubs[0])
                          - datetime.date.fromisoformat(dues[0])).days == 7)
            if not plus7:
                conflicts.append((k, "요일 체크섬 통과 0 + due+7 패턴 불성립", vs))
                continue
            rec = dict(vs[0])
            rec["cross_checked_by"] = sorted({v["source"] for v in vs})
            rec["weekday_typo_all_sources"] = True
            discrepancies.append({
                "settlement": k, "rule": "weekday_typo_all_sources_plus7",
                "resolved_publication": pubs[0],
                "sources": rec["cross_checked_by"]})
        rec.pop("source", None)
        rec.pop("weekday_ok", None)
        rec["delay_days"] = (datetime.date.fromisoformat(rec["publication"])
                             - datetime.date.fromisoformat(k)).days
        merged[k] = rec
    if conflicts:
        raise DisseminationError(f"해소 불능 불일치 {len(conflicts)}건: {conflicts}")
    return merged, discrepancies


def archive_coverage_check(merged: dict, si_dir: Path = SI_DIR) -> list[str]:
    """검증 4: SI 아카이브 결제일 전수가 매핑에 존재해야 한다."""
    missing = []
    for p in sorted(si_dir.glob("shrt*.csv")):
        ymd = p.stem[len("shrt"):]
        iso = f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:]}"
        if iso not in merged:
            missing.append(iso)
    return missing


def build(archive_dir: Path = ARCHIVE_DIR, out_json: Path = OUT_JSON,
          si_dir: Path = SI_DIR) -> dict:
    candidates: dict[str, list[dict]] = {}
    for fname in sorted(SNAPSHOTS):
        p = archive_dir / fname
        if not p.is_file():
            raise DisseminationError(f"{fname} 아카이브 부재 — 먼저 fetch")
        for k, vs in parse_snapshot(p).items():
            candidates.setdefault(k, []).extend(vs)
    merged, discrepancies = merge(candidates)
    missing = archive_coverage_check(merged, si_dir)
    if missing:
        raise DisseminationError(f"SI 아카이브 결제일 매핑 구멍 {len(missing)}건: {missing}")
    delays = sorted({v["delay_days"] for v in merged.values()})
    out = {
        "_provenance": {
            "spec": "specs/B4_short_interest.md §2 개정 (D71) — LAG=14 상수의 실측 대체",
            "method": ("Wayback 연도별 스냅샷 파싱 — 요일명 체크섬·중복 연도 "
                       "cross-check·규칙 1~3 (모듈 docstring)·SI 아카이브 전수 대조"),
            "snapshots": SNAPSHOTS,
            "column_name_history": "Exchange Receipt Date (~2021) → Publication Date (2022~)",
            "delay_days_observed": delays,
            "lag14_conservative_in_sample": all(d <= 14 for d in delays),
        },
        "_discrepancies": discrepancies,
        "settlement_to_publication": merged,
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1)
                        + "\n", encoding="utf-8")
    return {"rows": len(merged), "range": [min(merged), max(merged)],
            "delays": delays, "discrepancies": len(discrepancies)}


def load_map(out_json: Path = OUT_JSON) -> dict[str, str]:
    """소비자용 평탄 매핑 {settlement_iso: publication_iso}. 파일 부재 = 예외
    (LAG 폴백은 스펙상 '매핑에 없는 결제일'에만 허용 — 파일 자체 부재는 구성 오류)."""
    data = json.loads(out_json.read_text(encoding="utf-8"))
    return {k: v["publication"]
            for k, v in data["settlement_to_publication"].items()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=("fetch", "build"))
    args = ap.parse_args()
    if args.cmd == "fetch":
        r = fetch()
        print(f"fetch: 신규 {len(r['fetched'])} · 기존 유지 {len(r['kept'])}")
    else:
        r = build()
        print(f"build: {r['rows']}행 {r['range'][0]}→{r['range'][1]} · "
              f"지연 {r['delays']}일 · 불일치 해소 기록 {r['discrepancies']}건")
        print(f"→ {OUT_JSON.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
