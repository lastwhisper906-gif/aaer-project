"""E2 스냅샷 케이스 생성기 — 동결 그리드(EARLINESS_PLAN §1·§2 + D65 주석) 기계 구현.

freeze-commit-then-run: 이 코드 커밋이 생성 산출물(data/e2/*) 커밋에 선행한다.
결정론 — 타임스탬프 0, sort_keys 직렬화; 두 번 생성해 바이트 동일해야 한다.

산출물 (data/e2/):
  registry_e2.json          스냅샷 ID → 컷오프 레지스트리 (cutoff_guard 입력)
  case_{NN}_s{j}.json       스냅샷 생성 기록 — 컷오프·문서 단위 provenance·
                            payload_sha256·b3/b4 동반 점수 (B4는 D61대로 대부분
                            not_computable — 상태를 생략하지 않고 기록)
  cases_e2_s{j}.json        러너 소비용 배치 (j별) — **evaluatee 5필드만**.
                            e2 메타를 엔트리에 넣지 않는 이유: build_payload가
                            케이스 필드를 페이로드에 그대로 복사하므로(원본 변형
                            누출 표면), 메타는 전부 사이드카 기록에만 둔다.
  E2_MANIFEST.json          전 (케이스×j≤8) 행 회계 — buildable / grid_ineligible
                            / build_failed, 예산 = buildable evaluatee + 0 grader.

케이스 ID 설계 (PLAN §2 "case_NN_s{j}" 와 perturb 동일-k 요건의 양립):
러너 배치 엔트리의 case_id는 **기저 case_NN 그대로** — perturb_factor(case_id)가
스냅샷 간 동일 k를 유지해야 궤적 내 점이 비교 가능하다(PLAN §2 명문).
스냅샷 정체성 case_NN_s{j}는 배치 파일(j)×기저 ID의 곱으로 결정되며, 기록
파일·레지스트리·매니페스트가 그 ID를 보유한다. 러너 출력은 runs/e2/s{j}/에
기저 ID로 격리된다.

로스터는 하드코딩하지 않는다 — PLAN §1 규칙의 기계 출력:
  wave-1 detected = baseline_table.csv group=fraud & llm_score(원본 본채점) ≥ 50
  wave-2 detected = runs/wave2/scores/*.json p ≥ 50 (id_mapping_wave2 경유,
                    채점측 매핑은 로스터 도출에만 소비 — 산출물에 미기록)
  대조군          = candidates.json C01–C08 (RP-01 확정 8)
MON(28)·CSC(40)·BRX(20)는 규칙에 의해 자동 탈락한다 (명시 제외 목록 없음).
"""
from __future__ import annotations

import argparse
import csv
import datetime
import glob
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
sys.path.insert(0, str(REPO / "analysis"))
sys.path.insert(0, str(REPO / "analysis" / "vendor"))

import build_payload as bp  # noqa: E402 — 동결 빌더, 무수정 소비
import cutoff_guard  # noqa: E402
from b3_compute import b3_score  # noqa: E402
from b4_short_interest import b4_score  # noqa: E402

DATA_DIR = Path.home() / "aaer-data"
OUT_ROOT = REPO / "data" / "e2"
FLAG = 50                      # 동결 FLAG=50 (detected 규칙)
SNAP_CAP = 8                   # PLAN §2
MIN_REMAINING = 6              # PLAN §1 스냅샷 최소 요건
XBRL_FORMS = ("10-K", "10-Q")
GEN_VERSION = "e2gen-v1 (EARLINESS_PLAN §1–§2 + D65)"


class E2GenError(Exception):
    """fail-closed: 로스터/그리드/생성 불변식 위반."""


# ---------------------------------------------------------------- roster

def _mapping(path: Path) -> dict:
    j = json.loads(path.read_text(encoding="utf-8"))
    return j.get("mapping", j)


def _evaluatee_entries(path: Path) -> dict:
    return {c["case_id"]: c
            for c in json.loads(path.read_text(encoding="utf-8"))["cases"]}


def derive_roster(repo: Path = REPO) -> list[dict]:
    """PLAN §1 규칙의 기계 출력 — [{snapshot base 정보}] (treatment 13 + control 8)."""
    cand = {c["case_id"]: c for c in json.loads(
        (repo / "data/candidates/candidates.json").read_text(encoding="utf-8"))["candidates"]}
    inv1 = {v: k for k, v in _mapping(repo / "scoring/id_mapping.json").items()}
    ev1 = _evaluatee_entries(repo / "data/evaluatee/cases.json")

    roster = []
    for r in csv.DictReader(open(repo / "analysis/baseline_table.csv", encoding="utf-8")):
        if r["case_id"].startswith("T") and r["group"] == "fraud" \
                and float(r["llm_score"]) >= FLAG:
            tid = r["case_id"]
            roster.append({"tier": "wave1", "group": "treatment", "reg_id": tid,
                           "base_case": ev1[inv1[tid]],
                           "base_cutoff": cand[tid]["cutoff_date"]})
    for cid, c in cand.items():
        if c["group"] == "control" and cid.startswith("C"):
            roster.append({"tier": "wave1", "group": "control", "reg_id": cid,
                           "base_case": ev1[inv1[cid]],
                           "base_cutoff": c["cutoff_date"]})

    cand2 = {c["case_id"]: c for c in json.loads(
        (repo / "data/candidates/candidates_wave2.json").read_text(encoding="utf-8"))["candidates"]}
    map2 = _mapping(repo / "scoring/id_mapping_wave2.json")
    ev2 = _evaluatee_entries(repo / "data/evaluatee/cases_wave2.json")
    for p in sorted(glob.glob(str(repo / "runs/wave2/scores/case_*.json"))):
        j = json.loads(Path(p).read_text(encoding="utf-8"))
        tid = map2.get(j["case_id"])
        if tid and cand2[tid]["group"] == "treatment" \
                and j["misstatement_probability"] >= FLAG:
            roster.append({"tier": "wave2", "group": "treatment", "reg_id": tid,
                           "base_case": ev2[j["case_id"]],
                           "base_cutoff": cand2[tid]["cutoff_date"]})

    roster.sort(key=lambda x: x["base_case"]["case_id"])
    n_t = sum(1 for x in roster if x["group"] == "treatment")
    n_c = sum(1 for x in roster if x["group"] == "control")
    if n_c != 8:
        raise E2GenError(f"대조군 {n_c} != 8 (RP-01)")
    return roster


# ---------------------------------------------------------------- grid

def xbrl_filings(ticker: str, cutoff: str, data_dir: Path = DATA_DIR) -> list[dict]:
    """isXBRL 10-K/10-Q, filed <= cutoff, accession dedup, filed 내림차순."""
    out = {}
    for f in sorted(glob.glob(str(data_dir / ticker / "edgar" / "CIK*.json"))):
        j = json.loads(Path(f).read_text(encoding="utf-8"))
        r = j.get("filings", {}).get("recent")
        blocks = [r] if r else ([j] if "form" in j else [])
        for b in blocks:
            forms = b.get("form", [])
            isx = b.get("isXBRL", [1] * len(forms))
            for i, fo in enumerate(forms):
                if fo in XBRL_FORMS and b["filingDate"][i] <= cutoff and isx[i]:
                    out[b["accessionNumber"][i]] = {
                        "accession": b["accessionNumber"][i],
                        "filed": b["filingDate"][i], "form": fo}
    return sorted(out.values(), key=lambda d: (d["filed"], d["accession"]),
                  reverse=True)


def snapshot_grid(filings: list[dict]) -> list[dict]:
    """j=1..cap 전 행 — eligible 여부와 사유를 전부 기록 (조용한 스킵 금지)."""
    rows = []
    for j in range(1, SNAP_CAP + 1):
        if j > len(filings):
            rows.append({"j": j, "eligible": False, "reason": "beyond_available"})
            continue
        remaining = filings[j - 1:]
        if len(remaining) < MIN_REMAINING:
            rows.append({"j": j, "eligible": False, "reason": "insufficient_remaining"})
        elif not any(d["form"] == "10-K" for d in remaining):
            rows.append({"j": j, "eligible": False, "reason": "no_10k_remaining"})
        else:
            cut = (datetime.date.fromisoformat(filings[j - 1]["filed"])
                   + datetime.timedelta(days=1))
            rows.append({"j": j, "eligible": True, "cutoff": str(cut)})
    return rows


# ---------------------------------------------------------------- build + verify

def _canonical(payload_send: dict) -> bytes:
    return json.dumps(payload_send, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def payload_documents(payload: dict) -> list[dict]:
    """문서 단위 provenance — (accession, filed, form, n_facts)."""
    docs: dict[str, dict] = {}
    for vals in payload["financial_series_point_in_time"].values():
        for v in vals:
            key = v.get("accession") or f"noacc:{v['filed']}"
            d = docs.setdefault(key, {"accession": v.get("accession"),
                                      "filed": v["filed"],
                                      "form": v.get("form"), "n_facts": 0})
            d["n_facts"] += 1
    return sorted(docs.values(), key=lambda d: (d["filed"], d["accession"] or ""))


def assert_no_leak(payload: dict, cutoff: str, chronology_key: str = "filing_chronology") -> None:
    """독립 재검증 (가드 불신뢰 원칙) — 컷오프 후 filed 사실이 하나라도 있으면 예외."""
    for tag, vals in payload["financial_series_point_in_time"].items():
        for v in vals:
            if v["filed"] > cutoff:
                raise E2GenError(f"LEAK: {tag} filed={v['filed']} > cutoff={cutoff}")
    for ch in payload.get(chronology_key, []):
        if ch["filing_date"] > cutoff:
            raise E2GenError(f"LEAK: chronology {ch['form']} "
                             f"{ch['filing_date']} > cutoff={cutoff}")


def guard_pass(snapshot_id: str, ticker: str, payload: dict, registry: Path,
               data_dir: Path = DATA_DIR) -> int:
    """실제 cutoff_guard 경유 — 문서 단위로 load_document (fail-closed 그대로).
    accession 있는 문서는 가드의 EDGAR filingDate 교차검증까지 태운다."""
    n = 0
    for d in payload_documents(payload):
        cutoff_guard.load_document(
            snapshot_id, f"payload:{ticker}:{d['form']}:{d['accession'] or d['filed']}",
            d["filed"], accession_no=d["accession"],
            registry_path=registry, edgar_data_dir=data_dir,
            loader=lambda p: "")
        n += 1
    for ch in payload.get("filing_chronology", []):
        cutoff_guard.load_document(
            snapshot_id, f"chronology:{ticker}:{ch['form']}:{ch['filing_date']}",
            ch["filing_date"], registry_path=registry,
            edgar_data_dir=data_dir, loader=lambda p: "")
        n += 1
    return n


# ---------------------------------------------------------------- generation

def compute_manifest(roster: list[dict], data_dir: Path = DATA_DIR) -> dict:
    """순수 산술 — 파일 생성 없이 전 행 회계 (러너의 드리프트 대조에도 사용)."""
    rows = []
    for case in roster:
        base_id = case["base_case"]["case_id"]
        grid = snapshot_grid(xbrl_filings(case["base_case"]["ticker"],
                                          case["base_cutoff"], data_dir))
        for g in grid:
            rows.append({"snapshot_id": f"{base_id}_s{g['j']}",
                         "base_case_id": base_id,
                         "ticker": case["base_case"]["ticker"],
                         "tier": case["tier"], "group": case["group"], "j": g["j"],
                         "status": "buildable" if g["eligible"] else "grid_ineligible",
                         **({"cutoff": g["cutoff"]} if g["eligible"]
                            else {"reason": g["reason"]})})
    buildable = sum(1 for r in rows if r["status"] == "buildable")
    return {"generator": GEN_VERSION, "rows": rows,
            "totals": {"buildable": buildable,
                       "grid_ineligible": len(rows) - buildable,
                       "build_failed": 0},
            "budget_of_record": {"evaluatee_calls": buildable, "grader_calls": 0,
                                 "cite": "D65 주석 2"}}


def generate(out_root: Path = OUT_ROOT, data_dir: Path = DATA_DIR,
             repo: Path = REPO, only_tickers: set[str] | None = None) -> dict:
    roster = derive_roster(repo)
    if only_tickers is not None:
        roster = [c for c in roster if c["base_case"]["ticker"] in only_tickers]
    out_root.mkdir(parents=True, exist_ok=True)
    manifest = compute_manifest(roster, data_dir)

    registry = out_root / "registry_e2.json"
    registry.write_text(json.dumps(
        {"_meta": {"role": "cutoff_guard 스냅샷 레지스트리 (D66)", "generator": GEN_VERSION},
         "candidates": [{"case_id": r["snapshot_id"], "ticker": r["ticker"],
                         "cutoff_date": r["cutoff"]}
                        for r in manifest["rows"] if r["status"] == "buildable"]},
        ensure_ascii=False, sort_keys=True, indent=1) + "\n", encoding="utf-8")

    batches: dict[int, list[dict]] = {}
    for row in manifest["rows"]:
        if row["status"] != "buildable":
            continue
        case = next(c for c in roster if c["base_case"]["case_id"] == row["base_case_id"])
        entry = dict(case["base_case"])
        entry["cutoff_date"] = row["cutoff"]
        try:
            payload = bp.build_payload(entry, perturb=True)
            payload_send = {k: v for k, v in payload.items() if not k.startswith("_")}
            assert_no_leak(payload_send, row["cutoff"])          # 독립 검증
            n_docs = guard_pass(row["snapshot_id"], entry["ticker"],
                                payload_send, registry, data_dir)  # 실제 가드
            b3 = b3_score(entry["ticker"], datetime.date.fromisoformat(row["cutoff"]),
                          730, data_dir=data_dir)
            b4 = b4_score(entry["ticker"], datetime.date.fromisoformat(row["cutoff"]))
            record = {
                "snapshot_id": row["snapshot_id"], "base_case_id": row["base_case_id"],
                "tier": row["tier"], "group": row["group"], "j": row["j"],
                "ticker": entry["ticker"], "cik": entry.get("cik"),
                "snapshot_cutoff": row["cutoff"], "base_cutoff": case["base_cutoff"],
                "payload_sha256": hashlib.sha256(_canonical(payload_send)).hexdigest(),
                "documents": payload_documents(payload_send),
                "guard": {"documents_passed": n_docs},
                "b3_W8": {"score": b3["score"], "indicators": b3["indicators"],
                          "flags": b3["flags"]},
                "b4": ({"state": "computed", "score_slope_aug": b4["score_slope_aug"],
                        "score_level": b4["score_level"]}
                       if b4["score_slope_aug"] is not None else
                       {"state": "not_computable", "flags": b4["flags"],
                        "cite": "D61 — 커버 2/13, 상태를 생략하지 않고 기록"}),
                "generator": GEN_VERSION,
            }
            (out_root / f"{row['snapshot_id']}.json").write_text(
                json.dumps(record, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
                encoding="utf-8")
            batches.setdefault(row["j"], []).append(entry)
        except (E2GenError, cutoff_guard.CutoffGuardError,
                FileNotFoundError, KeyError, ValueError) as e:
            row["status"] = "build_failed"
            row["reason"] = f"{type(e).__name__}: {e}"
            manifest["totals"]["buildable"] -= 1
            manifest["totals"]["build_failed"] += 1
            manifest["budget_of_record"]["evaluatee_calls"] -= 1

    for j, entries in sorted(batches.items()):
        (out_root / f"cases_e2_s{j}.json").write_text(json.dumps(
            {"_meta": {"role": f"E2 스냅샷 s{j} 러너 배치 — evaluatee 5필드만 "
                               "(메타는 사이드카 기록에, 페이로드 복사 누출 방지)",
                       "variant": "perturbed only (PLAN §2)",
                       "generator": GEN_VERSION},
             "cases": sorted(entries, key=lambda c: c["case_id"])},
            ensure_ascii=False, sort_keys=True, indent=1) + "\n", encoding="utf-8")

    (out_root / "E2_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=1) + "\n",
        encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-root", default=str(OUT_ROOT))
    args = ap.parse_args()
    m = generate(Path(args.out_root))
    t = m["totals"]
    print(f"E2 생성 완료: buildable {t['buildable']} · grid_ineligible "
          f"{t['grid_ineligible']} · build_failed {t['build_failed']} — "
          f"예산 {m['budget_of_record']['evaluatee_calls']} evaluatee + 0 grader")
    return 0 if t["build_failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
