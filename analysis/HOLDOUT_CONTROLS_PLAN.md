# E1 사전 등록 — 홀드아웃 매칭 대조군 (H2의 구멍 메우기)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-08, OWNER-GATE-E.
> **본 파일은 E1 첫 채점 전에 커밋된다 (freeze-commit-then-run, §5-6).** 커밋 후
> 불변 — 실행 후 수정 금지. 채점 순서는 아래 §5에 사전 고정(quota 절단 = 결과 독립).
> 범위 한정(§5-5): Claude 단일 파이프라인(claude-sonnet-5 핀).

## 0. 동기 (왜 E1인가)

홀드아웃 per-case 점수 HUBG 70 · WMK 32 · GNE 42는 **컷오프-후 매칭 대조군 분포가
없어** 해석이 불완전하다. "70"이 높은지 낮은지는 같은 프레임·같은 시대에서 clean
회사가 어떤 점수를 받는지를 알아야 판단 가능하다. E1은 그 대조 분포를 만든다.
**H1(순열 유의성)은 N=3에서 과소검정이라 주장하지 않는다** — 이 사실을 사전 명시하고
(§4), E1의 산출은 per-case 점수 대 대조군 분포의 **병기(H2 강화)**이지 유의성 주장이
아니다.

## 1. 대조군 선정 — 동결 순수 함수 (수기 지명 금지)

- **기준**: `docs/CONTROL_CRITERIA_v2.md` 전조항 승계 + **E8b 집행이력 부적격 체크**
  (소유자 확인 비-AAER 집행 테이블) + **S0-v2 정정**(frames 조잡 게이트→우선순위,
  비달력 FYE 오배제 방지). 선정 = 기준+검증된 풀의 **순수 함수, 네트워크 없음**.
- **매칭 축 서열 (S2-v2)**: 규모(|log PIT 매출비| 0.05 버킷) → 산업(SIC 계층) →
  시대(FYE 월 원형거리) → CIK 타이브레이크. 홀드아웃 각 케이스의 컷오프를 대조군에
  **복사**(구조 동일).
- **케이스당 2–3 대조군** (S3-v2, 최소 2, 자격자 부족 시 있는 만큼 + 플래그).
  목표 6–9 대조군 (홀드아웃 3사 × 2–3).
- **매칭 대상 프로파일** (홀드아웃 프레임 — identity, 컷오프=폭로 전일):
  - HUBG (case_71, 컷오프 2026-02-04): 트럭운송/물류(SIC 4700대), 매출 ~$4B.
  - WMK (case_72, 컷오프 2026-02-19): 식료품 소매(SIC 5411), 매출 ~$4–5B.
  - GNE (case_73, 컷오프 2026-03-11): 에너지 소매/캡티브(소형), 매출 ~$0.4B.
- 산출: `runs/holdout/controls/control_group_holdout.json` (status: PROPOSED — 소유자
  §Final 없이도 GA-001 연속 실행 하 채점 진입 가능하나 human_finalized=false 유지) +
  전수 also-ran + 절단 기록.

## 2. 컷오프-후 비인지 게이트 (모든 대조군 필수 통과)

- 각 선정 대조군에 **recognition probe** 실행 (홀드아웃 프라우드와 동일 계기):
  익명 페이로드에서 "이 회사가 최근 restatement/non-reliance 사건을 겪었는가"
  knows_event 프로브. **knows_event=False 여야 admit** (컷오프 후라 구조적으로 비인지
  기대). transcript는 `runs/holdout/controls/recognition/`에 커밋.
- knows_event=True인 대조군은 **탈락**(차순위 alternate 자동 승격 — 순수 함수 재실행).
  이는 대조군이 "폭로를 아는" 오염을 차단한다(실험군 홀드아웃과 동일 게이트).
- 게이트는 name-ID(정체 인식)가 아니라 **event 인지** — 정체는 알아도(예: "Pennsylvania
  supermarket") 폭로 미인지면 admit (홀드아웃 프라우드 admit 논리와 동일).

## 3. 페이로드·불변량

- **identity frame PRIMARY** (홀드아웃 프라우드 프레임과 일치 — 대조 유효성). 교란
  프레임은 부록(선택, 이 라운드 미실행).
- cutoff_guard: 각 대조군 자신의 매칭 컷오프(=대응 홀드아웃 케이스 폭로 전일)에서
  능동 — raising, never silently filtering. verify_blindness 신규 페이로드 배치마다.
- I1 스키마 무변경(case_input 필드만). 중립 ID: `hc_NN`, 매핑은 채점 전용
  `scoring/id_mapping_holdout_controls.json`.
- EVALUATEE_FORBIDDEN_MARKERS 값 수준 가드(cli_client) 전건 통과 필수.

## 4. 분석 — 사전 고정

- **1차 산출 (H2 강화)**: per-case 홀드아웃 프라우드 점수를 **매칭 대조군 분포와
  병기**. 예: HUBG 70 vs {HUBG 매칭 대조군 2–3사 점수}. per-case 표 + 점플롯.
- **정확 소표본 분리 검정 = CONTEXT ONLY**: 홀드아웃 프라우드(N=3) vs 전체 대조군
  (6–9)에 정확 순열/Mann-Whitney를 **참고로만** 보고. **H1(유의성 주장) 미충족·미주장을
  사전 명시** — N=3은 과소검정, p값은 맥락 수치이지 결론 근거가 아니다.
- **FPR**: 대조군 중 p≥50 개수. **rule-of-three 언어**(fp=0이면 상한 3/n; fp>0이면
  Clopper-Pearson). **0% 헤드라인 금지**. wave-1/wave-2 FPR과 병기(교차 비교는 CP
  구간 겹침 명시 — worse/better-but-not-provably).
- **HUBG 기제 재확인**: E1 대조군 분포와 무관하게, HUBG 70이 대조군 상단이면 H2
  방향 강화; 단 P1의 "tier 적중/기제 빗나감(dim2=1)" 단서 유지 — 대조 우위가 forensic
  기제 정확성을 입증하지 않는다.

## 5. 채점 순서 (사전 고정 — quota 절단 시 결과 독립)

케이스 알파벳순, 케이스 내 대조군은 hc_NN 오름차순:
1. GNE(case_73) 매칭 대조군 → 2. HUBG(case_71) 매칭 대조군 → 3. WMK(case_72) 매칭 대조군.
각 대조군: (a) recognition probe → (통과 시) (b) identity-frame 채점 → (c) 채점자.
케이스 경계마다 freeze·commit·push (RESUME.md 갱신). 절단은 케이스 경계에서만.

## 6. 호출 추정 (E1)

- recognition probe: 6–9 · 채점: 6–9 (통과분) · 채점자(grader): 6–9. **≈ 18–27 호출**
  (미션 추정 ~30 이내). 전역 320 cap에 계상.

## 7. 결론 처리 (사전 명시)

- 대조군 분포가 홀드아웃 프라우드보다 **낮으면**: H2 방향(암기 불가에서도 신호 잔존)
  강화 — 단 N=3, 통제 아님, gradient 방향 증거로만.
- **겹치거나 높으면**: 정직 보고 — "N=3 홀드아웃에서 매칭 대조군 대비 분리 미검출"
  (미화 금지 §10). HUBG 단일 우위는 per-case 일화로 한정.
- 어느 쪽이든 `analysis/holdout_summary.md` §5(INCOMPLETE: 매칭 대조군) 해소 +
  Issue #2 초안 갱신. **발행 안 함**(소유자 게이트).

## 8. 면책

단일 Claude 파이프라인, 채점 Claude 보조 + 인간 확정 대기. 대조군="비집행"(무결
아님). 홀드아웃 G2 provisional — "fraud"·"분식" 금지, restatement/non-reliance로만 서술.
