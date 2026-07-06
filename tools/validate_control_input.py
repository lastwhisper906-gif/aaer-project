"""RP-08 1c: 수집 풀 4층 방어 검증 (CONTROL_CRITERIA_v1 §6).

층 1 형태(shape): pool_extract.json 스키마 — 케이스·후보 레코드의 필수 필드,
      타입, 값 범위 (CIK 10자리, 날짜 ISO, 카운트 비음수, eligible↔fails 상호배타).
층 2 해시: MANIFEST.sha256 전 항목 실측 재해시 일치 + 매니페스트 밖 원시 파일 부재.
층 3 provenance: provenance.jsonl — 모든 네트워크 산출 파일에 URL·시각·HTTP 200
      기록 존재, sha256이 매니페스트/실측과 일치.
층 4 교차 일관성: pool_extract의 모든 후보 CIK에 대응하는 submissions 원시 파일
      존재 · pit_fetched=True인 후보의 companyfacts 존재 · 케이스 상수(CASES)와
      pool_extract의 컷오프 일치 · S0 절단 카운트 재계산 일치.

실패 항목은 runs/rp08/quarantine/quarantine.json에 사유와 함께 격리 기록 —
무침묵 탈락 금지. exit 0 = 전층 PASS (격리 0), exit 1 = 격리 존재.
"""
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rp08_common import (BIG_DIR, CASES, MANIFEST, N_PIT, PROVENANCE, RAW_DIR,
                         sha256_file)

QUARANTINE = RAW_DIR.parent / "quarantine/quarantine.json"

REQUIRED_CAND_FIELDS = ["cik", "sic_pool", "eligible", "fails"]
SCREENED_FIELDS = ["pre_cutoff_10K", "pre_cutoff_10Q", "xbrl_pre_cutoff",
                   "active_in_window", "item_402_in_window", "first_counted",
                   "former_names", "e4_hit_count"]


def check(problems: list, cond: bool, layer: str, what: str, detail: str = ""):
    if not cond:
        problems.append({"layer": layer, "item": what, "reason": detail})


def layer1_shape(pool: dict, problems: list):
    check(problems, "_meta" in pool and "cases" in pool, "1-shape", "pool_extract", "최상위 키")
    for tid, cdata in pool.get("cases", {}).items():
        check(problems, tid in CASES, "1-shape", tid, "미지의 케이스 ID")
        check(problems, bool(cdata.get("sics_used")), "1-shape", tid, "sics_used 공백")
        for cik, r in cdata.get("candidates", {}).items():
            wid = f"{tid}/{cik}"
            check(problems, re.fullmatch(r"\d{10}", cik) is not None, "1-shape", wid, "CIK 형식")
            for f in REQUIRED_CAND_FIELDS:
                check(problems, f in r, "1-shape", wid, f"필수 필드 부재: {f}")
            if r.get("eligible"):
                check(problems, not r.get("fails"), "1-shape", wid,
                      "eligible=True인데 fails 비공백")
                for f in SCREENED_FIELDS:
                    check(problems, f in r, "1-shape", wid, f"자격자 스크린 필드 부재: {f}")
                check(problems, r.get("pre_cutoff_10K", -1) >= 0
                      and r.get("pre_cutoff_10Q", -1) >= 0, "1-shape", wid, "카운트 음수")
                fc = r.get("first_counted")
                if fc:
                    try:
                        datetime.date.fromisoformat(fc)
                    except ValueError:
                        check(problems, False, "1-shape", wid, f"first_counted 비ISO: {fc}")
            else:
                check(problems, bool(r.get("fails")), "1-shape", wid,
                      "eligible=False인데 fails 공백 (무침묵 탈락)")


def layer2_hashes(problems: list) -> dict:
    manifest = {}
    if not MANIFEST.exists():
        check(problems, False, "2-hash", "MANIFEST.sha256", "부재")
        return manifest
    for line in MANIFEST.read_text().splitlines():
        if not line.strip():
            continue
        h, path = line.split("  ", 1)
        manifest[path] = h
        p = Path(path)
        if not p.exists():
            check(problems, False, "2-hash", path, "매니페스트 항목의 파일 부재")
        elif sha256_file(p) != h:
            check(problems, False, "2-hash", path, "sha256 불일치 (변조/부패)")
    for base in (RAW_DIR, BIG_DIR):
        for p in sorted(base.rglob("*")):
            if p.is_file() and p.name != "MANIFEST.sha256":
                check(problems, str(p) in manifest, "2-hash", str(p), "매니페스트 밖 원시 파일")
    return manifest


def layer3_provenance(manifest: dict, problems: list) -> dict:
    prov = {}
    if not PROVENANCE.exists():
        check(problems, False, "3-prov", "provenance.jsonl", "부재")
        return prov
    for i, line in enumerate(PROVENANCE.read_text().splitlines()):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            check(problems, False, "3-prov", f"line {i+1}", "JSON 파싱 실패")
            continue
        for f in ("url", "retrieved_at", "http_status", "sha256", "path"):
            check(problems, f in row, "3-prov", f"line {i+1}", f"필드 부재: {f}")
        if row.get("http_status") != 200:
            check(problems, False, "3-prov", row.get("path", f"line {i+1}"),
                  f"HTTP {row.get('http_status')}")
        prov[row.get("path")] = row
    # 네트워크 산출 파일(원시 디렉토리의 .atom/.json, 추출·매니페스트 제외)은
    # 전부 provenance를 가져야 한다
    for path in manifest:
        p = Path(path)
        if p.suffix in (".atom", ".json") and p.name not in (
                "pool_extract.json", "quarantine.json", "e4_manual_overrides.json"):
            row = prov.get(path)
            check(problems, row is not None, "3-prov", path, "provenance 부재")
            if row and row.get("sha256") != manifest.get(path):
                # 재실행 캐시 히트 시 provenance는 최초 수집분 — 파일이 그 후 변조
                # 되지 않았어야 하므로 불일치는 결함
                check(problems, False, "3-prov", path, "provenance sha256 ≠ 매니페스트")
    return prov


def layer4_cross(pool: dict, problems: list):
    for tid, cdata in pool.get("cases", {}).items():
        spec = CASES.get(tid)
        if spec:
            check(problems, cdata.get("cutoff") == spec["cutoff"], "4-cross", tid,
                  f"컷오프 불일치: {cdata.get('cutoff')} ≠ {spec['cutoff']}")
        n_trunc = 0
        for cik, r in cdata.get("candidates", {}).items():
            wid = f"{tid}/{cik}"
            if r.get("e4_hit_count") is not None or r.get("eligible"):
                sub = BIG_DIR / f"submissions/CIK{cik}.json"
                check(problems, sub.exists(), "4-cross", wid, "submissions 원시 부재")
            if r.get("pit_fetched"):
                facts = BIG_DIR / f"facts/CIK{cik}.json"
                check(problems, facts.exists(), "4-cross", wid, "companyfacts 원시 부재")
            if r.get("truncated_by_S0_cap"):
                n_trunc += 1
        rec = cdata.get("s0_truncated_count")
        check(problems, rec == n_trunc, "4-cross", tid,
              f"S0 절단 카운트 불일치: 기록 {rec} ≠ 재계산 {n_trunc}")


def main() -> int:
    pool_p = RAW_DIR / "pool_extract.json"
    problems = []
    if not pool_p.exists():
        problems.append({"layer": "1-shape", "item": str(pool_p), "reason": "부재"})
        pool = {}
    else:
        try:
            pool = json.loads(pool_p.read_text())
        except json.JSONDecodeError as e:
            problems.append({"layer": "1-shape", "item": str(pool_p), "reason": f"JSON 파싱: {e}"})
            pool = {}
    if pool:
        layer1_shape(pool, problems)
        manifest = layer2_hashes(problems)
        layer3_provenance(manifest, problems)
        layer4_cross(pool, problems)
    QUARANTINE.parent.mkdir(parents=True, exist_ok=True)
    QUARANTINE.write_text(json.dumps({
        "validated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "verdict": "PASS" if not problems else "FAIL",
        "problem_count": len(problems),
        "problems": problems}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{'PASS' if not problems else 'FAIL'} — 문제 {len(problems)}건 → {QUARANTINE}")
    for p in problems[:20]:
        print(f"  [{p['layer']}] {p['item']}: {p['reason']}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
