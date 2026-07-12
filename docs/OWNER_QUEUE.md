# OWNER_QUEUE.md — 소유자 판단 대기열 (무인 세션이 append, 절대 self-resolve 안 함)

> 이 세션(2026-07-08 야간, OWNER-GATE-E 미션)은 연속 실행 모드다. 소유자 판단이
> 필요한 항목은 여기에 append하고 작업을 계속한다. 각 항목은 소유자가 한 줄로
> 결정 가능하도록 옵션·근거·기본값(default if no answer)을 명시한다.
> 형식: Q-NNN — 질문 / 옵션 / 근거 / 세션 기본 조치 / 상태.

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

## Q-F01 — HUBG submissions 하위 파일 1건 미캐시 (payload-v2 coverage 구멍) — OPEN

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
- **상태**: OPEN

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

## Q-F03 — RP-15 라벨 명명 diff (DIFF-4/DIFF-5) 서명 — OPEN

- **질문**: 발행 표면의 홀드아웃 라벨 서술에 "Big R (Item 4.02 non-reliance)"
  정밀화 + 기저율 한정 + 4년 모니터링 윈도를 반영할까?
  (`review_packets/RP-15_label_naming_diff.md` — ISSUE_2 §7 불릿 교체 +
  README 양어 1문장.)
- **근거**: 기계 태깅 3/3 bigR (accession 증거, `analysis/label_tags_holdout.json`);
  기저율 ~2.2%(Karpoff et al. TAR 2017)가 잠정 라벨의 노이즈를 정직 한정.
- **옵션**: (A) 적용 (GitHub Issue #3은 edited 표시 + 사유 코멘트 병행) ·
  (B) 문구 수정 후 적용 · (C) 기각 (사유 → overrides.md).
- **세션 기본 조치**: 미적용 유지 (diff-only).
- **상태**: OPEN
