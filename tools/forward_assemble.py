"""러너 출력(llm_output v1.2) → forward scores.json 기계 조립 (spec §6, D100).

usage: python tools/forward_assemble.py --cycle forward/cycle_001 \
    --runs runs/forward/cycle_001

**사전 등록 유도 규칙 (실행 시점 재량 0 — 봉인 전 개정은 일반 커밋+사유,
봉인 후 FREEZE_REV 전용):**

- `misstatement_risk_score` = `misstatement_probability` 값 그대로 (서수
  경계 개명 — specs/RISK_SCORE_SEMANTICS.md §3).
- `evidence_sufficiency`: checklist 중 finding=insufficient_data 비율 r —
  r > 1/2 → insufficient · r > 1/5 → partial · 그 외 → sufficient.
- `assessment_confidence`: checklist confidence의 평균 (high=3·medium=2·
  low=1) — ≥2.5 → high · ≥1.5 → medium · 그 외 → low.
- `decision_state`: insufficient → abstain · 그 외 score ≥70 flag /
  40–69 review / <40 no_flag (spec §5 서수 컷).
- `top_signals` = overall.top_signals · `affected_account_areas` =
  mechanism_hypotheses[*].affected_line_items 합집합(순서 보존) ·
  `cited_sources` = documents_used accession 목록.
- `benign_alternative_explanations` = [] — v1.2 출력 스키마가 이 항목을
  유도하지 않음 (spec §6 주석 — 프롬프트 확장은 Cycle-2 등록 후보).
- `prompt_sha256`/`schema_sha256` = 동결 러너 소스·출력 스키마 파일 해시.

레코드 부재 = not_scored 명시 등재 (spec §3-3). 네트워크 0 · 모델 호출 0.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_common import (REPO, assert_subscription_only, read_json, write_json,
                            sha256_file)

CONF_NUM = {"high": 3, "medium": 2, "low": 1}


def derive_sufficiency(checklist) -> str:
    r = sum(1 for c in checklist if c["finding"] == "insufficient_data") / max(len(checklist), 1)
    return "insufficient" if r > 0.5 else ("partial" if r > 0.2 else "sufficient")


def derive_confidence(checklist) -> str:
    if not checklist:
        return "low"
    mean = sum(CONF_NUM.get(c["confidence"], 1) for c in checklist) / len(checklist)
    return "high" if mean >= 2.5 else ("medium" if mean >= 1.5 else "low")


def derive_state(score: int, sufficiency: str) -> str:
    if sufficiency == "insufficient":
        return "abstain"
    return "flag" if score >= 70 else ("review" if score >= 40 else "no_flag")


def assemble_record(rec_meta: dict, out: dict | None) -> dict:
    base = {"record_id": rec_meta["record_id"],
            "company": {"name": rec_meta["name"], "ticker": rec_meta["ticker"],
                        "cik": rec_meta["cik"]}}
    if out is None:
        return {**base, "status": "not_scored"}
    checklist = out.get("checklist", [])
    score = out["misstatement_probability"]
    suff = derive_sufficiency(checklist)
    areas, seen = [], set()
    for h in out.get("mechanism_hypotheses", []):
        for a in h.get("affected_line_items", []):
            if a not in seen:
                seen.add(a)
                areas.append(a)
    return {
        **base,
        "misstatement_risk_score": score,
        "decision_state": derive_state(score, suff),
        "evidence_sufficiency": suff,
        "assessment_confidence": derive_confidence(checklist),
        "top_signals": out.get("overall", {}).get("top_signals", []),
        "benign_alternative_explanations": [],
        "affected_account_areas": areas,
        "cited_sources": [d["accession_no"] for d in out.get("documents_used", [])],
        "model_id": out.get("model", ""),
        "prompt_sha256": sha256_file(REPO / "pipeline/runner.py"),
        "schema_sha256": sha256_file(REPO / "schemas/llm_output.json"),
        "scored_at": out.get("run_timestamp", ""),
        "run_id": out.get("run_id", ""),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True)
    ap.add_argument("--runs", required=True, help="러너 출력 디렉토리 (케이스당 JSON)")
    args = ap.parse_args()
    assert_subscription_only()
    cycle = REPO / args.cycle
    runs = REPO / args.runs

    universe = read_json(cycle / "universe.json")
    records = []
    for r in universe["selected"]:
        # 러너 케이스 ID 규약: record_id를 케이스 ID로 사용
        out_path = runs / f"{r['record_id']}.json"
        records.append(assemble_record(r, read_json(out_path) if out_path.exists() else None))
    write_json(cycle / "scores.json", {"records": records,
                                       "assembled_by": "tools/forward_assemble.py",
                                       "derivation": "모듈 docstring 사전 등록 규칙"})
    n = sum(1 for r in records if r.get("status") != "not_scored")
    print(f"OK — scores.json 조립: scored {n}/{len(records)} "
          f"(미채점 {len(records) - n}건 not_scored 명시)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
