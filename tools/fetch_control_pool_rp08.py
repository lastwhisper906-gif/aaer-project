"""RP-08 1b: 광역 대조군 후보 풀 수집 (CONTROL_CRITERIA_v1 §2/§3/§4-S0의 수집 축).

단계 (전부 재개 가능 — 캐시 존재 시 재요청 안 함):
  A. 케이스별 1차 SIC의 EDGAR 등록자 전수 열거 (browse-edgar atom, 전 페이지)
     → runs/rp08/control_pool_raw/sic_lists/ (원문 커밋 대상, 소형 텍스트)
  B. 후보별 submissions JSON (+구형 청크) → ~/aaer-data/_rp08/submissions/
     (대용량, git 밖 — data/README 규약) → E1/E3/E5/E6a/E7/E8 + E4(로컬 AAER
     색인) 스크린 → 케이스별 자격자 <5면 보충 SIC를 선언 순서대로 확장 (§2)
  C. XBRL frames 조잡 게이트 (S0, |log|≤log6, 미적중은 통과) → 조잡 거리
     오름차순 상위 25/케이스만 companyfacts 조회 → ~/aaer-data/_rp08/facts/
  D. pool_extract.json (선정 스크립트의 입력) + provenance.jsonl + MANIFEST.sha256

SEC fair-access: 선언 User-Agent, 4 req/s 미만, 429/503 지수 백오프.
이 수집은 채점 보조자의 선정용 메타데이터 수집이며 피평가자 입력이 아니다 —
fetch_primary_sources.py 규약대로 cutoff_guard 비경유 (PIT 규율은 filed≤cutoff
필드 수준에서 적용, criteria §1 각주).
"""
import datetime
import json
import math
import re
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rp08_common import (BIG_DIR, CASES, COARSE_BAND, FRAME_TAGS, MANIFEST,
                         MIN_ELIGIBLE, N_PIT, PROVENANCE, RAW_DIR, aaer_hits,
                         eligibility, screen_submissions, sha256_file,
                         treatment_ciks)

UA = {"User-Agent": "chaeper lastwhisper906@gmail.com"}
RATE_SECONDS = 0.28
_last = [0.0]
_prov = []


def fetch(url: str, timeout: int = 60) -> requests.Response:
    for attempt in range(6):
        wait = RATE_SECONDS - (time.monotonic() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.monotonic()
        resp = requests.get(url, headers=UA, timeout=timeout)
        if resp.status_code in (429, 503):
            back = 2 ** (attempt + 1)
            print(f"    {resp.status_code} → backoff {back}s", flush=True)
            time.sleep(back)
            continue
        resp.raise_for_status()
        return resp
    raise RuntimeError(f"429/503 백오프 소진: {url}")


def fetch_to(url: str, path: Path) -> Path:
    """GET → 파일 저장 + provenance 기록. 캐시 존재 시 재요청 안 함."""
    if path.exists():
        return path
    resp = fetch(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(resp.content)
    _prov.append({"url": url,
                  "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  "http_status": resp.status_code,
                  "sha256": sha256_file(path),
                  "path": str(path)})
    flush_provenance()
    return path


def flush_provenance():
    PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROVENANCE, "a", encoding="utf-8") as f:
        for row in _prov:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    _prov.clear()


# ── A. SIC 전수 열거 ──────────────────────────────────────────────────────
def sic_ciks(sic: str) -> list:
    out, start = [], 0
    while True:
        url = ("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany"
               f"&SIC={sic}&type=10-K&dateb=&owner=include&count=100&start={start}&output=atom")
        path = RAW_DIR / f"sic_lists/SIC{sic}_start{start}.atom"
        fetch_to(url, path)
        text = path.read_text(encoding="utf-8", errors="replace")
        # SIC 목록 atom은 <title>이 깨져 있음(EDGAR 버그) — <cik> 태그로 열거,
        # 사명은 submissions JSON에서 취득.
        hits = re.findall(r"<cik>(\d{10})</cik>", text)
        if not hits:
            break
        out.extend(hits)
        if len(hits) < 100:
            break
        start += 100
    seen, dedup = set(), []
    for cik in out:
        if cik not in seen:
            seen.add(cik)
            dedup.append({"title": "", "cik": cik})
    return dedup


# ── B. submissions + 스크린 ──────────────────────────────────────────────
def load_submissions(cik10: str):
    base = BIG_DIR / "submissions"
    main = fetch_to(f"https://data.sec.gov/submissions/CIK{cik10}.json",
                    base / f"CIK{cik10}.json")
    j = json.loads(main.read_text())
    blocks = [j["filings"]["recent"]]
    for extra in j["filings"].get("files", []):
        p = fetch_to(f"https://data.sec.gov/submissions/{extra['name']}",
                     base / extra["name"])
        blocks.append(json.loads(p.read_text()))
    return j, blocks


def main() -> int:
    only = sys.argv[sys.argv.index("--only-case") + 1] if "--only-case" in sys.argv else None
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    idx = json.loads((Path.home() / "aaer-data/_aaer_index/aaer_index.json")
                     .read_text(encoding="utf-8"))
    t_ciks = treatment_ciks()
    overrides_p = RAW_DIR.parent / "e4_manual_overrides.json"
    overrides = json.loads(overrides_p.read_text()) if overrides_p.exists() else {}

    pool = {"_meta": {"criteria": "docs/CONTROL_CRITERIA_v1.md",
                      "aaer_index_fetched_at": idx["fetched_at"],
                      "aaer_index_entries": len(idx["entries"]),
                      "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat()},
            "cases": {}}
    sub_cache = {}

    for tid, spec in CASES.items():
        if only and tid != only:
            continue
        cutoff = datetime.date.fromisoformat(spec["cutoff"])
        sics_used, candidates = [], {}
        eligible_n = 0
        plan = spec["sic_primary"] + spec["sic_supp"]
        for i, sic in enumerate(plan):
            is_supp = sic in spec["sic_supp"]
            if is_supp and eligible_n >= MIN_ELIGIBLE:
                break
            print(f"\n[{tid}] SIC {sic} {'(보충)' if is_supp else '(1차)'} 열거", flush=True)
            listing = sic_ciks(sic)
            sics_used.append(sic)
            print(f"  등록자 {len(listing)}", flush=True)
            for row in listing:
                cik = row["cik"]
                if cik in candidates:
                    continue
                if cik in t_ciks or cik == spec["cik"]:
                    candidates[cik] = {"cik": cik, "listing_title": row["title"],
                                       "sic_pool": sic, "fails": ["E7 실험군/후보 풀 자기 배제"],
                                       "eligible": False}
                    continue
                try:
                    if cik not in sub_cache:
                        meta, blocks = load_submissions(cik)
                        sub_cache[cik] = (meta, blocks)
                    meta, blocks = sub_cache[cik]
                except Exception as e:  # noqa: BLE001
                    candidates[cik] = {"cik": cik, "listing_title": row["title"],
                                       "sic_pool": sic, "fails": [f"수집 실패: {e}"],
                                       "eligible": False}
                    continue
                rec = screen_submissions(blocks, meta, cutoff)
                rec["cik"] = cik
                rec["sic_pool"] = sic
                rec["listing_title"] = row["title"]
                hits = aaer_hits([rec["name"] or row["title"]] + rec["former_names"],
                                 idx["entries"])
                ok, fails, disc = eligibility(rec, cutoff, hits, overrides)
                rec.update({"eligible": ok, "fails": fails, "discretionary": disc,
                            "e4_hits": hits[:5], "e4_hit_count": len(hits)})
                candidates[cik] = rec
                if ok:
                    eligible_n += 1
            print(f"  누적 자격자 {eligible_n}", flush=True)
        pool["cases"][tid] = {"cutoff": spec["cutoff"], "sics_used": sics_used,
                              "candidates": candidates}

    # ── C. frames 조잡 게이트 + companyfacts ─────────────────────────────
    frames_cache = {}
    for tid, cdata in pool["cases"].items():
        spec = CASES[tid]
        cy = datetime.date.fromisoformat(spec["cutoff"]).year - 1
        fmap = frames_cache.get(cy)
        if fmap is None:
            fmap = {}
            for tag in reversed(FRAME_TAGS):  # 우선순위 높은 태그가 나중에 덮어씀
                try:
                    p = fetch_to(f"https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/USD/CY{cy}.json",
                                 BIG_DIR / f"frames/{tag}_CY{cy}.json")
                    for d in json.loads(p.read_text())["data"]:
                        fmap[str(d["cik"]).zfill(10)] = d["val"]
                except Exception as e:  # noqa: BLE001
                    # 연도에 태그 frame 부재(예: ASC606 태그의 2018년 이전) = 스킵
                    print(f"  frames {tag} CY{cy} 불가: {e}", flush=True)
            frames_cache[cy] = fmap
        ranked = []
        for cik, rec in cdata["candidates"].items():
            if not rec.get("eligible"):
                continue
            fv = fmap.get(cik)
            rec["coarse_rev"] = fv
            if fv and fv > 0:
                dist = abs(math.log(fv / spec["rev_pit"]))
                rec["coarse_dist"] = round(dist, 4)
                if dist > COARSE_BAND:
                    rec["eligible"] = False
                    rec["fails"] = [f"S0 조잡 게이트 |log|={dist:.2f} > log6 (frames CY{cy})"]
                    continue
            else:
                rec["coarse_dist"] = None  # 미적중 = 통과 (제외 불가)
            ranked.append(rec)
        # 미적중(None)은 0.0으로 정렬 — PIT 확인 기회를 보존 (criteria S0)
        ranked.sort(key=lambda r: (r["coarse_dist"] if r["coarse_dist"] is not None else 0.0,
                                   r["cik"]))
        for i, rec in enumerate(ranked):
            if i < N_PIT:
                try:
                    fetch_to(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{rec['cik']}.json",
                             BIG_DIR / f"facts/CIK{rec['cik']}.json")
                    rec["pit_fetched"] = True
                except Exception as e:  # noqa: BLE001
                    rec["pit_fetched"] = False
                    rec["fails"] = [f"companyfacts 수집 실패: {e}"]
                    rec["eligible"] = False
            else:
                rec["pit_fetched"] = False
                rec["truncated_by_S0_cap"] = True  # 무침묵 절단 기록
        n_trunc = max(0, len(ranked) - N_PIT)
        cdata["s0_truncated_count"] = n_trunc
        print(f"[{tid}] PIT 조회 {min(len(ranked), N_PIT)} / 절단 {n_trunc}", flush=True)

    pool["_meta"]["finished_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    out = RAW_DIR / "pool_extract.json"
    out.write_text(json.dumps(pool, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nsaved → {out}", flush=True)

    # ── D. 매니페스트 (repo 원시 + git 밖 대용량 전부) ────────────────────
    lines = []
    for base in (RAW_DIR, BIG_DIR):
        for p in sorted(base.rglob("*")):
            if p.is_file() and p.name != "MANIFEST.sha256":
                lines.append(f"{sha256_file(p)}  {p}")
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"manifest {len(lines)} files → {MANIFEST}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
