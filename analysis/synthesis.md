# 교차-웨이브 종합 (P2) — 암기 dose-response + 통합표 + 웨이브별 규칙

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-08.
> 재현: `python analysis/synthesis.py` (결정론, seed 20260708) → `synthesis.json` +
> `unified_table.csv` + `fig_memorization_doseresponse.png`. 동결 함수만 재사용
> (probe_verdict.name_match · screens.run_case · stats.auc/boot_auc_ci) — 재채점 없음.
> **범위 한정(§5-5)**: Claude 단일 파이프라인(claude-sonnet-5 핀) 한정.

## 1. 암기 dose-response (핵심 그림)

| tier | name-ID(암기 대리) | 분리 AUC (부트 95% CI) | 규칙 |
|---|---|---|---|
| wave-1 (유명) | **50.0%** | **0.824** [0.599, 0.983] | R3 (암기 얽힘) |
| wave-2 (덜 유명) | **21.9%**¹ | **0.829** [0.616, 0.983] | R4 (잔여 능력) |
| 홀드아웃 (컷오프후·암기불가) | **0.0%** (recognition gate 0/3) | N=3, AUC 불가 — per-case HUBG 70·GNE 42·WMK 32 | H2 |

**판독 (백본 = standalone 유의성)**: 암기 대리지표(name-ID)가 50% → ~22% → 0%로
반감·소멸하는 동안, **각 wave의 standalone 순열 유의성이 독립 생존한다** — wave-1
p=0.00114 · wave-2 p=0.00116 — 그리고 암기가 구조적으로 불가능한 홀드아웃에서도
가장 misstatement-like한 HUBG를 70으로 탐지(E1 매칭 대조군 상회 + 5-draw robust,
2026-07-09). ⇒ **분리는 암기로 설명되지 않는다** — Issue #0의 R3 헤드라인("분리의
일부는 암기, 일부는 분석")을 암기 제거 축에서 독립 확증. **2차 gradient 관찰**:
AUC 0.824 [0.599, 0.983] → 0.829 [0.616, 0.983]는 점추정이 나란하다는 관찰일 뿐,
**CI 폭이 동등성 주장을 금지한다** (N=30·32 부트스트랩). 세 표본은 시대·유명도·라벨
tier가 달라 **통제 실험이 아니라 gradient 판독**이다.

¹ **name-ID 21.9%는 동결 `name_match` 규칙값(7/32)**. wave2_summary 산문의 25%(8/32)는
단일 경계 케이스 DAR(구명 "Darling International" 미처리)를 사람이 인식으로 계수한 값.
발행 규약 선택 = OWNER_QUEUE Q-E02. 어느 값이든 반감 서사 불변. 상세: `synthesis.json`
§wave2_name_id_reconcile.

## 2. 통합 점수표 → `unified_table.csv` (65행)

전 실험군·대조군(wave-1 30 + wave-2 32 + 홀드아웃 3) 1행/사, 열: wave · ticker · group ·
llm_score · flag(p≥50) · llm_perturbed · perturb_delta · recognized(동결규칙) · m_score ·
m_flag(≤−1.78) · f_score · f_flag(≥1). M/F는 동결 `screens.run_case`(오프라인) 실측.

- 기계 기준선의 한계 재확인: 홀드아웃 HUBG는 M/F **계산불능**(결측)인데 LLM은 70 탐지 →
  LLM 신호는 Beneish/Dechow 복제가 아님(R2·H2 정합).

## 3. 웨이브별 발동 규칙 (자동 흐름)

- wave-1 = **R3**(암기 얽힘) · wave-2 = **R4**(잔여 능력) · 홀드아웃 = **H2**(per-case, N=3).
- **E3 의존**: wave-2 규칙은 E3(교란 재추첨) 확정 시 사전 등록 규칙에 따라 자동 갱신 —
  median-delta dominance ≥5/9면 R3가 R4를 supersede(그때 본 표·그림·Issue 자동 갱신).
  현재 단일 draw 기준 3/9 → R4. (E3 미실행: launch-ready.)

## 4. 3층 서사 (Issue #0/#1/#2 공통 골격)

유명 사건(wave-1) → R3 암기 얽힘(점수 팽창) → 덜 유명(wave-2) → R4 잔여 능력(name-ID
반감) → 컷오프후 홀드아웃(암기 불가) → 신호 약화하나 붕괴 아님(HUBG는 M/F가 계산조차
못한 곳에서 탐지). **"bounds, not eliminates"** — 암기를 제거할수록 점수는 내려가되
신호는 잔존.

## 5. 면책

단일 Claude 파이프라인 한정, 채점 Claude 보조 + 인간 확정 대기. 대조군="비집행"(무결
아님). 홀드아웃 G2 provisional. 통제 실험 아님(표본 이질) — gradient 방향 증거.
