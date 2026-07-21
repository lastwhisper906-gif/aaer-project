"""레지스트리 기반 블라인드·무결성 기계 검증기 (결정론, API 호출 0).

커밋 산출물만으로 (a) 각 실험의 채점 커밋이 라벨 결합보다 앞선다는 git
이력 증명, (b) 레지스트리 클래스별 실명·티커·정답지 마커 스캔,
(c) 등록된 모든 출력 표면의 카나리 GUID 스캔, (d) runs/ 전체와
runs/MANIFEST.sha256의 대조를 수행한다. perturbed > output > aux 우선순위와
스캔 표면은 scoring/experiment_registry.json만을 기준으로 한다.

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
REGISTRY_PATH = REPO / "scoring/experiment_registry.json"
ANSWER_KEY_MARKERS = ["aaer", "scheme_summary", "matched_case", "m_score",
                      "beneish", "dechow", "montier", "sloan", "piotroski"]
VOCAB_WARN_MARKERS = ["fraud", "manipulat"]
CANARIES = ["9fa11f98", "a2d69cfe"]
SUFFIXES = {"inc", "inc.", "corp", "corp.", "corporation", "company", "co",
            "co.", "ltd", "ltd.", "n.v.", "s.a.", "plc", "group", "holdings",
            "international", "technology", "technologies", "brands"}

FAILS: list[str] = []
WARNS: list[str] = []


def fail(msg: str) -> None:
    FAILS.append(msg)


def load_registry(root: Path = REPO) -> dict:
    return json.loads((root / "scoring/experiment_registry.json").read_text(encoding="utf-8"))


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, capture_output=True,
                          text=True, check=True).stdout


def check_history(root: Path = REPO, registry: dict | None = None) -> None:
    registry = registry or load_registry(root)
    for exp in registry["experiments"]:
        score, joined = exp["score_commit"], exp["label_join_commit"]
        if score != "UNKNOWN" and joined != "UNKNOWN":
            rc = subprocess.run(["git", "merge-base", "--is-ancestor", score, joined],
                                cwd=root, capture_output=True).returncode
            if rc:
                fail(f"(a) {exp['name']}: 채점 커밋 {score}이 라벨 결합 {joined}의 조상이 아님")
        artifacts = exp.get("label_join_artifacts", [])
        required = exp.get("blind_state_required", [])
        if not artifacts and not required:
            continue
        try:
            tree = set(git(root, "ls-tree", "-r", score, "--name-only").splitlines())
        except subprocess.CalledProcessError:
            fail(f"(a) {exp['name']}: 채점 커밋 {score} 트리를 읽지 못함")
            continue
        for path in artifacts:
            if path in tree:
                fail(f"(a) 라벨 결합 산출물 {path}이 채점 커밋 {score} 트리에 존재")
            intro = git(root, "log", "--diff-filter=A", "--format=%H", "--reverse", "--", path).splitlines()
            if not intro:
                fail(f"(a) {path} 도입 커밋을 이력에서 찾지 못함")
            elif subprocess.run(["git", "merge-base", "--is-ancestor", score, intro[0]],
                                cwd=root, capture_output=True).returncode:
                fail(f"(a) 채점 커밋이 {path} 도입 커밋({intro[0][:7]})의 조상이 아님")
        for path in required:
            if path not in tree:
                fail(f"(a) 채점 커밋 {score} 트리에 {path} 부재 — 블라인드 스냅샷 주장 불성립")


def _registered_paths(root: Path, registry: dict) -> dict[str, set[Path]]:
    matched = {kind: set() for kind in ("perturbed", "output", "aux")}
    for exp in registry["experiments"]:
        for kind in matched:
            for pattern in exp.get(f"{kind}_globs", []):
                matched[kind].update(p for p in root.glob(pattern) if p.is_file())
    return matched


def _discovered_paths(root: Path) -> set[Path]:
    paths = set((root / "runs").rglob("*.json")) if (root / "runs").is_dir() else set()
    for relative in ("pilot/runs", "pilot/grades", "scoring/grades"):
        base = root / relative
        if base.is_dir():
            paths.update(base.rglob("*.json"))
    scoring = root / "scoring"
    if scoring.is_dir():
        for base in scoring.glob("probe_results*"):
            if base.is_dir():
                paths.update(base.rglob("*.json"))
    return {p for p in paths if p.name != "MANIFEST.sha256"}


def _variant(name: str) -> str:
    value = name.lower().strip()
    if value.startswith("the "):
        value = value[4:]
    tokens = value.split()
    while tokens and tokens[-1].strip(",") in SUFFIXES:
        tokens.pop()
    value = " ".join(tokens).rstrip(",")
    # These singular/scope descriptors become trailing only after stripping the
    # registered suffix chain; unlike "Kraft Heinz", neither is a brand phrase.
    for descriptor in (" global", " brand"):
        if value.endswith(descriptor):
            value = value[:-len(descriptor)]
    return value


def derive_treatment_patterns(root: Path, exp: dict) -> tuple[re.Pattern, re.Pattern] | None:
    try:
        ids_doc = json.loads((root / exp["perturbed_treatment_ids"]).read_text(encoding="utf-8"))
        ids = [x["case_id"] for x in ids_doc["cases"]] if isinstance(ids_doc, dict) else ids_doc
        mapping_doc = json.loads((root / exp["names_mapping"]).read_text(encoding="utf-8"))
        mapping = mapping_doc["mapping"]
        candidates_doc = json.loads((root / exp["names_candidates"]).read_text(encoding="utf-8"))
        candidates = {x["case_id"]: x for x in candidates_doc["candidates"]}
        selected = []
        for case_id in ids:
            candidate_id = mapping[case_id]
            candidate = candidates[candidate_id]
            if not candidate.get("company_name") or not candidate.get("ticker"):
                raise KeyError(f"{case_id} 후보의 company_name/ticker")
            selected.append(candidate)
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        fail(f"(b) {exp.get('name', '<unnamed>')} 실험군 이름 파생 실패: {exc}")
        return None
    names = {str(c.get("company_name", "")).lower().strip() for c in selected}
    names.discard("")
    variants = {_variant(name) for name in names}
    variants.discard("")
    tickers = {str(c.get("ticker", "")).strip() for c in selected}
    tickers.discard("")
    if not names or not variants or not tickers:
        fail(f"(b) {exp.get('name', '<unnamed>')} 실험군 이름 또는 티커 집합이 비어 있음")
        return None
    name_re = re.compile("|".join(re.escape(x) for x in sorted(names | variants, key=len, reverse=True)))
    ticker_re = re.compile(r"\b(?:" + "|".join(re.escape(x) for x in sorted(tickers)) + r")\b")
    return name_re, ticker_re


def check_semantic_scans(root: Path = REPO, registry: dict | None = None) -> None:
    registry = registry or load_registry(root)
    registered = _registered_paths(root, registry)
    all_registered = set().union(*registered.values())
    for path in sorted(_discovered_paths(root) - all_registered):
        fail(f"unregistered output surface: {path.relative_to(root)}")

    patterns: dict[str, tuple[re.Pattern, re.Pattern] | None] = {}
    for exp in registry["experiments"]:
        if exp.get("perturbed_globs"):
            patterns[exp["name"]] = derive_treatment_patterns(root, exp)

    for path in sorted(all_registered):
        kind = next(k for k in ("perturbed", "output", "aux") if path in registered[k])
        text = path.read_text(encoding="utf-8")
        low = text.lower()
        relative = path.relative_to(root)
        if kind == "perturbed":
            for exp in registry["experiments"]:
                if path not in {p for pattern in exp.get("perturbed_globs", []) for p in root.glob(pattern) if p.is_file()}:
                    continue
                pair = patterns.get(exp["name"])
                if pair:
                    name_match = pair[0].search(low)
                    ticker_match = pair[1].search(text)
                    if name_match:
                        fail(f"(b) 교란 기록 {relative}에 실명 '{name_match.group(0)}'")
                    if ticker_match:
                        fail(f"(b) 교란 기록 {relative}에 티커 '{ticker_match.group(0)}'")
        if kind in ("perturbed", "output"):
            for marker in ANSWER_KEY_MARKERS:
                if marker in low:
                    fail(f"(b) 피평가자 출력 {relative}에 정답지 마커 '{marker}'")
            for marker in VOCAB_WARN_MARKERS:
                if marker in low:
                    WARNS.append(f"(b) 모델 어휘 '{marker}' — {relative} (누출 증거 아님)")
        for canary in CANARIES:
            if canary in low:
                fail(f"(c) 카나리 {canary} 출현 — {relative}")


def manifest_lines(root: Path = REPO) -> list[str]:
    lines = []
    for path in sorted((root / "runs").rglob("*")):
        if path.is_file() and path.name not in {"MANIFEST.sha256", ".DS_Store"}:
            lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(root).as_posix()}")
    return lines


def check_manifest(write: bool, root: Path = REPO) -> None:
    manifest = root / "runs/MANIFEST.sha256"
    current = manifest_lines(root)
    if write:
        manifest.write_text("\n".join(current) + "\n", encoding="utf-8")
        print(f"매니페스트 기록: {len(current)}파일 → {manifest.relative_to(root)}")
        return
    if not manifest.is_file():
        fail("(d) runs/MANIFEST.sha256 부재 — --write-manifest로 생성 후 커밋")
        return
    recorded = [line for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()]
    rec_set, cur_set = set(recorded), set(current)
    for line in sorted(rec_set - cur_set):
        fail(f"(d) 매니페스트 기재 파일 누락/변조: {line.split('  ')[1]}")
    for line in sorted(cur_set - rec_set):
        fail(f"(d) 매니페스트 미기재 파일 존재: {line.split('  ')[1]}")


def main() -> int:
    FAILS.clear()
    WARNS.clear()
    registry = load_registry(REPO)
    check_history(REPO, registry)
    check_semantic_scans(REPO, registry)
    check_manifest("--write-manifest" in sys.argv, REPO)
    for warning in WARNS:
        print(f"WARN {warning}")
    for failure in FAILS:
        print(f"FAIL {failure}")
    print(f"\n{'PASS' if not FAILS else 'FAIL'} — 이력 증명 + 실명/마커/카나리 스캔 + 매니페스트 대조")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
