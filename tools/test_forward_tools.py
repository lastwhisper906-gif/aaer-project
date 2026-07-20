"""forward 봉인 도구의 오프라인 테스트 (spec §11, D100). 네트워크 0·호출 0."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import forward_common as fc
import forward_prepare
import forward_seal
import forward_validate
import forward_outcome_append


def make_universe(n=12):
    sel = [{"record_id": f"fw001-r{i:02d}", "cik": f"{1000+i:010d}", "ticker": f"TK{i:02d}",
            "name": f"Test Co {i}", "sic": "3674", "float_usd": 2e9 + i} for i in range(1, n + 1)]
    return {"selected": sel, "alternates": [], "rule_ref": "docs/UNIVERSE_SELECTION.md#§6",
            "enumerated_at": "2026-07-20", "candidate_count": n, "excluded_by_reason": {}}


def make_record(rid, score=45, suff="sufficient"):
    state = "abstain" if suff == "insufficient" else (
        "flag" if score >= 70 else "review" if score >= 40 else "no_flag")
    return {"record_id": rid, "company": {"name": "Test", "ticker": "T", "cik": "1"},
            "misstatement_risk_score": score, "decision_state": state,
            "evidence_sufficiency": suff, "assessment_confidence": "medium",
            "top_signals": ["s"], "benign_alternative_explanations": ["b"],
            "affected_account_areas": ["rev"], "cited_sources": ["0000000000-26-000001"],
            "model_id": "claude-sonnet-5", "prompt_sha256": "x", "schema_sha256": "y",
            "scored_at": "2026-11-15"}


@pytest.fixture
def cycle(tmp_path):
    c = tmp_path / "cycle_t"
    (c / "evidence").mkdir(parents=True)
    fc.write_json(c / "universe.json", make_universe())
    fc.write_json(c / "source_manifest.json", {"sources": [
        {"url": "https://data.sec.gov/x", "filing_date": "2026-11-14",
         "retrieval_date": "2026-11-15", "sha256": "abc", "description": "d"}]})
    fc.write_json(c / "scores.json", {"records": [
        make_record(f"fw001-r{i:02d}") for i in range(1, 13)]})
    (c / "PROTOCOL.md").write_text("proto", encoding="utf-8")
    (c / "outcome_updates.jsonl").write_text("", encoding="utf-8")
    return c


# ── 구독 전용 가드 ────────────────────────────────────────────────────────

def test_guard_refuses_metered_credentials(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    with pytest.raises(RuntimeError, match="구독 OAuth"):
        fc.assert_subscription_only()
    monkeypatch.delenv("ANTHROPIC_API_KEY")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    with pytest.raises(RuntimeError):
        fc.assert_subscription_only()


# ── universe 정합 ─────────────────────────────────────────────────────────

def test_universe_checks_catch_violations():
    u = make_universe(11)
    assert any("≠ 12" in e for e in forward_prepare.check_universe(u))
    u = make_universe()
    u["selected"][1]["cik"] = u["selected"][0]["cik"]
    assert any("중복 CIK" in e for e in forward_prepare.check_universe(u))
    u = make_universe()
    u["selected"][0]["float_usd"] = 5e8
    assert any("$1B" in e for e in forward_prepare.check_universe(u))
    assert forward_prepare.check_universe(make_universe()) == []


# ── 컷오프·완결성·서수 컷 검증 ────────────────────────────────────────────

def test_validate_passes_good_cycle(cycle):
    assert forward_validate.validate(cycle) == []


def test_validate_catches_cutoff_violation(cycle):
    sm = fc.read_json(cycle / "source_manifest.json")
    sm["sources"][0]["filing_date"] = "2026-11-16"
    fc.write_json(cycle / "source_manifest.json", sm)
    assert any("cutoff" in e for e in forward_validate.validate(cycle))


def test_validate_completion_fraction(cycle):
    sc = fc.read_json(cycle / "scores.json")
    # 11 scored + 1 not_scored → PASS (사전 등록 ≥11/12)
    sc["records"][11] = {"record_id": "fw001-r12", "status": "not_scored",
                         "company": {"name": "Test"}}
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle) == []
    # 10 scored → FAIL
    sc["records"][10] = {"record_id": "fw001-r11", "status": "not_scored",
                         "company": {"name": "Test"}}
    fc.write_json(cycle / "scores.json", sc)
    assert any("완료 분율" in e for e in forward_validate.validate(cycle))


def test_validate_decision_state_machine_consistency(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["misstatement_risk_score"] = 80  # state는 review 그대로 → 불일치
    fc.write_json(cycle / "scores.json", sc)
    assert any("서수 컷" in e for e in forward_validate.validate(cycle))


def test_validate_abstain_rule(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0] = make_record("fw001-r01", score=90, suff="insufficient")
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle) == []  # insufficient→abstain이 정답


def test_validate_universe_score_bijection(cycle):
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["record_id"] = "fw001-r99"
    fc.write_json(cycle / "scores.json", sc)
    errs = forward_validate.validate(cycle)
    assert any("누락" in e for e in errs) and any("유니버스 밖" in e for e in errs)


# ── 봉인·검증 왕복 ────────────────────────────────────────────────────────

def run_seal(cycle, capsys=None):
    sys.argv = ["forward_seal.py", "--cycle", str(cycle)]
    return forward_seal.main()


def test_seal_verify_roundtrip_and_tamper(cycle, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    assert forward_seal.main() == 0
    assert (cycle / "MANIFEST.sha256").exists() and (cycle / "SEAL_RECORD.md").exists()

    import forward_verify_seal
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    assert forward_verify_seal.main() == 0

    # 변조 검출
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0]["misstatement_risk_score"] = 44
    fc.write_json(cycle / "scores.json", sc)
    assert forward_verify_seal.main() == 1
    out = capsys.readouterr().out
    assert "변조됨: scores.json" in out


def test_reseal_refused(cycle, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    assert forward_seal.main() == 0
    with pytest.raises(SystemExit):
        forward_seal.main()  # MANIFEST 존재 → 거부 (spec §3-5)


def test_seal_refused_on_invalid_cycle(cycle, monkeypatch):
    (cycle / "source_manifest.json").unlink()
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle)])
    with pytest.raises(SystemExit):
        forward_seal.main()


# ── 결과 append-only ─────────────────────────────────────────────────────

def test_outcome_append_chains_previous_label(cycle, monkeypatch):
    base = ["x", "--cycle", str(cycle), "--record-id", "fw001-r01",
            "--event-date", "2027-03-02", "--event-public-date", "2027-03-02",
            "--source", "acc-x", "--reviewer", "owner", "--rationale", "r"]
    monkeypatch.setattr(sys, "argv", base + ["--event-type", "item_402_nonreliance",
                                             "--new-label", "item_402_nonreliance"])
    scores_before = (cycle / "scores.json").read_bytes()
    assert forward_outcome_append.main() == 0
    monkeypatch.setattr(sys, "argv", base + ["--event-type", "aaer_or_final_enforcement",
                                             "--new-label", "aaer_or_final_enforcement"])
    assert forward_outcome_append.main() == 0
    lines = [json.loads(l) for l in
             (cycle / "outcome_updates.jsonl").read_text().splitlines()]
    assert len(lines) == 2
    assert lines[0]["previous_label"] == "none_observed"
    assert lines[1]["previous_label"] == "item_402_nonreliance"
    assert (cycle / "scores.json").read_bytes() == scores_before  # 원 점수 무접촉


# ── scores 조립 (사전 등록 유도 규칙) ─────────────────────────────────────

def test_assemble_derivation_rules():
    import forward_assemble as fa
    mk = lambda finding, conf: {"finding": finding, "confidence": conf}
    assert fa.derive_sufficiency([mk("flag", "high")] * 10) == "sufficient"
    assert fa.derive_sufficiency([mk("insufficient_data", "low")] * 3
                                 + [mk("flag", "high")] * 7) == "partial"
    assert fa.derive_sufficiency([mk("insufficient_data", "low")] * 6
                                 + [mk("flag", "high")] * 4) == "insufficient"
    assert fa.derive_confidence([mk("f", "high")] * 3) == "high"
    assert fa.derive_confidence([mk("f", "high"), mk("f", "low")]) == "medium"
    assert fa.derive_state(70, "sufficient") == "flag"
    assert fa.derive_state(69, "sufficient") == "review"
    assert fa.derive_state(39, "partial") == "no_flag"
    assert fa.derive_state(95, "insufficient") == "abstain"


def test_assemble_record_roundtrips_validate(cycle):
    import forward_assemble as fa
    meta = {"record_id": "fw001-r01", "name": "Test Co", "ticker": "T", "cik": "1"}
    out = {"misstatement_probability": 72, "model": "claude-sonnet-5",
           "run_id": "x", "run_timestamp": "2026-11-15T00:00:00Z",
           "checklist": [{"finding": "flag", "confidence": "high"}] * 5,
           "mechanism_hypotheses": [{"affected_line_items": ["revenue", "AR"]}],
           "overall": {"top_signals": ["CL1"]},
           "documents_used": [{"accession_no": "0000000000-26-000001"}]}
    r = fa.assemble_record(meta, out)
    assert r["misstatement_risk_score"] == 72 and r["decision_state"] == "flag"
    assert r["affected_account_areas"] == ["revenue", "AR"]
    assert fa.assemble_record(meta, None)["status"] == "not_scored"
    # 조립 레코드가 forward_validate 검사를 통과하는 형태인지
    sc = fc.read_json(cycle / "scores.json")
    sc["records"][0] = r
    fc.write_json(cycle / "scores.json", sc)
    assert forward_validate.validate(cycle) == []


def test_outcome_append_rejects_unknown_record(cycle, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["x", "--cycle", str(cycle),
                                      "--record-id", "fw001-r99", "--event-date", "d",
                                      "--event-public-date", "d", "--event-type",
                                      "sec_complaint", "--source", "s", "--new-label",
                                      "sec_complaint", "--reviewer", "o", "--rationale", "r"])
    with pytest.raises(SystemExit):
        forward_outcome_append.main()
