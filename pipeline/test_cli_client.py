"""cli_client (freeze 개정 #2 실행층) 테스트 — subprocess 모킹 (stub `claude` 실행 파일).

검증 대상 계약:
  ① 핀 플래그 세트·격리 (repo 밖 cwd, CLAUDE_CONFIG_DIR 격리, stdin 페이로드)
  ② structured_output 파싱 + 스키마 검증
  ③ 재시도 1회 → 2연속 실패 = FAIL (전체 중단 없음)
  ④ 레이트 리밋 감지 = RateLimitedError
  ⑤ 서빙 모델 핀 불일치 = FAIL
  ⑥ 값 수준 송출 가드 — 변조 주입(mutation injection) 시 호출 자체가 일어나지 않는다
  ⑦ ANTHROPIC_API_KEY 존재 시 즉시 중단
  ⑧ 멱등 skip 판정
"""
import json
import os
import stat
import sys
from pathlib import Path

import pytest

import cli_client
import runner as runner_mod

REPO = Path(__file__).resolve().parent.parent

SCHEMA = {"type": "object", "additionalProperties": False,
          "required": ["answer"], "properties": {"answer": {"type": "string"}}}

STUB = r'''#!/usr/bin/env python3
import json, os, sys
stub_dir = os.environ["STUB_DIR"]
payload = sys.stdin.read()
n = len([f for f in os.listdir(stub_dir) if f.startswith("call_")])
with open(os.path.join(stub_dir, f"call_{n:02d}.json"), "w") as f:
    json.dump({"argv": sys.argv[1:], "cwd": os.getcwd(),
               "env_nonessential": os.environ.get("DISABLE_NON_ESSENTIAL_MODEL_CALLS"),
               "env_traffic": os.environ.get("CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"),
               "stdin": payload}, f)
responses = json.load(open(os.path.join(stub_dir, "responses.json")))
r = responses[min(n, len(responses) - 1)]
sys.stdout.write(r if isinstance(r, str) else json.dumps(r))
'''


def good_response(structured, model="claude-sonnet-5"):
    return {"type": "result", "subtype": "success", "is_error": False,
            "result": json.dumps(structured), "session_id": "sess-test",
            "total_cost_usd": 0.0, "usage": {"input_tokens": 10, "output_tokens": 5},
            "modelUsage": {model: {"outputTokens": 5}},
            "structured_output": structured}


@pytest.fixture()
def stub(tmp_path, monkeypatch):
    """PATH 맨 앞에 stub `claude`를 심고, 호출 기록 디렉토리를 돌려준다."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    exe = bin_dir / "claude"
    exe.write_text(STUB, encoding="utf-8")
    exe.chmod(exe.stat().st_mode | stat.S_IXUSR)
    stub_dir = tmp_path / "stub"
    stub_dir.mkdir()
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("STUB_DIR", str(stub_dir))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    class Stub:
        dir = stub_dir

        @staticmethod
        def set_responses(*objs):
            (stub_dir / "responses.json").write_text(json.dumps(list(objs)), encoding="utf-8")

        @staticmethod
        def calls():
            return [json.loads(p.read_text(encoding="utf-8"))
                    for p in sorted(stub_dir.glob("call_*.json"))]

    return Stub


def _call(log_dir, **kw):
    return cli_client.call_model("claude-sonnet-5", "SYSTEM PROMPT", '{"case": 1}',
                                 SCHEMA, log_dir=log_dir, log_name="t", **kw)


# ① 플래그 세트 + 격리
def test_pinned_flags_isolated_cwd_and_config(stub, tmp_path):
    stub.set_responses(good_response({"answer": "x"}))
    r = _call(tmp_path / "logs")
    assert r.ok and r.structured == {"answer": "x"}
    (call,) = stub.calls()
    argv = call["argv"]
    assert argv[0] == "-p"
    for flag, val in [("--model", "claude-sonnet-5"), ("--output-format", "json"),
                      ("--max-turns", "2"),  # 구조화 출력 도구 왕복 1턴 포함 (J13-d)
                      ("--setting-sources", ""), ("--tools", ""),
                      ("--disallowedTools", cli_client.DISALLOWED_TOOLS),
                      ("--system-prompt", "SYSTEM PROMPT")]:
        assert argv[argv.index(flag) + 1] == val, flag
    assert json.loads(argv[argv.index("--json-schema") + 1]) == SCHEMA
    assert "--strict-mcp-config" in argv, "MCP 0개 강제 플래그 누락"
    assert call["stdin"] == '{"case": 1}'
    # 격리: 작업 디렉토리는 저장소 밖 임시 + 하우스키핑 모델 호출 차단 env
    assert not Path(call["cwd"]).resolve().is_relative_to(REPO)
    assert call["env_nonessential"] == "1" and call["env_traffic"] == "1"
    # 로그 계약 (SR 11-7)
    log = json.loads((tmp_path / "logs" / "t.json").read_text(encoding="utf-8"))
    assert log["session_id"] == "sess-test" and log["pin_ok"] is True
    assert log["served_models"] == ["claude-sonnet-5"]
    assert "freeze" in log and log["harness_pin"] == cli_client.HARNESS_PIN


# ② + ③ 재시도·2연속 실패
def test_schema_failure_retries_once_then_fails(stub, tmp_path):
    stub.set_responses(good_response({"wrong": 1}))  # 스키마 위반 반복
    r = _call(tmp_path / "logs")
    assert not r.ok and r.fail_reason == "schema_failure" and r.attempts == 2
    assert len(stub.calls()) == 2, "동일 입력 정확히 1회 재시도"


def test_second_attempt_success(stub, tmp_path):
    stub.set_responses(good_response({"wrong": 1}), good_response({"answer": "ok"}))
    r = _call(tmp_path / "logs")
    assert r.ok and r.attempts == 2 and r.structured == {"answer": "ok"}


def test_empty_stdout_counts_as_failure(stub, tmp_path):
    stub.set_responses("", "")
    r = _call(tmp_path / "logs")
    assert not r.ok and r.fail_reason == "empty" and r.attempts == 2


# ④ 레이트 리밋
def test_rate_limit_raises_for_idempotent_resume(stub, tmp_path):
    stub.set_responses("You've reached your usage limit. Your limit will reset at 3pm.")
    with pytest.raises(cli_client.RateLimitedError):
        _call(tmp_path / "logs")


def test_error_response_with_429_status_is_rate_limit(stub, tmp_path):
    stub.set_responses(json.dumps({"type": "result", "is_error": True,
                                   "result": "API Error: status 429 too many requests"}))
    with pytest.raises(cli_client.RateLimitedError):
        _call(tmp_path / "logs")


def test_successful_response_containing_429_number_is_not_rate_limit(stub, tmp_path):
    """J13-g 회귀: 정상 응답 본문의 재무 수치 '84,429' 등이 레이트 리밋으로 오탐되면 안 된다."""
    stub.set_responses(good_response({"answer": "Revenues=84,429 (FY2014); limit of detection"}))
    r = _call(tmp_path / "logs")
    assert r.ok and "429" in r.structured["answer"]


# ⑤ 서빙 모델 핀 불일치
def test_served_model_pin_mismatch_is_fail(stub, tmp_path):
    stub.set_responses(good_response({"answer": "x"}, model="claude-haiku-4-5"))
    r = _call(tmp_path / "logs")
    assert not r.ok and r.fail_reason == "pin_mismatch"
    assert r.served_models == ["claude-haiku-4-5"]


def test_dated_suffix_of_pin_is_accepted(stub, tmp_path):
    stub.set_responses(good_response({"answer": "x"}, model="claude-sonnet-5-20260203"))
    r = _call(tmp_path / "logs")
    assert r.ok and r.pin_ok


# ⑥ 값 수준 송출 가드 — 변조 주입 시 호출 미발생
@pytest.mark.parametrize("marker", ["9FA11F98-6380-4BF5-AB3C-8542459ACA6F",
                                    "A2D69CFE-CA8A-4DE1-8393-5B225099299B",
                                    "scheme_summary", "beneish", "AAER-1272"])
def test_mutation_injected_payload_never_leaves(stub, tmp_path, marker):
    clean = json.dumps({"case": {"ticker": "ZZZZ"}, "series": [1, 2, 3]})
    mutated = clean[:-1] + f', "x": "{marker}"}}'
    with pytest.raises(cli_client.PayloadGuardError):
        cli_client.call_model("claude-sonnet-5", "SYSTEM", mutated, SCHEMA,
                              log_dir=tmp_path / "logs", log_name="t",
                              forbid_markers=cli_client.EVALUATEE_FORBIDDEN_MARKERS)
    assert stub.calls() == [], "가드 위반 페이로드가 프로세스 경계를 넘음"


def test_clean_payload_passes_guard(stub, tmp_path):
    stub.set_responses(good_response({"answer": "x"}))
    r = cli_client.call_model("claude-sonnet-5", "SYSTEM", '{"revenue": 100}', SCHEMA,
                              log_dir=tmp_path / "logs", log_name="t",
                              forbid_markers=cli_client.EVALUATEE_FORBIDDEN_MARKERS)
    assert r.ok


# ⑦ 종량 자격 증명 차단
def test_api_key_presence_aborts_before_any_call(stub, tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-not-a-real-key")
    with pytest.raises(RuntimeError, match="구독 OAuth 전용"):
        _call(tmp_path / "logs")
    assert stub.calls() == []


# ⑧ 멱등 skip
def test_output_is_valid_gates_idempotent_skip(tmp_path):
    p = tmp_path / "case_01.json"
    assert not cli_client.output_is_valid(p, SCHEMA)          # 부재
    p.write_text("not json", encoding="utf-8")
    assert not cli_client.output_is_valid(p, SCHEMA)          # 파손
    p.write_text(json.dumps({"wrong": 1}), encoding="utf-8")
    assert not cli_client.output_is_valid(p, SCHEMA)          # 스키마 위반
    p.write_text(json.dumps({"answer": "x"}), encoding="utf-8")
    assert cli_client.output_is_valid(p, SCHEMA)              # 유효 → skip


def test_runner_skips_existing_valid_output(stub, tmp_path):
    """러너 멱등성: 유효한 기존 출력이 있으면 모델 호출이 일어나지 않는다."""
    case = {"case_id": "case_99", "ticker": "ZZZZ", "cik": "0000000000",
            "company_name": "Nowhere Corp", "cutoff_date": "2020-01-01"}
    out_dir = tmp_path / "runs"
    out_dir.mkdir()
    valid = {
        "case_id": "case_99", "run_id": "original-case_99-r1",
        "model": "claude-sonnet-5", "pipeline_version": "x" * 40,
        "run_timestamp": "2026-07-06T00:00:00+00:00",
        "documents_used": [{"accession_no": "a", "form_type": "10-K",
                            "filing_date": "2019-01-01"}],
        "checklist": [{"item_id": "CL1", "question": "q", "finding": "no_flag",
                       "confidence": "low",
                       "evidence": [{"quote": "concept=1 (FY)", "source_accession_no": "a",
                                     "location": "tag"}]}],
        "misstatement_probability": 10,
        "mechanism_hypotheses": [],
        "overall": {"risk_tier": "clear", "top_signals": []},
    }
    (out_dir / "case_99.json").write_text(json.dumps(valid), encoding="utf-8")
    res = runner_mod.run_case(case, False, out_dir, tmp_path / "logs")
    assert res["status"].startswith("skip")
    assert stub.calls() == [], "멱등 skip인데 호출 발생"
