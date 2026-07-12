# specs/payload_v2.md — payload-v2 진단 추출기 사전 등록 (WS-1 / F-4)

> **freeze-commit-then-run**: 본 스펙 커밋은 `pipeline/payload_v2_extract.py`가
> git 이력에 존재하기 **전에** 이루어진다. 커밋 순서가 사전 등록의 증거다.
>
> **진단 전용(diagnostic-only) 선언**: 본 추출기의 출력은 어떤 피평가자
> 페이로드에도 편입되지 않는다. 동결 페이로드(`pipeline/build_payload.py`)는
> 불변이며, 편입은 **별도 소유자 게이트**(신규 미터링 런 + 페이로드 재동결 +
> freeze 개정)를 요구하는 명명된 미래 결정이다. 이 세션(미터링 0)의 범위 밖.

## 1. 목적 — 닫으려는 페이로드 맹점 2개

외부 검토 F-4: 동결 페이로드의 제출물 연대기(`load_filing_chronology`)는
`(form, filingDate)`만 실어 **8-K가 전부 동질**로 보인다 — Item 4.01(감사인
교체)·4.02(비신뢰 선언)가 일반 8-K(실적 발표 2.02 등)와 구분 불능. 또한 XBRL
시계열은 `USD` 단위 화이트리스트라 **주식수·주당 지표가 비가시**
(`shares`, `USD/shares` 단위 전부 필터에서 탈락).

본 추출기는 두 채널을 **진단 산출물로만** 복원한다:
(a) 8-K item 코드, (b) 주식수·EPS 사실.

## 2. 데이터 계약 (2026-07-12 로컬 캐시 실측으로 검증)

### 2.1 EDGAR submissions JSON (`~/aaer-data/{ticker}/edgar/CIK*.json`)

- `data.sec.gov/submissions/CIK##########.json`의 미러. `filings.recent` 아래
  병렬 배열: `accessionNumber`, `form`, `filingDate`, **`items`** 등.
- 8-K 행의 `items`는 쉼표 구분 문자열 — 실측 예: `"4.01"`, `"2.02,9.01"`,
  `"1.01,3.03,5.03,8.01,9.01"`. 비-8-K 행은 빈 문자열.
- 구형 청크 파일(`CIK…-submissions-NNN.json`)이 본체와 병존할 수 있다
  (실측: 77티커 중 64개). 본체의 `filings.files`에 열거된 하위 파일이
  로컬에 없으면 **fetch하지 않고 coverage에 기록**한다
  (실측: HUBG 1건 — `CIK0000940942-submissions-001.json`, 1996-05-15~
  2007-11-12 구간. 소유자 fetch 과제로 OWNER_QUEUE 등록).
- `items` 필드 자체는 실측 77/77 티커 전부 존재.

### 2.2 companyfacts JSON (`~/aaer-data/{ticker}/xbrl/*CIK*.json`)

추출 대상 태그·단위 (실측 검증):

| namespace | tag | unit |
|---|---|---|
| dei | `EntityCommonStockSharesOutstanding` | `shares` |
| us-gaap | `EarningsPerShareBasic` | `USD/shares` |
| us-gaap | `EarningsPerShareDiluted` | `USD/shares` |
| us-gaap | `WeightedAverageNumberOfSharesOutstandingBasic` | `shares` |
| us-gaap | `WeightedAverageNumberOfDilutedSharesOutstanding` | `shares` |
| us-gaap | `WeightedAverageNumberOfSharesOutstandingDiluted` | `shares` (별칭 — 아래 주) |
| us-gaap | `CommonStockSharesOutstanding` | `shares` |

**정직 기록**: 미션 지시문의 `WeightedAverageNumberOfSharesOutstandingDiluted`는
실측(HTZ companyfacts)에서 부재 — 실제 us-gaap 표준 태그는
`WeightedAverageNumberOfDilutedSharesOutstanding`이다. 두 철자를 모두
화이트리스트에 두고 존재하는 쪽을 추출한다 (택소노미 연차별 변형 대비).

## 3. 추출 규칙 (사전 고정)

### 3.1 공통 PIT 의미론 — 동결 빌더와 동일

- **컷오프 필터**: `filed <= cutoff_date` (등호 포함 — cutoff_date 자체가 폭로
  '전일'로 정의됨, `cutoff_guard.py` 동일). 시간 필터는 모듈 내 **단일 비교
  지점**으로 수렴한다 (`build_payload.py`와 동일한 기계 검증 가능 구조).
- **기간 중복 해소**: 같은 `(tag, start|end)` 키는 컷오프 전 **최신 filed 승리**,
  동률은 accession 문자열 큰 쪽 (동결 빌더 line 109 tie-break와 동일:
  `(filed, accession or "") > (prev_filed, prev_accession or "")`).
- **기간 분류**: duration 사실(start 존재)은 동결 빌더와 동일 밴드 —
  연차 340–400일, 분기 75–100일, 그 외 span 폐기. instant 사실(start 부재,
  주식수 계열)은 `instant`로 보존.
- **provenance**: 모든 사실에 `accession`, `filed`, `form` 동반.

### 3.2 8-K item 파싱 규칙

- 대상 form: `8-K`, `8-K/A` (form 원문 보존 — /A 여부는 소비자가 판단).
- `items` 원시 문자열을 **그대로 보존**(`items_raw`)하고, 파생 리스트는
  쉼표 분리 → 각 토큰 공백 strip → 빈 토큰 제거 (`items`).
- 2004-08 이전 구형 item 번호 체계(예: `"5"`, `"7"`)도 동일 규칙으로 파싱만
  한다 — 해석(4.01/4.02 매칭 등)은 소비자(B3 등) 몫.
- 컷오프 필터는 `filingDate <= cutoff_date`.

### 3.3 fail-closed 자세 (`cutoff_guard` 미러)

- 파싱 불가 날짜 → **예외** (skip 금지 — 위반 사실을 지우는 조용한 필터 금지).
- 케이스에 필요한 submissions/companyfacts 파일 부재 → 코어 함수는 **예외**.
  CLI 레벨에서만 케이스 단위로 포착해 coverage에 `missing`으로 기록하고
  나머지 케이스를 계속한다 (네트워크 fetch 금지 — 계약 9).

### 3.4 `cutoff_guard.load_document()` 비경유 사유 (문서화 의무 이행)

`load_document()`는 **후보 레지스트리(정답지) 기반·문서 단위** 게이트웨이다
(case_id → candidates.json 컷오프 조회 + accession 단건 대조). 본 추출기는
동결 빌더 `build_payload.py`와 동일한 **피평가자측 벌크 패턴**을 따른다:
`data/evaluatee/cases*.json`의 cutoff_date만 입력으로 받고(정답지 접근 없음),
submissions/companyfacts를 직접 읽되 look-ahead 필터를 단일 비교 지점으로
수렴시키며, 그 지점을 단위 테스트가 기계 검증한다. 가드의 fail-closed 자세
(§3.3)는 그대로 미러링한다. 이는 기존 동결 빌더가 이미 확립한 선례의 확장이며
새 우회 경로가 아니다.

## 4. 케이스 유니버스와 출력

- **유니버스**: `data/evaluatee/` 5개 파일 전체 — `cases.json`(16) +
  `cases_v2.json`(22) + `cases_wave2.json`(32) + `cases_holdout.json`(3) +
  `cases_holdout_controls.json`(9) = **82 케이스 엔트리** (고유 티커 77).
- **출력**: `runs/diagnostics/payload_v2/{case_id}.json` — 구조:

```json
{
  "spec": "specs/payload_v2.md",
  "diagnostic_only": true,
  "case_id": "…", "ticker": "…", "cutoff_date": "…", "source_file": "cases*.json",
  "eightk_items": [
    {"accession": "…", "form": "8-K", "filing_date": "YYYY-MM-DD",
     "items_raw": "2.02,9.01", "items": ["2.02", "9.01"]}
  ],
  "share_facts": {
    "dei:EntityCommonStockSharesOutstanding": [
      {"start": null, "end": "…", "period_type": "instant", "value": 0,
       "unit": "shares", "filed": "…", "accession": "…", "form": "…"}
    ]
  },
  "coverage": {
    "submissions_files_read": 0,
    "paginated_subfiles_listed_not_cached": [],
    "facts_namespaces_present": ["dei", "us-gaap"],
    "tags_found": {"…": 0}
  }
}
```

- **coverage 집계**: `runs/diagnostics/payload_v2/COVERAGE.json` —
  `coverage: n/82`, 케이스별 결측·부분(하위 파일 미캐시) 명세.
- `runs/` 추가 커밋이므로 커밋 전 `verify_blindness.py --write-manifest`
  전역 매니페스트 재생성 필수 (HANDOFF 규약).

## 5. 테스트 계약 (`pipeline/test_payload_v2.py`, 픽스처 `pipeline/fixtures/`)

1. item 파싱: 단일(`"4.01"`)·다중(`"2.02,9.01"`)·공백 포함·빈 문자열.
2. 컷오프 필터: `filingDate`/`filed` > cutoff 항목의 부재 기계 검증,
   == cutoff 포함 검증.
3. 주식수·EPS 단위 추출: `shares`·`USD/shares`·dei namespace가 실리고
   기존 USD 화이트리스트와 교차 오염이 없는지.
4. (tag, period) 최신 filed 승리 + accession tie-break.
5. 파일 부재 fail-closed: 예외 발생 (조용한 빈 출력 금지).
6. 파싱 불가 날짜: 예외 발생.

## 6. 이 산출물이 아닌 것 (스코프 부정 명세)

- 피평가자 페이로드 변경 아님 (§0 선언). 동결 런의 재실행 근거 아님.
- 지표·점수 계산 아님 — B3(WS-2)가 본 추출기의 **파서만** 재사용한다.
- 발행 표면 변경 아님 — 발행 인용은 소유자 게이트 diff 경유.

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
