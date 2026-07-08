# AUDIT_FINDINGS — 전면 스캔 (2026-07-08, 무인 재개 세션 #2)

> 소유자 지시 "scan all detail, check improvements/research"에 따른 저장소 전면 감사.
> 3개 병렬 감사 패스(방법론·통계 / 코드·테스트·재현성 / 문서·발행정합) + 직교 스캔.
> **FIXED = 본 세션 안전 수정(비동결, CI green). PROPOSED = 소유자 판단(OWNER_QUEUE).**
> 원칙: 동결/발행 수치 불침해, 가드 약화 금지(강화만), 방법론·발행 결정은 self-resolve 안 함.

## A. 안전 수정 (이 세션에서 처리 — 비동결·가드 강화·명백 버그)

| # | 발견 | 근거 | 상태 |
|---|---|---|---|
| A1 | 러너가 모델 출력을 **정식 스키마(llm_output.json) 미검증**으로 기록 → 계약 위반 아티팩트가 OK로 저장, 멱등 깨져 재-미터링, p 무경계 | runner.py MODEL_SCHEMA(0-100·minItems·p≥40 조건 없음) vs schemas/llm_output.json; runner.py:141-151 full 미검증 write | FIXED |
| A2 | build_payload look-ahead 필터(filed≤cutoff)가 **CI 미검증**(캐시 없으면 test 전량 skip) | test_build_payload.py:16-18 skipif; CI 4 skip | FIXED |
| A3 | `lint_publication` (F) 수치정합 검사가 **dead code**(canon() 미호출) → 산문 drift가 green CI 통과 | lint_publication.py:37-49 canon() 무호출, docstring §9-11 과대광고 | FIXED |
| A4 | `synthesis.py` 중위수 버그: `sorted(x)[len//2]`가 짝수 n에서 상위중앙 반환 → wave1 fraud median **60.0**(정답 57.5) | synthesis.py:126-127; frozen scores median 57.5(results_stats.json) | FIXED |
| A5 | `REPRODUCING.md` "76 passed" stale (실제 101 passed 4 skipped) | REPRODUCING.md:13,31,36-37 | FIXED |
| A6 | Issue #1 헤더 "human-finalized" ↔ 본문 "human_finalized=false" 모순; Issue #0도 동일 | ISSUE_1:4 vs :73; ISSUE_0:62 | FIXED |
| A7 | 발행 후보 문서에 생성 잔재 `</content>` 태그 | ISSUE_1:102, ISSUE_2:113, wave2_summary:80, holdout_summary:64, ANALYSIS_PLAN_WAVE2:119 | FIXED |
| A8 | 문서/코드 stale docstring: cli_client "max-turns 1"(실제 2) | cli_client.py:13 vs :176 | FIXED |
| A9 | README가 `reproduce_analysis`를 "발행 수치 전건 재계산"으로 과대표기(실제 RP-05 파일럿만) | README:99-105; reproduce_analysis.py:29-31(p=0.0226) | FIXED |

## B. 소유자 판단 / 리서치 (OWNER_QUEUE Q-E07~ 로 이관 — self-resolve 안 함)

### B-발행/정합 (owner-judgment)
- **B1 (HIGH)**: Issue #0의 22 대조군 grades가 `human_finalized=false`인데 draft는 "all grades human-finalized"로 주장. 게다가 이 22 v2 대조군은 RP-13 서명 워크벤치(wave-2 32 + 홀드아웃 3)에 **미포함** → 확정 경로 부재. (문서 문구는 A6에서 수정, 실체 확정은 소유자.) 근거: scoring/grades_v2/controls/*.json 22/22 false.
- **B2 (HIGH)**: 현재 헤드라인(8v22 p=0.00114·AUC 0.824·wave2·홀드아웃)을 **CI가 재계산 검증 안 함**(reproduce_analysis는 RP-05 파일럿만). 발행 "verifiable" 기둥과 불일치. → A9로 문구는 정정, **실측 검증 추가는 리서치 항목**(B9 참조).
- **B3 (MED)**: Issue #2 라이브 3사(HUBG/WMK/GNE) 달러 수치에 §6-2 공시 원문 링크(accession) 부재.
- **B4 (MED)**: RP-13/HANDOFF "E2/E4/E5 launch-ready"가 Q-E04/E05(미구현·캐시부재)로 superseded인데 병기 없음.
- **B5 (MED)**: Issue #0 §8이 홀드아웃을 "future work(미실행)"로 서술하나 Issue #2가 실행함(N=3). 각주만 존재.
- **B6 (LOW)**: Issue #0 §5가 라이브 대조군 3사를 실명 "false positive"로 명시(§6 라이브사 주의) — 익명화 여부 소유자 확인.

### B-방법론/통계 (owner-judgment + research)
- **B7 (HIGH)**: wave-1 R3(암기 우세) 헤드라인이 **정확히 5/8** 경계에서 발동, SCOR는 임계 대비 +0.8pp(1 SEM 이내). 1건 이탈 시 4/8 → R4로 결론 반전. → frozen 재추첨(k=5) 부트스트랩으로 P(count≥5) 공개 권고.
- **B8 (HIGH)**: 암기 dose-response가 **대조군 주도** — fraud-side name-ID는 wave1 37.5%→wave2 33%로 거의 불변, 하락은 대조군 유명도. wave1→wave2 leg의 독립 근거 약함. fraud/control name-ID 분리 보고 권고.
- **B9 (HIGH·research)**: 홀드아웃 "capability 잔존"이 **단일 케이스 HUBG=70**에 의존하고 그마저 기제 빗나감(dim2=1), **매칭 대조군 0**. → **E1(감독 실행)**이 최고가치 공백(신규 fraud·look-ahead 추가 없음). 그전엔 "tier hit, mechanism miss" 일화로 표기.
- **B10 (MED)**: ECE(0.209/0.179)가 n≈3/bin 점추정·무CI·기저율조건부. 부트스트랩 CI + adaptive-binning + base-rate 명시(frozen 점수 재사용, 재채점 아님).
- **B11 (MED·research)**: 단일 채점자(fable-5) IRR 없음, human_finalized=false. → **frozen 피평가자 출력에 2차 채점자**로 Cohen's κ 산출(피평가자 재채점 아님) → dim2 forensic 주장의 불확실 밴드.
- **B12 (MED)**: 교란 프레임 flag 검정 p=0.06(4/8)인데 헤드라인은 유리한 AUC 0.86만 인용. flag 4/8·Fisher p=0.06 병기 권고.
- **B13 (MED·research)**: R3 계수가 **점수 부풀림(HTZ +30)과 억제(MON −16)를 |Δ|로 합산**. signed effect 보고 + "정체 인식이 탐지를 돕나 해치나" 연구질문(MON=유명무죄 prior).
- **B14 (LOW-MED)**: 기계 베이스라인이 complete-case(22/30)만 — 비무작위 결측, 그 부분집합에서 스크린 무력. ρ·잔차검정 complete-case 한정 명시.
- **B15 (research)**: wave-1 delta의 sampling-vs-memorization 분해(E3가 wave-2에 한 것의 wave-1판) — B7 취약성을 frozen 재추첨만으로 직접 해소.
- **B16 (research)**: E2 조기성(하네스 이번 세션 구현 완료) — lead-time 실무 질문 미답. 캐시 복원 후 발사(owner-gate).

### B-코드/가드 (owner-judgment)
- **B17 (MED)**: `probe_verdict.name_match` prefix 규칙 과매칭("Apple"⊂"Apple Hospitality") → n_recog 부풀림(D7 오염판정 보수적이나 무검정). 전체토큰/최소공유토큰 규칙 + 테스트.
- **B18 (LOW-MED)**: 러너가 출력의 canary_hit를 기록만 하고 FAIL 안 함(verify_blindness가 downstream 포착 — defense-in-depth). 탐지 즉시 hard-FAIL 승격 검토.
- **B19 (MED)**: build_payload 페이로드 빌드를 cutoff_guard 게이트웨이 경유로 라우팅할지(현재 인라인 필터 + A2 CI 테스트로 강화). 아키텍처 결정.

## C. 소유자 직접 산출물 (내가 대신 못 함)
- **C1**: §9 사전/사후 자가평가 diff — `docs/self_assessment/week4.md` 미작성(day0만 존재). 성공지표(§5). 소유자 본인 언어·무검색 규칙이라 대필 불가.

## 강점 (수정 대상 아님 — 노력 낭비 방지)
기저율 번역(PPV@0.7%, 0%FPR 금지, Clopper-Pearson) · 선택/생존편향 명시(sr11-7) · look-ahead 코드가드 fail-closed + EDGAR 대조 · 사전등록 순서증명 real · cli_client 격리/핀/페이로드가드 실스텁 테스트 · earliness_grid 순수 property 테스트 · numpy 부재로 수치 결정성.
