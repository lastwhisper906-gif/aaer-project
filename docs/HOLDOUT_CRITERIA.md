# HOLDOUT_CRITERIA — Temporal Holdout Tier 1 사전 커밋 기준

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-07.
> **지위: 홀드아웃의 어떤 채점 호출보다 먼저 커밋된다.** 목적: 암기가 **구조적
> 으로 불가능한** 사건 위의 분석 능력 시험 — 피평가자 claude-sonnet-5의 지식
> 컷오프(2026-01) **이후** 최초 폭로된 회계 사건. 본 결과는 Claude 단일
> 파이프라인 한정(§5-5). 동결 wave-1·wave-2 결과 불침해.

## a. Universe (사전 고정)

- **1차 (primary)**: `docs/FUTURE_HOLDOUT_CANDIDATES.md` Tier 1 —
  **HUBG**(2026-02-05, 8-K Item 4.02) · **WMK**(2026-02-20) · **GNE**(2026-03-12).
- **2차 풀 (secondary)**: MPWR·CORZ·NFE·AVAV — 동일 게이트 적용 후 조건부 편입.
- 공매도-리포트 단계(ADMA·GIL·VERI 등)는 정답 키 미확정 리스크로 **이번 티어
  제외**(4.02/집행 확인 후 재고). RR = E1급 이력 미달 예비.

## b. 라벨 티어 (사전 커밋 — 프로즈 제약)

**G1 AAER > G2 8-K Item 4.02 > G3 SEC complaint > G4 DOJ indictment.**
현 후보 **전원 G2 = PROVISIONAL**. 프로즈는 **"restatement / non-reliance
event"**로만 서술하고 **"confirmed fraud"·"분식"·"조작"을 절대 쓰지 않는다**.
월 1회 재조사로 티어 소급 상향(G2→G1 등). 상향 이력은 추가 기록.

## c. A-type 스크린 (wave-1과 동일)

각 후보에 대해: ① 스킴이 **폭로 전 흔적**을 남기는가(재무제표 발자국), ②
**최소 사전-폭로 XBRL 분기 수** 충족, ③ **Principle-A 폭로일** EDGAR 1차 문서
검증. 추가로 **스킴 유형이 fraud-like vs error-like인지 케이스별 정직 기록**
(사용하되 제외 근거로 쓰지 않음):
- **WMK**: 재고 과대계상 + 내부고발 → **강(fraud-like)**.
- **HUBG**: 매입운송비 과소계상·미기록 AP + 임원 해임 → **강**.
- **GNE**: 캡티브 보험 부채 회계 오류 → **약(error-like)** — 부정성 조사 대기.

## d. RECOGNITION GATE (척추 — 편입의 사활)

**절차**: 각 후보 회사 **및 각 매칭 대조군**에 대해 claude-sonnet-5를 프로브 —
**폭로 후 사건**(재작성·비신뢰 공시·임원 해임 등)을 아는가. 프로브 스키마·
채점은 동결 인지 프로브 계기 재사용.
- **오직 폭로 사건의 NON-RECOGNITION이 실증된 케이스만 편입**한다. 인지가
  드러나면 홀드아웃 자격 상실(암기 오염).
- **경계 케이스(HUBG, 컷오프 +5일)**: `FUTURE_HOLDOUT_CANDIDATES §3`의 직접
  최근사 스크린(모델에 회사 최근 사건 직접 질문)을 **추가**로 통과해야 함.
- **프로브 transcript를 증거로 커밋**(runs/holdout probes).

## e. 대조군 (사전 커밋)

동결 순수 함수(`control_v2`) 그대로, 케이스당 **2–3**. 대조군도 **자신의 폭로-후
기간에 대해 동일 non-recognition 게이트를 통과**해야 한다. E8b 집행 이력 스크린
동일 적용. 시간 열화 사다리 2순위: 예산 초과 시 케이스당 **2개로 축소**하고
로그 기록.

## f. 프레임 (사전 고정)

- **정체 프레임 = PRIMARY**: 폭로 암기가 구조적으로 불가능하므로 정체는 이제
  **오염이 아니라 정보**를 더한다. 실명 노출 원본 페이로드가 1차.
- **익명화 프레임 = secondary**: wave-1 비교 가능성 위해 병기.

## g. 결론 규칙 (사전 커밋)

- **H1**: 홀드아웃 fraud vs 홀드아웃 control 순열 p < 0.05 → **"암기 불가 사건
  위 분석적 탐지"** 주장 허용, 단 **G2-provisional 캐비앳 필수**.
- **H2**: 케이스별 점수를 wave-1 점수 분포와 **나란히**(맥락) 보고 — **pooling
  없음**.
- **H3**: null이거나 게이트 통과 **N < 3**이면 → **주장 STOP**. 로스터·프로브·
  "후보 축적 대기"를 정직하게 발행 — **그 브랜치에서는 그것이 산출물**이다.

## h. 빌드/실행 (P2.1)

EDGAR/XBRL 조회(HUBG·WMK·GNE + 대조군; 컷오프 = 각 폭로일 전일). sec.gov egress
차단 시 **fetch manifest 발행**(claude.ai-side 조회용) — 침묵 실패 금지.
불변 검사 → 채점 + 프로브 + 채점자(human_finalized=**false**, 소유자 확정) →
freeze. 분석(P2.2): 소규모-N exact 순열 · 효과크기 · 티어 라벨 · 이름 예측 프로브
· M/F 기준선(연속성).

---

**불변**: BLINDNESS(정체 프레임은 폭로-후 정보 비접근이 non-recognition
게이트로 보장) · CUTOFF(컷오프=폭로 전일, cutoff_guard 경유) · RESULT
IMMUTABILITY. 이 파일이 홀드아웃 첫 점수보다 먼저 커밋된다. 발행 없음.
</content>
