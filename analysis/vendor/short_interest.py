"""FINRA Consolidated Short Interest — downloader / parser / PIT aligner / B4 scorer.

Canonical implementation (aaer-evals D52, specs/B4_short_interest.md). The aaer-evals
repo carries a byte-identical vendored snapshot (analysis/vendor/short_interest.py,
reverse of this repo's vendor/aaer_evals convention) — edit HERE, then re-export.

Design constraints:
  - stdlib only, no intra-package imports (so the snapshot imports cleanly anywhere).
  - PIT rule: a settlement-date-t report enters features iff t + LAG_DAYS <= cutoff
    (LAG_DAYS = 14 calendar days, pre-registered conservative dissemination lag;
    replacing it with measured dissemination dates requires a spec amendment first).
  - First-disseminated value: settlement t is read from file shrt{t}.csv only;
    later-file revisions (revisionFlag=R) are counted as a diagnostic, never applied.
  - fail-closed: missing file / missing symbol / missing denominator -> flags and
    None scores, never imputation. Network fetch happens only in download_range();
    scoring functions never touch the network.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import statistics
import urllib.error
import urllib.request
from pathlib import Path

CDN_URL = "https://cdn.finra.org/equity/otcmarket/biweekly/shrt{ymd}.csv"
LAG_DAYS = 14                 # settlement -> dissemination, conservative (spec §2)
TRAILING_DAYS = 365           # abnormal-SI median window (spec §3)
MIN_TRAILING_REPORTS = 12     # of ~24 possible bi-monthly reports
SLOPE_REPORTS = 4             # trailing reports for the slope term
SHARES_FRESHNESS_DAYS = 400   # denominator instant fact: t-400 <= end <= t
SHARES_TAG = "dei:EntityCommonStockSharesOutstanding"
DATA_FLOOR = datetime.date(2017, 12, 29)  # earliest FINRA partition (probed 2026-07-13)
HEADER_PREFIX = "accountingYearMonthNumber|symbolCode|issueName"


class ShortInterestError(Exception):
    """fail-closed: bad file, bad header, unusable arguments."""


# ---------------------------------------------------------------- discovery

def _month_end(year: int, month: int) -> datetime.date:
    nxt = datetime.date(year + month // 12, month % 12 + 1, 1)
    return nxt - datetime.timedelta(days=1)


def settlement_targets(start: datetime.date, end: datetime.date) -> list[datetime.date]:
    """Bi-monthly target dates (15th + month-end) in [start, end]; actual settlement
    dates are found by probing backward from each target (business-day adjustment)."""
    targets = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        for cand in (datetime.date(y, m, 15), _month_end(y, m)):
            if start <= cand <= end:
                targets.append(cand)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return targets


# ---------------------------------------------------------------- download

def _fetch(url: str, user_agent: str, timeout: int = 60) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def download_settlement(target: datetime.date, dest_dir: Path, user_agent: str,
                        max_backoff_days: int = 6) -> Path | None:
    """Probe target date then backward up to max_backoff_days for the real
    settlement file. Existing verified file short-circuits (resumable batch).
    Returns the archived path, or None if the half-month has no file."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    for back in range(0, max_backoff_days + 1):
        day = target - datetime.timedelta(days=back)
        if day.weekday() >= 5:  # settlement dates are business days
            continue
        path = dest_dir / f"shrt{day.strftime('%Y%m%d')}.csv"
        if path.is_file():
            _verify_header(path)
            return path
        data = _fetch(CDN_URL.format(ymd=day.strftime("%Y%m%d")), user_agent)
        if data is None:
            continue
        head = data[:200].decode("utf-8", errors="replace")
        if not head.startswith(HEADER_PREFIX):
            raise ShortInterestError(f"unexpected header for {day}: {head[:80]!r}")
        tmp = path.with_suffix(".csv.part")
        tmp.write_bytes(data)
        tmp.rename(path)
        _log_checksum(dest_dir, path, data)
        return path
    return None


def _log_checksum(dest_dir: Path, path: Path, data: bytes) -> None:
    rec = {"file": path.name, "url": CDN_URL.format(ymd=path.stem[len("shrt"):]),
           "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    with (dest_dir / "checksums.log").open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def download_range(start: datetime.date, end: datetime.date, dest_dir: Path,
                   user_agent: str) -> dict:
    """Archive every bi-monthly settlement file in [start, end]. Resumable:
    already-archived files are kept. Returns {found: [...], missing_halfmonths: [...]}."""
    found, missing = [], []
    for target in settlement_targets(start, end):
        path = download_settlement(target, dest_dir, user_agent)
        if path is None:
            if target >= DATA_FLOOR:
                missing.append(str(target))  # never silently skipped
        else:
            found.append(path.name)
    return {"found": sorted(set(found)), "missing_halfmonths": missing}


# ---------------------------------------------------------------- parse / align

def _verify_header(path: Path) -> None:
    with path.open(encoding="utf-8") as f:
        if not f.readline().startswith(HEADER_PREFIX):
            raise ShortInterestError(f"{path.name}: bad header")


def load_symbol_row(path: Path, symbol: str) -> dict | None:
    """Exact symbolCode match (spec §3: no fuzzy mapping; case exceptions must be
    pre-committed in the spec's §11 table before compute)."""
    with path.open(encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("|")
        idx = {name: i for i, name in enumerate(header)}
        for line in f:
            cells = line.rstrip("\n").split("|")
            if cells[idx["symbolCode"]] == symbol:
                return {k: cells[i] for k, i in idx.items()}
    return None


def si_series(symbol: str, si_dir: Path, cutoff: datetime.date,
              lag_days: int = LAG_DAYS) -> tuple[list[dict], dict]:
    """All archived reports for symbol with settlement + lag <= cutoff, ascending.
    Each item: {settlement: date, short_qty: int, revised_next: bool placeholder}.
    Second return: diagnostics {files_scanned, revision_seen}."""
    if not si_dir.is_dir():
        raise ShortInterestError(f"{si_dir} missing — archive step not run")
    rows, revision_seen = [], 0
    files = sorted(si_dir.glob("shrt*.csv"))
    usable_files = []
    for path in files:
        ymd = path.stem[len("shrt"):]
        settlement = datetime.date(int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8]))
        if settlement + datetime.timedelta(days=lag_days) <= cutoff:
            usable_files.append((settlement, path))
    for settlement, path in usable_files:
        row = load_symbol_row(path, symbol)
        if row is None:
            continue  # symbol absent that cycle — recorded via gaps in the series
        if (row.get("revisionFlag") or "").strip() == "R":
            revision_seen += 1  # diagnostic only; first-disseminated value kept
        rows.append({"settlement": settlement,
                     "short_qty": int(row["currentShortPositionQuantity"])})
    return rows, {"files_scanned": len(usable_files), "revision_seen": revision_seen}


def shares_at(share_facts: dict, on: datetime.date,
              freshness_days: int = SHARES_FRESHNESS_DAYS) -> float | None:
    """Denominator: latest (end, filed) instant dei shares-outstanding fact with
    on - freshness <= end <= on. share_facts = payload_v2 extract_share_facts()[0]
    (already PIT-filtered filed <= cutoff upstream)."""
    facts = share_facts.get(SHARES_TAG, [])
    best = None
    for f in facts:
        if f.get("period_type") != "instant":
            continue
        end = datetime.date.fromisoformat(f["end"])
        if end > on or end < on - datetime.timedelta(days=freshness_days):
            continue
        key = (end, f.get("filed") or "")
        if best is None or key > best[0]:
            best = (key, float(f["value"]))
    return None if best is None else best[1]


# ---------------------------------------------------------------- score (spec §3–§4)

def _ols_slope(ys: list[float]) -> float:
    n = len(ys)
    xbar = (n - 1) / 2
    ybar = sum(ys) / n
    num = sum((i - xbar) * (y - ybar) for i, y in enumerate(ys))
    den = sum((i - xbar) ** 2 for i in range(n))
    return num / den


def b4_from_series(series: list[dict], share_facts: dict,
                   cutoff: datetime.date, diagnostics: dict | None = None) -> dict:
    """Spec §3 metrics + §4 scores from an aligned series. Pure, no I/O."""
    flags = {"insufficient_history": False, "no_si_file": False,
             "no_shares_denominator": False, "slope_unavailable": False,
             "revision_seen_diagnostic": (diagnostics or {}).get("revision_seen", 0)}
    out = {"score_level": None, "score_slope_aug": None, "sir_last": None,
           "abnormal_sir_last": None, "slope4": None,
           "n_reports_trailing12m": 0, "last_settlement": None,
           "flags": flags, "cutoff": str(cutoff)}
    if not series:
        flags["no_si_file"] = True
        return out

    sir = []  # ascending [(settlement, SIR)]
    for rep in series:
        denom = shares_at(share_facts, rep["settlement"])
        if denom is None or denom <= 0:
            continue
        sir.append((rep["settlement"], rep["short_qty"] / denom))
    if not sir:
        flags["no_shares_denominator"] = True
        return out

    def abnormal(i: int) -> tuple[float, int]:
        t, v = sir[i]
        lo = t - datetime.timedelta(days=TRAILING_DAYS)
        window = [x for (d, x) in sir[:i] if lo <= d < t]  # self excluded
        if len(window) < MIN_TRAILING_REPORTS:
            return float("nan"), len(window)
        return v - statistics.median(window), len(window)

    a_last, n12 = abnormal(len(sir) - 1)
    t_last, sir_last = sir[-1]
    out["last_settlement"] = str(t_last)
    out["sir_last"] = sir_last
    out["n_reports_trailing12m"] = n12
    if a_last != a_last:  # NaN
        flags["insufficient_history"] = True
        return out
    out["abnormal_sir_last"] = a_last
    out["score_level"] = a_last

    if len(sir) < SLOPE_REPORTS:
        flags["slope_unavailable"] = True
        return out
    tail = sir[-SLOPE_REPORTS:]
    a_tail = [abnormal(len(sir) - SLOPE_REPORTS + j)[0] for j in range(SLOPE_REPORTS)]
    gap_ok = all(
        (tail[j + 1][0] - tail[j][0]).days <= 21 for j in range(SLOPE_REPORTS - 1)
    )  # consecutive bi-monthly reports: adjacent settlements <= 3 weeks apart
    if any(a != a for a in a_tail) or not gap_ok:
        flags["slope_unavailable"] = True
        return out
    out["slope4"] = _ols_slope(a_tail)
    out["score_slope_aug"] = a_last + out["slope4"]
    return out


def b4_from_facts(symbol: str, cutoff: datetime.date, si_dir: Path,
                  share_facts: dict) -> dict:
    """E2-contract core (spec §8): pure function over archived files + PIT share
    facts. Missing archive dir raises (archive precedes scoring); missing symbol
    rows produce flagged None scores, never exceptions (keeps E2 loops alive)."""
    series, diag = si_series(symbol, si_dir, cutoff)
    return b4_from_series(series, share_facts, cutoff, diag)
