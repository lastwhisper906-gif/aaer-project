# FUTURE_CYCLE_PROTOCOL.md — Cycle 2 오염 위생 프로토콜 (전방 오염 대응)

> 2026-07-10 기입 (D31, 2차 외부 검토 W7). 이 문서는 **Cycle 2(차기 평가 사이클)
> 개시 전에 반드시 적용할 위생 규칙**을 사전 고정한다. Cycle 1(wave-1/2·홀드아웃)
> 산출물·판정에는 소급 적용하지 않는다 — 발행 동결값 불변.

## 0. 전제: 이 저장소 자체가 오염원이 된다

**이 저장소(공개 ground truth 매핑 포함)가 미래 모델의 학습 데이터에 들어가는
순간, 현재의 케이스 세트·중립 ID(case_NN)·교란 시드는 영구적으로 소각(burned)
된다.** case_NN ↔ 실명 매핑, 교란 상수배, 정답 키, 채점 rationale이 전부 공개
텍스트로 존재하므로, 이후 학습된 모델에게 이 저장소의 케이스는 "암기 불가"
주장이 원리적으로 성립하지 않는다. 이것은 결함이 아니라 공개 벤치마크(G2)의
구조적 수명이다 — 대응은 은닉이 아니라 **사이클마다 소모품을 교체**하는 것이다.

## 1. Cycle 2 위생 규칙 (사전 고정)

### (a) 중립 ID salt 갱신
- Cycle 2의 케이스 ID는 새 salt로 생성한다:
  `case_id = f"c2_{sha256(ticker + CYCLE2_SALT).hexdigest()[:8]}"` 형태.
- `CYCLE2_SALT`는 사이클 개시 커밋에서 생성하되 **값 자체는 §(b) 봉인 대상**
  (salt가 공개되면 매핑 역산이 가능하므로 매핑과 동급으로 취급).
- Cycle 1의 `case_NN` 체계는 재사용 금지 (소각됨, §0).

### (b) ground truth 매핑 봉인 (pre-fixed 증명 유지)
- 케이스 ↔ 실명 매핑·정답 키는 **cycle freeze까지 비공개**(로컬 `~/aaer-data/`
  또는 private 경로) — repo에는 **sha256 해시만 사전 커밋**한다:
  `sha256(canonical_json(mapping))` 1줄. 이것이 "매핑은 채점 전에 고정되어
  있었다"의 공개 증명이며, freeze 후 원문 공개 시 해시 대조로 검증된다.
- 채점·판정 규칙 문서는 지금처럼 공개 사전 커밋 유지 (freeze-commit-then-run
  불변) — 봉인 대상은 **정답에 해당하는 것**만이다.

### (c) 새 모델 핀 채택 전 카나리 GUID 프로브 2회 의무
- 새 피평가자/채점자 모델 핀을 채택하기 전, 저장소에 심어둔 카나리 GUID
  (예: `docs/methodology_limitations.md`의 D9 카나리)를 모델에게 직접 질의하는
  프로브를 **최소 2회** 실행한다.
- 카나리를 재생하면 = 이 저장소가 해당 모델의 학습 데이터에 들어갔다는 실증
  → **Cycle 1 소모품 전량 소각 확정** (§0), Cycle 2는 반드시 새 케이스 세트로.
- 카나리 미재생은 "미유입 증명"이 아니다 (거짓음성 가능) — 방향성 증거로만
  기록한다. 프로브 transcript는 `runs/canary/`에 커밋.

### (d) 평가 tier 재편: rolling holdout이 1차
- **rolling post-cutoff holdout**(월간 재조사로 누적되는 컷오프-후 사건,
  `docs/FUTURE_HOLDOUT_CANDIDATES.md`)을 **1차 평가 tier로 승격**한다 —
  구조적으로 암기 불가한 유일한 tier이므로.
- **wave-1/wave-2는 calibration 데이터로 강등**: 계기 보정(채점 루브릭·프로브
  민감도·기준선 대조)에만 사용하고, 능력 주장(capability claim)의 근거 tier로
  쓰지 않는다.
- 홀드아웃 자격 게이트는 k≥5 (Cycle 1의 k=1 게이트 거짓음성 산술 — 케이스당
  인지 확률 30% 가정 시 3/3 통과 ≈34% — 참조: methodology_limitations
  §Instrument bias directions).

## 2. 적용 시점

- 이 프로토콜은 Cycle 2 개시 결정(소유자)과 함께 발효한다. Cycle 1 잔여 작업
  (E2·E4·E5 wave-2 arm 등 launch-ready 동결분)은 Cycle 1 규약대로 실행한다.
- 변경은 §5-6 이력 공개 조건 하에서만.

## 부록 A — Cycle 2 사전 등록 후보 대장 (등록만 — 발효는 Cycle 2 개시 시)

> 2026-07-16 기입. 이 부록은 Cycle 2 개시 시점에 sealed 사전 등록으로 승격할
> 후보를 **소급 성능 주장 없이** 쌓아두는 대장이다. 여기 등록되었다는 사실은
> 어떤 검증도 아니다.

### A-1. 결합 규칙: B3 게이트(W8 score ≥ 2) AND LLM(score ≥ T)

- **유래**: D87 결정 표 워크스트림의 EXPLORATORY 산출 (`analysis/decision_table.json`,
  사전 등록 `analysis/DECISION_TABLE_PLAN.md` §5). 동결 데이터를 열람한 뒤 구성한
  **사후(post-hoc) 규칙**이므로, Cycle 1 데이터 위의 어떤 수치도 이 규칙의 성능
  근거로 인용할 수 없다 (D87 산출물의 라벨이 그 금지를 명문화).
- **검증 무대 (유일)**: 분기 봉인 전향 예측 (본 문서 §1(b) 해시 봉인 방식,
  첫 봉인 2026-11-15 — `docs/MONTHLY_RITUAL.md` §B). 봉인 시점에 임계 T·판정
  규칙·성공 지표를 sealed 문서 안에 사전 등록하고, 폭로·AAER 발생 후 개봉
  대조한다. 그때부터의 실적만이 이 규칙의 실적이다.
- **상태**: 후보 등록 (소유자 서명 불요 — 등록 자체는 주장이 아님. 봉인 편입
  여부는 seal 작성 시점의 소유자 결정).

### A-2. 기존 등록 질문 포인터

- 설명가능성(explainability) 채점 설계 — OWNER_QUEUE **Q-M04** (등록만 상태
  유지, 설계는 Cycle 2 개시 후).
- 점수 필드 개명(`misstatement_probability` → 서수 명칭) — Q-F04 근거 문서
  `specs/calibration_scope.md`의 Cycle-2 개명 등록.
