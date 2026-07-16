# MONTHLY_RITUAL.md — 홀드아웃 성장 루프 월간 의식 (소유자 체크리스트, ~20분)

> 목적: 시간이 흐를수록 N=3 홀드아웃이 저절로 자라게 하는 반복 루프.
> 도구는 전부 존재한다 (`tools/holdout_rescan.py` · `tools/seal_predictions.py` ·
> `docs/FUTURE_CYCLE_PROTOCOL.md`). 이 문서는 실행 순서만 고정한다.
> 실행일: **매월 1일** (놓치면 그 주 안에 — 스캔 구간은 날짜 인자라 늦어도 무손실).

## A. 월간 재조사 (~15분)

1. **사전 점검** (~2분): `git pull` → `git status` 클린 확인. 백그라운드 러너가
   돌고 있으면 종료 후 진행 (repo 쓰기가 대기 중 러너를 죽이는 상호작용 실측).
2. **스캔 실행** (~3분): `make rescan SINCE=<지난 실행일>` (기본 SINCE=2026-02-01).
   - 네트워크 fetch는 실행 시점의 소유자 입회 승인이 전제다 — cron 등 무인
     자동화 금지 (PROJECT.md §5-1, Q-E03 판례: 무감독 fetch는 look-ahead 누출을
     조용히 만든다).
   - **egress 차단 시**: 스크립트가 fetch 매니페스트(질의 URL + 수기 취득 지침)를
     `data/candidates/holdout_rescan/rescan_<enddt>.json`에 출력하고 정상 종료한다.
     매니페스트의 지침대로 브라우저에서 취득해 지정 경로에 저장 후 재실행.
3. **후보 심사** (~7분): 출력 JSON의 신규 4.02/재작성 사건을
   `docs/FUTURE_HOLDOUT_CANDIDATES.md` Tier-2 표에 등재 (제외하는 것도 사유와
   함께 "제외 기록" 절에 — 오염 통제의 절반은 제외 이력).
   - 컷오프 경계 ±수일 사건은 Tier 1 하단 규칙 승계 (훈련 경계 퍼짐).
   - 기존 등재사에 후속 사건(AAER 발행 등)이 있으면 tier 소급 승격
     (G1 AAER > G2 4.02 > G3 SEC complaint > G4 DOJ).
4. **커밋** (~3분): `git add data/candidates docs/FUTURE_HOLDOUT_CANDIDATES.md`
   → 커밋 메시지 `monthly rescan YYYY-MM` → push → CI green 확인.

## B. 분기 봉인 (해당 월에만: 2026-11-15가 첫 봉인 — 이후 분기마다)

1. 봉인 대상 예측 파일 작성 (워치리스트·점수·판정 규칙 — seal 시점에 지표까지
   사전 등록).
2. `python tools/seal_predictions.py <예측 파일>` → 해시 파일 생성.
3. **해시 파일을 본 실행 전에 커밋+push** (커밋 타임스탬프 = 봉인 증거,
   FUTURE_CYCLE_PROTOCOL §1(b)와 동일 원리). 예측 원문은 폭로 후 공개 시
   해시 대조로 검증.
4. 봉인된 이름에 폭로·AAER 발생 시: 개봉 → 예측 대비 실측 비교 → 그 결과가
   전향(prospective) 실적의 1차 데이터다 — 소급 주장 아닌 유일한 실적 축.

## C. 유니버스 모니터 (docs/UNIVERSE_SELECTION.md 서명·열거 이후에만)

- 월간 재조사와 같은 날, 유니버스 12사 중 신규 분기 공시가 나온 회사만 추적
  목록에 표시 (스크리닝 실행 여부·예산은 별도 소유자 결정 — 이 문서는 실행을
  강제하지 않는다).

## 이 의식이 지키는 것

- **암기 불가 tier의 N**: 홀드아웃은 시간이 만든다 — 월 1회 20분이 유일한 비용.
- **전향 실적**: 분기 봉인만이 "사후 규칙" 비판이 원리적으로 불가능한 실적을
  만든다 (D87 EXPLORATORY 결합 규칙의 검증 무대도 여기다 —
  FUTURE_CYCLE_PROTOCOL 부록 A).
- 채점: Claude 보조 + 인간 최종 확정. 본 결과는 Claude 기반 단일 파이프라인에
  한정된다 (PROJECT.md §5-5).
