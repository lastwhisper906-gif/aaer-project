# OWNER_QUEUE.md — 소유자 판단 대기열 (무인 세션이 append, 절대 self-resolve 안 함)

> 이 세션(2026-07-08 야간, OWNER-GATE-E 미션)은 연속 실행 모드다. 소유자 판단이
> 필요한 항목은 여기에 append하고 작업을 계속한다. 각 항목은 소유자가 한 줄로
> 결정 가능하도록 옵션·근거·기본값(default if no answer)을 명시한다.
> 형식: Q-NNN — 질문 / 옵션 / 근거 / 세션 기본 조치 / 상태.

## ⚡ 레버리지 순 요약 (2026-07-16 재작성 — 상세는 아래 개별 항목·docs/HANDOFF.md §게시 절차)

1. **소유자 수동 게시 4종** (HANDOFF §게시 절차의 명령 그대로):
   ① Issue #4 게시 (GIL 메모 — `analysis/ISSUE_4_GIL_MEMO_DRAFT.md` FINAL, 제목 확정본)
   ② RP-18 코멘트 (Issue #2 — `review_packets/RP-18_body.md`)
   ③ Issue #1/#3 편집 (RP-15/16 반영분 — edited 표시 + 사유 코멘트)
   ④ 독자 발송 5–10명 ({ISSUE_URL} 치환 — 미발송 시 Tier 3 검증 0점).
2. **차기 소유자 감독 세션 1번 작업**: 유니버스 열거 — Q-O04 발효분
   (`docs/UNIVERSE_SELECTION.md` §6 확정 · `docs/RESUME.md` 재개 순서).
3. **Q-F02** — Chu et al. 원문 대조 (소유자 직접 — 옵션은 아래 항목).
4. **Q-F07** — 교차 패밀리 채점자 (~20호출 종량 — 옵션은 아래 항목).
5. **Q-F08 실행** — 계획은 사전 등록 완료(D96), 실행은 감독 세션 편승.
6. **Q-M01** — FINRA ToS/라이선스 확인.
7. **Q-M04** — HOLD (Cycle-2 개시 시점 일괄 설계, D96).
8. **Q-M05** — 야간 프롬프트 §5 절단 (재전송/폐기/부분 재지시 선택).
9. **변호사 2종** (screener S-10 증권 · S-13 이민/whistleblower).
10. **Zenodo vs release** (Q-R03 — 경로 확정, 소유자 계정 실행 대기).
- 잔여 launch-ready 지출 옵션 (소유자 임의 시점, 본 재작성 시점 OPEN):
  **Q-M06**(7호출 — E2 j=0 AUC 가능화) · **Q-M07**(P5 32호출 — E5 wave-2 재추첨).
- **2026-07-16 서명 일괄 해소** (owner, 2026-07-16, this session's structured
  decision responses): RP-17 수용(D90) · RP-15/Q-F03·RP-16/Q-F04 적용(D91) ·
  RP-18 발행 승인(D92 — 게시 대기) · Q-O01·Q-O03 서명(D93) · Q-O02 서명(D94) ·
  Q-O04 발효(D95) · Q-F08 계획 등록·Q-M04 HOLD(D96).
- 종전 해소 (요약 이관): Q-F01(D62) · Q-M02(D72/D77~D79) · Q-M03(D56/D57 —
  RP-17 서명 D90으로 원복 경로 소멸) · Q-F05(D84) · Q-F06(D85) · E2 발사
  사슬 완결(D82) · Q-E01/E02/E03 · Q-R01/R02 · Q-R03(경로 확정, 실행 대기).

---

## Q-E03 — E1 무인 실행 보류 (네트워크 대조군 빌드 = §5-1 look-ahead 위험) — **RESOLVED**

- **발견 (실행 가능성 검토)**: E1은 "채점 발사"가 아니라 **2026-era 매칭 대조군 풀을
  새로 빌드**(EDGAR SIC browse + companyfacts fetch, 네트워크)해야 한다 — `~/aaer-data`
  캐시에 홀드아웃 대조군 후보가 없다(wave-2 티커만 존재). 신규 회사의 XBRL을 무인
  fetch하면 각 사의 2026 컷오프에 대한 look-ahead 누출을 **조용히** 낼 수 있고(FPR
  오염), 이는 §5-1(post-cutoff 데이터 접근 필요 시 STOP·보고)의 정지 규칙에 해당.
- **조치**: **E1 무인 실행 보류.** 사전 등록(`HOLDOUT_CONTROLS_PLAN.md`)·순수 선정
  함수는 준비됨. 실행은 **감독 하 1회**(풀 fetch → validate → PROPOSED → 컷오프 검증
  → 채점)로 — wave-2 대조군이 RP-08/09에서 받은 것과 동일한 게이트. 수기 지명 아님.
- **옵션**: (A 기본) 감독 하 실행으로 이관 · (B) 소유자가 "무인 fetch 승인" 시 진행.
- **상태**: **RESOLVED (소유자, 2026-07-09)** — **(A) 감독 하 실행, 최우선.** E1 감독
  실행 + 홀드아웃 k=5 재추첨(W2_MAINSCORE_REDRAW_PLAN §7)을 소유자 입회 세션에서
  최우선 실행. 순서 GNE→HUBG→WMK, 케이스 경계 commit·push (승인 계획
  `~/.claude/plans/i-want-to-solve-happy-moonbeam.md` Phase 3–4).

---

## Q-E01 — E2·E4·E5 미터링 스코어링의 무인 발사 여부 (spend 게이트) — **RESOLVED**

- **질문**: E1(+E3) 이후, E2(조기성 ~160호출)·E4(교차모델 ~20)·E5(wave-2 본채점
  재추첨 ~32) ≈ **212 호출**을 이 무인 세션이 발사할까?
- **맥락 (실측)**: 호출당 벽시계 median 90s·max 435s → 212 호출 ≈ 5–6시간+ 연속
  구독 소진. 본 백그라운드 세션이 소유자의 동일 구독 위에서 실행됨. 미션은 320
  호출을 상한으로 허용하나, 세션은 "quota 소진을 목표로 삼지 않는다"는 실행층
  판단(overrides.md OWNER-GATE-E / J14)에 따라 E1(+E3)에서 미터링을 멈추고 이
  결정을 이관한다.
- **옵션**:
  - **(A) 기본** — E2/E4/E5는 발사하지 않고 **launch-ready 상태로 동결** (사전
    등록·페이로드 빌드 완료). 소유자가 임의 시점에 `docs/RESUME.md`의 정확한
    재개 명령으로 분 단위 발사. → 익일 구독 소진 없음.
  - **(B)** E3만 추가 발사(이미 우선). 나머지는 (A).
  - **(C)** E2·E4·E5 전부 무인 발사 승인 (문자 그대로 run-to-quota, 320 상한).
    → 익일 소유자의 Claude Code 사용이 제한될 수 있음을 인지한 승인.
- **근거**: E1은 H2의 실제 구멍(대조군 분포)을 메워 호출당 가치 최고. E2는 가치
  높으나 최대 단일 spend(~160). E4는 exploratory(각주 1문단). E5는 안정성 밴드
  (최저 우선순위). → 가치/호출 곱이 E1≫E3>E2>E4≈E5.
- **세션 기본 조치 (답 없을 시)**: **(A)** — 무인 미터링을 E1(+E3, 실행 가능 시)로
  한정하고 나머지는 launch-ready 동결. 무-미터링 P-작업은 전량 계속 수행.
- **상태**: **RESOLVED (소유자, 2026-07-11, D40)** — **(A) launch-ready 동결 유지.**
  발행(v1.0)은 현재 동결값으로 진행, E2/E4/E5는 v1.0 이후 소유자 임의 시점에
  `docs/RESUME.md` 재개 명령으로 발사. (E1은 D26에서 이미 감독 실행 완료.)

---

## Q-E02 — wave-2 name-ID rate 발행 규약: 21.9%(동결 규칙) vs 25%(사람 판독) — **RESOLVED**

- **질문**: wave-2 이름 예측(name-ID) rate를 발행물에 어느 값으로 쓸까?
- **발견 (P2 synthesis)**: 동결 `name_match` 규칙 = **21.9%(7/32)**; wave2_summary.md
  산문은 **25%(8/32)**. 차이는 단일 경계 케이스 **DAR(Darling Ingredients)** — 프로브
  응답 "Darling International Inc. (now Darling Ingredients Inc.)"는 명백한 정체 인식이나
  동결 규칙이 구명(舊名) 미처리로 False 판정. (fraud는 양쪽 3/9 동일.)
- **옵션**:
  - **(A) 기본** — 동결 규칙 **21.9%**를 1차 발행값, 25%는 각주 병기(방법론:
    "동결 판정 규칙 재해석 금지", name_probes.py 헤더). synthesis.json은 이미 이 형태.
  - **(B)** 산문 25%를 유지하고 name_match 규칙을 rename-aware로 개정 후 **재동결**
    (재채점 = 프레임 변경, freeze-then-run 재실행 필요 — 비용/이력공개 대상).
  - **(C)** DAR를 "인식"으로 수기 오버라이드 계수(8/32=25%)하고 overrides.md 기록.
- **세션 기본 조치**: **(A)** — synthesis는 21.9% 1차 + 25% 병기. wave2_summary.md
  산문 25%는 **무단 수정 안 함**(재채점 금지); 본 큐 해소 시 소유자 규약대로 정합.
- **정성 불변**: 어느 값이든 name-ID 50%→~22–25%→0% 반감 서사·R4 결론 불변.
- **상태**: **RESOLVED (소유자, 2026-07-11, D40)** — **(A) 동결 규칙 21.9% 1차
  발행값 + 25%(rename-aware 사람 판독, DAR 경계 케이스) 각주 병기.** 정합 적용:
  README 양어·synthesis는 이미 이 형태(무변경), ISSUE_1은 DIFF-3 수정 적용에
  통합(RP-14 서명 절), wave2_summary.md §4 산문은 본 규약으로 정합 (D40).

---

## Q-R01 — Issue #1/#2 서사 보강 diff 서명 (D31 0-5 + D39 A-1, RP-14 DIFF-1/2/3) — **RESOLVED**

- **질문**: RP-14의 diff 3건을 적용할까? — DIFF-1: `ISSUE_2_HOLDOUT_DRAFT.md` §3
  crux 문단에 "After E1, the holdout evidence rests on a single robust case
  (HUBG, 5/5 redraws)" 병기 · DIFF-2: §2 gate k=5 band 병기 · DIFF-3 (D39 신규):
  `ISSUE_1_WAVE2_DRAFT.md` §5 논증 사슬 재배선 ("덜 유명 → 덜 암기 → 잔여 능력"이
  D35 실측 outcome-knowledge 8/9와 모순 — 발행 전 필수, 3차 외부 검토).
  Issue #1/#2 발행 서명에 선행하는 항목.
- **옵션**: (A 기본) diff 그대로 적용 · (B) 문구 수정 후 적용 · (C) 기각
  (사유 → overrides.md).
- **근거**: 3차 외부 검토 — "weakens but does not collapse" 서사가 단일 케이스
  의존(HUBG 1/3만 분리, E1 D26)을 명시하지 않으면 3케이스 전반 신호 잔존으로
  오독됨. 데이터: `holdout_controls_results.json` + D27 k=5 (HUBG 5/5·WMK/GNE 0/5).
- **세션 기본 조치**: 미적용 유지 (diffs only — 서명 전 draft 본문 무변경).
  단 §3b의 GRDX 78 사실 병기는 미션 0-1의 직접 지시로 이미 반영됨 (D31).
- **연동**: Phase 1(recognition gate k=5, D32)에서 HUBG가 knows_event ≥2/5로
  자격 상실 시 본 diff 무효 + **Issue #2 발행 보류** 긴급 항목이 우선.
  → **실측 (D33)**: HUBG·WMK·GNE 전건 0/5, 자격 유지 — 긴급 항목 비발동.
  RP-14에 **DIFF-2**(§2 gate k=5 band 병기) 추가 — 서명 대상 2건으로 확대.
  → **D39 (2026-07-11)**: RP-14에 **DIFF-3**(Issue #1 §5 재배선, 발행 전 필수)
  추가 — 서명 대상 3건으로 확대.
- **상태**: **RESOLVED (소유자, 2026-07-11, D40)** — DIFF-1/2 적용 · DIFF-3
  수정 적용(Q-E02(A) 정합: 21.9% 1차 + 25% 각주). 적용기
  `tools/apply_rp14_diffs.py`, 서명 기록 RP-14 하단 + decisions_log D40.

---

## Q-R02 — freeze 개정 #3 (피평가자 raw API 이행) 발효 여부 — **RESOLVED (GO)**

- **질문**: 피평가자 호출을 하네스(`claude -p`)에서 순수 Anthropic SDK로 옮기는
  freeze 개정 #3(`docs/FREEZE_REV3_DRAFT.md`)을 발효할까? L-2(J13-e
  currentDate/system-reminder 주입)·W8(2차 검토)의 해소 경로. **스캐폴드는 커밋
  완료** (`pipeline/api_client.py`·`runner_api.py`·무호출 테스트 5건) — 이중
  안전장치(AAER_RAW_API_APPROVED=1 + API 키)로 발효 전 실행 불가.
- **소유자 인프라 결정 3건** (세션 권한 밖): ① INVARIANT 4(구독 OAuth 전용) 개정
  + API 키 발급·보관 ② 종량 과금 예산 (동치성 테스트 ~30호출 + 이후 배치)
  ③ 발효 시점 (권장: E2 조기성 발사 전 — 조기성 결과가 처음부터 깨끗한 경로에 섬).
- **옵션**: (A) 발효 + 동치성 테스트부터 (FREEZE_REV3_DRAFT §3 설계 그대로) ·
  (B) 보류 (스캐폴드 동결 유지, 언제든 분 단위 재개) · (C) 기각 (사유 기록).
- **세션 기본 조치**: 없음 — **동결 결과 재실행 금지** 불변, 기존 러너는 어떤
  것도 api_client를 import하지 않음 (테스트가 인터페이스 동일성만 검증).
- **상태**: **RESOLVED (소유자, 2026-07-11, D40)** — **(A) GO, 다음 실행
  배치부터 발효 확정.** 이번 세션은 실행/과금 배선 없음 — 래치 해제 조건
  (키 주입 방식·E2 전 스모크 테스트 계획)은 `docs/FREEZE_REV3_DRAFT.md`
  §6(신설)에 문서화. 동결 결과 재실행 금지 불변. 소유자 잔여: API 키 발급·
  종량 예산 승인 (실행 개시 시점에).

---

## Q-R03 — Zenodo DOI 연동 (v1.0.0 릴리스의 인용 가능 DOI) — **RESOLVED (경로 확정, 실행 대기)**

- **질문**: v1.0.0 GitHub Release에 Zenodo DOI를 붙일까? (소유자 계정 필요 —
  세션 권한 밖, 자동화 금지 대상.)
- **3줄 절차**: ① zenodo.org 로그인(GitHub 계정 연동) → Settings → GitHub에서
  `lastwhisper906-gif/aaer-evals` 토글 ON. ② GitHub에서 릴리스를 새로 발행해야
  Zenodo가 아카이브를 생성하므로, 토글 후 v1.0.1 태그(문서 무변경, DOI 전용) 또는
  기존 v1.0.0의 재발행(edit→publish)으로 웹훅 트리거. ③ 발급된 DOI 배지를 README
  '발행/Publication' 절에 추가 (인용 형식은 Zenodo 페이지가 자동 생성).
- **근거**: 릴리스 노트에 "release = citable freeze point"를 명시했으나 DOI가
  있어야 학술 인용·영속 아카이브가 보장된다. GitHub URL은 계정/repo 이름 변경에
  취약(이미 D30에서 rename 1회).
- **세션 기본 조치**: 없음 (소유자 계정 작업).
- **상태**: **RESOLVED (소유자, 2026-07-12, D43)** — 경로 (A) **토글 + v1.0.0
  재발행** (릴리스 삭제→동일 태그·동일 노트 재생성, 웹훅 트리거; annotated
  tag·URL 불변 = 단일 동결점 유지). 실행은 소유자 계정 작업으로 대기 —
  DOI 발급 후 배지 README 반영은 세션 몫.

---

## Q-F01 — HUBG submissions 하위 파일 1건 미캐시 (payload-v2 coverage 구멍) — **RESOLVED (D62, 2026-07-13)**

> 해소: CIK0000940942-submissions-001.json (547건, 1996-05~2007-11) fetch·캐시
> (UA 규약)·매니페스트 512 등재. payload_v2 재생성 diff = case_71+COVERAGE만
> (partial 0, 82/82 완전). HUBG b3_score W4/W8 동결값 대비 기계 대조 무변화
> (1996–2007 제출은 어떤 B3 창과도 비교차) — B3·라벨링 비영향 확증.

- **발견 (WS-1/D44 실측)**: `~/aaer-data/HUBG/edgar/` 본체 JSON의 `filings.files`가
  `CIK0000940942-submissions-001.json` (1996-05-15~2007-11-12 구간)을 열거하나
  로컬 미캐시. 세션은 fail-closed 규약(fetch 금지)에 따라 coverage에만 기록 —
  `runs/diagnostics/payload_v2/COVERAGE.json` partial 1/82.
- **영향 범위**: payload-v2 진단의 HUBG 8-K 전 이력 완전성만. **B3(WS-2)·라벨
  태깅(WS-3)은 무영향** — HUBG 컷오프 2026-02-04의 최장 윈도(W8×4 = 2018년까지)가
  2007년 이전에 도달하지 않음.
- **옵션**: (A 기본) 소유자가 `tools/fetch_primary_sources.py` 경로로 해당 파일
  fetch 후 `verify_manifest.py --write` + README "(N 파일)" 갱신 → payload-v2
  재실행 · (B) 방치 (진단 계열 영향 0 문서화로 충분).
- **세션 기본 조치**: 없음 (fetch 금지 — 계약 9).

---

## Q-F02 — Chu/Dechow/Hui/Wang (2018) 정확 수치 인용의 원문 대조 — OPEN

- **맥락 (WS-3/D46)**: 라벨 기저율 문서화(specs/label_taxonomy.md §3,
  LABEL_REPORT §2)는 Chu et al. 2018을 "AAER 조사 대부분이 재작성 계기"라는
  **정성 방향으로만** 인용한다. 이 논문의 정확 퍼센트를 발행 표면에 쓰려면
  소유자가 원문 해당 문장을 직접 대조해야 한다 (2차 인용 금지).
- **옵션**: (A 기본) 정성 인용 유지 (수치 불사용) · (B) 소유자 원문 대조 후
  정확 수치+페이지 인용으로 승격.
- **세션 기본 조치**: (A) — 산출물 전부 정성 인용으로 작성 완료.
- **상태**: OPEN

---

## Q-F03 — RP-15 라벨 명명 diff (DIFF-4/DIFF-5) 서명 — **RESOLVED (2026-07-16)**

- **질문**: 발행 표면의 홀드아웃 라벨 서술에 "Big R (Item 4.02 non-reliance)"
  정밀화 + 기저율 한정 + 4년 모니터링 윈도를 반영할까?
  (`review_packets/RP-15_label_naming_diff.md` — ISSUE_2 §7 불릿 교체 +
  README 양어 1문장.)
- **근거**: 기계 태깅 3/3 bigR (accession 증거, `analysis/label_tags_holdout.json`);
  기저율 ~2.2%(Karpoff et al. TAR 2017)가 잠정 라벨의 노이즈를 정직 한정.
- **옵션**: (A) 적용 (GitHub Issue #3은 edited 표시 + 사유 코멘트 병행) ·
  (B) 문구 수정 후 적용 · (C) 기각 (사유 → overrides.md).
- **세션 기본 조치**: 미적용 유지 (diff-only).
- **상태**: **RESOLVED (owner, 2026-07-16, this session's structured decision
  responses)** — **(A) 적용.** repo 표면(ISSUE_2 초안·README 양어) 반영 완료
  (D91). GitHub Issue #3 본문 편집 + 사유 코멘트는 소유자 잔여 작업
  (명령은 HANDOFF §게시 절차).

---

## Q-F04 — RP-16 보정 언어 diff (DIFF-6/DIFF-7) 서명 — **RESOLVED (2026-07-16)**

- **질문**: 발행 표면의 확률 함의 언어 2건을 서수(ordinal) 규약으로 교체할까?
  (ISSUE_0 §5 "these probabilities are rankings" 문장 강화 + ISSUE_2 표 헤더
  `LLM p` → `LLM score (0–100, ordinal)`.)
- **근거**: specs/calibration_scope.md — ECE 0.209/0.179 개선 없음, N≈30–60
  재보정은 노이즈 지배, 점수는 순위·플래그로만 검증됨. 스키마 필드
  `misstatement_probability`는 무변경 (Cycle-2 개명 등록 — 재현성).
- **옵션**: (A) 적용 (Issue #1/#3 edited 표시 + 사유 코멘트) · (B) 문구 수정
  후 적용 · (C) 기각 (사유 → overrides.md).
- **세션 기본 조치**: 미적용 유지 (diff-only).
- **상태**: **RESOLVED (owner, 2026-07-16, this session's structured decision
  responses)** — **(A) 적용.** repo 표면(ISSUE_0 §5·ISSUE_2 표 헤더) 반영
  완료 (D91). 스키마 필드 무변경(Cycle-2 개명 등록 유지). GitHub Issue
  #1/#3 편집은 소유자 잔여 작업 (HANDOFF §게시 절차).

---

## Q-F05 — perturbation-v2 name-ID 프로브 런 (launch-ready, 미터링 62호출) — **RESOLVED (2026-07-13)**

- **질문**: v2 날짜 이동 페이로드로 name-ID 프로브를 재실행할까?
  (specs/perturb_v2.md §5 — 사전 등록 엔드포인트: v2 rate vs 동결 v1
  wave-1 **50% [15/30]** · wave-2 **21.9% [7/32]**, 동일 프로브 문구·동일 k.)
- **호출 산술 (repo 계수)**: wave-1 프레임 30 (`name_probe_results.json`
  n_probes=30) + wave-2 32 (`cases_wave2.json` 전건) = **62 호출**. 홀드아웃
  제외 (v1 name-ID 기준선 부재 — 정체 가시 프레임).
- **구현 상태**: `pipeline/date_shift.py` + 테스트 8건 커밋 완료 (무비용 위생
  포함). 실행은 러너 배선 + 미터링 승인 대기.
- **위생 주의 (구현 중 실측)**: 주-단위 오프셋이 원본 날짜쌍 차와 일치하면
  (364일 = 52주 = 역년 start↔end) 이동 날짜가 다른 원본 날짜 문자열 위에
  착지하는 **양성 충돌**이 있다 — 발사 전 위생 스캔은 케이스별로 오프셋 ∉
  날짜쌍 차 집합을 확인하고, 충돌 케이스는 필드 단위 이동 검증으로 대체
  (`test_date_shift.py::test_collision_property_documented` 실증).
- **옵션**: (A) E 배치(E2+E4)와 같은 창에서 발사 · (B) 별도 시점 · (C) 보류.
- **세션 기본 조치**: 없음 (launch-ready 동결 — 미터링 0 계약).
- **상태**: **RESOLVED (owner, 2026-07-13, written overnight authorization —
  this mission's prompt, §A-5)** — **(A-변형: 금야 창) 발사 승인.** 전제 순서
  고정: ① date_shift 러너 배선(spec §5) ② 발사 전 위생 스캔(케이스별 오프셋
  ∉ 원본 날짜쌍 차 집합, 충돌 케이스는 필드 단위 이동 검증 대체) ③ 테스트+
  5게이트 — 전부 무호출·커밋 후 62호출. 엔드포인트 사전 등록 그대로
  (v1 wave-1 50% [15/30] · wave-2 21.9% [7/32], 동일 문구·동일 k, 홀드아웃 제외).

---

## Q-F06 — WS-6 median-of-3 발사 예산 게이트 (launch-ready) — **RESOLVED (2026-07-13)**

- **질문**: specs/draw_k3.md의 k=3 median 병기 1차값 런을 발사할까?
- **예산 (repo 계수 산술)**: (A) 전량 신규 = (30 wave-1 + 32 wave-2) × 2draw
  = **124 피평가자 호출, 채점자 0** · (B) wave-1 treatment 8은 커밋된
  hardening draw_2/3 재사용 = **108 호출** (grades 병합 금지 규약 불변 —
  median은 통계 병기).
- **산출**: flip-rate 표 (사전 등록) + median 분리 통계 병기. 동결 draw-1
  발행 수치 불변. 홀드아웃 k=5 유지.
- **옵션**: (A) 124 신규 · (B) 108 재사용 · (C) 보류.
- **세션 기본 조치**: 없음 (spec only — 미터링 0 계약).
- **상태**: **RESOLVED (owner, 2026-07-13, written overnight authorization —
  this mission's prompt, §A-6)** — **(B) 108호출.** wave-1 treatment 8케이스는
  커밋된 hardening draw_2/3 재사용, 나머지 (30−8)×2 + 32×2 = 108 신규.
  산출 = specs/draw_k3.md 그대로 flip-rate 표 + median 분리 통계 **주석 병기**
  (grade 병합 금지, draw-1 발행 수치 불변, 홀드아웃 k=5 유지).

---

## Q-F07 — WS-7 교차 패밀리 채점자 게이트 (launch-ready, E4 동배치) — OPEN

- **질문**: specs/cross_grader.md의 비-Anthropic 채점자 n=20 스팟체크를
  발사할까? 소유자 결정 3건: ① 채점자 모델 선정 (실행 시점 최강 가용
  비-Anthropic — 스펙은 사전 지명 안 함) ② API 키·과금 (~20호출, 종량)
  ③ 실행 창 (권장: 이미 launch-ready인 E4 교차모델 런과 같은 배치 —
  D43 계획 4의 E2+E4 창).
- **사전 등록 판독**: κ ≥ 0.6 양 차원 → 결론 유지 · κ < 0.6 → 해당 주관
  차원 "grader-dependent" 강등 diff 의무 (동결값 불변).
- **옵션**: (A) E4 배치에 편승 발사 · (B) 별도 시점 · (C) 기각.
- **세션 기본 조치**: 없음 (spec only).
- **상태**: OPEN

---

## Q-F08 — 대조군 풀 생존 편향(survivorship) 감사 — **RESOLVED (2026-07-16, 계획 등록)**

- **발견 (WS 외 등록 — 미션 지시)**: 대조군 풀이 **현재 시점** EDGAR SIC
  browse에서 열거되었다면, 상장폐지·등록취소(deregistered) 제출자가 풀에서
  과소 표집되었을 수 있다 — 생존한 회사만 대조군 후보가 되는 방향의 편향
  (대조군을 "깨끗한 생존자" 쪽으로 기울여 분리를 과대평가할 수 있는 축).
- **감사 경로**: 풀 수집 시점의 SIC browse 스냅샷( `runs/rp08/`,
  `runs/rp09/` 커밋 산출물)을 Form 25(상장폐지)·Form 15(등록취소) 기록과
  대조 — 수집 당시 이미 살아있던 회사 중 이후 폐지된 비율과, 실험군
  컷오프 연도 기준으로 그때 존재했으나 지금 없는 회사의 누락 규모 추정.
- **옵션**: (A) 다음 무-미터링 세션에서 감사 스크립트 (EDGAR full-text
  아님, 로컬+무료 인덱스 범위 확인 필요 — 네트워크 필요 시 소유자 감독) ·
  (B) 한계 절(L-8 후보)로만 기입 · (C) 기각.
- **세션 기본 조치**: 등록만 (열린 소유자 항목).
- **상태**: **RESOLVED (owner, 2026-07-16, this session's structured decision
  responses)** — **감사 계획만 사전 등록** (`docs/SURVIVORSHIP_AUDIT_PLAN.md`,
  판독 규칙 §3 사전 고정, D96). 실행은 차기 감독 세션 (RESUME.md 2번 작업,
  네트워크 필요분 Q-E03 선례).

---

## Q-M01 — FINRA 공매도 잔고 데이터 ToS/라이선스 확인 — OPEN

- **맥락**: B4 기준선(specs/B4_short_interest.md, D55)이 FINRA Consolidated
  Short Interest 공개 파일(cdn.finra.org)을 사용. 내부 분석·회고 채점은 공개
  데이터 사용 범주이나, **발행물(리포트·seal 공개 파일)에 FINRA 파생 수치를
  게재할 때의 라이선스/귀속 조건**은 소유자가 FINRA 데이터 이용약관에서 확인.
- **옵션**: (A) 약관 확인 후 귀속 문구 추가로 게재 · (B) 파생 통계(순위·정밀도)만
  게재하고 원수치 비게재 · (C) FINRA에 서면 문의.
- **세션 기본 조치**: 게재 전 확인 필요 항목으로 등록만. B4_REPORT는 저장소 내부
  문서 (발행 표면 아님).
- **상태**: OPEN

## Q-M02 — FINRA 과거 공표일(dissemination date) 실측 입수 가능성 — **RESOLVED (D72/D77~D79, 2026-07-13 — 구현 완결)**

> 구현 완결: D72(도구+데이터 223행+아카이브) → D77(스펙 §14, 재실행 전 커밋
> 7a12bb8) → D78(소비자 배선·E2 관할 핀) → D79(재실행 — holdout 경계 3건 편입,
> 헤드라인 불변). GO 인용 = (owner, 2026-07-13, written overnight authorization
> — this mission's prompt, §A-8).

> 조사 완료 (analysis/DISSEMINATION_DATES_MEMO.md): Wayback 연도별 스냅샷에서
> 3열 일정표 복원 가능 (2020 표본 파싱 검증 — 관측 지연 11–12일 ≤ LAG 14).
> 잔여 결정: 구현 GO/NO (1세션 분량, 스펙 개정 D-엔트리 동반 — 메모 §3 계획).

- **맥락**: B4 PIT 규칙은 보수 상수 LAG=14일(결제일→공표일)을 사전 등록. FINRA는
  연도별 Short Interest Reporting Deadlines 표(공표일 포함)를 게시하므로, 과거
  연도 표를 수집하면 상수를 실측 공표일로 대체 가능 (더 정확, 덜 보수적).
- **제약**: 대체는 **신규 D-엔트리로 스펙 개정 후에만** (specs/B4_short_interest.md
  §2 — 사후 완화 금지 조항).
- **옵션**: (A) 과거 일정표 수집 지시 (무-미터링 세션 작업 가능) · (B) LAG=14 유지.
- **세션 기본 조치**: 등록만.

---

## Q-M03 — B4 분모 폴백 스펙 개정 (holdout 커버리지 7/12 원인 교정) — **RESOLVED (병렬 실행됨, 소유자 revert 경로 유지)**

- **발견 (B4 1차 실행, 커밋 287a92a)**: 스펙 §6 기대 커버리지 holdout 12/12,
  실측 **7/12 (58%)** — 70% 바 미달로 holdout까지 서술 전용. 원인: SIR 분모가
  `dei:EntityCommonStockSharesOutstanding` 단일 태그인데, 다중 클래스 발행사는
  companyfacts가 클래스별(차원) 사실을 평탄화하지 않아 해당 태그가 체계적으로
  결측 (fail-closed로 케이스 탈락 — 대체·보간 금지 규칙은 정상 작동).
- **교정 후보 (전부 스펙 §3 변경 = 신규 D-엔트리 사전 등록 후에만)**:
  (A) 분모 폴백 사다리 등록 — dei 단일 → us-gaap CommonStockSharesOutstanding →
  WeightedAverage 계열 (스펙에 순서 고정, 클래스 합산 규칙 명시) ·
  (B) 현상 유지 + 커버리지 한계 문서화 (첫 seal의 워치리스트 b4 필드도 동일
  분모라 null 비율이 그대로 전이됨을 수용) · (C) 다중 클래스 발행사만 별도
  집계 규칙.
- **권고**: 첫 seal(2026-11-15) 전 해소 — sealed 엔트리의 `b4_level/slope_aug`
  null 비율이 프로토콜 §2의 selection_note 부담으로 직결된다.
- **세션 기본 조치**: 등록만 (스펙 개정은 소유자 승인 D-엔트리로).
- **상태**: **RESOLVED (2026-07-13 병합 세션)** — 병렬 워크트리 세션이 옵션 (A)
  분모 폴백 사다리를 **D56 스펙 §13 개정(재실행 전 커밋) + D57 재실행**으로
  이미 실행 (holdout 7/12 → **10/12 (83%)**; 비교 성립 tier는 여전히 없음 —
  holdout 동결 LLM AUC 부재). 본 큐 등록과 병렬 실행이 겹친 중복이었다.
  **소유자 기각 경로 보존** (병렬 세션 정합 노트 그대로): D56/D57 기각 시
  결과 커밋 revert로 원복 — 동결 발행 수치 무접촉.

---

## Q-M04 — Cycle-2 등록: 설명가능성(explainability) 채점 설계 — **HOLD (2026-07-16)** (원번호 Q-M03 재부여)

- **맥락**: screener stage-2 출력 계약이 계정 수준 가설 스키마로 고정됨
  (screener/schemas/flag_explanation.json + validate_explanation.py 기계
  검증 — 접지성(groundedness)은 기계가 강제). 그러나 **가설의 품질**(기제
  타당성·증거 적합성·반증 조건의 예리함) 채점은 평가 설계 문제 — Cycle-2
  aaer-evals 질문으로 등록. 이 세션은 등록만, 설계·구축 없음
  (docs/FUTURE_CYCLE_PROTOCOL.md 절차를 따를 것).

- **상태**: **HOLD (owner, 2026-07-16, this session's structured decision
  responses)** — 정당 보류: "Cycle-2 개시 시점에 일괄 설계 — 현재 어떤
  하류 작업도 이에 막혀 있지 않다 (첫 seal 2026-11-15)." 발행·발송 크리티컬
  패스 우선 (D96).

---

## Q-M05 — 야간 미션 프롬프트 §5(zero-call backlog B-1…B-10) 절단 — OPEN (신규, 2026-07-13 야간)

- **발견**: 2026-07-13 야간 서면 승인 프롬프트가 §4 P1 항목 2 중간에서 절단됨 —
  §5(zero-call backlog B-1…B-10 목록)와 §4 잔여가 세션에 도달하지 않았다.
  §A-9가 B-1…B-10을 포괄 승인하고 §1이 "B-4 citation check"(publisher/journal
  페이지 네트워크 허용)를 언급하나, **목록 자체가 부재**.
- **세션 조치**: 미도달 목록을 추측 실행하지 않는다 (self-resolve 금지 규약의
  연장). 레이트 리밋 대기 블록의 zero-call 작업은 **명시 승인된 A-8**(공표일
  재구성 구현)과 P-큐 전처리(P3 배선 등)로 대체 수행. B-4가 Q-F02(Chu et al.
  원문 대조)를 지시하는 것으로 추정되나, Q-F02는 "소유자 직접 대조" 조건이
  걸려 있어 추정 실행 시 이중 위반 위험 — 보류.
- **옵션**: (A) 소유자가 §5 전문 재전송 (차기 세션 실행) · (B) B-목록 폐기,
  A-8+P-큐로 충분 · (C) B-4만 Q-F02 완화와 함께 재지시.
- **세션 기본 조치**: A-8을 백로그 작업으로 사용, B-목록은 미실행.
- **상태**: OPEN

---

## Q-M06 — v1 대조군 perturbed j=0 채점 7호출 (E2 LLM j=0 AUC 계산 가능화) — OPEN (신규, 2026-07-13 야간)

- **발견 (D71)**: E2 대조군(RP-01 v1 대조군 7건 buildable)은 perturbed 프레임
  동결 점수가 없어 어댑터가 j=0 llm_p를 null로 기록 — engine_verdict의 LLM
  j=0 AUC가 fail-closed null (플래그 병기). **§4 브랜치 판정은 무영향**
  (실험군 median lead만 소비); 잃는 것은 j=0 AUC 병기와 b_strict/b_residual
  하위 라벨 선명도뿐.
- **옵션**: (A) 7호출 승인 — `pipeline/runner.py --perturbed --only case_04
  case_05 case_07 case_10 case_11 case_14 case_15 --out runs/perturbed` (동결
  러너 그대로, 멱등; 완료 후 e2_runner --postrun-only 재실행이 AUC를 채움) ·
  (B) null 유지 (플래그가 이미 정직 기록).
- **주의**: (A) 실행 시 이 7건은 draw-1이 아니라 **2026-07 신규 draw**임을
  verdict D-엔트리에 명기해야 한다 (실험군 j=0은 2026-07-06~09 draw-1 —
  시점 비대칭 각주 의무).
- **세션 기본 조치**: (B) — 미션 사전 승인 외 지출이므로 실행 안 함.
- **상태**: OPEN

---

## Q-M07 — P5(E5 wave-2 본채점 재추첨 arm) 캡 잔여 부족으로 미발사 — OPEN (2026-07-13 야간)

- **산술**: 야간 캡 380 중 351 지출 (재지출 16 + 재시도 1 포함) — P5 32호출은
  383 > 380으로 발사 불가. launch-ready 동결 유지 (W2_MAINSCORE_REDRAW_PLAN).
- **발사 명령**: `python pipeline/runner.py --cases data/evaluatee/cases_wave2.json
  --out runs/wave2/mainscore_redraw/draw_2` (멱등) → 부분/전체 밴드 분석.
- **상태**: OPEN (소유자 임의 시점 — 종전 launch-ready 동결과 동일 지위)

---

## Q-O01 — OUT-GIL-V1 소비 가능 산출물 서명 게이트 (GIL 블라인드 메모 v1) — **RESOLVED (2026-07-16)**

- **대상**: (1) `runs/gil_memo_v1/citation_adjudication.md` — 비-VERIFIED 인용 5건
  수기 판정(전부 "…" 병합 인용, 날조 0) 서명; (2) 메모 승인 —
  `output/GIL_memo_v1.md` (과제 규격 영문판, 검증표 부록 포함) +
  `runs/gil_memo_v1/memo_draft.md` (한글 발행용 초안). 서명 전 외부 공개 금지.
- **추가 사실 검증 (memo assembly 단계, 판정 파일 미수록)**: 모델 서술의
  "$201.6 million"(연차 공시상 step-up 추정 총액)은 원문 부재 — 40-F MD&A는
  **총액 $237M**을 명시하며, $201.6M = 237.0 − 35.4(FY2025 인식분)의 파생값.
  Q1 인식 $106.3M + 잔여 $95M ≈ $201.6M로 산술 정합. memo Flag 1에 assembly
  note로 명기 완료 — 서명 시 이 판정도 함께 확인 요망.
- **상태 갱신**: **RESOLVED (owner, 2026-07-16, this session's structured
  decision responses)** — 서명 + $201.6M 파생값 노트 확인. 판정 파일·양판
  memo 서명 블록 기입, 원장 D93.
- **병렬 세션 병합 기록**: 08be4ee(20:38, 데이터·평가 2호출·검증·한글 초안 커밋)
  + 본 커밋(과제 규격 memo·원장·큐) — 동일 실험의 분업, 수치 충돌 없음.

---

## Q-O02 — DECISION_TABLE 서명 게이트 (임계·비용 결정 표, README 링크 전제) — **RESOLVED (2026-07-16)**

- **대상**: `analysis/DECISION_TABLE.md` (서명 전 초안) + 수치 원본
  `analysis/decision_table.json`. 사전 등록 `analysis/DECISION_TABLE_PLAN.md`
  (계산 전 단독 커밋 2fc3d23 — freeze-commit-then-run 준수 증거).
- **내용 요약**: 임계 {40,50,60,70} × 4레이어, 전 셀 CP95 병기, 탐지당 비용
  ($0.5304/스크린 인용). 주 서술 = "궤적 레이어에서 단독 LLM 임계는 지배
  전략 없음". EXPLORATORY 결합 규칙(B3≥2 AND llm_p≥T)은 오탐 0/7이나
  사후 규칙 — Cycle-2 sealed 후보로만 등록 (D87).
- **검토 포인트**: ① L1 프레임 비대칭 서술(§1) ② L3 "이벤트 플래깅" 명칭
  (G2 잠정 라벨) ③ §5 EXPLORATORY 격리가 충분한가 ④ §4 읽기 문단의 서술
  수위.
- **옵션**: (A) 서명 → README '발행/Publication' 절에 링크 (별도 커밋) ·
  (B) 문구 수정 후 서명 · (C) 기각 (사유 → overrides.md).
- **세션 기본 조치**: README 무접촉 유지 (서명 전 링크 금지).
- **상태**: **RESOLVED (owner, 2026-07-16, this session's structured decision
  responses)** — **(A) 서명.** DECISION_TABLE 헤더 서명일 기입 + README 양어
  Publication 절 링크(한 줄 요약 병기) 반영, 원장 D94.

---

## Q-O03 — GIL 메모 발행 패키지 서명 (Issue #4 텍스트 + 보강 2건 — Q-O01 연동) — **RESOLVED (2026-07-16)**

- **대상 (Q-O01의 서명 대상이 이번 세션에서 보강됨 — 서명은 보강본 기준)**:
  1. **선정 배경 공개 절 추가** — `runs/gil_memo_v1/memo_draft.md`(한글)·
     `output/GIL_memo_v1.md`(영문) 양판. 내용: Jehoshaphat 리포트(2026-06-16)
     인지 후 선정 + 입력 컷오프 2026-06-15 코드 강제 → "무작위 스크리닝
     적중"이 아니라 **봉인된 사전-리포트 복제**. §2 가치 기준 1(참)의
     방어선 — 이 절 없이 발행하면 과장이 된다.
  2. **증거 라인 부록** — `analysis/EVIDENCE_LINES.md` (동결 51케이스
     체크리스트 flag 빈도 실험군/대조군 정직 병기 + 유형별 원문 인용
     accession 병기 + HUBG 박스 README 범위 내). 신규 주장 0.
  3. **Issue #4 게시 최종 텍스트** — `analysis/ISSUE_4_GIL_MEMO_DRAFT.md`
     (제목 2안, §6 자가 감사 7항목 PASS 표 첨부, 게시 전 체크리스트 포함).
- **참고**: runs/gil_memo_v1/memo_draft.md 수정에 따라 runs/MANIFEST.sha256
  재생성 (verify_blindness --write-manifest, 게이트 PASS). "ISSUE_3_DRAFT"
  파일은 저장소에 없음 — Issue #3은 ISSUE_2_HOLDOUT_DRAFT.md에서 게시된
  전례를 따름.
- **옵션**: (A) 서명 → 소유자가 Issue 게시 + README 링크 + 독자 5–10명 발송
  (발송 없으면 Tier 3 검증 0점) · (B) 문구 수정 후 서명 · (C) 기각
  (사유 → overrides.md; 보강 2건 revert는 커밋 단위 원복).
- **세션 기본 조치**: 게시·발송 안 함 (소유자 전용 작업).
- **상태**: **RESOLVED (owner, 2026-07-16, this session's structured decision
  responses)** — **(A) 서명, 제목 proposal 1 확정.** ISSUE_4 초안 FINAL 승격
  (D93). 게시·독자 발송은 소유자 잔여 (HANDOFF §게시 절차).

---

## Q-O04 — UNIVERSE_SELECTION 발효 서명 (SIC 집합 확정 — 열거 개시 게이트) — **RESOLVED (2026-07-16)** (원번호 Q-O03 병렬 랜딩 재부여)

- **대상**: `docs/UNIVERSE_SELECTION.md` (D89 사전 등록). EQ 모니터 유니버스의
  기계 선정 기준 — 서명 + §6 SIC 집합 선택 전에는 어떤 세션도 후보 기업을
  조회하지 않는다 (문서 §0 — 순서가 방어).
- **옵션 (§6)**: (A 기본) 하드웨어·전력 사슬 협의 12개 SIC · (B) 소프트웨어
  포함 광의 · (C) 협의 − 유틸리티. 부수 확정: 선정 수 12 (8~15 중앙) 유지 여부,
  float 하한 $1B 유지 여부.
- **근거**: GIL 판례 — 선정이 기준보다 먼저 오면 산출물이 영구히 "사후 선택"
  각주를 단다. 첫 열거 이후 개정은 FREEZE_REV+D-엔트리로만.
- **세션 기본 조치**: 없음 (서명 전 열거 금지 — 네트워크 작업 자체가 소유자
  입회 사안, Q-E03).
- **상태**: **RESOLVED (owner, 2026-07-16, this session's structured decision
  responses)** — **옵션 (A) 협의 SIC 집합 · 선정 수 12 · float ≥$1B 확정,
  발효.** §6 확정 절 기입 + FREEZE 조항 재확인 (D95). 열거는 차기 감독
  세션 1번 작업 (RESUME.md) — 본 세션 네트워크 작업 없음.
