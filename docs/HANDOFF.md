# HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-10, 잔여 교정 미션 D31–D38 전 Phase 완료)

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
