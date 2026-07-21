"""채점자 러너 (개정 #2 경로) — 폴백·멱등·중립 ID 규율 테스트 (subprocess 모킹)."""
import json
import os
import stat
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
sys.path.insert(0, str(REPO / "scoring"))

import cli_client  # noqa: E402
import grader_runner as gr  # noqa: E402

STUB = r'''#!/usr/bin/env python3
import json, os, sys
if sys.argv[1:] == ["--version"]:
    # 하네스 핀 강제 경로 (C3, D109) — call_ 기록 없이 버전만 응답
    sys.stdout.write(os.environ.get("STUB_VERSION", "STUB-VERSION-UNSET"))
    sys.exit(0)
stub_dir = os.environ["STUB_DIR"]
payload = sys.stdin.read()
n = len([f for f in os.listdir(stub_dir) if f.startswith("call_")])
with open(os.path.join(stub_dir, f"call_{n:02d}.json"), "w") as f:
    json.dump({"argv": sys.argv[1:], "stdin": payload}, f)
responses = json.load(open(os.path.join(stub_dir, "responses.json")))
r = responses[min(n, len(responses) - 1)]
sys.stdout.write(r if isinstance(r, str) else json.dumps(r))
'''

GRADE = {"dim1_probability_band": 2, "dim2_mechanism": None,
         "dim3_genre_mapping": {"mapped_genre": None, "score": None},
         "dim4_evidence_quality": 2, "memorization_suspect_condition2": False,
         "rationale": "test"}


def resp(structured=None, model="claude-fable-5", is_error=False, result="x"):
    body = {"type": "result", "is_error": is_error, "result": result,
            "session_id": "sess-g", "total_cost_usd": 0.0,
            "usage": {"input_tokens": 1, "output_tokens": 1},
            "modelUsage": {model: {"outputTokens": 1}}}
    if structured is not None:
        body["structured_output"] = structured
    return body


@pytest.fixture()
def stub(tmp_path, monkeypatch):
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
    # 하네스 핀 강제 (C3, D109): 핀 일치 버전 응답 + 프로세스 캐시 리셋
    monkeypatch.setenv("STUB_VERSION", f"{cli_client.HARNESS_PIN} (Claude Code)")
    monkeypatch.setattr(cli_client, "_harness_version_actual", None)
    monkeypatch.setattr(gr, "answer_key", lambda oid, *a, **k: {"group": "treatment",
                                                       "scheme_summary": "s",
                                                       "scheme_type": ["x"],
                                                       "manipulation_period": [None, None],
                                                       "genre_tag_row": None})

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


OUTPUT = {"case_id": "case_01", "misstatement_probability": 80}


def test_pin_success_no_fallback(stub, tmp_path):
    stub.set_responses(resp(GRADE))
    status = gr.grade_one("case_01", "TXX", OUTPUT, tmp_path / "g", tmp_path / "l", "note")
    assert status.startswith("OK") and "[fallback]" not in status
    grade = json.loads((tmp_path / "g" / "case_01.json").read_text(encoding="utf-8"))
    assert grade["_meta"]["grader_pin_used"] == gr.GRADER_PIN
    assert grade["_meta"]["fallback_used"] is False
    (call,) = stub.calls()
    assert call["argv"][call["argv"].index("--model") + 1] == gr.GRADER_PIN


def test_fallback_triggered_on_pin_failure_and_logged(stub, tmp_path):
    # 핀 모델 2회 실패(error) → 폴백 opus-4-8 성공. D6: 발동 기록.
    stub.set_responses(resp(is_error=True, result="API Error"),
                       resp(is_error=True, result="API Error"),
                       resp(GRADE, model=gr.GRADER_FALLBACK))
    status = gr.grade_one("case_01", "TXX", OUTPUT, tmp_path / "g", tmp_path / "l", "note")
    assert status.startswith("OK") and "[fallback]" in status
    grade = json.loads((tmp_path / "g" / "case_01.json").read_text(encoding="utf-8"))
    assert grade["_meta"]["fallback_used"] is True
    assert grade["_meta"]["grader_pin_used"] == gr.GRADER_FALLBACK
    models = [c["argv"][c["argv"].index("--model") + 1] for c in stub.calls()]
    assert models == [gr.GRADER_PIN, gr.GRADER_PIN, gr.GRADER_FALLBACK]


def test_double_failure_marks_case_fail_and_continues(stub, tmp_path):
    stub.set_responses(resp(is_error=True, result="API Error"))
    status = gr.grade_one("case_01", "TXX", OUTPUT, tmp_path / "g", tmp_path / "l", "note")
    assert status.startswith("FAIL")
    assert not (tmp_path / "g" / "case_01.json").exists()


def test_idempotent_skip_on_valid_existing_grade(stub, tmp_path):
    out = tmp_path / "g"
    out.mkdir()
    (out / "case_01.json").write_text(
        json.dumps({**GRADE, "_meta": {"case_id": "case_01"}}), encoding="utf-8")
    status = gr.grade_one("case_01", "TXX", OUTPUT, out, tmp_path / "l", "note")
    assert status.startswith("skip")
    assert stub.calls() == []


def test_grading_payload_contains_answer_key_and_output(stub, tmp_path):
    stub.set_responses(resp(GRADE))
    gr.grade_one("case_01", "TXX", OUTPUT, tmp_path / "g", tmp_path / "l", "note")
    (call,) = stub.calls()
    payload = json.loads(call["stdin"])
    assert set(payload) == {"answer_key", "evaluatee_output"}
    assert payload["evaluatee_output"]["case_id"] == "case_01"
