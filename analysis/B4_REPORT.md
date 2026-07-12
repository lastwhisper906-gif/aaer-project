# B4 리포트 — 비정상 공매도 잔고 기준선 (D52)

- 스펙: specs/B4_short_interest.md (커밋 4753824, 계산 전 동결)
- 데이터: FINRA Consolidated Short Interest, 하한 2017-12-29, PIT LAG 14일
- 시드 20260713 · perm 100,000 · boot 10,000 · 1차 점수 = slope-augmented

> 본 결과는 Claude 기반 단일 파이프라인의 보조 기준선 문서에 한정된다 (PROJECT.md §5-5). LLM/B1/B2/B3 값은 동결 인용 — 재계산 0.

## 5열 표 (tier별, pooled 없음)

| tier | B1 (M) | B2 (F) | B3 (W8) | **B4 (slope-aug)** | LLM | B4 커버리지 |
|---|---|---|---|---|---|---|
| wave1 | 0.5104 | 0.5729 | 0.7898 | 1.0000 ⚠️coverage-limited | 0.8239 | 3/30 |
| wave2 | 동결값 없음 | 동결값 없음 | 0.5483 | 계산 불가 ⚠️coverage-limited | 0.829 | 1/32 |
| holdout | 동결값 없음 | 동결값 없음 | 0.4259 | 0.1667 ⚠️coverage-limited | 없음(N=3) | 7/12 |

⚠️coverage-limited = 커버리지 <70% (스펙 §6) — **서술 전용, 헤드라인 주장 금지**. FINRA 무료 데이터 하한(2017-12-29)이 원인이며 사전 등록된 산술 그대로다.

## wave1

- **score_level**: coverage 3/30, AUC 1.0 CI [1.0, 1.0] p=0.332927
  - precision@3 = 0.3333 (1/3) — 농축 표본, 유니버스 precision@30과 수치 비교 불가 (스펙 §5)
- **score_slope_aug**: coverage 3/30, AUC 1.0 CI [1.0, 1.0] p=0.332927
  - precision@3 = 0.3333 (1/3) — 농축 표본, 유니버스 precision@30과 수치 비교 불가 (스펙 §5)
- 결측 케이스 (fail-closed): T07, T11, T12, T13, T16, T17, T21, V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20

## wave2

- **score_level**: coverage 2/32 — 통계 계산 불가(커버 처치/대조 부족)
- **score_slope_aug**: coverage 1/32 — 통계 계산 불가(커버 처치/대조 부족)
- 결측 케이스 (fail-closed): T02, T04, T19, T20, T22, T23, T24, T26, T29, W01, W02, W03, W04, W05, W06, W07, W08, W09, W10, W11, W12, W13, W14, W15, W16, W17, W18, W19, W20, W22

## holdout

- **score_level**: coverage 7/12, AUC 0.1667 CI [0.0, 0.5] p=0.856481
  - precision@2 = 0.0 (0/2) — 농축 표본, 유니버스 precision@30과 수치 비교 불가 (스펙 §5)
- **score_slope_aug**: coverage 7/12, AUC 0.1667 CI [0.0, 0.5] p=0.856481
  - precision@2 = 0.0 (0/2) — 농축 표본, 유니버스 precision@30과 수치 비교 불가 (스펙 §5)
- 결측 케이스 (fail-closed): GRDX, VIASP, VLGEA, case_71, case_73

## 해석 (스펙 §7 사전 등록 규칙)

- 비교 성립 tier: 없음
- 비교 성립 tier 없음 — wave-1/2는 커버리지 미달(<70%), holdout은 동결 LLM AUC 부재(N=3). 무료 신호 벤치마크는 전향 비교(E2 스냅샷·sealed 분기)에서 성립한다.
- 결합 조항: 비교 성립 조건 충족 미래 시점에서 LLM(또는 워치리스트) 성능 <= B4 성능이면 E2 평결과 동일 가중치로 엔진 결정 입력에 들어간다 — 완화 금지 (specs/B4_short_interest.md §7)
