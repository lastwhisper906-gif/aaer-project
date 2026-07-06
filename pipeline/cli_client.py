"""공용 모델 호출 모듈 (freeze 개정 #2) — Claude Code 구독 헤드리스 (`claude -p`).

러너 3종(runner / probe_runner / grader_runner)이 공유하는 유일한 호출 경로.
설계 계약 (decisions_log "freeze 개정 #2"의 소유자 지시문 PHASE 2):

  격리 (플래그 기반 — CLAUDE_CONFIG_DIR 방식은 구독 OAuth 차단이 실증되어 기각,
  decisions_log 개정 #2 부록 J13-b/c):
  - 호출별 작업 디렉토리 = 저장소 밖 fresh 임시 디렉토리 (호출 후 삭제).
  - --setting-sources "" + --strict-mcp-config + --tools "" + --system-prompt 대체
    → 설정·훅·MCP·내장 도구·메모리·CLAUDE.md 전면 차단 (게이트가 프로브로 실증).
  - ANTHROPIC_API_KEY가 환경에 존재하면 즉시 예외 (구독 OAuth 전용 — INVARIANT 4).
  - 하우스키핑 모델 호출 차단 env → 서빙 모델 = 핀 단독.
  - --max-turns 1 + --json-schema 구조화 출력.
  - 송출 전 페이로드 가드: forbid_markers가 주어지면 페이로드에 마커가 하나라도
    있으면 호출 없이 예외 (정답지·카나리의 피평가자 유출 차단 — 값 수준 스캔).

  신뢰성:
  - 스키마 실패·빈 응답: 동일 입력 1회 재시도. 2연속 실패 = FAIL 반환 (전체 중단 없음).
  - 레이트 리밋 감지: RateLimitedError — 러너가 재개 명령을 출력하고 중단 (멱등 재개).

  기록 (SR 11-7): 호출별 JSON 로그 — 플래그 전체·session_id·modelUsage(서빙 모델
  핀 대조)·토큰·total_cost_usd(참고 기록 전용 — 과금은 인증 경로가 결정)·타임스탬프·
  freeze 해시. 시크릿·토큰은 기록하지 않는다.
"""
from __future__ import annotations

import dataclasses
import datetime
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import jsonschema

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_BIN = "claude"
HARNESS_PIN = "2.1.201"  # freeze 개정 #2 하네스 핀 — 실측 불일치는 로그로 드러난다

DISALLOWED_TOOLS = ("Bash,Read,Edit,Write,Glob,Grep,WebFetch,WebSearch,"
                    "Task,NotebookEdit")

# 피평가자·프로브 페이로드 송출 전 값 수준 가드 (소문자 대조).
# test_build_payload.FORBIDDEN_PAYLOAD_SUBSTRINGS와 동일 계열 + 카나리 GUID.
# 채점 페이로드는 정답 키를 정당하게 포함하므로 이 목록을 적용하지 않는다.
EVALUATEE_FORBIDDEN_MARKERS = [
    "aaer", "fraud", "manipulat", "scheme_summary", "matched_case",
    "m_score", "beneish", "dechow", "montier", "sloan", "piotroski",
    "9fa11f98", "a2d69cfe",  # 카나리 GUID — 페이로드 반입 즉시 누출
]

# 주의 (J13-g): 정상 응답 본문의 재무 수치가 '429'를 포함해 오탐된 사례 실증 —
# 레이트 리밋 판정은 (a) 오류 응답에서만 수행하고 (b) 429는 HTTP 문맥을 요구한다.
RATE_LIMIT_PATTERNS = re.compile(
    r"rate.?limit|usage.?limit|limit (reached|will reset)|hit your limit"
    r"|too many requests|(status|http|error)[ :]*429|overloaded_error", re.I)


class PayloadGuardError(RuntimeError):
    """송출 전 가드 위반 — 페이로드에 금지 마커 존재. 호출은 일어나지 않았다."""


class RateLimitedError(RuntimeError):
    """레이트 리밋 감지 — 러너는 재개 명령을 출력하고 중단한다 (멱등)."""


@dataclasses.dataclass
class CallResult:
    ok: bool
    structured: dict | None      # 스키마 통과한 구조화 출력 (ok=True일 때)
    fail_reason: str | None      # ok=False일 때: schema_failure / empty / refusal / error / pin_mismatch
    served_models: list[str]     # modelUsage 키 (서버 보고 서빙 모델)
    pin_ok: bool                 # 서빙 모델 전부가 요청 핀과 일치하는가
    session_id: str | None
    usage: dict | None
    total_cost_usd: float | None
    attempts: int
    wall_seconds: float
    raw_result_text: str | None  # structured 부재 시 진단용 (성공 시 None — 로그 비대 방지)


def freeze_state() -> dict:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_ROOT,
                           capture_output=True, text=True, check=True).stdout.strip()
    return {"head": head, "clean_tree": not dirty}


# 멱등 재개를 위해 clean-tree 판정에서 무시하는 미추적 출력 경로 (기준 파일은 전부
# 추적 파일이므로, 추적 파일 변경은 여전히 무조건 거부 = freeze-commit-then-run 유지)
UNTRACKED_OUTPUT_PREFIXES = ("runs/", "logs/", "pilot/runs/", "pilot/grades/",
                             "scoring/grades/", "scoring/probe_results/")


def require_clean_tree() -> None:
    porcelain = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_ROOT,
                               capture_output=True, text=True, check=True).stdout
    bad = []
    for line in porcelain.splitlines():
        status, path = line[:2], line[3:]
        if status == "??" and path.startswith(UNTRACKED_OUTPUT_PREFIXES):
            continue  # 실행 산출물 — 멱등 재개 허용
        bad.append(line)
    if bad:
        raise RuntimeError("freeze-commit-then-run 위반 — 작업 트리 비정상:\n"
                           + "\n".join(bad))


def assert_no_metered_credentials() -> None:
    if "ANTHROPIC_API_KEY" in os.environ:
        raise RuntimeError(
            "ANTHROPIC_API_KEY가 환경에 존재 — 구독 OAuth 전용 실행 규약 위반 "
            "(freeze 개정 #2 INVARIANT 4). unset 후 재실행.")


def guard_payload(payload: str, forbid_markers: list[str]) -> None:
    low = payload.lower()
    hits = [m for m in forbid_markers if m.lower() in low]
    if hits:
        raise PayloadGuardError(f"페이로드 금지 마커 {hits} — 송출 중단 (호출 미발생)")


# 격리 = 플래그 기반 (2026-07-06 실증 확정 — decisions_log 개정 #2 부록 J13-c):
# CLAUDE_CONFIG_DIR 격리(빈 디렉토리·최소 시드 모두)는 구독 OAuth를 차단함이 실증되어
# 기각. 대신 기본 설정 디렉토리(=RP-04가 감사한 그 구성) + 플래그 전면 차단:
#   --setting-sources ""  → 설정 미로딩 (hooks·env 주입 차단)
#   --strict-mcp-config   → MCP 0개
#   --tools ""            → 내장 도구 0개
#   --system-prompt       → 기본 시스템 프롬프트 조립(메모리·CLAUDE.md) 전면 대체
#   cwd = repo 밖 임시     → 프로젝트 컨텍스트 원천 부재
# + 하우스키핑 모델 호출 차단 env (서빙 모델 = 핀 단독임을 게이트가 검증):
ISOLATION_ENV = {"DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1",
                 "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"}


def _served_models(model_usage: dict) -> list[str]:
    return sorted(model_usage.keys()) if isinstance(model_usage, dict) else []


def _pin_matches(pin: str, served: list[str]) -> bool:
    # 핀은 날짜 접미사 없는 정식 ID — 서버가 접미사 부가 문자열을 보고해도 인정.
    # 핀과 무관한 모델이 하나라도 서빙되면 불일치 (엄격 — 게이트에서 드러나야 한다).
    return bool(served) and all(m == pin or m.startswith(pin + "-") for m in served)


def _looks_rate_limited(*texts: str) -> bool:
    return any(RATE_LIMIT_PATTERNS.search(t or "") for t in texts)


def call_model(model: str,
               system_prompt: str,
               user_payload: str,
               schema: dict,
               log_dir: Path,
               log_name: str,
               forbid_markers: list[str] | None = None,
               timeout_seconds: int = 1800,
               extra_flags: list[str] | None = None) -> CallResult:
    """단일 모델 호출 — 격리 임시 디렉토리에서 `claude -p` 1회 (+1 재시도)."""
    assert_no_metered_credentials()
    if forbid_markers:
        guard_payload(user_payload, forbid_markers)
        guard_payload(system_prompt, forbid_markers)

    cmd = [CLAUDE_BIN, "-p",
           "--model", model,
           "--output-format", "json",
           # --json-schema 구조화 출력은 내부적으로 StructuredOutput 도구 호출 1턴을
           # 소모한다 — max-turns 1은 간헐적 error_max_turns 실증 (J13-d). 도구가
           # 전면 차단된 상태라 2턴째는 구조화 출력 마무리 외에 아무것도 될 수 없다.
           "--max-turns", "2",
           "--setting-sources", "",   # user/project/local 설정 미로딩 → hooks·env 주입 차단
           "--strict-mcp-config",     # --mcp-config 미제공 + 이 플래그 = MCP 0개 강제
           "--tools", "",             # 내장 도구 전면 비활성 (disallowedTools는 이중 방어)
           "--disallowedTools", DISALLOWED_TOOLS,
           "--system-prompt", system_prompt,
           "--json-schema", json.dumps(schema, ensure_ascii=False)]
    if extra_flags:
        cmd += extra_flags

    validator = jsonschema.Draft7Validator(schema)
    t0 = time.monotonic()
    last: dict = {"fail_reason": "empty", "raw": None, "obj": None}
    attempts = 0

    for attempts in (1, 2):
        work_dir = tempfile.mkdtemp(prefix="aaer-run-")
        env = dict(os.environ)
        env.update(ISOLATION_ENV)
        try:
            proc = subprocess.run(cmd, input=user_payload, cwd=work_dir, env=env,
                                  capture_output=True, text=True,
                                  timeout=timeout_seconds)

            def _rate_limit_check():  # 오류 경로에서만 호출 (J13-g — 정상 응답 오탐 차단)
                if _looks_rate_limited(proc.stdout[-2000:] if proc.stdout else "",
                                       proc.stderr[-2000:] if proc.stderr else ""):
                    raise RateLimitedError(
                        f"레이트 리밋 감지 (exit={proc.returncode}) — "
                        f"tail: {(proc.stderr or proc.stdout or '')[-300:]}")

            try:
                obj = json.loads(proc.stdout)
            except (json.JSONDecodeError, TypeError):
                _rate_limit_check()
                last = {"fail_reason": "empty",
                        "raw": (proc.stdout or "")[:1000] + (proc.stderr or "")[-500:],
                        "obj": None}
                continue
            last["obj"] = obj
            if obj.get("is_error"):
                _rate_limit_check()
                last = {"fail_reason": "error", "raw": str(obj.get("result"))[:1000], "obj": obj}
                continue
            structured = obj.get("structured_output")
            if structured is None:
                # 방어적 폴백: result 텍스트가 그대로 JSON일 수 있다
                try:
                    structured = json.loads(obj.get("result") or "")
                except (json.JSONDecodeError, TypeError):
                    reason = "refusal" if "refus" in str(obj.get("result", "")).lower() else "empty"
                    last = {"fail_reason": reason, "raw": str(obj.get("result"))[:1000], "obj": obj}
                    continue
            errors = list(validator.iter_errors(structured))
            if errors:
                last = {"fail_reason": "schema_failure",
                        "raw": "; ".join(e.message for e in errors[:5]), "obj": obj}
                continue
            wall = time.monotonic() - t0
            result = _finish(model, obj, structured, None, attempts, wall)
            _write_log(log_dir, log_name, cmd, model, result, None)
            return result
        finally:
            shutil.rmtree(work_dir, ignore_errors=True)

    wall = time.monotonic() - t0
    result = _finish(model, last.get("obj") or {}, None, last["fail_reason"], attempts, wall,
                     raw=last.get("raw"))
    _write_log(log_dir, log_name, cmd, model, result, last.get("raw"))
    return result


def _finish(model: str, obj: dict, structured: dict | None, fail_reason: str | None,
            attempts: int, wall: float, raw: str | None = None) -> CallResult:
    served = _served_models(obj.get("modelUsage") or {})
    pin_ok = _pin_matches(model, served)
    ok = structured is not None
    if ok and not pin_ok:
        ok, fail_reason = False, "pin_mismatch"
    return CallResult(ok=ok, structured=structured, fail_reason=fail_reason,
                      served_models=served, pin_ok=pin_ok,
                      session_id=obj.get("session_id"),
                      usage=obj.get("usage"),
                      total_cost_usd=obj.get("total_cost_usd"),
                      attempts=attempts, wall_seconds=round(wall, 1),
                      raw_result_text=None if structured is not None else raw)


def _write_log(log_dir: Path, log_name: str, cmd: list[str], model: str,
               r: CallResult, raw: str | None) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    flags = cmd[:]
    # 시스템 프롬프트·스키마 전문은 플래그 로그에서 축약 (원문은 freeze된 코드가 근거)
    for i, a in enumerate(flags):
        if len(a) > 400:
            flags[i] = a[:200] + f"...[{len(a)} chars]"
    (log_dir / f"{log_name}.json").write_text(json.dumps({
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "harness_pin": HARNESS_PIN,
        "flags": flags,
        "model_requested": model,
        "served_models": r.served_models,
        "pin_ok": r.pin_ok,
        "ok": r.ok,
        "fail_reason": r.fail_reason,
        "session_id": r.session_id,
        "usage": r.usage,
        "total_cost_usd_reference_only": r.total_cost_usd,
        "attempts": r.attempts,
        "wall_seconds": r.wall_seconds,
        "freeze": freeze_state(),
        "raw_tail": (raw or "")[:1000] if not r.ok else None,
    }, ensure_ascii=False, indent=2), encoding="utf-8")


def output_is_valid(path: Path, schema: dict) -> bool:
    """멱등 skip 판정: 출력 파일이 존재하고 스키마를 통과하는가."""
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    return not list(jsonschema.Draft7Validator(schema).iter_errors(data))
