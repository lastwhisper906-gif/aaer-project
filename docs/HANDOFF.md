# HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-13, 야간 메가 미션 완결 — D68~D85, 미터링 351/380)

## 야간 메가 미션 요약 (2026-07-13, 소유자 서면+라이브 지시, 351호출·grader 0 — D68~D85)

**헤드라인: 엔진 판정 = `a_llm_engine`** — median lead LLM **7.0분기** vs B3
**5.5분기** (ENGINE_DECISION §4 기계 규칙, 재량 0). **정직 병기 필수: 대조군
궤적 FPR LLM 5/7=71.4% CP[29.0%,96.3%] vs B3 0/7** — stage-2 활성 결정
(LAUNCH_SEQUENCE 4단계)은 두 숫자를 함께 본 소유자의 것. b4_comparison.valid=
false (D60/D61 예측 적중). **human_finalized=false — 서명 대기.**

- **경로**: freeze 개정 #4 (D68, docs/FREEZE_REV4_HARNESS_E2.md) — 전 발사 하네스,
  개정 #3(raw)은 스모크 래치와 한 몸 보류. L-2 상속 명기 의무·L-3 미해소.
- **P0 E2 (162호출 실지출 = 146 최종 + 재지출 16)**: 실사격 결함 3건 발견·해소 —
  ① D70 로그 충돌(스냅샷별 log_dir 격리) ② D71 대조군 s0 부재(llm_p null 규약,
  ENGINE §3 주석 — 판정 무영향, 해소 7호출 옵션 Q-M06) ③ top_signals maxItems
  잠복 불일치(재추첨 수렴, ~7% 발현). buyer_metrics 캐시 과금 등가 개정(D82):
  **$0.5304/스크린·~300 stage-2 1회전 $159** (sonnet-5 목록가; 인트로가 별도).
- **A-8 Q-M02 완결 (D72·D76~D79)**: FINRA 공표일 223행 실측 재구성(Wayback 13
  스냅샷, 요일 체크섬·불일치 3건 사전등록 규칙 해소) → 스펙 §14 → 재실행 —
  holdout 경계 보고서 3건 추가 편입, **헤드라인 전부 불변** (정밀화 실증).
- **P2 E4 (18호출, D81)**: opus-4-8 교차모델 — **ρ=0.781·flag 15/18·κ=0.658**
  (EXPLORATORY 각주 전용).
- **P3 Q-F05 (63호출, D84)**: v2 date-shift name-ID — **wave-1 50%→13.3% ·
  wave-2 21.9%→0%** (동결 규칙·사전 등록 기준선). 날짜 지문이 잔존 인지의
  주 채널이었다는 산술.
- **P4 Q-F06-B (108호출, D85)**: median-of-3 병기 — flip 3/30·3/32(경계 케이스),
  **밴드(0.8494/0.8261)가 동결 draw-1(0.8239/0.829)을 감싼다.** 발행값 불변.
- **P5 미발사**: 캡 산술 351+32>380 (Q-M07 — launch-ready 동결 유지).
- **거버넌스**: D80/D83 라이브 순서 개정(소유자 실시간 지시, 동시 2 상한) 원장
  기록. 신규 소유자 큐: Q-M05(미션 §5 절단)·Q-M06(대조군 s0 7호출)·Q-M07(P5).
- **5게이트 최종 실측**: pytest **184** · reproduce **100/100** · lint **PASS** ·
  blindness **PASS** · manifest **PASS (526 files)**. CI green.

### 소유자 서명 대기 (레버리지 순)
1. **D82 판정 서명** — a_llm_engine 수용 여부 + stage-2 활성 GO/STOP (FPR 병기 필독).
2. RP-15/16/17/18 (기존 계류 불변 — 야간 무접촉).
3. Q-M06 (대조군 s0 7호출 — LLM j=0 AUC 계산 가능화) · Q-M07 (P5 32호출) ·
   Q-M05 (§5 백로그 목록 재전송 여부).

# HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-13, E2 무장(Armed) 미션 — D65~D67, 미터링 0)

## E2 무장 미션 요약 (2026-07-13 무인, 미터링 0 — D65~D67)

**헤드라인: E2는 이제 명령 하나 거리다 — 잔여 차단은 소유자 스모크 래치
(§6-3) 단 하나.** 스모크 뒤:
`AAER_RAW_API_APPROVED=1 .venv/bin/python tools/e2_runner.py --execute`
→ 146 evaluatee 호출(0 grader) → 완료 시 자동으로 e2_trajectories →
engine_verdict → runs/e2/E2_SUMMARY.md (b4_comparison.valid=false 자기 기록,
D60/D61 예측 그대로).

- **Phase 0 상태표**: RP-15/16/17/18 전건 미서명 · smoke 미발사 → 서명 적용
  전건 클린 스킵, 스모크 채점 스킵 (프리플라이트만).
- **D65 (거버넌스 선행)**: EARLINESS_PLAN 드리프트 주석 2건 — 원문 보존
  append: ① "~7–8사"는 추정, §1 규칙 출력 13케이스(cutoff 열거)가 지배
  ② "채점자 동수"는 E2 비작동(지표가 원점수만 소비, 동수 해석 시 292>cap
  자기모순) — **기록 예산 146+0**. runs/e2 부재 시점 커밋 = 결과 전 증명.
- **D66 (생성기)**: tools/e2_generate_cases.py → data/e2/ 156파일 —
  로스터 하드코딩 0(규칙 기계 출력, 테스트 강제)·이중 전체 생성 **바이트
  동일**·실제 cutoff_guard 문서 단위 경유(accession 교차검증)+**독립
  anti-leak 이중 검증**·전 행 회계(146 buildable+22 grid_ineligible,
  build_failed 0)·러너 배치는 기저 ID(perturb 동일-k 보존)+evaluatee 5필드만
  (메타 사이드카 격리). b4 동반 실측 7/146 — D61 추정 3은 보수 하한의
  과소집계, **케이스 커버 2/13·판정 불변** (메모 §5 후기).
  도중 교훈: 생성기를 pipeline/에 뒀다가 가드 우회 정적 스캔에 정확히
  차단됨(answer-key 참조 금지) → tools/로 이전 — 경계가 기계로 지켜짐을 실측.
- **D67 (레일)**: tools/e2_runner.py — ① 매니페스트 드리프트 정지 ② 지출
  가드 이중 ③ 온도 핀 0.0 상수 ④ INVARIANT 4 키 스크럽(발견 시 삭제+정지)
  ⑤ 크래시-재개 멱등(runner_api 원자 기록 패치 — 중복 0·갭 0 크래시 시뮬
  테스트) + 후처리 자동화 종단 테스트. 실데이터 dry-run: 드리프트 통과·
  계획 146·완료 0.
- **미서명 패킷**: RP-15/16/17/18 — 대기 유지 (한 줄 보고, 조치 없음).
- **5게이트 (D67 커밋 시점)**: pytest **151 passed** · reproduce 100/100 ·
  lint PASS · blindness PASS · manifest PASS (512 files). 최종 HEAD 재실측
  push 직전 병기. 미터링 **0**.

# (이전) HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-13, 소유자-액션 후속 + E2 프리플라이트 + 소규모 큐 소진 미션 — D61~D64, 미터링 0)

## 소유자-액션 후속 + E2 프리플라이트 미션 요약 (2026-07-13 무인, 상태 적응형, 미터링 0)

**개시 상태표 (Phase 0 실측)**: RP-15 **미서명**(PROPOSED 유지) · RP-17
**미서명** · smoke **미발사**(DRYRUN_MANIFEST만) · screener UA **미설정**
· screener 원격 **부재**. → Phase 1(서명 적용) 전건 클린 스킵, Phase 2는
프리플라이트만, Phase 3 3건 전부 실행.

**E2 한 줄 답 (docs/E2_PREFLIGHT.md)**: **"명령 하나 거리" 아님 — NO.**
차단 = ① 스냅샷 케이스 파일 생성기 부재(유일한 코드 차단 — 발사 세션
앞부분에서 무호출·결정론으로 생성 가능, PLAN §2가 이미 사전 등록)
② 스모크 래치 미발사(소유자) ③ RESUME E2 절 부재(본 세션 보완).
호출 산술 재생성: **146 evaluatee** (detected 13케이스 — WFT·MOS는 최소
요건의 기계적 귀결로 0스냅샷; ≤ 하위 cap 160, 절단 규칙 휴면). 드리프트
플래그 2건: PLAN §5 "~7–8사" 추정 vs §1 규칙(13사) 불일치 — §1 지배;
"채점자 동수" 문구 vs p-궤적은 채점 0 정합 (동수 해석 시 292 > cap).

- **D61**: 무대 메모 로스터 교정 — D60이 구판 DESIGN 7케이스로 계산 →
  지배 문서 PLAN detected 13케이스로 재계산: **3/146 계산 가능(전부 UAA)·
  케이스 커버 2/13(15.4%)** — **판정 불변**(비교 비성립, seal이 유일 무대).
  헤드라인·LAUNCH_SEQUENCE 수치 동기 + D61형 verdict 픽스처 테스트 추가.
- **D62 (Q-F01 해소)**: HUBG 하위 제출 파일 fetch(547건, 1996~2007) →
  payload_v2 **82/82 완전**(diff = case_71+COVERAGE만) · HUBG b3_score
  W4/W8 동결값 기계 대조 **무변화**(1996~2007 제출은 B3 창과 비교차) ·
  매니페스트 512 files 재생성.
- **D63 (Q-M02 → CONVERTED)**: 과거 공표일 **입수 가능** —
  analysis/DISSEMINATION_DATES_MEMO.md: Wayback 연도별 스냅샷(2019~2026
  실측)에서 3열 일정표 복원 가능, 2020 스냅샷 파싱 검증(관측 지연 11–12일
  ≤ LAG 14 — 상수의 표본 내 보수성 확인). 잔여 = 구현 GO(1세션 견적, 스펙
  개정 D-엔트리 동반). 2018년분 스냅샷은 구현 1단계에서 확인.
- **D64 (RP-18 준비)**: D53 비대칭 메모 발행 패킷 — 게시 가능 완성 영문
  텍스트(가설 표지 전건 유지·라벨 순환성 2문장·한계 1줄)·배치 2안(Issue 1
  부록 권장)·게시 명령. 게시 0, 결정은 소유자.
- **미서명 패킷**: RP-15·RP-17 — 서명 대기 유지 (본 세션 조치 없음).
- **5게이트 (D62 커밋 시점 실측)**: pytest **136 passed** · reproduce
  **100/100** · lint **PASS** · blindness **PASS** · manifest **PASS (512
  files)** — 최종 HEAD 재실측은 push 직전 병기. 미터링 **0** (네트워크 =
  SEC 공개 파일 1건 + finra.org/web.archive.org 조회).

# (이전) HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-13, 병합 확정 + RP-17 + B4 무대 판정 미션 — D59/D60, 미터링 0)

## 병합 확정 + RP-17 + B4 무대 판정 미션 요약 (2026-07-13 무인, 미터링 0 — D59/D60)

**헤드라인 — B4 무대 판정 (D60, analysis/B4_VENUE_MEMO.md)**: **LLM-vs-B4
비교는 E2에서 성립하지 않는다 — 신규 스냅샷 112개(실험군 48) 중 B4 점수 계산
가능 0개.** s0 재사용점을 넣어도 실험군 케이스 커버 1/7(14%) < §4b 성립 조건
70%, E2를 실행해도 불변(그리드가 과거로만 자란다). 귀결: engine_verdict는
`b4_comparison.valid=false`를 자기 기록(설계 정상), `b4_dominated` 강등은
E2에서 트리거 불능, **무료 신호 대결의 유일한 무대 = 전향 seal** — 첫 증거
≈2027-11(2026-11-15 seal + 4분기 창), stage-gate 최초 개방 가능 ≈2028-08.
LAUNCH_SEQUENCE 2단계에 기대치 주석 반영: **E2 발사 편익에 B4 대결 해소를
계상하지 말 것** (E2가 사는 것은 LLM vs B3 리드타임이다).

- **단일 작성자 확인**: 개시 시 60초 재확인 — remote/양 워크트리/screener
  HEAD 무이동, lock 없음, 클린 트리 (직전 정합 병합 세션은 01:56 push로 종료).
- **Phase 1 (검증만 — 병합은 직전 세션이 완료)**: 재부여 매핑 전수 grep —
  잔존 구번호 인용 0 (전 인용이 '원번호' 주석 동반, HANDOFF 역사 절은 명시
  보존). freeze 순서 git log --follow 실측 — 스펙<구현<결과 전 계열 정상
  (4753824<a14d746<287a92a · 7994e2d<efaf4a1 · f03d331<0a57eb6), 병합이
  merge 커밋이라 그래프 보존, 정합 노트 불요. 원장 D51~D60 중복 0.
- **Phase 2 (D59)**: `review_packets/RP-17_denominator_fallback.md` —
  D56/D57 사후 분모 개정의 소유자 분류 판정 (기계 결함 vs 분석 변경). 양판
  전량 델타 실측 명기: **holdout AUC 0.1667→0.4762/0.5238 — AUC가 움직였다**
  (커버리지만이 아니라). checkout 기반 무충돌 원복 명령·양측 최강 논거·
  CLAUDE.md 거버넌스 3줄(사후 개정 한계·5게이트·단일 작성자) 제안 diff 동봉
  (소유자 서명 시에만 적용). 미션 문면의 RP-16은 D47 diff가 선점 — RP-17로
  발행 (D14 생성 순서 규칙).
- **Phase 4 (screener)**: 81 passed + vendor 무결성 green. 구성 검증 2건 —
  (a) publish 경로 게이트 순서(b4_top30 구조 검증 선행 → lint가 b4-유효
  워치리스트 차단·파일 미기록) 시퀀스 테스트 신규 5af8a8c; (b) stage-1
  fixtures_of_record diff 검토(2287907) — rank_rule = M/F/B4 flags +
  b4_slope_aug tiebreak, B3 보조열 유지, 램프→플래그/평탄→0.0 픽스처 정상.
  과학 모듈 무변경 → 재vendoring 불요.
- **5게이트 실측 (2026-07-13)**:
  - main(0c219e5 시점): pytest **135 passed**(analysis/ 포함) ·
    reproduce **100/100** · lint **PASS** · blindness **PASS** ·
    verify_manifest **PASS (511 files)** — 아래 커밋 후 재실측 병기.
  - branch(a3ba603): pytest 111 · 나머지 4종 전부 PASS.
  - screener: **81 passed** (vendor 무결성 포함). CI: main push 전건 green.
- 미터링: **0호출.** 네트워크 = git fetch/push·gh만.

### 소유자 통합 체크리스트 (레버리지 순 — 직전 두 목록 대체)

1. **RP-17 서명** — D56/D57 수용 or 기각 (기각 = 패킷 §2 명령 그대로, 커밋
   1개 원복·재실행 0). 수용 시 CLAUDE.md 거버넌스 3줄 diff도 함께 서명 권장.
2. **RP-15 서명** — 라벨 명명 diff (계류 지속).
3. **screener 원격 + UA** — S-03(remote-add/push 명령 62ba9cc에 있음) +
   S-01(config.json UA). seal 앵커 사슬의 전제.
4. **`make smoke`** (~30호출 종량) — FREEZE_REV3 §6-3 래치, E2 전 필수.
5. **E2 예산·발사** (~112–160호출) — **D60 주석 확인 후**: E2는 B4 대결을
   해소하지 않는다. 사는 것 = LLM vs B3 리드타임 + 엔진 판정 §4.
6. **FINRA ToS** (Q-M01/S-08) — 발행물 원수치 게재 전 확인.
7. **공표일 실측** (Q-M02/S-09) — 입수 시 LAG 14 대체는 신규 D-엔트리 개정.
8. **변호사 2종** (S-10 증권 + S-13 이민·whistleblower, wrapper W-8).
9. **Zenodo vs GitHub release** (S-02 + Q-R03) — seal 앵커 채널 단일화.
10. **Q-F01** — HUBG 하위 파일 fetch (payload_v2 커버리지 완결).
11. **D53 EXPLORATORY 메모 발행 여부** — wave-1 B3 비대칭 산술 분해.
12. **WS-6/7 예산** (Q-F06 124/108 · Q-F07 ~20호출) — E4 동배치 권장 유지.

# (이전) HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-13, 병렬 워크트리 정합 병합 — main D51~D53 + worktree D54~D57, 미터링 0)

> **정합 병합 노트 (통합 세션)**: 아래 두 미션이 같은 날 병렬 실행되어 병합됨. 워크트리 D-번호는 최종 **D54(게이트 수리)·D55(B4 사전 등록)·D56(분모 개정)·D57(재실행 확정)·Q-M04(설명가능성)**로 재부여 — 각 원장 엔트리의 renumber_note가 원번호·원 커밋 SHA를 보존한다. 아래 시장조사 미션 절 본문의 D51~D54/Q-M03 표기는 작성 당시 브랜치 번호(역사 기록)로 무수정 유지.

## 정합 병합 미션 요약 (2026-07-13, 통합 세션 — merge×2 + B4 완결 + 발사 준비, 미터링 0)

두 병렬 미션을 원장 무손상으로 병합하고 (merge 선택 — rebase는 스펙 동결 SHA
증거를 파괴), B4를 완결, 발사 준비를 마감했다. **동결값 불변·발행 표면 무변경.**

- **Phase 1 (병합 ×2)**: worktree 7커밋을 두 라운드로 병합 — 원장 재부여
  **D54(게이트 수리)·D55(B4 사전 등록)·D56(분모 개정)·D57(재실행 확정)·
  Q-M04(설명가능성)**, 각 엔트리 renumber_note가 원번호·원 커밋 보존. freeze
  순서 감사: 스펙 4753824(01:11) → 구현 a14d746(01:18) → 계산 287a92a(01:25)
  — 원 SHA 그대로, 위조 노트 불필요. 인용 파일 전수 재부여 (양 리포).
- **Phase 2 (B4 완결)**: D57 산출물 결정론 재현 검증 (results_b4.json diff 0).
  B4_REPORT에 **결정 관련성 한 문장**("결정에 관련된 B4 수치는 holdout과 모든
  미래 seal") + 스펙 개정 D56 커밋 인용 병기. 최종 5열 표: holdout **10/12
  (83%) slope-aug AUC 0.4762** [0.0,1.0] — 커버리지 바 통과·판독 불가(N=3)·
  **비교 성립 tier 없음** (사전 등록 그대로). main Q-M03(분모) = D56/D57
  실행으로 RESOLVED (기각 시 revert 경로 보존). 시장 워크스트림 완결:
  WS-EXPLAIN 2층 (stage-1 explanation.schema+validator 12테스트 / stage-2
  flag_explanation+STAGE2_PROMPT_SPEC — 병렬 세션분) · WS-LEGAL
  (PUBLICATION_WRAPPER + lint_release L1~L4 → seal create/reveal 하드 게이트)
  · WS-DDQ 2종 (DDQ.md 문답 + DDQ_PACK.md 포인터) · WS-KR 스펙+DART 프로브.
- **Phase 3 (교차 배선)**: E2 인터페이스 계약 테스트 (b3_score/b4_score 병행·
  §8 키·결측=플래그·결정론; shares_source 반환 확장을 §13에 명문화) ·
  **stage-1 B4 열 실장** (rank = M/F/B4 플래그 + slope_aug tiebreak, 합성
  FINRA 픽스처 32파일, fixtures_of_record 재생성·행별 검토, 무아카이브
  fail-closed 강등 테스트) · seal b4_top30 동봉+lint 게이트 테스트 확인 ·
  역방향 vendored 재수출 (screener b60fd85, PROVENANCE sha 갱신; aaer→screener
  5모듈은 무변경 — 재수출 불요).
- **Phase 4 (발사 준비)**: 스모크 dry-run 재생성 = 커밋본과 byte 동일 (델타 0)
  · **D58 ENGINE_DECISION §4b** — B4 결합 조항의 기계 이행 (E2 실행 전 개정,
  스펙 선행 커밋): 성립 조건(실험군 B4 커버리지 ≥70% + 짝지은 LLM 재계산) 하에
  LLM ≤ B4 (리드·AUC 모두) 이면 판정 (a)→(b) `b4_dominated` 강등, (b)/(c)
  불변. 픽스처 5건 (지배/비지배/커버리지 미달/키 부재 호환/(c) 불변) ·
  **docs/LAUNCH_SEQUENCE.md** (스모크→E2→판정→첫 seal, 기서명 결정의 지도).

### 소유자 통합 체크리스트 (두 미션 목록 대체 — 레버리지 순)

| # | 항목 | 위치/게이트 | 규모 |
|---|---|---|---|
| ① | **screener GitHub 원격 생성 + SEC User-Agent** — seal 타임스탬프 앵커의 전원 스위치. `config.example.json`→`config.json` 기입 + `git remote add origin <url> && git push -u origin main --tags` | screener S-01/S-03 | 수분 |
| ② | **RP-15 서명** (Big R 정밀화 diff — 3/3 기계 증거·기저율 2.2%·4년 윈도; 미적용 유지 중) + RP-16 (서수 규약) | Q-F03/Q-F04 | 판단 |
| ③ | **스모크 발사** `export ANTHROPIC_API_KEY=… && make smoke` (~30호출; 결과 커밋 전 E2 금지) | FREEZE_REV3 §6-3 / LAUNCH_SEQUENCE 1단계 | ~30호출 |
| ④ | **E2 예산 승인 + 발사** (~112–160호출) → 어댑터 → engine_verdict (D58 §4b 포함) → buyer_metrics | LAUNCH_SEQUENCE 2–4단계 | ~160호출 |
| ⑤ | **FINRA ToS 확인** — 발행물/seal 공개 파일의 SI 파생 수치 게재 조건 (해소 전 lint L2가 자동 차단) | Q-M01 / screener S-08 | 확인 |
| ⑥ | **Zenodo vs GitHub release** — v1.0.0 DOI (Q-R03 경로 확정분) + screener seal 앵커 채널 (한 채널 고정) | Q-R03 / S-02 | 계정 작업 |
| ⑦ | **변호사 검토 2종** — 증권 (PUBLICATION_WRAPPER, lint가 강제 중이나 법적 검토 전) · 이민/내부고발 (F-1/OPT 수익·whistleblower — W-8) | screener S-10/S-13 | 외부 |
| ⑧ | **DART API 키** (KR 확장 스펙 전제 — 스펙만 존재, 구축 게이트) | screener S-11 | 수분 |
| ⑨ | **Q-F01 HUBG 하위 파일 캐시** (fetch → manifest → payload-v2 재실행) | Q-F01 | 수분 |
| ⑩ | **D53 EXPLORATORY 메모 공개 여부** (기본 비공개) | D53 | 판단 |
| ⑪ | **WS-6/WS-7 예산 게이트** (k=3 124/108 · 교차 채점자 ~20, E4 동배치) | Q-F06/Q-F07 | 판단 |
| — | 2차: D56/D57 추인(기각 시 결과 커밋 revert — 동결 무접촉) · Q-M02 공표일 · Q-M04 Cycle-2 · S-12 DDQ 미소싱 · Q-F02 Chu · Q-F05 v2 프로브 62 · Q-F08 생존편향 · 독자 warm 5–7 발송(D43, 이번 주) | 각 큐 | — |


## 시장조사 통합 미션 요약 (2026-07-13 무인, 미터링 0 — 브랜치 mkt-integration-2026-07-13)

**헤드라인 — B4 5열 표 (tier별, 재계산 0, analysis/B4_REPORT.md 정본):**

| tier | B1 (M) | B2 (F) | B3 (W8) | B4 (slope-aug) | LLM | B4 커버리지 |
|---|---|---|---|---|---|---|
| wave1 | 0.5104 | 0.5729 | 0.7898 | 1.0000 ⚠️서술전용 | 0.8239 | 3/30 |
| wave2 | — | — | 0.5483 | 1.0000 ⚠️서술전용 | 0.829 | 3/32 (level 4/32) |
| holdout | — | — | 0.4259 | **0.4762** [0.0,1.0] | 없음(N=3) | **10/12** |

**B4가 wave-2에서 LLM을 이겼는가 — 판정 불성립이 정직한 답이다.** FINRA 무료
데이터 하한(결제일 2017-12-29, 프로브 실측)으로 wave-1/2 커버리지가 10%대
(사전 등록 §6 산술 그대로) → 서술 전용. holdout은 커버리지 바(83%)를 넘지만
동결 LLM AUC가 없다(N=3). **결론: LLM vs B4는 회고로 성립하지 않는 비교이며,
전향 무대(E2 스냅샷·sealed 분기)로 사전 등록 결합 조항과 함께 이관** —
비교 성립 시 LLM≤B4이면 E2 평결과 동일 가중치로 엔진 결정 입력 (스펙 §7,
완화 금지). 이 사실이 이 미션의 핵심 발견이다: 무료 신호 벤치마크는
본질적으로 앞으로의 seal에서만 이길 수 있고, 그래서 seal 프로토콜에 B4
top-30 동봉을 의무화했다.

- **WS-SI (D52 스펙→구현→D53 개정→D54 확정)**: specs/B4_short_interest.md
  사전 등록(freeze-commit-then-run, 4753824) → screener/ingest/short_interest.py
  정본 + analysis/vendor 역방향 vendoring(PROVENANCE+무결성 테스트) +
  analysis/b4_short_interest.py (b4_score = b3_score 동형 E2 계약, 동결 E2
  무수정) → FINRA 79파일 아카이브(~/aaer-data/short_interest/, 매니페스트
  511파일 등재) → 1차 실행(287a92a, holdout 7/12 — 다중클래스 분모 구멍
  진단) → **D53 개정**(분모 4단 사다리, 1차 결과 커밋 후 공개 개정) →
  **D54 재실행**(holdout 10/12). PIT: 결제일+14일 보수 LAG 사전 등록.
- **게이트 수리 (D51, 이 브랜치 번호)**: 세션 개시 verify_manifest FAIL
  (reference/ 2건 미등재, D36 산물) → 귀속 분기+재생성, 전 게이트 green 복구.
- **WS-SEAL-METRICS (screener)**: 프로토콜 pre-first-seal 개정 — 헤더 목표
  밴드(precision@30 ≥25–33%), §2 b4 필드, §3 b4_top30 공개 파일 의무 동봉
  (seal create 하드 게이트), §5 metric 3(lift vs B4 동일 유니버스·동일 창),
  §5b 4연속 분기 초과 시 escalation gate = seal/verdict.py 계산 필드.
- **WS-EXPLAIN (screener)**: schemas/flag_explanation.json (계정 태그·방향·
  기제 통제 어휘·accession 앵커 증거·반증 조건·서수 confidence) +
  validate_explanation.py 결정론 하드 게이트 + STAGE2_PROMPT_SPEC.md (호출 0).
  aaer-evals 쪽 Cycle-2 채점 질문 등록(이 브랜치 Q-M03→재부여 Q-M04).
- **WS-DDQ (screener)**: docs/DDQ_PACK.md — 포인터 큐레이션 (PIT 보증·계보·
  한계 L-1~L-7 원제·제3자 seal 검증 커맨드 시퀀스); 미소싱 항목 S-12.
- **WS-LEGAL/WS-KR**: **병렬 소유자 세션에 양도/합작** (아래 충돌 노트).
  본 세션 기여: W-8(F-1/OPT·whistleblower 상담 게이트)+S-13, KR_DART.md §4
  DART DS003 프로브 실측 기록.

### ⚠️ 병렬 세션 충돌 노트 (통합자 필독)

같은 시간대에 main에서 별도 세션(git author chaeryeol, 로드맵 운영화 미션
D51~D53 + 본 브랜치 부분 병합 f465961 + WS-LEGAL/WS-KR)이 진행됨. **이
브랜치의 D51~D54는 main 규약으로 재부여 필요** — 매핑 제안은 원장 말미 정합
노트: D53→D56·D54→D57·Q-M03→Q-M04, main Q-M03(분모 폴백 질문)은 D56/D57
실행으로 RESOLVED 가능(소유자 기각 시 결과 커밋 revert로 원복, 동결 수치
무접촉). analysis/b4_short_interest.py 내 "D52" 문자열 인용은 재부여 시
4e850ad 방식으로 전수 갱신할 것.

- **소유자 잔여 (이 미션분)**: Q-M01 FINRA ToS · Q-M02 공표일 실측 ·
  Q-M03/M04 재부여 확정 · screener S-08~S-13 (ToS·공표일·변호사 2종·DART
  키·DDQ 미소싱) · 본 브랜치 main 병합.
- **미터링: 전 워크스트림 0호출.** 네트워크는 공개 규제 데이터(FINRA CDN·
  Query API 프로브, DART 문서 페이지)만.
- **최종 4게이트 (2026-07-13, 이 브랜치에서 실측)**: 아래 커밋 직전 실측값
  병기 — reproduce 100/100 · blindness PASS · manifest 511 files PASS ·
  lint PASS · pytest 101+10(analysis) passed.

# (병렬) HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-13, 로드맵 운영화 미션 — D51~D53 + screener 리포 v0.1.0, 미터링 0)

## 로드맵 운영화 미션 요약 (2026-07-13, 미터링 0 — D51~D53 + 신규 리포)

로드맵(도구 가치 1→5)의 인프라 전환. **동결값·발행 표면 무변경** (D53 메모는
not-for-publication 배너). 두 리포 두 체제: aaer-evals = 기존 거버넌스 전부 /
`~/Documents/screener` (신규, v0.1.0 태그) = semver+pytest만, fail-closed 원칙만 계승.

- **Phase A 정합 확인**: 로컬 = origin/main 695cf8f 동률·clean에서 시작.
  4게이트 전건 green (수치 하단). B3 동결값 대조 확인 — wave-2 W8 AUC 0.5483·
  귀속비 0.1468 `non_trivial` / wave-1 W8 0.7898 (LLM 0.8239, 귀속비 0.8947) /
  holdout 0.4259 (귀속비 미계산). **설계 귀결 이행: 운영 퍼널에서 B3를 stage-1
  1차 필터에서 보조 열로 강등, 기계 비율 스크린(Beneish M·Dechow F)이 1차** —
  근거는 전망 유니버스가 wave-2형 모집단이라는 것 (screener/docs/FUNNEL.md §0).
- **Phase B — screener 리포 부트스트랩** (`~/Documents/screener`, 커밋 9·태그
  v0.1.0·pytest 19 green, 네트워크 0):
  - B1 벤더링: cutoff_guard·payload_v2_extract·b3_compute·stats·screens 5모듈
    verbatim + PROVENANCE.md(소스 커밋 695cf8f·sha256 표) + 무결성 테스트가
    로컬 수정을 게이트. 어댑테이션은 전부 래퍼(screener/science.py).
  - B2 docs/FUNNEL.md: 2단계 퍼널 설계 기준 문서 (stage-2는 ENGINE_DECISION
    판정 조건부 — 그 전까지 rules-only 완주 의무).
  - B3 ingest/: 재개 가능 다운로드(체크섬 로그·UA fail-closed)·per-CIK 추출+
    SQLite 인덱스·유니버스 필터(SIC 제외·18개월 신선도·XBRL 8분기)·stage-1
    랭커. --sample 모드 실행 완료 — 합성 6사 픽스처의 universe/stage1 산출물을
    fixtures_of_record로 커밋 (회귀 diff 테스트).
  - B4 seal/ (**핵심 산출물**): specs/SEALED_FORECAST_PROTOCOL.md (N=30 분기
    봉인·첫 봉인 2026-11-15·per-item 32B salt SHA-256 커밋먼트·정렬 리스트
    Merkle root·선택적 공개·판정 규칙 = 4분기 내 4.02/AAER·기저율 0.9건/yr·
    유의 주장 ≥3배) → `seal create/verify/reveal` CLI. 테스트: 라운드트립·
    1바이트 변조 검출·위조 reveal 기각·형제 항목 비누출.
  - B5 monitor/: 주간 제출물 diff (8-K 4.02/4.01·NT·정정) — 봉인 티커 +
    aaer-evals 홀드아웃 업그레이드 윈도(2030까지, WS-3)를 같은 인프라로.
    WS-1 parse_items 재사용 (문법 단일화).
- **Phase C — 미터링 준비 (발사 0)**:
  - C1 (D52): tools/smoke_rev3.py + `make smoke` — FREEZE_REV3 §6-3 래치의
    실행 형태. **dry-run 매니페스트 30호출 커밋** (`runs/smoke_rev3/
    DRYRUN_MANIFEST.json` — pilot 2케이스×5draw×3arm, temp 핀 명시). live는
    매니페스트 불일치 시 정지·하네스 arm 동안 API 키 임시 제거(INVARIANT 4).
    절차는 docs/RESUME.md 스모크 절.
  - C2 (D52): analysis/buyer_metrics_build.py + BUYER_METRICS.template.md —
    E2 완료 후 단일 명령으로 구매자 지표 4종 (리드타임 LLM vs B3 · FPR@50
    CP95 · 토큰 실측 cost-per-screen · 커버리지). 합성 픽스처 테스트 5건.
  - C3 (D51): **specs/ENGINE_DECISION.md 사전 등록** (판정 코드 선행 커밋) —
    3브랜치 순서 고정·전역 완전: (c) 양쪽 lead ≤1분기 → 도구 종료 / (a) LLM
    ≥ B3+1분기 → LLM 엔진·stage-2 활성 / (b) 그 외 → 규칙 엔진. B3 플래그
    ≥2 신규 사전 등록. analysis/engine_verdict.py 픽스처 테스트 6건 (3브랜치
    전수·잔여지대·fail-closed).
- **Phase D (D53)**: analysis/EXPLORATORY_wave1_b3_asymmetry.md — 비대칭의
  유병률 분해 산술만 (w1 최대 기여 = 10-K/A 4/8 vs 2/22 · w2 동일 지표 역전
  1/9 vs 6/23), 가설 전부 질문형. **발행 표면 접촉 0 — 공개 여부는 소유자.**
- **실행 환경 사고 기록 (무-미터링)**: screener venv editable install이 간헐
  소실 — 원인: 샌드박스 pip가 쓴 `.pth`에 macOS UF_HIDDEN 플래그, Python 3.12
  site가 hidden .pth를 스킵. `chflags nohidden`으로 해소 (메모리 등록).

### 소유자 통합 체크리스트 (이 미션 후 계류 전건 — **superseded: 최상단 통합 체크리스트로 대체**)

| # | 항목 | 위치/게이트 | 규모 |
|---|---|---|---|
| 1 | **RP-15 서명** (라벨 명명 diff — DIFF-4 ISSUE_2 §7 Big R 정밀화 + DIFF-5 README 1문장; 3/3 Big R 기계 증거 + 기저율 2.2% 한정 + 4년 윈도. 미적용 유지 확인) | Q-F03 | 판단 |
| 2 | RP-16 서명 (보정 언어 서수 규약 2건) | Q-F04 | 판단 |
| 3 | HUBG 하위 파일 캐시 (fetch 후 manifest 갱신 + payload-v2 재실행) | Q-F01 | 수분 |
| 4 | Chu et al. 원문 대조 (정성 인용 유지 시 액션 불요) | Q-F02 | 선택 |
| 5 | **스모크 발사**: `export ANTHROPIC_API_KEY=… && make smoke` (30호출 종량, 결과 커밋 선행 후에만 E2) | FREEZE_REV3 §6-3 / D52 | ~30호출 |
| 6 | **E2 발사** (~160호출) → e2_trajectories 어댑터 → engine_verdict.py → 판정 D-엔트리 → buyer_metrics_build.py | D51/D52, RESUME.md | ~160호출 |
| 7 | Zenodo vs GitHub release — v1.0.0 DOI (Q-R03 경로 확정분) **+ screener 봉인 앵커 채널 선택** | Q-R03 / screener S-02 | 계정 작업 |
| 8 | screener config.json **SEC User-Agent 기입** + GitHub 원격 생성·push | screener S-01/S-03 | 수분 |
| 9 | WS-6 k=3 예산 게이트 (124 vs 108) | Q-F06 | 판단 |
| 10 | WS-7 교차 채점자 (E4 동배치 권장, ~20호출) | Q-F07 | 판단 |
| 11 | D53 EXPLORATORY 메모 검토 (공개 여부 — 기본 비공개) | D53 | 판단 |
| 12 | 독자 warm 5–7 발송 (D43 계획 — 이번 주) | D43 | 인간 작업 |

- **4게이트 (2026-07-13 HEAD, 실측)**: `pytest pipeline/ tools/ scoring/ -q`
  **106 passed** · `reproduce_analysis.py` **PASS 100/100** ·
  `lint_publication.py` **PASS** · `verify_blindness.py` **PASS** (146 모델
  출력 + 매니페스트 — runs/smoke_rev3 편입). 병기: `pytest analysis/ -q`
  **18 passed** (b3 7 + engine_verdict 6 + buyer_metrics 5). screener:
  **pytest 19 passed**.
- 미터링: **전 Phase 0호출.** 계류 브랜치 `hardening/2026-07-08` 불변.


# (이전) HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-12, 기능 약점 교정 미션 F-1…F-8 — D44~D50, 미터링 0)

## 기능 약점 교정 미션 요약 (2026-07-12 무인, 미터링 0 — D44~D50)

외부 검토 기능 약점 8건(F-1~F-8)의 무-미터링 교정. **발행 동결값·R/H 판정
전부 불변 — 신규 결과 전량 병기, 발행 표면은 diff-only.** 전 워크스트림
freeze-commit-then-run (스펙 커밋 해시가 검증 경로, `git log --follow`).

- **⚠ 실행 환경 특이사항 (소유자 필독)**: 세션 시작 시 `~/Documents` TCC
  차단이 **재발** (07-12 해소 기록 이후 재퇴행 — 메모리 갱신됨). 본 세션은
  GitHub 미러(로컬 HEAD 5147af3과 동률·clean 확인 후)를 풀 클론해 작업하고
  push했다. **소유자 로컬 저장소는 `git pull` 필요** (로컬에서 커밋하기 전에
  — 로컬은 이 미션의 커밋 11건이 없는 상태다). Full Disk Access 재부여도
  점검 대상.
- **WS-1 (F-4, D44)**: `specs/payload_v2.md` → `pipeline/payload_v2_extract.py`
  (테스트 12) → `runs/diagnostics/payload_v2/` **82/82 케이스** (8-K item 코드 +
  shares/EPS PIT, 진단 전용 — 페이로드 편입은 명명된 미래 소유자 게이트).
  partial 1 = HUBG 1996–2007 하위 파일 미캐시 (**Q-F01**, B3/라벨링 무영향).
  정직 기록: 미션 문면의 diluted 태그 철자는 실측 부재 — 실제 태그
  `WeightedAverageNumberOfDilutedSharesOutstanding` 병기.
- **WS-2 (F-1, D45)**: `specs/B3_metasignal.md` (윈도 W4/W8·6지표·비가중 합·
  해석 규칙 — 전부 계산 전 커밋 053e780) → `analysis/b3_compute.py` →
  `results_b3.json` + `B3_REPORT.md`. **판정(wave-2 W8): 귀속비 0.1468 ≤ 0.2
  → non_trivial** — "분리는 사소한 연대기 규칙에 귀속되지 않음", 병기만,
  주장 무변경 (≥0.5 diff 의무 브랜치 비발화). **참고 병기: wave-1 W8 귀속비
  0.8947** (B3 AUC 0.7898 vs LLM 0.8239) — tier 비대칭의 산술 사실만 기록,
  원인 서술은 사전 등록 문장 밖 (소유자 검토 대상). E2 통합:
  `b3_score(ticker, cutoff, window_days)` import 가능 (E2 동결 파일 무수정).
- **WS-3 (F-6, D46)**: `specs/label_taxonomy.md` → 홀드아웃 태깅 **3/3 bigR**
  (accession 증거: HUBG 0001193125-26-039396 · WMK 0000105418-26-000009 ·
  GNE 0001437749-26-007981) + `LABEL_REPORT.md` (기저율 ~2.2% 집행 연계 등) +
  업그레이드 프로토콜 (4년 윈도, 대칭 — 무집행 만료도 보고 결과) +
  **RP-15** 명명 diff (미적용, **Q-F03**) + Chu et al. 원문 대조 **Q-F02**.
- **WS-4 (F-7, D47)**: `specs/calibration_scope.md` — 점수 = 서수 규약,
  재보정 비실행 근거(N≈30–60 노이즈 지배) 사전 등록, 재개 하한 N≥150,
  스키마 필드 개명 금지(Cycle-2 등록만). **RP-16** diff (ISSUE_0 확률 문장
  강화 + ISSUE_2 표 헤더 `LLM p`→`LLM score`, 미적용, **Q-F04**).
- **WS-5 (F-2, D48)**: `specs/perturb_v2.md` → `pipeline/date_shift.py` +
  테스트 8 (결정론·주 단위·간격/요일 보존·컷오프 불변·no-leak 스캔).
  교란 재실행 0 — v2 name-ID 프로브 런은 launch-ready (**Q-F05**, 62호출
  산술). 구현 중 실측: 364일(52주) 오프셋의 **양성 충돌** (역년 start↔end
  간격과 일치 시 이동 날짜가 타 원본 날짜 문자열에 착지) — 발사 전 위생
  스캔 전제 조건으로 Q-F05에 기록. accession 연도 누출 → 순차 중립 ID
  마스킹 사전 등록.
- **WS-6 (F-3, D49, SPEC ONLY)**: `specs/draw_k3.md` — median-of-3 병기
  1차값, 예산 산술 **(30+32)×2 = 124 피평가자 호출·채점자 0** (재사용 옵션
  108), flip-rate 표 사전 등록, temp=0 비결정론 단서. 게이트 **Q-F06**.
- **WS-7 (F-8, D50, SPEC ONLY)**: `specs/cross_grader.md` — 비-Anthropic
  채점자 n=20 (n=10 기각 근거 명시), 층화 tier×등급 seed 20260712, 주관
  2차원(dim2/dim4)만, κ≥0.6 사전 판독, E4 동배치 ~20호출. 게이트 **Q-F07**.
- **OWNER_QUEUE 신규 8건**: Q-F01(HUBG 하위 파일 fetch) · Q-F02(Chu et al.
  원문 대조) · Q-F03(RP-15 diff) · Q-F04(RP-16 diff) · Q-F05(v2 프로브 62호출)
  · Q-F06(k=3 예산 124/108) · Q-F07(교차 채점자 ~20호출) · **Q-F08(대조군 풀
  생존 편향 감사** — 현재 시점 SIC browse 열거가 상장폐지/등록취소 제출자를
  과소 표집했을 가능성, Form 25/Form 15 대조 감사 열린 항목).
- **최종 4게이트 (2026-07-12, 이 클론에서 실측)**:
  - `pytest pipeline/ tools/ scoring/ -q` → **101 passed**
  - `tools/reproduce_analysis.py` → **PASS — 100/100 항목 일치**
  - `tools/lint_publication.py` → **PASS — 발행 정합**
  - `tools/verify_blindness.py` → **PASS — 이력 증명 + 스캔(146) + 매니페스트 대조**
  - (병기) `pytest analysis/test_b3_compute.py -q` → **7 passed** (4게이트
    경로가 analysis/를 순회하지 않아 명시 실행 — specs/B3_metasignal.md §10-5)
- 미터링: **전 워크스트림 0호출.** 계류 브랜치 `hardening/2026-07-08` 불변.


## 발행 완결 미션 요약 (2026-07-11~12, 소유자 대화형 — D39~D42, 미터링 0)

**발행이 세상에 존재한다.** 3-이슈 GitHub Issues 게시 + v1.0.0 동결 + 독자 검증
패키지 ready-to-send. Phase E(c′ arm)는 소유자 SKIP — Phase E용 D43/D44는
미사용. (D43은 이후 2026-07-12 소유자 인간 작업 실행 계획 서명에 발번 —
아래 '소유자 잔여 액션' 절. D44는 미발번.)

- **발행 URL (시리즈 번호 0/1/2 = GitHub 번호 1/2/3)**:
  - Issue 0: <https://github.com/lastwhisper906-gif/aaer-evals/issues/1>
  - Issue 1: <https://github.com/lastwhisper906-gif/aaer-evals/issues/2>
  - Issue 2: <https://github.com/lastwhisper906-gif/aaer-evals/issues/3>
  - 태그/릴리스: **v1.0.0** = citable freeze point
    <https://github.com/lastwhisper906-gif/aaer-evals/releases/tag/v1.0.0>
- **D39 (Phase A, 이전 세션분)**: DIFF-3 재배선(RP-14) + 3-arm confound 서사 +
  L-7 + lint (I).
- **D40 (Phase B, 소유자 서명)**: DIFF-1/2 적용 · **DIFF-3 수정 적용**(Q-E02(A)
  정합 — 21.9% 1차 + 25% rename-aware 각주, 적용기 `tools/apply_rp14_diffs.py`) ·
  E4 EXPLORATORY 문언 승인 · Console $0.00 확인 · **Q-E01 RESOLVED(A)** 동결
  유지 · **Q-E02 RESOLVED(A)** · **Q-R01 RESOLVED** · **Q-R02 RESOLVED(A) GO**
  (다음 실행 배치부터, 래치 해제 조건 = FREEZE_REV3_DRAFT §6) · 발행 형식 =
  Issues · Phase E = SKIP.
- **D41 (Phase C)**: 3-이슈 게시 (건별 소유자 최종 렌더 확인 3회 전건 승인;
  본문 = 서명본 전문 + 표면 변환 4종 — 제목 분리·Published 배너+번호 매핑·
  Issue #N→Issue N 자동링크 오염 방지·저장소 푸터) + README 양어 발행 절 +
  초안 배너 PUBLISHED + v1.0.0 annotated tag/Release (영문 고정 구조: 3-tier
  동결값·방법론·3줄 재현·L-1~L-7) + **Q-R03 신설**(Zenodo DOI, 3줄 절차).
  deviation: 배너 일자 07-11(서명일) vs 게시 UTC 07-12T00:15Z — D41 기록.
- **D42 (Phase D)**: `docs/reader_validation/` 4종 — ONE_PAGER(영문, lint 편입
  PASS, GRDX 78 포함) · FEEDBACK_FORM(핵심 3 고정 + 유형별) · TARGET_LIST_TEMPLATE
  (5–10 슬롯, 회신 +10일) · OUTREACH_MESSAGE(cold/warm, <120단어, 단일 요청).
  **패키지 발송은 소유자 인간 작업 — 자동화 금지.**
- **소유자 잔여 액션 — 실행 계획 서명 완료 (D43, 2026-07-12, 전건 추천안 채택)**:
  ① 독자 발송 = **warm 5–7명 1차, 이번 주** (유형 균형 유지, 이메일 본문에
  원페이저 붙여넣기 + 핵심 3문항, 기한 +10일; 회신은
  `docs/reader_validation/responses/`에 원문 기록; cold는 2차 배치)
  ② Zenodo = **토글 + v1.0.0 재발행** (Q-R03 RESOLVED — 릴리스 삭제→동일
  태그·노트 재생성; DOI 배지 README 반영은 세션 몫)
  ③ Q-R02 후속 = **발송 직후 이번 주** 키 발급·스모크(~30호출) → E2는 회신
  대기 기간에 실행 (8/18 전 완결 경로; 스모크 결과 커밋 선행 — FREEZE_REV3 §6)
  ④ E 배치 = **E2 + E4만** (E5는 launch-ready 동결 유지).
- 미터링: 전 Phase 0호출. 계류 브랜치 `hardening/2026-07-08` 불변(스코프 외).

## 잔여 교정 세션 완료 요약 (2026-07-10, 무인 — D31~D38, 미터링 54/60)

2·3차 외부 검토 잔여 항목 실행. **발행 동결값·R/H 판정 전부 불변 — 신규 결과는
전량 병기.** 전 Phase freeze-commit-then-run (사전 등록 커밋 해시가 검증 경로).

- **Phase 0 (D31, 무호출)**: ① GRDX 78 표면화 (README 양어 + ISSUE_2 §3b + lint
  (H) GRDX·78 co-presence 강제) ② W3 교정 — "교란=능력 하한"을 "덜 오염 측정,
  clean lower bound 아님 (잔여 인지 5–6/8)"으로 교체 + lint (G) 금지 패턴
  ③ methodology_limitations §Instrument bias directions (4계기 편향 방향 표,
  k=1 게이트 거짓음성 산술 ≈34% 포함) ④ docs/FUTURE_CYCLE_PROTOCOL.md (Cycle 2
  위생: salt·GT sha256 봉인·카나리 2회·rolling holdout 승격 + repo 학습유입 시
  소모품 소각) ⑤ Issue #2 서사 보강은 **diff-only** — RP-14 + Q-R01.
  **정직 기록**: 미션 문면 "잔여 인지 4–5/8"은 동결 L-5(6/8·5/8)와 불일치 →
  repo 값 5–6/8 채택 (D31 deviation_note).
- **Phase 1 (D32/D33, 13호출)**: recognition gate k=5 승격 — HTZ 양성대조
  True(high) · **HUBG·WMK·GNE 전건 0/5** → 사전 규칙(≤1/5)상 자격 3/3 draw
  잡음에 강건 (결과 방향 (i), gate_k5_analyze.py 기계 판정). Issue #2 발행 보류
  긴급 항목 비발동. holdout_summary §1 + README 양어 병기, ISSUE_2는 RP-14 DIFF-2.
- **Phase 2 (D34/D35, 32호출)**: wave-2 outcome-recognition (branchless) —
  **실험군 knows_event 8/9=88.9% CP[51.7%,99.7%] vs 대조군 0/23 CP[0%,14.8%]**.
  event_only 5건(BRX·CGI·MDXG·TNGO·WFT) = name-ID 거짓음성 실증. **정직 판독:
  "덜 암기(wave-1의 절반)" 서사는 name-ID 계기 한정 — 직접 축은 wave-2 88.9% →
  홀드아웃 0%, 암기 제거는 wave-2→홀드아웃 사이.** R4 불변 (사전 등록 무분기).
  synthesis §1 2축 표 + README 양어 반영.
- **Phase 3 (D36/D37, 9호출)**: 정체 3-arm — 가공 사명(EDGAR 1,049,982행+티커
  10,418 전수 스크린, 충돌 0, 전건 attempt 0) 중첩 arm (b) 9호출. **median(b−a)
  =+6.0 · median(c−b)=−2.0 → 사전 분류 (ii) "암기의 점수 기여가 작다는 방향
  증거 (a≈b≈c)"** (N=9 방향 증거, 인과 확정 금지). synthesis §1b + README 병기.
- **Phase 4 (D38, 무호출)**: freeze 개정 #3 초안(docs/FREEZE_REV3_DRAFT.md —
  하네스→순수 SDK, J13-e 주입 제거, L-2·W8 해소 경로) + 스캐폴드
  (pipeline/api_client.py·runner_api.py·무호출 테스트 5건, 이중 안전장치,
  기존 러너 import 0). 발효는 Q-R02 (키·과금·시점 = 소유자 인프라).
- **미터링 가계부 (정직 기록)**: Phase 1 = 13 (HTZ 1 + 3케이스×4draws 12) ·
  Phase 2 = 32 (32사 × 1) · Phase 3 = 9 (arm-b 9) — **합계 54/60, 초과·낭비·
  재시도 0, FAIL 0, 핀 불일치 0.** 전 미터링 케이스/draw 경계 commit·push,
  미터링 커밋 CI 전건 green.
- **사고 기록 (무-미터링)**: D38 스캐폴드 커밋 `b456c18`~`27618ea` 2건 CI 적색 —
  test_api_client가 로컬에서만 통과 (`anthropic` 로컬 설치·CI 미설치, 페이로드
  가드가 SDK import 뒤에 있었음). `9d3af07`에서 가드를 import 앞으로 이동해
  복구 (가드 선행이 옳은 순서이기도 함) + anthropic 부재 시뮬레이션으로 재검증.
  교훈: 로컬 green ≠ CI green — 신규 의존성 접점은 push 직후 CI 확인까지가 완료.
- **소유자 액션 (이 미션분)**: ① RP-14 DIFF-1/DIFF-2 서명 (Q-R01 — Issue #2
  발행 서명에 선행) ② Q-R02 freeze 개정 #3 발효 결정 ③ (기존 계류) 3-이슈 발행
  결정 · E4 EXPLORATORY · Console $0.00 · Q-E01/E02.

> 이 미션의 신규 결과 판독 시 주의: D35(사건 지식 8/9 가용)와 D37(실명이 점수를
> 안 끌어올림)은 **서로 독립 계기의 병기**다 — 종합 해석("알지만 안 쓴다" 등)은
> 사전 등록 문장 밖이므로 세션이 서술하지 않았다. 소유자 검토 대상.

## 6-약점 교정 세션 완료 요약 (2026-07-09~10, 소유자 입회 — D24~D30)

- **Phase 1** 채점 57건 확정(D24, 오버라이드 0 + 고무도장 점검) → 이후 E1 9건
  추가 확정(D26) — **계류 채점 0**.
- **Phase 2** E5 §7 개정(홀드아웃 k=5 arm) + Q-E03 RESOLVED + 도구 4종 사전 커밋(D25).
- **Phase 3 (E1)** 감독 fetch→선정 9사→비인지 게이트(FWRD 탈락→XPO 승격)→채점:
  **HUBG 70만 매칭 대조군 상회** (RXO 42·BCO 30·XPO 20); WMK·GNE 분리 미검출;
  FPR 2/9 CP[2.8%,60%] (D26). holdout_summary §5 해소 + ISSUE_2 §3b.
- **Phase 4 (k=5)** HUBG **5/5 draw p≥50 [58–76] → 사전 규칙상 robust**;
  WMK/GNE 0/5 (D27). 발행 수치 draw-1 불변.
- **Phase 5** README/synthesis 백본 = standalone 유의성(0.00114/0.00116),
  AUC 비교 2차 강등 + CI 본문 병기; L-6 기입; lint canon() 배선 (D28).
- **Phase 6** 영어 README.md + README.ko.md 분리·린트 편입 (D29);
  **repo rename aaer-project→aaer-evals** (D30, GitHub 자동 리다이렉트).
- 미터링 세션 총 42 호출 (E1 30 [추정 18–27 +3: FWRD 탈락 1 + 비멱등 재실행 2] +
  redraw 12). CI 전 push green.
- 잔여 소유자 액션: ② 3-이슈 발행 결정 ③ E4 EXPLORATORY 문단 ④ Console $0.00
  (RP-13_final_packet §7). E2·E4·E5(wave-2 arm)는 launch-ready 동결 (Q-E01).
- 별도 계류: 원격 브랜치 `hardening/2026-07-08` (~3.9k줄, 소유자 검토 대기 —
  main 기준 진행 결정, 2026-07-09).

> 다음 세션: CLAUDE.md → PROJECT.md → 이 문서 → `review_packets/RP-13_final_packet.md`
> → `review_packets/RP-13_grading_workbench.md` → `RP-11_expansion_holdout.md`.

## RP-13 확정 요약 (2026-07-09, 소유자 대화형 세션)

- **채점 57건 전건 확정 (D24)**: wave-2 32 + 홀드아웃 3 + wave-1 대조군 22.
  TIER A 13 플래그 우선 개별 검토(경계 3·대조군 오탐 5·미탐 2·홀드아웃 3) →
  TIER B 22 재검증 서명 → grades_v2/controls 22 일괄(RP-09/RP-10 기근거).
  오버라이드 0건 — Issue #0 §9 고무도장 기준을 커밋 전 명시 제시, 소유자 확인.
- 적용기 `tools/apply_rp13_finalization.py` (신규) — 워크벤치 틱 파서 + OV 블록
  생성기. **주의: 확정 후 `tools/build_rp13_workbench.py` 재실행 금지 (틱 파괴).**
- 잔여 소유자 액션(RP-13_final_packet §7): ② 3-이슈 발행 ③ E4 EXPLORATORY ④ Console.
- 발견: Jul 8–9 무인 작업은 로컬이 아니라 원격 브랜치 `hardening/2026-07-08`에
  있음 (57건 워크벤치·finalize_grades.py 포함, ~3.9k줄) — 소유자 결정: main 기준
  진행, 브랜치는 별도 검토 세션으로 보류.
- 다음: 계획 Phase 2 (E5 §7 개정 커밋 → E1 스캐폴딩) — `~/.claude/plans/i-want-to-solve-happy-moonbeam.md`.

## OWNER-GATE-E 요약 (2026-07-08, 무인 세션)

- **거버넌스**: OWNER-GATE-E 기록(overrides.md) + spend 재량 **JE-1**(quota 소진을
  목표로 삼지 않음). OWNER_QUEUE Q-E01/E02/E03 · RESUME.md(재개 명령·가계부).
- **무-미터링 P-작업 전량**: P1 오류해부(`error_analysis_wave2_holdout.md` — 오탐=양성
  오독·미탐 비대칭·HUBG tier적중/기제빗나감·ECE 0.179) · P2 종합(`synthesis.*` —
  암기 dose-response, unified_table 65행) · P3 워크벤치(`RP-13_grading_workbench.md`
  35건) · P4 발행정합(README 3층 재작성 + `lint_publication.py` CI 편입) · P5
  재현성(`REPRODUCING.md` + `holdout_rescan.py` + matplotlib 핀) · P6(`RP-13_final_packet.md`).
- **E1–E5 사전 등록**(`analysis/*_PLAN.md`, `c1b85a7`, 채점 전 동결).
- **E3 실행 → R4 확증**: 교란 재추첨 18호출(피평가자 claude-sonnet-5, pin 18/18,
  FAIL 0, 채점자 0). median-delta dominance **4/9 < 5** → **R4 유지**(R3 미발동),
  per-case σ 3.2pp. 순서 증명: 사전등록 05:24 < 첫채점 05:47. **미터링 18/320.**
- **E1 보류**(무인 부적합 — 2026-era 대조군 네트워크 빌드 = §5-1 look-ahead, Q-E03).
  **E2/E4/E5 launch-ready**(Q-E01 spend 게이트). **미발행 유지, human_finalized=false.**
- **소유자 액션 4**(RP-13_final_packet §7): ① 채점 35 확정 ② 3-이슈 발행 결정
  ③ E4 EXPLORATORY 문단 ④ Console $0.00.

## (이전) RP-11 요약

> **현재 위치: Issue #0 초안이 여전히 소유자 발행 게이트(불변). RP-11 companion 2건:
> (1) wave-2 로스터 확정(생존 9), (2) 홀드아웃 RECOGNITION GATE → HUBG·WMK·GNE 3/3
> 비인지 admit(N=3). wave-2·홀드아웃 채점 human_finalized=false.**

## RP-11 요약 (2026-07-07, 이 세션)

- **P0**: README를 RP-10 정합으로 수정 (`67523af`) — RP-05 잔재 제거.
- **P1.0/P2.0 사전 커밋 (발사 전 타임스탬프)**: `analysis/ANALYSIS_PLAN_WAVE2.md`
  + `EXCLUSION.md` (`9438b0c`), `docs/HOLDOUT_CRITERIA.md` (`62d2fda`).
- **P1.1 wave-2 로스터 확정** (`190783b`, 점수 독립): A형 23 − 채점 8 − 오염 2
  (VRX·GE) − G-XBRL 실패 4 (PUDA 404 / MILL·DMND XBRL 채택이 폭로 후 / PWE
  IFRS) = **생존 9** BRX·CGI·CSC·HAIN·MDXG·OSIR·TNGO·UAA·WFT. 커버리지 주석:
  BRX(REIT 매출태그 결측) · OSIR(NI 분기 얕음).
- **P2.1 RECOGNITION GATE** (`0d64a7a`, freeze): 후보 3/3 knows_event=False →
  admit (N=3, H3-STOP 비발동). 양성대조 HTZ·KHC = knows_event=True high (계기
  검증). transcript `runs/holdout/recognition/`.
- **wave-2 채점 완료 (소유자 발사 승인)**: 대조군 23 선정 → 32 채점(9v23)+교란 9
  +프로브 64+채점자 32 (human_finalized=**false**) 동결 → **발동 규칙 R4 (능력
  시연)**: p=0.00116, AUC 0.829, R1/R2/R3 전부 비발동, 이름 프로브 25%(wave-1
  50%의 절반). `analysis/wave2_summary.md`.
- **홀드아웃 채점 완료 → H2**: 암기 불가 3사 per-case — HUBG p=70(탐지 d1=2) ·
  WMK 32 · GNE 42. N=3 → H1 과소검정(미주장), H2 병기. HUBG 기계 M/F 계산불능 →
  복제 아님. `analysis/holdout_summary.md`.
- **서사**: wave-1 R3(암기) → wave-2 R4(잔여능력) → 홀드아웃(암기 불가, HUBG
  잔존) — 암기 제거 축에서 Issue #0 확증.
- **P3 산출물**: RP-11 갱신 · Issue #1(R4)/#2(H2) 초안 갱신 · ISSUE_0 companion
  포인터. make verify green (402 files · reproduce 100/100 · pytest 76).
- **INCOMPLETE**: 홀드아웃 매칭 대조군 + H1 순열 (N=3 과소검정 — 후보 누적 후 재개).
- **소유자 게이트**: wave-2 32 + 홀드아웃 3 grades human_finalized=false 확정 ·
  Issue #0/#1/#2 발행 결정 (초안, 미발행).
- **비용(참고, 구독 흡수)**: recognition 5 $0.059 + wave-2 ~137 + 홀드아웃 6 호출.

## (이전) RP-10 — Issue #0 발행 게이트 (불변, 유지)

> 다음 실측 라운드 후보였던 "컷오프 후 홀드아웃"은 RP-11에서 착수됨(위).

## RP-10 요약 (2026-07-07 완료)

Phase 0 (A1 ADI→BHE 규칙 교체 · A2 검증 · ANALYSIS_PLAN R1-R4 사전 커밋 ·
불변량 검사) → Phase 1 발사 (74호출 FAIL 0 — 대조군 22 채점 32.5 중위/오탐 3
+ 프로브 30 식별률 50% + 채점자 22) → Phase 2 (M/F 기준선 무력, R2 비발동;
순열 p=0.00114; make analysis 재현) → Phase 3 (오류 해부·계층화·조기성 1-4q·
ECE 0.209·암기 산점도) → Phase 4 (Issue #0 초안) → RP-10 패킷. 사고 1건 D23
(이중 역할 5티커 아카이브 덮어쓰기 — PIT 동치 검증, I3 무침해, 도구 패치).

## RP-09 스테이지 상태 (재개 시 첫 미완 스테이지부터)

- [x] **Stage 0** — 채점 26건 human_finalized=true (D21, 인가: 986a893).
  이 커밋부터 scoring/grades/ + pilot/grades/ **I3 동결**. 실험군 정답 평가 종결.
- [x] Stage 1 — RP-07 D-2 종결 (8b21be9): 32호출 FAIL 0 · **draw-3 = 표본 잡음**
  (원본 프레임 5/5 ≥25pp) · delta 분해 7/8 실효 (HTZ +30 vs MON −16 대칭) —
  `review_packets/RP-07_robustness_closure.md`
- [x] Stage 2 — CONTROL_CRITERIA_v2 (b22e84e + S0 개정) → 풀 재수집·4층 검증
  PASS(격리 0) → **22선정** (`runs/rp09/control_group_v2.json`, 복원 3/3:
  GRMN·FORR·GIS) → 메모 `review_packets/RP-09_control_v2_memo.md` (표 22 ·
  3픽: ADI·CPB·UPBD · 웹스크린 블록)
- [x] Stage 3 — 채점 준비 패키지 (fe8b767): 런북 `tools/run_control_v2_scoring.py`
  (게이트 `RP-09-FINAL: YES` in overrides.md) · 프로브 분석 계획 사전 등록 ·
  검정력 사전 계산 (rp09_power.json) · probe_runner 병렬화 — **발사 안 함**
- [x] Stage 4 — docs/EARLINESS_DESIGN.md (MON 부적격 플래그, 112–160호출 추정)
- [x] Stage 5 — docs/FUTURE_HOLDOUT_CANDIDATES.md (Tier2 공집합 — 월간 재조사)
- [x] Stage 6 — docs/AUDIT_STATE.md (I1–I3 PASS · pytest 74 · reproduce 100/100)
- [ ] Final — 소유자 단일 결정: "control_group_v2 승인 + 채점 발사: YES / AMEND"
  (YES 시: overrides.md에 `RP-09-FINAL: YES` 줄 기록·커밋 →
  `python3 tools/run_control_v2_scoring.py --launch`)

## 이전 사이클 위치 (참고): RP-06 완결 + RP-08 v1.1 산출물 커밋 (ed2e132)

RP-05 결과(불변) 위에 RP-06 강화 사이클 완료: A1 인지 재추첨 8 + A2 교차
채점 6 + A3 표본분산 k=5 64 = **78호출 (FAIL 0 · 핀 불일치 0)**, 전 산출물
runs/hardening/ 커밋. 발행 수치 재현·블라인드·매니페스트는 CI가 매 push
검증한다 (`tools/reproduce_analysis.py` 100/100 · `tools/verify_blindness.py`).

## 소유자 대기열 (RP-09로 재편 — ③④ 완료, ⑦ superseded)

> RP-09 지시로: ③ 워크벤치 검토 + ④ 채점 26건 확정 = **완료 (Stage 0, D21)**.
> ⑦ RP-08 아침 게이트의 v1.1 PROPOSED는 **Stage 2의 v2로 supersede** — 서명
> 대상은 이제 control_group_v2 하나. 잔여 소유자 항목: ② Console $0.00 확인,
> ⑤ A1/A3 판독, ⑥ 발행 결정, 그리고 **RP-09 §Final 단일 결정**.

1. ~~**RAT-001 서명**~~ — ✅ **완료 (2026-07-07)**: 소유자 추인 서명
   (세션 내 직접 진술 전사 — `scoring/overrides.md` RAT-001 서명 블록).
2. **Console 대시보드 $0.00 확인** (RP-04 check C) — 구독 외 종량 과금
   부재의 소유자측 확인. (참고 합계: RP-06 total_cost_usd $24.83 — 기록
   전용, 과금은 구독 OAuth 경로.)
3. **워크벤치 검토** — `review_packets/RP-06_grading_workbench.md`,
   **MODEL 귀속 5건(⚑ SKEPTICAL-REVIEW) 먼저**, UNCLASSIFIED 2건(MRVL)의
   DATA(설계) PROPOSAL 판정 포함. 참고: A2 교차 채점 밴드 일치 6/6 ·
   Ryder 오탐은 k=5 중 최대값 1회 관측 (RP-06 §3-2 각주 자료).
4. **채점 26건 확정** — human_finalized=False → true 갱신, 오버라이드는
   overrides.md 기록 ("채점: Claude 보조 + 인간 최종 확정").
5. **A1/A3 판독 → 발행 프레이밍 확정** — RP-06 §1/§3: **정체 인지
   주의문("perturbation disrupts memorized NUMBERS, not IDENTITY
   recognition")은 README 헤드라인 문장에 이미 병기** — 유지 여부가 소유자
   결정. A3 밴드 문구(p·AUC 강건 / 분리 4/5 / delta 분해 부분 해소)의 주장
   강도 서열 확인 (RP-06 §5).
6. **발행 결정** (소유자 확정 사항 — §7). GO 시 README.md가 발행 관문
   (보고 언어 제약 3-6 적용 완료 상태).
7. **RP-08 아침 게이트** (2026-07-07 야간 산출, D19 사전 승인) —
   `review_packets/RP-08_selection_memo.md` §0 순서대로: 메모 통독 →
   스팟체크 3건(T12 Fortinet → T17 First Solar → T28 Campbell) →
   `docs/CONTROL_CRITERIA_v1.md` 서명/수정 (v1.1 개정 후보 2건 포함) →
   `runs/rp08/control_group_PROPOSED.json` 서명/기각. **서명 전 채점
   파이프라인 진입 금지** (status 필드 강제). 기각 재실행은 분 단위
   (memo §0 명령). ①~⑥과 독립 — RP-05 결과·RP-01 확정 대조군 불변.

## 유예 등록부 (DEFERRED — 실행 금지, 소유자 지시로만 개시)

- **D-1**: 논문/공개 모니터 write-up 초안 — 대기열 ④·⑤ **이후에만**
  (프레이밍이 A1/A3와 확정 채점에 의존).
- **D-2**: k>5 에스컬레이션 — A3 분해가 미해결(케이스 단위 delta 4/8 잡음
  분리 불능; 병목은 **원본 쪽 k=1**이므로 실체는 원본 재추첨 +32호출)이고
  **동시에** 발행 GO일 때만.

## 이 사이클의 고정값 (불변 — 이전과 동일 + RP-06 추가분)

- freeze `82a7717` + 로그된 개정 2건 + RP-06 addendum (기준 무변경 —
  `git diff 9dfcf44..HEAD -- review_packets/RP-05_results.md scoring/grades/`
  = 공백으로 증명).
- 모델 실측: 피평가자 claude-sonnet-5 단독 서빙 (72호출) / 채점 fable-5
  (본채점, 폴백 0) · opus-4-8 (A2 스팟체크 6호출 — 설계 고정). 하네스
  v2.1.201 재확인. 인증 = 구독 OAuth, API 키 부재 전 호출 assert.
- 원시: runs/ (MANIFEST.sha256 변조 증거) · scoring/grades/ (무변경) ·
  runs/hardening/ (신규 — probe_recognition·regrade_opus·draws, 본채점 비병합).

## 금지·주의 (유효 지속)

- 세션 내 피평가자 판정 생성 금지 — 러너 경유만. runs/hardening 출력을
  scoring/grades/ 에 병합 금지 (SPOT-CHECK 라벨).
- 보고 언어 제약 전부 유지 (% 헤드라인 금지 / 상한 명기 / 오염 명시 /
  BOUND-not-eliminate / 선택·생존 편향 / **L-5 정체 인지 주의문 헤드라인
  병기** / L-2~L-4 인용).
- 로컬 커밋은 기록이 아니다 — push까지. **push도 끝이 아니다 — CI green까지**
  (push 후 `gh run list -L1` 확인. 2026-07-07 실측: be95e75~b22e84e 구간 CI가
  연속 실패했는데 아무도 몰랐다).
- **runs/ 아래 파일을 추가·수정하는 모든 커밋은 커밋 전에
  `python tools/verify_blindness.py --write-manifest` 를 포함**해야 한다 —
  verify_blindness (d)가 runs/ 전체를 전역 MANIFEST와 대조하므로, 하위
  디렉토리 전용 매니페스트(_rp08 등)만 갱신하면 CI가 깨진다 (위 실측의 원인).

---

# 2026-07-16 서명 일괄 세션 (D90~D96, 미터링 0)

**전 서명 인용**: (owner, 2026-07-16, this session's structured decision
responses). 결정 12건 전부 해소 — OWNER_QUEUE에 서명 전 OPEN 항목은
Q-F02(소유자 원문 대조)·Q-F07(교차 채점자)·Q-M01(FINRA ToS)·Q-M05(§5 절단)·
Q-M06(7호출 옵션)·Q-M07(P5 32호출)만 남음 (전부 종전 지위 그대로).

- D90 RP-17 수용 — CLAUDE.md 방법론 규율 6·7·8 발효 (사후 개정 한계·5게이트·단일 작성자)
- D91 RP-15/16 적용 — Big R 정밀화·서수 언어 (repo 표면 완료; GH Issue 편집은 아래)
- D92 RP-18 승인 — 배치 A, 게시 텍스트 `review_packets/RP-18_body.md`
- D93 Q-O01/Q-O03 서명 — GIL 메모 확정 (제목 1안), access_log 해시 핀
  (스냅샷 sha256 856d50f3984d, hash-only, 원본 미커밋 + .gitignore)
- D94 Q-O02 서명 — DECISION_TABLE README 양어 등재
- D95 Q-O04 발효 — (A) 협의 SIC·12개·float ≥$1B; 열거는 차기 감독 세션
- D96 Q-F08 감사 계획 사전 등록(실행 보류)·Q-M04 정당 보류

## 게시 절차 (소유자 실행 — 세션 게시 금지 계약)

1. **Issue #4 (GIL 메모)**: `analysis/ISSUE_4_GIL_MEMO_DRAFT.md`의
   "Proposed issue body" 절을 그대로 게시:
   `gh issue create --repo lastwhisper906-gif/aaer-evals --title "EQ Memo #1 — Gildan Activewear (GIL): what pre-report filings alone reconstruct" --body-file <본문 추출본>`
   → 게시 후: README 양어 Publication 절에 URL 추가 · ISSUE_4 헤더 PUBLISHED
   갱신 · URL D-엔트리 (차기 세션 가능).
2. **RP-18 코멘트**: `gh issue comment 2 --repo lastwhisper906-gif/aaer-evals --body-file review_packets/RP-18_body.md` → URL D-엔트리.
3. **Issue #1/#3 편집 (RP-15/16 반영)**: GitHub 웹 또는 `gh issue edit` —
   ISSUE_0_DRAFT §5 보정 불릿·ISSUE_2 §7 첫 불릿·§2 표 헤더의 현재 repo
   텍스트를 각 이슈 본문에 반영. **edited 표시 + 사유 코멘트** ("RP-15/16
   owner-signed 2026-07-16 — label precision + ordinal language; frozen
   source texts in analysis/ISSUE_*_DRAFT.md, ledger D91").
4. **독자 발송 5–10명**: `docs/reader_validation/OUTREACH_MESSAGE.md`의
   {ISSUE_URL}을 1의 게시 URL로 치환 → 발송 → TARGET_LIST 기입 (Q1/Q2/Q3
   verbatim 열). **미발송 시 Tier 3 검증 0점.**

차기 감독 세션(네트워크): RESUME.md 말미 — ① 유니버스 열거 (Q-O04 발효분)
② 생존 편향 감사 (SURVIVORSHIP_AUDIT_PLAN) ③ 게시 잔여 확인.
