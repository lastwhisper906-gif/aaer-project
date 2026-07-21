"""payload_v2_extract.py — payload-v2 진단 추출기 (WS-1/F-4, specs/payload_v2.md).

진단 전용(diagnostic-only): 출력은 runs/diagnostics/payload_v2/ 로만 가며 어떤
피평가자 페이로드에도 편입되지 않는다 (편입 = 별도 소유자 게이트, 스펙 §0).

추출 2채널:
  (a) 8-K item 코드 — submissions JSON `items` 병렬 배열 (스펙 §3.2)
  (b) 주식수·EPS 사실 — companyfacts dei/us-gaap, shares·USD/shares 단위 (스펙 §2.2)

PIT 의미론은 동결 빌더(build_payload.py)와 동일하다. corpus 읽기는 cutoff_guard
벌크 로더를 경유해 레지스트리 컷오프, accession filingDate 대조, 접근 로그를
적용하며 정적 강제 테스트가 우회를 검출한다. fixture 레지스트리는 실제 corpus에
사용할 수 없다.

fail-closed: 파싱 불가 날짜 → 예외 (조용한 skip 금지). 파일 부재 → 코어 함수
예외, CLI 만 케이스 단위 포착·coverage 기록 (네트워크 fetch 금지).

사용: .venv/bin/python pipeline/payload_v2_extract.py [--out runs/diagnostics/payload_v2]
"""
from __future__ import annotations

import argparse
import datetime
import json
from pathlib import Path

import cutoff_guard

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = cutoff_guard.DEFAULT_EDGAR_DATA
EVALUATEE_CASES = REPO_ROOT / "data" / "evaluatee" / "cases.json"
CASE_FILES = ["cases.json", "cases_v2.json", "cases_wave2.json",
              "cases_holdout.json", "cases_holdout_controls.json"]
OUT_DIR = REPO_ROOT / "runs" / "diagnostics" / "payload_v2"

# 스펙 §2.2 — (namespace, tag, unit). 두 diluted 철자 병기 (정직 기록: 실측 태그는
# WeightedAverageNumberOfDilutedSharesOutstanding, 미션 문면 철자는 변형 대비 보존).
SHARE_TAGS = [
    ("dei", "EntityCommonStockSharesOutstanding", "shares"),
    ("us-gaap", "EarningsPerShareBasic", "USD/shares"),
    ("us-gaap", "EarningsPerShareDiluted", "USD/shares"),
    ("us-gaap", "WeightedAverageNumberOfSharesOutstandingBasic", "shares"),
    ("us-gaap", "WeightedAverageNumberOfDilutedSharesOutstanding", "shares"),
    ("us-gaap", "WeightedAverageNumberOfSharesOutstandingDiluted", "shares"),
    ("us-gaap", "CommonStockSharesOutstanding", "shares"),
]
EIGHTK_FORMS = ("8-K", "8-K/A")
ANNUAL_DAYS = (340, 400)    # 동결 빌더와 동일 밴드
QUARTER_DAYS = (75, 100)


class PayloadV2Error(Exception):
    """fail-closed: 파싱 불가 날짜·파일 부재 등 — 조용한 skip 금지."""


def _iso(value, field: str) -> datetime.date:
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError as e:
        raise PayloadV2Error(f"{field}={value!r}: ISO 날짜가 아님 — fail-closed") from e


def parse_items(items_raw: str) -> list[str]:
    """스펙 §3.2: 쉼표 분리 → strip → 빈 토큰 제거. 원시 문자열은 호출자가 보존."""
    return [tok.strip() for tok in (items_raw or "").split(",") if tok.strip()]


def _case_and_registry(case_or_ticker, cutoff, data_dir, registry_path=None):
    if registry_path is not None:
        registries = [registry_path]
    else:
        registries = [EVALUATEE_CASES.parent / name for name in CASE_FILES]
    if isinstance(case_or_ticker, dict):
        matches = []
        for path in registries:
            cases = cutoff_guard._load_cases(path)
            if cases.get(case_or_ticker.get("case_id")) == case_or_ticker:
                matches.append(path)
        if len(matches) != 1:
            raise cutoff_guard.CutoffGuardError(
                f"case={case_or_ticker.get('case_id')!r}: 정확히 한 레지스트리에 속하지 않음")
        return case_or_ticker, matches[0]
    matches = []
    for path in registries:
        for case in cutoff_guard._load_cases(path).values():
            if case.get("ticker") == case_or_ticker:
                matches.append((case, path))
    distinct = {}
    for case, path in matches:
        key = (case.get("ticker"), case.get("cutoff_date"), case.get("cik"))
        distinct.setdefault(key, (case, path))
    if not distinct and Path(data_dir).resolve() != DATA_DIR.resolve():
        case = {"case_id": f"FIXTURE-{case_or_ticker}", "ticker": case_or_ticker,
                "cutoff_date": str(cutoff)}
        return case, registry_path or {"cases": [case]}
    if len(distinct) != 1:
        raise cutoff_guard.CutoffGuardError(
            f"ticker={case_or_ticker!r}, cutoff={cutoff}: 정확히 한 케이스가 아님")
    case, path = next(iter(distinct.values()))
    if _iso(case.get("cutoff_date"), "cutoff_date") != _iso(cutoff, "cutoff_date"):
        raise cutoff_guard.CutoffGuardError("호출자 cutoff_date가 레지스트리와 불일치")
    return case, path


def extract_8k_items(case_or_ticker, cutoff: datetime.date,
                     data_dir: Path = DATA_DIR, registry_path=None) -> tuple[list[dict], dict]:
    """컷오프 전(포함) 8-K/8-K/A 행의 item 코드. 반환: (rows, coverage)."""
    try:
        case, registry_path = _case_and_registry(case_or_ticker, cutoff, data_dir, registry_path)
        loaded, metadata = cutoff_guard.load_edgar_chronology(
            case["case_id"], case["ticker"], cutoff, data_dir=data_dir,
            registry_path=registry_path)
    except cutoff_guard.CutoffGuardError as e:
        raise PayloadV2Error(str(e)) from e
    rows = []
    for row in loaded:
        if row["form"] in EIGHTK_FORMS:
            raw = row["items"]
            rows.append({"accession": row["accessionNumber"], "form": row["form"],
                         "filing_date": row["filingDate"], "items_raw": raw,
                         "items": parse_items(raw)})
    rows.sort(key=lambda r: (r["filing_date"], r["accession"]))
    # 다중 청크 병합 중복 제거 (accession 기준)
    dedup, seen = [], set()
    for r in rows:
        if r["accession"] not in seen:
            seen.add(r["accession"])
            dedup.append(r)
    coverage = {"submissions_files_read": len(metadata["files_read"]),
                "paginated_subfiles_listed_not_cached": metadata["listed_subfiles"]}
    return dedup, coverage


def extract_share_facts(case_or_ticker, cutoff: datetime.date,
                        data_dir: Path = DATA_DIR, registry_path=None) -> tuple[dict, dict]:
    """컷오프 전(포함) 주식수·EPS PIT 시계열. 반환: (facts, coverage)."""
    try:
        case, registry_path = _case_and_registry(case_or_ticker, cutoff, data_dir, registry_path)
        loaded, metadata = cutoff_guard.load_xbrl_facts(
            case["case_id"], case["ticker"], cutoff, data_dir=data_dir,
            registry_path=registry_path,
            allow_unindexed_accessions=isinstance(registry_path, dict))
    except cutoff_guard.CutoffGuardError as e:
        raise PayloadV2Error(str(e)) from e
    table: dict[str, dict] = {}
    wanted = set(SHARE_TAGS)
    for row in loaded:
        ns, tag, unit, f = row["namespace"], row["tag"], row["unit"], row["fact"]
        if (ns, tag, unit) in wanted:
                start = f.get("start")
                if start:
                    span = (_iso(f["end"], "end") - _iso(start, "start")).days
                    if ANNUAL_DAYS[0] <= span <= ANNUAL_DAYS[1]:
                        ptype = "annual"
                    elif QUARTER_DAYS[0] <= span <= QUARTER_DAYS[1]:
                        ptype = "quarterly"
                    else:
                        continue
                else:
                    ptype = "instant"
                key = (start or "") + "|" + f["end"]
                slot = table.setdefault(f"{ns}:{tag}", {})
                prev = slot.get(key)
                cand = {"start": start, "end": f["end"], "period_type": ptype,
                        "value": f["val"], "unit": unit, "filed": f["filed"],
                        "accession": f.get("accn"), "form": f.get("form")}
                if prev is None or (cand["filed"], cand["accession"] or "") > (prev["filed"], prev["accession"] or ""):
                    slot[key] = cand
    facts_out = {tag: sorted(vals.values(), key=lambda v: (v["end"], v["start"] or ""))
                 for tag, vals in sorted(table.items())}
    coverage = {"facts_namespaces_present": metadata["namespaces"],
                "tags_found": {tag: len(vals) for tag, vals in facts_out.items()}}
    return facts_out, coverage


def extract_case(case: dict, source_file: str, data_dir: Path = DATA_DIR) -> dict:
    cutoff = _iso(case["cutoff_date"], "cutoff_date")
    registry = REPO_ROOT / "data" / "evaluatee" / source_file
    eightk, cov_e = extract_8k_items(case, cutoff, data_dir, registry)
    shares, cov_x = extract_share_facts(case, cutoff, data_dir, registry)
    return {
        "spec": "specs/payload_v2.md",
        "diagnostic_only": True,
        "case_id": case["case_id"], "ticker": case["ticker"],
        "cutoff_date": case["cutoff_date"], "source_file": source_file,
        "eightk_items": eightk,
        "share_facts": shares,
        "coverage": {**cov_e, **cov_x},
    }


def load_universe(repo_root: Path = REPO_ROOT) -> list[tuple[dict, str]]:
    out = []
    for name in CASE_FILES:
        data = json.loads((repo_root / "data" / "evaluatee" / name).read_text(encoding="utf-8"))
        for case in data["cases"]:
            out.append((case, name))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(OUT_DIR))
    args = ap.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    universe = load_universe()
    done, partial, missing = [], [], []
    for case, src in universe:
        cid = case["case_id"]
        try:
            payload = extract_case(case, src)
        except PayloadV2Error as e:
            missing.append({"case_id": cid, "ticker": case["ticker"], "reason": str(e)})
            continue
        (out_dir / f"{cid}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        done.append(cid)
        if payload["coverage"]["paginated_subfiles_listed_not_cached"]:
            partial.append({"case_id": cid, "ticker": case["ticker"],
                            "missing_subfiles": payload["coverage"]["paginated_subfiles_listed_not_cached"]})
    coverage = {
        "spec": "specs/payload_v2.md",
        "coverage": f"{len(done)}/{len(universe)}",
        "complete": len(done), "total": len(universe),
        "partial_cases_subfiles_not_cached": partial,
        "missing_cases": missing,
        "note": "partial = 본체 filings.files에 열거된 하위 파일이 로컬 미캐시 (fetch 금지 — OWNER_QUEUE 등록)",
    }
    (out_dir / "COVERAGE.json").write_text(
        json.dumps(coverage, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"payload-v2: {len(done)}/{len(universe)} 케이스 추출, partial {len(partial)}, missing {len(missing)}")
    for m in missing:
        print("  MISSING:", m["case_id"], m["ticker"], m["reason"])
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
