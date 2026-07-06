# Eval Spec — v1.1 (Phase 2-1)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> v1 → 별도 컨텍스트 self-red-team (발견 12건, 부록 A) → **v1.1 반영 완료 (2026-07-06)**.
> freeze 커밋으로 고정. 본 결과는 Claude 기반 단일 파이프라인에 한정 (§5-5).
> 채점: Claude 보조 + 인간 최종 확정.

## 1. 피평가자 과제 (정확한 문언 — 중립화 적용)

파이프라인이 피평가자 모델에 주는 과제 문언 (케이스별 독립 호출, GP-6 3조항):

> You are analyzing the financial reporting quality of {company_name} ({ticker},
> CIK {cik}) using only the structured data provided below, which reflects public
> filings available on or before {cutoff_date}. Do not use any knowledge of events
> after {cutoff_date}. Complete the checklist, then: (a) estimate the probability
> (0–100) that the company's financial statements **contain, or have contained
> during the periods covered by the available filings**, a material misstatement;
> (b) if you estimate this probability at 40 or above, describe the most likely
> mechanism(s), most confident first (at most 3): which financial statement line
> items are affected, in which direction, and through what accounting treatment.
> Every finding must cite the specific data points provided, in the form
> 'concept=value (period)'. If the data is insufficient for an item, say so —
> do not guess.

- 문언 개정 (red-team #3): "contain, or have contained during the periods covered"
  — 컷오프 전 정정 완료 케이스에서 감지가 0점 되는 경로 차단.
- **중립화 (D4)**: 장르 분류 체계(적극/누락), "fraud"·"manipulation"·사기 문헌 용어,
  그룹 구조 언급 금지. 출력 필드명도 `misstatement_probability` (red-team #1).
- 컷오프의 유래(폭로일)는 알리지 않는다.

## 2. 입력 범위

| 구성 | 내용 | 근거 |
|---|---|---|
| 케이스 필드 | `evaluatee_input` v1.1의 5필드만 | GP-6 페이로드 규약 |
| 구조화 재무 시계열 | point-in-time XBRL 연차·분기 개념표 (Python 결정론 추출, `filed <= cutoff`), 각 값에 provenance(accession) | §5-4 수치=Python |
| 제출물 연대기 | 컷오프 전 EDGAR 제출 인덱스 (form type, filing date — NT·8-K·/A 포함) | T2 메타신호 채널 |
| **불포함** | 서사·각주 텍스트 (D10), 베이스라인 스크린 출력(누출 금지), candidates.json·채점 문서 일체 | D10, 1-1 |

호출 형태: 케이스당 독립 API 호출, 교차 컨텍스트 없음 (GP-9 ①의 성립 조건).
입력이 구조화 데이터뿐이므로 evidence의 quote/location은 **제공 데이터 포인트 참조**
('concept=value (period)')로 정의 — 문장 인용 형식은 날조로 채점 (red-team #6).

## 3. 출력 계약 (llm_output v1.2 — 반영 완료)

`schemas/llm_output.json` v1.2 (2026-07-06 개정 착륙):
- `misstatement_probability`: integer 0–100, 필수.
- `mechanism_hypotheses`: array **maxItems 3**, 배열 순서 = 확신 순위. p≥40이면
  minItems 1 (스키마 if/then으로 기계 강제 — red-team #2/#5/#10).
- evidence 필드 의미 재정의 (#6). risk_tier ↔ p 정합 규칙 스키마 명기 (#12).

## 4. 채점 루브릭 — 4차원 분리 채점 (D4)

채점자(D6: grader 모델 + 인간 감사)는 정답 키(candidates.json, genre_tags.md,
명령문 원문)와 피평가자 출력을 받고 차원별 독립 점수를 매긴다. 피평가자는
채점자 자료를 절대 받지 않는다.

### 차원 1 — misstatement 확률 (보정)
- 케이스 점수 (겹침 없는 밴드 — red-team #4):
  실험군 p≥70 → 2 / 50≤p<70 → 1 / p<50 → 0.
  대조군 p≤30 → 2 / 30<p<50 → 1 / p≥50 → 0.
- 집계 병기 (전부 결정론 Python): ① 16케이스 Brier (실험군=1, 대조군=0) ②
  상수 p=50 기준선 Brier(0.25) 대비 ③ 판별 통계: 실험군/대조군 p의 rank-sum
  기반 AUC. **퇴화 분포**(16케이스 p 표준편차 < 5pp)는 §5 실패 기준 (b) 발동.
- 주의: 대조군 라벨 0은 "비집행"이지 "무결"이 아님 (GP-8 '조용한 미적발' 한계 명기).

### 차원 2 — 기제 식별 (실험군 전용, 0–3, **최상위 가설 기준**)
- 0: 가설 없음(p≥40인데 부재 = 0 — #10) 또는 명령문과 무관한 계정.
- 1: 최상위 가설의 영향 계정 영역이 명령문 서술과 일치.
- 2: 계정 + 방향 + 회계 처리 유형이 실질 일치.
- 3: 2에 더해 **genre_tags.md에 pinpoint된 케이스 특이 사실 ≥1개를 실질 지목**
  (예: 유통사 계약 조건, 리베이트 시점 — #7 경계 확정).
- 다중 기제 정답 케이스: 최상위 가설이 정답 기제 중 **어느 하나**와 최적 일치하는
  것으로 채점하고, 정답 기제 수·커버된 수를 케이스 노트에 기록 (#7).
- 대조군: N/A. 대조군에서의 기제 주장은 차원 2가 아니라 **차원 4에서 채점**된다 —
  주장을 지지하지 못하는 evidence는 그 자체로 감점 (#9 정정: v1의 "차원 1에서
  이미 감점" 문장은 오류였음 — 삭제).

### 차원 3 — 장르 분류 (실험군 전용, **최상위 가설 매핑 — #8**)
채점자가 최상위 가설 서술을 active / omission-estimate / mixed로 매핑 후
`scoring/genre_tags.md`와 대조. 진실×매핑 3×3 행렬 (사전 고정):

| 진실 \ 매핑 | active | omission-est. | mixed |
|---|---|---|---|
| active | 2 | 0 | 1 |
| omission-est. | 0 | 2 | 1 |
| mixed | 1 | 1 | 2 |

- 피평가자에게 분류 체계는 미노출 — 서술의 실질을 평가. 매핑 판정은 §7 대상
  (grader 1차 + 근거 + 인간 감사).

### 차원 4 — 인용 근거 품질 (전 케이스, 0–3)
- 0: 인용이 제공 데이터에 없는 값(날조) 또는 논거와 무관.
- 1: 인용 존재하나 일반론적 (구체 개념·기간·값 미지시).
- 2: 구체 데이터 포인트가 논거를 실제 지지 (대조군의 기제 주장 포함 — 지지
  불능 주장이면 0~1로).
- 3: 2에 더해 다년 추세·복수 데이터 포인트의 정합적 결합.
- 감점 규칙: risk_tier↔p 정합 위반 시 차원 4 상한 1 (#12).
- `memorization_suspect`(L-1 기계 규칙 2단) 판정과 결합: 플래그 케이스는 집계
  두 벌 병기.

## 5. 성공 기준 / 실패 정의 (존재 증명 어법 — 3-6)

- **성공 기준**: "블라인드 구조화 데이터만으로 명령문이 서술한 기제 X를 식별한
  케이스가 존재한다"를 케이스 단위로 입증/반증 + 장르별 비대칭의 방향 관찰
  (사전 기준선: docs/baseline_screens.md §3).
- **실패 정의** (사전 고정 — #11):
  - (a) 스키마 불통과 또는 인용 날조(차원 4=0)가 16케이스 중 ≥4.
  - (b) 판별 부재: 실험군/대조군 `misstatement_probability`의 one-sided
    Mann-Whitney rank-sum p ≥ 0.20 **또는** 중위값 분리 < 10pp **또는** 퇴화
    분포(차원 1 정의). n=8+8의 저검정력은 해석에 명기.
  - (c) memorization_suspect 제외 집계에서 (a)(b) 발생.
- 헤드라인에 정밀도/재현율 % 금지. n=8 신뢰구간(≈±35pp) 명기. 모든 양성 결과는
  잔여 오염 하의 **상한**. D5 단일 실행 한계 문구 의무. 선택/생존 편향 문단 의무.

## 부록 A — self-red-team 결과 (2026-07-06 수신 — 전건 v1.1 반영 완료)

| # | 심각도 | 발견 (요지) | 반영 |
|---|---|---|---|
| 1 | HIGH | `fraud_probability` 필드명이 fraud 프레이밍 누출 | `misstatement_probability` 개명 (스키마 v1.2) |
| 2 | HIGH | v1.2 스키마 미착륙 + "개연 시 ≥1" 기계 강제 불능 | 스키마 착륙 + if/then p≥40 → minItems 1 |
| 3 | HIGH | "as filed to date" 문언이 컷오프 전 정정 케이스 미정의 | §1 "contain, or have contained during the periods covered" |
| 4 | HIGH | 차원 1 밴드 겹침 [40,60] — 상수 p 전략 | 밴드 재설계(50 경계) + AUC·기준선 Brier 병기 + 퇴화 분포 = 실패 (b) |
| 5 | HIGH | 가설 샷건 전략 | maxItems 3 + 순위 강제 + 최상위만 채점 |
| 6 | HIGH | 구조화 입력 vs 원문 인용 evidence 모순 (날조 유도) | evidence 의미 재정의 ('concept=value (period)') |
| 7 | MED | 차원 2 앵커 경계·다중 기제 규칙 부재 | 3점 = pinpoint 사실 ≥1 / 다중 기제 최적 일치 + 기록 |
| 8 | MED | 차원 3 매핑 불완전 | 3×3 행렬 고정 + 최상위 가설 매핑 |
| 9 | MED | "대조군 기제 주장은 차원 1 감점" 주장 오류 | 문장 삭제, 차원 4로 채점 경로 명시 |
| 10 | MED | 중간 p + 빈 가설로 차원 2 회피 | p≥40 필수(스키마) + 실험군 부재 시 차원 2=0 |
| 11 | MED | 실패 기준 (b) 검정 부재 | rank-sum p≥0.20 ∨ 중위 분리<10pp ∨ 퇴화 분포 |
| 12 | LOW | risk_tier 자유 헤지 채널 + 부록 A 상태 표기 | 정합 규칙(스키마) + 위반 시 차원 4 상한 1; 본 표가 반영 기록 |
