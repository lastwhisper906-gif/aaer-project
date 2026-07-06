"""validate_control_input 변이 주입 테스트 (4층 방어가 실제로 잡는지 실증).

각 테스트 = 정상 픽스처 PASS 확인 후 결함 1개 주입 → 해당 층이 격리하는지 단언.
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_control_input as vc
from rp08_common import sha256_file

CIK = "0000085961"


def build_fixture(tmp_path):
    raw = tmp_path / "raw"
    big = tmp_path / "big"
    (raw / "sic_lists").mkdir(parents=True)
    (big / "submissions").mkdir(parents=True)
    (big / "facts").mkdir(parents=True)

    atom = raw / "sic_lists/SIC7510_start0.atom"
    atom.write_text(f"<feed><entry><cik>{CIK}</cik></entry></feed>")
    sub = big / f"submissions/CIK{CIK}.json"
    sub.write_text(json.dumps({"cik": 85961, "filings": {"recent": {}}}))
    facts = big / f"facts/CIK{CIK}.json"
    facts.write_text(json.dumps({"facts": {"us-gaap": {}}}))

    pool = {
        "_meta": {"criteria": "docs/CONTROL_CRITERIA_v1.md"},
        "cases": {"T13": {
            "cutoff": "2014-05-12", "sics_used": ["7510"],
            "s0_truncated_count": 0,
            "candidates": {CIK: {
                "cik": CIK, "sic_pool": "7510", "eligible": True, "fails": [],
                "pre_cutoff_10K": 10, "pre_cutoff_10Q": 30,
                "xbrl_pre_cutoff": True, "active_in_window": True,
                "item_402_in_window": [], "first_counted": "1994-03-30",
                "former_names": [], "e4_hit_count": 0, "e4_hits": [],
                "pit_fetched": True,
            }}}}}
    (raw / "pool_extract.json").write_text(json.dumps(pool, ensure_ascii=False))

    prov = raw / "provenance.jsonl"
    net_files = [atom, sub, facts]
    rows = [{"url": f"https://example.sec.gov/{p.name}", "retrieved_at": "2026-07-07T12:00:00+00:00",
             "http_status": 200, "sha256": sha256_file(p), "path": str(p)} for p in net_files]
    prov.write_text("".join(json.dumps(r) + "\n" for r in rows))
    manifest = raw / "MANIFEST.sha256"
    all_files = net_files + [raw / "pool_extract.json", prov]
    manifest.write_text("".join(f"{sha256_file(p)}  {p}\n" for p in all_files))
    return raw, big


@pytest.fixture()
def env(tmp_path, monkeypatch):
    raw, big = build_fixture(tmp_path)
    monkeypatch.setattr(vc, "RAW_DIR", raw)
    monkeypatch.setattr(vc, "BIG_DIR", big)
    monkeypatch.setattr(vc, "MANIFEST", raw / "MANIFEST.sha256")
    monkeypatch.setattr(vc, "PROVENANCE", raw / "provenance.jsonl")
    monkeypatch.setattr(vc, "QUARANTINE", tmp_path / "quarantine/quarantine.json")
    return raw, big, tmp_path


def run(env_tuple):
    raw, big, tmp = env_tuple
    code = vc.main()
    q = json.loads((tmp / "quarantine/quarantine.json").read_text())
    return code, q


def test_clean_fixture_passes(env):
    code, q = run(env)
    assert code == 0 and q["verdict"] == "PASS", q["problems"]


def test_mutation_bitflip_caught_by_layer2(env):
    raw, big, _ = env
    p = big / f"facts/CIK{CIK}.json"
    b = bytearray(p.read_bytes())
    b[0] ^= 0xFF  # 변이 주입: 1바이트 반전
    p.write_bytes(bytes(b))
    code, q = run(env)
    assert code == 1
    assert any(pr["layer"] == "2-hash" and "불일치" in pr["reason"] for pr in q["problems"])


def test_mutation_unmanifested_file_caught_by_layer2(env):
    raw, big, _ = env
    (big / "submissions/CIK9999999999.json").write_text("{}")  # 몰래 추가된 파일
    code, q = run(env)
    assert code == 1
    assert any(pr["layer"] == "2-hash" and "매니페스트 밖" in pr["reason"] for pr in q["problems"])


def test_mutation_missing_provenance_caught_by_layer3(env):
    raw, big, _ = env
    prov = raw / "provenance.jsonl"
    lines = prov.read_text().splitlines()
    prov.write_text("\n".join(lines[:-1]) + "\n")  # facts 행 삭제
    code, q = run(env)
    assert code == 1
    assert any(pr["layer"] == "3-prov" and "provenance 부재" in pr["reason"]
               for pr in q["problems"])


def test_mutation_non200_status_caught_by_layer3(env):
    raw, big, _ = env
    prov = raw / "provenance.jsonl"
    rows = [json.loads(x) for x in prov.read_text().splitlines()]
    rows[0]["http_status"] = 429
    prov.write_text("".join(json.dumps(r) + "\n" for r in rows))
    code, q = run(env)
    assert code == 1
    assert any(pr["layer"] == "3-prov" and "HTTP 429" in pr["reason"] for pr in q["problems"])


def test_mutation_eligible_with_fails_caught_by_layer1(env):
    raw, big, _ = env
    pp = raw / "pool_extract.json"
    pool = json.loads(pp.read_text())
    pool["cases"]["T13"]["candidates"][CIK]["fails"] = ["E1 조작된 모순"]
    pp.write_text(json.dumps(pool))
    code, q = run(env)
    assert code == 1
    assert any(pr["layer"] == "1-shape" and "상호" not in pr["reason"]
               and "fails" in pr["reason"] for pr in q["problems"])


def test_mutation_silent_drop_caught_by_layer1(env):
    raw, big, _ = env
    pp = raw / "pool_extract.json"
    pool = json.loads(pp.read_text())
    pool["cases"]["T13"]["candidates"][CIK].update(eligible=False, fails=[])
    pp.write_text(json.dumps(pool))
    code, q = run(env)
    assert code == 1
    assert any(pr["layer"] == "1-shape" and "무침묵" in pr["reason"] for pr in q["problems"])


def test_mutation_missing_submissions_caught_by_layer4(env):
    raw, big, _ = env
    (big / f"submissions/CIK{CIK}.json").unlink()
    code, q = run(env)
    assert code == 1
    assert any(pr["layer"] == "4-cross" and "submissions 원시 부재" in pr["reason"]
               for pr in q["problems"])


def test_mutation_cutoff_drift_caught_by_layer4(env):
    raw, big, _ = env
    pp = raw / "pool_extract.json"
    pool = json.loads(pp.read_text())
    pool["cases"]["T13"]["cutoff"] = "2015-01-01"  # criteria 상수와 어긋난 컷오프
    pp.write_text(json.dumps(pool))
    code, q = run(env)
    assert code == 1
    assert any(pr["layer"] == "4-cross" and "컷오프 불일치" in pr["reason"]
               for pr in q["problems"])


def test_mutation_truncation_undercount_caught_by_layer4(env):
    raw, big, _ = env
    pp = raw / "pool_extract.json"
    pool = json.loads(pp.read_text())
    pool["cases"]["T13"]["candidates"][CIK]["truncated_by_S0_cap"] = True  # 기록 0과 모순
    pp.write_text(json.dumps(pool))
    code, q = run(env)
    assert code == 1
    assert any(pr["layer"] == "4-cross" and "절단 카운트" in pr["reason"]
               for pr in q["problems"])


def test_mutation_corrupt_json_caught(env):
    raw, big, _ = env
    pp = raw / "pool_extract.json"
    pp.write_text(pp.read_text()[:50])  # 절단 부패
    code, q = run(env)
    assert code == 1
    assert any("JSON 파싱" in pr["reason"] for pr in q["problems"])
