# BUYER_METRICS — 구매자 지표 4종 (E2 완료 후 자동 채움, D52)

> 이 파일은 템플릿이다. E2 완료 후 `analysis/buyer_metrics_build.py`가
> `{placeholder}`를 실측으로 채워 `analysis/BUYER_METRICS.md`를 생성한다.
> 어떤 값도 손으로 넣지 않는다 — 전 수치의 출처는 커밋 산출물
> (`e2_trajectories.json` + E2 호출 로그). 본 결과는 Claude 기반 단일
> 파이프라인에 한정된다 (PROJECT.md §5-5).

## 1. 탐지 리드타임 (조기성 — "몇 분기 먼저 아는가")

| 지표 | LLM (p≥50) | B3 규칙 (score≥2) |
|---|---|---|
| 중위 리드타임 (분기, 실험군 detected) | **{lead_llm_median}** | **{lead_b3_median}** |
| 케이스별 범위 | {lead_llm_range} | {lead_b3_range} |

- 정의: 스냅샷 궤적에서 임계를 처음 넘는 스냅샷의 폭로까지 분기 수
  (specs/ENGINE_DECISION.md §3 — 엔진 판정과 동일 산식·동일 데이터).
- n = {n_treatment} (E2 적격 = 본채점 detected fraud — EARLINESS_PLAN §1).

## 2. 오탐률 @ 임계 (대조군 궤적)

| 지표 | LLM (p≥50) | B3 (score≥2) |
|---|---|---|
| FPR (어느 스냅샷이든 임계 돌파) | **{fpr_llm}** | {fpr_b3} |
| Clopper–Pearson 95% CI | **{fpr_llm_ci}** | {fpr_b3_ci} |

- n = {n_control} 대조군 × 전 스냅샷. CP 구현은 동결
  `holdout_controls_analyze.clopper_pearson` 재사용 (신규 통계 코드 0).

## 3. 스크린당 비용 (실측 토큰)

| 항목 | 값 |
|---|---|
| 호출당 평균 입력 토큰 | {tokens_in_mean} |
| 호출당 평균 출력 토큰 | {tokens_out_mean} |
| 측정 호출 수 | {n_calls_measured} |
| **스크린당 비용 (1케이스 1스냅샷)** | **{cost_per_screen}** |
| 유니버스 1회전 (~300 stage-2) 추정 | {cost_stage2_pass} |

- 단가: {pricing_note}. 토큰은 E2 호출 로그의 `usage` 실측 — 추정 아님.

## 4. 커버리지 정의 (무엇을 스크린한 것인가)

- 실험군: {coverage_treatment}
- 대조군: {coverage_control}
- 스냅샷 깊이: {coverage_depth}
- 계산 불능/절단: {coverage_truncation}
- 한정: 리드타임·FPR은 위 커버리지 안에서만 정의된다 — 유니버스 일반화 금지
  (대조군 = "비집행"이지 "깨끗함 확정"이 아님, EARLINESS_PLAN §7).
