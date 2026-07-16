# AAER Evals — 이해상충 없는 회계 품질 신호의 백테스트

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> 본 결과는 Claude 기반 단일 파이프라인(피평가자 claude-sonnet-5 핀)에 한정된다
> (PROJECT.md §5-5). **These controls BOUND memorization risk; they do not eliminate it.**

## 무엇인가

상장사 회계 품질에 대한 독립 신호는 구조적 공백이다: 감사인은 피감사인이 보수를
지급하고, 셀사이드는 거래 관계가 있으며, 신용평가사는 발행사가 수수료를 낸다. 이
저장소는 그 공백을 겨냥한 장치 — **LLM이 point-in-time 구조화 공시 데이터만으로
왜곡표시 위험을 스크리닝할 수 있는가** — 를 SEC 집행(AAER) 확정 사건과 매칭 비집행
대조군으로 백테스트하고, 컷오프-후 홀드아웃(암기 불가)으로 그 능력을 독립 검증한 기록이다.
포지션 없음 · 교육·정보 목적 · 투자 조언 아님.

## 발행 (v1.0 — 2026-07-11, 소유자 서명 D40/D41)

3-이슈 시리즈를 GitHub Issues로 발행했다 (시리즈 번호 0/1/2; GitHub 번호
1/2/3). 게시된 이슈가 발행 표면이고, `analysis/ISSUE_*_DRAFT.md`는 그 동결
원문이다.

- **Issue 0** (wave-1, R3 — 암기 얽힘 분리): <https://github.com/lastwhisper906-gif/aaer-evals/issues/1>
- **Issue 1** (wave-2, R4 — 잔여 능력, 범위 한정): <https://github.com/lastwhisper906-gif/aaer-evals/issues/2>
- **Issue 2** (컷오프 후 홀드아웃, H2 — 암기 불가 축): <https://github.com/lastwhisper906-gif/aaer-evals/issues/3>
- **인용 가능한 동결점**: 릴리스 [v1.0.0](https://github.com/lastwhisper906-gif/aaer-evals/releases/tag/v1.0.0) (annotated tag, 발행 동결값 그대로).

## 헤드라인 — 3층 서사 (암기 축을 따라 벗겨내기)

발동 결론 규칙은 **사전 커밋**된 R1–R4 / H1–H3의 기계 판정이다(점수 존재 전 커밋 —
freeze-commit-then-run). 세 층은 "얼마나 암기 가능한가"로 정렬된다:

**① 유명 사건 (wave-1, 실험군 8 vs 대조군 22) → R3 (암기 얽힘).**
LLM은 확정 분식을 대조군과 분리하나, 그 점수는 모델이 각 회사에 대해 *기억하는 것*과
얽혀 있다. **읽는 순서는 교란(정체-가림) 우선** — 단, 교란 프레임은 *덜 오염된*
측정이지 **깨끗한 능력 하한이 아니다**: 교란 후에도 잔여 정체 인지가 지속된다
(recognition-probe draw별 실험군 8사 중 5–6사 실명 지목 — L-5). 이 설계에서
구조적 하한은 컷오프-후 홀드아웃(③)뿐이다:
- 교란 프레임: 순열 p = **0.0021** / AUC **0.864** [0.722, 0.969] / 플래그 4/8.
- 정체-노출(원본, 얽힌 상한): p = **0.00114** (100k, one-sided) / 평균차 **+19.8pp**
  (중위 57.5 vs 33.0) / AUC **0.824** [0.599, 0.983] — N=30 불안정, 점 그림이 1차 시각.
- 암기 분해: 8케이스 중 **5건**이 R3 임계 초과. 익명 페이로드 이름 지목률 **50%**.

**② 덜 유명한 사건 (wave-2, 실험군 9 vs 대조군 23) → R4 (잔여 능력).**
암기 지표가 약해 R3가 비발동 → 분리가 암기·기계신호로 설명되지 않는 잔여 능력을 시사:
- 순열 p = **0.00116** / 평균차 **+20.6pp** / AUC **0.829** [0.616, 0.983] / 플래그 7/9.
- 이름 지목률 **21.9%**(동결 name_match 규칙; 사람 판독 25% 병기 — 단일 경계 케이스
  DAR, `analysis/synthesis.json` §reconcile) = **wave-1의 절반**. 정체-교란 dominance
  3/9(과반 미달) → R3 비발동. **R4 프레이밍 제약**: 벤치마크 정확도/AUC 비교 주장 금지.
- **outcome-recognition 프로브 (실명 노출, 2026-07-10 실행, 사전 등록 D34 — 무분기,
  R/H 판정 입력 아님): 모델은 실험군 9사 중 8사의 집행/정정 사건을 상기한다
  (88.9%, CP [51.7%, 99.7%]; 대조군 0/23, CP [0%, 14.8%]).** 5사는 익명 페이로드
  에서 이름은 복원 못 하나 실명을 주면 사건을 안다(name-ID 거짓음성 방향). 정직
  한정: "wave-1의 절반" 판독은 **name-ID 계기에 한정** — 직접 계기로는 정체-노출
  프레임(발행 1차)에서 사건 지식이 광범위하게 가용했다. R4 불변(입력은 교란
  dominance 3/9). `analysis/outcome_recognition_results.json`.
- **정체 3-arm 실험 (사전 등록 D36, 2026-07-10 실행)**: 동일 교란 페이로드를
  가공 사명(EDGAR 전 filer 1,049,982행 충돌 전수 스크린 통과) 하에 재채점.
  **1차 증거는 b−a 대비(+6.0pp median)** — 동일 교란 페이로드에 이름 토큰만
  다른, 이 설계의 유일한 깨끗한 인과 대비. **c−b 대비(−2.0pp median)는 2차
  혼입(confounded) 관찰** — arm (c)는 실명과 실수치(원본 스케일)를 함께
  복원하므로 정체 효과와 스케일 복원 효과가 혼재한다. 해상도 한계: (a)·(c)는
  과거 동결 draw, (b)는 신규 draw — arm 간 비교는 draw 잡음을 포함하며
  (케이스당 5-draw 밴드 12–18pp ≈ ±10pp, E5 §7 실측), ±6pp median은 그 해상도
  내의 방향 판독이다. 양쪽 모두 사전 등록 10pp 바 미달 → 사전 등록 판독
  **(ii): 이 세트에서 암기의 점수 기여가 작다는 방향 증거 (a≈b≈c; N=9 방향
  증거 — 인과 확정 아님)**. `analysis/identity_3arm_results.json` · 한계 L-7.

**③ 컷오프-후 홀드아웃 (암기 구조적 불가, HUBG·WMK·GNE) → H2 (per-case, N=3).**
recognition gate 3/3 비인지(폭로 미암기 실증, draw-1). **게이트 k=5 승격
(2026-07-10, 규칙 사전 커밋): HUBG·WMK·GNE 각각 knows_event 0/5 — 사전 규칙
(≤1/5)상 홀드아웃 자격은 draw 잡음에 강건, 양성대조 HTZ 재검 True.**
세 회사 라벨은 전건 G2 잠정 — 그리고 **전건 Big R**(Item 4.02 비신뢰 선언 동반,
기계 검증 `analysis/label_tags_holdout.json`), 확정 집행 아님.
신호는 **약화하나 붕괴하지 않는다**:
- per-case: **HUBG p=70(플래그)** · GNE 42 · WMK 32. **HUBG는 기계 스크린(Beneish
  M·Dechow F)이 결측으로 계산조차 못 한 곳에서 탐지** → LLM 신호는 M/F 복제가 아니다.
- 단 정직 단서(오류해부 P1): HUBG의 적중은 **tier 적중 / 기제 빗나감**(dim2=1 — 과거
  2018 정정 클러스터에 정박, 2026 사건 기제 미상). 리스크 스크리닝 ≠ forensic 기제 탐지.
- **E1 매칭 대조군 (2026-07-09 감독 실행)**: HUBG 70은 **매칭 대조군 전부를 상회**
  (RXO 42·BCO 30·XPO 20) — 단 WMK·GNE는 각자 대조군과 분리 미검출 (3케이스 중 1건만
  대조 우위, `analysis/holdout_controls_results.json`). 정확 순열 p=0.20은 CONTEXT ONLY.
  **홀드아웃 tier 전체의 단일 최고점은 대조군 오탐이다 (GridAI, GRDX, 78)** —
  HUBG(70)는 자기 매칭 대조군은 상회하나 풀링된 대조군 집합은 상회하지 못한다.
- **k=5 재추첨 (E5§7)**: HUBG 플래그는 **5/5 draw에서 p≥50** [58–76] — 사전 규칙(≥4/5)상
  draw 잡음에 강건. WMK [28–42]·GNE [30–42]는 0/5 (뒤집힘 없음). 발행 수치는 draw-1.
- **H1(순열 유의성)은 N=3 과소검정이라 미주장.**

**암기-소멸 백본 (핵심)**: 각 wave의 **standalone 순열 유의성이 암기 지표(name-ID
50% → 21.9% → 0%)의 반감·소멸에도 독립 생존한다** — wave-1 p=**0.00114**(교란 프레임
0.0021 우선 판독) · wave-2 p=**0.00116** · 홀드아웃은 recognition gate 3/3 비인지에서
HUBG 탐지가 매칭 대조군을 상회하고 5-draw robust. ⇒ **분리는 암기로 설명되지 않는다**.
**2차 gradient 관찰 (이제 2축)**: name-ID 축은 50%→21.9%→0%로 반감·소멸하는 동안
AUC 0.824 [0.599, 0.983] → 0.829 [0.616, 0.983] — 점추정은 나란하나 **CI 폭이
동등성 주장을 금지한다** (N=30·32 부트스트랩; "사실상 불변"은 관찰이지 결론이
아니다). **직접 계기(outcome-knowledge, 홀드아웃 게이트와 동일; wave-1 미측정)로
정렬한 축은 wave-2 88.9% → 홀드아웃 0% — 암기 제거는 wave-2→홀드아웃 사이에서
일어난다.** 세 표본은 시대·유명도·라벨 tier가 달라 **통제 실험이 아니라
gradient 판독**이다 (`analysis/synthesis.md` §1 2축 표,
`fig_memorization_doseresponse.png`).

## 거짓양성 — 환각이 아니라 과잉해석 (정직 기록)

- wave-1 FPR **3/22 = 13.6%** Clopper–Pearson 95% **[2.9%, 34.9%]** · wave-2 FPR
  **5/23 = 21.7%** CP **[7.5%, 43.7%]** · 홀드아웃 대조군(E1) FPR **2/9 = 22.2%**
  CP **[2.8%, 60.0%]**. **"0%"로 보고하지 않는다.** 점추정은 악화 방향이나 CP
  구간이 크게 겹쳐 **입증되지 않는다**(worse-but-not-provably).
- wave-2 오탐 5건은 **전건 채점자 검증상 근거됨(dim4 상단) — 수치 날조(환각)가 아니라
  실재 수치의 양성 오독**(정상 구조/비율 발산을 위험으로 승격). 신뢰 경계는 환각이
  아니라 base-rate/보정 축이다 (`analysis/error_analysis_wave2_holdout.md`).
- 보정: wave-2 ECE **0.179** (wave-1 0.209와 동일 차수 — 개선 없음, null-ish).

## 기계 기준선 대조 (R2 비발동)

동일 30사·동일 PIT: Beneish M p=0.498/AUC 0.510 · Dechow F p=0.268/AUC 0.573 — 정량
스크린은 이 표본에서 무분리. LLM 순위는 둘과 사실상 무상관(wave-1 ρ −0.075/−0.144;
wave-2 0.337/0.265), 잔차 분리가 살아남는다 → 사전 커밋 R2 **비발동**. LLM은 기계
공식의 재현이 아니다.

## 채점·확정 상태

- 채점: **Claude 보조 + 인간 최종 확정.** 피평가자 **claude-sonnet-5**(핀, 호출별 서빙
  모델 검증, 핀 불일치 0). 채점자 claude-fable-5.
- wave-1 채점 26건 `human_finalized=true`(동결). **wave-2 32 + 홀드아웃 3 + wave-1
  대조군 22 채점도 `human_finalized=true`** (2026-07-09 소유자 확정, D24 · 오버라이드
  0건 — §9 고무도장 점검 포함) — 워크벤치 `review_packets/RP-13_grading_workbench.md`.

## 확장 실험 E1–E5 (사전 등록 완료 — freeze-then-run)

전 실험은 채점 전 사전 등록·커밋되었다(`analysis/*_PLAN.md`, 커밋 `c1b85a7`):
- **E1** 홀드아웃 매칭 대조군 — **실행 완료 (2026-07-09 감독, D26)**: 9사 중 HUBG
  매칭군만 분리, FPR 2/9 (H1 N=3 미주장 유지).
- **E2** 조기성 (분기별 탐지 선행시간, 제출-정렬 스냅샷).
- **E3** wave-2 교란 재추첨 (R4 draw-잡음 방어 — **median-dominance ≥5/9면 R3가 R4를
  supersede**, 규칙이 결정).
- **E4** 교차모델 (**EXPLORATORY** — claude-opus-4-8, 한계 각주 전용).
- **E5** wave-2 본채점 재추첨 (안정성 밴드, draw-1 published 불변) — **§7 홀드아웃
  arm 실행 완료 (2026-07-09, D27)**: HUBG 5/5 robust; wave-2 arm은 최저 우선순위 유지.

실행 상태·미터링 spend 게이트: `docs/OWNER_QUEUE.md`(Q-E01) · `docs/RESUME.md`.
**발행 완료 (2026-07-11, D40/D41)** — 상단 '발행' 절의 이슈 3건 + v1.0.0.
E2/E4(**EXPLORATORY**)/E5 발사는 launch-ready 동결 유지 (Q-E01 RESOLVED (A)).

## 거버넌스 지도 (읽는 순서)

1. `PROJECT.md` — 단일 기준 문서 (방법론 §5, 협업 모델 §7, 스코프 가드 §8)
2. `CLAUDE.md` — 세션 가드레일 · `scoring/decisions_log.md` — 결정 대장 + freeze 해시
3. `scoring/overrides.md` — 오버라이드·서명·게이트 (OWNER-GATE-E 포함)
4. `review_packets/INDEX.md` · `RP-11_expansion_holdout.md` · `RP-10_final.md` — 감사 진입점
5. 발행 이슈 동결 원문: `analysis/ISSUE_0_DRAFT.md`(wave-1) · `ISSUE_1_WAVE2_DRAFT.md`(R4) ·
   `ISSUE_2_HOLDOUT_DRAFT.md`(H2) — 소유자 서명 후 2026-07-11 게시 (D40/D41,
   URL은 상단 '발행' 절).

## 수치 재현 (제3자 검증)

```bash
pip install -r requirements.txt
python tools/reproduce_analysis.py   # 발행 수치 전건 재계산 → PASS/FAIL (100/100)
python tools/verify_blindness.py     # 채점 선행 이력 증명 · 실명/카나리 스캔 · runs/ sha256
python tools/verify_manifest.py      # 데이터 매니페스트 대조 (429 파일)
python analysis/synthesis.py         # 교차-웨이브 종합 (결정론, seed 20260708)
```

셋 다 커밋 산출물만 사용한다 (API 호출 0, 원문 코퍼스 불요) — CI가 매 push 검증한다.
원시: `runs/`(sha256 매니페스트) · `scoring/grades*/` · `scoring/probe_results*/` ·
`logs/run_*/`(호출별 서빙 모델·격리 플래그·freeze 해시).

## 한계 (전문: docs/methodology_limitations.md)

L-1 모델 내부 지식은 차단 불가 — 측정·공개만. L-2 실행층은 Claude Code 하네스 매개.
L-3 샘플링 파라미터 고정 불능 — 케이스 판정은 비결정론 표본의 점추정. L-4 격리는 실행별
게이트 검증. **L-5 교란은 수치 암기를 흩뜨릴 뿐 정체 인지를 제거하지 못한다**
("perturbation disrupts memorized NUMBERS, not IDENTITY recognition") — 이름 지목률이
그 증거이며, 모든 양성 결과는 잔여 오염 하의 값이다. **L-6** 채점자(claude-fable-5)와
피평가자(claude-sonnet-5)는 동일 Claude 계열 — 동일 계열 관대화는 배제 불가, 인간 전수
확정(§7)과 E4(EXPLORATORY)로만 완화. **L-7** 정체 3-arm 실험의 c−b 대비는 설계상
혼입(정체 효과 + 스케일 복원 효과) — 깨끗한 대비는 b−a뿐이며, arm 간 delta는 draw
잡음(케이스당 ≈±10pp 밴드)을 포함한다. 선택·생존 편향: 실험군은 "적발까지
간 사건"의 생존 표본, 대조군 라벨은 "무결"이 아니라 "비집행"(Dyck-Morse-Zingales: 대형사
~10% 연간 증권사기, ~⅓만 적발 — 특이도 하향 편향, 거짓양성 결과는 그만큼 보수적).

## 이것이 아닌 것

존재 증명 시도이지 성능 추정치가 아니다(정밀도/재현율 % 헤드라인 의도적 부재 — 신뢰구간
넓음, 실회사 벤치마크 비교 불가, R4 프레이밍 제약). 단일 분석자(+AI) 산출물, 외부 재현·
감사 전. 피평가자는 하네스 매개 호출이라 원시 API 재현과 다를 수 있다. 케이스 판정은
비결정론 표본. pooled wave1+wave2 수치(p=3.0e-05 등)는 **2차 병기 전용** — standalone
wave별 결론이 헤드라인이다. 특정 기업에 대한 주장이 아니며 — 현재/G2 기업 산출물에
"분식/fraud/조작" 서술을 쓰지 않는다(§6) — 투자 조언은 더더욱 아니다.
