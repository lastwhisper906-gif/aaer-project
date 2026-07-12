# ENGINE_DECISION.md — 도구 경로 엔진 판정 사전 등록 (roadmap 1.6, D51)

> **E2(조기성) 실행 전 커밋 — freeze-commit-then-run.** 판정은 E2 산출물로부터
> `analysis/engine_verdict.py`(본 스펙 후행 커밋, 픽스처 테스트)가 **기계적으로**
> 계산한다. 사후 재해석의 여지 0 — 스펙의 규칙이 전부이고, 규칙 밖 서사는
> 판정에 영향을 주지 못한다. 범위 한정(§5-5): Claude 기반 단일 파이프라인.

## 0. 결정 대상

운영 리포(`screener`)의 2단계 퍼널에서 **stage-2(미터링 LLM 딥분석)가 존재할
자격**이 있는가. 근거는 E2 조기성 실측 — "LLM이 결정론 규칙(B3)보다 몇 분기
먼저 신호를 켜는가."

## 1. 입력 (E2 산출물 → trajectories 어댑터)

- E2 동결 계획(`analysis/EARLINESS_PLAN.md`)의 출력 그대로: 케이스별 스냅샷
  궤적 (`case_NN_s{j}`, 케이스당 ≤8 스냅샷, 실험군 = detected fraud,
  대조군 = RP-01 8). **E2 스펙은 무변경** — 본 스펙은 소비자다.
- E2 완료 후 어댑터가 조립하는 `analysis/e2_trajectories.json` 스키마
  (buyer-metrics 빌더와 공유):

```json
{
  "flag_threshold_llm": 50,
  "flag_threshold_b3": 2,
  "cases": [
    {"case_id": "case_NN", "ticker": "XXX", "group": "treatment",
     "snapshots": [
       {"j": 0, "cutoff": "YYYY-MM-DD", "quarters_to_revelation": 1,
        "llm_p": 72, "b3_score": 1}
     ]}
  ]
}
```

- `llm_p` = 해당 스냅샷 미터링 점수 (j=0은 동결 본실행 점수 재사용 — E2 §2).
- `b3_score` = 동결 `b3_compute.b3_score(ticker, snapshot_cutoff, 730)` —
  스냅샷별 재계산 (결정론, 무비용).

## 2. 사전 고정 임계

- **LLM 플래그: p ≥ 50** (동결 FLAG=50, ANALYSIS_PLAN §1 — 재사용, 신규 아님).
- **B3 플래그: score ≥ 2** (신규 사전 등록 — 단일 지표는 NT 1건/정정 1건으로도
  점화되어 이벤트로서 과민; 2 = 연대기 이벤트 동시 발생. 민감도 보고: ≥1, ≥3
  리드타임을 괄호 열로 병기하되 **분기 판정에는 무가중**).

## 3. 리드타임 정의 (기계적)

- 케이스별: `lead = max{ quarters_to_revelation(s) : score(s) ≥ 임계 }`
  (가장 이른 임계 돌파 스냅샷의 t). 돌파 스냅샷 없음 → `lead = 0`.
- 집계: **실험군 케이스별 lead의 중위값** (LLM/B3 각각).
- AUC: **스냅샷 j=0 점수**로 실험군 vs 대조군 tie-aware AUC (동결
  `analysis/stats.py::auc` 의미론) — LLM/B3 각각. j=0 = 운영 스크리닝이 서는
  위치(최신 컷오프).

## 4. 판정 규칙 (순서 고정 · 전역 완전 — 이 순서대로 첫 일치가 판정)

| 순서 | 조건 | 판정 |
|---|---|---|
| 1 | `median_lead_llm ≤ 1` **AND** `median_lead_b3 ≤ 1` | **(c) 도구 경로 종료** — 어느 쪽도 폭로 직전 분기를 넘는 선행 신호 없음. screener 리포 아카이브, aaer-evals는 과학 산출물로 존속. stage-2 없음. |
| 2 | `median_lead_llm ≥ median_lead_b3 + 1` | **(a) LLM 엔진** — stage-2 활성 (top ~300 딥분석). LLM이 규칙 대비 온전한 1분기 이상의 리드로 미터링 비용을 정당화. |
| 3 | 그 외 전부 | **(b) 규칙 엔진** — stage-2 제거, LLM은 리포트 초안 보조로 강등. |

- 브랜치 3에는 두 하위 상황이 있고 verdict JSON에 구분 기록한다 (판정 무영향,
  서사 정직성용): `b_strict` = B3가 리드타임·AUC 모두 ≥ LLM (미션 문면의 (b)) ·
  `b_residual` = LLM 우위가 있으나 1분기 미만 (stage-2는 온전한 1분기 리드를
  벌어야 존재 — 미달 시 무료 규칙이 이긴다는 보수 기본값).
- 동률·경계는 위 부등호가 전부 결정한다 (≤, ≥ 문면 그대로). 중간 판정 없음.

## 5. 실행·기록 규약

- 판정 스크립트: `analysis/engine_verdict.py` — 입력 `e2_trajectories.json`,
  출력 `analysis/engine_verdict.json` (판정 + 전 중간값 + 케이스별 lead 표).
  픽스처 테스트가 세 브랜치 전부를 커버한다.
- E2 완료 → 어댑터로 trajectories 조립 → verdict 실행 → 결과 커밋 → 신규
  D-엔트리로 판정 기록. **판정 후 screener 측 이행(FUNNEL.md §2)은 판정
  JSON을 인용**하며, 사람의 재량 판단이 낄 자리는 브랜치 3의 하위 구분
  서사뿐이다 (판정 자체는 불변).
- 본 판정의 개정은 E2 실행 전에만 가능 (freeze-commit-then-run — 실행 후
  변경은 이력 공개 의무, PROJECT.md §5-6).

## 6. 정직 조항

- (c)가 나오면 그대로 발행한다 — "도구가 안 된다"는 결과도 trust boundary
  데이터다 (PROJECT.md §10). (b)에서 LLM 강등도 동일.
- N(실험군 detected ~7–8)이 작아 중위 리드타임의 신뢰구간은 넓다 — verdict
  JSON에 케이스별 lead 전수 표를 동반해 독자가 재계산 가능하게 한다 (§2-4
  검증가능성).

## §4b B4 결합 조항 이행 (개정 1 — D58, 2026-07-13, E2 실행 전)

> specs/B4_short_interest.md §7(D55, 완화 금지 조항)이 등록한 결합을 본 판정
> 규칙에 기계적으로 이행한다. **E2 실행 전 개정** — §5 개정 조건 충족.
> 판정 코드(engine_verdict.py §4b 지원)는 이 개정 커밋에 후행한다.

- **입력 확장**: trajectories 스냅샷에 선택적 `b4_slope_aug` (float|None) —
  동결 `b4_score(ticker, snapshot_cutoff)`의 `score_slope_aug` (결정론, 무비용).
  부재/전건 None 허용 (커버리지 판정으로 귀결).
- **B4 플래그 임계 (기존 사전 등록 재사용, 신설 아님)**: `b4_slope_aug > 0` —
  screener FUNNEL §1 rank key·프로토콜 §2와 동일 임계.
- **비교 성립 조건 (B4 스펙 §7 문면 그대로)**: (i) 실험군 B4 커버리지 ≥ 70%
  (케이스가 커버 = ≥1 스냅샷에서 b4_slope_aug 비-None) AND (ii) 동일 산식의
  LLM 성능이 같은 데이터에 존재 (E2 궤적 자체가 이를 공급).
- **결합 규칙 (순서: §4 기본 판정 후 적용, 전역 완전)**:
  - 비교 불성립 → 기본 판정 그대로, verdict JSON에 `b4_comparison.valid=false`
    + 사유 기록.
  - 비교 성립 AND `median_lead_llm ≤ median_lead_b4` AND `auc_llm ≤ auc_b4`
    (둘 다, 경계 포함 — "성능 ≤"의 기계 번역) → **LLM ≤ B4 = E2 평결과 동일
    가중치**: 기본 판정이 (a)였다면 **(b) 규칙 엔진으로 강등**
    (`b_subcase="b4_dominated"`), (b)/(c)는 불변 (이미 stage-2 없음).
  - 비교 성립 AND LLM이 어느 한 축에서라도 우위 → 기본 판정 그대로,
    비교 전량 기록.
- **정직 조항**: B4 리드타임·AUC는 커버 케이스 부분집합에서 계산 — LLM 값도
  **같은 부분집합으로 재계산해 짝지어 비교**한다 (커버리지 편향 차단). 전체
  실험군 LLM 값과의 차이는 verdict JSON에 병기.
