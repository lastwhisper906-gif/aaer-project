#!/usr/bin/env python3
"""lint_doc_counts.py — 문서-저장소 수치 정합 lint (Phase B3, D108).

파생 원천 (저장소 자체 — 문서가 아니라 코드/데이터가 기준):
  - 데이터 매니페스트 파일 수: data/manifests/aaer_data_manifest.json `file_count`
  - pytest 수집 수: `pytest pipeline tools scoring analysis --collect-only -q`
  - 재현 명령 목록: Makefile의 verify-public / verify-full 레시피 행

대상 문서: README.md · README.ko.md · REPRODUCING.md
  각 문서의 BEGIN/END-GENERATED 블록이 파생 렌더링과 정확히 일치해야 PASS.
  블록 밖의 `N files/파일` · `N passed` · `N tests collected` 패턴은
  파생값과 다르면 FAIL (수기 시점값 표류 방지 — 402/429 사건, REVIEW_CLAIMS_AUDIT).

갱신: `make docs-refresh` (= 본 스크립트 --write) — 블록 내용만 교체.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "data" / "manifests" / "aaer_data_manifest.json"
MAKEFILE = REPO / "Makefile"
DOCS = ["README.md", "README.ko.md", "REPRODUCING.md"]

BEGIN = "<!-- BEGIN-GENERATED: repro-facts (refresh: make docs-refresh; CI: tools/lint_doc_counts.py) -->"
END = "<!-- END-GENERATED: repro-facts -->"

PYTEST_ARGS = ["pipeline", "tools", "scoring", "analysis"]


def manifest_count() -> int:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    n = m["file_count"]
    if n != len(m["files"]):
        sys.exit(f"FAIL: 매니페스트 file_count({n}) ≠ files 항목 수({len(m['files'])})")
    return n


def pytest_collected() -> int:
    py = REPO / ".venv" / "bin" / "python"
    exe = str(py) if py.exists() else sys.executable
    out = subprocess.run(
        [exe, "-m", "pytest", *PYTEST_ARGS, "--collect-only", "-q"],
        cwd=REPO, capture_output=True, text=True,
    )
    m = re.search(r"(\d+) tests? collected", out.stdout)
    if not m:
        sys.exit(f"FAIL: pytest --collect-only 파싱 실패\n{out.stdout[-500:]}{out.stderr[-500:]}")
    return int(m.group(1))


def make_recipe(target: str) -> list[str]:
    lines = MAKEFILE.read_text(encoding="utf-8").splitlines()
    out, active = [], False
    for ln in lines:
        if re.match(rf"^{re.escape(target)}\s*:", ln):
            active = True
            continue
        if active:
            if ln.startswith("\t"):
                cmd = ln.strip()
                if not cmd.startswith("@"):  # corpus-check 안내 에코 블록 제외
                    out.append(cmd)
            elif ln.strip() and not ln.startswith("\t"):
                break
    if not out:
        sys.exit(f"FAIL: Makefile에서 타깃 {target} 레시피를 찾지 못함")
    return out


def render_block() -> str:
    n_manifest = manifest_count()
    n_tests = pytest_collected()
    pub = make_recipe("verify-public")
    full = make_recipe("verify-full")
    lines = [
        BEGIN,
        f"- data manifest: **{n_manifest} files** "
        "(`data/manifests/aaer_data_manifest.json` · `file_count`)",
        f"- pytest: **{n_tests} tests collected** (`{' '.join(PYTEST_ARGS)}`)",
        "- `make verify-public` (zero external data):",
        *[f"  - `{c}`" for c in pub],
        "- `make verify-full` (requires `~/aaer-data` corpus; see REPRODUCING.md §2):",
        *[f"  - `{c}`" for c in full],
        END,
    ]
    return "\n".join(lines)


def split_doc(text: str, doc: str) -> tuple[str, str, str]:
    if BEGIN not in text or END not in text:
        sys.exit(f"FAIL: {doc}에 BEGIN/END-GENERATED repro-facts 블록 부재")
    pre, rest = text.split(BEGIN, 1)
    block, post = rest.split(END, 1)
    return pre, BEGIN + block + END, post


STALE_PATTERNS = [
    (re.compile(r"(\d[\d,]*)\s*(?:files|파일)\b"), "manifest"),
    (re.compile(r"(\d[\d,]*)\s+passed\b"), "pytest"),
    (re.compile(r"(\d[\d,]*)\s+tests? collected\b"), "pytest"),
]


def scan_stale(outside_text: str, doc: str, n_manifest: int, n_tests: int) -> list[str]:
    errs = []
    for pat, kind in STALE_PATTERNS:
        for m in pat.finditer(outside_text):
            val = int(m.group(1).replace(",", ""))
            ref = n_manifest if kind == "manifest" else n_tests
            if val != ref:
                errs.append(
                    f"{doc}: 블록 밖 수기 수치 '{m.group(0)}' ≠ 파생값 {ref} ({kind})"
                )
    return errs


def main() -> None:
    write = "--write" in sys.argv
    expected = render_block()
    n_manifest = manifest_count()
    n_tests = pytest_collected()
    errs = []
    for doc in DOCS:
        p = REPO / doc
        text = p.read_text(encoding="utf-8")
        pre, block, post = split_doc(text, doc)
        if write:
            p.write_text(pre + expected + post, encoding="utf-8")
        elif block != expected:
            errs.append(f"{doc}: GENERATED 블록이 파생 렌더링과 불일치 — make docs-refresh 후 커밋")
        errs.extend(scan_stale(pre + post, doc, n_manifest, n_tests))
    if write:
        print(f"WROTE — {len(DOCS)}개 문서 블록 갱신 (manifest {n_manifest} · pytest {n_tests})")
        return
    if errs:
        print("FAIL — 문서-저장소 수치 불일치:")
        for e in errs:
            print(f"  - {e}")
        sys.exit(1)
    print(f"PASS — 문서 수치 정합 (manifest {n_manifest} · pytest {n_tests} · 명령 목록 일치)")


if __name__ == "__main__":
    main()
