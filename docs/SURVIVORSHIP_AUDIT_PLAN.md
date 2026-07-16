# SURVIVORSHIP_AUDIT_PLAN — 대조군 풀 생존 편향 감사 (사전 등록, 실행 전)

> **사전 등록 문서 — 실행 없음 (Q-F08, owner 2026-07-16: "draft audit plan
> only").** 감사 실행은 네트워크가 필요하므로 소유자 감독 세션 전용
> (Q-E03 선례). 이 문서는 감사 방법·판독 규칙을 결과를 보기 전에 고정한다.
> 미터링 0 (전 단계 무-LLM — 결정론적 대조뿐).

## 1. 감사 대상 가설

대조군 풀이 **수집 시점(2026-07)의 EDGAR SIC browse**에서 열거되었으므로,
그 이전에 상장폐지(Form 25)·등록취소(Form 15)된 발행사가 풀에서 체계적으로
누락되었을 수 있다. 편향 방향은 단방향으로 예측된다: **대조군이 "깨끗한
생존자" 쪽으로 기울어 실험군-대조군 분리를 과대평가**할 수 있다 (실험군은
시대 불문 AAER 확정 케이스이므로 동일 필터를 받지 않는다). RP-18 게시문이
"registered separately as an audit item"으로 공표한 항목이 바로 이것이다.

## 2. 데이터와 절차 (결정론 — LLM 0)

입력 (전부 커밋 산출물 + 공개 인덱스):
1. 풀 수집 스냅샷: `runs/rp08/`·`runs/rp09/` (wave-1/2 대조군 풀 원본) ·
   `runs/holdout/controls/pool_raw/` (E1 풀).
2. 실험군 컷오프 연도별 기준: `data/evaluatee/cases*.json`의 cutoff_date.
3. 상장폐지·등록취소 기록: EDGAR full-text가 아니라 **폼 타입 인덱스**
   (Form 25 / 25-NSE / Form 15) — 수집은 감독 세션에서 `tools/
   fetch_primary_sources.py` UA 규약으로.

절차:
- (a) 풀 스냅샷의 CIK 전수에 대해 이후 Form 25/15 제출 여부를 대조 →
  "수집 당시 생존, 이후 소멸" 비율 r₁.
- (b) 각 실험군 컷오프 연도에 해당 SIC에 존재했으나(당시 10-K 제출 실적)
  현재 열거에 부재한 CIK 수를 폼 인덱스로 역산 → 누락 규모 추정 r₂
  (연도별 표).
- (c) r₂의 케이스: 소멸 사유 표본 분류 (합병/사유화 vs 파산/폐지 — 후자가
  EQ 관점에서 "깨끗하지 않은 소멸").

## 3. 판독 규칙 (사전 고정 — 결과 열람 후 변경 금지)

- r₂ 중 파산/폐지형 소멸이 **풀 크기의 ≥10%**: 발행 표면 한계 절에
  "control-pool survivorship: separation estimates carry an upward-bias
  risk of unmeasured magnitude" 문구 의무 + 향후 풀 수집을 point-in-time
  인덱스로 개정하는 FREEZE_REV 후보 등록.
- **<10%**: 한계 절에 측정치 병기로 충분 (L-8 확정, 문구는 측정값 인용).
- 어느 쪽이든 **기존 동결 결과의 재계산·재채점은 하지 않는다** — 이 감사는
  한계의 크기를 재는 것이지 결과를 고치는 것이 아니다.

## 4. 실행 조건

- 소유자 감독 세션 (네트워크 fetch 승인) — `docs/RESUME.md` 차기 감독 세션
  2번 작업으로 등재. 유니버스 열거(1번)와 같은 세션에 편승 권장 (동일
  인덱스 fetch 재사용).
- 산출물: `analysis/survivorship_audit.json` + 본 문서 §3 규칙의 기계 판독.

본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).
채점: Claude 보조 + 인간 최종 확정.
