# FREEZE_REV4_HARNESS_E2.md — freeze 개정 #4: E2 및 금야(2026-07-13) 발사분의 하네스 경로 확정

> **서명**: (owner, 2026-07-13, written overnight authorization — this mission's
> prompt, §A-1). 본 문서는 배선 코드가 존재하기 전에 커밋된다
> (freeze-commit-then-run — git 타임스탬프가 증거).
>
> **본 문서가 지배하는 발사**: 금야 미션의 P0(E2)·P2(E4)·P3(Q-F05 v2 프로브)·
> P4(Q-F06-B k=3) — §4 발사별 적용표 참조. 문서 1개·서명 1개.

## 1. 무엇을 확정하나

E2(조기성)와 금야의 나머지 하네스 발사분은 **동결 구독 하네스 경로**
(`pipeline/cli_client.py`, `claude -p`, freeze 개정 #2)에서 실행한다 —
지금까지 발행된 모든 tier(wave-1/2, holdout, E1, E3, 전 프로브)와 동일 경로.

raw API 경로(freeze 개정 #3, D40 GO)는 **DEFERRED — 폐기가 아니다**:

- FREEZE_REV3_DRAFT.md와 그 스모크 래치(§6-3)는 **한 몸으로 이동**한다 —
  raw 경로가 실제로 사용되는 시점까지. 스모크 래치는 raw 경로의 전제이므로
  하네스 발사에는 적용되지 않는다 (`make smoke`는 금야 스코프 밖).
- `pipeline/api_client.py`·`runner_api.py` 스캐폴드는 무변경 동결 유지.
  `AAER_RAW_API_APPROVED`는 금야 어떤 시점에도 설정하지 않는다.

## 2. 근거 (record verbatim — 소유자 지시문 원문)

> (a) **path-consistency** — the LLM-vs-B3 lead-time verdict compares LLM
> scores produced the same way as all frozen tiers; (b) **zero marginal
> cost**; (c) freeze rev #3 (raw API) is **DEFERRED, not revoked** — it and
> its smoke latch travel together to whenever the raw path is actually used.

한국어 요지: E2의 산출물(LLM 점수 궤적)은 동결 tier들과 같은 방식으로 생산될
때에만 리드타임 비교가 경로 교란 없이 성립한다. 한계 비용 0(구독). 개정 #3은
보류이지 철회가 아니며, 발효 조건(§6 래치 4건)은 원문 그대로 유효하다.

## 3. 정직한 비용 (record verbatim — 소유자 지시문 원문)

> **L-2** (harness system-reminder injection, incl. currentDate vs PIT
> framing) is **INHERITED by E2** and must appear on any E2 publication
> surface as an inherited limitation; **L-3** remains open (no temperature
> pin on the harness — e2_runner's TEMPERATURE_PIN assertion is N/A in
> harness mode; E5 §7 draw-noise bands are the interpretive resolution
> limit).

이행 규칙:

1. **L-2 상속**: E2 결과가 닿는 모든 발행 표면(요약·이슈·릴리스)은 L-2를
   상속 한계로 명기해야 한다. currentDate 주입은 컷오프 역산→암기 회수 촉진
   방향(L-2 인과 명세)이므로 PIT 프레이밍 편차로 기록된다.
2. **L-3 미해소**: 하네스에는 temperature 핀이 없다 — `tools/e2_runner.py`의
   `TEMPERATURE_PIN` 상수·assert는 하네스 모드에서 N/A (raw 모드 전용 레일).
   해석 분해능의 한계는 E5 §7 draw-노이즈 밴드가 정의한다.

## 4. 발사별 적용표 (금야, 전부 하네스 경로 — 본 문서 1서명으로 커버)

| 발사 | 규모 | 근거 문서 | 본 개정 적용 |
|---|---|---|---|
| P0 E2 조기성 | 146 evaluatee · 0 grader | analysis/EARLINESS_PLAN.md (D65 주석) · D66/D67 | §1–§3 전부 (L-2 상속 명기 의무) |
| P2 E4 교차모델 | ~20 (opus-4-8) | analysis/CROSSMODEL_PLAN.md | 동일 — EXPLORATORY 프레이밍(R4 제약) 유지 |
| P3 Q-F05 v2 프로브 | 62 | specs/perturb_v2.md §5 | 동일 — v1 기준선(동결)과 동일 하네스 경로라 비교 성립 |
| P4 Q-F06-B k=3 | 108 | specs/draw_k3.md | 동일 — draw-1(하네스)과 동일 경로, 통계 병기만 |
| (조건부) P5 E5 wave-2 arm | ~32 | W2_MAINSCORE_REDRAW_PLAN | 동일 — P0–P4 완료 시에만 |

- 전 발사 공통: `assert_no_metered_credentials`(INVARIANT 4) 강제 —
  `ANTHROPIC_API_KEY` 존재 시 즉시 예외. grader 호출 0. 동결 발행 수치 불변.
- J14("quota 소진을 목표로 삼지 않는다") 실행층 주의는 **금야 한정 소유자
  오버라이드** (미션 §2, 하드 캡 380호출 내) — 익일 이후 원상 복귀.

## 5. 불변량 (개정 #2·#3에서 승계)

- freeze-commit-then-run · 페이로드 가드(EVALUATEE_FORBIDDEN_MARKERS) ·
  서빙 모델 핀 검증 · SR 11-7 로그 스키마 — 경로와 무관하게 유지.
- 동결 결과 재실행 금지 — 발행된 draw-1 수치는 절대 불변, 신규 draw는
  통계 주석만 (specs/draw_k3.md 계약).
- 발행물에는 "E2는 하네스 경로(개정 #2 규약)로 실행되었고 개정 #3은 보류
  상태였다"를 경로 이력으로 명시한다 (FREEZE_REV3 §4 문구 규칙의 대칭).
