# Temporal Holdout Tier 1 — 결과 (H2/H3 branch): 암기 불가 사건 위 per-case 채점

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-07.
> 사전 커밋 기준: `docs/HOLDOUT_CRITERIA.md` (`62d2fda`, 채점 전). 피평가자
> claude-sonnet-5(핀), 채점 human_finalized=false. **전 후보 G2 provisional —
> "restatement/non-reliance event"로만 서술, "fraud"·"분식" 금지.** 컷오프 후
> 폭로라 암기가 **구조적으로 불가능**(recognition gate로 실증). 동결 결과 불침해.

## 1. RECOGNITION GATE (척추) — 통과 3/3 (기동결 `0d64a7a`)

HUBG·WMK·GNE 전원 폭로 사건 **비인지**(knows_event=False). 양성 대조
HTZ·KHC는 고신뢰 인지(계기 검증). ⇒ **N=3 편입, H3의 N<3 STOP 비발동.**
정체는 알되(WMK="Pennsylvania 슈퍼마켓") 폭로는 미암기 = 이상적 홀드아웃.

## 2. per-case 채점 (identity frame PRIMARY, 컷오프=폭로 전일)

| 회사 (G2) | 컷오프 | LLM p | tier | Beneish M | Dechow F | 플래그(p≥50) |
|---|---|---|---|---|---|---|
| **HUBG** (매입운송비 과소·미기록 AP, 임원 해임) | 2026-02-04 | **70** | elevated | 계산불능(결측2) | 계산불능(결측3) | **예** |
| **WMK** (재고 과대, 내부고발) | 2026-02-19 | 32 | watch | 계산불능(결측1) | 0.25 | 아니오 |
| **GNE** (캡티브보험 부채 오류, error-like) | 2026-03-11 | 42 | watch | −2.05 | 0.36 | 아니오 |

- **HUBG 강한 플래그(70)** — 가장 fraud-like한 케이스(미기록 AP + 임원 해임)를
  암기 불가 데이터에서 탐지. **기계 스크린은 HUBG의 M/F를 계산조차 못 했다**
  (결측) → LLM 신호는 Beneish/Dechow 복제가 아니다.
- **WMK 미탐(32)** — 재고 과대는 포착 못 함. **GNE 중간(42)** — error-like 성격에
  걸맞은 불확실. 기계 기준선도 셋 다 무플래그(GNE M −2.05는 −1.78 문턱 미달).

## 3. 발동 결론 규칙: **H2 (+ H3 정직 프레이밍)**

- **H1 (순열 p<0.05 → "분석적 탐지" 주장) 미충족·미실행**: N=3에서 매칭 대조군
  대비 순열 검정은 **구조적으로 과소검정**(3 vs ~6). 이 표본 크기로는 유의성
  주장을 하지 않는다 (사전 커밋 H1의 자격 미달).
- **H2 발동 (per-case 병기, no pooling)**: 홀드아웃 점수를 동결 분포와 병기 —
  wave-1 실험군 중위 57.5 / wave-2 중위 58 / 대조군 중위 ~34 대비, **HUBG 70 =
  실험군 상단**, GNE 42 = 경계, WMK 32 = 대조군대. 암기 불가 사건에서 **탐지력은
  실재하나(HUBG) 강도는 modest·혼재**(3중 1 플래그).
- **H3 정직 기록**: N=3은 유의성 주장에 부족 — 이것이 그 branch의 산출물이다.
  로스터·프로브·per-case 점수를 정직 발행하고 "후보 축적 대기"(월 재스캔,
  `docs/FUTURE_HOLDOUT_CANDIDATES.md`). 정답 키는 전원 **G2 provisional**;
  4.02/AAER 상향 시 티어 갱신.

## 4. 프로젝트 서사와의 정합 (핵심)

wave-1(유명 사건) = R3 **암기 얽힘**(점수 팽창). wave-2(덜 유명) = R4 **잔여
능력**(암기 약함, 이름 프로브 25%). 홀드아웃(**암기 불가**) = 탐지력이 **더
낮아지나 0은 아니다** — 가장 fraud-like한 HUBG를 잡음. 즉 **암기를 제거할수록
점수가 내려가되(57.5→58→per-case 32~70) 신호는 잔존**한다 = "분리의 일부는
암기, 일부는 분석"이라는 Issue #0의 R3 헤드라인을 암기 불가 축에서 독립 확증.
단 N=3, 단일 파이프라인 — 능력의 크기 추정이 아니라 존재의 방향 증거.

## 5. E1 매칭 대조군 (2026-07-09 감독 실행 완료 — Q-E03 RESOLVED)

사전 등록 `HOLDOUT_CONTROLS_PLAN.md` 그대로: 동결 순수 함수 선정(케이스당 3,
FWRD는 recognition gate knows_event=True로 탈락 → XPO 승격), 비인지 게이트 9/9
admit, identity frame 채점. 결과 (`analysis/holdout_controls_results.json`):

- **per-case 병기 (1차 산출)**: **HUBG 70 > 매칭 대조군 전부** (RXO 42 · BCO 30 ·
  XPO 20) — H2 방향 강화. **WMK 32는 분리 미검출** (GO 58 · SFM 32 · VLGEA 12 —
  동률/하회). **GNE 42도 분리 미검출** (GRDX 78 상회 · VIASP 35 · UTL 20). §7
  사전 명시대로 정직 보고: 3케이스 중 1건만 대조 우위.
- **대조군 FPR**: 2/9 = 22.2%, Clopper-Pearson 95% **[2.8%, 60.0%]** (GRDX 78 ·
  GO 58). wave-1 3/22 · wave-2 5/23과 구간 크게 겹침 — 비교 주장 없음.
- **정확 순열 p = 0.2045 — CONTEXT ONLY** (N=3 과소검정, H1 미주장 사전 명시).
- HUBG 단서 유지: 대조 우위는 tier 적중의 강화이지 기제 정확성(dim2=1) 입증 아님.
- 채점 9건 확정 상태는 `scoring/grades_holdout_controls/` 참조.
- verbatim/이름 프로브: 미실행 (recognition gate가 핵심 계기, 완료).

## 6. 면책

각 서술은 공개 8-K(Item 4.02)에 근거한 **의견**이며 SEC 확정 부정 아님(G2
provisional). 포지션 없음, 비공개 정보 미사용, 교육·정보 목적. 단일 Claude
파이프라인, 채점 Claude 보조 + 인간 확정 대기.
</content>
