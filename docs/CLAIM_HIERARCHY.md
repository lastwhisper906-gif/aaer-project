# docs/CLAIM_HIERARCHY.md — 증거 수준별 주장 위계 (모든 현재·미래 주장의 상한)

> 2026-07-20, owner plan §3 위임 (ledger D100). 이 문서는 이 저장소의 어떤
> 산출물이 어떤 수준의 주장까지 지지하는지를 고정한다. 상위 수준 주장은
> 해당 수준의 증거 없이 쓸 수 없다. 기계 강제: `tools/lint_publication.py`
> 규칙 (K).

## Level 0 — Engineering validity (엔지니어링 유효성)

> The pipeline executed under the stated controls and its published
> calculations are reproducible from committed artifacts.

파이프라인이 선언된 통제 하에 실행되었고, 발행 계산이 커밋 산출물에서
재현된다. (게이트: pytest·reproduce·lint·blindness·verify_manifest 5종.)

## Level 1 — Case-specific evidence (케이스 특정 증거)

> The frozen system identified specified accounting-risk signals in a
> particular case.

동결 시스템이 특정 케이스에서 명시된 회계 위험 신호를 식별했다.
(예: HUBG 스코어 70 + 근거 인용 — 단일 케이스 서술, 통계 주장 아님.)

## Level 2 — Retrospective selected-sample separation (회고·선택 표본 분리)

> Scores differed between treatment and controls in this selected
> retrospective sample.

이 **선택된 회고 표본** 안에서 실험군·대조군 점수가 분리되었다. 표본 선택
규칙 밖 일반화 없음. 암기 오염은 통제로 **경계 지을 뿐 제거하지 못한다**
(README 배너).

## Level 3 — Prospective forward evidence (전향 봉인 증거)

> Scores sealed before the outcome showed a specified relationship with
> subsequently observed events.

결과 관측 **이전에 봉인된** 점수가 이후 관측 사건과 사전 지정된 관계를
보였다. 요건: 유니버스 사전 동결 + 컷오프 기계 검증 + 외부 검증 가능
타임스탬프 봉인 + 사전 등록 판독 규칙 (`specs/FORWARD_WATCHLIST_V1.md`).

## Level 4 — Population performance (모집단 성능) — **본 프로젝트 미지지**

광범위하고 방어 가능한 표본틀, 현실 기저율, 충분한 표본 수, 성숙한 라벨,
전향 평가, 그리고 가급적 외부 재현을 요구한다. **현재 프로젝트는 Level 4
주장을 지지하지 않는다.** 12사 협의-SIC 유니버스의 forward 결과도 그 유니버스
정의 밖으로 일반화되지 않는다.

## 현재 산출물 매핑

| 산출물 | 주장 수준 | 비고 |
|---|---|---|
| v1 wave-1 (Issue 0, R3) | **Level 2** | 유명 케이스 — 암기 얽힘 명시 |
| v1 wave-2 (Issue 1, R4) | **Level 2** | 잔여 능력 — R4 프레임 제약 (벤치마크 비교 금지) |
| post-cutoff holdout (Issue 2, H2) | **주로 Level 1** (+제한적 Level 2 문맥) | N=3 per-case; H1 통계 주장 없음 (사전 선언) |
| GIL 메모 (Issue 4) | **Level 1** | post-hoc selection 트랙 — 선정 배경 공개 의무 |
| 첫 forward seal (2026-11-15, 결과 성숙 전) | **Level 0** | 성공 기준 = 봉인 무결성, 예측 성능 아님 |
| 성숙한 forward 사이클 (6–48개월 후) | **잠재 Level 3** | 사전 등록 판독 규칙 충족 시에만 |

## 금지 문구 (현 증거 수준에서 무자격 사용 금지 — lint (K) 강제)

- "predicts fraud in public companies"
- "estimates real-world fraud probability"
- "validated fraud detection system"
- "population-level performance" (긍정 주장으로)
- 한국어 동형: "검증된 사기 탐지 시스템" · "모집단 수준 성능"

부정·한정 문맥("does not support population-level performance")은 허용.

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
