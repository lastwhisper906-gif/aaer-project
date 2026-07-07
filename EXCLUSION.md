# EXCLUSION.md — Wave 2 로스터 규칙 + 제외 사유 (사전 커밋)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-07.
> **지위: wave-2의 어떤 채점 호출보다 먼저 커밋된다.** 로스터는 **규칙**이
> 결정하며 재량이 아니다. 아래 기대 생존 집합은 sanity check일 뿐, **규칙과
> 게이트 결과가 binding**이다. 동결 wave-1 로스터·결과는 불침해.

## 1. 로스터 규칙 (기계적, 재량 없음)

1. 시작 = 동결 킬 스위치 **A형 23** (`data/candidates/candidates.json`,
   `ab_classification=="A" && ab_signed_off==true`; 표: `scoring/ab_first_pass.md`).
2. **마이너스 wave-1 채점 8** (동결): MON·OFIX·LOGI·HTZ·ICON·MRVL·SCOR·KHC.
   → 잔여 **15**: CSC·WFT·PUDA·MILL·DMND·PWE·VRX·OSIR·BRX·TNGO·HAIN·CGI·GE·MDXG·UAA.
3. **마이너스 worked-example 오염 2** (§2): VRX·GE. → **13**.
4. **동결 게이트 적용** (§3, 빌드 시 기계 판정 — 점수와 무관):
   XBRL 가용성 · 폭로일 검증(Principle A) · 문서 무결성. 게이트 실패분 제외.
   게이트 결과는 §4에 기록. **사전 판단 금지 — 게이트가 결정.**

## 2. Worked-example 오염 제외 (사전, 확정)

| 티커 | 사유 (한 줄) |
|---|---|
| **VRX** (Valeant, T18) | WORKED-EXAMPLE CONTAMINATION — 채점 기준(A/B·오류 taxonomy)을 이 케이스의 정답 키를 보며 구성. 채점 시 튜닝 데이터로 시험하는 꼴. 결과 가치 보호 목적의 제외(프로세스 아님). |
| **GE** (General Electric, T25) | WORKED-EXAMPLE CONTAMINATION — 동일. 기준 구성 시 answer-key와 함께 학습된 케이스. |

## 3. 동결 게이트 정의 (빌드 시 적용 — 점수 독립, 사전 판단 금지)

- **G-XBRL (가용성)**: `data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json`가
  존재하고, **컷오프 이전** 최소 사전-폭로 XBRL 분기 수(동결 기준: E-시리즈
  최소 분기)를 충족. 수기-비용/40-F 전용/XBRL 시대 이전이면 실패. **CSC의
  2010 XBRL 시대 커버리지를 사전 판단하지 않는다 — companyfacts를 실제로 조회해
  게이트가 결정.**
- **G-DATE (폭로일)**: Principle A(최초 공개 폭로일)를 EDGAR 1차 문서에서
  재검증 가능. 컷오프 = 폭로일 전일. 검증 불가 시 실패. 케이스별 출처 문서
  기록(§5).
- **G-DOC (무결성)**: AAER/1차 문서 원문 대조 무결(위조·불일치 없음), documents
  집합이 동결 매니페스트 규약 충족.
- **E8b (집행 이력 — 대조군 전용)**: 대조군 후보의 10b-5/AAER 집행 이력 스캔
  (동결 `control_v2.OWNER_CONFIRMED_ENFORCEMENT_CIKS` + `aaer_hits_v2`). 실험군엔
  적용 안 함.

## 4. 게이트 결과 (실행 완료 2026-07-07 — G-XBRL companyfacts 조회 + 동결 `load_pit_series` PIT 커버리지)

**방법**: `tools/fetch_xbrl_facts.py`로 각 후보 companyfacts를 data.sec.gov에서
조회(availability), 동결 `pipeline/build_payload.load_pit_series`로 **컷오프 전**
PIT 시계열을 조립해 커버리지 측정(점수 독립·오프라인·결정론). 통과 = 자산
instant ≥2 AND (매출 또는 순이익 분기≥4 또는 연차≥2) AND 페이로드 태그 ≥8.

**결과: 생존 9 / 실패 4** — 규칙+게이트가 결정(사전 기대와 일치하나 게이트가
근거).

| 티커 | G-XBRL (커버리지) | G-DATE | G-DOC | 최종 | memorization_risk |
|---|---|---|---|---|---|
| CSC  | PASS (rev q6/a3, NI q6/a3, assets i5, 30tags/176facts) | 2010-08-10 | ok | **생존** | 사후측정 |
| WFT  | PASS (rev q8/a3, NI q8/a3, assets i7, 36tags/274facts; 전신 CIK 0001170565 companyfacts 404 — XBRL 시대 이전, 주 CIK가 커버) | 2011-02-28 | ok | **생존** | 사후측정 |
| OSIR | PASS (rev q22/a6, NI q2/a0, assets i18, 35tags/458facts) | 2015-11-05 | ok | **생존** | 사후측정 |
| BRX  | PASS (표준 Revenues 태그 부재=REIT 임대수익 태그, NI q10/a3 + assets i10, 19tags/178facts로 통과 — 페이로드는 표준 매출 결측·주석 대상) | 2016-02-07 | ok | **생존** | 사후측정 |
| TNGO | PASS (rev q20/a6, NI q20/a6, assets i19, 33tags/595facts) | 2016-03-06 | ok | **생존** | 사후측정 |
| HAIN | PASS (rev q21/a7, NI q21/a7, assets i24, 35tags/721facts) | 2016-08-14 | ok | **생존** | 사후측정 |
| CGI  | PASS (rev q26/a7, NI q26/a7, assets i24, 31tags/599facts) | 2017-04-04 | ok | **생존** | 사후측정 |
| MDXG | PASS (rev q25/a6, NI q25/a6, assets i23, 31tags/616facts) | 2016-12-14 | ok | **생존** | 사후측정 |
| UAA  | PASS (rev q40/a12, NI q40/a11, assets i41, 35tags/1127facts) | 2019-11-02 | ok | **생존** | 사후측정 |
| PUDA | **FAIL** — companyfacts 404 (data.sec.gov 무등록, 中 RTP 소형) | 2011-04-07 | — | **제외** | true (해당 없음 — 탈락) |
| MILL | **FAIL** — 컷오프 2011-07-27 이전 PAYLOAD-태그 사실 0건 (최초 us-gaap 사실 filed 2011-10-05 = 컷오프 +70일; XBRL 채택이 폭로 이후) | 2011-07-27 | — | **제외** | — |
| DMND | **FAIL** — 최초 PAYLOAD-태그 사실 filed 2012-11-14 = 컷오프(2011-10-31) +1년 (XBRL 채택이 폭로 이후, "수기 비용" 플래그 실증) | 2011-10-31 | — | **제외** | — |
| PWE  | **FAIL** — 캐나다 40-F/IFRS 제출자 (ifrs-full 163태그, us-gaap는 2018-03 이후만 = 컷오프 2014-07-28 후) | 2014-07-28 | — | **제외** | — |

> **최종 wave-2 실험군 로스터 (게이트 확정, 9)**: BRX·CGI·CSC·HAIN·MDXG·OSIR·
> TNGO·UAA·WFT (알파벳 = 채점 순서, ANALYSIS_PLAN_WAVE2 §7). **memorization_risk
> 사전 태그(China-RTO 클러스터) 해당자 없음** — PUDA(T06, 유일 China-RTO)가
> G-XBRL 탈락. 9사 암기는 사후 프로브·교란으로 측정(§9). **BRX·OSIR 커버리지
> 주석** 위 표 기재 — 채점 해석 시 참조.
>
> G-DATE는 동결 candidates.json의 `first_revelation_date`(킬 스위치 단계 확정,
> 컷오프=전일)를 승계하며, Principle-A EDGAR 1차 문서 재검증은 빌드 시 출처
> accession 기록으로 수행(동결 wave-1 폭로일 불침해).

## 5. 폭로일 재검증 절차 (Principle A — 케이스별 출처 문서 빌드 시 기록)

각 생존 후보에 대해: EDGAR 1차 문서(8-K Item 4.02 / 최초 재작성 공시 / SEC
litigation release 중 **가장 이른 공개일**)를 조회해 Principle A 폭로일을 확정,
**컷오프 = 폭로일 전일**로 등록(`pipeline/cutoff_guard` 레지스트리). 출처
accession/URL을 케이스별로 §4 확장표에 기록. 동결 wave-1 케이스의 폭로일은
재검증 대상 아님(불침해).

## 6. 대조군 규칙 (사전 커밋 — 동결 순수 함수 재사용)

- 동결 `tools/control_v2.py`(= `docs/CONTROL_CRITERIA_v2.md`) 순수 함수 그대로:
  E1–E9 하드 스크린 + **E8b 집행 이력** + **FYE 보정 S0**. 실험군 케이스당
  **2–3** 대조군, **기존 22 대조군과 dedup**.
- 기존 대조군이 매칭될 수 있으나 **wave-2 내에서 새로 채점**한다(동결 점수
  재사용 금지 — RESULT IMMUTABILITY). 네트워크: companyfacts 조회 필요 시
  `control_v2 fetch`, 선택은 순수 함수(네트워크 불요).

## 7. China-RTO / 고암기 케이스

게이트 생존한 China-RTO(또는 동결 고암기 클러스터) 케이스는 `memorization_risk=
true` 태그로 편입하고 ANALYSIS_PLAN_WAVE2 §9 계층 비교에 넣는다. 태그는 제외
사유가 아니다(편입 후 계층 분석).

---

**불변**: BLINDNESS · CUTOFF · RESULT IMMUTABILITY. 이 파일과
`analysis/ANALYSIS_PLAN_WAVE2.md`가 wave-2 첫 점수보다 먼저 커밋된다.
</content>
