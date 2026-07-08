# HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-08, OWNER-GATE-E — E3 실행/R4 확증 + P1–P6, E1 보류)

> 다음 세션: CLAUDE.md → PROJECT.md → 이 문서 → `review_packets/RP-13_final_packet.md`
> → `review_packets/RP-13_grading_workbench.md` → `RP-11_expansion_holdout.md`.
> **최신 상태는 아래 "재개 세션 #2".**

## 재개 세션 #2 요약 (2026-07-08 야간, 무인 ~14h 창) — 미터링 0, 하드 스톱 + E2 하네스 구현

- **미터링 플랜 하드 스톱 (Q-E04)**: fresh ephemeral 컨테이너에 `~/aaer-data` PIT 캐시(git
  밖 402파일 SEC) 부재 → E2/E5/E4 전 유닛의 build_payload가 **API 호출 전** FileNotFoundError.
  캐시 재생성=네트워크 fetch=미션 최상위 금지·§5-1 → **무인 실행 불가, 미터링 18/320 불변(0 소비).**
- **E2 조기성 하네스 구현 (Q-E05, 소유자 "keep going/권한 최종" 지시 반영, 0-미터링·0-네트워크)**:
  "launch-ready"로 기술됐으나 실제 **미구현**(EARLINESS_DESIGN §5 "설계만")이던 하네스를
  오프라인 구현·검증. 커밋 `4aec7bf`(그리드)·`799acc4`(base_id)·`bb90ca4`(생성기)·
  `893ecdb`(런북)·`51439d1`(분석):
  · `pipeline/earliness_grid.py` — 순수 스냅샷 그리드 + look-ahead 가드 G1(폭로상한)/
    G2(인접누출)/G3(중복일). `pipeline/build_payload.py` base_id(스냅샷 간 동일 k, 하위호환).
  · `tools/build_earliness_snapshots.py` — 선정(데이터드리븐 21=detected13+대조군8) + 그리드 +
    스냅샷별 cutoff_guard 경계검사(≤폭로, fail-closed). `analysis/earliness_analyze.py` — §3 지표.
  · `docs/EARLINESS_RUNBOOK.md` — 발사 절차(캐시복원 + `EARLINESS-LAUNCH: YES` 게이트).
  · 신규 테스트 19건(전부 캐시/점수 불요, CI 상주). 전체 97 passed 4 skipped, reproduce
    100/100, lint PASS, CI green(run #66).
- **E2 = 생성→(채점 owner-gate)→분석 turnkey.** E5 draw-2/3·E4는 기존 러너 재사용(무코드),
  캐시 복원 시 즉시 launch-ready. **채점 미발사 — 발사는 소유자 권한이 마지막(캐시+토큰).**
- **불변식 3 무침해**: 실행 0. build_payload 변경은 하위호환(기본=바이트동일). runs/main·
  frozen grades·published draw-1 무변경. cutoff/blindness 경로는 **강화만**(신규 가드), 약화 0.
- **소유자 결정**: Q-E04(감독 하 캐시 복원) · Q-E05(E2 발사 게이트) · 기존 Q-E01/02/03 +
  RP-13 §7 액션 4 유지.

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
