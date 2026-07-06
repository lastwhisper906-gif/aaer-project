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

## GA-001 부속 — 소유자 확인 D2·D3 (2026-07-06, 오버라이드 아님 — 기존 서명 규칙의 재확인)

- **D2 (T17 MRVL 조작기간)**: 명령문 Relevant Period 2015-01~07 (¶2) — GP-3 서명
  원칙("창 = 명령문 정의, 재량 0")의 적용 결과와 동일. 변경 없음, 소유자 재확인만 기록.
- **D3 (T27 WAGE 수치 기준)**: 명령문 인쇄 수치 '>9%'(¶44) 기준, 2차 수치(-18.6%/$9.75)는
  출처 명기 주석 — GP-1 채택안 ①과 동일. 변경 없음, 소유자 재확인만 기록.
- 근거·기각 대안 전문: `scoring/decisions_log.md` D2/D3.
