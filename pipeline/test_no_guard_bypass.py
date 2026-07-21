"""가드 우회 정적 스캔 (CLAUDE.md 방법론 규율 1: "우회 코드를 작성하지 않는다"의 기계적 강제).

pipeline/ 안의 모듈(피평가자 쪽 코드)은 cutoff_guard를 제외하고:
  1. 네트워크 라이브러리를 직접 import할 수 없다 — 모든 원격 로딩은
     load_document(loader=...) 콜백 주입으로만.
  2. candidates.json을 직접 참조할 수 없다 — 이 파일은 ground truth
     (scheme_summary, AAER 링크 등 정답지)를 포함하므로, 피평가자 코드가
     읽는 순간 look-ahead와 무관하게 백테스트가 오염된다.
     (cutoff_guard.load_registry는 컷오프 날짜만 추출해 노출 — 유일한 예외.)

규범이 아니라 테스트다: 위반 코드는 커밋 전에 여기서 깨진다.
"""
import re
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
EXEMPT = {"cutoff_guard.py"}  # 게이트웨이 본체만 예외

FORBIDDEN_PATTERNS = {
    "network import": re.compile(
        r"^\s*(import|from)\s+(requests|urllib|http\.client|httpx|aiohttp|socket)\b", re.M
    ),
    "candidates.json direct reference": re.compile(r"candidates\.json"),
    # 중립 ID ↔ 원본 매핑은 채점 전용(OV-001) — 피평가자 코드가 읽으면 그룹 소속 역산 가능
    "id_mapping direct reference": re.compile(r"id_mapping\.json"),
    # V7 (threat model): 피평가자 쪽 코드는 채점 모듈을 import할 수 없다 — 채점 자료
    # (정답 키·루브릭)의 역류 차단. 경로 문자열 언급(출력 저장 등)은 허용, import만 금지.
    "scoring import": re.compile(r"^\s*(import\s+scoring|from\s+scoring)\b", re.M),
    "raw aaer-data read": re.compile(r"aaer-data"),
}


def scannable_sources():
    for p in sorted(PIPELINE_DIR.glob("*.py")):
        if p.name in EXEMPT or p.name.startswith("test_"):
            continue
        yield p


def test_pipeline_modules_do_not_bypass_guard():
    violations = []
    for path in scannable_sources():
        source = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            for m in pattern.finditer(source):
                line_no = source[: m.start()].count("\n") + 1
                violations.append(f"{path.name}:{line_no} [{label}] {m.group(0).strip()}")
    assert not violations, (
        "cutoff_guard 우회 의심 코드 발견 — load_document(loader=...) 경유로 수정할 것:\n"
        + "\n".join(violations)
    )
