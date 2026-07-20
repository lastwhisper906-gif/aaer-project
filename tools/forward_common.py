"""forward 사이클 공용 헬퍼 (specs/FORWARD_WATCHLIST_V1.md §9, D100).

구독 전용 가드: owner plan 2026-07-20 §0.4 (zero-metered) — 종량 자격증명이
환경에 있으면 forward 도구는 기동을 거부한다. INVARIANT 4
(pipeline/cli_client.assert_no_metered_credentials)의 확장판.
"""
import datetime
import hashlib
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SEC_UA = {"User-Agent": "chaeper lastwhisper906@gmail.com"}  # fetch_primary_sources 규약
SCREENING_CUTOFF = "2026-11-15"          # specs/FORWARD_WATCHLIST_V1.md §2
EXECUTION_WINDOW_END = "2026-11-22"
MIN_SCORED = 11                          # §3-3 사전 등록 완료 분율 (12사 중 ≥11)
UNIVERSE_SIZE = 12

# 봉인 대상 파일 (§9 디렉토리 규범 — MANIFEST 자신·.ots는 제외)
SEALED_FILES = ["PROTOCOL.md", "universe.json", "source_manifest.json", "scores.json"]

METERED_CREDENTIAL_VARS = [
    "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY",
    "MISTRAL_API_KEY", "COHERE_API_KEY", "XAI_API_KEY", "DEEPSEEK_API_KEY",
]


def assert_subscription_only():
    """zero-metered 가드 — 종량 자격증명 존재 시 즉시 거부 (설명 출력)."""
    present = [v for v in METERED_CREDENTIAL_VARS if os.environ.get(v)]
    if present:
        raise RuntimeError(
            f"종량 API 자격증명 {present} 이(가) 환경에 존재한다.\n"
            "이 프로젝트의 모든 모델 실행은 구독 OAuth(claude -p + "
            "CLAUDE_CODE_OAUTH_TOKEN) 전용이다 (owner plan 2026-07-20 §0.4 "
            "zero-metered 명령, INVARIANT 4). 해당 변수를 unset 후 재실행하라. "
            "이 가드는 우발적 종량 과금을 기계적으로 차단한다.")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def evidence_files(cycle: Path):
    ev = cycle / "evidence"
    return sorted(p for p in ev.rglob("*") if p.is_file()) if ev.exists() else []


def manifest_text(cycle: Path) -> str:
    """봉인 매니페스트 본문 — 결정론적 순서 (§9)."""
    lines = []
    for name in SEALED_FILES:
        p = cycle / name
        if p.exists():
            lines.append(f"{sha256_file(p)}  {name}")
    for p in evidence_files(cycle):
        lines.append(f"{sha256_file(p)}  {p.relative_to(cycle)}")
    return "\n".join(lines) + "\n"


def parse_date(s: str) -> datetime.date:
    return datetime.date.fromisoformat(s[:10])


def fail(msg: str) -> "NoReturn":
    print(f"FAIL — {msg}")
    sys.exit(1)
