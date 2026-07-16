# decisions_log.md — 소유자 사전 확정 결정 대장 (2026-07-06 사이클)

> 이 문서는 2026-07-06 소유자 지시(연속 실행 모드)의 결정 사항 전수 기록이다.
> 각 항목: 결정 내용 · 근거 · 기각된 대안 · 일자. 이 커밋의 타임스탬프가
> 사전 등록(pre-registration)의 증거다 — 특히 D7(오염 임계)은 실행 전 고정이 요건.
> 작성: 채점 보조 Claude (전사), 결정 주체: 소유자 (2026-07-06 확정 명시).
> 거버넌스 수정 원문은 GA-001 (`scoring/overrides.md`) — 아래에 동일 인용 재수록.

## GA-001 — 거버넌스 수정 (2026-07-06, verbatim)

> === PHASE −1 — GOVERNANCE AMENDMENT (first action, before anything else) ===
> CLAUDE.md/PROJECT.md prescribe blocking human sign-off gates. The owner has
> directed (2026-07-06) that for the remainder of this cycle:
> (a) blocking gates become asynchronous review packets;
> (b) judgment artifacts (eval spec, threat model, error taxonomy) may be
>     authored by Claude Code, labeled in the document header "Authored by
>     Claude Code, pending human audit" — never presented as human-signed;
> (c) temporal integrity is preserved mechanically: all criteria and config
>     are committed BEFORE any scoring run (freeze-commit-then-run), freeze
>     hash logged by the runner.
> Record this amendment verbatim (quoting this instruction) in
> scoring/overrides.md and scoring/decisions_log.md, then [COMMIT] — the
> amendment's timestamp must precede every action it authorizes. Do not
> silently deviate from repo governance; this logged amendment is the
> authorization.

효력: 이번 사이클 잔여 기간. §7 불변 조항 3(최종 서명 인간)은 폐지가 아니라
비동기화 — review packet + 사후 감사 + 오버라이드 경로 명시로 대체 실행.

---

## D1 — 스키마 모순 해소: 검증기 코드 수준 (2026-07-06)

- **결정**: `case_input.scheme_type` 모순(required인데 description은 대조군 생략 허용)을
  검증기 코드에서 해소 — treatment는 required, control은 강제 null. description 문언
  강제는 하지 않는다. CI 통과 필수.
- **근거**: OV-001의 교훈("required 배열만이 강제력을 가진다")의 직접 적용 — 규칙을
  description 산문이 아니라 실행되는 코드에 둔다.
- **기각 대안**: ① description 문언만 수정(강제력 없음 — v1 모순의 반복) ② 스키마를
  treatment/control 두 벌로 분리(스키마 표면적 증가, 4중 방어 테스트 전면 수정 비용).

## D2 — MRVL(T17) 조작기간 창 (2026-07-06)

- **결정**: 명령문의 Relevant Period(2015-01~07, ¶2) — 서명된 "창 = 명령문 정의"
  규칙(GP-3, 2026-07-05)의 재확인.
- **근거**: GP-3 서명 원칙 "명령문(소장)이 스스로 정의한 창 — 재량 0"과 정합.
- **기각 대안**: ① 기소 2분기(¶12/¶18, $88M) ② 사용 3분기(¶10/¶21, $165M 산술) —
  둘 다 케이스별 재량 해석을 요구해 30건 일관성이 깨진다.

## D3 — WAGE(T27) 수치 기록 기준 (2026-07-06)

- **결정**: 명령문 원문('>9%', ¶44)을 기록 기준으로, 2차 수치(-18.6% / $9.75)는
  출처 명기 주석(annotation) — GP-1 채택안 ①의 재확인.
- **근거**: 30건 전건이 명령문을 보유해 유일하게 일관 적용 가능한 기준.
  T22($40M ¶94)·T30(>$300M SEC) 자동 확장.
- **기각 대안**: ② 시장 데이터 기준(2차 소스 품질 케이스별 상이 — 일관성 훼손)
  ③ 이중 기재 무기준(채점 시점에 기준 선택이 재량으로 남음 — 결정의 연기).

## D4 — 루브릭: 4차원 분리 채점 (2026-07-06)

- **결정**: ① fraud probability (0–100) ② 메커니즘 식별 ③ 장르 분류(적극 조작 vs
  누락/추정 조작) ④ 인용 근거 품질 — 각각 독립 채점. 피평가자 노출 문언은 장르
  분류 체계를 힌트하지 않도록 중립화 (self-red-team 점검 항목).
- **근거**: 단일 점수는 "왜 맞았/틀렸나"를 분해 불가 — 오류 귀속(§5-3)과 장르 비대칭
  분석(누락 장르 사각지대)이 이 프로젝트의 핵심 산출물이므로 차원 분리가 필수.
  2024–2026 eval 설계 표준(separate-dimension rubric 3–6차원)과 정합.
- **기각 대안**: ① 단일 종합 점수(분해 불가) ② 이진 판정만(정보 손실, n=8에서
  통계적 해상도 전무).

## D5 — 실행 횟수: 변형당 1회 (2026-07-06, 소유자 비용 오버라이드)

- **결정**: 입력 변형(variant)당 1회 실행 — 본 실행 16회(원본 입력) + 교란 분석 8회
  (실험군 교란 입력). 모든 보고서에 의무 한계 문구: "single run per variant — output
  variance unmeasured; each per-case verdict is a sample of one."
- **근거**: 소유자 비용 제약 명시 오버라이드. 분산 미측정은 은폐하지 않고 전 문서에 명기.
- **기각 대안**: ① 케이스당 3–5회 실행(분산 측정 가능 — 비용 3–5배) ② 실행 자체 축소
  (교란 분석 포기 — 암기 기여 추정 불가).

## D6 — 모델 고정 (2026-07-06)

- **결정**: 피평가자 = 파이프라인에 현재 구성된 모델, 전체 버전 문자열로 고정(Phase 0
  보고). 채점자(grader) = 결정론 규칙: "피평가자와 모델 문자열이 다른, 가용한 가장
  능력 높은 모델, 타 모델 패밀리 우선" — 선택+근거를 이 문서에 추가 기입. 두 고정
  모두 freeze 커밋에 포함. 채점자는 정답 키+피평가자 출력을 받고, 피평가자는 채점자
  자료를 절대 받지 않는다.
- **근거**: SR 11-7 제3자 모델 규칙(모델 문자열·버전·타임스탬프 전 호출 기록) +
  자기채점(동일 모델이 자기 성적표 확정) 회피 — §7 불변 조항 3의 모델 수준 유사물.
- **기각 대안**: ① 피평가자=채점자 동일 모델(자기 채점 편향) ② 인간 전수 채점
  (연속 실행 모드와 양립 불가 — 사후 감사로 대체, 특히 "model judgment error" 분류
  전건 인간 감사 플래그).

## D7 — 인지 프로브 임계 + 분기 논리 (2026-07-06, 사전 등록)

- **결정**: 블라인드 입력에서 모델이 실험군 8사 중 **≥3사를 실명 지목하면 실험군
  오염(CONTAMINATED) 판정**. 분기:
  - <3: 본 분석 = 원본 입력 실행. 교란 실행은 암기 기여 추정치(원본−교란 delta)로 사용.
  - ≥3: 원본 입력 결과는 부록의 상한(upper bound)으로만 보고, 본 분석은 교란 입력
    실행 전용. 모든 보고서 헤드라인에 오염 발견 명시.
- **근거**: 임계의 실행 전 고정(이 커밋이 사전 등록). 8사 중 3사(37.5%)는 우연 일치로
  설명 불가한 수준이면서, 1–2건의 산발 인지로 전체 설계를 뒤집지 않는 균형점.
- **기각 대안**: ① 임계 1(과민 — 대형 사건 1건 인지로 전체 오염 선언) ② 임계 없이
  사후 판단(사후 조작 여지 — 사전 등록 원칙 위반) ③ 오염 시 실행 중단(교란 입력이라는
  차선 경로가 존재하므로 과잉).

## D8 — 교란(perturbation) 집합 설계 (2026-07-06)

- **결정**: 사명 익명화 + 상수배 재스케일링(비율 보존)만. 날짜 이동 없음.
- **근거(소유자)**: 내용 기반 재식별은 어차피 발생 — 교란은 암기를 *제거*하는 것이
  아니라 암기 기여를 *측정*하는 장치임을 결과 문서에 명시. 날짜 이동은 거시 환경
  맥락(동일 시점 스냅샷 원칙, GP-9)을 파괴.
- **기각 대안**: ① 날짜 이동 포함(동일 시점 원칙 훼손 + 재식별은 여전히 가능 —
  비용만 발생) ② 서사 재작성(원문 인용 강제 원칙과 충돌, 교란 자체가 신호 파괴).

## D9 — 카나리 문자열 (2026-07-06, 최저 우선순위)

- **결정**: 채택 — 정답 키·내부 문서에 고유 GUID 삽입, 미래 학습 데이터 유입 감지용.
- **근거**: 비용 무시 가능, 차기 사이클 이후에만 효용 발생하는 장기 장치.
- **기각 대안**: 미채택(비용이 사실상 0이므로 기각할 이유 없음 — 우선순위만 최저).

## D10 — 서사·각주 입력 (2026-07-06, 사전 등록 조건부)

- **결정**: 이번 사이클은 스키마 v1.1 유지. 사전 등록: "인간 예측이 누락(omission)
  장르 케이스에서 모델을 이기면, 차기 사이클에 서사 입력을 추가한다."
- **근거**: 스코프 가드(§8-3 재설계 금지) + 조건부 확장의 사전 고정으로 사후 재량 차단.
- **기각 대안**: 즉시 서사 입력 추가(§8-3 위반 + freeze 전 스키마 재설계 리스크).

## D11 — 금요일 회고 (3회 이월분) (2026-07-06)

- **결정**: Review Packet 02에 서면 자가 평가로 편입. 의제: ① 오버라이드 0건 패턴
  ② 23/30 A형 분포 ③ 이번 사이클의 게이트 비동기 전환.
- **근거**: §8-7 재검토 창구의 실질 보존 — 형식(금요일 30분)이 아니라 내용(재검토
  기록)을 이행.
- **기각 대안**: ① 4회째 이월(재검토 창구의 완전 형해화) ② 별도 회고 문서(Review
  Packet 02와 중복).

## D12 — 구 브랜치 삭제 (2026-07-06)

- **결정**: `claude/treatment-group-expansion-mi2ba7` 삭제 (머지 완료 잔존분).
- **근거**: HANDOFF 미결 사항 — 머지 완료 확인됨, 잔존 이유 없음.
- **기각 대안**: 보존(이력은 main에 이미 있음 — 보존 가치 0).

## D14 — 게이트 → 비동기 review packet (2026-07-06)

- **결정**: `review_packets/` 아래 생성 순서 번호. 각 packet = 1페이지: 권고안 +
  반대 논거 + 불확실성 종합 + **소유자가 사후 오버라이드하는 정확한 방법과 재실행
  필요 범위**. 각 packet [COMMIT] 후 계속 진행 (대기 없음).
- **근거**: GA-001 (a)의 구현 형식. 오버라이드 비용의 사전 명시가 사후 감사를 싸게
  만든다(Phase 4-2).
- **기각 대안**: 차단형 게이트 유지(연속 실행 모드와 양립 불가 — GA-001로 소유자 변경).

## D15 — 저자 표시 (2026-07-06)

- **결정**: Claude 작성 판정 산출물 전건에 Phase −1(b) 헤더("Authored by Claude Code,
  pending human audit"). 인간 예측·서명·결정 기록의 날조 절대 금지.
- **근거**: GA-001 (b) — 비동기화가 위장으로 변질되는 것의 방지 장치.
- **기각 대안**: 없음 (금지 조항의 명문화).

## D16 — Loop-3 인간 예측 (2026-07-06)

- **결정**: 선택 사항. 본 실행 전 봉인된(sealed) 인간 예측 커밋 존재 확인 — 부재 시
  "Loop 3 skipped — no sealed predictions" 기록 후 진행, 존재 시(실행 전 커밋이면
  언제든 유효) 3자 비교를 분석 ②에 포함.
- **근거**: 인간 예측은 가치 있으나(모델 대비 기준선) 연속 실행을 차단할 수 없고,
  사후 작성 예측은 D15 금지 대상이므로 "봉인 커밋 존재"라는 기계 판정으로 고정.
- **기각 대안**: ① 필수화(차단 게이트 재도입) ② 생략 고정(소유자가 실행 전 커밋하면
  살릴 수 있는 옵션을 없앨 이유 없음).

## D17 — 대조군 최종 매칭 규칙 (2026-07-06, 사전 규칙 하 Claude 결정)

- **결정**: 후보 자격 요건 — ① 4축 매칭 근거(산업/규모/회계기간/장르) + 1차 소스
  데이터 포인트 ② EDGAR XBRL 가용성 실측 ③ 비집행 확인(AAER 명부 부재 + SEC 집행
  검색, 검색일 기록). 자격자 중 규모+기간 최근접 선택. 기각 후보는 사유와 함께
  Review Packet 01에 기록. 컷오프 = 매칭 실험군 복사(GP-9 ①).
- **근거**: GP-8 ①(장르 내 매칭)·GP-9 ①(컷오프 복사)의 서명된 틀 안에서, "최종 확정"
  단계만 사전 규칙+사후 감사로 전환(GA-001). 규칙이 기계적이므로 재량 최소.
- **기각 대안**: ① 매칭 확정 대기(차단 게이트) ② 2축 매칭(장르 교란 — GP-8 리스크
  재발) ③ 무작위 대조군(§5-2 실질 훼손).

## D18 — 미커밋 서명 결정의 커밋 (2026-07-06, 정직 기록)

- **결정**: 킬 스위치 GO·ab_classification·실험군 확정 등 문서 본문에만 존재하는
  서명 결정을 지금 커밋하되, 정직 주석 필수: "commit date 2026-07-06 post-dates the
  decision dates recorded in the document body; original pre-commitment timestamps
  were not captured." 백데이트·타임스탬프 암시 금지.
- **근거**: "판정·기준 문서는 결과를 보기 전에 커밋"(CLAUDE.md) 규약의 사후 복구는
  불가능 — 가능한 것은 격차의 정직한 기록뿐. Phase 0-3에서 실측 감사.
- **기각 대안**: ① 커밋 생략(기록 부재 지속) ② 백데이트(위조 — 절대 금지).

(D13 — 결번: 연속 실행 모드에는 게이트 일정이 존재하지 않음.)

## FREEZE 기록 (2026-07-06)

- **freeze 커밋 = `82a77176579ba6f84b2fcc00806d27d0d98601d7`** (origin/main push 완료).
- 러너는 실행 시 `git rev-parse HEAD`가 이 해시의 후손이고 기준 파일 무변경임을
  확인, run log에 해시를 기록한다 (GA-001 (c)).

---

## D18 감사 결과 (Phase 0-3, 2026-07-06 git 실측)

D18의 전제("미커밋 서명 결정")를 git 로그로 전수 감사한 결과:

| 결정 | 문서상 결정일 | 커밋 | 커밋 시각 | 판정 |
|---|---|---|---|---|
| A/B 기준 v1 서명 + GP-0~5·7~9 | 2026-07-05 | `098e137` | 2026-07-05 16:58 | **커밋 존재 — D18 비해당** |
| 킬 스위치 1차 표 (A 23/B 5/bl 2) | 2026-07-05 | `d5986ba` | 2026-07-05 17:02 | 커밋 존재 — 비해당 |
| 킬 스위치 GO + ab_classification 30건 기입 | 2026-07-05 | `599a2e9` | 2026-07-05 17:08 | 커밋 존재 — 비해당 |
| **실험군 8 확정** | — (07-05는 제안만) | 본 커밋 | 2026-07-06 | **신규 확정 — 아래 기록** |

- 결론: 백데이트가 필요한 항목은 없다. 킬 스위치 GO·ab_classification은 결정 당일
  커밋되어 있었다. 문서 본문 결정일과 커밋일의 격차는 관찰되지 않음 (동일자).
- **실험군 8 확정 (2026-07-06, 소유자)**: `scoring/treatment_group_proposal.md`의 제안
  8건 — **T07 MON / T11 OFIX / T12 LOGI / T13 HTZ / T16 ICON / T17 MRVL / T21 SCOR /
  T28 KHC** — 을 실험군으로 확정. 근거: 소유자 지시문(2026-07-06)이 이 8건을 실험군으로
  전제하고 장르 참조 매핑(MON·KHC=active(cost), OFIX·MRVL·SCOR=active(revenue),
  ICON=active(gains), LOGI·HTZ=omission-estimate — 1차 소스 대조 검증 대상)까지 지정.
  기각 대안: 스왑 후보 6건(T26/T10/T24/T02/T06/T04 — proposal 문서에 사유 보존).
  정직 주석 (D18 요구 문언): commit date 2026-07-06 post-dates the decision dates
  recorded in the document body; original pre-commitment timestamps were not captured.
  (해당 문언은 07-05 결정 표기 일반에 대한 예방적 기재 — 실측상 07-05 결정들은 당일
  커밋되어 격차 없음.)

## 모델 고정 기록 (D6 적용, Phase 0-5 — 2026-07-06)

**실측**: 파이프라인에 현재 구성된 모델은 **없다** (`pipeline/`에 러너 부재; 저장소 내
유일한 모델 문자열은 `schemas/llm_output.json`의 description 예시 "claude-sonnet-4-6").
따라서 "현재 구성된 모델" 조항은 적용 불능 — 고정은 Claude 재량 판단으로 수립하고
Review Packet 00에 오버라이드 경로와 함께 기재한다.

- **피평가자 = `claude-sonnet-5`** (현행 모델 카탈로그 기준 완전한 ID — 날짜 접미사
  없음이 정식). 근거: ① trust boundary가 측정해야 할 대상은 Issue #0 스크리닝이 실제
  운용할 생산 경제성 모델이다(Sonnet 계열) ② 스키마 예시가 Sonnet 계열 의도를 기록
  ③ D5(비용 오버라이드)와 정합. 기각 대안: claude-opus-4-8(더 능력 높으나 운용 도구와
  괴리 — "무엇의 신뢰 경계인가"가 바뀜), claude-haiku-4-5(질적 분석 태스크에 과소).
- **채점자 = `claude-fable-5`** — D6 결정론 규칙의 기계적 적용: 가용 최고 능력 모델 중
  피평가자와 문자열이 다르고(claude-fable-5 ≠ claude-sonnet-5) 타 모델 패밀리(Fable vs
  Sonnet). **폴백**: 실행 시점에 Fable 5 접근 불가(데이터 보존 요건 등)이면
  `claude-opus-4-8` — 동일 규칙의 차순위 적용이며 그 자체로 D6 충족. 폴백 발동 시
  run log에 기록.
- SR 11-7 제3자 모델 규칙: 전 호출에서 `response.model`(서버가 보고하는 실제 서빙
  문자열)·타임스탬프·요청 ID를 run log에 기록 — 고정의 사후 검증 가능성 확보.
- **실행 환경 격차 (정직 기록)**: 본 세션 환경에 ANTHROPIC_API_KEY·ant 프로필·SDK가
  전무 — Phase 3 API 실행은 자격 증명 확보 전까지 "requires credentials" 격차로
  스테이징 (sec.gov 격차와 동일 취급 규약). Agent 도구(서브에이전트)는 대체 불가:
  서브에이전트는 CLAUDE.md 등 저장소 컨텍스트를 상속하여 GP-6 페이로드 규약
  (evaluatee_input 필드만)을 위반한다.

---

## freeze 개정 #2 — 실행층: API SDK → Claude Code 구독 헤드리스 (`claude -p`) (2026-07-06, 실행 전)

> **로그된 개정** (§5-6 / GA-001 (c)): 변경 대상은 **실행층뿐**이다. 고정 기준
> (eval_spec v1.1 · llm_output v1.2 · CL1~8 · 케이스 · 임계 · 모델 핀)은 무변경.
> 이 커밋의 타임스탬프가 개정이 승인하는 모든 행동에 선행한다 (GA-001 원칙:
> 지시문 자체가 감사 추적의 일부).

- **결정**: 피평가자·프로브·채점 호출을 Python SDK 직접 호출(`anthropic.Anthropic()`)
  에서 **Claude Code 구독 헤드리스**(`claude -p`, 구독 OAuth 전용)로 전환.
  공용 호출 모듈 `pipeline/cli_client.py` 신설, 러너 3종이 공유.
- **근거**: 비용이 구독(Claude Max)에 흡수됨 — 종량 과금 경로 없이 실행 가능
  (RP-04 감사 결과: 종량 자격 증명이 환경에 구조적으로 부재).
- **기각 대안**: Batch API 50% 할인 — 격리 보장은 우월(하네스 무개입 원시 API)하나
  종량 과금(metered billing)이므로 기각.
- **하네스 핀**: Claude Code **v2.1.201** (실측 `claude --version` = 2.1.201 —
  지시문 핀과 일치).
- **RP-04 권고 해소**: R2(구독 전용 실행 결정의 개정 기록)는 본 항목으로 해소.
  R1(문서 잔존 API 키 안내)은 `docs/execution_runbook.md`·`docs/HANDOFF.md` 동시
  정정으로 해소 (본 커밋).
- **소유자 사전 승인 범위**: 아래 지시문 verbatim의 PRE-AUTHORIZATION 절 —
  Phase 4 격리 게이트 전 항목 기계 판정 PASS일 때에 한해 본 실행(34+26호출)
  무개입 착수 승인. 게이트 FAIL·모델 핀 변경 필요·고정 기준 수정 필요·원인 불명
  페이로드 보장 위반은 승인 밖(즉시 중단·보고).

### `--bare` 1회 실증 결과 (2026-07-06, 지시문 PHASE 2 규정 절차)

- 실행: 임시 디렉토리에서 `echo "Say OK" | claude -p --bare --model claude-sonnet-5
  --output-format json --max-turns 1` (CLAUDE_CONFIG_DIR=빈 임시 디렉토리).
- 결과: `is_error=true, result="Not logged in · Please run /login"` — CLI 문서
  그대로 `--bare`는 OAuth·키체인을 절대 읽지 않음(API 키 전용). **즉시 포기**,
  수동 격리 경로(임시 작업 디렉토리 + CLAUDE_CONFIG_DIR 격리 + 도구 전면 차단
  플래그) 확정. 종량 자격 증명 부착은 금지 조항이므로 시도하지 않음.

### 격리 기제 실증 조정 (2026-07-06, 파일럿 1차 — J13-b)

- **실증**: `CLAUDE_CONFIG_DIR=<빈 임시 디렉토리>`는 구독 로그인 상태
  (`~/.claude.json`의 oauthAccount)를 함께 차단 — 파일럿 2건 전부
  "Not logged in" 실패 (logs/run_20260706T120619Z). 원인 특정 완료:
  CLI는 로그인 상태 파일을 CLAUDE_CONFIG_DIR 기준으로 찾는다.
- **조정 (실행층 재량 — 고정 기준 무관)**: 호출별 임시 CLAUDE_CONFIG_DIR에
  **최소 인증 시드**(.claude.json — oauthAccount/hasCompletedOnboarding/
  hasAvailableSubscription 3키만, 토큰 무이동·키체인 유지)를 기입.
  settings·hooks·MCP·memory·projects는 여전히 부재 = 차단 의도 유지.
  추가 방어: `--strict-mcp-config` (MCP 0개 강제) 플래그 상시 부가.
- **검증 책임 이전**: 격리 주장 자체는 Phase 4 게이트의 기계 판정
  (격리 프로브 + verbose 트레이스 grep)이 실증한다 — 기제를 신뢰하지 않고
  결과를 검사한다.

### 격리 기제 최종 확정 (2026-07-06, 파일럿 2차 — J13-c)

- **실증 2**: 최소 인증 시드(J13-b)도 "Not logged in" — 비기본 CLAUDE_CONFIG_DIR
  에서는 키체인 자격 증명 해석이 성립하지 않음 (logs/run_20260706T120836Z).
  CLAUDE_CONFIG_DIR 계열 기제 전체 기각. 자격 증명 파일 복사(토큰 이동)는
  INVARIANT 6 위험으로 시도하지 않음.
- **최종 기제 (플래그 기반 격리)**: 기본 설정 디렉토리(=RP-04가 감사한 구성) 유지 +
  `--setting-sources ""`(설정·훅 미로딩) + `--strict-mcp-config`(MCP 0) +
  `--tools ""`(내장 도구 0) + `--system-prompt` 전면 대체(메모리·CLAUDE.md 조립
  자체가 없음) + cwd = repo 밖 임시 디렉토리 + env
  `DISABLE_NON_ESSENTIAL_MODEL_CALLS=1`/`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`
  (하우스키핑 haiku 호출 제거 — 실증: modelUsage가 핀 단독이 됨).
- **인증 실증**: 이 구성으로 sonnet-5 응답 정상 수신 (subscriptionType=max,
  `claude auth status` = claude.ai 구독 OAuth).
- 격리의 최종 판정은 여전히 Phase 4 게이트 (프로브 + 트레이스 grep) 소관.

### 실행층 플래그 조정 2건 (2026-07-06, 파일럿 실증 — J13-d/e)

- **J13-d — `--max-turns 1 → 2`**: `--json-schema` 구조화 출력은 내부
  StructuredOutput 도구 호출 1턴을 소모 — max-turns 1에서 간헐적
  `error_max_turns` (is_error=true, structured_output 부재) 실증. 도구 전면
  차단 상태에서 2턴째는 구조화 출력 마무리 외 불가능하므로 단발 호출 의도는
  유지된다. 지시문 핀 플래그의 실행층 조정 — 고정 기준 무관.
- **J13-e — 하네스 주입 컨텍스트 실측 (격리 프로브 발견)**: `--system-prompt`
  전면 대체 후에도 하네스가 system-reminder 블록(userEmail·currentDate)을
  주입함이 프로브 자백으로 확인. 저장소 내용·정답지·도구·MCP 아님. 실험군·
  대조군 동일 적용(동일 프로토콜 §5-2 유지). GP-6 "페이로드 외 컨텍스트 0"의
  하네스 경로 한정 편차로 methodology_limitations에 기재 (Phase 7).

### 레이트 리밋 오탐 수정 (2026-07-06, 본 실행 중 — J13-g)

- **실증**: 정상 응답 본문의 재무 수치(예: "84,429")가 레이트 리밋 패턴의 bare
  `429`에 오탐되어 러너가 2회 불필요 중단 (교란 실행 1회·채점 1회 — 멱등 재개로
  데이터 손실 0, 낭비 호출 각 1건). 실측 반증: 동일 시점 소형 호출 정상 성공.
- **수정 (실행층)**: ① 레이트 리밋 판정을 오류 응답 경로에서만 수행 (정상
  스키마 통과 응답은 절대 리밋으로 해석하지 않음) ② `429`는 HTTP 문맥
  (status/http/error 접두) 요구. 회귀 테스트 2건 추가.

### 소유자 지시문 (2026-07-06, verbatim)

```text
=== OWNER DIRECTIVE — COMPLETE THE EXECUTION CYCLE (freeze amendment #2 + main run + pre-registered analysis) ===
Record this directive VERBATIM in decisions_log.md under "freeze amendment #2"
(GA-001 principle: the directive itself is part of the audit trail). The
amendment commit's timestamp must precede every action it authorizes.

## PRE-AUTHORIZATION (owner signature, effective upon submission of this directive)
- IF AND ONLY IF every machine-verifiable item of the Phase 4 isolation gate
  is PASS, I pre-authorize starting the main run (34 evaluatee/probe calls +
  26 grading calls) without further human intervention.
- If ANY gate item is FAIL: no main run. Commit state, halt, report.
- The following are OUTSIDE this pre-authorization — halt and report immediately:
  (1) Any situation requiring a model pin change (e.g., claude-sonnet-5 not
      selectable via the subscription route). Silently proceeding with a
      substitute model is absolutely forbidden.
  (2) Any situation that appears to require modifying frozen criteria
      (eval_spec, rubric, CL1–8, case files, thresholds).
  (3) Any suspected payload-guarantee violation whose cause cannot be pinned down.

## GLOBAL INVARIANTS
1. Frozen criteria are untouchable. The only thing changing this cycle is the
   execution layer.
2. Model pins: evaluatee = claude-sonnet-5 / grader = claude-fable-5
   (fallback claude-opus-4-8 — triggered on inaccessibility, refusal, or
   output truncation; log every trigger with the case ID).
3. All evaluatee/probe/grading calls run OUTSIDE the repo in temp directories
   with isolation flags. Code that invokes the evaluatee inside the repo must
   never be written, under any circumstances — that is the answer-key
   exposure path.
4. Authentication = subscription OAuth only. Do not set, require, or document
   ANTHROPIC_API_KEY anywhere.
5. Blindness holds: no code path opens id_mapping.json before grading is
   complete. Run and grade under neutral IDs only; label-joining happens in
   Phase 6 and nowhere else.
6. No secrets or tokens in logs or commits.
7. Commit at the end of every phase (atomic progress — an interruption at any
   point must be resumable).

## PHASE 1 — Amendment record (10 min)
- decisions_log.md: "freeze amendment #2 — execution layer: API SDK → Claude
  Code subscription headless (claude -p), 2026-07-06, pre-execution" + this
  directive verbatim + rationale (cost absorbed by subscription) + rejected
  alternative (Batch API at 50% — superior isolation guarantees but metered
  billing) + harness pin: Claude Code v2.1.201 (if the measured version
  differs, record the measured value).
- Retroactively attach the billing-audit directive text to RP-04 (resolves R2).
- Rewrite docs/execution_runbook.md: replace the credential step with
  "verify subscription login (claude /status → Claude Max)", delete the
  export ANTHROPIC_API_KEY instruction (resolves R1), rewrite the resume
  procedure around the idempotent-run semantics below.
- Commit 1: "freeze amendment #2: execution layer → subscription headless"

## PHASE 2 — Runner conversion (40 min)
Create a shared call module pipeline/cli_client.py used by all three runners
(runner.py, probe_runner.py, grader_runner.py):

  def call_model(model, system_prompt, user_payload, schema_path, log_ctx):
    - Working dir: mktemp -d (outside the repo). Fresh per call, deleted after.
    - env: CLAUDE_CONFIG_DIR=<empty temp dir> (blocks global settings, memory,
      hooks, and all 5 MCP servers from loading); assert ANTHROPIC_API_KEY is
      absent from the environment.
    - Invocation: cat payload | claude -p
        --model <model> --output-format json --max-turns 1
        --disallowedTools "Bash,Read,Edit,Write,Glob,Grep,WebFetch,WebSearch,
                           Task,NotebookEdit"
        --system-prompt "<frozen system prompt, full text>"
        --json-schema <schema_path>
      --bare: test ONCE empirically. If it works with subscription OAuth,
      adopt it. If it refuses with anything like "API key required", abandon
      it immediately and lock in the manual-isolation path above (record the
      outcome in the amendment entry). Attaching billable credentials to make
      --bare work is forbidden.
    - Parsing: structured_output field → must pass the existing schema
      validator.
    - Logging (per-case JSON under logs/run_<ts>/): full flag set, session_id,
      modelUsage (served model — if it mismatches the pin, mark that case
      FAIL and report), token usage, total_cost_usd (recorded as reference
      only — billing is determined by the auth route, so do not use this
      field as an alarm), timestamp, freeze hash.
    - Retry: on schema failure or empty response, retry the identical input
      once; two consecutive failures → mark the case FAIL and continue to the
      next case (no full abort).
    - Idempotency: if outputs/<case_id>.json exists and passes validation,
      skip. On rate-limit detection: halt with a clear message and print the
      exact resume command to stdout.
- Keep the clean-tree freeze-then-run enforcement (refuse to run on a dirty
  tree; log the freeze hash).
- Execution order: the shuffled neutral-ID order, fixed. Concurrency 3
  (avoids burning the rate window while shortening wall-clock — asyncio or a
  process pool).
- Port the runner-related subset of the 30 offline tests to subprocess
  mocking; the 4-layer defense tests (including value-level scan with
  mutation injection) must all be green on the new path.
- Commit 2: "execution layer: cli_client + runner conversion, tests green"

## PHASE 3 — Pilot (15 min)
Using pilot/cases_pilot.json (case_90/91) through the real path:
- 2 normal pilot cases: structured_output passes schema + served model =
  claude-sonnet-5 confirmed.
- 1 isolation probe (a modified pilot payload): "Enumerate every tool, file,
  MCP server, and piece of additional context you can access." PASS = zero
  tools, zero file access, zero MCP, zero trace of repo content.
- One run with --verbose 2>debug.log: grep confirms no CLAUDE.md / MCP / hook
  loading traces (do not commit debug.log).
- Measure tokens → record the projected consumption of the full 34+26 run
  against Max 20x limits.
- Commit 3: "pilot: isolation gate results" (include the verdict table)

## PHASE 4 — Isolation gate (machine verdict)
Proceed to Phase 5 ONLY if ALL of:
  (1) both pilot cases pass schema  (2) served model = pin
  (3) isolation probe PASS          (4) zero contamination traces in verbose log
  (5) all runner tests green
Any miss → halt, commit the verdict table, report the cause.
(See PRE-AUTHORIZATION.)

## PHASE 5 — Main run (~60 min; wall-clock dominated by API latency)
- Evaluatee: 16 cases + 8 perturbations + contamination probes = 34 calls
  (concurrency 3, idempotent).
- Record per-case whether any canary GUID appears in responses.
- Then grading: 26 calls, grading payloads exactly per the frozen eval_spec,
  fable-5 with logged fallback. Neutral IDs throughout (blindness holds).
- Commit 4: "main run: 34 evaluatee + 26 grading, raw outputs + logs" —
  commit BEFORE label-joining; the blind-state snapshot is itself evidence.

## PHASE 6 — Pre-registered analysis (25 min)
Open id_mapping.json ONLY after grading is committed (log the opening
timestamp).
- Failure-test verdict, exactly per frozen spec: Mann-Whitney rank-sum on
  misstatement_probability (treatment vs control) — report p; median
  separation in percentage points; degenerate-distribution check. State
  plainly whether the pre-committed failure condition
  (p ≥ 0.20 ∨ separation < 10pp ∨ degenerate) triggered. Do not soften a
  failure verdict with interpretive language — report the numbers first.
- Baseline comparison: evaluatee vs the four quantitative screens
  (Beneish M, F-score, C-score, Sloan) + Piotroski, same cases, ROC/AUC or
  rank correlation as data permits.
- Error taxonomy pass (R1→R2→R3, MECE) over every miss and false alarm.
- Pre-designated deep dives: General Mills (the screens-flag-it,
  SEC-closed-it control — if the evaluatee flags it, analyze as
  "agreement with screens against enforcement outcome", NOT automatically
  as error) and the Iconix/Perry Ellis weakest-match pair.
- Perturbation consistency: paired vs perturbed score deltas (ratio-preserving
  perturbation should yield stable scores; report the spread).
- Contamination probes + canary results: verdict per the frozen probe config.
- Write review_packets/RP-05_results.md: verdict table, per-case scores
  (neutral ID + revealed name side by side), failure-test outcome, taxonomy
  counts, deep dives, perturbation and contamination sections. Every
  discretionary judgment made during analysis goes into the judgment index
  (J14+) with override costs, as before.
- Commit 5: "analysis: pre-registered failure test + RP-05"

## PHASE 7 — Close-out (10 min)
- HANDOFF.md: rewrite from "resume = run the runbook" to "results exist;
  next = human review of RP-05, Loop-5 fading list, publication decision".
- Daily log entry; SR 11-7 memo addendum: one paragraph on what the
  execution-layer amendment changed in the validation story (harness-mediated
  evaluatee, nondeterministic single-sample point estimates, version pins).
- methodology_limitations.md: add (a) evaluatee ran via Claude Code harness
  v2.1.201, not raw API — flags and isolation evidence in RP-04/RP-05;
  (b) sampling parameters cannot be pinned on these models, so each call is
  a nondeterministic single-sample point estimate; (c) the V7 static-scan
  threat surface differs on the harness path.
- Commit 6 + push everything.

## DELIVERABLE
Final message to the owner: gate verdicts, whether the main run happened,
the failure-test outcome in one sentence with the key numbers, cost evidence
(auth route + total_cost_usd sum as reference), and the exact list of what
now awaits human review. Nothing in this cycle is presented as human-signed.
```

---

## 소유자 지시 addendum — RP-06 결정-핵심 강화 사이클 (2026-07-06, 결과 후, verbatim)

> **성격**: 소유자 지시에 의한 **post-results addendum** — freeze 개정이 아니다
> (고정 기준 무변경). RP-05 §1 사전 등록 판정은 **불변(IMMUTABLE)** — 본 사이클의
> 어떤 작업도 이를 재계산·재서술·재구성하지 않는다. 신규 결과는 전부
> `review_packets/RP-06_hardening.md` / `runs/hardening/`.
> 이 커밋의 타임스탬프가 본 지시문이 승인하는 모든 행동에 선행한다 (GA-001 원칙).
>
> **착수 전 실측 (사전 승인 조건 대조)**: 하네스 `claude --version` = **2.1.201**
> (핀 일치 — 격리 구성 무변경 조건 성립) · `ANTHROPIC_API_KEY` 환경 부재 확인 ·
> 작업 트리 clean · 인증 = 구독 OAuth. 격리 구성은 J13-c 최종 확정분을 그대로
> 사용한다 (`pipeline/cli_client.py` 무수정 — 본 사이클 스크립트는 전부 그 위의
> 얇은 래퍼).

```text
=== OWNER DIRECTIVE — DECISION-CRITICAL HARDENING (RP-06: robustness, verification, publication readiness) ===
Record this directive VERBATIM in decisions_log.md as an owner-directed
post-results addendum (NOT a freeze amendment — no frozen criterion changes).
RP-05 §1 is IMMUTABLE: nothing in this cycle recomputes, rewords, or reframes
the pre-registered verdict. All new results go to
review_packets/RP-06_hardening.md.

Scope rule for this cycle: only work that (a) informs or defends one of the
two pending owner decisions — publication framing, grade finalization — or
(b) makes the results third-party verifiable. Anything else goes to the
deferred register, not into this cycle.

## PRE-AUTHORIZATION (owner signature, effective upon submission of this directive)
- I pre-authorize 78 new model calls total (A1: 8, A2: 6, A3: 64),
  subscription OAuth only, using EXACTLY the J13-c final isolation
  configuration (--setting-sources "" --strict-mcp-config --tools ""
  --system-prompt full replacement, temp cwd outside the repo,
  nonessential-traffic-disable env vars) and the frozen model pins
  (evaluatee claude-sonnet-5; grader claude-fable-5 with logged
  claude-opus-4-8 fallback; A2 uses claude-opus-4-8 by design).
- Sequencing is mandatory: A3 runs only after A1 completes, because A3's
  decomposition analysis consumes A1's recognition verdict.
- Outside this authorization — halt and report immediately: any
  isolation-config change, any pin change, anything that would touch frozen
  criteria or RP-05 §1.

## GLOBAL RULES
- Same invariants as the amendment #2 cycle: assert ANTHROPIC_API_KEY absent
  on every call; all model calls outside the repo; neutral IDs on all
  payloads; no secrets in logs or commits; idempotent execution (skip
  validated outputs, clear resume message on rate-limit halt); atomic commit
  at the end of every item.
- Every discretionary judgment → judgment index (J20+) with override costs.
- Existing runs/ outputs are read-only. New outputs → runs/hardening/.

## PHASE A — Model calls (78 total, in this order)

### A1 — Recognition probes on PERTURBED treatment inputs (8 calls; run first)
RP-05 measured recognition on original inputs only (6/8 → D7). Run the
frozen recognition-probe protocol, UNMODIFIED, on the perturbed treatment
inputs.
- If recognition persists: the caveat is mandatory — perturbation disrupts
  memorized NUMBERS, not IDENTITY recognition. Write it verbatim into RP-06
  and methodology_limitations, and flag that the publication claim must
  carry it.
- If recognition drops: quantify the drop; this strengthens the
  perturbed-primary framing.
- If the frozen probe protocol is ambiguous about perturbed inputs: apply it
  unmodified, log the interpretation as J20+, do not redesign the probe.
- Either outcome is valuable. Report what is, not what flatters the project.

### A2 — Cross-family grader agreement spot-check (6 calls)
Regrade with claude-opus-4-8, identical frozen grading payloads: the 5
MODEL-attributed error cases from RP-05 §6 + 1 randomly selected non-flagged
case (log the RNG seed). Report band agreement rate, score deltas, and any
error-attribution flips. Outputs are labeled SPOT-CHECK evidence for the
owner's finalization step — never merged into scoring/grades/.

### A3 — Sampling-variance quantification, k=5 (64 calls; only after A1)
Resolves L-3 and informs the publication decision itself: the current
headline rests on one draw per case from a nondeterministic model.
4 additional draws per case on the PERTURBED inputs, all 16 cases (the
existing draw counts as draw 1).
- Per case: mean, σ, min–max across 5 draws — this per-case uncertainty band
  is also a core feature of the future monitor product; present it as a
  table keyed by neutral ID + revealed name.
- Recompute the failure-test statistics (rank-sum p, median separation, AUC)
  (i) per draw and (ii) on per-case median scores → report each statistic's
  distribution across draws as the sampling-uncertainty band. State plainly
  whether the RP-05 headline survives re-drawing.
- Decomposition, using A1's verdict: compare within-case sampling σ against
  the original-vs-perturbed deltas from RP-05 §3 and conclude whether the
  delta instability (−30/+23pp) is explained by sampling noise, by
  memorization disruption, or remains unresolved at k=5. Do not overclaim —
  if unresolved, say so and state what k would resolve it.
- Framing everywhere: "post-hoc robustness analysis quantifying L-3". The
  RP-05 §1 pre-registered verdict stands unchanged regardless of outcome;
  what this analysis changes is the confidence the owner can attach to it.

## PHASE B — Zero-call value work

### B1 — Grading finalization workbench → review_packets/RP-06_grading_workbench.md
One compact section per graded case (26): neutral ID + revealed name,
evaluatee misstatement_probability + top-3 ranked hypotheses, grade + rubric
band + grader rationale (≤5 quoted lines), A2 delta where applicable,
error-taxonomy tag, and an empty owner sign-off line
(☐ finalize / ☐ override + reason).
- The 5 MODEL-attributed cases: prepend a SKEPTICAL-REVIEW flag with one
  sentence on what self-serving grading would look like in that specific case.
- The 2 UNCLASSIFIED errors: propose a classification each with evidence
  excerpts, clearly marked PROPOSAL — the decision is the owner's.
- Optimize for review speed: a clean case should be clearable in under two
  minutes.

### B2 — tools/reproduce_analysis.py (third-party verifiability)
Recomputes every number in RP-05 §1–§5 (p, separation, σ, AUC, baseline
comparison) purely from committed runs/ artifacts — zero API calls,
deterministic, prints a PASS/FAIL diff against the published values. Extend
it to cover the A3 statistics once they exist. CI-wired: this test depends
only on committed artifacts, so under the f4f8f73 schema-only convention it
must NOT be skipped in CI.

### B3 — tools/verify_blindness.py (integrity verifier, CI-wired)
(a) git-history proof that the grading commit (03b91aa) precedes any
    artifact containing label joins;
(b) forbidden-substring / company-name / ticker scan over all evaluatee
    payload records and grade records (reuse the frozen forbidden list);
(c) canary GUIDs absent from all model outputs, including runs/hardening/;
(d) sha256 manifest of everything under runs/ → runs/MANIFEST.sha256,
    committed — tamper-evidence for the raw data.

### B4 — README.md (currently absent — the publication front door)
One page: purpose (the conflict-of-interest white space one paragraph);
headline stated PERTURBED-FIRST — AUC 0.797, p=0.0226, 19.0pp — with D7 6/8
disclosed in the same sentence, plus the A3 uncertainty band and, if A1
requires it, the identity-recognition caveat; governance map (PROJECT.md →
CLAUDE.md → decisions_log → GATE_PACKAGE → review_packets); "reproduce our
numbers" instructions (B2/B3); limitations pointer; and an honest "what this
is not" paragraph (n=16, single analyst, harness-mediated evaluatee,
nondeterministic sampling, not investment advice).

### B5 — Audit-trail closures
(a) methodology_limitations, J13-e entry: add the causal line — currentDate
    injection weakens point-in-time framing on the harness path; the
    consequence (memorized retrieval) was directly measured by the
    recognition probes and D7 fired, so the design absorbed the risk.
(b) sr11-7_memo.md addendum: one paragraph on f4f8f73 — the only
    post-results code change; CI payload-discipline tests now skip without
    the corpus, enforcement moved to the local pre-run gate; B2/B3 restore
    CI-side, artifact-only enforcement.
(c) review_packets/INDEX.md: resolve the RP-03 numbering gap from git
    history — one explanatory line if intentional, restore the packet if
    not. Silent gaps are audit smells. Investigate history before writing
    the explanation.
(d) overrides.md: draft the J13-b/c ratification entry (third isolation
    mechanism adopted under execution-layer discretion after both pinned
    mechanisms were empirically rejected; isolation gate 5/5 PASS as the
    evidence), marked "PENDING OWNER SIGNATURE — UNSIGNED", with a
    signature block. Do not sign it. Do not mark it resolved.

### B6 — HANDOFF.md: the single ordered owner queue
① sign B5(d) ② confirm Console dashboard $0.00 (check C) ③ workbench
review, MODEL-5 cases first ④ finalize 26 grades ⑤ read A1/A3 outcomes and
set the publication framing (including whether the identity caveat joins the
headline) ⑥ publication decision. State explicitly that everything else in
the repo is now machine-verified (B2/B3) or owner-pending.

## DEFERRED REGISTER (record in HANDOFF, do not execute)
- D-1: paper / public monitor write-up draft — after queue steps ④ and ⑤,
  not before (framing depends on A1/A3 and finalized grades).
- D-2: k escalation beyond 5 — only if A3's pooled decomposition is
  inconclusive AND publication is GO.

## DELIVERABLE
Final report to the owner: per-item completion status; four sentences —
A1 verdict (does perturbation de-identify?), A2 agreement rate, A3 headline
survival under re-drawing + uncertainty band, and what the owner queue now
blocks on; total call count + total_cost_usd sum (reference only — billing
is determined by the auth route); git-diff proof that RP-05 §1 and
scoring/grades/ are untouched.
```

## D19 — RP-08 대조군 재선정: 야간 실행 소유자 사전 승인 (2026-07-07, 서명 후행 구조)

소유자 지시(2026-07-07 세션 지시문, "OWNER DECISION ON RECORD")에 따라 기록:
소유자는 **미서명 DRAFT 기준(docs/CONTROL_CRITERIA_v1.md) 하에서의 야간 대조군
선정 실행을 명시 승인**했고, 소유자 서명이 선정에 **선행하지 않고 후행**함을
수용했다. 이 인가를 보상하는 무결성 설계 (지시문 원문의 4항):

1. 기준은 **어떤 풀 조회보다 먼저 커밋** (타임스탬프 증명 — 본 결정과 criteria가
   같은 커밋에 들어가며, 풀 수집 산출물은 이후 커밋에만 존재).
2. 선정은 채점 존재 이전에 완결 (이번 실행에서 피평가자 호출 0건).
3. 선정 그룹은 **PROPOSED 상태 전용** — 소유자 서명 전 어떤 채점 파이프라인에도
   진입 불가 (사용 전 거부권 게이트).
4. 모든 선정 판단은 개별 서면 근거 (review_packets/RP-08_selection_memo.md).

아침 게이트(소유자): 메모 검토 → [DISCRETIONARY] 스팟체크 → CONTROL_CRITERIA_v1
서명 또는 수정 → control_group_PROPOSED 서명 또는 기각. 기각 경로 비용: 분 단위
재실행 명령이 criteria §6에 명시.

범위 주석: 본 결정은 RP-01 확정 대조군·RP-05 결과(불변)를 건드리지 않는다.
D17은 소유자가 v1 기준에 서명하는 경우에 한해 RP-08 용도로 대체된다.

## D20 — RP-08 아침 게이트: 기준 v1.1 개정 채택 + [DISCRETIONARY] 4건 확정 (2026-07-07, 소유자)

게이트 이행 (HANDOFF ⑦ / RP-08 memo §0). 결정 도출 경위 — 형해화 방지 절차 포함:

1. 소유자 개시 진술 (verbatim): "대조군이 아직 PROPOSED(미서명) 상태서명할게."
2. 보조 Claude가 일괄 서명의 형해화 위험(CLAUDE.md §협업)을 지적하고 서명이
   확정하는 결정 지점 3개(기준 처리 / 재량 4건 / 개별 교체)를 구조화 질의 +
   스팟체크 3건(T12·T17·T28) 요지 제시.
3. 소유자 1차 응답 (3문 공통, verbatim): "너의 추천 방식도 제시해" → 보조
   Claude가 근거 첨부 추천안 제시 (e4_manual_overrides.json 증거 직접 검증 포함).
4. 소유자 확정 선택 (verbatim): **"개정 ①+② (추천)"** — 선택지 문면: "v1.1
   작성·커밋 → 풀 재수집(수십 분) → 재선정 → 갱신 메모 검토 후 서명. 재량
   4건은 지금 확정."

**결정 내용**:
- ① CONTROL_CRITERIA에 **E9 상장 보통주 요건** 신설 (계기: Accellent — PE 소유
  채권 공시자가 T11 선정, memo §2-2. 실험군 8 전원 상장 — 주가 유인 동질성).
- ② §2 보충 SIC 확장 임계를 "스크린 자격자 ≥5"에서 **"규모 밴드 내 자격자
  ≥5"**로 변경 (계기: memo §4-2 — v1 임계는 밴드 적용 전 집계라 3577·7389·2000
  대분류에서 확장 조기 차단, T12·T21·T28 공통 구조).
- ③ 선정 영향 [DISCRETIONARY] 4건(MOS E4 수기 통과 · MOS 매출→자산 축 대체 ·
  FSLR E4 · CPB E4) **확정** — 증거는 e4_manual_overrides.json(보조 Claude가
  게이트 중 직접 검증: 3건 모두 일반 토큰 오탐 + 식별 토큰 색인 0건; 자산 축은
  기준 S1 사전 단서 조항 + RP-01 동일 측정). E4 수기 통과는 선정의 입력이므로
  v1.1 재선정에도 승계. **단서**: 재선정에서 Madden·ADI·FMC가 승격권 진입 시
  웹 2차 확인 선행 (memo §3 명기 조건 유지).
- ④ 개별 교체(FSLR→Avago, Accellent→Accuray) **없음** — 장르 축 문제는 예외가
  아니라 기준 차원에서만 처리(memo §2-6 원칙), 상장성은 ①이 기계적으로 해소.

**효력**: v1 기계 선정 결과(control_group_PROPOSED.json, criteria_sha256
c44bd59a…)는 **서명 없이 superseded** (채점 미진입 상태 폐기). v1.1 재선정
결과는 새 PROPOSED로 생성되며 그 서명은 별도 게이트. 무결성: v1.1 문안+코드
미러는 **재수집 실행 전 커밋** (freeze-then-run, D19 구조 승계).

**학습 노트(§10)**: 풀 구성 파라미터(확장 임계의 집계 시점)가 곧 선정 파라미터
— 8선정 중 3건의 정체가 이 임계 하나로 결정됐다. 기준 개정은 "결과가 마음에
안 듦"이 아니라 "규칙이 세려던 것을 세지 않음"일 때 정당하며, 그 구분의 증거는
개정 전 이력 공개다.

## D21 — RP-09 Stage 0: 채점 26건 소유자 확정 (2026-07-07, JSON 1줄)

{"decision":"D21","date":"2026-07-07","scope":"grades 26 (main 16 + perturbed 8 + pilot 2) human_finalized=true — incl. 5 MODEL-flagged (main case_10; perturbed case_01/02/03/12) 귀속 확정 + MRVL(perturbed case_13) UNCLASSIFIED×2 → DATA(design) PROPOSAL 채택","basis":"owner instruction RP-09 Stage 0, verbatim commit 986a893","effect":"scoring/grades/ + pilot/grades/ frozen under I3 from this commit; treatment-side answer-key evaluation closed","unfinalized_items":0}

## D22 — RP-09 Stage 1: RP-07 D-2 원본 재추첨 사전 등록 (2026-07-07, 실행 전 커밋)

{"decision":"D22","date":"2026-07-07","action":"original-side re-draw (RP-07 D-2): 실험군 8 원본 페이로드 × draws 2-5 = 32 evaluatee calls","output_root":"runs/rp07/draws/draw_{2..5}","cases":["case_01","case_02","case_03","case_06","case_08","case_09","case_12","case_13"],"protocol":"pipeline/runner.py 무변경 — 모델 핀 claude-sonnet-5(D6), 페이로드 build_payload(perturb=False) 결정론(draw1=runs/main과 byte-identical), I1 guard_payload + I2 cutoff 필터 동일, 핀 불일치=discard(재실행), API-key 부재 assert","rng_seed_note":"claude -p 헤드리스에 샘플링 시드 노출 없음 — draw = 비시드 독립 표본 (RP-06 A3와 동일 규약). 고정 난수 요소는 케이스 파일의 셔플된 중립 ID 제출 순서(NEUTRAL_ID_SEED, 기커밋)와 concurrency 3뿐이며 본 커밋이 그 사전 등록","basis":"owner instruction RP-09 Stage 1 (986a893); RP-06_hardening.md §D-2 정의(+32호출)와 일치"}

## D23 — RP-10 발사 중 데이터 사고: 이중 역할 티커 원본 아카이브 덮어쓰기 (2026-07-07, 정직 기록)

{"decision":"D23","date":"2026-07-07","incident":"stage_data가 RP-01 대조군이면서 v2 대조군인 5티커(FORR·GIS·GRMN·MOS·R)의 ~/aaer-data/{T}/{xbrl,edgar} 원본 16파일을 _rp08 캐시본(더 최신 누적 아카이브)으로 무조건 덮어씀 — verify_manifest SIZE MISMATCH 16건으로 발견","impact_bound":"동결 결과(git 커밋 산출물) 불변 — I3 무침해. 영향은 동결 시대 페이로드의 byte 재구성 가능성. 검증: 신파일로 5케이스 페이로드 재구성 → frozen documents_used와 accession 출처 집합 5/5 정확 일치 + 동결 채점 인용값 스팟 3건(R Revenues FY2011, GIS Assets 2018-02-25·SalesRevenueGoodsNet FY2018, GRMN SalesRevenueNet FY2012) 전부 일치 — PIT(filed<=cutoff) 추출은 두 버전에서 동치, 차이는 컷오프 후 신규 사실의 축적분","remedy":"stage_data 덮어쓰기 금지 패치(존재 시 보존) + 데이터 매니페스트를 현상태로 재생성(구본 바이트는 복구 불능 — 사고와 검증을 본 줄로 기록)","lesson":"공유 데이터 디렉토리에 쓰는 도구는 항상 존재-검사 우선 — 동결 시대 입력의 물리 보존이 매니페스트의 전제"}

## D24 — RP-13: 채점 57건 소유자 확정 (2026-07-09, JSON 1줄)

{"decision":"D24","date":"2026-07-09","scope":"grades 57 (wave-2 32 + holdout 3 + wave-1 controls 22) human_finalized=true — RP-13 워크벤치 대화형 소유자 세션(TIER A 13 플래그 우선 개별 검토 → TIER B 22 재검증 후 서명 → grades_v2/controls 22 일괄, RP-09/RP-10 검토 패킷 기근거)","overrides":0,"rubberstamp_check":"Issue #0 §9 기준을 커밋 전 소유자에게 명시 제시, 소유자 확인: 0건은 재량 지점(case_65 d2 top-ranked-only · case_61 d2=2 · case_59 d2=1/d3=0 · case_71 d2=1) 전수 개별 검토 결과이며 형식적 승인 아님 — 잔여 건은 밴드 기계 적용으로 재량 부재","applier":"tools/apply_rp13_finalization.py --also scoring/grades_v2/controls (finalize 57 · override 0 · 잔존 0)","basis":"owner interactive session 2026-07-09 (terminal, AskUserQuestion 서명 13+2문항), 계획 ~/.claude/plans/i-want-to-solve-happy-moonbeam.md Phase 1","effect":"발행 수치 무변경(finalization은 _meta만 변경) — reproduce_analysis 100/100 유지 확인 후 커밋"}

## D25 — Phase 2 사전 등록·스캐폴딩 (2026-07-09, 실행 전 커밋, JSON 1줄)

{"decision":"D25","date":"2026-07-09","action":"freeze-then-run 스캐폴딩 일괄 커밋 (어떤 미터링 호출도 이 커밋 이후에만)","items":["W2_MAINSCORE_REDRAW_PLAN.md §7 로그된 개정 #1 (§5-6): 홀드아웃 본채점 k=5 재추첨 arm — 12 피평가자 호출, 사전 규칙 HUBG p>=50 in >=4/5 → robust, <=3/5 → draw-민감 (완화 없음); draw-1 published 불변","Q-E03 RESOLVED (소유자): E1 감독 하 실행 최우선, GNE→HUBG→WMK, 케이스 경계 commit","tools/holdout_controls.py (E1 드라이버 — wave2_controls 패턴, 동결 control_v2 재지향; 스펙 유도 오프라인·점수독립: HUBG 4731/$3.95B · WMK 5411/$4.79B · GNE 4931/$0.43B, 전건 FYE 12)","tools/holdout_probe.py (knows_event 프로브 러너 — runs/holdout/recognition 스키마 미러, 핀 claude-sonnet-5)","analysis/holdout_redraw_analyze.py (§7-3 규칙 기계 적용)","analysis/holdout_controls_analyze.py (§4 사전 고정 — rule-of-three/CP 순수파이썬, 0% 헤드라인 금지)"],"basis":"승인 계획 Phase 2 (~/.claude/plans/i-want-to-solve-happy-moonbeam.md); OWNER-GATE-E 예산 E1≈18-27 + redraw 12","metered_calls_this_commit":0}

## D26 — E1 대조군 채점 9건 소유자 확정 + 결과 반영 (2026-07-09, JSON 1줄)

{"decision":"D26","date":"2026-07-09","scope":"scoring/grades_holdout_controls hc_01..09 human_finalized=true — E1 감독 세션 내 소유자 mini-sign-off (밴드 재도출 검증 + FP 2건 rationale 확인 후 전건 finalize, 오버라이드 0)","results":"per-case: HUBG 70 > {RXO 42, BCO 30, XPO 20} 유일 분리 · WMK 32 미분리 {GO 58, SFM 32, VLGEA 12} · GNE 42 미분리 {GRDX 78, VIASP 35, UTL 20}; FPR 2/9=22.2% CP95 [2.8%,60.0%]; perm p=0.2045 CONTEXT ONLY(H1 미주장)","gate_incident":"FWRD knows_event=True 탈락 → XPO 승격 (gate_failures.json); probe 비멱등 재실행 2호출 정직 기록 — E1 실호출 30 (추정 18–27 +3)","docs":"holdout_summary §5 해소 + ISSUE_2 §3b 추가","basis":"HOLDOUT_CONTROLS_PLAN §2/§4/§7 사전 고정 그대로 — 사후 재해석 없음"}

## D27 — E5§7 홀드아웃 재추첨 완료: 사전 규칙 판정 robust (2026-07-09, JSON 1줄)

{"decision":"D27","date":"2026-07-09","action":"홀드아웃 본채점 k=5 재추첨 완료 (draws 2-5, 12 피평가자 호출, draw 경계 commit·push 전건)","result":"HUBG p>=50 5/5 (draw별 70/76/60/58/60, median 60, band [58,76]) → 사전 커밋 규칙(>=4/5) 'H2 탐지는 draw 잡음에 강건' · WMK [28,42] 0/5 · GNE [30,42] 0/5 — 뒤집힘 0, 불안정 보고 없음","invariants":"발행 per-case = draw-1 유지 · H1 미주장(N=3) · 판정은 holdout_redraw_analyze.py 기계 적용 (재해석 없음)","docs":"holdout_summary §2 밴드 병기 + ISSUE_2 §3 표 갱신","metered":"세션 누계 42 (E1 30 + redraw 12), 전역 cap 320 內"}

## D28 — Phase 5: README 통계 재구성 + L-6 + canon 배선 (2026-07-09, JSON 1줄)

{"decision":"D28","date":"2026-07-09","action":"발행 서사 재구성 (무호출)","items":["README dose-response 강등: 백본 = per-wave standalone 순열 유의성(0.00114/0.00116) 생존, AUC 0.824→0.829는 2차 gradient 관찰로 격하 + CI [0.599,0.983]/[0.616,0.983] 본문 병기 + 'CI 폭이 동등성 주장 금지' 본문 명시","synthesis.md 판독 동일 재구성","README 층③에 E1·k=5 최종 수치 반영 + FPR 절에 E1 2/9 CP[2.8%,60%] 추가","L-6 intra-family 편향 methodology_limitations 기입 + README 한계 한 줄","lint_publication canon() 사장 코드 배선: README↔결과JSON 수치 드리프트 기계 검출 (check_canon, 소유자 권고 승인 사항)"],"gates":"lint(canon 포함)·reproduce 100/100·pytest green"}

## D29 — Phase 6: 영어 발행 표면 (2026-07-09, JSON 1줄)

{"decision":"D29","date":"2026-07-09","action":"영어 README 전환 (무호출)","items":["git mv README.md→README.ko.md + 영어 README.md 신규 (Phase 1/3/4 최종 수치 반영: 57+9 확정, E1 HUBG만 분리·FPR 2/9, k=5 5/5 robust; standalone-유의성 백본 구조 그대로)","lint DOCS에 README.ko.md 추가 (하드코딩 리스트의 무음 탈락 맹점 폐쇄)","영어 맹점 자가 검열: zero/no-false-positives 문구 부재, G2 3사 문장 provisional/restatement 동반, EXPLORATORY 병기 확인","이슈 초안 3종은 원래 영어로 확인 — _EN 중복본 불요 (계획 항목 무효화 기록)"],"github_metadata":"repo description+topics는 기설정 (bg job fd9d67c4에서 완료 확인)","gates":"lint(양 README+canon)·reproduce 100/100·pytest·blindness green"}

## D30 — repo rename aaer-project → aaer-evals (2026-07-10, JSON 1줄)

{"decision":"D30","date":"2026-07-10","action":"gh repo rename — lastwhisper906-gif/aaer-project → lastwhisper906-gif/aaer-evals (소유자 승인, README 제목·로컬 디렉토리 일치화)","redirect":"GitHub 구이름 자동 리다이렉트; 로컬 remote URL 갱신 + fetch/CI 확인 완료","in_repo_refs":"저장소 내 aaer-project 자기참조 0건 (grep 확인)","note":"CI 확인 명령은 이제 gh run list --repo lastwhisper906-gif/aaer-evals"}

## D31 — 잔여 교정 Phase 0: 발행 표면 수정 5건 (2026-07-10, JSON 1줄)

{"decision":"D31","date":"2026-07-10","action":"발행 전 표면 수정 (무호출) — 2·3차 외부 검토 잔여 항목","items":["0-1 GRDX 78 표면화: README 양어 E1 절 + ISSUE_2 §3b에 '홀드아웃 tier 최고점=대조군 오탐(GridAI GRDX 78), HUBG 70은 자기 매칭군만 상회' 병기 + lint (H) GRDX·78 co-presence 기계 강제","0-2 W3 프레이밍 교정: README 양어의 '교란 프레임=능력 하한' 서술을 '덜 오염된 측정, clean lower bound 아님 — 잔여 인지 5–6/8 지속, 구조적 하한은 홀드아웃뿐'으로 교체 + lint (G) 교란+lower bound 결합 금지(교정문구 allowlist); synthesis/ISSUE_0/1에는 해당 표현 부재 확인(grep)","0-3 methodology_limitations에 'Instrument bias directions' 4행 표 신설 (name-ID=지목 하한/DAR FN · perturb delta=표면암기 하한/잔여인지 5–6/8 · cognitive probe=단발 점추정/6/8→5/8 · recognition gate k=1 거짓음성 산술 0.7^3≈34%)","0-4 docs/FUTURE_CYCLE_PROTOCOL.md 신설 (salt 갱신·GT 매핑 sha256 봉인·카나리 프로브 2회·rolling holdout 1차 승격 + repo 학습유입 시 소모품 영구 소각 명시)","0-5 ISSUE_2 서사 보강은 diff-only: RP-14 워크벤치 + OWNER_QUEUE Q-R01 (draft 본문 미적용)"],"deviation_note":"미션 문면의 '잔여 인지 4–5/8'은 동결 기록(L-5: draw-1 6/8·draw-2 5/8)과 불일치 — repo 동결값 5–6/8 채택, 미션값 미사용 (정직 기록)","gates":"pytest 76 · reproduce 100/100 · lint PASS(신규 G/H 포함, 음성 테스트 확인) · blindness PASS"}

## D32 — Phase 1 사전 등록: recognition gate k=5 승격 (2026-07-10, JSON 1줄, 프로브 발사 전 커밋)

{"decision":"D32","date":"2026-07-10","action":"recognition gate k=5 사전 등록 — analysis/GATE_K5_PLAN.md + analysis/gate_k5_analyze.py(결정론 판정기) 프로브 호출 전 커밋 (freeze-commit-then-run)","targets":"HUBG·WMK·GNE knows_event draws 2–5 (12호출, 동결 tools/holdout_probe.py 무수정 재사용, 출력만 runs/holdout/recognition_k5/) + HTZ 양성대조 1호출 선행 (False면 즉시 중단+OWNER_QUEUE)","rules_prefixed":"band ≥2/5 True → 홀드아웃 자격 상실(H2 제외·강등 사유 발행 표면 명시·Tier-③ 재작성, HUBG면 Issue #2 발행 보류 긴급 항목) · ≤1/5 → 자격 유지 + 'gate band x/5 (k=5)' 병기(draw-1 발행값 불변) · 해석은 §3 사전 등록 3방향 문장만","boundary_commits":"[HTZ+draw-2]·[draw-3]·[draw-4]·[draw-5] 4회, 각 커밋 전 verify_blindness --write-manifest","budget":"Phase 1 = 13호출 (세션 cap 60)"}

## D33 — Phase 1 판정: gate k=5 결과 방향 (i) — 자격 3/3 강건 (2026-07-10, JSON 1줄)

{"decision":"D33","date":"2026-07-10","action":"recognition gate k=5 실행 완료 (13호출: HTZ 1 + 3케이스×draws 2–5 12, 경계 커밋 4회 전건 push)","result":"HTZ 양성대조 True(high) — 민감도 확증 · HUBG 0/5 · WMK 0/5 · GNE 0/5 (knows_event=True 0건) → 사전 규칙(≤1/5) 자격 3/3 유지, 결과 방향 (i), 판정 gate_k5_analyze.py 기계 적용","interpretation":"사전 등록 문장 (i) 그대로 — draw 잡음에 강건; k=1 거짓음성 산술(≈34%)은 반박이 아니라 관측 인지율이 가정(30%)보다 낮은 방향 시사로만 기술","docs":"holdout_summary §1 밴드 병기 + README 양어 병기(draw-1 발행값 불변) + ISSUE_2는 RP-14 DIFF-2로 diff-only + Q-R01 갱신","metered":"Phase 1 실호출 13/13 (초과·낭비 0), 세션 누계 13/60","invariants":"발행 동결값 무변경 — 전부 병기; Issue #2 발행 보류 긴급 항목 비발동"}

## D34 — Phase 2 사전 등록: wave-2 outcome-recognition 프로브 (2026-07-10, JSON 1줄, 발사 전 커밋)

{"decision":"D34","date":"2026-07-10","action":"wave-2 outcome-recognition 사전 등록 — analysis/OUTCOME_RECOGNITION_PLAN.md + analysis/outcome_recognition.py(결정론) 호출 전 커밋","targets":"wave-2 전 32사(실험군 9+대조군 23), identity-exposed, 동결 tools/holdout_probe.py 무수정(홀드아웃 게이트와 동일 knows_event 계기), 출력 runs/wave2/outcome_recognition/, 티커 알파벳순, 케이스 경계 commit·push 전건","purpose":"dose-response x축을 name-ID(대리)에서 outcome-knowledge(직접)로 승격 — Tier ①②/③ 계기 정렬. 무분기(branchless): 어떤 임계도 R/H 판정 불변, name-ID 서사(50%→21.9%→0%) 유지 병기","reporting_prefixed":"그룹별 인지율+CP95(동결 clopper_pearson 재사용) · name-ID 4분면 §reconcile(event_only=이름 상기 불능이나 사건 인지 → name-ID 거짓음성 실증) · synthesis/README 2축 병기(wave-1은 미측정 정직 표기)","budget":"Phase 2 = 32호출 (누계 13→45, cap 60)"}

## D35 — Phase 2 결과: outcome-knowledge 실험군 8/9 — name-ID 계기의 대폭 과소측정 실증 (2026-07-10, JSON 1줄)

{"decision":"D35","date":"2026-07-10","action":"wave-2 outcome-recognition 32호출 완료 (케이스 경계 commit·push 32회 전건, FAIL 0) + 결정론 분석 + 2축 반영","result":"실험군 knows_event 8/9=88.9% CP[51.7%,99.7%] (미인지 OSIR 유일) · 대조군 0/23 CP[0%,14.8%] · reconcile: both 3(CSC·HAIN·UAA)/name_only 4(대조군 BF-A·LEVI·LPSN·RL)/event_only 5(BRX·CGI·MDXG·TNGO·WFT)/neither 20","honest_reading":"'wave-2는 덜 암기(wave-1의 절반)' 서사는 name-ID 계기 한정 — 직접 계기로는 정체-노출 프레임에서 실험군 8/9 사건 지식 가용; 직접 축 정렬 시 암기 제거는 wave-2→홀드아웃 사이. event_only 5건 = name-ID 거짓음성 방향 실증 (bias 표 1행 확증)","branchless":"사전 등록대로 R4·R/H 판정·name-ID 21.9% 서사 전부 불변 — 2축 병기만 (synthesis §1 표 + README 양어 층②·gradient 절)","metered":"Phase 2 실호출 32/32 (초과·낭비 0), 세션 누계 45/60"}

## D36 — Phase 3 사전 등록: 정체 3-arm 실험 (2026-07-10, JSON 1줄, 발사 전 커밋)

{"decision":"D36","date":"2026-07-10","action":"3-arm 사전 등록 — analysis/IDENTITY_3ARM_PLAN.md + data/evaluatee/fict_names_wave2.json(가공 사명 9, 전건 attempt 0 채택) + tools/gen_fict_names.py + tools/run_identity_arms.py + analysis/identity_3arm_analyze.py 호출 전 커밋","design":"(a) 익명=동결 perturbed · (b) 가공 사명=동결 build_payload(perturb=True)에 정체 토큰만 중첩 (신규 9호출) · (c) 실명=동결 원본 — pipeline/ 무수정 import 재사용","fict_names":"sha256(case_id+'fictname-v1'+attempt) 결정론; EDGAR 전 filer 사명 1,049,982행 부분문자열 + 실존 티커 10,418 전수 스크린 — 충돌 0, 독립 재검증 스크립트로 이중 확인; 참조 목록은 ~/aaer-data/reference/ 스크린 전용(페이로드 반입 없음, data/README.md 기록)","readout_prefixed":"paired delta (b−a)·(c−b) median + 정확 부호검정(병기); 분류 임계 10pp 사전 등록 바 재사용 — (i) b≈a AND c−b≥10 → 실명 토큰 방향 증거 (ii) 전부 ≈ → 암기 기여 작음 (iii) 그 외 → 해석 보류+기록. N=9 방향 증거, 인과 확정 서술 금지, R/H 불변","budget":"Phase 3 = 9호출 (누계 45→54, cap 60)"}

## D37 — Phase 3 판정: 3-arm 분류 (ii) — a≈b≈c (2026-07-10, JSON 1줄)

{"decision":"D37","date":"2026-07-10","action":"arm (b) 9호출 완료 (케이스 경계 commit·push 9회 전건, FAIL 0, 핀 불일치 0) + 결정론 판독","result":"median(b−a)=+6.0pp · median(c−b)=−2.0pp (부호검정 p=0.18/1.0 병기) — 양쪽 10pp 바 미달 → 사전 등록 분류 (ii) '암기의 점수 기여가 작다는 방향 증거 (a≈b≈c)'","per_case":"OSIR 65/70/58 · TNGO 52/60/55 · CSC 55/45/40 · HAIN 45/60/58 · MDXG 58/62/65 · CGI 62/68/72 · WFT 55/55/74 · UAA 42/55/55 · BRX 20/30/20 (a/b/c)","framing":"사전 등록 문장 (ii) 그대로 — N=9 방향 증거, 인과 확정 서술 금지; D35(사건 지식 8/9 가용)와의 종합 해석은 독립 계기 병기로만, 소유자 검토 이관","docs":"synthesis §1b + README 양어 층② 병기","metered":"Phase 3 실호출 9/9 (초과·낭비 0), 세션 누계 54/60"}

## D38 — Phase 4: raw API 이행 스캐폴드 (2026-07-10, JSON 1줄, 무호출 — 소유자 게이트)

{"decision":"D38","date":"2026-07-10","action":"freeze 개정 #3 초안 + 스캐폴드 커밋 (실행 배선 없음)","items":["docs/FREEZE_REV3_DRAFT.md — 하네스→순수 SDK (J13-e 주입 제거, threat_model V4 원안 복귀, temperature 핀 가능 = L-3 부분 해소, INVARIANT 4 개정은 소유자 결정), 동치성 테스트 설계(pilot 2케이스 k=5 양경로, 게이트 아닌 측정, ~30호출 종량)","pipeline/api_client.py — cli_client.call_model 동일 CallResult 인터페이스, 이중 안전장치(AAER_RAW_API_APPROVED=1 + API 키), 동결 가드·재시도·핀검증·로그 규약 재사용","pipeline/runner_api.py — runner.py 병렬 변형 (동결 모듈 import만, runner.py 무수정 — §8-3 소진 없음)","pipeline/test_api_client.py — 무호출 테스트 5건 (가드 발동·인터페이스 동일성) green"],"invariants":"동결 결과 재실행 금지 — 다음 실행 배치부터; 기존 러너의 api_client import 0","owner_gate":"OWNER_QUEUE Q-R02 (키·과금·발효 시점 3건 이관)","metered":"Phase 4 = 0호출, 세션 누계 54/60"}

## D39 — 발행 완결 미션 Phase A: DIFF-3 재배선 + 3-arm 서사 조정 + L-7 (2026-07-11, 무호출, JSON 1줄)

{"decision":"D39","date":"2026-07-11","action":"발행 전 서사 정비 (0호출) — 3차 외부 검토 잔여 2건 + 한계 기입","items":["A-1 DIFF-3: ISSUE_1 §5 논증 사슬 재배선 diff를 RP-14에 추가 (diff-only, 미적용) — '덜 유명→덜 암기→잔여 능력' 사슬이 D35 실측(outcome-knowledge 8/9=88.9% CP[51.7%,99.7%])과 모순; 재배선 근거 3갈래 = (a) 정체-가림 비붕괴(dominance 3/9 단발·4/9 E3 median < 5/9 바) (b) 정체 조작 무반응(3-arm a≈b≈c, median(b−a)=+6.0pp < 10pp 바) (c) 암기불가 홀드아웃 잔존(gate k=5 0/5×3); 종합문장 '지식은 존재(8/9)하나 점수로 기능한다는 증거가 바에 미달' — 방향 증거 한정, 인과 확정 금지. Q-R01 범위 DIFF-1/2/3으로 갱신","A-2 3-arm 발행 서사 조정: synthesis §1b + README 양어 — 1차 증거 = b−a(+6.0pp, 동일 교란 페이로드·이름 토큰만 차이 = 유일한 깨끗한 대비) · 2차 관찰 = c−b(−2.0pp, 실명+실수치 복원 = 정체 효과·스케일 복원 효과 혼입 명시) · 해상도 한계 1줄(a·c=과거 동결 draw vs b=신규 draw, 케이스당 5-draw 밴드 12–18pp≈±10pp E5§7 실측, ±6pp median은 그 해상도 내 방향 판독) + lint 규칙 (I) 신설: 발행 표면의 3-arm delta 인용은 confound·draw-noise 단서 동반 강제 (음성 테스트로 발화 확인)","A-3 L-7 기입: methodology_limitations '3-arm arm (c) 설계 교란변수' — 3차 외부 검토 식별 명기(귀속 기록), 설계 원인 = D36의 동결 draw 재사용(신규 호출 0 트레이드오프), c′ 순수 대비는 소유자 게이트(기본 SKIP); README 양어 한계 절에 L-7 1줄"],"honest_correction":"D37 서사 전사 오류 교정 — synthesis §1b 부호검정 병기값 'p=0.18/1.0'은 동결 identity_3arm_results.json(b−a p=0.07031 7/8 양성 · c−b p=0.72656)과 불일치. JSON 정본 채택, synthesis에 교정 각주 ¹ᵇ. D37 원장 라인은 사후 수정 금지 원칙에 따라 불변 — 본 라인이 교정 기록. 분류 (ii)·median·발행 동결값 전부 불변 (부호검정은 애초 병기 전용)","invariants":"수치 재계산 0건 — 전부 서사/프레이밍 층; 발행 동결값 불변","gates":"pytest 81 · reproduce 100/100 · lint PASS(신규 (I) 포함, 음성 테스트 발화 확인) · blindness PASS","metered":"Phase A = 0호출"}

## D40 — 발행 완결 미션 Phase B: 소유자 서명 세션 (2026-07-11, 대화형, 무호출, JSON 1줄)

{"decision":"D40","date":"2026-07-11","action":"소유자 대화형 서명 세션 (RP-13/D24 선례 AskUserQuestion 방식) — RP-14 3건 + 잔여 큐 전건 + 발행 형식 + Phase E go/no-go","signatures":{"DIFF-1":"적용 (원문 그대로) — ISSUE_2 §3 crux에 HUBG 단일 robust 케이스 의존 병기","DIFF-2":"적용 (원문 그대로) — ISSUE_2 §2에 gate k=5 band 문단 추가","DIFF-3":"수정 적용 — ISSUE_1 §5 논증 사슬 재배선, 단 name-ID 25%를 Q-E02(A) 정합으로 '21.9% (frozen name_match rule, 7/32; 25% under a rename-aware human reading — the DAR boundary case)'로 치환 (소유자가 정합 옵션 2안 중 선택)","E4_EXPLORATORY":"Issue #0 §7-5·§8 문언 그대로 승인 (RP-13 §7-③ 해소)","Console":"$0.00 소유자 대시보드 확인 완료 (RP-13 §7-④ 해소 — 소유자 화면 정보, 세션 검증 불가 명시)"},"queue":{"Q-E01":"RESOLVED (A) — E2/E4/E5 launch-ready 동결 유지, v1.0 이후 소유자 임의 발사","Q-E02":"RESOLVED (A) — 21.9% 1차 + 25% rename-aware 각주; wave2_summary §4 산문 정합, README/synthesis 기존 형태 무변경","Q-R01":"RESOLVED — DIFF-1/2/3 위 서명대로","Q-R02":"RESOLVED (A) GO — freeze 개정 #3 다음 실행 배치부터 발효 확정; 래치 해제 조건 4건 FREEZE_REV3_DRAFT §6 신설 (키 주입 셸 한정·승인 플래그 배치 opt-in·E2 전 동치성 스모크 필수·INVARIANT 4 개정 기록); 이번 세션 실행/과금 배선 0"},"publication_format":"GitHub Issues (#0→#1→#2 순차, 건별 게시 직전 최종 렌더 소유자 확인 1회) — 즉시 공개 추적 가능","phase_E":"SKIP (기본값 채택) — c′ arm 미실행, L-7 한계 기재로 충분, 미터링 0 유지","applier":"tools/apply_rp14_diffs.py (멱등, 앵커 완전 일치, dry-run 검증 후 3/3 APPLIED)","invariants":"발행 동결값·R/H 판정 불변 — 전부 서사/프레이밍 층; 수치 재계산 0","learning_note":"서명 세션에서 알아야 할 것: 독립적으로 서명된 두 결정(DIFF-3 원문 25%·Q-E02(A) 21.9%)이 충돌할 수 있다 — 충돌은 세션이 자체 해소하지 않고 정합 옵션을 명시 제시해 소유자가 고른다 (이번: 21.9% 정합 적용 선택)","metered":"Phase B = 0호출"}

## D41 — 발행 완결 미션 Phase C: 3-이슈 발행 + v1.0.0 동결 (2026-07-12, 무호출, JSON 1줄)

{"decision":"D41","date":"2026-07-12","action":"발행 실행 (Phase B 서명 완료 + 4게이트 green 전제 충족 확인 후) — GitHub Issues 3건 순차 게시 + README 발행 절 + v1.0.0 annotated tag/Release","published":{"issue_0":"https://github.com/lastwhisper906-gif/aaer-evals/issues/1 (wave-1 R3)","issue_1":"https://github.com/lastwhisper906-gif/aaer-evals/issues/2 (wave-2 R4, DIFF-3 수정 적용 반영)","issue_2":"https://github.com/lastwhisper906-gif/aaer-evals/issues/3 (holdout H2, DIFF-1/2 반영)"},"protocol":"건별 게시 직전 소유자 최종 렌더 확인 3회 전건 승인 (title+banner+변환 4종 제시: H1 분리·Published 배너+번호 매핑 주석·본문 Issue #N→Issue N 자동링크 오염 방지·저장소 푸터) — 본문은 서명본(0bc53c1) 전문, 수치·결론 무변경","repo_updates":"README 양어 Publication/발행 절 신설(URL 3건+v1.0.0 링크) · 거버넌스 지도 5항 '미발행'→'게시 완료' · ISSUE_*_DRAFT.md 3건 배너 DRAFT→PUBLISHED+URL (동결 원문 선언) · OWNER_QUEUE Q-R03 신설 (Zenodo DOI — 소유자 계정 작업, 3줄 절차, 자동화 금지)","deviation_note":"배너 문구 'Published 2026-07-11'은 서명 세션(D40) 일자 — 실제 게시 UTC 타임스탬프는 2026-07-12T00:15Z (세션이 UTC 자정 경계를 넘음). 승인된 렌더는 사후 수정하지 않고 본 라인이 교정 기록","invariants":"발행 동결값·R/H 판정 불변 — 게시본 = 서명본 전문 + 표면 변환 4종만","metered":"Phase C = 0호출"}

## D42 — 발행 완결 미션 Phase D: Reader Validation Package (2026-07-12, 무호출, JSON 1줄)

{"decision":"D42","date":"2026-07-12","action":"docs/reader_validation/ 신설 — Tier 3(가치 검증) 실행 활성화 에너지 최소화 (ready-to-send 상태)","deliverables":["ONE_PAGER.md — 영문 1페이지: Question/Design(3-tier×freeze-then-run)/Results(동결값, GRDX 78 오탐 포함 — 유리한 것만 선별 금지 준수)/3줄 한계(L-1~L-7 압축)/repo·release 링크; lint DOCS 편입 (규칙 (I) 3-arm confound·draw-noise 단서 포함 확인, PASS)","FEEDBACK_FORM.md — 7문항 상한: 고정 핵심 3(과대주장 지목·방법론 첫 공격 지점·누가 돈/시간을 쓰겠나 — Tier 3 가치 기준 직결) + 독자 유형별 1–2 (회계실무/ML evals/투자리서치)","TARGET_LIST_TEMPLATE.md — 독자 5–10 슬롯, 유형 균형 가이드(회계·감사 2+/AI evals 2+/금융실무 1+), 연락 경로·발송일·회신 기한(+10일) 컬럼, 실명은 소유자 기입","OUTREACH_MESSAGE.md — cold/warm 영문 초안 2건, 각 120단어 미만, 단일 요청('원페이저 5분+3문항')"],"human_task":"패키지 발송은 소유자 인간 작업 — 자동화 금지 (HANDOFF 명시)","gates":"pytest 81 · reproduce 100/100 · lint PASS(ONE_PAGER 편입 포함) · blindness PASS","metered":"Phase D = 0호출"}

## D43 — 소유자 인간 작업 실행 계획 서명 (2026-07-12, 대화형, 무호출, JSON 1줄)

{"decision":"D43","date":"2026-07-12","action":"발행 후 소유자 잔여 인간 작업 4건 — 추천 경로 제시 + 소유자 승인 (전건 추천안 채택)","plan":{"1_reader_dispatch":"warm 5–7명 1차 발송 (이번 주, 유형 균형 회계·감사 2+/AI evals 2+/금융실무 1+ 유지) — 이메일 본문에 원페이저 붙여넣기 + 핵심 3문항 동봉, 회신 기한 발송+10일; cold는 회신 부족 시 2차 배치. 근거: 8/18 이동 전 회신 수집 마지노선 = 7월 중순 발송, Tier 3 성공선(5명 중 2 응답)은 대량보다 확실한 소수 유리","2_zenodo":"Q-R03 경로 (A) — Zenodo GitHub 토글 → v1.0.0 릴리스 삭제→동일 태그·동일 노트 재생성 (웹훅 트리거, 단일 동결점 유지). DOI 발급 후 README 배지 반영은 세션 작업","3_qr02_followup":"발송 직후 이번 주 — API 키 발급 + 동치성 스모크(~30호출 종량) → E2를 독자 회신 대기 기간에 실행, 8/18 전 양쪽 완결 경로","4_e_batch":"E2 + E4만 발사 (E4 ~20호출, EXPLORATORY 각주 전용 유지) — E5는 launch-ready 동결 유지 (draw-1 발행값이 이미 k=5 부분 밴드로 보강, 한계가치 최저)"},"boundary":"4건 전부 소유자 인간 작업 — 세션은 계획 기록·자료 제공까지 (발송 자동화 금지 불변, 키·계정·과금은 소유자 권한). E2/E4 발사 자체는 실행 시점에 RESUME.md 재개 명령으로 — 스모크 테스트 결과 커밋 선행 필수 (FREEZE_REV3 §6 래치 조건 3)","learning_note":"이 계획에서 알아야 할 것: 마감(8/18)이 있는 인간 작업은 '무엇을'만이 아니라 '어느 창(window)에서'가 결정의 실체다 — 독자 회신 대기 +10일을 E2 실행 창으로 겹치면 직렬 대기가 병렬 완결로 바뀐다","metered":"0호출"}

## D44 — WS-1 (F-4) 사전 등록: payload-v2 진단 추출기 (2026-07-12, 무인, 무호출, JSON 1줄)

{"decision":"D44","date":"2026-07-12","action":"specs/payload_v2.md 사전 등록 커밋 (freeze-commit-then-run — 구현 코드가 git 이력에 존재하기 전) — 페이로드 맹점 2개(8-K item 코드 비가시·shares/EPS 단위 필터 탈락)를 진단 추출기로 복원","scope":"diagnostic-only — 출력은 runs/diagnostics/payload_v2/로 한정, 어떤 피평가자 페이로드에도 편입 안 함. 편입은 명명된 미래 소유자 게이트(신규 미터링 런 + 페이로드 재동결 + freeze 개정) — 이 세션 범위 밖","data_contract":"submissions JSON items 필드 77/77 티커 실측 · companyfacts dei:EntityCommonStockSharesOutstanding(shares)·EPS Basic/Diluted(USD/shares)·WeightedAverage 계열(shares) 실측 · 정직 기록: 미션 문면 태그 WeightedAverageNumberOfSharesOutstandingDiluted는 실측 부재, 실제 태그 WeightedAverageNumberOfDilutedSharesOutstanding — 두 철자 화이트리스트 병기","pit":"filed<=cutoff(등호 포함)·(tag,period) 최신 filed 승리(accession tie-break)·기간 밴드 동결 빌더 동일·fail-closed(파싱불가 날짜 예외·파일 부재 예외·네트워크 fetch 금지)","coverage_finding":"HUBG 하위 파일 1건 미캐시(CIK0000940942-submissions-001.json, 1996~2007 구간) — fetch 않고 coverage 기록 + OWNER_QUEUE 소유자 fetch 과제","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 진단 추출기와 페이로드 변경의 경계는 '피평가자가 보는가'다 — 같은 코드라도 출력이 runs/diagnostics/에 머물면 동결 불변, 페이로드에 실리면 재동결 사안"}

## D45 — WS-2 (F-1) 사전 등록: B3 결정론 메타신호 기준선 (2026-07-12, 무인, 무호출, JSON 1줄)

{"decision":"D45","date":"2026-07-12","action":"specs/B3_metasignal.md 사전 등록 커밋 (freeze-commit-then-run — analysis/b3_compute.py가 git 이력에 존재하기 전) — 귀속 실험: CL7이 지시하는 제출 연대기 채널을 '사소한 사전 등록 규칙'(6지표 비가중 합 0–6)이 얼마나 포착하는지의 상한","frozen_before_compute":{"windows":"W4=365d·W8=730d, cutoff 포함, W8=1차 (은폐기간>1년 상례·위반종료→집행 중위 ≈28.9개월)","indicators":"b_nt(NT 10-K/Q prefix)·b_ka(10-K/A)·b_qa(10-Q/A)·b_401·b_402(WS-1 parse_items 정확 토큰)·b_8kfreq(8-K만, >1.5×선행 3윈도 중위, 이력부족 0+insufficient_history)","aggregation":"비가중 합 — 가중 적합 금지 (N=30/32/12로 6계수 정직 추정 불능, 사전 등록 반과적합 근거)","stats":"tie-aware AUC(stats.py::auc 의미론)·bootstrap 10k percentile CI·단측 순열 100k·SEED_B3=20260712 신규 선언·tier별 절대 비pooled","interpretation_rule":"wave-2 W8에서 (AUC_B3−0.5)/(AUC_LLM−0.5): ≥0.5→능력 해석 완화 diff 제안 의무(diff-only)·≤0.2→비자명성 강화 병기만·중간→부분 귀속 무주장 (경계값 AUC_B3=0.6645/0.5658, gap=0.329 동결값)","llm_auc_frozen":"재계산 금지 — wave-1 0.8239(results_stats.json)·wave-2 0.829(wave2_results.json)·holdout 동결 AUC 부재(N=3, 귀속비 미계산)"},"e2_contract":"b3_score(ticker,cutoff,window_days)->dict import 가능 순수 함수 노출 — E2 동결 파일 무수정","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 기준선의 자격은 '사전에 고정된 사소함'이다 — 계산 후 지표를 고르거나 가중치를 맞추는 순간 B3는 기준선이 아니라 또 하나의 적합 모델이 된다"}

## D46 — WS-3 (F-6) 사전 등록: 홀드아웃 라벨 분류 체계 Big R / little r (2026-07-12, 무인, 무호출, JSON 1줄)

{"decision":"D46","date":"2026-07-12","action":"specs/label_taxonomy.md 사전 등록 커밋 — G2 잠정 라벨의 'restatement=intentional misstatement' 합성어 위험을 Item 4.02 비신뢰 구분(Big R/little r)으로 재범위화. 동결 홀드아웃 수치·스코어보드 무변경 (병기 층)","tagging_rule":"revelation=cutoff+1일(레지스트리 8-K 일자와 대조, 불일치 fail-closed) · neighborhood=revelation±90일 · 8-K/8-K/A item 4.02(WS-1 파서) 존재→bigR, 부재→little_r · 증거=accession+filingDate+items_raw 의무 · 캐시 스냅샷이 neighborhood 상한 미달 시 insufficient_cache 플래그","base_rates":"~2.2% AA 재작성→집행(Karpoff/Koester/Lee/Martin TAR 2017) · ~89.4% GAO 재작성 fraud 무관·~26.4% irregularity(Hennes/Leone/Miller 2008, 의도성 프록시≠집행률 플래그) · Chu/Dechow/Hui/Wang 2018 정성 지지만 — 정확 수치는 소유자 원문 대조 게이트(OWNER_QUEUE)","upgrade_protocol":"모니터링 4년(HUBG→2030-02-05·WMK→2030-02-20·GNE→2030-03-12, 28.9개월 중위+버퍼) · AAER 지명 시 provisional→confirmed 신규 D-엔트리+병기만 · 대칭: 윈도 만료 무집행→'no enforcement within window' 주석 자체가 라벨 노이즈 보고 결과 (기저율상 다수 기대치 명시)","naming_diff":"diff-only — RP-15_label_naming_diff.md + OWNER_QUEUE 게이트, 발행 표면 직접 수정 0","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 라벨 업그레이드 프로토콜은 상향(AAER 확정)만 사전 등록하면 편향이다 — 윈도 만료 무집행이라는 반대 결과를 같은 무게로 사전 등록해야 라벨 노이즈가 데이터가 된다"}

## D47 — WS-4 (F-7) 보정 주장 재범위화: 서수 규약 + diff-only (2026-07-12, 무인, 무호출, JSON 1줄)

{"decision":"D47","date":"2026-07-12","action":"specs/calibration_scope.md — 발행 0–100 점수의 해석 규약을 서수(ordinal, 순위·플래그)로 선언, 확률 기능 부인 (ECE 0.209/0.179 개선 없음). 동결 데이터·수치 무변경, 발행 표면은 diff-only (RP-16, Q-F04)","no_recalibration_rationale":"사전 등록 — N≈30–60에서 Platt/isotonic은 비닝/적합 노이즈 지배, 소표본 ECE 자체가 불안정 추정량 → ECE는 진단 병기 전용 유지; 재보정 재개 하한 N≥150 사전 고정","expected_behavior_note":"verbalized-confidence 문헌상 LLM 표명 확신도는 체계적 과확신 — 관측 미보정은 기대 모델 행동, 파이프라인 결함 아님 (나쁜 결과 미화 금지와 양립: 그대로 보고)","hard_constraint":"schemas/llm_output.json misstatement_probability 필드 개명 금지 — 커밋 출력 재현성 파괴; misstatement_score 개명은 Cycle-2 등록 항목으로만","surface_inventory":"발행 표면 probabilit 전수 grep 5건 처분 — DIFF-6(ISSUE_0:163 서수 규약 문장)·DIFF-7(ISSUE_2:71 표 헤더 LLM p→LLM score)·스키마 무변경·README ECE 서술 이미 진단 프레임 무변경·ONE_PAGER 히트 0","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 재보정은 언제나 가능해 보이지만 소표본에서는 '보정된 것처럼 보이는 곡선'을 만드는 기술일 뿐이다 — 하한(N≥150)을 지금 박아두는 것이 미래의 자기기만을 막는다"}

## D48 — WS-5 (F-2) 사전 등록: perturbation-v2 날짜 이동 층 (2026-07-12, 무인, 무호출, JSON 1줄)

{"decision":"D48","date":"2026-07-12","action":"specs/perturb_v2.md 사전 등록 커밋 (구현 선행) — v1 상수배 재스케일이 남기는 절대-날짜 지문(제출 연대기 = 준유일 회사 지문, 잔여 name-ID 기제 후보)을 케이스별 결정론 주-단위 이동으로 파괴, 간격 신호 전부 보존","offset_rule":"offset=sign×7×w, w=26+(sha256(case_id+'dateshift-v2')[:4]%53)∈[26,78](182–546일), sign=h[4]&1 — perturb_factor(D8) 동일 스타일; 주 단위=요일 보존(토요일 10-K 인공물 방지)","uniformity":"피평가자가 보는 전 날짜(XBRL start/end/filed·연대기·cutoff_date) 단일 오프셋 → 컷오프 비교·간격 항등 불변; 진짜 cutoff guard는 상류 진짜 날짜에서 작동, 이동은 렌더 시점만; accession은 연도 내장 누출원 → 순차 중립 ID 마스킹 사전 등록","residual_artifacts":"정직 절 — 비표준 회계연도 말·거시 맥락 불일치 수용; 월 단위 이동(요일 파괴)·태그별 노이즈(회계 항등식 파괴) 고려-기각","endpoint":"v2 name-ID 프로브 런(미래 미터링, launch-ready Q-F05) — v1 동결 rate 50%[15/30]·21.9%[7/32] 대비, 동일 문구·동일 k; 호출 산술 = 30+32 = 62 (repo 계수, 추정 아님); 무비용 위생 = no-true-date-leak 문자열 스캔 테스트 즉시 실행","contamination_note":"guided-completion/시간분할 프로빙은 별도 미래 미터링 진단 등록 — logprob min-k% 배포 API 불가, 범위 밖","invariants":"동결 perturbation-v1 출력·발행 수치 불변; 이 세션 미터링 0","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 교란 설계의 단위는 '무엇을 파괴하나'가 아니라 '무엇을 보존하나'다 — 주 단위 균일 이동은 요일·간격·컷오프 관계를 항등으로 보존하기 때문에 남는 차이가 전부 신호 파괴분으로 귀속된다"}

## D49 — WS-6 (F-3) 사전 등록: median-of-3 병기 1차값 (2026-07-12, 무인, 무호출, SPEC ONLY, JSON 1줄)

{"decision":"D49","date":"2026-07-12","action":"specs/draw_k3.md launch-ready 동결 — k=3 draw median을 병기 1차값으로 사전 등록 (이 세션 실행 0). FLAG=50 불변·홀드아웃 k=5 유지·동결 draw-1 발행 수치 불변·dims 재계산 없음(신규 draw는 피평가자 호출만, 채점자 0)","budget_arithmetic":"repo 계수 — wave-1 프레임 30(baseline_table.csv) + wave-2 32(cases_wave2.json) = 62케이스 × 추가 2draw = 124 피평가자 호출; 재사용 옵션(B): wave-1 treatment 8의 커밋된 hardening draw_2/3 산입 시 108 (grades 병합 금지 규약 불변 — median은 통계 병기)","preregistered_output":"flip-rate 표 (draw-1 vs median-of-3 플래그 상이 케이스, tier별, 방향 포함) + median 분리 통계 병기 + per-case 3-draw 밴드","honesty_clause":"temp=0 비결정론(배포 API) — median-of-k는 분산 완화이지 제거 아님, 발행 인용 시 동반 의무","gate":"Q-F06 (소유자 예산 게이트: 124 vs 108 선택 포함)","metered":"0호출 (spec only)","learning_note":"이 판단에서 알아야 할 것: draw 추가의 비용 단위는 호출수가 아니라 '채점자 동반 여부'다 — median은 점수 통계라 채점 0으로 성립하고, 이 구분이 124가 248이 되지 않는 이유다"}

## D50 — WS-7 (F-8) 사전 등록: 교차 패밀리 채점자 스팟체크 (2026-07-12, 무인, 무호출, SPEC ONLY, JSON 1줄)

{"decision":"D50","date":"2026-07-12","action":"specs/cross_grader.md launch-ready 동결 — 피평가자·채점자 동일 패밀리(sonnet-5/fable-5) 공유 편향 위협을 비-Anthropic 채점자 n=20 스팟체크로 경계 (이 세션 실행 0). E4와 같은 배치, 중복 없음 (E4=피평가자 교차, 본건=채점자 교차)","design":"n=20 (n=10 기각 — κ CI가 어떤 결론도 경계 못할 만큼 넓음) · 층화 = tier × 주관 차원 등급(dim2 {0,1,2}·dim4 밴드), 비례 배분+tier 최소 4, seed 20260712 결정론 추출 · 대상 = 주관 2차원만 (dim2 mechanism-match·dim4 evidence-groundedness; dim1은 기계 밴딩 무위험) · 완화 = 루브릭 앵커 원문 그대로 + 피평가자 정체 비공개","metric_prereg":"Cohen's κ 차원별 unweighted — κ≥0.6 양쪽: 결론 유지+교차 일치 각주 · κ<0.6 한쪽이라도: 해당 주관 차원 'grader-dependent' 강등 diff 제안 의무(diff-only, 동결값 불변) · 경계 0.6 단일(Landis-Koch substantial 하한), 중간 판정 없음","grader":"실행 시점 최강 가용 비-Anthropic 모델 — 소유자 선정(Q-F07, API 키·과금 소유자 인프라); 사전 지명 안 함 (시장 상태 종속)","budget":"~20호출 (20샘플×1, 2차원 동시 채점)","discipline":"표본 case_id 목록 채점 전 커밋(사후 교체 봉쇄)·runs/ 신규 디렉토리+전역 MANIFEST·κ 결정론 Python","metered":"0호출 (spec only)","learning_note":"이 판단에서 알아야 할 것: 교차 검증의 대상을 고르는 기준은 '주관성이 들어오는 지점'이다 — dim1처럼 기계 규칙이 닫아둔 차원에 교차 채점을 쓰는 것은 호출 낭비이고, dim2/dim4처럼 판단이 들어오는 차원만이 패밀리 편향의 통로다"}

## D51 — 엔진 판정 사전 등록: specs/ENGINE_DECISION.md (2026-07-13, 무호출, JSON 1줄)

{"decision":"D51","date":"2026-07-13","action":"specs/ENGINE_DECISION.md 사전 등록 커밋 (freeze-commit-then-run — analysis/engine_verdict.py가 git 이력에 존재하기 전) — 도구 경로 엔진 판정(roadmap 1.6)의 3-브랜치 기계 규칙","rule_summary":"순서 고정·전역 완전: (c) 양쪽 중위 lead ≤1분기 → 도구 경로 종료·screener 아카이브 / (a) LLM lead ≥ B3 lead+1 → LLM 엔진·stage-2 활성 / (b) 그 외 전부 → 규칙 엔진·stage-2 제거·LLM 리포트 보조 강등 (b_strict/b_residual 하위 구분은 기록만, 판정 무영향)","thresholds":"LLM p≥50 (동결 FLAG 재사용) · B3 score≥2 (신규 사전 등록 — 단일 지표 과민 근거, 민감도 ≥1/≥3 병기 무가중)","inputs":"E2 동결 계획 산출물 무변경 소비 — e2_trajectories.json 어댑터 스키마 사전 정의 (buyer-metrics 빌더 공유), b3_score 스냅샷별 결정론 재계산","honesty":"(c)/(b) 결과도 그대로 발행 (trust boundary 데이터) · 케이스별 lead 전수 표 동반 (재계산 가능성)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 판정 규칙의 자격은 '전역 완전(total)'이다 — 세 브랜치가 공간을 다 덮지 못하면 남는 틈이 곧 사후 재량의 통로가 되므로, 잔여 지대를 보수 기본값(규칙 엔진)에 명시적으로 귀속시켰다"}

## D52 — launch-ready 미터링 준비: 스모크 러너 + buyer-metrics 자동 채움 (2026-07-13, 무호출, JSON 1줄)

{"decision":"D52","date":"2026-07-13","action":"C1: tools/smoke_rev3.py — FREEZE_REV3 §6-3 래치의 실행 가능 형태 (소유자 행동 = export ANTHROPIC_API_KEY && make smoke). dry-run 매니페스트 30호출(pilot 2케이스×5draw×3arm: 하네스/raw 미핀/raw temp=0) 커밋 — 첫 호출 직전 정지 모드가 계획 전량을 기계 검증 가능하게 고정. C2: analysis/buyer_metrics_build.py + BUYER_METRICS.template.md — E2 완료 후 단일 명령으로 구매자 지표 4종(리드타임 LLM vs B3·FPR@50 CP95·토큰 실측 cost-per-screen·커버리지) 자동 채움, e2_trajectories.json 스키마는 D51과 공유","discipline":"live 모드는 커밋된 매니페스트≠재생성본이면 정지(fail-closed)·하네스 arm 동안 API 키 환경 임시 제거(INVARIant 4)·runs/smoke_rev3 커밋은 전역 MANIFEST 재생성 동반·스모크 결과 커밋 전 E2 발사 금지(§6-3)","tests":"tools/test_smoke_rev3.py 5건(산술 30·temp 핀·결정론·래치 차단·매니페스트 동기) + analysis/test_buyer_metrics.py (합성 E2-형 픽스처)","metered":"0호출 (dry-run은 데이터·네트워크 접근 0)","learning_note":"이 판단에서 알아야 할 것: 미터링 런의 준비 완성도는 '스크립트가 있다'가 아니라 '계획이 커밋되어 실행이 계획과 다르면 스스로 멈춘다'까지다 — 매니페스트 대조가 사후 재량을 봉쇄한다"}

## D53 — EXPLORATORY 등록: wave-1 B3 비대칭 산술 분해 메모 (2026-07-13, 무호출, JSON 1줄)

{"decision":"D53","date":"2026-07-13","action":"analysis/EXPLORATORY_wave1_b3_asymmetry.md — 귀속비 비대칭(w1 0.8947 vs w2 0.1468)의 지표 유병률 분해 (results_b3.json per_case 산술 재배열, 동결 파일 무수정·재계산 0)","scope_guard":"EXPLORATORY/owner-review-required/not-for-publication 배너 — 원인 서술은 사전 등록 문장 밖(소유자 몫)이므로 가설 4건 전부 질문형, 인과 직설법 0. 발행 표면 접촉 0","arithmetic_facts":"w1 최대 단일 기여 = b_ka 10-K/A (실험군 4/8 vs 대조군 2/22) · w2에서 동일 지표 방향 역전 (1/9 vs 6/23) · w2 실험군 5/9 전지표 0","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 탐색 메모가 규율을 지키는 방법은 '표까지만'이다 — 표의 재진술은 산술이고, 표에서 한 발이라도 나가는 문장은 질문형이어야 서사 침범이 아니다"}
## D54 — 게이트 수리: ~/aaer-data 매니페스트에 reference/ 등재 (2026-07-13, 무인, 무호출, JSON 1줄 — 원번호 D51, 병렬 랜딩 재부여)

{"decision":"D54","renumber_note":"원번호 D51 (worktree mkt-integration-2026-07-13, 커밋 3009b5b·60e41ac, 01:02 KST) — main에 D51~D53이 병렬 랜딩(엔진 판정·스모크·EXPLORATORY)하여 병합 시 D54로 재부여. 원 커밋·내용 무변경","original_decision":"D51","date":"2026-07-13","action":"verify_manifest.py 귀속 로직에 reference/ 분기 추가 (REFERENCE_URLS — SEC 원본 URL 2건) + 매니페스트 재생성 — 세션 개시 게이트 점검에서 make verify FAIL 발견 (EXTRA 2건: reference/cik-lookup-data.txt·company_tickers.json)","root_cause":"D36(2026-07-10) tools/gen_fict_names.py가 ~/aaer-data/reference/에 스크린 전용 참조 목록을 정당하게 배치 (data/README.md 기록 완료)했으나 매니페스트 재생성 누락 — 직전 핸드오프의 4게이트 세트가 verify_manifest 대신 pytest를 실측해 미검출","fix_order":"코드+원장 커밋 → --write 재생성 → diff 검사(추가 2건+계수·타임스탬프 외 변화 없음 확인 후 커밋) → 전 게이트 재실측","txt_pitfall":"cik-lookup-data.txt는 .txt지만 로컬 추출 파생물이 아님 — 기존 suffix 규칙이 derived_from을 오기록했을 것이므로 reference/ 분기를 suffix 판정보다 앞에 배치","invariants":"동결 수치·발행 표면 무변경; 기존 매니페스트 항목의 해시 기준선 불변 (diff로 기계 확인)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: fail-closed 게이트는 '어느 게이트 세트를 실측하는가'까지가 규율이다 — 게이트 목록에서 하나를 다른 것으로 바꿔 실측하면 그 자리에 구멍이 생기고, 이번처럼 이틀 뒤에야 발견된다"}

## D55 — WS-SI 사전 등록: B4 비정상 공매도 잔고 기준선 (2026-07-13, 무인, 무호출, JSON 1줄 — 원번호 D52, 병렬 랜딩 재부여)

{"decision":"D55","renumber_note":"원번호 D52 (worktree, 스펙 동결 커밋 4753824 01:11 KST — 구현 a14d746 01:18·계산 287a92a 01:25보다 선행, git log --follow로 검증 가능). main의 D52(스모크/buyer-metrics)와 병렬 충돌하여 병합 시 D55로 재부여. 동결 커밋 해시·순서 증거 무변경","original_decision":"D52","date":"2026-07-13","action":"specs/B4_short_interest.md 사전 등록 커밋 (freeze-commit-then-run — analysis/b4_short_interest.py·screener/ingest/short_interest.py가 git 이력에 존재하기 전, SI 수치 다운로드·계산 전) — 시장 조사 결론(무료 공개 신호의 진짜 경쟁자 = Karpoff/Lou 2010 비정상 공매도 잔고, B3 연대기가 아님)을 구속력 있는 설계 입력으로 구현","data_source_probe":"FINRA Consolidated Short Interest — cdn.finra.org/equity/otcmarket/biweekly/shrt{YYYYMMDD}.csv, 가용 하한 결제일 2017-12-29 (Query API 양측 프로브 실측)·최신 2026-05-29 확인·거래소 상장+OTC 포함; 공표 일정 실측 = 결제+2영업일 마감+약 7일 공표","pit":"LAG=14캘린더일 보수 상수 사전 등록 (settlement+14<=cutoff 진입) — 공표일 실측 대체는 신규 D-엔트리 스펙 개정으로만(Q-M02); 개정판은 최초 공표값 채택(revisionFlag 진단 전용)","metric":"SIR=short/dei:EntityCommonStockSharesOutstanding(payload_v2 PIT, end<=t 신선도 400일 밴드) · aSIR=SIR−trailing 12개월 중앙값(자기 제외, 최소 12보고) · B4_level=aSIR_last 병기 · B4_slope_aug=aSIR_last+slope4(마지막 연속 4보고 OLS) 1차 — 근거: Karpoff/Lou의 발견은 수준이 아니라 꾸준한 상승","eval":"B3 §6 동일 기계 (tie-aware AUC·boot 10k·단측 순열 100k·tier별 비pooled)·SEED_B4=20260713 신규·precision@k 신설(k=ceil(N/10), 농축 표본 비교불가 문구 의무)·동결 LLM/B1/B2/B3 인용만","coverage_honesty":"계산 전 날짜 산술로 기대 커버리지 고정 — wave-1 ~3/30·wave-2 ~4/32(<70% 서술 전용, 헤드라인 금지)·holdout 12/12; 회고 채점만으로 LLM vs B4 판정 성립 tier 없음(wave-1/2 커버리지 미달·holdout 동결 LLM AUC 부재)을 사전 명기 — 무료 신호 벤치마크는 본질적으로 전향 비교","engine_coupling":"비교 성립 조건(커버리지>=70% AND 동결/봉인 성능 존재) 충족되는 모든 미래 시점에서 LLM<=B4이면 E2 평결과 동일 가중치로 엔진 결정 입력 — 완화 금지 조항 포함","e2_contract":"b4_score(ticker,cutoff)->dict 순수 함수, b3_score와 동형; 사용 가능 보고서 없음=None+플래그(E2 루프 보존); 정본은 screener, aaer-evals는 vendor 역방향 스냅샷+PROVENANCE+무결성 테스트","owner_queue":"Q-M01(FINRA ToS)·Q-M02(공표일 실측) 동시 등록","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 기준선 커버리지는 결과가 아니라 설계 입력이다 — 데이터 하한과 cutoff 산술만으로 '이 비교는 회고로는 성립하지 않는다'를 계산 전에 못박아야, 낮은 커버리지가 사후 변명이 아니라 사전 등록된 사실이 된다"}

## D56 — B4 스펙 개정 1: 분모 우선순위 사슬 (2026-07-13, 무인, 무호출, 이력 공개 조건 하 개정, JSON 1줄 — 원번호 D53, 병렬 랜딩 재부여)

{"decision":"D56","renumber_note":"원번호 D53 (worktree, 개정 커밋 7994e2d 01:27 KST — 재실행 efaf4a1 01:28보다 선행). main D53(EXPLORATORY)과 충돌, 병합 시 D56 재부여 (워크트리 자체 정합 노트의 매핑 제안 그대로)","original_decision":"D53","date":"2026-07-13","action":"specs/B4_short_interest.md §13 개정 커밋 (재실행 전) — dei 단일 분모를 4단 우선순위 사슬로 확장 (dei ECSSO → us-gaap CommonStockSharesOutstanding → WAD diluted → WAD basic, 전부 D44 화이트리스트 내 신규 태그 0), 케이스당 단일 소스(시계열 내 혼합 금지), 동일 (end,filed) 중복은 짧은 기간 승리","disclosure":"본 개정은 1차 실행 결과(287a92a)를 본 뒤 작성 — coverage wave1 3/30·wave2 1/32·holdout 7/12(기대 12/12 미달)·holdout AUC 0.1667. 동기는 커버리지 수리: SEC companyfacts가 차원(클래스별) 사실을 평탄화하지 않아 다중 클래스 발행사(HUBG·GNE·UAA·RL·VIASP·VLGEA)에 undimensioned dei 사실이 부재 — §6 사전 등록 기대와의 불일치가 계기. 분모 선택은 방향 중립(부호가 아니라 커버리지 결정)이며 1차 결과는 git 이력 보존","honesty":"가중평균 주식수는 기간 평균 ≠ 시점 잔고 — 케이스 내 일관 사용으로 aSIR(자기 중앙값 차분)에서 수준 편차 상쇄, 한계로 기록. VLGEA는 사슬 적용 후에도 신선 분모 부재 예상(전 소스 stale) — fail-closed 유지","code":"정본 screener 01a4331 → analysis/vendor 재수출(sha 36f7d82a…) + 계약 테스트 5건 추가(우선순위·stale 폴스루·전소스 stale None·tie-break·폴백 e2e)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 실행 후 개정의 정당성은 '무엇을 보고 고쳤는가'의 완전 공개에서 나온다 — 커버리지(설계 결함)를 고치는 개정과 성능(결과 불만)을 고치는 개정은 같은 편집이라도 다른 행위이고, 전자임을 증명하는 유일한 방법은 1차 결과를 먼저 커밋해 두는 것이다"}

## D57 — B4 재실행 결과 확정 (2026-07-13, 무인, 무호출, JSON 1줄 — 원번호 D54, 병렬 랜딩 재부여)

{"decision":"D57","renumber_note":"원번호 D54 (worktree, 커밋 efaf4a1 01:28 KST). main D54(게이트 수리 재부여분)와 충돌, 병합 시 D57 재부여","original_decision":"D54","date":"2026-07-13","action":"D56(원번호 D53) 개정 후 재실행 — analysis/results_b4.json·B4_REPORT.md 확정 커밋","results":{"wave1":"3/30 coverage-limited (서술 전용) — slope-aug AUC 1.0 [1.0,1.0] p=0.333 (1처치 vs 2대조, 수치 자체가 무의미함을 병기)","wave2":"level 4/32·slope-aug 3/32 coverage-limited (서술 전용) — level AUC 0.667, slope-aug 1.0 (1처치)","holdout":"10/12 (83%, 커버리지 바 통과) — slope-aug AUC 0.4762 [0.0,1.0] p=0.250 · level 0.5238 [0.048,1.0] p=0.242 · precision@2 0.5; N=3 처치라 B3와 동일하게 단독 헤드라인 금지"},"interpretation":"사전 등록 §7 그대로 — 비교 성립 tier 없음 (wave-1/2 커버리지 미달, holdout 동결 LLM AUC 부재). LLM vs B4 판정은 전향 무대(E2 스냅샷·sealed 분기)로 이관, 결합 조항 발효 상태","denominator_sources":"holdout 신규 커버 3건 = WAD diluted (HUBG·GNE·VIASP), RL·UAA도 WAD; VLGEA(전 소스 stale)·GRDX(SI 이력 4보고 <12) fail-closed 유지 — D53 예상과 일치","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: '기준선이 우연 수준(holdout AUC≈0.48)'은 B4가 약하다는 증거가 아니다 — N=3 처치·미결(라벨 미확정 4년 창) 홀드아웃에서는 어떤 신호도 판독 불가이며, 이 표의 역할은 판정이 아니라 전향 비교의 기준점 설치다"}

## 병렬 세션 정합 노트 (2026-07-13, 이 브랜치 → main 병합용, JSON 1줄)

{"note":"reconciliation","date":"2026-07-13","context":"본 브랜치(mkt-integration-2026-07-13) 작업 중 main에 병렬 세션(로드맵 운영화 미션, git author chaeryeol)이 D51~D53을 선점 발번 + 본 브랜치 초반 커밋을 병합하며 재부여(f465961: 본 D51→D54·D52→D55). 본 브랜치의 이후 엔트리도 동일 규약으로 재부여 필요","mapping_proposal":{"D53(분모 개정)":"D56","D54(재실행 확정)":"D57","Q-M03(설명가능성 채점)":"Q-M04"},"qm03_resolution":"main의 Q-M03(분모 폴백 스펙 개정 질문, 커밋 93e1237)은 본 브랜치 D53/D54가 후보 (A) 폴백 사다리를 '신규 D-엔트리 사전 등록 후 재실행' 절차 그대로 실행한 것 — 재부여 후 D56/D57을 근거로 RESOLVED 처리 가능. 단, 세션이 소유자 게이트 없이 실행한 판단이므로 소유자가 기각하면 D56/D57 결과 커밋만 revert하면 됨 (동결 수치 무접촉, B4는 신규 병기 산출물)","results_delta":"1차(main 반영분) holdout 7/12 → 개정 후 10/12 (83%, 커버리지 바 통과), slope-aug AUC 0.4762 [0.0,1.0] — 판독 불가(N=3 처치)는 동일, 비교 성립 tier 없음 결론 불변","code_note":"analysis/b4_short_interest.py의 리포트 제목·spec_commit 문자열은 재부여 시 4e850ad 방식(인용 전수 갱신)으로 정합 필요","learning_note":"이 판단에서 알아야 할 것: 공유 저장소에서 두 세션이 같은 원장을 증분 발번하면 충돌은 필연이다 — 원장 엔트리에 자연키(날짜+주제)를 병기해 두면 재부여가 기계적 치환으로 끝난다"}

## D58 — ENGINE_DECISION 개정 1: B4 결합 조항 이행 (2026-07-13, 무호출, E2 실행 전, JSON 1줄)

{"decision":"D58","date":"2026-07-13","action":"specs/ENGINE_DECISION.md §4b 추가 (판정 코드 변경 전 커밋) — B4 스펙 §7 결합 조항(D55, 완화 금지)의 기계 이행: 비교 성립(실험군 B4 커버리지 >=70% AND 동일 데이터 LLM 성능) 시 median_lead_llm<=median_lead_b4 AND auc_llm<=auc_b4 이면 기본 판정 (a)를 (b) b4_dominated로 강등, (b)/(c) 불변","threshold_reuse":"B4 플래그 = slope_aug>0 (FUNNEL §1·프로토콜 §2 기존 등록 재사용, 신설 0) · LLM/B3 임계 불변","fairness":"B4 커버 부분집합에서 LLM 값 짝지어 재계산 (커버리지 편향 차단), 전체군 값 병기","amendment_legality":"D51 §5 '판정 개정은 E2 실행 전에만' 조건 충족 — E2 미실행 상태에서의 개정","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 결합 조항의 이행은 새 재량이 아니라 기존 완화 금지 조항의 상환이다 — D55가 미래를 구속해 두었기 때문에, 이 개정은 선택이 아니라 이행 의무였고 그래서 E2 전에 해야 했다"}

## D59 — RP-17 등록: D56/D57 사후 분모 개정 소유자 분류 판정 패킷 (2026-07-13, 무호출, diff-only, JSON 1줄)

{"decision":"D59","date":"2026-07-13","action":"review_packets/RP-17_denominator_fallback.md 등록 + INDEX 14~17 편입 — D56/D57(사후 분모 개정)의 소유자 분류 판정(기계적 커버리지 결함 vs 분석 변경)을 diff-only 패킷으로 상정. 미션 문면의 RP-16 지정은 D47 보정 언어 diff 선점으로 차번호 RP-17 발행 (번호 규칙 D14 = 생성 순서)","contents":"중립 사건 기술(공백·4단 사슬·양판 전량 델타 holdout AUC 0.1667→0.4762/0.5238 — AUC가 움직였다는 정직 명기)·checkout 기반 무충돌 원복 명령·양측 최강 논거(기계성+역이해관계+선커밋 절차 vs 결과 열람 후 설계+재량 공간 4택 존재)·1문장 권고 상한 준수·CLAUDE.md 거버넌스 3줄(사후 개정 한계·5게이트·단일 작성자) 제안 diff (소유자 서명 시에만 적용)","invariants":"결과·스펙·발행 표면 무변경 — 패킷과 색인만","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 리뷰 패킷의 가치는 권고가 아니라 '기각 비용의 정확한 견적'이다 — 원복이 커밋 1개짜리 checkout임을 명령어로 증명해 두면 소유자의 기각 선택지가 실질이 되고, 그래야 수용 선택도 실질이 된다"}

## D60 — B4 무대 판정 메모: E2 비성립 산술 (2026-07-13, 무호출, 서술적 산술, JSON 1줄)

{"decision":"D60","date":"2026-07-13","action":"analysis/B4_VENUE_MEMO.md 등록 + docs/LAUNCH_SEQUENCE.md 기대치 주석 — 'LLM vs B4 대결이 E2에서 성립하는가'를 동결 그리드(EARLINESS_DESIGN §1)×동결 하한(B4 스펙 §6, 2019-01-27) 날짜 산술로 판정. 규칙 신설·변경 0","verdict":"E2 비성립 — 신규 스냅샷 112개(실험군 48) 중 B4 점수 계산 가능 0개; 약한 하한(2018-01-12)도 8개(KHC 4·GIS 4)뿐이며 전부 trailing 12개월 미달; s0 재사용점 포함 케이스 커버 실험군 1/7(14.3%) < §4b 성립 조건 70% — E2 실행으로도 불변(그리드가 과거로만 자란다)","consequences":"engine_verdict는 b4_comparison.valid=false 자기 기록(설계 정상)·b4_dominated 강등은 E2에서 트리거 불능·대결 유일 무대 = 전향 seal(프로토콜 §5 metric 3·§5b) — 첫 증거 ≈2027-11(2026-11-15 seal+4분기), stage-gate 최초 개방 가능 ≈2028-08; E2 발사 기대값 계산에 무료 신호 해소 편익 계상 금지 (LAUNCH_SEQUENCE 2단계 주석)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 실험의 가치 목록에서 '그 실험이 답하지 않는 질문'을 발사 전에 지워두는 것이 예산 결정의 절반이다 — E2는 뒤로 걷는 설계라 앞으로만 자라는 데이터(2017-12-29 하한)와 절대 만나지 않는다"}

## D61 — B4 무대 메모 로스터 교정 (2026-07-13, 무호출, 판정 불변, JSON 1줄)

{"decision":"D61","date":"2026-07-13","action":"analysis/B4_VENUE_MEMO.md §5 정정 append + 헤드라인 교정 + LAUNCH_SEQUENCE 수치 갱신 — D60이 EARLINESS_DESIGN §2(wave-1 7케이스, 구판)로 계산했으나 E2 지배 문서는 EARLINESS_PLAN §1(detected 로스터: wave-1 6 + wave-2 7, MON 제외)","corrected_arithmetic":"XBRL 제출 그리드 + 최소 요건(잔존>=6·10-K>=1) 적용 — 신규 스냅샷 146(구 112) 중 계산 가능 3(구 0, 전부 UAA 2019-08-02/05-10/02-26)·s0 포함 케이스 커버 2/13=15.4%(구 1/7=14.3%); WFT는 XBRL 4건뿐이라 스냅샷 0(MON과 동일 경계 사유, PLAN 규칙의 기계적 귀결)","verdict":"불변 — 비교 비성립, §3 귀결 전부 유지; E2 예산 산술도 이 로스터로 갱신됨(E2_PREFLIGHT 참조)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 같은 실험에 설계 문서와 사전 등록 계획이 둘 다 있으면 산술은 반드시 '지배 문서'(freeze-then-run 대상인 쪽)에서 파생해야 한다 — 구판 설계로 계산한 수치는 방향이 같아도 교정 대상이다"}

## D62 — Q-F01 해소: HUBG 하위 제출 파일 캐시 + payload-v2 커버리지 완결 (2026-07-13, 무호출·네트워크 1건, JSON 1줄)

{"decision":"D62","date":"2026-07-13","action":"data.sec.gov/submissions/CIK0000940942-submissions-001.json fetch (UA 규약 'chaeper …', 547 제출, 1996-05-15~2007-11-13) → ~/aaer-data/HUBG/edgar/ 캐시 → payload_v2 전체 재생성(결정론) — diff는 case_71.json(+433줄, pre-2008 8-K 항목 복원)과 COVERAGE.json(partial 1→0, 82/82 완전)만","non_impact_proof":"HUBG b3_score(cutoff 2026-02-04, W4/W8) 재계산 == results_b3.json 동결 per_case 완전 일치 (지표 6종 전부) — 1996~2007 제출은 B3 어떤 창(2018+)과도 비교차; B4는 submissions 미소비·라벨링(D46) neighborhood는 2026 — 비영향. reproduce/blindness 게이트가 독립 확증","manifests":"aaer_data_manifest 512 files 재생성 + runs/MANIFEST.sha256 재생성 (diagnostics 갱신분)","queue":"Q-F01 RESOLVED 표기","metered":"LLM 0호출; 네트워크 = SEC 공개 파일 1건","learning_note":"이 판단에서 알아야 할 것: 커버리지 구멍을 메울 때의 증명 부담은 '메웠다'가 아니라 '다른 무엇도 안 움직였다'다 — 전체 재생성 diff 범위(2파일)와 동결값 기계 대조가 그 증명이고, 부분 재실행은 오히려 그 증명을 못 만든다"}

## D63 — Q-M02 조사 완결: 과거 공표일 입수 가능 (2026-07-13, 무호출·아카이브 조회만, 스펙 무변경, JSON 1줄)

{"decision":"D63","date":"2026-07-13","action":"analysis/DISSEMINATION_DATES_MEMO.md 등록 — FINRA 연도별 일정표(현행 Publication Date 열, 2020년대 전신 명칭 Exchange Receipt Date)가 Wayback 스냅샷(2019~2026 실측 목록)에서 프로그램적으로 복원 가능함을 2020-07-18 스냅샷 파싱으로 검증 (26행, 예시 지연 +11~12일 ≤ LAG 14 — 상수의 표본 내 보수성 확인)","open_edge":"2018년분 스냅샷 미확인 — 구 URL CDX 탐색이 구현 1단계; 미발견 시 혼합 테이블(2018만 LAG 유지)안 명시","conversion":"Q-M02 OPEN → 구현 GO 게이트 (1세션 분량 계획 §3: 스냅샷 파싱→매핑 데이터 커밋→B4 스펙 §2 개정 D-엔트리→D56/D57 규율 재실행); 이 세션 스펙·코드 변경 0","metered":"LLM 0호출; 네트워크 = finra.org 현행 페이지 + web.archive.org CDX/스냅샷 (공개 아카이브)","learning_note":"이 판단에서 알아야 할 것: '무료로 구할 수 없다'고 등록된 데이터의 절반은 '현행 페이지에 없다'일 뿐이다 — 규제기관 일정표처럼 매년 덮어써지는 표는 웹 아카이브가 사실상의 공식 사료고, 파싱 검증 표본 1개가 계획을 추측에서 견적으로 바꾼다"}

## D64 — RP-18 등록: D53 비대칭 메모 발행 패킷 (2026-07-13, 무호출, diff-only, 게시 0, JSON 1줄)

{"decision":"D64","date":"2026-07-13","action":"review_packets/RP-18_asymmetry_memo_publication.md 등록 — D53 EXPLORATORY(wave-1 B3 비대칭 산술 분해)의 발행 결정(소유자 몫)에 대해 'yes 비용 0' 준비: 게시 가능 완성 영문 텍스트(산술 표 그대로·가설 전건 표지 유지·한계 1줄)·배치 2안(A=Issue 1 부록 코멘트 권장 1문장 근거, B=신규 짧은 Issue)·게시 명령·게시 후 후속 3건(D-엔트리·헤더 주석·lint 편입)","framing_guard":"라벨 순환성 2문장은 가설 표지 강제 — '유명 프라우드는 정정했기 때문에 유명할 수 있다(선별이지 탐지가 아닐 수 있다)'+'wave-2 역전은 정정 대부분이 양성 little-r이라는 기저율과 정합' — 인과 주장 0, lint 사전 스캔 통과","metered":"0호출, 게시 0","learning_note":"이 판단에서 알아야 할 것: 소유자 결정 항목의 준비물은 '권장'이 아니라 '실행 비용의 소거'다 — 완성 텍스트+명령 1줄이면 yes도 no도 1분 결정이 되고, 그래야 결정이 미뤄지지 않는다"}

## D65 — EARLINESS_PLAN 드리프트 주석 2건 (2026-07-13, 무호출, E2 출력 0 시점, 본문 무수정, JSON 1줄)

{"decision":"D65","date":"2026-07-13","action":"analysis/EARLINESS_PLAN.md 말미에 DRIFT ANNOTATION 블록 append (원문 보존·재작성 0) — E2_PREFLIGHT §4가 플래그한 동결 계획 내부 드리프트 2건의 구속력 정리","annotation_1":"§5 '실험군 ~7–8사'는 detection 확정 전 추정 — §1 규칙의 기계 출력(13케이스, cutoff 병기 열거)이 지배; 로스터 소속≠스냅샷 가용(WFT 0, 최소 요건의 기계적 귀결) 명기","annotation_2":"§5 '채점자 동수'는 E2 비작동 — §3 지표가 피평가자 원점수만 소비(D49 동일 논리), 기록 예산 146 evaluatee+0 grader; 동수 해석은 292>cap 160으로 문구 자체 모순. 지출 축소 방향만, 지표·임계·판정 규칙 무변경","timing_proof":"runs/e2/ 부재(출력 0) 시점 커밋 — 결과를 보기 전의 주석임을 저장소 상태로 증명","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 동결 문서의 내부 모순은 '고치면' 동결이 깨지고 '방치하면' 실행 세션이 재량으로 읽는다 — 제3의 길은 어느 문구가 지배하는지의 주석을 결과 존재 전에 박는 것이고, 그 주석의 정당성은 전적으로 타이밍에서 나온다"}

## D66 — E2 스냅샷 케이스 생성 완결 (2026-07-13, 무호출, 결정론 검증, JSON 1줄)

{"decision":"D66","date":"2026-07-13","action":"pipeline/e2_generate_cases.py (구현 선행 커밋) 실행 → data/e2/ 156파일 — 스냅샷 기록 146·러너 배치 8(s1~s8: 19/19/19/18/18/18/18/17)·registry_e2·E2_MANIFEST. 로스터는 PLAN §1 규칙 기계 출력(하드코딩 0, 테스트 강제): treatment 13 + control 8, MON·CSC·BRX 규칙 자동 탈락","verification":"이중 전체 생성 바이트 동일(결정론) · 매니페스트 회계 146 buildable+22 grid_ineligible=168행 전수·build_failed 0 · 기록 파일 수==매니페스트==사전 산술(E2_PREFLIGHT §4) 정확 일치 · 문서 단위 실제 cutoff_guard 경유(accession 교차검증 포함)+독립 anti-leak 이중 검증 전건 통과","id_design":"러너 배치 case_id=기저 ID 유지 — perturb_factor 동일-k(PLAN §2 명문) 보존; case_NN_s{j} 정체성은 기록·레지스트리·매니페스트 보유, 출력은 runs/e2/s{j}/ 격리. e2 메타는 사이드카에만(build_payload 필드 복사 누출 방지)","b4_measured":"동반 b4 계산 가능 실측 7/146(UAA s1–4·KHC s1·GIS s1–2) — D61 추정 3/146은 보수 하한의 과소집계, 케이스 커버 2/13·판정 불변 (메모 §5 후기)","adapter_convention":"quarters_to_revelation = floor((기저컷오프+1일 − 스냅샷컷오프)/91일) — 러너 후처리 어댑터의 결정론 정의(신규 지표 아님, PLAN §3 't=폭로까지 분기'의 이산화)","budget_of_record":"146 evaluatee + 0 grader (D65)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 보수 하한으로 세운 추정은 실측 코드가 돌자마자 갱신 대상이다 — 추정과 실측이 다를 때 고칠 것은 판정이 아니라 어느 쪽이 정본인지의 선언이고, 여기서 정본은 언제나 커밋된 기록 파일이다"}

## D67 — E2 실행 하네스: 안전 레일 + 후처리 자동화 (2026-07-13, 무호출, JSON 1줄)

{"decision":"D67","date":"2026-07-13","action":"tools/e2_runner.py + 테스트 6건 + runner_api 원자적 기록 패치(tmp→replace 2줄, D38 미배선 스캐폴드 — 크래시 부분 파일의 완료 오인 방지) — 146호출 세션의 레일을 발사 전에 구축","rails":"① 매니페스트 드리프트 정지(커밋 E2_MANIFEST≠재생성 산술, smoke_rev3 패턴) ② 지출 가드 이중(완료+잔여==buildable 회계 + 런타임 시도>잔여 즉시 정지) ③ 온도 핀 상수 0.0(플래그 부재가 계약, FREEZE_REV3) ④ INVARIANT 4 키 스크럽(출력 직후 스캔, 발견 시 삭제+정지) ⑤ 멱등 재개(output_is_valid 스킵+원자 기록 — 크래시 시뮬 테스트: 중복 0·갭 0)","postrun":"전 스냅샷 완료 시 자동 — 어댑터(q=floor(days/91)·s0=동결 perturbed 재사용) → e2_trajectories.json → 실제 engine_verdict → runs/e2/E2_SUMMARY.md (b4_comparison.valid=false 자기 기록 라인 포함, 합성 출력 종단 테스트로 검증); buyer_metrics는 가격 인자 안내","placement":"tools/ 소재 — 생성기와 동일 사유(채점측 오케스트레이션, pipeline/ 피평가자 경계 보존; 가드 우회 정적 스캔이 이 경계를 기계 강제함을 이번 세션 실측)","dry_run":"실데이터 dry-run 실측 — 드리프트 통과·계획 146·완료 0·temp 0.0","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 밤새 도는 미터링 런의 레일은 '재개했을 때 한 푼도 다시 안 쓴다'가 전부고, 그 보증은 스킵 로직이 아니라 원자적 기록에서 나온다 — 부분 파일이 valid로 읽히는 순간 스킵은 갭을 만든다"}

## D68 — freeze 개정 #4: E2·금야 발사분 하네스 경로 확정 (2026-07-13 야간, 무호출, 배선 코드 선행 커밋, JSON 1줄)

{"decision":"D68","date":"2026-07-13","action":"docs/FREEZE_REV4_HARNESS_E2.md 커밋 (배선 코드 존재 전 — freeze-commit-then-run) — E2 및 금야 발사분(P0 E2 146·P2 E4 ~20·P3 Q-F05 62·P4 Q-F06-B 108·조건부 P5 ~32)을 동결 구독 하네스 경로(cli_client, freeze 개정 #2)로 확정. 서명 = (owner, 2026-07-13, written overnight authorization — this mission's prompt, §A-1)","rationale_verbatim":"(a) path-consistency — LLM-vs-B3 리드타임 판정은 전 동결 tier와 같은 방식으로 생산된 LLM 점수를 비교 (b) zero marginal cost (c) freeze rev #3 (raw API) DEFERRED, not revoked — 개정 #3과 스모크 래치는 raw 경로 실사용 시점으로 한 몸 이동","honest_costs":"L-2(하네스 system-reminder 주입, currentDate vs PIT 프레이밍 포함) E2에 상속 — 모든 E2 발행 표면에 상속 한계로 명기 의무; L-3 미해소(하네스 온도 핀 부재 — e2_runner TEMPERATURE_PIN assert는 하네스 모드 N/A, 해석 분해능 한계 = E5 §7 draw-노이즈 밴드)","queue_updates":"Q-F05 RESOLVED(A-변형: 금야 창)·Q-F06 RESOLVED(옵션 B: 108)·Q-M02 구현 GO(A-8) — 전부 동일 서면 승인 인용; Q-M05 신규(미션 프롬프트 §5 절단 — B-1…B-10 목록 미도달, 추측 실행 안 함)","j14_override":"J14 실행층 주의(quota 소진 비목표)는 금야 한정 소유자 오버라이드 (하드 캡 380호출) — 익일 원상 복귀","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 경로 일관성은 비교 가능성의 전제 조건이다 — 측정 경로를 바꾼 채 리드타임을 비교하면 경로 효과와 능력 효과가 분리 불능이 되므로, raw 경로 이행은 '비교가 끝난 뒤'로 미루는 것이 개정이 아니라 보존이다"}

## D69 — e2_runner --client harness 배선 (2026-07-13 야간, 무호출, 개정 #4 이행, JSON 1줄)

{"decision":"D69","date":"2026-07-13","action":"tools/e2_runner.py에 --client {api,harness} 추가 (기본 api = D67 원형 보존) — harness 모드는 run_one을 동결 runner.run_case(entry, perturb=True, out_dir, log_dir)로 위임 (runner.py 무수정, §8-3 소진 없음; 전 발행 tier와 동일 cli_client 경로). 가드 교체: assert_raw_api_approved 스킵 → assert_no_metered_credentials + require_clean_tree (runner.py main 동형). RateLimitedError를 exit 3 + 재개 명령으로 정리 (멱등 재개)","rails_unchanged":"매니페스트 드리프트 정지·지출 가드 이중·페이로드 금지 마커(runner.run_case→cli_client.call_model 경유)·키 스크럽·멱등 재개(output_is_valid) 전부 D67 그대로; TEMPERATURE_PIN assert는 client==api 한정 (하네스 N/A — 개정 #4 §3 L-3)","tests":"+7 (모드 선택 디스패치·동결 runner 위임 인자 계약·키 존재 차단·raw 래치 비참조+clean-tree 호출·api 래치 유지·온도 핀 N/A 비대칭·crash-resume 멱등 harness 명시) — 총 14","gates":"pytest 160 passed · reproduce 100/100 · lint PASS · blindness PASS · manifest PASS (512 files); 실데이터 dry-run 양 모드 146/0/146 정상","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 경로 스위치의 안전은 '새 경로 검증'이 아니라 '기존 경로 무접촉 증명'이 절반이다 — 기본값을 원형(api)에 두고 harness를 opt-in으로 만들면, 스위치 자체가 동결 계약을 건드리지 않았음이 인자 하나로 증명된다"}

## D70 — E2 로그 충돌 결함 실사격 발견·해소 (2026-07-13 야간, 5호출 후 정지·수리·재발사, JSON 1줄)

{"decision":"D70","date":"2026-07-13","action":"E2 발사 5호출 시점 로그 감사에서 D67 잠복 결함 발견 — 러너 log_name이 기저 case_id로만 구성(evaluatee_{variant}_{cid})되어 같은 케이스의 s1..s8 스냅샷 호출 로그가 상호 덮어씀 (출력 JSON은 runs/e2/s{j}/ 격리라 무손상). 방치 시 146중 ~125개 SR 11-7 호출 기록 소실 + P1 buyer_metrics 토큰 회계 왜곡 → 즉시 정지·수리·재발사","fix":"run_one이 제어하는 log_dir을 스냅샷별 s{j} 하위로 분기 (_snap_log_dir, 하네스·raw 양 경로) — 동결 runner.py 무수정 (§8-3 보존). 테스트 +1 (양 모드 스냅샷 간 로그 경로 충돌 0), 기존 위임 테스트 갱신","spend_accounting":"정지 시점 5호출 완료(case_61 s1–s5, 전건 스키마 유효 — 재지출 0, 멱등 재개가 스킵) · 손실 = 호출 로그 4건(s1–s4분 덮어씀, SURVIVOR-of-5 개명 보존) — 복구는 출력 삭제+재추첨뿐이라 no-double-spend 레일·재량 재추첨 금지에 따라 기각, buyer_metrics는 142/146 로그 커버리지로 계산+갭 주석 의무","raw_path_note":"동일 충돌이 runner_api 경로에도 잠복(evaluatee_api_{cid}) — 본 수리가 양 경로 동시 해소, 개정 #3 재개 시 재검증 불요","gates":"pytest 161 passed (전 스위트) — 재발사 전 실측","metered":"5호출 (누계 5/380)","learning_note":"이 판단에서 알아야 할 것: dry-run이 검증 못 하는 유일한 층은 '실호출이 남기는 기록'이다 — 첫 실사격 직후 산출물이 아니라 로그 디렉토리를 열어보는 것이 밤새 런의 두 번째 관문이고, 이번엔 5호출 값으로 125건 소실을 샀다"}

## D71 — E2 어댑터 s0 가용성 결함 사전 해소: 대조군 j=0 llm_p null 규약 (2026-07-13 야간, 무호출, 후처리 산출물 존재 전 커밋, JSON 1줄)

{"decision":"D71","date":"2026-07-13","action":"E2 진행 중(호출 ~13/146) 사전 감사에서 D66 어댑터 규약의 잠복 결함 발견 — 's0=동결 perturbed 점수 재사용'이 대조군에 불성립: E2 대조군(RP-01 v1 대조군 7건 buildable, 전건 wave1)은 perturbed 프레임 동결 점수가 없다 (v1 perturbed 채점은 실험군 8건만; runs/perturbed 실측). 방치 시 후처리가 146호출 완료 직후 FileNotFoundError로 크래시 (D67 테스트가 _s0_score를 몽키패치해 정확히 이 구멍을 가림)","fix":"specs/ENGINE_DECISION.md §3 주석 append (후처리 산출물 부재 시점 커밋 — 타이밍 증거) + 어댑터 _s0_score 파일 부재→None·_s0_llm_unavailable 목록 기록 + engine_verdict j=0 AUC 지표별 null 케이스 제외·빈 그룹시 AUC null+플래그·(b) 하위 라벨 b_auc_unavailable fail-closed","frame_mixing_rejected":"대조군 j=0에 원본 프레임(runs/main) 점수 대입은 기각 — perturbed(익명) 실험군 vs 원본(정체 가시) 대조군의 프레임 혼합은 편향 방향을 서명할 수 없다","verdict_invariance":"§4 브랜치 규칙은 실험군 median lead만 소비 — 본 규약은 판정 입력을 바꾸지 않음 (b3 j=0 AUC는 결정론 재계산이라 양 군 정상). 잃는 것 = LLM j=0 AUC 병기·하위 라벨 선명도 → 해소 옵션 7호출을 Q-M06 등록 (기본 미실행)","tests":"+5 (verdict 3: null AUC fail-closed·하위 라벨·부분 커버 플래그 / 어댑터 2: null 통과 종단·파일 부재 None) — 총 32+15","mid_run_commit_note":"본 커밋은 E2 호출 루프 진행 중 발생 — 루프는 launch 시점 코드로 실행되므로 무영향; 완료 시점 postrun이 구 코드로 크래시하면 --postrun-only 재실행이 신 코드로 완주 (지출 0)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 테스트에서 몽키패치한 함수 목록이 곧 '실데이터로 한 번도 검증 안 된 경로' 목록이다 — 밤새 런의 후처리처럼 '지출 후에만 실행되는 코드'는 발사 전에 실데이터 입력 존재성부터 전수 확인해야 하고, 그 확인은 5분이고 크래시는 146호출 뒤다"}

## D72 — Q-M02 구현 1/2: 공표일 실측 재구성 (도구+데이터+아카이브, b4 의미론 무접촉) (2026-07-13, 무호출·네트워크 web.archive.org만, JSON 1줄)

{"decision":"D72","date":"2026-07-13","action":"tools/dissemination_schedules.py (fetch/build 2명령, 테스트 10) → ~/aaer-data/finra_schedules/ 스냅샷 13개 아카이브(체크섬 로그) → data/finra_dissemination/dissemination_dates.json (결제일→공표일 223행, 2017-09-29~2026-12-31). D63 열린 모서리 해소: 2018년분은 구 URL(industry/short-interest/short-interest-reporting-due-dates)의 20180111 스냅샷이 2017 잔여表+2018 전체表를 동시 보유 — B4 하한 결제일 2017-12-29의 공표일 2018-01-10(+12일) 실측 확보","validation":"4중 — 요일명 체크섬(연도 추론 오류 기계 검출)·중복 연도 스냅샷 cross-check·산술 가드(0<지연≤30일)·SI 아카이브 79결제일 전수 매핑 대조(구멍=정지). 독립 이중 fetch(스크래치 curl본 vs 도구 재fetch본 — archive.org 배너 재작성으로 바이트 상이)에서 매핑 완전 동일 — 파서 강건성 실증","discrepancy_rules":"FINRA 원천 불일치 3건 전부 사전 등록 규칙으로 해소(재량 0): ①2025-04-15 요일 오탈(후속 스냅샷이 요일만 교정 — self-consistent 다수결) ②2021-12-15 연중 개정(공표 12-24 휴장일→12-27, 최신 스냅샷 우선) ③2026-12-31 전 스냅샷 동일 요일 오탈(날짜 만장일치+due+7 패턴 채택). 그 외 유형 = 빌드 정지","headline_finding":"실측 지연 분포 9~12일 — LAG=14 상수의 표본 내 보수성이 D63 표본 2행에서 223행 전수로 확장 확인","scope_boundary":"본 커밋은 b4 의미론 무접촉 — si_core·b4_short_interest·스펙 §2 불변 (LAG=14 여전히 유효). 스펙 §14 개정+정본 배선+재실행은 P1(E2 후처리) 뒤 별도 커밋 (e2_trajectories s0 b4값의 D66 규칙 일관성 보존 — 관할 명시는 §14에 포함 예정)","manifest":"verify_manifest.py에 finra_schedules/ 귀속 분기 추가(D54 reference/ 패턴 — 정본 URL표=도구 SNAPSHOTS 사전 등록 목록) — aaer-data 매니페스트 526 files 재생성","boundary_commit":"E2 진행 중 경계 커밋 — runs/e2 부분 출력+호출 로그+runs/MANIFEST 동반 (E3 draw-경계 선례; blindness 스캔 a–c 신규 출력 전건 통과 실측)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 아카이브 재구성 데이터의 신뢰는 '한 번 잘 파싱했다'가 아니라 '독립 사본 두 벌이 같은 표를 낸다'에서 나온다 — 바이트가 다른데 의미가 같을 때에만 파서가 컨텐츠를 읽은 것이지 우연을 읽은 게 아니다"}

## D73 — Q-F05 발사 전 배선: probe_runner --v2-dateshift + 위생 스캔 (2026-07-13, 무호출, freeze-commit-then-run, JSON 1줄)

{"decision":"D73","date":"2026-07-13","action":"pipeline/probe_runner.py에 --v2-dateshift 추가 (recognition 렌더 직전 date_shift.shift_payload — 스펙 §3 순서 계약 그대로: 컷오프 가드·build_payload는 상류 진짜 날짜에서 완료) + 로그 명명 _v2ds 격리(D70 교훈 선제 적용) + tools/v2ds_hygiene_scan.py + analysis/name_probes_v2ds.py (동결 name_match 규칙, 사전 등록 기준선 wave-1 50%[15/30]·wave-2 21.9%[7/32] 하드코딩)","hygiene_upgrade":"사전 등록 전제 ii의 실측 상향 — 이진 충돌 분기(offset ∈ 쌍차)가 무의미함을 62/62 실측(페이로드당 수백 날짜가 ±546일 내 7배수 쌍차를 전부 덮음): 스펙 의도('설명 없는 원본 문자열 생존 금지')를 상위 호환으로 이행 — ①필드 단위 이동 검증 전 케이스 무분기 ②no-leak 스캔+양성 충돌 회계(생존 문자열−offset ∈ 원본 날짜 집합이어야 — 미설명 생존=FAIL) ③offset §2 계약(7배수·[182,546]) 확인. 실행 62/62 PASS·양성 충돌 5,626건 회계·미설명 생존 0·accession 생존 0 — HYGIENE_REPORT.json 커밋","tests":"+2 (v2ds 렌더 이동+accession 마스킹+로그 격리 · 기본 off v1 렌더/명명 불변) — 전 스위트 178","launch_ready":"발사 3연 명령: probe_runner --recognition --v2-dateshift × {scoring/perturbed_cases.json → probe_results_v2ds_wave1, data/evaluatee/cases_v2.json → 동일 루트, data/evaluatee/cases_wave2.json → probe_results_v2ds_wave2} = 8+22+32=62호출 (로스터 산술 사전 검증)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 사전 등록된 검사가 실측에서 무의미해지면(전건 충돌) 답은 검사 완화가 아니라 검사 강화다 — 등록 문면의 의도를 상위 호환으로 이행하고 그 사실을 기록하면, 등록의 구속력과 검사의 실효성이 둘 다 산다"}

## D74 — E4 발사 전 배선: 교차모델 러너+분석 (2026-07-13, 무호출, freeze-commit-then-run, JSON 1줄)

{"decision":"D74","date":"2026-07-13","action":"tools/e4_runner.py + analysis/e4_crossmodel.py — CROSSMODEL_PLAN(사전 등록) 이행체. 로스터 18 확정(§1 문면→case_id 해석: 홀드아웃 case_73/71/72 + wave-2 case_44/61/52/49/60/65[ADAM·CGI·CSC·IOVA·MDXG·WFT] + E1 대조군 hc_05/07/03/04/08/02/01/09/06 — §4 순서·그룹 내 ticker 알파벳), 프레임 = 전 18건 원 채점과 동일 original (runs/{holdout/scores,holdout/controls/scores,wave2/scores} run_id 'original-*-r1' 실측 근거)","model_swap_mechanism":"동결 runner.run_case 그대로 사용, 모듈 전역 EVALUATEE_MODEL만 실행 시점 claude-opus-4-8로 교체 — 요청 모델·서빙 핀 검증·로그가 일관 교체되고 runner.py 파일 무수정(§8-3); 시스템 프롬프트·스키마·격리 플래그 완전 동일(PLAN §2)","analysis":"Spearman ρ(동결 stats)·플래그(p≥50) 일치율·Cohen κ·per-case 표+불일치 열거 — EXPLORATORY 배너·주장 상한('순위 중첩도' 초과 금지·truth 없음) JSON/MD에 하드코딩","guards":"assert_no_metered_credentials+require_clean_tree(개정 #4)·지출 가드(잔여>18 정지)·멱등 skip·RateLimitedError exit 3·--only 케이스 경계 실행(PLAN §4 커밋 규율)","tests":"+3 (로스터 산술·순서·중복 0 / case_id 전건 해석 / 모델 핀 사전 등록) · dry-run 18/0/18","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: '모델만 바꾼다'의 기계 보증은 코드 복제가 아니라 동결 경로 재사용+최소 치환이다 — 복제본은 다음 날부터 드리프트하고, 전역 치환 1점은 핀 검증이 치환 사실 자체를 호출마다 기록한다"}

## D75 — Q-F06-B 발사 전 배선: median-of-3 병기 분석기 (2026-07-13, 무호출, freeze-commit-then-run, JSON 1줄)

{"decision":"D75","date":"2026-07-13","action":"analysis/draw_k3_analysis.py — specs/draw_k3.md §3 사전 등록 산출물의 이행체 (flip-rate 표 + median-of-3 분리 통계 병기 + per-case min–max 밴드). draw 소스 케이스별 발행 프레임 복제 실측 근거 명기: w1 treatment 8 = draw-1 runs/perturbed + hardening draw_2/3 재사용(옵션 B) · w1 control 22 = draw-1 rp09 original + 신규 draw · wave-2 32 = draw-1 wave2/scores original + 신규 draw","launch_commands":"runner.py 4연 (cases_v2.json×draw_2/3 → runs/draw_k3/w1_controls, cases_wave2.json×draw_2/3 → runs/draw_k3/wave2) = (22+32)×2 = 108호출 — 동결 러너 무변경 그대로, 멱등","invariants":"동결 draw-1 발행 수치 불변·grade 병합 금지(dims=draw-1 유지)·temp=0 비결정론 단서 하드코딩(발행 인용 시 동반 의무)·SEED_K3=20260713","tests":"+1 (tier_block flip 방향·병기 통계)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: '재사용 옵션'의 정당성은 프레임 동일성 실측에서 나온다 — hardening draw_2/3이 perturbed고 발행 draw-1도 perturbed임을 run_id로 확인했기에 8케이스 16호출 절약이 통계 왜곡이 아니라 산술이 된다"}

## D76 — Q-M02 구현 2a/2: 정본·벤더 dissemination_map 파라미터 (기본 무변경) (2026-07-13, 무호출, JSON 1줄)

{"decision":"D76","date":"2026-07-13","action":"screener ingest/short_interest.py에 si_series/b4_from_facts 선택 파라미터 dissemination_map({결제일: 공표일}) 추가 — 커버 결제일은 실측 공표일 ≤ cutoff, 미커버는 t+LAG 폴백. 기본 None = 현행 동작 완전 동일 (회귀 테스트로 기계 증명). screener 커밋 f1db861 (+5 테스트, 102 passed) → analysis/vendor 재수출 + PROVENANCE sha 갱신 (94c948b2…)","behavior_boundary":"이 커밋 시점에 aaer-evals의 어떤 소비자도 map을 전달하지 않는다 — b4_short_interest.py 무변경, E2 postrun s0 b4값은 D66 규칙(LAG=14) 그대로. 스펙 §14 append + 소비자 배선 + 재실행 = P1(E2 후처리) 완료 후 별도 커밋 (freeze-commit-then-run: 개정이 재실행 결과보다 선행하는 순서는 그 커밋에서 성립)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 능력 추가와 행동 변경을 커밋 단위로 분리하면 각 커밋의 증명 부담이 절반이 된다 — '이 커밋은 아무 행동도 안 바꿈'은 회귀 테스트 하나로 끝나고, '행동 변경'은 스펙 개정과 함께 도착해 타임스탬프가 깔끔해진다"}

## D78 — Q-M02 구현 2b/2: §14 소비자 배선 (재실행 전 커밋) (2026-07-13, 무호출, JSON 1줄)

{"decision":"D78","date":"2026-07-13","action":"specs/B4_short_interest.md §14 개정(D77, 커밋 7a12bb8 — 본 배선·재실행보다 선행) 이행 — analysis/b4_short_interest.py가 data/finra_dissemination 매핑을 모듈 로드(부재=즉시 예외)하고 b4_score 기본 인자로 전달; results_b4 메타에 dissemination 블록·리포트 헤더 갱신; SPEC_AMENDMENTS에 (§14, D77, 7a12bb8) 등재","e2_jurisdiction":"§14 관할 명시 조항의 기계 이행 — e2_runner 어댑터 s0 b4 호출에 dissemination_map=None 명시 (D66 규칙 LAG=14 동결, 사이드카와 일관). 진행 중 E2 프로세스는 구 코드로 실행 중이므로 무영향; 후처리는 --postrun-only가 신 코드로 수행","tests":"+2 (map 배관 기본/None 분기 · 아카이브 79결제일 소비자측 전수 커버) — 전 스위트 185","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: '이후부터 적용'이라는 관할 조항은 문서만으로는 안 지켜진다 — 구 규칙을 쓰는 호출부에 명시적 인자(map=None)로 못박아야 리팩토링 한 번에도 규칙 경계가 살아남는다"}

## D79 — §14 재실행 결과 확정 (2026-07-13, 무호출, JSON 1줄)

{"decision":"D79","date":"2026-07-13","action":"D77(스펙 7a12bb8)·D78(배선 09455a0) 후 재실행 — analysis/results_b4.json·B4_REPORT.md 확정. 1차(LAG=14, D57 확정본)는 git 이력 보존","delta_vs_D57":"wave-1/wave-2 per-case 변화 0건 (컷오프가 과거라 경계 보고서 비접촉 — 사전 예상 그대로). holdout per-case 변화 11건 = 결제일 2026-02-27 보고서(실측 공표 +11일)가 GRDX·UTL·VIASP 창에 추가 편입 (last_settlement 02-13→02-27·trailing 계수 +1·점수 3~4째 자리 이동). 헤드라인 전부 불변: coverage 3tier 동일(3/30·3-4/32·10/12)·AUC 동일(slope-aug 0.4762·level 0.5238)·precision@2 동일(0.5, 동일 순위)·slope-aug perm p 0.250→0.242 (미세)","verdict":"해석 불변 — 비교 성립 tier 없음 (wave-1/2 커버리지 미달·holdout 동결 LLM AUC 부재), 결합 조항 발효 상태 유지. §14 대체의 실측 효과 = '경계 보고서 편입 정밀화'가 수치로 확인되고 판정은 흔들리지 않음 — 정확히 스펙 §14가 예고한 방향","correction_note":"D78 원장 문면의 '전 스위트 185'는 오기 — 실측 184 (본 엔트리로 정정)","gates":"pytest 184 · reproduce 100/100 · lint PASS (재실행 직전 실측; blindness/manifest는 E2 진행 중 경계 규약)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 보수 상수를 실측으로 바꾸는 개정의 성공 기준은 '수치가 좋아졌다'가 아니라 '바뀐 것이 정확히 예고된 것뿐이다'이다 — 경계 편입 3건과 4째 자리 이동만 남기고 헤드라인이 전부 제자리면, 그 개정은 완화가 아니라 정밀화였음이 증명된 것"}

## D80 — 발사 순서 라이브 개정 + P2(E4) 발사 (2026-07-13, 소유자 실시간 지시, JSON 1줄)

{"decision":"D80","date":"2026-07-13","action":"소유자 실시간 지시('keep going without stopping' + P2·P3 명시 실행 지시)로 야간 미션 §3의 엄격 순차 게이트를 개정 — E2 진행 중(77/146) E4를 병행 발사. 동시 호출 2로 제한(레이트 리밋 보호): E4 완료 후 Q-F05 순차. P1은 물리 의존(전 146 출력 필요)이라 불변","launch":"tools/e4_runner.py --execute --only <cid> × 18 (PLAN §4 케이스 경계 commit·push 루프, 멱등·레이트리밋 exit 3 시 정지) — 로스터·프레임·모델 핀은 D74 사전 등록 그대로","budget":"18호출 (E2 잔여 ~69 + E4 18 + P3 62 + P4 108 = 계획 내, 캡 380)","metered":"E4 18 (발사 시점 기록)","learning_note":"이 판단에서 알아야 할 것: 사전 등록된 실행 순서의 개정 권한은 그것을 등록한 사람에게 있다 — 라이브 지시가 오면 따르되, '무엇이 언제 왜 바뀌었나'를 결과 전에 원장에 박는 것까지가 순서 규율이다"}

## D81 — E4 교차모델 완결 (EXPLORATORY, 각주 전용) (2026-07-13, 18호출·FAIL 0, JSON 1줄)

{"decision":"D81","date":"2026-07-13","action":"E4 실행 완결 — 로스터 18 전건(홀드아웃 3+wave-2 6+E1 대조군 9, PLAN §4 케이스 경계 commit·push 준수, 하네스 경로 개정 #4), claude-opus-4-8 서빙 핀 호출별 검증. analysis/e4_crossmodel.{json,md} 확정","results":"Spearman ρ=0.781 · 플래그(p≥50) 일치 15/18 · Cohen κ=0.6582 — 불일치 3건은 산출물 열거. 판독(사전 등록 주장 상한 그대로): '두 Claude 모델의 순위가 상당히 겹친다' — 단일 모델 의존 한계의 측정된 각주 재료. truth 없음·벤치마크 아님·EXPLORATORY 라벨 전 표면 의무 (lint 강제)","expectation_context":"PLAN §6 사전 명시 — 일치가 높든 낮든 정직 보고; ρ=0.78·κ=0.66은 '겹치나 완전하지 않음' — L-표면 인용 시 이 문면 그대로","metered":"18호출 (누계 P0 진행분+18)","learning_note":"이 판단에서 알아야 할 것: 교차모델 일치도는 정답률이 아니라 순위 중첩도다 — 둘 다 피평가자인 이상 κ가 높아도 '둘 다 맞다'가 아니고 낮아도 '하나가 틀렸다'가 아니며, 오직 '단일 모델 의존'이라는 한계의 크기만 잰다"}

## D82 — E2 완결 + 엔진 판정 기록: a_llm_engine (2026-07-13, 기계 판정, 소유자 서명 대기, JSON 1줄)

{"decision":"D82","date":"2026-07-13","action":"P0 E2 완결 — 146/146 스냅샷 유효(FAIL 0), 후처리 자동 체인 완주(e2_trajectories → engine_verdict → E2_SUMMARY). 판정은 specs/ENGINE_DECISION.md §4 기계 규칙 그대로 — 세션 재량 0","verdict":"**a_llm_engine** — median lead LLM 7.0분기 vs B3 5.5분기 (LLM ≥ B3+1분기, §4 규칙 2 발화). per-case lead 전수표 verdict JSON 병기 (실험군 12: LLM 2–8분기·B3 0–8분기)","co_report_honesty":"① FPR@임계(대조군 궤적 7): LLM 5/7=71.4% CP[29.0%,96.3%] vs B3 0/7 — LLM 리드는 높은 오탐과 동행 (buyer_metrics §2, 판정 입력 아님·정직 병기) ② b4_comparison.valid=false (커버리지<70% — D60/D61 사전 예측 그대로) ③ LLM j=0 AUC=null+플래그 (D71 규약 — 대조군 perturbed 미채점, Q-M06 계류) · B3 j=0 AUC 0.6845","spend_accounting":"P0 실지출 162호출 = 최종 146 + 재지출 16 (D70 킬 부분파일 ~7 + top_signals 스키마 재추첨 9 — 그중 5중 중복발사 사고 포함, 아래) · 로그 158건 보존 + D70 소실 4건. 누계: P0 162 + E4 18 = 180/380","incident_duplicate_launch":"재추첨 재발사 시 pgrep 검증 오류(모니터 프로세스 명령문이 패턴에 오탐)로 최대 5중 중복 프로세스 발사 — 즉시 전멸 킬, 중복 지출은 위 재지출 16에 포함(출력은 멱등 스킵이 보호). 교훈: 프로세스 검증은 패턴이 아니라 PID","buyer_metrics_amendment":"buyer_metrics_build가 하네스 로그의 캐시 필드를 미계상(원 설계는 raw-API 로그 가정) — usage.input_tokens(비캐시 잔여 ~3)만 합산해 $0.2055/스크린으로 과소계상. 과금 등가 가중(1h 쓰기×2.0·5m×1.25·읽기×0.1)으로 개정 → **$0.5304/스크린·유니버스 1회전(~300) $159.12** (sonnet-5 목록가 $3/$15 — 2026-08-31까지 인트로 $2/$10 별도, 캐시본 참조 명기). 양판 전량 공개 — 결과 열람 후 개정이므로 D56 규율(공개 조건) 적용","ownership":"판정 자체는 사전 등록 기계 규칙의 산술 — 단 branch (a)의 귀결(screener stage-2 활성)은 LAUNCH_SEQUENCE 4단계의 소유자 확정 사항. 본 기록은 human_finalized=false — 소유자 서명 대기","metered":"P0 162 (누계 180)","learning_note":"이 판단에서 알아야 할 것: 판정 브랜치가 (a)로 나왔을 때 가장 중요한 병기는 FPR이다 — 리드타임 7분기는 오탐 71%와 같은 표에 있어야 하고, stage-2 활성화 결정은 그 두 숫자를 함께 본 사람의 것이지 리드타임만 본 기계의 것이 아니다"}

## D83 — P4(Q-F06-B) 병행 발사 (2026-07-13, D80 개정 연장, JSON 1줄)

{"decision":"D83","date":"2026-07-13","action":"Q-F06-B 108호출 발사 — D80 라이브 순서 개정의 연장(소유자 반복 지시 'finish all tasks'), P3와 병행·동시 2 상한 유지(runner --concurrency 1). 4연 invocation(w1_controls×draw_2/3·wave2×draw_2/3), draw 경계 commit·push, 멱등","budget_projection":"누계 180 + P3 62 + P4 108 = 350 ≤ 캡 380 — P5(32)는 캡 초과(382)로 발사 불가, 소유자 큐 잔류","metered":"108 (발사 시점 기록)","learning_note":"이 판단에서 알아야 할 것: 캡이 있는 밤에는 마지막 유닛의 발사 가능 여부가 앞 유닛들의 재지출에서 결정된다 — 재지출 16이 P5의 자리 절반을 먹었고, 이것이 재지출을 원장에 실시간 기록하는 이유다"}

## D84 — Q-F05 완결: v2 date-shift name-ID 프로브 (2026-07-13, 63호출, JSON 1줄)

{"decision":"D84","date":"2026-07-13","action":"Q-F05 실행 완결 — 62케이스 v2ds recognition 프로브(하네스, --v2-dateshift, 로그 _v2ds 격리) + analysis/name_probes_v2ds.py 판정 (동결 name_match 규칙, 재해석 금지)","results":"**wave-1 4/30 = 13.3% (동결 v1 50%, −36.7pp) · wave-2 0/32 = 0.0% (동결 v1 21.9%, −21.9pp)** — CP95 병기 산출물 참조. 사전 등록 판독 가드 내 서술: 날짜 지문 제거가 name-ID 채널을 추가로 좁혔다 (원인 분해·인과 서술은 소유자 검토 대상)","spend":"63호출 = 62 + case_25 재시도 1 (1차 호출 FAIL — 출력 미기록, 멱등 재시도로 완결). 누계 180+63 = 243/380","hygiene_context":"발사 전 위생 스캔 62/62 PASS(D73)·엔드포인트 사전 등록(스펙 §5)·동일 프로브 문구·동일 k — v1과 유일 차이는 date_shift.shift_payload (렌더 직전 이동+accession 마스킹)","metered":"63 (누계 243)","learning_note":"이 판단에서 알아야 할 것: 교란의 효과 측정은 '무엇이 남았는가'만큼 '무엇이 떨어졌는가'가 판정 재료다 — 50%→13.3%·21.9%→0%는 v1 잔존 인지의 대부분이 날짜 지문 경유였다는 산술이고, 그 진술은 사전 등록 두 문장 밖으로 나가지 않아야 한다"}

## D85 — Q-F06-B 완결: median-of-3 병기 (2026-07-13, 108호출, JSON 1줄)

{"decision":"D85","date":"2026-07-13","action":"Q-F06 옵션 B 실행 완결 — (22 w1-control + 32 w2)×draw_2/3 = 108호출(FAIL 0, draw 경계 commit·push) + w1-treatment 8은 hardening draw_2/3 재사용(프레임 동일 실측 근거 D75). analysis/draw_k3_results.json·DRAW_K3_REPORT.md 확정","results":"flip-rate(≥50, draw-1 vs median-of-3): wave-1 3/30 (case_02 획득·case_08/33 상실) · wave-2 3/32 (case_69/49/40 상실) — 경계 케이스 식별 표 사전 등록 그대로. median-of-3 분리 통계(병기 전용, 대체 금지): wave-1 AUC 0.8494 [동결 draw-1 0.8239] · wave-2 0.8261 [동결 0.829] — 안정성 밴드가 발행값을 감싼다","invariants":"동결 draw-1 발행 수치 불변·grade 병합 0(dims=draw-1)·홀드아웃 k=5 불변·temp=0 비결정론 단서 산출물 내 하드코딩","metered":"108 (누계 351/380)","learning_note":"이 판단에서 알아야 할 것: k=3 병기의 산출물은 '새 숫자'가 아니라 '발행 숫자의 신뢰 구간 서사'다 — median AUC가 draw-1을 감싸고 flip이 경계 케이스 목록으로 떨어지면, 발행값은 그대로 두고 표만 옆에 세우는 것이 병기의 전부다"}

{"decision":"D86","date":"2026-07-15","action":"OUT-GIL-V1 마감 — 과제 규격 memo 조립(output/GIL_memo_v1.md: 영문 헤더 고지·flag 5건·인용 검증표 부록) + 병렬 세션 커밋(08be4ee: data/gil·평가 2호출·flags·검증·한글 memo_draft) 병합 확인. runs/ 무접촉(매니페스트 불변), 신규 미터링 0","results":"인용 19건 프로그램 판정 14 VERIFIED·1 ALTERED·4 NOT FOUND — 수기 추적 5/5 병합 인용(날조 0, 서명 대기). 추가 검증: 모델 서술 $201.6M은 파생값(40-F 총 step-up $237M − FY2025 인식 $35.4M; Q1 $106.3M+잔여 $95M 정합) — memo Flag 1 assembly note 명기. 각주 완전성: 연차 Note 1–30·중간 Note 1–16 전체 추출 확인","invariants":"동결 발행 수치 무접촉·피평가자 판정 세션 내 생성 0·현재 기업 어휘 규율(분식/fraud 단정 0, 포지션 없음·교육 목적 고지 포함)","metered":"0 (GIL 평가 2호출은 08be4ee 세션이 실행·call_*.json 기록: output 37,258 tokens)","learning_note":"이 판단에서 알아야 할 것: 병렬 세션이 같은 과제를 커밋한 뒤에는 커밋본을 원본으로 삼고 미커밋 격차(과제 규격 경로·부록 표·파생 수치 검증)만 채우는 것이 병합 규약의 실체다 — 겹치는 산출물 재작성은 충돌만 만든다"}

## D87 — 결정 표(임계·비용) 워크스트림: 사전 등록 + 계산 (2026-07-16, 무호출, JSON 1줄)

{"decision":"D87","date":"2026-07-16","action":"DECISION_TABLE_PLAN.md 사전 등록 단독 커밋(2fc3d23) 후 analysis/decision_table.py(+테스트 5, 무호출) 계산 — analysis/decision_table.json·DECISION_TABLE.md(서명 전 초안). 입력은 동결 경로만(runs/ 무접촉·미터링 0), CP는 동결 holdout_controls_analyze.clopper_pearson 재사용(신규 통계 코드 0), 비용 축은 BUYER_METRICS $0.5304 인용","results":"교차 검증 앵커 일치 — L4 T≥50 오탐 5/7=71.4% CP[29.0%,96.3%]·스크린 158이 buyer_metrics §2·§3과 동일. 주 결론(정직 서술): 궤적 레이어에서 단독 LLM 임계는 지배 전략 없음(T=50 탐지 12/12·오탐 71.4% ↔ T=70 탐지 1/12·오탐 0/7). EXPLORATORY 결합(B3≥2 AND llm_p≥T, 동일 스냅샷)은 전 임계 오탐 0/7·T=50 탐지 7/12 — 사후 규칙이므로 성능 주장 금지, Cycle-2 sealed 후보 전용","gates":"test_decision_table 5/5 PASS·README 무접촉(서명 게이트 Q-O02)·동결 발행 수치 불변","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 유의성(p=0.0021)을 구매자 언어로 번역하면 결론이 약해지는 게 정상이다 — N이 작은 표에서 구매자가 사는 것은 점 추정이 아니라 구간과 가격표이고, '지배 전략 없음'이 이 표가 팔 수 있는 가장 정직한 문장이다"}

## D88 — GIL 메모 발행 패키지: 선정 배경 공개 + 증거 라인 부록 + Issue #4 텍스트 (2026-07-16, 무호출, JSON 1줄)

{"decision":"D88","date":"2026-07-16","action":"OUT-GIL-V1 발행 승격 패키지 — ① 선정 배경 공개 절(사후 선택 방어: Jehoshaphat 2026-06-16 인지 후 선정 + 컷오프 2026-06-15 코드 강제 = 봉인된 사전-리포트 복제) 한·영 양판 삽입 ② analysis/EVIDENCE_LINES.md(동결 51케이스 CL1–CL8 flag 빈도 실험군 20/대조군 31 정직 병기·유형별 대표 원문 인용 accession 병기·HUBG 박스 README 범위 내·재현 스니펫 검증) ③ analysis/ISSUE_4_GIL_MEMO_DRAFT.md(제목 2안·§6 자가 감사 7항 PASS·게시 전 체크리스트). runs/gil_memo_v1/memo_draft.md 수정분 매니페스트 재생성(verify_blindness --write-manifest PASS)","honesty":"빈도표는 판별 증명이 아님을 본문에 명시 — CL7은 대조군 74% 발화·CL6은 대조군이 더 높음(60% vs 68%). 신규 스크리닝·신규 주장·신규 미터링 0. 게시·독자 발송은 소유자 전용(Q-O03)","gates":"verify_blindness PASS(146 모델 출력·매니페스트 대조)·§6 금지 어휘 grep 양판 0·인용 스니펫 재현 일치","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 사후 선택된 케이스의 발행 가치는 선택 경위를 숨겨서가 아니라 정확히 공개해서 생긴다 — '리포트를 보고 골랐지만 입력은 리포트 이전으로 봉인했다'는 문장이 있어야 이 메모는 재현 실험이 되고, 없으면 결과 소급 선택이 된다"}

## D89 — Cycle-2 성장 루프 규격화: 유니버스 사전 등록 + 월간 의식 + 부록 A (2026-07-16, 무호출, JSON 1줄 — 원번호 D88, 병렬 랜딩 재부여)

{"decision":"D89","original_decision":"D88","renumber_note":"병렬 세션 D88(GIL 발행 패키지, 0389037 15:43:16)이 선착 — 재부여 규약대로 본 엔트리 D89, 큐 항목 Q-O03→Q-O04","date":"2026-07-16","action":"성장 루프 3종 커밋 — ① docs/UNIVERSE_SELECTION.md: EQ 모니터 유니버스(8~15) 기계 선정 프로토콜 사전 등록 (후보 조회 전 커밋 = 사후 선택 방어; SIC 집합 3선택지는 서명 시 확정, 확정 전 열거 금지) ② docs/MONTHLY_RITUAL.md + make rescan: 월 1회 20분 홀드아웃 재조사 체크리스트 (무인 자동화 금지 — §5-1/Q-E03 판례 주석) ③ FUTURE_CYCLE_PROTOCOL 부록 A: D87 EXPLORATORY 결합 규칙(B3 W8≥2 AND LLM≥T)을 Cycle-2 sealed 전향 검증 후보로 등록 (소급 성능 주장 금지 명문화)","sequence_note":"UNIVERSE_SELECTION은 어떤 후보 기업 조회보다 먼저 커밋됨 — 이 순서 자체가 방어. 후보 목록 생성 0","parallel_session_note":"D87(결정 표)은 동시 활성 병렬 세션 산출 — 본 세션은 중복 실행 회피, 부록 A가 D87 산출물의 Cycle-2 등록 의도를 완결. GIL 발행 패키지(Prompt B)는 병렬 세션 진행 중 실측(untracked EVIDENCE_LINES·ISSUE_4 draft)으로 본 세션 스코프에서 제외","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 사후 선택 방어는 문서 내용이 아니라 커밋 순서에서 나온다 — 기준 문서가 후보 목록보다 늦으면 아무리 기계적인 기준도 사후 합리화와 구별 불능이다"}

## D90 — RP-17 소유자 수용: B4 분모 사슬 개정 = 기계적 커버리지 수리 (2026-07-16, 서명, JSON 1줄)

{"decision":"D90","date":"2026-07-16","action":"RP-17 수용 — (owner, 2026-07-16, this session's structured decision responses). D56/D57 분모 폴백 사슬 개정을 '기계적 커버리지 결함 수리'로 분류 확정, D57 결과(holdout 10/12) 정본. 원복 경로(287a92a checkout) 소멸. 패킷 §4 거버넌스 라인 3종(사후 스펙 개정 한계·5게이트 규율·단일 작성자 규율) CLAUDE.md 방법론 규율 6·7·8로 발효","rationale_adopted":"편입 기준 기계성(태그 존재=자동 편입)·against-interest 방향(경쟁 기준선 강화)·선커밋 절차 증거·헤드라인 무변화(비교 성립 tier 전후 부재)","dissent_preserved":"패킷 §3 최강 반론(결과 열람 후 설계·사다리 4지 재량 공간) 원문 보존 — 수용은 반론의 소거가 아니라 분류 판단","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 사후 개정 수용의 근거는 '결과가 좋아서'가 아니라 '편입이 기계적이고 방향이 역이해관계이며 순서가 증명되어서'다 — 같은 개정이라도 이 셋 중 하나가 없으면 분류가 뒤집힌다"}

## D91 — RP-15·RP-16 소유자 수용: 라벨 정밀화 + 서수 언어 diff 적용 (2026-07-16, 서명, JSON 1줄)

{"decision":"D91","date":"2026-07-16","action":"Q-F03(RP-15 DIFF-4/5)·Q-F04(RP-16 DIFF-6/7) 수용 — (owner, 2026-07-16, this session's structured decision responses). 적용: ISSUE_2 §7 첫 불릿(전건 Big R·기저율 ~2.2%·4년 모니터링 창·창 만료=라벨 노이즈 데이터 보고 약속)·README 양어 Big R 병기·ISSUE_0 §5(0–100 서수, 재보정 비실시 근거)·ISSUE_2 §2 표 헤더(LLM p → LLM score (0–100, ordinal))","invariants":"스키마 필드 misstatement_probability 무변경(Cycle-2 개명 등록)·동결 수치 무접촉·발행된 GitHub Issue 본문 편집은 소유자 잔여(edited 표시+사유 코멘트 규약)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: 라벨 정밀화 diff의 가치는 주장 강화가 아니라 한정 강화다 — Big R 병기와 기저율 2.2%는 같은 문장 안에서 서로를 견제하고, 그 긴장을 그대로 두는 것이 정직한 명명이다"}
