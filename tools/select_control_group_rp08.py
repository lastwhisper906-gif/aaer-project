"""RP-08 1d/1e: 기계 선정 — CONTROL_CRITERIA_v1 §3/§4의 순수 함수 구현.

입력: runs/rp08/control_pool_raw/pool_extract.json (validate_control_input PASS 후)
      + ~/aaer-data/_rp08/facts/ (PIT 계산용 로컬 원시)
      + runs/rp08/e4_manual_overrides.json (있으면 — E4 동명이인 수기 통과, 전부
        [DISCRETIONARY] 플래그)
출력: runs/rp08/control_group_PROPOSED.json — 선정 8 + 케이스별 대안 3 +
      전수 also-ran(탈락 사유). 네트워크 접근 없음 — 재실행 = 동일 결과.

동률 규칙 구현 주: criteria S2의 "동률(Δ<0.05)"는 |log 매출비|를 0.05 폭 버킷으로
양자화(floor)한 값의 동일성으로 구현 — 완전 결정론 정렬 (버킷, FYE 월거리, CIK).
"""
import datetime
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rp08_common import (BIG_DIR, CASES, N_ALT, RAW_DIR, SIZE_BAND, TIE_DELTA,
                         eligibility, fye_month_dist, pit_size, sha256_file)

OUT = RAW_DIR.parent / "control_group_PROPOSED.json"
OVERRIDES_P = RAW_DIR.parent / "e4_manual_overrides.json"


def load_facts(cik: str):
    p = BIG_DIR / f"facts/CIK{cik}.json"
    return json.loads(p.read_text()) if p.exists() else None


def tickers_for(cik: str):
    p = BIG_DIR / f"submissions/CIK{cik}.json"
    if not p.exists():
        return []
    j = json.loads(p.read_text())
    return sorted(set(j.get("tickers") or []))


def main() -> int:
    pool = json.loads((RAW_DIR / "pool_extract.json").read_text())
    overrides = json.loads(OVERRIDES_P.read_text()) if OVERRIDES_P.exists() else {}
    taken = set()
    selected, all_also_rans = {}, {}

    for tid in sorted(CASES):  # S4: 케이스 번호 오름차순 고정
        spec = CASES[tid]
        cutoff = datetime.date.fromisoformat(spec["cutoff"])
        cdata = pool["cases"][tid]
        ranked, also = [], []

        for cik, rec in sorted(cdata["candidates"].items()):
            row = {"cik": cik, "name": rec.get("name") or rec.get("listing_title"),
                   "sic": rec.get("sic"), "sic_pool": rec.get("sic_pool")}
            # 스크린 재적용 (fetch 후 추가된 override 반영 — E4 재판정)
            if rec.get("pre_cutoff_10K") is None:
                row["excluded"] = rec.get("fails") or ["수집 실패/자기 배제"]
                also.append(row)
                continue
            hits = rec.get("e4_hits") or []
            if rec.get("e4_hit_count") and not hits:
                hits = [{"aaer_no": "?", "respondents": "truncated"}]
            ok, fails, disc = eligibility(rec, cutoff, hits, overrides)
            if not ok:
                row["excluded"] = fails
                also.append(row)
                continue
            if rec.get("truncated_by_S0_cap"):
                row["excluded"] = ["S0 조회 상한 절단 (조잡 거리 순위 25 밖) — 무침묵 기록"]
                also.append(row)
                continue
            if not rec.get("pit_fetched"):
                if rec.get("fails"):
                    row["excluded"] = rec["fails"]
                else:
                    row["excluded"] = [f"S0 조잡 게이트 |log|={rec.get('coarse_dist')} > log6"]
                also.append(row)
                continue
            facts = load_facts(cik)
            if facts is None:
                row["excluded"] = ["companyfacts 로컬 부재 (수집 재실행 필요)"]
                also.append(row)
                continue
            rev, assets = pit_size(facts, cutoff)
            row.update({"rev_pit": rev, "assets_pit": assets})
            if rev and rev > 0:
                dist = abs(math.log(rev / spec["rev_pit"]))
                basis = "revenue"
            elif assets and assets > 0:
                dist = abs(math.log(assets / spec["assets_pit"]))
                basis = "assets"
                disc = disc + [{"flag": "S1-매출 PIT 불능 → 총자산 대체", "evidence": None}]
            else:
                row["excluded"] = ["S1 PIT 규모 계산 불능 (매출·자산 태그 부재)"]
                also.append(row)
                continue
            if dist > SIZE_BAND:
                row["excluded"] = [f"S1 규모 밴드 |log|={dist:.3f} > log4 ({basis})"]
                also.append(row)
                continue
            fdist = fye_month_dist(rec.get("fye"), spec["fye_month"])
            row.update({"size_dist": round(dist, 4), "size_basis": basis,
                        "fye": rec.get("fye"),
                        "fye_month_dist": fdist,
                        "discretionary": disc,
                        "former_names": rec.get("former_names"),
                        "e4_hit_count": rec.get("e4_hit_count", 0)})
            ranked.append(row)

        # S2: (0.05 버킷, FYE 월거리, CIK) — 결정론 전순서
        ranked.sort(key=lambda r: (int(r["size_dist"] / TIE_DELTA),
                                   r["fye_month_dist"] if r["fye_month_dist"] is not None else 9,
                                   r["cik"]))
        pick, alternates = None, []
        for rank, r in enumerate(ranked, 1):
            r["rank"] = rank
            if r["cik"] in taken:
                also.append(dict(r, excluded=["S4 중복 배정 — 선순위 케이스에 기배정"]))
            elif pick is None:
                pick = r
                taken.add(r["cik"])
            elif len(alternates) < N_ALT:
                alternates.append(r)
            else:
                also.append(dict(r, excluded=[f"순위 밖 (rank {rank})"]))
        if pick:
            pick["tickers"] = tickers_for(pick["cik"])
        selected[tid] = {"treatment": {"ticker": spec["ticker"], "cutoff": spec["cutoff"],
                                       "rev_pit": spec["rev_pit"], "fye_month": spec["fye_month"]},
                         "selected": pick, "alternates": alternates,
                         "eligible_ranked_count": len(ranked)}
        all_also_rans[tid] = also

    n_sel = sum(1 for v in selected.values() if v["selected"])
    n_disc = sum(len(v["selected"].get("discretionary", []))
                 for v in selected.values() if v["selected"])
    out = {
        "_meta": {
            "status": "PROPOSED — NOT FOR SCORING UNTIL OWNER-SIGNED",
            "criteria": "docs/CONTROL_CRITERIA_v1.md",
            "criteria_sha256": sha256_file(Path(__file__).resolve().parents[1]
                                           / "docs/CONTROL_CRITERIA_v1.md"),
            "pool_extract_sha256": sha256_file(RAW_DIR / "pool_extract.json"),
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "selected_count": n_sel,
            "discretionary_flag_count": n_disc,
            "rerun": "python3 tools/select_control_group_rp08.py (네트워크 불요, 분 단위)",
        },
        "selections": selected,
        "also_rans": all_also_rans,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"선정 {n_sel}/8 · [DISCRETIONARY] {n_disc} → {OUT}")
    for tid, v in selected.items():
        s = v["selected"]
        print(f"  {tid} ({v['treatment']['ticker']}): "
              + (f"{s['name']} CIK {s['cik']} dist={s['size_dist']} fye={s['fye']}"
                 if s else "선정 불능 (자격자 0)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
