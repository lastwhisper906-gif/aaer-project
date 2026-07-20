# CONTROL_CRITERIA v3 — 미래 사이클 대조군 청정성 체크리스트 + 매칭 규격

> **Authored by Claude Code, pending human audit** (D15 규약).
> 2026-07-20. authority: **D106 §3 (CONTROL_STRATIFICATION_v2,
> `governance/FEEDBACK_RESPONSE_v1.md`, owner-signed 2026-07-20)** — D106
> §0/§8에 따라 본 문서는 신규 D-엔트리를 요구하지 않는다 (사전 등록 범위
> 내 companion 문서). 내용 출처: 소유자 위임 지시문 2026-07-20 (서면 위임
> 선례). **효력 조건 (D106 §3)**: 본 문서는 미래 사이클의 어떤 대조군
> 선정보다 먼저 커밋되어야 한다 (freeze-commit-then-run).
> **적용 범위: 미래 사이클 전용.** 기존 대조군 집합(wave-1 C01–C08 ·
> wave-2 RP-09 22사 · holdout hc_01–hc_09)과 그 발행 FPR은 무변경 —
> v1/v1.1/v2 문서가 그 집합들의 역사적 선정 기록으로 남는다 (§4는 공시
> 전용 회고 감사만 등재).

## 0. 원칙 (v2 §"과학적 역할" 승계)

대조군은 "사기만 빼고 실험군과 최대한 유사"해야 한다. v3는 그 "사기만
빼고"(청정성)를 **명시적 체크리스트 + 출처 인용**으로, "최대한 유사"
(매칭)를 **3축 + 문서화된 완화**로 기계화한다. 모든 판정은 PASS / FAIL /
MINOR / INCOMPLETE 4값이며, 판정마다 **출처 인용(URL·질의문·검색일)**이
필수다 — 인용 없는 판정은 판정이 아니다 (§7 서명 규칙의 대조군 판).

**청정성 창(cleanliness window) W의 정의 (전 기준 공통)**:
W = [매칭 회계기간 시작일, 대조군 관측창 종료일 + 24개월].
관측창 = 모델 입력으로 사용되는 공시들이 커버하는 기간. (a)–(b)는 행위
기간(conduct period) 기준 — W 이후에 공표된 조치라도 행위 기간이 W와
교차하면 해당 기준 FAIL이다.

## 1. 청정성 체크리스트 (후보별 전 기준 문서화 의무)

### (a) SEC 집행 조치 부재

- **판정**: W와 행위 기간이 교차하는 SEC 집행 조치(AAER 또는 회계 관련
  litigation release) 없음 → PASS. 있으면 FAIL (MINOR 없음).
- **출처·절차**: ① AAER 색인 — sec.gov "Accounting and Auditing
  Enforcement Releases" 연도별 목록 (`https://www.sec.gov/divisions/enforce/friactions.htm`)
  ② SEC Action Lookup (`https://www.sec.gov/litigations/sec-action-look-up`).
  질의어 = 현재 등록자명 + `https://data.sec.gov/submissions/CIK{10자리}.json`
  의 `formerNames` 전부. 질의어 목록·검색일을 판정에 기록한다.

### (b) 재작성(restatement) 부재

- **판정**: W 기간 재무제표의 재작성(Big R — 기발행 재무제표의 신뢰 철회
  수반) 없음 → PASS. 있으면 FAIL. 비신뢰 선언 없는 비교표시 수정
  (little-r revision)은 (b)를 FAIL시키지 않으나 **기록 의무** (판정 노트).
- **출처·절차**: ① submissions JSON의 form 목록에서 W+24개월 내
  `10-K/A`·`10-Q/A` 전수 → 각 수정 사유 설명(explanatory note) 확인
  ② EDGAR 전문 검색 (`https://efts.sec.gov/LATEST/search-index?q=%22restatement%22`,
  CIK·양식 10-K/A·10-Q/A·8-K 필터, W+24개월). 검색 질의 URL·검색일 기록.

### (c) Item 4.02 비신뢰 공시 부재

- **판정**: W+24개월 내 Item 4.02 8-K 없음 → PASS. 있으면 FAIL.
- **출처·절차**: submissions JSON의 8-K `items` 필드에 `"4.02"` 포함 여부
  — 결정론 기계 판정 (전문 검색 불요). accession 번호를 기록한다
  (부재 시 "8-K n건 전수, 4.02 없음, 검색일" 형식).

### (d) SOX 404 중대한 취약점(material weakness) 부재

- **판정**: W 기간 ICFR 평가에서 material weakness 공시 없음 → PASS.
  공시 있으나 **차기 연차 평가까지 치유(remediated) + 재작성 무연결**이면
  MINOR. 미치유 지속 또는 재작성 연결이면 FAIL.
- **출처·절차**: EDGAR 전문 검색 `%22material%20weakness%22`, 양식
  10-K·10-K/A·10-Q, 해당 CIK, W 커버 회계연도 — 히트 시 Item 9A 원문
  확인·인용. accession + 인용 문구 기록.

### (e) 감사인 사임·해임 8-K 부재

- **판정**: W+24개월 내 Item 4.01 8-K(감사인 변경) 없음 → PASS. 있으나
  Item 304 의견 불일치(disagreement)·보고 대상 사건(reportable event)
  **없음** 명시(통상 교체)면 MINOR. 불일치·보고 대상 사건 수반 사임/해임
  이면 FAIL.
- **출처·절차**: submissions JSON 8-K `items`에 `"4.01"` — 히트 시 8-K
  원문에서 불일치 문언 확인·인용. accession 기록.

### (f) MTD 생존 증권 사기 집단소송 부재

- **판정**: 주장 기간(class period)이 W와 교차하는 증권 사기 집단소송이
  motion to dismiss에서 (전부 또는 일부) 생존 → FAIL. 소송 제기됐으나
  MTD 인용 기각·자진 취하 → MINOR. 소송 없음 → PASS.
- **출처·절차**: Stanford Securities Class Action Clearinghouse
  (`https://securities.stanford.edu`) — 회사명·티커 검색, 케이스 페이지의
  MTD 처리 상태 확인. 케이스 URL + 접근일 기록. (비-EDGAR 출처 — 접근
  불가 시 판정을 내리지 않고 INCOMPLETE + 사유 기록.)

### (g) 관측 후 추적창 24개월

- **판정**: 감사·선정 시점이 관측창 종료 + 24개월 이후 → PASS. 미달 →
  **INCOMPLETE** (FAIL 아님 — 시간이 해소하는 상태). INCOMPLETE 대조군은
  잠정(provisional) 딱지로만 선정 가능하며, 24개월 도달 시 (a)–(f)를
  재검색해 확정한다 (재검색일 기록).
- **출처·절차**: 기계 산술 (관측창 종료일 + 24개월 ≤ 판정일). 날짜 2개
  기록.

## 2. 티어링 (D106 §3 이행)

| 티어 | 요건 |
|---|---|
| **Tier A** | (a)–(g) 전부 PASS |
| **Tier B** | (a)–(c)·(g) PASS + (d)–(f)에 MINOR만 존재 (전건 문서화) |
| **부적격** | 그 외 전부 — FAIL 1건 이상 또는 미문서화 항목 존재 |

- **FPR 보고 규칙 (사전 등록)**: 미래 FPR은 **티어별 분리 표기**가 기본형
  이다. 합산(pooled) 수치는 티어별 수치를 **병기할 때에만** 허용 — 무언
  합산(silently pooled) 금지. 발행 표면 문언 예: "FPR: Tier A x/n_A,
  Tier B y/n_B (pooled (x+y)/(n_A+n_B))". lint 확장 후보로 등록
  (기계 강제는 차기 사이클 freeze에서).

## 3. 매칭 (D106 §3 "where feasible"의 기계화)

**3축 기본 요건** (짝 실험군 케이스 대비):

1. **산업**: 2-digit SIC 일치 (EDGAR submissions의 SIC 선두 2자리).
2. **규모**: PIT 시가총액 밴드 일치. 밴드 정의 (매칭 회계기간 말 기준,
   시가총액 산출 불가 시 `dei:EntityPublicFloat` 대용 — 대용 사실 기록):
   - micro: < $300M
   - small: $300M – $2B
   - mid: $2B – $10B
   - large: $10B – $50B
   - mega: ≥ $50B
3. **회계기간**: 대조군 관측창이 짝 실험군 관측창과 **길이의 ≥50% 중첩**.
   타이브레이크: FYE 월 원형 거리 0–6 (v2 S2-v2 승계).

**완화 사다리 (매칭 불가 시 — 순서 고정, 전건 문서화)**: 적격 후보가
0이 될 때에만 다음 단계로 내려가며, 적용된 완화는 manifest의
`relaxations[]`에 단계·사유와 함께 기록한다. 무언 완화 금지.

- R1: 인접 시가총액 밴드 허용 (±1 밴드)
- R2: 회계기간 중첩 50% → 25%
- R3: 2-digit SIC → 1-digit(major group) 일치

**정직 기록 — 규모 축의 변경**: v2(S2-v2)는 규모를 PIT **매출** 비율로
매칭했다. v3의 시가총액 밴드는 소유자 지시(2026-07-20, D106 위임)에 따른
**전향 변경**이며, 기존 집합의 매출 기반 매칭 기록을 소급 재평가하지
않는다.

## 4. 회고 감사 (공시 전용 — disclosure only)

- **모집단**: 기존 대조군 전수 — 4개 집합: ① wave-1 원 대조군 C01–C08 (8)
  ② wave-1 v2-controls 재추첨 V01–V22 (22, RP-09
  `runs/rp09/control_group_v2.json` — 초판 문면은 이 집합을 "wave-2"로
  오기했다: 실제로는 wave-1 팔의 대조군 확장이다) ③ wave-2 대조군
  W01–W23 (23, `data/candidates/candidates_wave2.json` — 초판 로스터
  누락분, 감사 실행 전 본 정정으로 편입) ④ holdout hc_01–hc_09 (9).
  총 62, CIK 중복은 1회만 감사하고 소속 집합을 병기한다.
  **정정 기록 (2026-07-21, 감사 실행 전)**: 초판(커밋 d096ff6) §4의
  집합 명명 오기·W-집합 누락을 실행 전에 정정 — 커버리지 확장이며 기준
  자체(§1–§3)는 무변경 (D106 ② 공시 전용 감사의 기계적 커버리지 수리).
- **감사 창 W의 조작화 (실행 전 고정)**: 대조군의 매칭 회계기간 시작일이
  후보 파일에 별도 기록되지 않은 경우, W 시작 = 짝 실험군
  (`matched_case_id`)의 `manipulation_period_start`, 그것도 null이면
  `cutoff_date` − 36개월. W 끝 = `cutoff_date` + 24개월. 이 조작화는
  §1의 W 정의를 기록 가용 필드로 구현한 것이며 감사 문서에 병기한다.
- **절차**: §1 체크리스트를 기존 대조군에 그대로 적용, 결과를
  `controls/retrospective_audit_v1.md`에 후보별 판정표(기준 × 판정 ×
  출처 인용)로 기록한다.
- **불변 경계 (D106 공통 OUT의 적용)**: 기존 대조군이 어떤 기준을
  FAIL해도 — ① **발행 FPR을 재계산하지 않는다** ② 대조군을 소급
  제거·재분류하지 않는다 ③ 동결 채점 레코드를 접촉하지 않는다. 유일한
  산출물은 공시다: `docs/methodology_limitations.md`에 **일자 기입
  L-엔트리**를 추가해 (i) 어느 대조군이 어느 기준을 FAIL하는지 (ii) 발행
  FPR이 **원 선정 기준(v1/v1.1/v2) 조건부**임을 명시한다.
- **실행 시점**: 본 문서 커밋 **후** 별도 실행 (freeze-commit-then-run —
  절차가 결과 관측보다 먼저 고정되어야 감사가 사전 등록의 성격을 갖는다).
  네트워크 출처: sec.gov(공개 fetch, D100 선례) + securities.stanford.edu.
  모델 호출 0 예상 — 검색·전사 작업.

## 5. 대조군 manifest 스키마 스텁 (차기 사이클 데이터 입력 강제)

정식 스키마 파일(`schemas/control_manifest.json`)은 **차기 사이클 freeze에
포함**해 커밋한다 — 선정 파이프라인은 입력 시점(data-entry time)에 본
스키마 검증을 통과하지 못하는 대조군을 즉시 예외로 거부한다 (검증기 없는
선정 실행 금지). 스텁 (필드 규범 — 정식 파일의 원문):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "control_manifest v3 stub — CONTROL_CRITERIA_v3 §5",
  "type": "object",
  "required": ["control_id", "cik", "paired_treatment", "cleanliness",
               "tier", "matching"],
  "properties": {
    "control_id": {"type": "string"},
    "cik": {"type": "string", "pattern": "^[0-9]{10}$"},
    "paired_treatment": {"type": "string"},
    "cleanliness": {
      "type": "object",
      "required": ["a_enforcement", "b_restatement", "c_item402",
                   "d_material_weakness", "e_auditor_change",
                   "f_class_action", "g_tracking_window"],
      "additionalProperties": false,
      "patternProperties": {
        "^[a-g]_": {
          "type": "object",
          "required": ["verdict", "source", "search_date"],
          "properties": {
            "verdict": {"enum": ["PASS", "FAIL", "MINOR", "INCOMPLETE"]},
            "source": {"type": "string", "minLength": 1},
            "search_date": {"type": "string", "format": "date"},
            "note": {"type": "string"}
          }
        }
      }
    },
    "tier": {"enum": ["A", "B", "provisional"]},
    "matching": {
      "type": "object",
      "required": ["sic2", "cap_band", "fiscal_overlap_pct", "relaxations"],
      "properties": {
        "sic2": {"type": "string", "pattern": "^[0-9]{2}$"},
        "cap_band": {"enum": ["micro", "small", "mid", "large", "mega"]},
        "cap_band_source": {"enum": ["market_cap", "public_float"]},
        "fiscal_overlap_pct": {"type": "number", "minimum": 0, "maximum": 100},
        "relaxations": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["step", "reason"],
            "properties": {
              "step": {"enum": ["R1", "R2", "R3"]},
              "reason": {"type": "string", "minLength": 1}
            }
          }
        }
      }
    }
  }
}
```

## 6. 경계 요약 (D106 공통 OUT 승계 — 본 문서가 하지 않는 것)

- 동결 산출물·발행 수치·과거 거버넌스 기록: **0건 변경** (본 문서는 신규
  파일 1개 추가일 뿐이다).
- 발행 FPR 재계산·소급 지표 변경: 금지 (§4가 명시 재확인).
- 기존 대조군 집합의 소급 재선정·제거: 금지.
- v1/v1.1/v2 문서의 소급 개정: 없음 (역사 기록으로 보존).

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
