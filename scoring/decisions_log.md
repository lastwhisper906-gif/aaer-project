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
