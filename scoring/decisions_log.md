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

## D51 — 게이트 수리: ~/aaer-data 매니페스트에 reference/ 등재 (2026-07-13, 무인, 무호출, JSON 1줄)

{"decision":"D51","date":"2026-07-13","action":"verify_manifest.py 귀속 로직에 reference/ 분기 추가 (REFERENCE_URLS — SEC 원본 URL 2건) + 매니페스트 재생성 — 세션 개시 게이트 점검에서 make verify FAIL 발견 (EXTRA 2건: reference/cik-lookup-data.txt·company_tickers.json)","root_cause":"D36(2026-07-10) tools/gen_fict_names.py가 ~/aaer-data/reference/에 스크린 전용 참조 목록을 정당하게 배치 (data/README.md 기록 완료)했으나 매니페스트 재생성 누락 — 직전 핸드오프의 4게이트 세트가 verify_manifest 대신 pytest를 실측해 미검출","fix_order":"코드+원장 커밋 → --write 재생성 → diff 검사(추가 2건+계수·타임스탬프 외 변화 없음 확인 후 커밋) → 전 게이트 재실측","txt_pitfall":"cik-lookup-data.txt는 .txt지만 로컬 추출 파생물이 아님 — 기존 suffix 규칙이 derived_from을 오기록했을 것이므로 reference/ 분기를 suffix 판정보다 앞에 배치","invariants":"동결 수치·발행 표면 무변경; 기존 매니페스트 항목의 해시 기준선 불변 (diff로 기계 확인)","metered":"0호출","learning_note":"이 판단에서 알아야 할 것: fail-closed 게이트는 '어느 게이트 세트를 실측하는가'까지가 규율이다 — 게이트 목록에서 하나를 다른 것으로 바꿔 실측하면 그 자리에 구멍이 생기고, 이번처럼 이틀 뒤에야 발견된다"}
