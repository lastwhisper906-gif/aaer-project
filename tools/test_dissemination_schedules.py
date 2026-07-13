"""dissemination_schedules 테스트 — 전부 오프라인 (합성 HTML 픽스처), 네트워크 0.

연도 추론(헤딩 지배·12월→1월 롤오버)·요일 체크섬·해소 규칙 1~3·해소 불능 정지·
산술 가드·SI 아카이브 커버리지 대조·load_map 평탄화·build 결정론.
"""
import json
from pathlib import Path

import pytest

import dissemination_schedules as ds


def table(year: int, rows: list[tuple[str, str, str]]) -> str:
    tr = "".join(
        f"<tr><td>{s}</td><td>{d} – 6 p.m.</td><td>{p}</td></tr>" for s, d, p in rows)
    return (f"<h2>{year} Short Interest Reporting Dates</h2>"
            f"<table><tr><th>Settlement Date</th><th>Due Date1</th>"
            f"<th>Publication Date</th></tr>{tr}</table>")


def write_snap(tmp_path, name, body):
    (tmp_path / name).write_text(f"<html><body>{body}</body></html>", encoding="utf-8")


@pytest.fixture()
def snaps(tmp_path, monkeypatch):
    """정본 목록을 합성 2스냅샷으로 대체."""
    monkeypatch.setattr(ds, "SNAPSHOTS", {
        "20180111_si.html": "synthetic://a", "20190121_si.html": "synthetic://b"})
    return tmp_path


def test_year_inference_and_rollover(snaps):
    write_snap(snaps, "20180111_si.html", table(2017, [
        ("December 15<br>Friday", "December 19<br>Tuesday", "December 27<br>Wednesday"),
        ("December 29<br>Friday", "January 3<br>Wednesday", "January 10<br>Wednesday"),
    ]))
    write_snap(snaps, "20190121_si.html", table(2018, [
        ("January 12<br>Friday", "January 17<br>Wednesday", "January 24<br>Wednesday"),
    ]))
    cands = {}
    for f in ("20180111_si.html", "20190121_si.html"):
        for k, v in ds.parse_snapshot(snaps / f).items():
            cands.setdefault(k, []).extend(v)
    merged, disc = ds.merge(cands)
    assert merged["2017-12-29"]["publication"] == "2018-01-10"   # 롤오버
    assert merged["2017-12-15"]["publication"] == "2017-12-27"   # 동년
    assert merged["2018-01-12"]["publication"] == "2018-01-24"
    assert disc == []
    assert merged["2017-12-29"]["delay_days"] == 12


def test_heading_gates_tables(snaps):
    """연도 헤딩 없는 테이블(무관 표)은 무시된다."""
    write_snap(snaps, "20180111_si.html",
               "<table><tr><th>Settlement Date</th><th>x</th><th>y</th></tr>"
               "<tr><td>January 5<br>Friday</td><td>January 9</td>"
               "<td>January 16</td></tr></table>" + table(2018, []))
    assert ds.parse_snapshot(snaps / "20180111_si.html") == {}


def test_rule1_weekday_typo_outvoted(snaps):
    # 2025-04-25는 금요일 — 첫 스냅샷은 Thursday 오탈, 둘째가 self-consistent
    write_snap(snaps, "20180111_si.html", table(2025, [
        ("April 15<br>Tuesday", "April 17<br>Thursday", "April 25<br>Thursday")]))
    write_snap(snaps, "20190121_si.html", table(2025, [
        ("April 15<br>Tuesday", "April 17<br>Thursday", "April 25<br>Friday")]))
    cands = {}
    for f in ds.SNAPSHOTS:
        for k, v in ds.parse_snapshot(snaps / f).items():
            cands.setdefault(k, []).extend(v)
    merged, disc = ds.merge(cands)
    assert merged["2025-04-15"]["publication"] == "2025-04-25"
    assert [d["rule"] for d in disc] == ["weekday_typo_outvoted"]
    assert merged["2025-04-15"]["weekday_typo_in"] == ["20180111_si.html"]


def test_rule2_revision_latest_wins(snaps):
    # 양쪽 다 self-consistent이나 공표일이 다름 (연중 개정) — 최신 스냅샷 승
    write_snap(snaps, "20180111_si.html", table(2021, [
        ("December 15<br>Wednesday", "December 17<br>Friday", "December 24<br>Friday")]))
    write_snap(snaps, "20190121_si.html", table(2021, [
        ("December 15<br>Wednesday", "December 17<br>Friday", "December 27<br>Monday")]))
    cands = {}
    for f in ds.SNAPSHOTS:
        for k, v in ds.parse_snapshot(snaps / f).items():
            cands.setdefault(k, []).extend(v)
    merged, disc = ds.merge(cands)
    assert merged["2021-12-15"]["publication"] == "2021-12-27"
    assert [d["rule"] for d in disc] == ["revision_latest_wins"]
    assert disc[0]["superseded_publications"] == ["2021-12-24"]


def test_rule3_all_sources_typo_plus7(snaps, monkeypatch):
    # 전 스냅샷 동일 오탈 요일 (2026-12-31 실증 형태): due+7 패턴이면 날짜 채택
    body = table(2026, [
        ("December 31<br>Thursday", "January 5<br>Monday", "January 12<br>Monday")])
    write_snap(snaps, "20180111_si.html", body)
    write_snap(snaps, "20190121_si.html", body)
    cands = {}
    for f in ds.SNAPSHOTS:
        for k, v in ds.parse_snapshot(snaps / f).items():
            cands.setdefault(k, []).extend(v)
    merged, disc = ds.merge(cands)
    assert merged["2026-12-31"]["publication"] == "2027-01-12"
    assert [d["rule"] for d in disc] == ["weekday_typo_all_sources_plus7"]


def test_unresolvable_halts(snaps):
    # 오탈 요일 + due+7 불성립 → 정지
    write_snap(snaps, "20180111_si.html", table(2026, [
        ("December 31<br>Thursday", "January 5<br>Monday", "January 13<br>Monday")]))
    write_snap(snaps, "20190121_si.html", table(2026, []))
    cands = {}
    for k, v in ds.parse_snapshot(snaps / "20180111_si.html").items():
        cands.setdefault(k, []).extend(v)
    with pytest.raises(ds.DisseminationError, match="해소 불능"):
        ds.merge(cands)


def test_arithmetic_guard(snaps):
    with pytest.raises(ds.DisseminationError, match="산술 가드"):
        ds.parse_snapshot(write_snap(snaps, "20180111_si.html", table(2020, [
            ("March 13<br>Friday", "March 17<br>Tuesday", "June 24<br>Wednesday")]))
            or snaps / "20180111_si.html")


def test_archive_coverage_check(tmp_path):
    (tmp_path / "shrt20200131.csv").write_text("x")
    (tmp_path / "shrt20200214.csv").write_text("x")
    merged = {"2020-01-31": {"publication": "2020-02-11"}}
    assert ds.archive_coverage_check(merged, tmp_path) == ["2020-02-14"]


def test_build_deterministic_and_load_map(snaps, tmp_path):
    write_snap(snaps, "20180111_si.html", table(2017, [
        ("December 29<br>Friday", "January 3<br>Wednesday", "January 10<br>Wednesday")]))
    write_snap(snaps, "20190121_si.html", table(2018, [
        ("January 12<br>Friday", "January 17<br>Wednesday", "January 24<br>Wednesday")]))
    si = tmp_path / "si"
    si.mkdir()
    (si / "shrt20171229.csv").write_text("x")
    out1, out2 = tmp_path / "o1.json", tmp_path / "o2.json"
    r1 = ds.build(snaps, out1, si)
    r2 = ds.build(snaps, out2, si)
    assert out1.read_bytes() == out2.read_bytes()      # 결정론
    assert r1 == r2 and r1["rows"] == 2
    data = json.loads(out1.read_text())
    assert data["_provenance"]["lag14_conservative_in_sample"] is True
    assert ds.load_map(out1) == {"2017-12-29": "2018-01-10",
                                 "2018-01-12": "2018-01-24"}


def test_build_halts_on_si_coverage_gap(snaps, tmp_path):
    write_snap(snaps, "20180111_si.html", table(2018, [
        ("January 12<br>Friday", "January 17<br>Wednesday", "January 24<br>Wednesday")]))
    write_snap(snaps, "20190121_si.html", table(2018, []))
    si = tmp_path / "si"
    si.mkdir()
    (si / "shrt20180131.csv").write_text("x")          # 매핑에 없는 결제일
    with pytest.raises(ds.DisseminationError, match="구멍"):
        ds.build(snaps, tmp_path / "o.json", si)
