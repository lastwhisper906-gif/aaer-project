"""~/aaer-data 무결성 매니페스트 — 생성(--write)·검증(기본)·자체점검(--schema-only).

배경: 2026-07-05 ~/aaer-data 전체가 조용히 소실된 사고 (daily_log/2026-07-05.md).
git 밖 원문 사본은 소실이 조용히 일어나므로, 커밋된 SHA-256 기준선과 대조해
복원본의 동일성을 기계로 확인한다. 매니페스트는 월요일 도시에 표본 점검의
참조본이기도 하다.

모드:
  --write        ~/aaer-data 전수 스캔 → data/manifests/aaer_data_manifest.json 생성.
                 source_url은 tools/fetch_primary_sources.py의 URL 로직(aaer_url,
                 EXTRA_DOCS, 저장된 HTML의 1-hop 링크, submissions 파일명)을 재사용해
                 역산한다. 로컬 파생물(.txt 추출본)은 source_url 없이 derived_from 기록.
  (기본)         디스크 전수 재해시 → 매니페스트와 대조. 누락/추가/해시 불일치 하나라도
                 있으면 exit 1 (fail-closed). ~/aaer-data 부재도 실패다 — 그게 사고다.
  --schema-only  매니페스트 파일 자체의 정합성만 점검 (CI용 — 러너에는 원본이 없다).

fetched_at은 파일 mtime(실제 수집 시각)의 기록이며 대조 항목이 아니다 —
복원 시 mtime은 달라져도 내용 해시가 같으면 동일본이다.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_primary_sources import (  # noqa: E402
    DATA_DIR,
    EXTRA_CIKS,
    EXTRA_DOCS,
    linked_litigation_docs,
    slug,
)

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "data" / "manifests" / "aaer_data_manifest.json"
REQUIRED_KEYS = {"path", "size", "sha256", "fetched_at", "source_url"}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def candidate_urls() -> dict[str, list[str]]:
    """ticker → 그 케이스에서 시도된 문서 URL 전부 (fetch 스크립트와 동일 로직)."""
    candidates = json.loads(
        (REPO / "data/candidates/candidates.json").read_text(encoding="utf-8")
    )["candidates"]
    by_ticker: dict[str, list[str]] = {}
    for c in candidates:
        ticker = c["ticker"].split("/")[0]
        urls = by_ticker.setdefault(ticker, [])
        if c.get("aaer_url"):
            urls.append(c["aaer_url"])
        urls += EXTRA_DOCS.get(c["case_id"], [])
    return by_ticker


def url_basenames(url: str) -> set[str]:
    """save_document의 확장자 보정을 역산 — url이 만들 수 있는 파일명 후보들."""
    base = slug(url)
    names = {base}
    if not base.lower().endswith(".pdf"):
        names.add(base + ".pdf")
    if not base.lower().endswith((".htm", ".html", ".json")):
        names.add(base + ".html")
    return names


def build_manifest() -> dict:
    if not DATA_DIR.is_dir():
        sys.exit(f"FAIL: {DATA_DIR} 부재 — 생성할 대상이 없다")

    # 1) 티커별 직접 URL + 저장된 HTML에서 1-hop 링크 복원 → 파일명 후보 → URL 매핑
    by_ticker = candidate_urls()
    for ticker, urls in by_ticker.items():
        for html in sorted((DATA_DIR / ticker).glob("*.htm*")):
            for u in linked_litigation_docs(
                html.read_text(encoding="utf-8", errors="replace")
            ):
                if u not in urls:
                    urls.append(u)

    files = []
    unattributed = []
    for path in sorted(DATA_DIR.rglob("*")):
        if not path.is_file() or path.name == ".DS_Store":
            continue
        rel = path.relative_to(DATA_DIR)
        ticker = rel.parts[0]
        entry = {
            "path": str(rel),
            "size": path.stat().st_size,
            "sha256": sha256_of(path),
            "fetched_at": datetime.fromtimestamp(
                path.stat().st_mtime, tz=timezone.utc
            ).isoformat(timespec="seconds"),
            "source_url": None,
        }
        if path.suffix == ".txt":  # pdf/html에서 로컬 추출한 파생물
            entry["derived_from"] = str(rel)[: -len(".txt")]
        elif rel.parts[1] == "edgar":
            entry["source_url"] = f"https://data.sec.gov/submissions/{path.name}"
        else:
            for u in by_ticker.get(ticker, []):
                if path.name in url_basenames(u):
                    entry["source_url"] = u
                    break
            if entry["source_url"] is None:
                unattributed.append(str(rel))
        files.append(entry)

    if unattributed:  # 출처 불명 파일은 조용히 넘기지 않는다
        print(f"WARN: source_url 역산 실패 {len(unattributed)}건:", file=sys.stderr)
        for p in unattributed:
            print(f"  {p}", file=sys.stderr)

    return {
        "manifest_version": 1,
        "root": "~/aaer-data",
        "generated_at": datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
        "generated_by": "tools/verify_manifest.py --write",
        "file_count": len(files),
        "total_bytes": sum(f["size"] for f in files),
        "files": files,
    }


def load_manifest() -> dict:
    if not MANIFEST.is_file():
        sys.exit(f"FAIL: {MANIFEST.relative_to(REPO)} 부재 — 먼저 --write로 생성")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def check_schema(m: dict) -> list[str]:
    """매니페스트 자체 정합성 (원본 디스크 없이 가능한 점검)."""
    errors = []
    if m.get("manifest_version") != 1:
        errors.append(f"manifest_version != 1: {m.get('manifest_version')}")
    files = m.get("files", [])
    if m.get("file_count") != len(files):
        errors.append(f"file_count {m.get('file_count')} != files {len(files)}")
    if m.get("total_bytes") != sum(f.get("size", 0) for f in files):
        errors.append("total_bytes가 size 합과 불일치")
    seen = set()
    for f in files:
        missing = REQUIRED_KEYS - f.keys()
        if missing:
            errors.append(f"{f.get('path', '?')}: 필수 키 누락 {sorted(missing)}")
        if not isinstance(f.get("sha256"), str) or len(f.get("sha256", "")) != 64:
            errors.append(f"{f.get('path', '?')}: sha256 형식 오류")
        if f.get("path") in seen:
            errors.append(f"중복 path: {f['path']}")
        seen.add(f.get("path"))
        if f.get("source_url") is None and "derived_from" not in f:
            errors.append(f"{f.get('path', '?')}: source_url도 derived_from도 없음")
    return errors


def verify(m: dict) -> list[str]:
    """디스크 전수 재해시 대조. 누락/추가/불일치 전부 보고 (fail-closed)."""
    errors = check_schema(m)
    if not DATA_DIR.is_dir():
        return errors + [f"{DATA_DIR} 부재 — 원본 디렉터리 소실"]
    on_disk = {
        str(p.relative_to(DATA_DIR)): p
        for p in DATA_DIR.rglob("*")
        if p.is_file() and p.name != ".DS_Store"
    }
    recorded = {f["path"]: f for f in m["files"]}
    for path in sorted(recorded.keys() - on_disk.keys()):
        errors.append(f"MISSING: {path} (매니페스트에 있으나 디스크에 없음)")
    for path in sorted(on_disk.keys() - recorded.keys()):
        errors.append(f"EXTRA: {path} (디스크에 있으나 매니페스트에 없음)")
    for path in sorted(recorded.keys() & on_disk.keys()):
        f, p = recorded[path], on_disk[path]
        if p.stat().st_size != f["size"]:
            errors.append(f"SIZE MISMATCH: {path} {p.stat().st_size} != {f['size']}")
        elif sha256_of(p) != f["sha256"]:
            errors.append(f"HASH MISMATCH: {path}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="매니페스트 생성")
    mode.add_argument("--schema-only", action="store_true", help="자체 정합성만 (CI)")
    args = ap.parse_args()

    if args.write:
        m = build_manifest()
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(
            json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"wrote {MANIFEST.relative_to(REPO)}: {m['file_count']} files, "
              f"{m['total_bytes']:,} bytes")
        return 0

    m = load_manifest()
    errors = check_schema(m) if args.schema_only else verify(m)
    label = "schema-only" if args.schema_only else "full verify"
    if errors:
        print(f"FAIL ({label}) — {len(errors)}건:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print(f"PASS ({label}): {m['file_count']} files, {m['total_bytes']:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
