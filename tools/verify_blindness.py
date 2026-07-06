"""블라인드·무결성 기계 검증기 (RP-06 B3) — 결정론, API 호출 0, CI 상시 실행.

커밋 산출물만으로 다음을 검증한다 (전 항목 커밋 산출물 의존 — f4f8f73
schema-only 관행의 skip 대상 아님):

(a) **git 이력 증명**: 채점 커밋 03b91aa의 트리에 라벨 결합 산출물
    (scoring/rp05_stats.json, review_packets/RP-05_results.md)이 없고, 채점
    원시 파일(runs/·scoring/grades/)은 있으며, 03b91aa가 라벨 결합 산출물
    도입 커밋의 조상임을 확인 — "채점 커밋이 id_mapping 개봉에 선행"
    (RP-05 §11)의 기계 증명. 주: 채점 파일 _meta의 original_id는 채점자
    정답 키 결합의 정당한 일부(mapping_access_note로 문서화)이며 검증
    대상 블라인드 주장은 '분석 시점 라벨 결합'이다.

(b) **교란 변형 기록의 실명 부재**: 교란 변형 피평가자 출력 전건
    (runs/perturbed/ + runs/hardening/draws/*/실험군 파일)에서 실험군 8사
    실명·티커 부재. 인지 프로브 출력은 제외 — company_guess에 실명이
    등장하는 것이 측정 그 자체다. 원본 변형 출력도 제외 — 페이로드에
    실명이 정당하게 포함됐다.
    **frozen 금지 마커** (cli_client.EVALUATEE_FORBIDDEN_MARKERS): 페이로드
    수준 강제는 송출 시점 guard_payload(frozen·테스트 존재)가 수행한다.
    커밋 산출물에서 검증 가능한 부분: 정답지 유래 마커(aaer·scheme_summary·
    matched_case·m_score·beneish·dechow·montier·sloan·piotroski)가 피평가자
    출력 전건에 부재. 'fraud'/'manipulat'은 모델 자체 어휘로 등장 가능 —
    WARN 전용 (누출 증거 아님, 건수만 보고).

(c) **카나리 GUID 부재**: 두 GUID(9FA11F98-…, A2D69CFE-…)가 모델 출력
    전건(runs/ 전체 — hardening 포함, scoring/grades/, scoring/probe_results/,
    pilot/{runs,grades})에 부재.

(d) **runs/ 변조 증거 매니페스트**: runs/ 이하 전 파일의 sha256 ↔
    runs/MANIFEST.sha256 대조 (누락·초과·불일치 전부 FAIL).
    갱신은 --write-manifest (신규 실행 산출물 커밋 시에만).

사용: python tools/verify_blindness.py [--write-manifest]   (실패 시 exit 1)
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GRADING_COMMIT = "03b91aa"
LABEL_JOIN_ARTIFACTS = ["scoring/rp05_stats.json", "review_packets/RP-05_results.md"]
BLIND_STATE_REQUIRED = ["runs/main/case_01.json", "scoring/grades/main/case_01.json"]

# 실험군 8 (교란 대상) — 실명·티커. 검증 목적상 이 파일에 상수로 전사
# (scoring/perturbed_cases.json과의 정합도 아래에서 대조).
TREATMENT_NAMES = ["comscore", "orthofix", "logitech", "monsanto", "hertz",
                   "iconix", "kraft heinz", "marvell"]
TREATMENT_TICKERS = ["SCOR", "OFIX", "LOGI", "MON", "HTZ", "ICON", "KHC", "MRVL"]

ANSWER_KEY_MARKERS = ["aaer", "scheme_summary", "matched_case", "m_score",
                      "beneish", "dechow", "montier", "sloan", "piotroski"]
VOCAB_WARN_MARKERS = ["fraud", "manipulat"]
CANARIES = ["9fa11f98", "a2d69cfe"]

FAILS: list[str] = []
WARNS: list[str] = []


def fail(msg):
    FAILS.append(msg)


def git(*args) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                          text=True, check=True).stdout


def check_history():
    tree = set(git("ls-tree", "-r", GRADING_COMMIT, "--name-only").splitlines())
    for p in LABEL_JOIN_ARTIFACTS:
        if p in tree:
            fail(f"(a) 라벨 결합 산출물 {p}이 채점 커밋 {GRADING_COMMIT} 트리에 존재")
    for p in BLIND_STATE_REQUIRED:
        if p not in tree:
            fail(f"(a) 채점 커밋 {GRADING_COMMIT} 트리에 {p} 부재 — 블라인드 스냅샷 주장 불성립")
    for p in LABEL_JOIN_ARTIFACTS:
        intro = git("log", "--diff-filter=A", "--format=%H", "--reverse", "--", p).splitlines()
        if not intro:
            fail(f"(a) {p} 도입 커밋을 이력에서 찾지 못함")
            continue
        rc = subprocess.run(["git", "merge-base", "--is-ancestor", GRADING_COMMIT, intro[0]],
                            cwd=REPO).returncode
        if rc != 0:
            fail(f"(a) 채점 커밋이 {p} 도입 커밋({intro[0][:7]})의 조상이 아님")


def perturbed_record_paths():
    """교란 변형 피평가자 출력 전건 (인지 프로브 출력 제외 — 문서 상단 사유)."""
    treat_ids = {c["case_id"] for c in json.loads(
        (REPO / "scoring/perturbed_cases.json").read_text(encoding="utf-8"))["cases"]}
    if len(treat_ids) != 8:
        fail(f"(b) perturbed_cases.json 실험군 수 {len(treat_ids)} ≠ 8")
    paths = sorted((REPO / "runs/perturbed").glob("case_*.json"))
    draws = REPO / "runs/hardening/draws"
    if draws.is_dir():
        for d in sorted(draws.iterdir()):
            paths += sorted(p for p in d.glob("case_*.json") if p.stem in treat_ids)
    return paths


def evaluatee_output_paths():
    roots = ["runs/main", "runs/perturbed", "pilot/runs"]
    paths = []
    for r in roots:
        paths += sorted((REPO / r).glob("case_*.json"))
    draws = REPO / "runs/hardening/draws"
    if draws.is_dir():
        for d in sorted(draws.iterdir()):
            paths += sorted(d.glob("case_*.json"))
    return paths


def all_model_output_paths():
    extra = []
    for r in ["scoring/grades/main", "scoring/grades/perturbed", "pilot/grades",
              "scoring/probe_results/recognition", "scoring/probe_results/verbatim",
              "runs/hardening/probe_recognition", "runs/hardening/regrade_opus"]:
        p = REPO / r
        if p.is_dir():
            extra += sorted(p.glob("case_*.json"))
    return evaluatee_output_paths() + extra


def check_blindness():
    name_re = re.compile("|".join(re.escape(n) for n in TREATMENT_NAMES))
    ticker_re = re.compile(r"\b(" + "|".join(TREATMENT_TICKERS) + r")\b")
    for p in perturbed_record_paths():
        text = p.read_text(encoding="utf-8")
        m = name_re.search(text.lower())
        if m:
            fail(f"(b) 교란 기록 {p.relative_to(REPO)}에 실명 '{m.group(0)}'")
        m = ticker_re.search(text)
        if m:
            fail(f"(b) 교란 기록 {p.relative_to(REPO)}에 티커 '{m.group(0)}'")
    for p in evaluatee_output_paths():
        low = p.read_text(encoding="utf-8").lower()
        for mk in ANSWER_KEY_MARKERS:
            if mk in low:
                fail(f"(b) 피평가자 출력 {p.relative_to(REPO)}에 정답지 마커 '{mk}'")
        for mk in VOCAB_WARN_MARKERS:
            if mk in low:
                WARNS.append(f"(b) 모델 어휘 '{mk}' — {p.relative_to(REPO)} (누출 증거 아님)")


def check_canary():
    for p in all_model_output_paths():
        low = p.read_text(encoding="utf-8").lower()
        for c in CANARIES:
            if c in low:
                fail(f"(c) 카나리 {c} 출현 — {p.relative_to(REPO)}")


def manifest_lines():
    lines = []
    for p in sorted((REPO / "runs").rglob("*")):
        if p.is_file() and p.name != "MANIFEST.sha256" and p.name != ".DS_Store":
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            lines.append(f"{h}  {p.relative_to(REPO).as_posix()}")
    return lines


def check_manifest(write: bool):
    mf = REPO / "runs/MANIFEST.sha256"
    current = manifest_lines()
    if write:
        mf.write_text("\n".join(current) + "\n", encoding="utf-8")
        print(f"매니페스트 기록: {len(current)}파일 → {mf.relative_to(REPO)}")
        return
    if not mf.is_file():
        fail("(d) runs/MANIFEST.sha256 부재 — --write-manifest로 생성 후 커밋")
        return
    recorded = [ln for ln in mf.read_text(encoding="utf-8").splitlines() if ln.strip()]
    rec_set, cur_set = set(recorded), set(current)
    for ln in sorted(rec_set - cur_set):
        fail(f"(d) 매니페스트 기재 파일 누락/변조: {ln.split('  ')[1]}")
    for ln in sorted(cur_set - rec_set):
        fail(f"(d) 매니페스트 미기재 파일 존재: {ln.split('  ')[1]}")


def main() -> int:
    write = "--write-manifest" in sys.argv
    check_history()
    check_blindness()
    check_canary()
    check_manifest(write)
    for w in WARNS:
        print(f"WARN {w}")
    for f_ in FAILS:
        print(f"FAIL {f_}")
    n_files = len(all_model_output_paths())
    print(f"\n{'PASS' if not FAILS else 'FAIL'} — 이력 증명 + 실명/마커/카나리 스캔"
          f" ({n_files}개 모델 출력 파일) + 매니페스트 대조")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
