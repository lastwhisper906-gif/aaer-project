"""RP-09 Stage 2: CONTROL_CRITERIA_v2 코드 미러 — fetch / validate / select.

사용 (criteria §6-v2):
  python3 tools/control_v2.py fetch      # 풀 수집 (무조건 SIC 확장, 캐시 재사용)
  python3 tools/control_v2.py validate   # 4층 검증 → quarantine
  python3 tools/control_v2.py select     # 순수 함수 선정 → runs/rp09/control_group_v2.json

v1 대비 개정 (docs/CONTROL_CRITERIA_v2.md — 문서 수정 없이 이 파일만 바꾸는 것 금지):
  (i)   §2-a 삭제 — 1차+보충 SIC 전체 무조건 열거 (조기 탈출 없음). T21 보충
        SIC에 8700·8742 추가 (8732·7375는 EDGAR 0건 실측 — 선언 유지, 무해).
  (ii)  케이스당 상위 3 선정(S3-v2) · S2-v2 전순서 (규모 버킷 → SIC 계층 →
        FYE 월거리 → CIK) · PIT 상한 40 (S0-v2).
  (iii) E4-v2 구문 단위 이름 대조 (aaer_hits_v2) — 수기 통과 불사용.

v1 도구(rp08_common/fetch_control_pool_rp08/select_control_group_rp08)는 무변경
잔존 — v1.1 재현성 보존. 공유 헬퍼만 rp08_common에서 import.
"""
import datetime
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rp08_common import (BIG_DIR, CASES, FRAME_TAGS, SIZE_BAND,
                         TIE_DELTA, fye_month_dist, pit_size, screen_submissions,
                         sha256_file, treatment_ciks, RP01_DISQUALIFIED_CIKS,
                         MIN_10K, MIN_10Q, HISTORY_Y)

REPO = Path(__file__).resolve().parents[1]
RAW2 = REPO / "runs/rp09/control_pool_raw"
PROV2 = RAW2 / "provenance.jsonl"
MANIFEST2 = RAW2 / "MANIFEST.sha256"
QUARANTINE2 = RAW2.parent / "quarantine/quarantine.json"
OUT2 = RAW2.parent / "control_group_v2.json"
CRITERIA_DOC = REPO / "docs/CONTROL_CRITERIA_v2.md"

N_PIT_V2 = 40      # S0-v2
N_SELECT = 3       # S3-v2: 케이스당 상위 3
N_ALT_V2 = 2       # 차순위 기록 수

# (i) T21 SIC 선언값 정정 — 그 외 케이스는 v1 §2 선언 무변경 승계
CASES_V2 = {tid: dict(spec) for tid, spec in CASES.items()}
CASES_V2["T21"]["sic_supp"] = ["8732", "7375", "8700", "8742"]

# E8b — 소유자 확인 비-AAER 집행 부적격 (RP-09 §Final A1, overrides.md 전사).
# AAER 색인 밖의 확정 10b-5 명령 등 — E4가 구조적으로 못 보는 집행 이력의
# 규칙화 (E8 RP01_DISQUALIFIED_CIKS와 동형: 증거는 1차 소스로 기재).
OWNER_CONFIRMED_ENFORCEMENT_CIKS = {
    "0000006281": "Analog Devices — SEC C&D §10(b)/10b-5 옵션 백데이팅, $3M, "
                  "2008-05-30 화해 (AP 3-13050, Rel 33-8923, PR 2008-102)",
}

# (iii) E4-v2 — 접미 목록: v1 _SUFFIXES + 복수형
E4_SUFFIXES = {"the", "co", "corp", "inc", "ltd", "llc", "plc", "company",
               "corporation", "holdings", "holding", "group", "international",
               "incorporated", "limited", "nv", "sa", "ag",
               "companies", "groups", "corps", "brands"}


def name_tokens_v2(name: str) -> list:
    toks = re.findall(r"[a-z]+", (name or "").lower())
    return [t for t in toks if t not in E4_SUFFIXES and len(t) >= 3]


def _entry_words(entry: dict) -> list:
    if "_words" not in entry:
        entry["_words"] = re.findall(r"[a-z]+", entry["respondents"].lower())
    return entry["_words"]


def aaer_hits_v2(names: list, index_entries: list) -> list:
    """E4-v2: 다토큰 = 전 토큰 단어 단위 공존 / 단일 토큰 = 직후 2단어 내 법인 접미."""
    hits = []
    for nm in names:
        toks = name_tokens_v2(nm)
        if not toks:
            continue
        for e in index_entries:
            words = _entry_words(e)
            wset = set(words)
            if len(toks) >= 2:
                matched = all(t in wset for t in toks)
            else:
                t = toks[0]
                matched = any(w == t and any(x in E4_SUFFIXES for x in words[i + 1:i + 3])
                              for i, w in enumerate(words))
            if matched:
                hits.append({"name_checked": nm, "tokens": toks,
                             "aaer_no": e["aaer_no"],
                             "respondents": e["respondents"][:80]})
    return hits


def eligibility_v2(rec: dict, cutoff: datetime.date, e4_hits: list) -> tuple:
    """E1~E9 하드 스크린 (E4-v2 — 수기 통과 없음). v1 eligibility의 v2 미러."""
    fails = []
    if rec["pre_cutoff_10K"] < MIN_10K or rec["pre_cutoff_10Q"] < MIN_10Q:
        fails.append(f"E1 filing history 10-K={rec['pre_cutoff_10K']} 10-Q={rec['pre_cutoff_10Q']}")
    if rec["fpi_forms"] > 0 and rec["pre_cutoff_10K"] == 0:
        fails.append("E1 FPI(20-F/40-F 전용)")
    if not rec["xbrl_pre_cutoff"]:
        fails.append("E2 XBRL 부재(pre-cutoff)")
    if not rec["active_in_window"]:
        fails.append("E3 비활동(18개월)")
    if e4_hits:
        fails.append(f"E4-v2 AAER 구문 적중 {len(e4_hits)}건 (예: AAER-{e4_hits[0]['aaer_no']})")
    if rec["item_402_in_window"]:
        fails.append(f"E5 Item 4.02 재작성 {rec['item_402_in_window']}")
    if rec["first_counted"] is None or datetime.date.fromisoformat(
            rec["first_counted"]) > cutoff - datetime.timedelta(days=HISTORY_Y * 365):
        fails.append("E6a 제출 이력 <3년")
    if rec["cik"] in RP01_DISQUALIFIED_CIKS:
        fails.append(f"E8 RP-01 실격 승계: {RP01_DISQUALIFIED_CIKS[rec['cik']]}")
    if rec["cik"] in OWNER_CONFIRMED_ENFORCEMENT_CIKS:
        fails.append(f"E8b 소유자 확인 집행 부적격: {OWNER_CONFIRMED_ENFORCEMENT_CIKS[rec['cik']]}")
    if "tickers" not in rec:
        fails.append("E9 판정 불능 (tickers 필드 부재)")
    elif not rec["tickers"]:
        fails.append("E9 상장 보통주 부재 (tickers 공백)")
    return (not fails), fails


def sic_tier(spec: dict, sic_pool: str):
    """S2-v2 산업 근접: 1차=0, 보충=1+선언 순번."""
    if sic_pool in spec["sic_primary"]:
        return 0
    return 1 + spec["sic_supp"].index(sic_pool)


# ── fetch ────────────────────────────────────────────────────────────────
def cmd_fetch() -> int:
    import fetch_control_pool_rp08 as f8  # fetch/fetch_to/rate-limit 재사용
    # v2 provenance/sic_lists 경로로 재지향 (모듈 전역 치환 — v1 파일 불변)
    f8.PROVENANCE = PROV2
    import rp08_common as r8
    r8.PROVENANCE = PROV2

    RAW2.mkdir(parents=True, exist_ok=True)
    idx = json.loads((Path.home() / "aaer-data/_aaer_index/aaer_index.json").read_text())
    t_ciks = treatment_ciks()

    def sic_ciks_v2(sic: str) -> list:
        out, start = [], 0
        while True:
            url = ("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany"
                   f"&SIC={sic}&type=10-K&dateb=&owner=include&count=100&start={start}&output=atom")
            path = RAW2 / f"sic_lists/SIC{sic}_start{start}.atom"
            # rp08 캐시 승계 (동일 URL 규약 — provenance는 rp08 기록)
            old = REPO / f"runs/rp08/control_pool_raw/sic_lists/SIC{sic}_start{start}.atom"
            if not path.exists() and old.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(old.read_bytes())
            f8.fetch_to(url, path)
            hits = re.findall(r"<cik>(\d{10})</cik>",
                              path.read_text(encoding="utf-8", errors="replace"))
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
                dedup.append(cik)
        return dedup

    pool = {"_meta": {"criteria": "docs/CONTROL_CRITERIA_v2.md",
                      "criteria_version": "v2",
                      "aaer_index_fetched_at": idx["fetched_at"],
                      "aaer_index_entries": len(idx["entries"]),
                      "cache_note": "submissions/facts/frames는 ~/aaer-data/_rp08 캐시 공유 (rp08 provenance 승계); 신규 수집분만 rp09 provenance",
                      "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat()},
            "cases": {}}
    sub_cache = {}

    for tid, spec in CASES_V2.items():
        cutoff = datetime.date.fromisoformat(spec["cutoff"])
        candidates = {}
        plan = spec["sic_primary"] + spec["sic_supp"]  # (i) 무조건 전체 — 조기 탈출 없음
        sics_used = []
        for sic in plan:
            print(f"\n[{tid}] SIC {sic} 열거 (무조건 확장)", flush=True)
            listing = sic_ciks_v2(sic)
            sics_used.append(sic)
            print(f"  등록자 {len(listing)}", flush=True)
            for cik in listing:
                if cik in candidates:
                    continue
                if cik in t_ciks or cik == spec["cik"]:
                    candidates[cik] = {"cik": cik, "sic_pool": sic, "eligible": False,
                                       "fails": ["E7 실험군/후보 풀 자기 배제"]}
                    continue
                try:
                    if cik not in sub_cache:
                        sub_cache[cik] = f8.load_submissions(cik)
                    meta, blocks = sub_cache[cik]
                except Exception as e:  # noqa: BLE001
                    candidates[cik] = {"cik": cik, "sic_pool": sic, "eligible": False,
                                       "fails": [f"수집 실패: {e}"]}
                    continue
                rec = screen_submissions(blocks, meta, cutoff)
                rec.update({"cik": cik, "sic_pool": sic})
                hits = aaer_hits_v2([rec["name"] or ""] + rec["former_names"],
                                    idx["entries"])
                ok, fails = eligibility_v2(rec, cutoff, hits)
                rec.update({"eligible": ok, "fails": fails,
                            "e4_hits": hits[:5], "e4_hit_count": len(hits)})
                candidates[cik] = rec
        pool["cases"][tid] = {"cutoff": spec["cutoff"], "sics_used": sics_used,
                              "candidates": candidates}

    # S0: frames 조잡 게이트 → PIT 상위 40 companyfacts
    for tid, cdata in pool["cases"].items():
        spec = CASES_V2[tid]
        cy = datetime.date.fromisoformat(spec["cutoff"]).year - 1
        fmap = f8.frames_map(cy)
        ranked = []
        for cik, rec in cdata["candidates"].items():
            if not rec.get("eligible"):
                continue
            fv = fmap.get(cik)
            rec["coarse_rev"] = fv
            # S0-v2 개정: 조잡 게이트는 제외 권한 없음 — 우선순위 전용
            # (frames CY는 비달력 FYE에서 체계 오차 — GIS 오배제 실측, criteria §S0-v2)
            rec["coarse_dist"] = (round(abs(math.log(fv / spec["rev_pit"])), 4)
                                  if fv and fv > 0 else None)
            ranked.append(rec)
        ranked.sort(key=lambda r: (r["coarse_dist"] if r["coarse_dist"] is not None else 0.0,
                                   r["cik"]))
        for i, rec in enumerate(ranked):
            if i < N_PIT_V2:
                try:
                    f8.fetch_to(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{rec['cik']}.json",
                                BIG_DIR / f"facts/CIK{rec['cik']}.json")
                    rec["pit_fetched"] = True
                except Exception as e:  # noqa: BLE001
                    rec["pit_fetched"] = False
                    rec["fails"] = [f"companyfacts 수집 실패: {e}"]
                    rec["eligible"] = False
            else:
                rec["pit_fetched"] = False
                rec["truncated_by_S0_cap"] = True
        cdata["s0_truncated_count"] = max(0, len(ranked) - N_PIT_V2)
        print(f"[{tid}] PIT 조회 {min(len(ranked), N_PIT_V2)} / 절단 {cdata['s0_truncated_count']}",
              flush=True)

    pool["_meta"]["finished_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # 후보 레코드에서 검증·선정에 불필요한 임시 필드 제거 없음 — 전수 기록 유지
    (RAW2 / "pool_extract.json").write_text(
        json.dumps(pool, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nsaved → {RAW2 / 'pool_extract.json'}", flush=True)

    lines = []
    for p in sorted(RAW2.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.sha256":
            lines.append(f"{sha256_file(p)}  {p}")
    MANIFEST2.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"manifest {len(lines)} files → {MANIFEST2}", flush=True)
    return 0


# ── validate (4층 — criteria §6-v2) ─────────────────────────────────────
def cmd_validate() -> int:
    problems = []

    def check(cond, layer, what, detail=""):
        if not cond:
            problems.append({"layer": layer, "item": what, "reason": detail})

    pool = json.loads((RAW2 / "pool_extract.json").read_text())
    # 층1 형태
    check("_meta" in pool and "cases" in pool, "1-shape", "pool_extract", "최상위 키")
    check(pool["_meta"].get("criteria_version") == "v2", "1-shape", "_meta", "criteria_version != v2")
    for tid, cdata in pool.get("cases", {}).items():
        check(tid in CASES_V2, "1-shape", tid, "미지의 케이스 ID")
        plan = CASES_V2[tid]["sic_primary"] + CASES_V2[tid]["sic_supp"]
        check(cdata.get("sics_used") == plan, "1-shape", tid,
              f"sics_used != 선언 전체 (무조건 확장 위반): {cdata.get('sics_used')}")
        for cik, r in cdata.get("candidates", {}).items():
            wid = f"{tid}/{cik}"
            check(re.fullmatch(r"\d{10}", cik) is not None, "1-shape", wid, "CIK 형식")
            for f in ("cik", "sic_pool", "eligible", "fails"):
                check(f in r, "1-shape", wid, f"필수 필드 부재: {f}")
            if r.get("eligible"):
                check(not r.get("fails"), "1-shape", wid, "eligible=True인데 fails 비공백")
                check(r.get("e4_hit_count", 0) == 0, "1-shape", wid,
                      "eligible=True인데 E4-v2 적중 존재 (수기 통과 금지 위반)")
    # 층2 해시
    listed = {}
    for line in MANIFEST2.read_text().splitlines():
        h, p = line.split("  ", 1)
        listed[p] = h
    for p, h in listed.items():
        pp = Path(p)
        check(pp.exists(), "2-hash", p, "매니페스트 항목 실파일 부재")
        if pp.exists():
            check(sha256_file(pp) == h, "2-hash", p, "sha256 불일치")
    for p in sorted(RAW2.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.sha256":
            check(str(p) in listed, "2-hash", str(p), "매니페스트 밖 원시 파일")
    # 층3 provenance (rp09 신규분 — sha256 존재·HTTP 200)
    if PROV2.exists():
        for line in PROV2.read_text().splitlines():
            row = json.loads(line)
            check(row.get("http_status") == 200, "3-prov", row.get("url", "?"),
                  f"HTTP {row.get('http_status')}")
            check(bool(row.get("sha256")), "3-prov", row.get("url", "?"), "sha256 부재")
    # 층4 교차 일관성
    for tid, cdata in pool.get("cases", {}).items():
        check(cdata["cutoff"] == CASES_V2[tid]["cutoff"], "4-cross", tid, "컷오프 불일치")
        n_trunc = sum(1 for r in cdata["candidates"].values()
                      if r.get("truncated_by_S0_cap"))
        check(n_trunc == cdata.get("s0_truncated_count"), "4-cross", tid,
              f"S0 절단 카운트 불일치 {n_trunc} != {cdata.get('s0_truncated_count')}")
        for cik, r in cdata["candidates"].items():
            if r.get("pit_fetched"):
                check((BIG_DIR / f"facts/CIK{cik}.json").exists(), "4-cross",
                      f"{tid}/{cik}", "pit_fetched=True인데 companyfacts 부재")
    QUARANTINE2.parent.mkdir(parents=True, exist_ok=True)
    QUARANTINE2.write_text(json.dumps(
        {"checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "problems": problems}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"4층 검증: 격리 {len(problems)}건 → {QUARANTINE2}")
    return 0 if not problems else 1


# ── select (순수 함수 — 네트워크 없음) ───────────────────────────────────
def load_facts(cik: str):
    p = BIG_DIR / f"facts/CIK{cik}.json"
    return json.loads(p.read_text()) if p.exists() else None


def cmd_select() -> int:
    pool = json.loads((RAW2 / "pool_extract.json").read_text())
    taken = set()
    selected, all_also_rans = {}, {}

    for tid in sorted(CASES_V2):  # S4 승계: 케이스 번호 오름차순
        spec = CASES_V2[tid]
        cutoff = datetime.date.fromisoformat(spec["cutoff"])
        cdata = pool["cases"][tid]
        ranked, also = [], []
        for cik, rec in sorted(cdata["candidates"].items()):
            row = {"cik": cik, "name": rec.get("name"), "sic": rec.get("sic"),
                   "sic_pool": rec.get("sic_pool")}
            # E8b 오버레이 (선정 시 재적용 — 풀 재수집 없이 규칙 개정 반영)
            if cik in OWNER_CONFIRMED_ENFORCEMENT_CIKS:
                row["excluded"] = [f"E8b 소유자 확인 집행 부적격: "
                                   f"{OWNER_CONFIRMED_ENFORCEMENT_CIKS[cik]}"]
                also.append(row)
                continue
            if not rec.get("eligible"):
                row["excluded"] = rec.get("fails") or ["수집 실패/자기 배제"]
                also.append(row)
                continue
            if rec.get("truncated_by_S0_cap"):
                row["excluded"] = [f"S0 조회 상한 절단 (조잡 거리 순위 {N_PIT_V2} 밖) — 무침묵 기록"]
                also.append(row)
                continue
            if not rec.get("pit_fetched"):
                row["excluded"] = rec.get("fails") or ["companyfacts 미조회"]
                also.append(row)
                continue
            facts = load_facts(cik)
            if facts is None:
                row["excluded"] = ["companyfacts 로컬 부재 (수집 재실행 필요)"]
                also.append(row)
                continue
            rev, assets = pit_size(facts, cutoff)
            row.update({"rev_pit": rev, "assets_pit": assets})
            flags = []
            if rev and rev > 0:
                dist = abs(math.log(rev / spec["rev_pit"]))
                basis = "revenue"
            elif assets and assets > 0:
                dist = abs(math.log(assets / spec["assets_pit"]))
                basis = "assets"
                flags.append("S1-매출 PIT 불능 → 총자산 대체")
            else:
                row["excluded"] = ["S1 PIT 규모 계산 불능 (매출·자산 태그 부재)"]
                also.append(row)
                continue
            if dist > SIZE_BAND:
                row["excluded"] = [f"S1 규모 밴드 |log|={dist:.3f} > log4 ({basis})"]
                also.append(row)
                continue
            row.update({"size_dist": round(dist, 4), "size_basis": basis,
                        "size_flags": flags, "fye": rec.get("fye"),
                        "fye_month_dist": fye_month_dist(rec.get("fye"), spec["fye_month"]),
                        "sic_tier": sic_tier(spec, rec["sic_pool"]),
                        "former_names": rec.get("former_names"),
                        "tickers": rec.get("tickers")})
            ranked.append(row)

        # S2-v2 전순서: 규모 버킷 → SIC 계층 → FYE 월거리 → CIK
        ranked.sort(key=lambda r: (int(r["size_dist"] / TIE_DELTA),
                                   r["sic_tier"],
                                   r["fye_month_dist"] if r["fye_month_dist"] is not None else 9,
                                   r["cik"]))
        picks, alternates = [], []
        for rank, r in enumerate(ranked, 1):
            r["rank"] = rank
            if r["cik"] in taken:
                also.append(dict(r, excluded=["S4 중복 배정 — 선순위 케이스에 기배정"]))
            elif len(picks) < N_SELECT:
                picks.append(r)
                taken.add(r["cik"])
            elif len(alternates) < N_ALT_V2:
                alternates.append(r)
            else:
                also.append(dict(r, excluded=[f"순위 밖 (rank {rank})"]))
        selected[tid] = {"treatment": {"ticker": spec["ticker"], "cutoff": spec["cutoff"],
                                       "rev_pit": spec["rev_pit"], "fye_month": spec["fye_month"]},
                         "selected": picks, "alternates": alternates,
                         "eligible_ranked_count": len(ranked),
                         "under_target": len(picks) < 2}
        all_also_rans[tid] = also

    n_sel = sum(len(v["selected"]) for v in selected.values())
    out = {
        "_meta": {
            "status": "PROPOSED — NOT FOR SCORING UNTIL OWNER-SIGNED (RP-09 §Final)",
            "criteria": "docs/CONTROL_CRITERIA_v2.md",
            "criteria_sha256": sha256_file(CRITERIA_DOC),
            "pool_extract_sha256": sha256_file(RAW2 / "pool_extract.json"),
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "selected_count": n_sel,
            "per_case_target": "2-3 (S3-v2)",
            "rerun": "python3 tools/control_v2.py select (네트워크 불요)",
        },
        "selections": selected,
        "also_rans": all_also_rans,
    }
    OUT2.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"선정 {n_sel} (목표 16-24) → {OUT2}")
    for tid, v in selected.items():
        names = ", ".join(f"{s['name']} ({s['size_dist']})" for s in v["selected"])
        print(f"  {tid} ({v['treatment']['ticker']}): {names or '선정 불능'}"
              + (" ⚠ under_target" if v["under_target"] else ""))
    return 0


if __name__ == "__main__":
    cmds = {"fetch": cmd_fetch, "validate": cmd_validate, "select": cmd_select}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        print("usage: control_v2.py {fetch|validate|select}", file=sys.stderr)
        sys.exit(2)
    sys.exit(cmds[sys.argv[1]]())
