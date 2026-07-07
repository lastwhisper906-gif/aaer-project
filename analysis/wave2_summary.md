# Wave-2 결과 요약 — 발동 규칙 **R4 (능력 시연)**, standalone 1차

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-07.
> 사전 커밋 계획: `analysis/ANALYSIS_PLAN_WAVE2.md` (`9438b0c`, 채점 전). 재현:
> `python analysis/wave2_analyze.py` (결정론, seed 20260707) → `wave2_results.json`.
> 피평가자 claude-sonnet-5(핀), 채점자 fable-5, 채점 32건 **human_finalized=false**
> (소유자 확정 대기). 동결 wave-1(8v22) 불침해 — pooled는 2차 병기 전용.

## 1. 발동 결론 규칙: **R4** (사전 커밋 R1-R4의 기계 판정)

wave-2 STANDALONE(실험군 9 vs 대조군 23):

- **R1 (귀무) 비발동**: 1차 프레임 순열 p = **0.00116** (100k, seed 20260707,
  평균차 +20.6pp, fraud 55.2 vs control 34.7). p < 0.05.
- **R2 (기계 신호 복제) 비발동**: Spearman ρ(LLM, M-Score) = **0.337**,
  ρ(LLM, F-Score) = **0.265** — 둘 다 임계 0.7 미만 (M 계산가능 20/32, F 17/32).
- **R3 (암기 지배) 비발동**: 9 케이스 중 **3건**만 정체-교란 임계 초과
  (CSC·BRX·UAA) — 과반(≥5) 미달. wave-1의 5/8과 대조.
  - **E3 재추첨 확증 (2026-07-08, `analysis/e3_results.json`)**: 교란 +2 draw(동결
    payload 위 모델 표본 재추첨) → per-draw dominance 3→4→4, **median-delta 4/9**
    (< 5) → 사전 등록 규칙(W2_PERTURB_REDRAW_PLAN §3)상 **R4 유지**(R3 미발동, draw
    잡음에 강건). per-case σ 평균 **3.2pp**(wave-1 ~12pp보다 안정). draw-1 published 불변.
- ⇒ **R1·R2·R3 전부 비발동 → R4 발동**: "큐레이션된 케이스 집합 위 능력
  시연." **프레이밍 제약(R4)**: Bao/RUSBoost·EDINET 등과의 벤치마크 비교 가능
  정확도/AUC 주장 금지 (N·과제 정의·기저율 상이).

**wave-1과의 대조가 핵심**: wave-1(유명 사건: Hertz·Monsanto·KHC)은 R3(암기
얽힘) 발동. wave-2(덜 유명한 사건: CSC·WFT·OSIR·BRX·TNGO·CGI·MDXG…)는 암기
지표가 약해(3/9) R3 비발동 → 분리가 암기·기계신호 양자로 설명되지 않는 **잔여
능력**을 시사. 단 N=9, 단일 파이프라인 한정.

## 2. 통계 (사전 고정 검정)

| 통계 (1차 프레임: 정체 노출, 9 vs 23) | 값 |
|---|---|
| 평균차 (fraud − control) | **+20.6pp** (55.2 vs 34.7) |
| 순열 검정 (100k, 단측) | **p = 0.00116** |
| Cliff's δ | 0.657 |
| AUC (부트스트랩 95% CI, 10k) | **0.829 [0.616, 0.983]** — N=32 불안정, 점플롯이 1차 시각자료 |
| Fisher 플래그 p≥50 | fraud 7/9 · control 5/23 |
| 거짓양성률 | 5/23 = **21.7%**, Clopper-Pearson 95% [7.5%, 43.7%] (0% 금지) |
| 정체-가림(교란) 프레임 | +15.8pp · p = 0.00427 · AUC 0.79 |

기준선 자체 분리(동일 32사): 계산가능분에서 M/F 모두 약분리 — LLM 순위는 두
기계 스크린과 낮은 상관(0.34/0.27)이라 잔차 분리가 유지된다(R2 비발동).

## 3. 오류 해부 (채점 기반, human_finalized=false)

- **탐지 7/9** (dim1 밴드 ≥1): WFT·CGI(밴드2) · HAIN·MDXG·OSIR·TNGO·UAA(밴드1).
  기제 정합(dim2): 대부분 1–2 (계정 영역+방향 일치), WFT는 밴드2이나 dim2=0
  (옳은 시점, 그른 기제).
- **미탐 2**: **CSC**(p=20) · **BRX**(p=40) — 공교롭게 정체-교란 초과 3건 중
  2건(암기 얽힘 케이스가 오히려 미탐). BRX는 REIT(표준 매출 태그 결측 — 커버리지
  주석), CSC는 대형 IT서비스 다분기.
- **거짓양성 5/23** (dim1=0, p≥50): IOVA·ADAM·LEVI·LPSN·AORT. **전건 근거됨(dim4
  상단) — 환각(i) 아니라 실재 수치의 양성 오독(ii-a)**. 전수 해부(taxonomy 4분류·
  verbatim 인용·CSC/BRX 미탐 비대칭·HUBG tier적중/기제빗나감·ECE 0.179):
  **`analysis/error_analysis_wave2_holdout.md` (P1, 이 스텁 해소)**.

## 4. 암기 계층화 (ANALYSIS_PLAN_WAVE2 §9)

- **이름 예측 프로브(익명 페이로드) 정답률 25%** (실험군 3/9, 대조군 5/23) —
  **wave-1의 50%(대조군 54.5%)의 절반**. wave-2 표본은 익명화가 더 잘 견딘다 =
  각인된 스캔들 지식이 약함. R3 비발동과 정합.
- 정체-교란 Δ가 임계를 넘은 3건(CSC·BRX·UAA)만 암기 의심 — 소수.

## 5. Pooled 2차 (병기 전용 — 단독 헤드라인 금지, DO NOT)

pooled wave1+wave2 (실험군 17 vs 대조군 45, wave-1 동결 점수 **재사용·재채점
없음**): 평균차 +20.2pp, 순열 p = **3.0e-05**, AUC 0.831. 표본 확대가 분리를
**강화**(희석 아님). 단 발동 규칙 헤드라인은 **standalone R4**이며, pooled는
맥락일 뿐이다.

## 6. 한계

N=9 실험군, 단일 파이프라인(claude-sonnet-5), 채점 Claude 보조+인간 확정 대기.
AAER 선택·생존 편향, 대조군 라벨="비집행"(무결 아님). R4 프레이밍 제약 준수 —
성능 추정치가 아니라 존재 증명. 컷오프 후 홀드아웃(암기 불가)이 능력 질문의
독립 검증.
</content>
