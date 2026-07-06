# overrides.md — 서명/오버라이드 기록 (PROJECT.md §7 서명 규칙)

> Claude 1차 판정을 인간이 뒤집은 건의 전수 기록. 이 기록은 trust boundary의
> 1차 데이터이며 Issue #0의 소재다 (§9: 0건이면 고무도장 의심, 전부 뒤집기면 과소신뢰 의심).
> 서명(승인)은 각 산출물 파일/커밋에 남기고, 이 파일에는 **오버라이드만** 적는다.

## 기록 형식

```
## OV-NNN — YYYY-MM-DD
- 대상: <케이스 ID 또는 산출물 경로> / <필드·항목>
- Claude 1차: <원 판정 + 근거 요약>
- 오버라이드: <인간 확정 내용>
- 사유: <근거 — 원문 인용/데이터 포인트>
- 사후 확인: (Week 3+ 기입) 옳았던 쪽 = claude | human | 미확정
```

---

## OV-001 — 2026-07-05
- 대상: `data/evaluatee/cases.json` 전건 + `schemas/evaluatee_input.json` / case_id 필드
- Claude 1차: 피평가자 입력 분리 설계에서 원본 case_id(T01~T30)를 화이트리스트에 포함하고
  스키마 패턴을 `^(T|C)[0-9]{2}$`로 고정 — "group 필드 제외로 그룹 소속이 은닉된다"고 판정
  (3중 방어: 재생성 대조·스키마·금지 필드 목록. 전부 **필드 존재** 검사).
- 오버라이드: case_id의 T/C **접두사 자체가** 그룹 소속(=은닉 대상 정답)을 인코딩 — 대조군
  편입 즉시 접두사가 정답을 그대로 노출. 중립 ID(case_NN) + 고정 시드 셔플로 치환, 매핑은
  채점 전용 `scoring/id_mapping.json`으로 분리 (최초 `data/scoring/` → 사용자 검토로
  `scoring/` 이동: 이 파일은 데이터가 아니라 채점 인프라(정답 열쇠)라는 성격 판단).
- 사유: 스키마 문언이 증거 — `"pattern": "^(T|C)[0-9]{2}$"` + 설명 "T=실험군(treated),
  C=대조군(control)". group 필드를 빼고도 같은 정보를 ID에 남긴 설계 모순. 인간 표본
  점검(§7)이 발견, Claude의 방어 3중은 값 수준을 보지 않아 구조적으로 잡을 수 없었음.
- 사후 확인: human (즉시 검증 — 값 실측으로 결함 확정, 방어 ④ 테스트로 기계 강제화)
- **학습 노트(§10)**: "필드를 지웠다"와 "정보를 지웠다"는 다르다 — 방어가 필드 목록을 볼 때
  누출은 값 안으로 이동한다.

## OV-002 — 2026-07-05
- 대상: `data/evaluatee/cases.json` T04/T14/T18 / company_name 필드
- Claude 1차: candidates.json의 company_name(법적 캡션 관행 그대로: "…; n/k/a Weatherford
  International plc", "(now Obsidian Energy Ltd.)", "(n/k/a Bausch Health Companies Inc.)")을
  무변환 통과 — 사명은 중립 메타데이터라고 암묵 판정.
- 오버라이드: 후신 사명은 **정의상 컷오프 이후 정보** — §5-1(look-ahead 차단) 위반이 필드
  값 안에 존재. 최악은 T18: Bausch Health로의 개명(2018)은 피평가자가 감지해야 할 스캔들
  그 자체의 결과물이고, 컷오프는 2015-10-18. T14도 동일 구조(Obsidian 개명 2017-06, 컷오프
  2014-07-28). 컷오프 시점 사명만 남기고 f/k/a(과거 정보)는 유지.
- 사유: 개명 시점 vs cutoff_date 대조 — T04 plc 전환(2014) > 컷오프 2011-02-28,
  T14 2017-06 > 2014-07-28, T18 2018 > 2015-10-18. 전건 컷오프 이후. 인간 표본 점검(§7) 발견.
- 사후 확인: human (즉시 검증 — 금지 부분열 스캔을 방어 ④에 편입)
- **학습 노트(§10)**: look-ahead는 데이터 로딩 경로만이 아니라 **문자열 값 내부**로도 들어온다
  — cutoff_guard가 지키는 것은 문서 날짜지 필드 값의 시제가 아니다.

## GA-001 — 2026-07-06 (거버넌스 수정 — 오버라이드가 아니라 협업 모델 자체의 소유자 변경 지시)

- 대상: CLAUDE.md·PROJECT.md §7의 **차단형(blocking) 인간 서명 게이트** — 이번 사이클 잔여 기간 한정.
- 성격: Claude 판정에 대한 오버라이드가 아니라, 소유자(사용자)가 협업 모델의 실행 형태를
  변경한 거버넌스 수정. §7 불변 조항 3(최종 서명은 인간)은 **폐지되지 않고 비동기화**된다 —
  인간 검토는 review packet을 통해 사후(post hoc)에 수행되며, 오버라이드 경로와 재실행
  비용이 각 packet에 명시된다.
- 세션 가드레일과의 긴장 (기록 의무): CLAUDE.md는 "검토 없는 일괄 승인은 인간 서명의
  형해화"라고 규정한다. 본 수정은 일괄 *승인*이 아니라 검토의 *시점 이동*(사전 차단 →
  사후 감사)이며, Claude 작성 산출물을 인간 서명으로 위장하는 것을 명시적으로 금지한다
  ((b), D15). 이 구분이 형해화 지적에 대한 소유자의 응답임을 기록한다.
- **소유자 지시 원문 (2026-07-06, verbatim)**:

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

- 부수 지시 (같은 지시문의 모드 선언): "Mode: CONTINUOUS EXECUTION. … All decisions that
  previously required human sign-off have been pre-decided by the owner (DECISIONS block)
  or converted to deterministic rules. Human review happens asynchronously via review
  packets; never stop to wait for it." — DECISIONS 블록 전문은 `scoring/decisions_log.md`.
- 효력 범위: 이번 사이클 잔여 기간. §5 방법론 규율(look-ahead 차단, 기준 사전 고정,
  대조군 동일 프로토콜)은 변경 없음 — (c)가 기준 사전 고정을 기계적으로 보존.
- **학습 노트(§10)**: "인간 서명"의 실질은 서명 행위가 아니라 (i) 기준이 결과보다 먼저
  고정되었다는 증거와 (ii) 감사 가능한 오버라이드 경로다 — 이 둘이 기계적으로 보존되면
  검토 시점(사전/사후)은 실행 형태의 문제가 된다. 단, 사후 검토가 실제로 수행되지 않으면
  이 수정은 소급적으로 형해화가 된다 (Review Packet 색인이 그 방지 장치).
- **소유자 확인 (2026-07-06, 세션 내 직접 진술)**: "I will confirm the GA-001" —
  본 거버넌스 수정 자체에 대한 인간 확인. **범위 주의**: 이 확인은 GA-001(게이트
  비동기화·저자 표시·freeze-then-run)의 유효성 확인이며, 그 틀 안에서 생성된 개별
  산출물(review packet 00~04, 재량 판단 J1~J12)의 일괄 승인이 아니다 — 개별 감사는
  `review_packets/INDEX.md` 경로로 별도 수행 (불변 조항 3의 형해화 방지).

## GA-001 부속 — 소유자 확인 D2·D3 (2026-07-06, 오버라이드 아님 — 기존 서명 규칙의 재확인)

- **D2 (T17 MRVL 조작기간)**: 명령문 Relevant Period 2015-01~07 (¶2) — GP-3 서명
  원칙("창 = 명령문 정의, 재량 0")의 적용 결과와 동일. 변경 없음, 소유자 재확인만 기록.
- **D3 (T27 WAGE 수치 기준)**: 명령문 인쇄 수치 '>9%'(¶44) 기준, 2차 수치(-18.6%/$9.75)는
  출처 명기 주석 — GP-1 채택안 ①과 동일. 변경 없음, 소유자 재확인만 기록.
- 근거·기각 대안 전문: `scoring/decisions_log.md` D2/D3.

## RAT-001 — J13-b/c 사후 추인(ratification) — **SIGNED: 추인 (2026-07-07, 소유자)** (개설: RP-06 B5(d), 2026-07-06)

> 이 항목은 오버라이드가 아니라 **실행층 재량의 사후 추인 요청**이다. 초안 작성:
> 채점 보조 Claude. (개설 시 문언: "서명 전까지 미해결 상태로 유지 — Claude는
> 이 항목을 서명하거나 해결 표시할 수 없다." — 서명 주체는 아래와 같이 소유자.)

- 대상: 격리 기제 제3안 채택 (J13-b/c — `scoring/decisions_log.md` freeze 개정 #2 부록)
- 사실 관계: freeze 개정 #2 지시문이 핀한 격리 기제 2종이 모두 실증 기각됨 —
  ① `--bare` (OAuth 미지원 — "Not logged in", 지시문 자체가 이 경우 즉시 포기 지시)
  ② `CLAUDE_CONFIG_DIR` 격리 (빈 디렉토리·최소 인증 시드 모두 구독 OAuth 차단 —
  파일럿 실증 2회, logs/run_20260706T120619Z·120836Z). 이에 실행층 재량으로
  **제3안(플래그 기반 격리)** 채택: `--setting-sources "" --strict-mcp-config
  --tools "" --system-prompt 전면 대체 + repo 밖 임시 cwd + nonessential-traffic
  차단 env.
- 재량의 성격: 지시문의 격리 **의도**(설정·훅·MCP·도구·저장소 컨텍스트 0)는
  보존하되 **기제**를 교체 — 고정 기준(eval spec·케이스·임계·핀) 무변경. 단,
  지시문이 명시적으로 핀한 기제의 교체이므로 실행층 재량의 상한선 사례다 —
  사후 추인이 필요하다고 판단해 이 항목을 개설한다.
- 증거: Phase 4 격리 게이트 **5/5 PASS** (기제를 신뢰하지 않고 결과를 검사 —
  격리 프로브 "도구 0·파일 0·MCP 0·저장소 흔적 0" 자백 + verbose 트레이스
  grep 무흔적 + 서빙 모델 핀 단독 + 파일럿 스키마 통과. 판정표: logs/run_log.md).
- 기각된 대안: 실행 중단 후 소유자 문의 (연속 실행 모드·PRE-AUTHORIZATION과
  충돌 — 격리 게이트 PASS가 진행 조건이었고 게이트는 PASS였다), 종량 자격
  증명 부착(--bare 구제 — 지시문 금지 조항).
- **서명 블록 (소유자 기입란)**:
  - [x] **추인** (J13-b/c 재량 승인 — 격리 기제 제3안을 사후 승인)
  - [ ] 기각 (승인 불가 — 필요 조치: ______________________________ )
  - 서명: **소유자 — 2026-07-07 세션 내 직접 진술, verbatim: "RAT-001 서명할게."**
    (D15/GA-001 선례에 따른 기록 형식: 서명 주체 = 소유자, 기입 = 채점 보조
    Claude의 전사 — 진술 원문 인용이 서명의 실체이며 Claude가 서명을 생성한
    것이 아님)  일자: 2026-07-07
  - 상태: **SIGNED — 추인 확정** (2026-07-07). 효력: J13-b/c(격리 기제 제3안
    채택)는 실행층 재량에서 **소유자 추인 재량**으로 전환 — INDEX.md J13a~g
    행의 감사 상태에 반영. 이 추인은 격리 기제 결정에 한정되며, 개별 채점
    26건의 확정(대기열 ④)과는 별개다.
