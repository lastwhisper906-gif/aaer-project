"""label_tags_holdout.py — 홀드아웃 Big R/little r 태깅 (WS-3/F-6, specs/label_taxonomy.md).

스펙 사전 등록 커밋(d60a6e0)이 본 파일보다 선행. 출력:
analysis/label_tags_holdout.json (증거 accession 포함, 결정론·무네트워크).

폭로-후 제출물 접근 주석: 채점측 ground-truth 작업 (스펙 §2 — 피평가자
페이로드 아님, 선례 tools/holdout_rescan.py).

사용: .venv/bin/python analysis/label_tags_holdout.py
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
from payload_v2_extract import parse_items  # WS-1 공유 파서

DATA_DIR = Path.home() / "aaer-data"
NEIGHBORHOOD_DAYS = 90
EIGHTK_FORMS = ("8-K", "8-K/A")


class LabelTagError(Exception):
    pass


def _rows(ticker: str) -> list[dict]:
    edgar_dir = DATA_DIR / ticker / "edgar"
    paths = sorted(edgar_dir.glob("CIK*.json"))
    if not paths:
        raise LabelTagError(f"{edgar_dir}: submissions 없음 — fail-closed")
    rows, seen = [], set()
    for path in paths:
        j = json.loads(path.read_text(encoding="utf-8"))
        blocks = [j["filings"]["recent"]] if "filings" in j else [j]
        for b in blocks:
            for i, form in enumerate(b.get("form", [])):
                acc = b["accessionNumber"][i]
                if acc in seen:
                    continue
                seen.add(acc)
                items = b.get("items", [])
                rows.append({"form": form, "date": b["filingDate"][i],
                             "items_raw": items[i] if i < len(items) else "",
                             "accession": acc})
    return rows


def tag_case(case: dict) -> dict:
    cutoff = datetime.date.fromisoformat(case["cutoff_date"])
    revelation = cutoff + datetime.timedelta(days=1)
    # 스펙 §2: 레지스트리 scheme_summary의 8-K 일자와 대조 (불일치 fail-closed)
    if str(revelation) not in case["scheme_summary"]:
        raise LabelTagError(
            f"{case['case_id']}: revelation={revelation} 이 scheme_summary와 불일치 — fail-closed")
    lo = revelation - datetime.timedelta(days=NEIGHBORHOOD_DAYS)
    hi = revelation + datetime.timedelta(days=NEIGHBORHOOD_DAYS)
    rows = _rows(case["ticker"])
    snapshot_max = max(r["date"] for r in rows)
    all_402 = [r for r in rows
               if r["form"] in EIGHTK_FORMS and "4.02" in parse_items(r["items_raw"])]
    in_nb = [r for r in all_402 if lo <= datetime.date.fromisoformat(r["date"]) <= hi]
    out_nb = [r for r in all_402 if r not in in_nb]
    insufficient = datetime.date.fromisoformat(snapshot_max) < hi
    return {
        "case_id": case["case_id"], "ticker": case["ticker"],
        "revelation_date": str(revelation),
        "neighborhood": [str(lo), str(hi)],
        "tag": None if insufficient else ("bigR" if in_nb else "little_r"),
        "insufficient_cache": insufficient,
        "evidence_in_neighborhood": in_nb,
        "observations_outside_neighborhood": out_nb,
        "cache_snapshot_max_filing_date": snapshot_max,
        "upgrade_monitoring_until": str(revelation.replace(year=revelation.year + 4)),
    }


def main() -> int:
    raw = json.loads((REPO / "data/candidates/candidates_holdout.json").read_text(encoding="utf-8"))
    cases = raw["candidates"] if isinstance(raw, dict) else raw
    out = {"spec": "specs/label_taxonomy.md", "spec_commit": "d60a6e0",
           "rule": f"8-K/8-K-A item 4.02 within revelation±{NEIGHBORHOOD_DAYS}d → bigR else little_r",
           "frozen_scoreboard_untouched": True,
           "tags": [tag_case(c) for c in cases]}
    (REPO / "analysis/label_tags_holdout.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for t in out["tags"]:
        print(t["case_id"], t["ticker"], t["tag"],
              [e["accession"] for e in t["evidence_in_neighborhood"]],
              "insufficient_cache" if t["insufficient_cache"] else "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
