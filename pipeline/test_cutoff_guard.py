"""cutoff_guard 테스트. v0: 허용 / 차단(예외) / 경계일 허용 / 양쪽 모두 로그.
v1 추가: 중복 case_id fail-closed / EDGAR accession 역조회(일치·불일치·미보유)."""
import json

import pytest

from cutoff_guard import CutoffGuardError, CutoffViolationError, load_document

CUTOFF = "2014-06-05"  # 예: 폭로일 2014-06-06의 전일
ACCESSION = "0001234567-14-000001"


@pytest.fixture
def env(tmp_path):
    registry = tmp_path / "candidates.json"
    registry.write_text(json.dumps({"candidates": [
        {"case_id": "T01", "ticker": "AAA", "cutoff_date": CUTOFF},
        {"case_id": "T02", "ticker": "BBB", "cutoff_date": "UNRESOLVED"},
    ]}), encoding="utf-8")
    doc = tmp_path / "doc.txt"
    doc.write_text("10-K body", encoding="utf-8")
    log = tmp_path / "logs" / "access_log.jsonl"
    edgar = tmp_path / "aaer-data"
    sub_dir = edgar / "AAA" / "edgar"
    sub_dir.mkdir(parents=True)
    (sub_dir / "CIK0001234567.json").write_text(json.dumps({"filings": {"recent": {
        "accessionNumber": [ACCESSION], "filingDate": ["2014-01-01"], "form": ["10-K"],
    }, "files": []}}), encoding="utf-8")
    return {"registry": registry, "doc": doc, "log": log, "edgar": edgar}


def read_log(log):
    return [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]


def load(env, doc_date, case_id="T01", **kwargs):
    return load_document(case_id, env["doc"], doc_date,
                         registry_path=env["registry"], log_path=env["log"],
                         edgar_data_dir=env["edgar"], **kwargs)


def test_allowed_load_returns_content_and_logs(env):
    assert load(env, "2014-01-01") == "10-K body"
    (entry,) = read_log(env["log"])
    assert entry["verdict"] == "allowed" and entry["case_id"] == "T01"
    assert "timestamp" in entry and entry["doc_date"] == "2014-01-01"


def test_violation_raises_exception_not_filter(env):
    with pytest.raises(CutoffViolationError) as exc:
        load(env, "2014-06-06")  # 폭로 당일 = 컷오프 다음날 → 차단
    assert exc.value.case_id == "T01"
    assert str(exc.value.doc_date) == "2014-06-06"
    assert str(exc.value.cutoff_date) == CUTOFF


def test_boundary_doc_date_equal_to_cutoff_is_allowed(env):
    assert load(env, CUTOFF) == "10-K body"
    assert read_log(env["log"])[-1]["verdict"] == "allowed"


def test_log_written_on_both_outcomes(env):
    load(env, "2014-01-01")
    with pytest.raises(CutoffViolationError):
        load(env, "2015-01-01")
    verdicts = [e["verdict"] for e in read_log(env["log"])]
    assert verdicts == ["allowed", "blocked"]
    assert read_log(env["log"])[1]["reason"] == "cutoff_violation"


def test_unresolved_cutoff_and_unknown_case_fail_closed(env):
    with pytest.raises(CutoffGuardError):
        load(env, "2000-01-01", case_id="T02")  # UNRESOLVED → 아무리 오래된 문서도 차단
    with pytest.raises(CutoffGuardError):
        load(env, "2000-01-01", case_id="T99")
    assert [e["reason"] for e in read_log(env["log"])] == ["cutoff_unresolved", "unknown_case_id"]


def test_duplicate_case_id_fails_closed(env):
    env["registry"].write_text(json.dumps({"candidates": [
        {"case_id": "T01", "ticker": "AAA", "cutoff_date": CUTOFF},
        {"case_id": "T01", "ticker": "AAA", "cutoff_date": "2020-01-01"},
    ]}), encoding="utf-8")
    with pytest.raises(CutoffGuardError, match="중복"):
        load(env, "2014-01-01")


def test_accession_crosscheck_pass(env):
    assert load(env, "2014-01-01", accession_no=ACCESSION) == "10-K body"
    entry = read_log(env["log"])[-1]
    assert entry["verdict"] == "allowed" and "cross-checked" in entry["reason"]
    assert entry["accession_no"] == ACCESSION


def test_accession_crosscheck_rejects_wrong_doc_date(env):
    # 신고 doc_date가 컷오프 안이어도 EDGAR filingDate와 다르면 통과 불가
    with pytest.raises(CutoffGuardError, match="EDGAR filingDate"):
        load(env, "2014-02-02", accession_no=ACCESSION)
    assert read_log(env["log"])[-1]["reason"] == "doc_date_mismatch_edgar"


def test_accession_crosscheck_unknown_accession_fails_closed(env):
    with pytest.raises(CutoffGuardError, match="미발견"):
        load(env, "2014-01-01", accession_no="0009999999-14-000009")


def test_accession_crosscheck_missing_submissions_fails_closed(env, tmp_path):
    with pytest.raises(CutoffGuardError, match="submissions JSON 없음"):
        load_document("T01", env["doc"], "2014-01-01", accession_no=ACCESSION,
                      registry_path=env["registry"], log_path=env["log"],
                      edgar_data_dir=tmp_path / "empty")
    assert read_log(env["log"])[-1]["reason"] == "edgar_crosscheck_unavailable"
