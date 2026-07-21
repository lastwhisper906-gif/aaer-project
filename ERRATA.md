# ERRATA — 게시 산출물 정오표 (append-only)

> 원칙: 동결·게시 산출물은 수정하지 않는다. 정정은 이 파일의 항목 추가 +
> 신규 코드 경로/신규 산출물 경로로만 이루어진다 (2d78faf de-identification
> disclosure 전례와 동일한 방식). 이 파일은 append-only — 기존 항목을
> 고치지 않고 후속 항목으로 갱신한다.

---

## E-001 (2026-07-21) — Wave-2 분석 코드가 사전 등록 계획과 불일치 (F1, V1/V2/V11)

**출처**: 외부 리뷰 (main @ db8b85f, 2026-07-20) 지적 F1 →
`audit/REVIEW_VERIFICATION.md` V1·V2·V11 (전부 CONFIRMED, file:line 증거).

**사실 (무엇이 달랐나)**:

1. **R2 판정 구현 이탈** — `analysis/ANALYSIS_PLAN_WAVE2.md` §4는 R2를
   "Spearman ρ ≥ 0.7 (부호 있는) **이고** 잔차 증분 검정 p ≥ 0.05"로 사전
   고정했으나, `analysis/wave2_analyze.py:101`은 `abs(rho) >= 0.7` 단독으로
   판정했다. 잔차 회귀·잔차 순열 검정은 wave-2 코드에 존재하지 않는다.
   (wave-1의 `analysis/stats.py:202`는 계획대로 구현되어 있음 — 이탈은
   wave-2 재구현 과정에서 발생.)
2. **사전 등록 통계 누락** — 계획 §2의 Fisher exact(단측), §3의
   Clopper–Pearson 구간(FP≥1 시), §1의 INCOMPLETE 최악 대체 감도가
   `wave2_analyze.py` 산출물(`wave2_results.json`)에 없다. 플래그 계수와
   원시 FPR%만 저장되었다.
3. **"verbatim" 서술 부정확** — `analysis/ISSUE_1_WAVE2_DRAFT.md:63`의
   "conclusion rules R1–R4 **verbatim**" 및 같은 문서 §5·
   `analysis/wave2_summary.md:5`의 "`python analysis/wave2_analyze.py`로
   재현" 주장은 v1 wave-2 릴리스 시점 기준 부정확했다. 특히 §5가 인용한
   "FPR 21.7% CP [7.5%, 43.7%]"는 해당 명령이 산출하지 않는 수치다.

**결론 수치에 대한 영향 (현재 확인 범위)**: 관측 ρ(LLM,M)=0.337,
ρ(LLM,F)=0.265는 모두 양수이며 0.7에서 멀어, abs→signed 정정만으로는 R2
판정이 뒤집히지 않는다. 정식 비교는 rev2 재실행(아래) 완료 후 본 파일에
후속 항목으로 기록한다.

**조치**:

- v1 산출물(`analysis/wave2_results.json`, `analysis/wave2_summary.md`,
  `analysis/ISSUE_1_WAVE2_DRAFT.md`)은 **동결 유지, 무수정**. 원 구현은
  `analysis/legacy/wave2_analyze_v1.py`로 보존한다 (Task 2).
- 교정 분석은 단일 판정 모듈(`aaer_eval/verdict.py`) + 단일 통계
  모듈(`aaer_eval/statistics.py`) 경유로 재실행하여 **wave-2 rev2**
  신규 경로(`analysis/out/wave2_rev2/`)에 병행 게시한다 — v1 대체가 아님.
- rev2 vs v1 판정 비교는 실행 후 본 파일 후속 항목(E-002 예정)에 기록.
  판정이 바뀌면 소유자 검토 전 어떤 의존 작업도 커밋하지 않는다
  (REMEDIATION_HARNESS_PROMPT QUARANTINE rule 1).

**공개 문구**: 본 항목이 곧 공개(disclosure) 절이다. 향후 wave-2를 인용하는
모든 외부 표면은 "v1 분석 코드는 사전 등록 계획과 3개 지점에서 불일치했고
(R2 판정식·누락 통계·재현 주장), rev2에서 교정·병행 게시되었다"를 링크해야
한다.

---

## E-002 (2026-07-21) — Wave-2 rev2 vs v1 비교 (Task 5 완결, 소유자 승인 D1)

**비교 기준**: v1 = 동결 `analysis/wave2_results.json` (게시). rev2 =
`analysis/out/wave2_rev2/wave2_results_rev2.json`
(재현: `PYTHONPATH=. python analysis/wave2_analyze.py`, seed 20260707).

**판정 불변**: 발동 규칙 **R4 = R4** (v1 = rev2). 1차 통계 완전 일치 —
순열 p 0.00116, 평균차 +20.57pp, Cliff δ 0.657, AUC 0.829 [0.616, 0.983],
R3 산입 3/9(비발동), 교란 2차 프레임 p 0.00427 / AUC 0.790, pooled 2차
p 3.0e-05 / AUC 0.831, 플래그 7/9 vs 5/23.

**변경된 게시 통계 (tie-aware Spearman 보정, V8)** — 두 값 모두 명시:

- **ρ(LLM, Beneish M): 0.337 → 0.333** (하향, n=20 동일)
- **ρ(LLM, Dechow F): 0.265 → 0.293** (**상향** — 보정이 유리한 방향으로만
  움직인 것이 아님을 명시, n=17 동일)

원인: v1 wave-2 구현의 Spearman이 동순위(tie)를 평균하지 않는 자체 랭킹을
사용(REVIEW_VERIFICATION V8). 두 값 모두 R2 임계 0.7에서 멀어 판정 무영향.

**신규 산출 (사전 등록이었으나 v1 미산출, V2)**: Fisher exact(단측)
p = 0.00573; FPR Clopper–Pearson 95% [7.5%, 43.7%]; INCOMPLETE 최악 대체
감도 n_incomplete=0 (1차 p 불변); R2 잔차 순열 p — M 0.0035, F 0.0023
(둘 다 < 0.05: 기준선 회귀 후에도 잔차 분리가 유의 — "기계 신호 복제"
반증 방향).

**게시 CP 구간의 출처에 관한 명시적 확인**: 게시 문서
(`analysis/ISSUE_1_WAVE2_DRAFT.md` §5)가 인용한 "FPR 21.7% CP
[7.5%, 43.7%]"는 **게시가 주장한 재현 명령(`python
analysis/wave2_analyze.py`)이 산출하지 않는 수치였다** — 그 코드에는 CP
계산이 존재하지 않았고, 수치의 출처는 재현 경로 밖이었다. rev2가 같은
구간 [7.5, 43.7]을 코드로 재산출함으로써 값 자체는 정확했음이 확인되나,
"재현 가능" 주장은 v1 시점에 부정확했다 (E-001 3항의 구체화).

**차기 계획 개정 플래그 (지금 변경 아님)**: R3 산입 규칙에서 교란 draw가
없는 실험군 케이스는 산입 분자에서 제외되면서 분모(n_treatment)에는
포함된다 — v1과 rev2 동일 동작이며 ANALYSIS_PLAN_WAVE2는 이 경우를
규정하지 않는다. 차기 계획 개정 시 명시적으로 규정할 것 (사전 고정 원칙에
따라 소급 변경 금지).

**지위**: 본 항목으로 rev2는 인용 가능(citable). v1 산출물은 동결 유지.
