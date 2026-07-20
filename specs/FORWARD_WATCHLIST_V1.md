# specs/FORWARD_WATCHLIST_V1.md — 첫 전향 워치리스트 사이클 동결 프로토콜 (cycle_001)

> 2026-07-20 동결 (owner plan 2026-07-20 §4 서면 위임, ledger D100).
> **모델 런 발사는 이 스펙으로 승인되지 않는다** — 발사는
> `forward/cycle_001/OWNER_LAUNCH_GATE.md`의 소유자 승인 전용.
> 이 스펙의 개정은 봉인 전 = 일반 커밋 + 사유, 봉인 후 = FREEZE_REV +
> D-엔트리 전용 (PROJECT.md §5-6).

## 0. 목적 (성공 기준의 정의)

첫 forward 사이클은 예측 성능 입증이 아니다. 입증 대상은 운영 무결성:

1. 결과 이전에 유니버스를 정의하고,
2. 스크리닝 시점 가용 데이터를 동결하고,
3. 동결 프로토콜로 점수를 생성하고,
4. 외부 검증 가능한 타임스탬프로 불변 봉인하고,
5. 원 점수를 수정하지 않은 채 이후 결과를 관측한다.

성숙 전 주장 수준: **Level 0** — 성숙 후 잠재 **Level 3**
(`docs/CLAIM_HIERARCHY.md`).

## 1. 스크리닝 유니버스 (Q-O04/D95 확정 규칙 — verbatim 편입)

`docs/UNIVERSE_SELECTION.md` §1–§3 + §6 확정이 규범 원문이다:

- 섹터 SIC 집합 **(A) 하드웨어·전력 사슬 협의**: 3674·3672·3661/3663/3669·
  3571·3572·3576·3577·3612/3613·3621·3585·4911.
- 선정 수 **12** (적격 >15 시 SIC 버킷 float 내림차순 라운드로빈, 동률 CIK
  오름차순, 잔여 alternates 순서 보존).
- 규모 하한 **`dei:EntityPublicFloat` ≥ $1B** · 폼 요건(24개월 10-K ≥1,
  10-Q ≥2, 외국사 제외) · XBRL 이력(≥8건, 10-K ≥2).
- 제외: 트레일링 24개월 4.02/공매도 리포트/AAER → post-hoc 트랙 강등 ·
  Cycle-1 기출 회사.

**유니버스는 모델 점수를 보기 전에 동결된다.** 열거 T₀ = 2026-07-20 세션
(governance/DECISION_FORWARD_UNIVERSE.md §5 — 서면 위임). 열거 산출물
`forward/cycle_001/universe.json`이 동결본이며, 점수 관측 후 개별 기업
추가·제거 금지. 봉인 전 §2 오염 발견 시에만 규칙 인용 + alternates 자동
승격 + 사유 기록 (`UNIVERSE_SELECTION.md` §3).

## 2. 스크리닝 일자와 실행 창

- **스크리닝 컷오프(screening_cutoff)**: `2026-11-15` (미국 동부시간 ET
  기준 그 날 23:59:59까지 — EDGAR acceptance datetime 기준).
- **실행 창**: 2026-11-15 ~ 2026-11-22 (컷오프 후 7일). 채점·봉인은 이
  창 안에서 완료한다. 실제 봉인 타임스탬프가 지배하며 지연은
  `SEAL_RECORD.md`에 기록.

## 3. 중단·지연·재봉인 규칙 (사전 동결 — 봉인 시점 즉흥 대응 금지)

1. **창 내 지연**: 실행이 밀려도 2026-11-22 내 완료면 사이클 유효.
   실제 봉인 시각 기록, 슬립 사유 `SEAL_RECORD.md` 병기.
2. **창 초과**: 사이클을 조용히 늘리지 않는다. `cycle_001`을 `aborted`로
   닫고(일자 사유 기입) `cycle_002`를 새 동결 창으로 연다. aborted
   디렉토리는 보존 — 삭제·개명 금지.
3. **부분 채점**: 동결 유니버스 12사 중 **≥11사 채점 완료 시에만 봉인
   가능** (사전 등록 완료 분율 — 12사 기준 ≥91.7%). 미채점 레코드는
   `scores.json`에 `not_scored`로 명시 등재. 11사 미만이면 규칙 2 적용
   (abort).
4. **데이터 소스 장애**: 필수 소스(EDGAR submissions/companyfacts) 불가 시
   장애를 기록하고 규칙 1/2를 적용한다. 일자 기입 오버라이드 기록 없이
   대체 소스 즉흥 투입 금지.
5. **소급 수정 금지**: aborted/부분 사이클의 파일은 그대로 동결. 교정은
   오직 새 사이클에서.

## 4. 입력 컷오프 규칙

- 모든 입력은 `filed_at_or_before <= screening_cutoff`. 판정 기준은 EDGAR
  **acceptance datetime (ET)**. 컷오프 당일(2026-11-15) 제출분은 포함.
- 정정 공시(amendment): 원 문서의 제출일이 아니라 **정정본 자체의
  제출일**로 판정 — 컷오프 후 제출된 정정본은 미포함 (원본만 포함).
- 지연 제출(late filing): 실제 제출일 기준 — 대상 기간이 컷오프 전이어도
  제출이 컷오프 후면 미포함.
- **retrieval_date(수집 시각)와 filing_date(제출 시각)는 분리 저장**
  (`source_manifest.json`) — 컷오프 후 수집이라도 제출이 컷오프 전이면
  적격이며, 그 사실이 기계 검증 가능해야 한다.
- 기계 검증: `tools/forward_validate.py`가 `source_manifest.json` 전 항목의
  filing_date ≤ cutoff를 검사 (`pipeline/cutoff_guard.py` 경유 로딩).

## 5. 모델 프로토콜

- **모델 핀**: `pipeline/runner.py::EVALUATEE_MODEL` — 봉인 시점에
  `forward/cycle_001/PROTOCOL.md`에 사본 기록. 현재 `claude-sonnet-5`.
- **하네스**: `pipeline/cli_client.py` (`claude -p`) — 격리 플래그 일체
  (`--setting-sources ""`·`--strict-mcp-config`·`--tools ""`·시스템 프롬프트
  치환·`--json-schema`·`--max-turns 2`·레포 밖 임시 cwd) 그대로.
- **실행 경로 (동결)**: **구독 OAuth 전용** — `claude -p` +
  `CLAUDE_CODE_OAUTH_TOKEN` (owner plan §0.4 zero-metered 명령). INVARIANT 4
  가드: `ANTHROPIC_API_KEY` 등 종량 자격증명이 환경에 있으면 러너는 기동
  거부 (`assert_no_metered_credentials` — forward 도구에도 동일 가드).
- **draw 수**: k=1 (v1 발행 규약과 동일 — 재추첨 밴드는 백로그).
- **재시도**: 스키마 불합격·전송 오류 시 동일 입력 재시도 최대 2회
  (v1 러너 규약). 레이트 리밋 시 중단 → 동일 명령 재개 (멱등 — 완료분
  자동 skip, 기채점 레코드 재채점 없음).
- **점수 의미론**: `specs/RISK_SCORE_SEMANTICS.md` — 필드
  `misstatement_risk_score` (0–100 서수) · `evidence_sufficiency` ·
  `assessment_confidence` · `decision_state`.
- **결정 임계 (사전 등록 서수 컷 — 보정 주장 아님)**: score ≥70 → `flag` ·
  40–69 → `review` · <40 → `no_flag` · `evidence_sufficiency=insufficient`
  → 점수 무관 `abstain`. (v1 risk_tier 밴드 70/40과 정렬 — 사이클 간 비교
  가능성.)
- **컨텍스트 격리**: 케이스 간 독립 호출, 세션 재사용 없음.

### 모델 승계 조항 (model-succession clause)

> Each forward cycle is sealed with the model version available and pinned at
> that cycle's screening date. Model providers deprecate versions on
> timescales shorter than this project's 24–48 month outcome horizons.
> Cross-cycle model changes are therefore expected, are recorded as protocol
> version increments in each cycle's `PROTOCOL.md`, and are disclosed in any
> cross-cycle analysis. Within a single cycle, the model version never
> changes after sealing.

이는 공표된 한계이지 결함이 아니다. 전환 판정 규칙은
`specs/MODEL_TRANSITION.md` (사전 등록 D98; 발효 서명 Q-O06 대기)를 따른다.

## 6. 출력 레코드 (scores.json — 레코드당)

`record_id`(중립 ID: `fw001-r01`…) · `company`(채점 측 식별: 사명·티커·CIK
— forward는 라이브 스크리닝이므로 정체 가시) · `misstatement_risk_score` ·
`decision_state` · `evidence_sufficiency` · `assessment_confidence` ·
`top_signals[]` · `benign_alternative_explanations[]`(사실/가설 분리 의무 —
v1.2 출력 스키마는 이 항목을 유도하지 않으므로 cycle_001은 빈 배열로 기록,
프롬프트 확장은 Cycle-2 등록 후보) · `affected_account_areas[]` ·
`cited_sources[]`(accession 인용) · `model_id`/`prompt_sha256`/
`schema_sha256` · `scored_at`.

조립은 `tools/forward_assemble.py`의 **사전 등록 유도 규칙**(모듈 docstring
— sufficiency 비율 컷 1/2·1/5, confidence 평균 컷 2.5/1.5, 서수 결정 컷)
으로만 한다 — 실행 시점 재량 0.

**법적 안전 규칙 (PROJECT.md §6 — 현재 기업)**: "분식/fraud/조작" 단어 사용
금지, 사실(지표)과 가설(해석) 분리, 전 수치 공시 원문 인용, 포지션 없음 +
교육·정보 목적 면책 문구. 워치리스트는 위험 신호의 검토 우선순위이지 위법
주장이 아니다.

## 7. 결과(outcome) 정책 — 계층 라벨

모든 재작성을 사기로 부르지 않는다. 라벨 계층 (성숙 시 상향만, 원 라벨
이력 보존):

1. `aaer_or_final_enforcement` — SEC AAER·최종 집행
2. `item_402_nonreliance` — 8-K Item 4.02 비신뢰 선언
3. `big_r_restatement` — Big R 재작성
4. `sec_complaint` — SEC 제소 (계류)
5. `doj_action` — DOJ 조치
6. `other_material_correction` — 기타 중대 정정
7. `unresolved_event` — 미해결 사건
8. `none_observed` — 관측 없음 (기본)

기록: `outcome_updates.jsonl` append-only (§9).

## 8. 모니터링 지평

사전 등록 검토일: 봉인 후 **6·12·24·48개월** (2027-05·2027-11·2028-11·
2030-11). **주 지평 = 24개월** — 결과 관측 후 변경 금지. 각 검토는
outcome_updates에 일자 기입; 원 점수·원 라벨 상태 무접촉.

## 9. 봉인 메커니즘

디렉토리 (`forward/cycle_001/`): `PROTOCOL.md` · `universe.json` ·
`source_manifest.json` · `scores.json` · `evidence/` · `MANIFEST.sha256` ·
`SEAL_RECORD.md` · `SEAL_RECORD.ots` · `outcome_updates.jsonl`.

도구 (결정론, `tools/`): `forward_prepare.py`(사이클 골격+유니버스 검증) ·
`forward_validate.py`(컷오프·스키마·완료 분율 검증) · `forward_seal.py`
(매니페스트 해시·봉인 기록·OTS 스탬프·push 명령 방출) ·
`forward_verify_seal.py`(봉인 후 무결성 재검증 + 외부 검증 안내) ·
`forward_outcome_append.py`(append-only 결과 기록).

### 외부 검증 가능 타임스탬프 (의무 — git 로컬 타임스탬프만으로 불충분)

1. **GitHub push 증거**: 봉인 즉시 `MANIFEST.sha256` 커밋 + annotated tag
   (`forward-cycle-001-seal`) push. `SEAL_RECORD.md`에 push 기록 + 검증
   방법 명시: GitHub API의 서버 기록 시각
   (`GET /repos/{owner}/{repo}/git/refs/tags/forward-cycle-001-seal` →
   commit의 서버 수신 시각) — 작성자가 소급 조작 불가.
2. **OpenTimestamps 앵커**: `ots stamp MANIFEST.sha256` →
   `MANIFEST.sha256.ots`(= SEAL_RECORD.ots) 커밋. 검증: `ots verify
   MANIFEST.sha256.ots` (무료·무계정, Bitcoin 블록체인 앵커).

지출 $0: GitHub free tier + OpenTimestamps만. 유료 타임스탬프·DB·호스팅
금지.

## 10. 체크포인트·재개 (quota 안전)

- 채점 출력은 레코드당 파일 — 존재+스키마 통과 시 skip (v1 러너 멱등
  규약). 레이트 리밋 중단 후 재실행 = 동일 명령, 기채점 재채점 없음.
- 12호출 규모에서 배치 분할 불요 (1일 1배치) — 산술은
  `governance/DECISION_FORWARD_UNIVERSE.md` §3.

## 11. 봉인 준비 완료 조건

유니버스 결정 기록(§4A) ✅ · 프로토콜 동결(본 문서) · 유니버스 결정론 생성
(`universe.json`) · 컷오프 기계 검증 · 서수 점수 스키마 · 봉인 도구 오프라인
테스트 통과 · 종량 자격증명 거부 가드 · `OWNER_LAUNCH_GATE.md` 1문서.

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
