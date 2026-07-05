"""cutoff_guard.py — 유일한 데이터 로딩 게이트웨이 (PROJECT.md §5-1, CLAUDE.md 방법론 규율 1).

모든 파이프라인 데이터 로딩은 load_document()를 경유한다. 컷오프 위반은
예외로 즉시 중단시킨다 — 조용한 필터가 아니다. 필터는 "위반이 일어났다는
사실"을 지우지만, 예외는 위반 시도를 로그와 함께 증거로 남긴다.
doc_date == cutoff_date는 허용 (cutoff_date 자체가 폭로 '전일'로 정의됨).

v1: EDGAR 문서는 accession_no를 주면 호출자 신고 doc_date를 로컬 submissions
JSON(~/aaer-data/{ticker}/edgar/)의 filingDate와 대조한다 — 가드의 강도가
호출자 메타데이터의 정확성에 종속되지 않도록. 불일치·미보유는 fail-closed.
"""
from __future__ import annotations

import datetime
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "data" / "candidates" / "candidates.json"
DEFAULT_LOG = REPO_ROOT / "logs" / "access_log.jsonl"
DEFAULT_EDGAR_DATA = Path.home() / "aaer-data"  # data/README.md 경로 규약


class CutoffGuardError(Exception):
    """가드 자체의 실패(미등록 케이스, 파싱 불가 날짜, 미확정 컷오프). 항상 fail-closed."""


class CutoffViolationError(CutoffGuardError):
    """doc_date > cutoff_date. 파이프라인 실행을 무효화해야 하는 위반."""

    def __init__(self, case_id: str, doc_date: datetime.date, cutoff_date: datetime.date):
        self.case_id = case_id
        self.doc_date = doc_date
        self.cutoff_date = cutoff_date
        super().__init__(
            f"look-ahead 위반: case={case_id} doc_date={doc_date} > cutoff_date={cutoff_date}"
        )


def _parse_date(value, field: str) -> datetime.date:
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError as e:
        raise CutoffGuardError(f"{field}={value!r}: ISO 날짜가 아님 (UNRESOLVED 케이스는 로딩 불가)") from e


def _load_cases(registry_path=DEFAULT_REGISTRY) -> dict:
    """candidates.json → {case_id: case dict}. 중복 case_id는 조용한 last-wins가
    아니라 예외 — 어느 컷오프가 적용됐는지 모호해지는 순간 가드 전체가 무효."""
    raw = json.loads(Path(registry_path).read_text(encoding="utf-8"))
    cases = raw.get("candidates", raw) if isinstance(raw, dict) else raw
    by_id = {}
    for case in cases:
        cid = case["case_id"]
        if cid in by_id:
            raise CutoffGuardError(f"중복 case_id={cid!r}: 레지스트리 모호 — fail-closed")
        by_id[cid] = case
    return by_id


def load_registry(registry_path=DEFAULT_REGISTRY) -> dict:
    """candidates.json → {case_id: cutoff_date(date) | None(미확정)}."""
    registry = {}
    for cid, case in _load_cases(registry_path).items():
        try:
            registry[cid] = _parse_date(case.get("cutoff_date"), "cutoff_date")
        except CutoffGuardError:
            registry[cid] = None  # UNRESOLVED → 접근 시 fail-closed
    return registry


def _normalize_accession(accession_no: str) -> str:
    digits = re.sub(r"[^0-9]", "", accession_no)
    if len(digits) != 18:
        raise CutoffGuardError(f"accession_no={accession_no!r}: 18자리 형식이 아님")
    return f"{digits[:10]}-{digits[10:12]}-{digits[12:]}"


def _edgar_filing_date(case: dict, accession_no: str, edgar_data_dir) -> datetime.date:
    """로컬 submissions JSON에서 accession의 filingDate를 역조회. 미보유·미발견은
    fail-closed — 검증 불가능한 문서를 통과시키지 않는다."""
    ticker = case.get("ticker", "").split("/")[0]
    edgar_dir = Path(edgar_data_dir) / ticker / "edgar"
    chunks = sorted(edgar_dir.glob("CIK*.json"))  # 본체 + 구형 청크(…-submissions-NNN.json) 모두 매칭
    if not chunks:
        raise CutoffGuardError(
            f"case={case.get('case_id')}: {edgar_dir}에 submissions JSON 없음 — "
            "tools/fetch_primary_sources.py로 수집 후 재시도 (fail-closed)"
        )
    target = _normalize_accession(accession_no)
    for chunk in chunks:
        j = json.loads(chunk.read_text(encoding="utf-8"))
        blocks = [j["filings"]["recent"]] if "filings" in j else [j]
        for b in blocks:
            for i, acc in enumerate(b.get("accessionNumber", [])):
                if acc == target:
                    return _parse_date(b["filingDate"][i], "filingDate")
    raise CutoffGuardError(
        f"accession_no={target}: {edgar_dir}의 submissions JSON에서 미발견 — fail-closed"
    )


def _log(log_path, record: dict) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), **record}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_document(case_id: str, path_or_url: str, doc_date, *,
                  accession_no: str | None = None,
                  registry_path=DEFAULT_REGISTRY, log_path=DEFAULT_LOG,
                  edgar_data_dir=DEFAULT_EDGAR_DATA, loader=None):
    """게이트웨이. 허용/차단 모든 시도를 log_path에 기록하고, 위반은 예외로 중단.

    accession_no가 주어지면(EDGAR 문서) doc_date를 로컬 submissions JSON의
    filingDate와 대조한다 — 호출자 자기신고만으로는 통과하지 못한다.
    """
    def attempt(verdict: str, reason: str) -> None:
        record = {"case_id": case_id, "doc": str(path_or_url),
                  "doc_date": str(doc_date), "verdict": verdict, "reason": reason}
        if accession_no is not None:
            record["accession_no"] = accession_no
        _log(log_path, record)

    cases = _load_cases(registry_path)
    if case_id not in cases:
        attempt("blocked", "unknown_case_id")
        raise CutoffGuardError(f"미등록 case_id={case_id!r}: 레지스트리에 없는 케이스는 로딩 불가")

    try:
        cutoff = _parse_date(cases[case_id].get("cutoff_date"), "cutoff_date")
    except CutoffGuardError:
        attempt("blocked", "cutoff_unresolved")
        raise CutoffGuardError(f"case={case_id}: cutoff_date 미확정(UNRESOLVED) — fail-closed") from None

    parsed = _parse_date(doc_date, "doc_date")

    if accession_no is not None:
        try:
            edgar_date = _edgar_filing_date(cases[case_id], accession_no, edgar_data_dir)
        except CutoffGuardError:
            attempt("blocked", "edgar_crosscheck_unavailable")
            raise
        if edgar_date != parsed:
            attempt("blocked", "doc_date_mismatch_edgar")
            raise CutoffGuardError(
                f"case={case_id} accession={accession_no}: 신고 doc_date={parsed} ≠ "
                f"EDGAR filingDate={edgar_date} — 호출자 메타데이터 불신, fail-closed"
            )

    if parsed > cutoff:
        attempt("blocked", "cutoff_violation")
        raise CutoffViolationError(case_id, parsed, cutoff)

    attempt("allowed", "doc_date <= cutoff_date"
            + (", edgar filingDate cross-checked" if accession_no is not None else ""))
    if loader is not None:
        return loader(path_or_url)
    p = Path(path_or_url)
    if not p.is_file():
        raise CutoffGuardError(f"{path_or_url!r}: 로컬 파일 아님 — URL은 loader= 콜백으로 주입 (v0)")
    return p.read_text(encoding="utf-8")
