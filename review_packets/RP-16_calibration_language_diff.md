# RP-16 — 보정 언어 diff 제안 (WS-4/F-7, diff-only, 미적용)

> **상태: PROPOSED — 소유자 서명(Q-F04) 전 어떤 발행 표면도 수정하지 않았다.**
> 근거: `specs/calibration_scope.md` — 발행 점수 = 서수(ordinal) 해석 규약.

## 전수 히트 목록 (repo-wide grep `probabilit`, 발행 표면 한정)

| # | 파일:라인 | 내용 | 처분 제안 |
|---|---|---|---|
| 1 | `analysis/ISSUE_0_DRAFT.md:163` (= GitHub Issue #1 본문) | "these probabilities are rankings, not calibrated risk estimates" | **DIFF-6** 교체 (아래) |
| 2 | `analysis/ISSUE_2_HOLDOUT_DRAFT.md:71` (= GitHub Issue #3 본문) | 표 헤더 `LLM p` | **DIFF-7** 교체 (아래) |
| 3 | `schemas/llm_output.json` `misstatement_probability` | 스키마 필드명 | **무변경** — Cycle-2 개명 등록 (스펙 §4-1, 커밋 출력 재현성) |
| 4 | `README.md:156` / `README.ko.md:108` | ECE 진단 병기 서술 | **무변경** — 이미 진단 전용 프레임 ("no improvement, null-ish") |
| 5 | `docs/reader_validation/ONE_PAGER.md` | 히트 0 | 해당 없음 |

## DIFF-6 (ISSUE_0 §5 Calibration 불릿 — Issue #1 본문 동반)

**원문**:

```
  (AUROC 0.656). Reported as a finding: these probabilities are rankings, not
  calibrated risk estimates.
```

**교체안**:

```
  (AUROC 0.656). Reported as a finding: the 0–100 output is an ordinal score —
  it ranks and flags (threshold 50), but does not function as a probability
  ("70" is not "70% risk"). We do not recalibrate at this N: Platt/isotonic
  fitting at N≈30–60 is dominated by binning noise, and small-N ECE is itself
  an unstable estimate — ECE is retained as a diagnostic co-report only.
  Verbalized-confidence research finds LLM-stated confidence systematically
  overconfident, so this miscalibration is expected model behavior, not a
  pipeline artifact.
```

## DIFF-7 (ISSUE_2 §2 표 헤더 — Issue #3 본문 동반)

**원문**: `| company (G2) | cutoff | LLM p | 5-draw band (k=5) | ...`

**교체안**: `| company (G2) | cutoff | LLM score (0–100, ordinal) | 5-draw band (k=5) | ...`

(동일 표기 원칙: 발행 표면의 케이스 점수 인용에서 "p=70" 형태가 추가 발견되면
"score 70"으로 — 본 packet 히트 목록이 전수이며, 순열 검정의 통계 p-값과는
표기 충돌 없음을 확인함.)

## 적용 조건

- 소유자 Q-F04 서명 후에만. GitHub Issue 본문 수정은 edited 표시 + 사유
  코멘트 병행 권장 (RP-15와 동일 규약). 적용 시 서명 블록 + decisions_log 기록.

---

## 서명 블록

**결정: 수용 — DIFF-6/DIFF-7 적용** (owner, 2026-07-16, this session's
structured decision responses). repo 표면 반영: ISSUE_0 §5 보정 불릿·ISSUE_2
§2 표 헤더 (D91). 스키마 필드 무변경. GitHub Issue #1/#3 편집 = 소유자 잔여.
