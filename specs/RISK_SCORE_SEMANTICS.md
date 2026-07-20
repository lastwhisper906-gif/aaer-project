# specs/RISK_SCORE_SEMANTICS.md — 전향(prospective) 서수 위험 점수 의미론

> 2026-07-20, owner plan §2 위임 (ledger D100). 적용 범위: **전향 전용** —
> forward watchlist(첫 seal 2026-11-15)·미래 스키마·미래 프롬프트·미래 결과
> 문서. v1 동결 산출물·`schemas/llm_output.json`의 `misstatement_probability`
> 필드명은 무접촉 (재현성 — `specs/calibration_scope.md` 범위 선언과 동일).
> 본 스펙은 calibration_scope §4-1의 Cycle-2 개명 등록을 구체화·발효한다:
> 등록명 `misstatement_score` → 확정명 `misstatement_risk_score`
> (owner plan §2.2가 명명을 직접 지정).

## 1. 필드 정의 (forward 스키마 규범)

| 필드 | 타입 | 의미 |
|---|---|---|
| `misstatement_risk_score` | integer 0–100 | **서수(ordinal)** 위험 점수. 순위·검토 우선순위 부여 전용. 보정된 확률로 해석 금지. |
| `evidence_sufficiency` | `sufficient` \| `partial` \| `insufficient` | 입력 데이터가 체크리스트 평가에 충분했는가 (데이터 축). |
| `assessment_confidence` | `high` \| `medium` \| `low` | 모델의 자기 평가 확신도 (판단 축 — 데이터 축과 분리). |
| `decision_state` | `flag` \| `review` \| `no_flag` \| `abstain` | 프로토콜 임계 규칙이 산출하는 결정 상태. `abstain`은 `evidence_sufficiency=insufficient` 등 사전 등록 조건에서만. |

## 2. 해석 규약 (의무 문구)

> A score of 70 means stronger model-assessed risk than a score of 40 under
> the same frozen protocol. It does not mean a 70% probability of
> misstatement.

- 점수 70 = 동일 동결 프로토콜 하에서 점수 40보다 강한 모델 평가 위험.
  **70% 확률이 아니다.**
- 근거: `specs/calibration_scope.md` §1 — 순위·플래그 기능은 검증(분리
  p=0.00114/0.00116, AUC 0.82/0.83), 확률 기능은 부정(ECE 0.209/0.179,
  개선 없음). 재보정은 N ≥ 150 전 금지 (§4-2 사전 고정 하한).
- 임계값은 "보정된 확률 컷"이 아니라 **사전 등록된 서수 컷**으로만 서술한다.
  보정 연구 없이 "calibrated" 서술 금지.
- 발행 표면에서 케이스 점수를 `p=NN` 형태로 쓰지 않는다 (RP-16/D91 규약
  — `score NN`). 통계 p-값(소수 형식)은 해당 없음.

## 3. v1 이력 처리

`misstatement_probability`(0–100 정수)는 **이름만 역사적**이다: v1 커밋
산출물의 재현성 때문에 필드명을 유지하되, 값은 처음부터 서수로만 검증·해석
되었다 (calibration_scope §1, RP-16 발행 표면 정리). 새 이름으로의 소급
개명은 하지 않는다.

## 4. 기계 강제

`tools/lint_publication.py` 규칙 (J): 발행 표면(README 양어·ONE_PAGER·
forward 사이클 문서)에서 ① 정수형 `p=NN` 케이스 점수 인용 ② "NN% 확률/
probability/likelihood" 형태의 서수 점수 확률화 서술을 기계 차단.
동결 ISSUE 초안 3종은 게시된 역사 텍스트이므로 규칙 적용에서 제외
(수정은 소유자 서명 diff로만 — RP-15/16 선례).

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
