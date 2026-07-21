# RESULTS.md — 발행 수치 단일 표 (행별 한계 병기)

> Authored by Claude Code, pending human audit (GA-001 (b)). 신규 주장 0 —
> 전 행이 동결 산출물 경로를 단다. 존재 증명(existence-proof) 프레이밍:
> 성능 추정치가 아니다. 재검증: `make verify-public`. 태스크 태그·비합산
> 규율은 README "Three tasks" 절 (D106 ④). 채점: Claude 보조 + 인간 최종
> 확정. 본 결과는 Claude 기반 단일 파이프라인에 한정.

| # | [태스크] 측정 | 발행 수치 | 이 행의 한계 (같이 읽지 않으면 오독) | 소스 |
|---|---|---|---|---|
| 1 | [T1] wave-1 정체-노출 분리 (실험군 8 vs 대조군 22) | 순열 p 0.00114 · 평균차 +19.8pp · AUC 0.824 [0.599, 0.983] | 암기 얽힘 상한선 — R3 발동(8중 5 임계 초과), name-ID 50%. N=30 소표본, CI 광폭 | `analysis/results_stats.json` |
| 2 | [T1] wave-1 교란 프레임 (우선 판독) | 순열 p 0.0021 · AUC 0.864 [0.722, 0.969] · 플래그 4/8 | *덜 오염된* 측정이지 깨끗한 하한 아님 — 교란 후 잔여 정체 인지 5–6/8, v1 프레임은 부분 탈익명화 (accession·연대기 유지) | `analysis/results_stats.json` · `docs/V1_PARTIAL_DEIDENTIFICATION_NOTE.md` |
| 3 | [T1] wave-2 분리 (실험군 9 vs 대조군 23) | 순열 p 0.00116 · 평균차 +20.6pp · AUC 0.829 [0.616, 0.983] · 플래그 7/9 | R4 프레이밍 제약(정확도·AUC 비교 주장 금지). 직접 계기에선 outcome-knowledge 8/9 (88.9%, CP [51.7%, 99.7%]) 가용 | `analysis/wave2_results.json` (rev2 병행: `analysis/out/wave2_rev2/`, ERRATA E-002) |
| 4 | [T1] name-ID 축 | 50% (15/30) → 21.9% (7/32) → 0% | 21.9%는 동결 규칙값 — rename-aware 사람 판독 25%(경계 케이스 DAR) 각주 병기 (Q-E02) | `analysis/name_probe_results.json` · `analysis/synthesis.json` |
| 5 | [T2] 컷오프-후 홀드아웃 per-case 점수 | HUBG 70 · GNE 42 · WMK 32 (0–100 서수) | N=3, per-case 전용 — H1(순열 유의성) 미주장. 라벨은 잠정 Big-R(4.02 비신뢰)이지 확정 집행 아님. HUBG 적중은 tier 적중/기제 빗나감(2018 정정 클러스터 정박) | `runs/holdout/` · `analysis/label_tags_holdout.json` |
| 6 | [T2] E1 매칭 대조군 | HUBG 70 > 매칭군 전부 (RXO 42·BCO 30·XPO 20); 분리는 3케이스 중 1건만 | 정확 순열 p=0.20은 CONTEXT ONLY. 홀드아웃 tier 단일 최고점은 대조군 오탐(GRDX 78) — HUBG는 풀링 대조군 집합을 상회하지 못함 | `analysis/holdout_controls_results.json` |
| 7 | [T2] 홀드아웃 draw 강건성 (k=5) | HUBG 5/5 draw에서 ≥50 [58–76]; WMK [28–42]·GNE [30–42] 0/5 | 발행 수치는 draw-1 — 밴드는 병기 통계 | `runs/holdout_redraw/` (E5 §7) |
| 8 | [T1] FPR wave-1 | 3/22 = 13.6% CP95 [2.9%, 34.9%] | 대조군은 "비집행"이지 "무결(clean)"이 아니다 — 특이도 하향 편향 방향 (생존·선택 편향, README Limitations) | `analysis/results_stats.json` |
| 9 | [T1] FPR wave-2 | 5/23 = 21.7% CP95 [7.5%, 43.7%] | 위와 동일 + 오탐 5건은 환각이 아니라 실재 수치의 양성 오독 (근거됨, dim4 상단) | `analysis/wave2_results.json` · `analysis/error_analysis_wave2_holdout.md` |
| 10 | [T2] FPR 홀드아웃 대조군 | 2/9 = 22.2% CP95 [2.8%, 60.0%] | 티어 간 FPR 무언 합산 금지 — CP 구간 대폭 중첩, worse-but-not-provably | `analysis/holdout_controls_results.json` |
| 11 | [T1] 보정 (calibration) | ECE wave-2 0.179 (wave-1 0.209) | **점수는 서수(0–100 순위)지 확률이 아니다** — 보정 개선 없음(null-ish), 재보정은 N≈30–60에서 노이즈 지배 (`specs/calibration_scope.md`) | `analysis/calibration_wave2.json` |
| 12 | [T1] 기계 기준선 대조 | Beneish M p 0.498/AUC 0.510 · Dechow F p 0.268/AUC 0.573 · LLM 순위 상관 w1 −0.075/−0.144 · w2 0.333/0.293 (rev2 tie-aware) | 동일 30사·동일 PIT 한정. w2 상관 v1값 0.337/0.265는 동순위 미평균 구현 — 두 값 모두 R2 임계 0.7에서 멀어 판정 무영향 (E-002) | `analysis/baseline_table.csv` · `ERRATA.md` E-002 |
| 13 | [탐색 L4] E2 궤적 단일 임계 | T≥50: 탐지 12/12 CP [73.5%, 100%] · **오탐 5/7 = 71.4%** CP [29.0%, 96.3%] | **궤적 레이어에서 단독 LLM 임계는 지배 전략 없음** — 민감 임계는 오탐과 동행, 오탐 통제 임계(T=70)는 탐지가 먼저 죽는다(1/12). EXPLORATORY 결합 규칙(B3≥2 AND llm_p≥T)은 오탐 0/7이나 사후 규칙 — Cycle-2 sealed 후보로만 등록 | `analysis/DECISION_TABLE.md` §4 (서명 D94) |

산문 벽 없음 — 각 행의 서사적 맥락은 README 헤드라인 절과 게시 이슈
(README Publication 절 링크)가 담당한다. 표의 수치를 인용할 때는 해당 행의
한계 열을 함께 인용할 것.
