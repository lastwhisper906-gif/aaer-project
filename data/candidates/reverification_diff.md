# REVERIFICATION_DIFF — 1차 소스 전수 재검증 (2026-07-03, 로컬 CLI 세션)

> **상태: PENDING HUMAN SIGN-OFF.** 웹 세션의 sec.gov 이그레스 차단(프록시 CONNECT 403)으로
> Stage 3~4의 모든 AAER 인용이 2차 소스 경유였다. 로컬 직접 접근 확보 후 30건 전수를
> **원문(AAER 명령문/소장/EDGAR 제출 이력)** 과 대조한 결과가 이 문서다.
> - 원문 사본: `~/aaer-data/{ticker}/` (git 밖, data/README.md 규약). 텍스트 추출본 `.txt` 병존.
> - 결정론 재계산: `tools/compute_edgar_fields.py` → `data/candidates/edgar_verification.json`
> - **객관 필드(날짜·수치·릴리스 번호)만 candidates.json에 반영**했다. 판단 의존 필드
>   (폭로일 원칙, 편입 기준)는 그대로 두고 §C에 월요일 안건으로 표시했다.
> - 학습 노트(§10): 이번 재검증에서 확인된 오류의 전형은 역시 '숫자 자체'가 아니라
>   **범주의 슬립**이었다 — SB-폼이라고 추정한 것이 정규 10-K/10-Q였고(T06/T12/T22),
>   8-K라고 기록된 것이 10-Q였다(T19). REVIEW.md 항목 1의 사전 감각과 일치.

## A. AAER/소장 원문 대조 (release no., 기간, scheme 수치)

방법: 30건 전수를 병렬 검증 에이전트 5조(케이스당 aaer_no 인쇄 헤더 / aaer_date / 조작기간 /
scheme 수치 전건 / 폭로 서술)로 원문 텍스트에 대조. 판정 등급: CONFIRMED / MISMATCH / NUANCE /
NOT-IN-FETCHED-DOCS. 아래는 **비(非)CONFIRMED 전건**. 열거되지 않은 필드(30건 전체의 aaer_no
인쇄 번호, aaer_date, 회사명 캡션, scheme 수치 대부분)는 원문 인쇄 텍스트와 일치 확인됨.

### A-1. MISMATCH → candidates.json 정정 반영

| ID | 필드 | 구값 | 신값 | 원문 근거 (인용 + pinpoint) |
|---|---|---|---|---|
| T04 WFT | scheme_summary | "a Bermuda 'Eliminations' entity" | 룩셈부르크(FY2007-08)·버뮤다(FY2009-10) 엔티티, 모두 'Eliminations region' 내 | ¶30: "plug' adjustment to two different Weatherford **Luxembourg entities** within Weatherford's Eliminations region"; ¶39: E&Y가 "proposed reclassifying the adjustment to a Bermuda entity"; ¶43: "made in 2009 and 2010 using **a Bermuda entity**"; ¶44 엔티티 표 (WFT Luxembourg SARL 등 → WFT Bermuda Ltd.) — 33-10221.pdf |
| T04 WFT | revelation_source (vehicle) | "Form 12b-25 notification" | Form 8-K (+ 동일자 NT 10-K, EDGAR 실측) | ¶55: "On March 1, 2011, Weatherford **filed a Form 8-K** with the Commission, in which it made public for the first time that it would be restating its financial results for 2007-2010" — 33-10221.pdf. 구기록이 인용한 34-79109는 E&Y 별건 명령 → 인용도 33-10221 ¶3/55로 교체 |
| T12 LOGI | manipulation_period_start | 2009-04 | **2008-04** | 명령문은 "a five-year period"(Summary) = FY09–FY13, fn.2: "The Company's fiscal year is April 1 to March 31"; ¶55: "**From late FY08 through FY09**, LOGI improperly recognized revenue for sales to its largest wholesale distributor (Distributor) in the AMR region"; ¶54: 10-K/A가 "revising its financial statements for FY09 through FY13" — 34-77644.pdf. 구값은 'FY09'를 달력 2009로 오독한 회계연도 슬립 (자체 scheme_summary의 'FY09 Americas revenue'와도 모순이었음) |
| T18 VRX | manipulation_period_start | 2014-01 | **2014-07** | ¶15: "Valeant reported its results for the quarters ended **September 30, 2014 through September 30, 2015**…"; ¶15a: "announced U.S. organic growth in the double digits for each quarter **from Q3 2014 through Q3 2015**" — 33-10809.pdf. 1월을 지지하는 원문 문장 없음. 대안 원칙(§C): Philidor 설립·지원은 2013부터(¶2,¶8), 최후 오도 제출은 FY2015 10-K 2016-04-29(¶25) |
| T19 OSIR | aaer_date | 2017-11-02 | **2017-11-03** | LR 페이지 헤더 인쇄: "Litigation Release No. 23978 / November 3, 2017 — **Accounting and Auditing Enforcement Release No. 3905 / November 3, 2017**" (소장 제출일은 11-02 — 맥락으로 보존). AAER-3905가 SEED 경유가 아니라 **LR 페이지에 직접 인쇄**되어 있음도 확인 |
| T19 OSIR | revelation_source | "2015-11-16 8-K" + 2016년 8-K URL | Q3 10-Q(11-16) + 8-K Item 4.02(11-20) | 소장 ¶29: "**On November 16, 2015, Osiris filed its Form 10-Q** for the third quarter of 2015 and, within that filing, disclosed a material weakness … In a **Form 8-K filed on November 20, 2015**, Osiris disclosed that it would be restating…" — comp-pr2017-207.pdf. §B-4 참조 |
| T21 SCOR | scheme_summary | "~$43-50M" | **~$50M** ($34.5M NMT + ~$12M linked) | ¶1: "materially overstated revenue by **approximately $50 million**"; ¶2: "overstated by over $34.5 million"; ¶3: "overstating revenue by approximately $12 million in 2015" — 33-10692.pdf. $43M은 원문 어디에도 없음 |
| T02 CSC | scheme_summary | "Nordic/Australia 'cookie jar' reserves" | 호주=cookie jar, Nordic=분쟁회계·자산과대·선급자본화로 분리 | ¶1/¶10: "senior CSC finance personnel **in Australia** fraudulently overstated the company's earnings using 'cookie jar' reserves"; ¶11(Nordic): "improperly accounting for client disputes, overstating assets, and capitalizing expenses"; ¶98+fn.32: unsupported prepaid assets >$30M — 33-9804.pdf |
| T30 LK | scheme_summary (수치 귀속) | ">RMB2.12B (~$311M)" 단일 표기 | SEC 수치(>$300M)를 주로, RMB2.12B는 회사 자체조사 수치로 병기 | LR-24987/PR 2020-319: "intentionally fabricated **more than $300 million** in retail sales"; RMB2.12B는 Luckin 2020-07-01 특별위 공시(2019 순매출 과대계상)로 **측정 대상이 다른 별개 문서의 수치** — 도시에 자체 발견 확정 |

### A-2. NUANCE — 값 유지, 근거 보강 (notes에 원문 pinpoint 추가)

| ID | 필드 | 내용 |
|---|---|---|
| T01 RINO | revelation_source | 소장은 폭로 주체를 "a Hong Kong-based investment firm"으로만 지칭(Muddy Waters 미명명, ¶24); 거래정지는 11-18(¶13). 11-10 보고서·기간·수치($491M/$31M)는 전부 확정 |
| T03 CCME | 기간 | 명시적 시작은 "at least November 2009"(¶3; 역합병 2009-10은 ¶13), 마지막 일자 있는 허위발표는 2011-02-03(¶44), 2011-03은 감사인 사임월(¶31). 월 정밀도 기록 유지 |
| T05 KEYP | 기간 | 부외 현금계좌는 "From at least July 2008 … until March 2011"(¶40)로 기록창(2010-05~2011-01)보다 넓음 — 기록창은 소장의 공시위반 창(¶3, ¶20)과 일치 |
| T06 PUDA | 기간·캡션 | 사기는 폭로 후에도 지속(위조 CITIC 서한 2011-08-31 ¶31, 오도성 8-K 2011-09-01 ¶32); 피고는 Zhao/Zhu뿐(회사는 당사자 아님 — notes 기존 기재와 일치). 4-11 확인 vehicle은 소장상 'press release'(¶28) |
| T07 MON | 기간 시작 | 원문 최초 행위: 캐나다 프로그램 2009-04(¶37), 미국 세일즈 통지 "late May 2009"(¶15) — 기록 2009-06과 근사, 유지 |
| T08 MILL | 기간 끝 | 2015-03은 ¶57("all three quarters of fiscal years 2011 through 2015", FY말 4/30)에서의 추론이지 인쇄된 날짜 아님 |
| T10 DMND | 기간 | FY2010–FY2011 경계(2009-08~2011-07)를 원문이 회계연도 단위로 서술(¶6, ¶28, ¶40); 최초 구체 행위는 2010-02(¶25). ~20% 하락 수치는 원문에 없음(2차 소스 유지) |
| T11 OFIX | 기간 | 원문 인쇄: "From at least 2011 to mid-2013"; 정정은 FY2010 연차분까지 포함(¶92) |
| T13 HTZ | 캡션·폭로일 | 명령 캡션은 2피고(Hertz Global Holdings + The Hertz Corporation). ¶33에 더 이른 공개 신호 2014-05-13(Q1 10-Q 제출불능 + FY2011 정정 가능성) 존재 → §C |
| T14 PWE | 폭로 서술 | 소장 ¶174가 2014-07-29 보도자료를 직접 인용, ¶180: $9.16→$7.86 (~15% 하락) — 기록 확정. LR들의 "no longer be relied upon"은 2014-09 정정 공시 귀속 |
| T15 RATE | 수치 구성 | ~$0.8M = $300K(¶9)+$176K(¶15)+$305K(¶15)=$781K; 쿠션 계정은 "since at least early 2011"(¶24, notes 기존 기재와 일치); SOX 수수료 ≥$99K(¶26-27) |
| T16 ICON | scheme 표현 | 허위 수익의 실체는 JV buy-in 과지급의 수익/이익 인식(소장 ¶45, ¶58-59) — 'licensing revenue' 표현은 넓은 의미. $239M+ 손상은 PR/LR + Clamen 명령 ¶4($239.4M~$259.4M)로 이중 확정 |
| T17 MRVL | 기간 | §C 참조 — 기소 2분기(¶12/¶18) vs 사용 3분기(¶10/¶21) vs 명령 자체 Relevant Period "January 2015 through July 2015"(¶2). '$165M'은 원문 미인쇄(산술 합) |
| T20 BRX | 폭로 서술 | ¶34가 2016-02-08 8-K(스무딩 공시+4인 사임)를 직접 서술 — 확정. ~20% 하락 수치는 원문에 없음. "accounting employee"=Accounting SVP(¶11) |
| T22 TNGO | 수치 | $40M = SEC 헤드라인/작업조서 수치(¶94), $30.5M = 2016-11 12b-25 추정치(¶93) — 상이한 기준의 두 수치 병존 |
| T23 HAIN | 기간·표현 | 원문: "From at least 2014 until May 2016"/"FY 2014-2016"(FY2014는 2013-07 개시); Q4 FY2016에도 인센티브 서술(¶14) → 끝 2016-06 방어 가능. 'return rights'→'spoils coverage'(상환, ¶5); 타겟은 유통사 재고구매 타겟(¶5-6). ~27% 하락·가이던스 미스는 원문에 없음 |
| T24 CGI | 수치 | $42.2M DPA 수치는 LR·소장 어디에도 없음(2차 소스 유지); 소장 내부 불일치: Q2 FY2017 10-Q 일자 ¶25(02-10) vs ¶31(02-02) |
| T25 GE | 기간 | 기록창은 보험창(Q3 2015~Q1 2017, Summary/¶36)과 파워창(2016-05~2017-10, ¶15)의 브래킷 — 원문 구조와 일치. 29%/45%(¶6), $2.5B(Summary; ¶13은 누적 >$2.7B 별도), $9.5B, $200M 전부 확정 |
| T26 MDXG | 폭로일 | 소장 ¶9: 공개 폭로를 2018-02~07 연쇄로 서술(-73%) — 기록된 2017-09-20(공매도 리포트)은 SEC 문서 밖 → §C |
| T27 WAGE | 하락률 | **도시에 가설 뒤집힘**: '>9%'는 $9.75의 오전사가 아니라 **명령문 ¶44의 원문 그대로** ("declined more than 9%"). 2차 소스(집단소송)의 -18.6%/$9.75와 병존 — notes에 양쪽 기재 |
| T28 KHC | 폭로일 | 명령문은 2019-02-21 사건(상각/소환장/하락)을 서술하지 않음(유일한 공개 사건은 2019-06-07 정정 10-K) — 기록은 동시대 시장 소스 기반 유지 |
| T29 UAA | 폭로일 | 명령문이 서술하는 시장 사건은 2017-01-31(-23%, ¶3/¶36)로 스킴 결과 사건이지 회계조사 폭로가 아님; 2019-11-03은 원문 밖(동시대 소스 기반 유지). no-GAAP-finding 각주(fn.2) 확정 |

### A-3. 확인된 인쇄 헤더 (aaer_no 30건 전수 결과 요약)

- 명령문 헤더/LR 페이지에 AAER 번호 인쇄 확인: T01(3482)·T02(3662)·T03(3479)·T04(3806)·T05(3447)·T06(3372)·T07(3741)·T08(3731)·T10(3527=LR-22902, 3526=33-9508)·T11(3845)·T12(3765)·T13(4012)·T14(4133=LR-24809 인쇄, "Accounting and Auditing Release" 표기)·T15(3683)·T17(4076)·T18(4153)·T19(3905=LR-23978 인쇄)·T20(4061)·T21(4091)·T23(3997)·T25(4194)·T27(4202)·T28(4248)·T29(4220)
- T09 FEED: AAER-3542는 **Marshall(개인 CFO) 명령 33-9557 헤더에만** 인쇄; Stadler 명령 33-9556·회사 소장·PR 2014-47에는 AAER 줄 없음 — 기록의 주의문 그대로 실증
- AAER 없음(페이지 무인쇄) 확정: T22 TNGO(LR-24255), T24 CGI(LR-24459), T26 MDXG(LR-24678), T30 LK(LR-24987)
- **T16 ICON 신규 사실**: 2019-12-05 행정명령 33-10730(respondent: Warren Clamen, CPA)의 헤더에 **AAER-4105 인쇄** — 임원 단독 AAER(T27 WAGE와 동일 축). aaer_no는 편입 기준 확정 전까지 null 유지 → §C
- 별건 AAER 확인: T14 PWE 관련 34-81544(Grab 102(e)) = AAER-3893 (회사 아님, 배제 유지 타당)

## B. EDGAR 제출 이력 재계산 (pre_revelation_quarters_available / xbrl_available / 폭로일 주변 제출물)

집계 규약(에지 케이스까지 `edgar_verification.json` `_meta.convention`에 고정):
10-K·10-K405·10-KT + 10-Q·10-QT, /A 제외, SB-폼 제외, filingDate가 폭로일 **이전**(strictly before).

### B-1. 정정 반영 (candidates.json 변경)

| ID | 필드 | 구값 | 신값 | 근거 (결정론 재계산) |
|---|---|---|---|---|
| T06 PUDA | quarters | 12 | **16** | 2007년 제출물(10-Q×3: 2007-05-21/08-14/11-14, 10-K FY2007: 2008-04-10)이 SB-폼이 아니라 **정규 10-K/10-Q**였음. 구기록의 "10-KSB/10-QSB일 것" 추정이 오류 |
| T07 MON | quarters | 41 | **43** | 10-K405(2001-03-26, FY2000) + 10-KT(회계연도 전환) 2건이 연차보고서로 실재. 32×10-Q + 9×10-K + 1×10-K405 + 1×10-KT |
| T11 OFIX | quarters | 43 | **42** | EDGAR 실측 11×10-K + 31×10-Q = 42. 구기록(5 recent + 38 older = 43)이 1건 과다 |
| T12 LOGI | quarters | 19 | **24** | 국내 filer 전환이 FY2010(2009-08)이 아니라 **FY2008부터**: 10-K 2008-05-30(rpt 2008-03-31)부터 10-K×6 + 10-Q×18 |
| T22 TNGO | quarters | 17 | **18** | 첫 10-Q가 2011-09-09(Q2 2011, IPO 직후) — 구기록("Q3 2011부터 13개")이 1건 누락. 4×10-K + 14×10-Q |
| T09 FEED | xbrl | true | **false** | 폭로 전 전 제출물 isXBRL=0. 구기록의 "2011-08-09 10-Q(기말 2011-06-30)는 Phase-3 의무라 XBRL 있을 것" 추정이 EDGAR 플래그와 불일치 (해당 10-Q isXBRL=0) |
| T10 DMND | xbrl | true | **false** | 폭로 전(2011-11-01 이전) 10-K/10-Q 전부 isXBRL=0 (FY2011 10-K 2011-09-15 포함). Phase-3 유예/지연으로 추정되나 플래그 기준 false |
| T10 DMND | quarters | null | **25** | 7×10-K(FY2005–FY2011) + 18×10-Q — 구기록의 "추정 ~25"와 일치, 이제 실측 |
| T02 CSC | quarters | null | **68** | 실측 (거대 filer, 웹 세션에서 JSON 잘림) |
| T04 WFT | quarters | null | **34** | **다중 CIK 합산**: 버뮤다 전신 CIK 0001170565(2002~2009-02) 27건 + 스위스 CIK 0001453090(2009-05~2010-11) 7건. FY2007~2008 10-K는 버뮤다 CIK 소속 확인 (10-K 2008-02-21, 2009-02-24) |
| T08 MILL | quarters | null | **16** | 실측 (FY말 4/30; FY2011 10-K는 폭로 다음날 2011-07-29 제출 → 제외 유지) |
| T13 HTZ | quarters | null | **29** | 전신 CIK 0001364479(현 Herc) 포함 합산 — 구기록 추정 ~28에 근사, 실측 29 |
| T16 ICON | quarters | null | **73** | 실측 |
| T17 MRVL | quarters | null | **60** | 실측 — 구기록 추정 ~59(15 10-K + 44 10-Q)에 근사 |
| T18 VRX | quarters | null | **23** | 실측 — 국내폼만 집계(Biovail 시절 40-F/6-K는 규약상 제외). 구기록 추정 ~19보다 4건 많음 |
| T19 OSIR | quarters | null | **37** | 실측 — 구기록 추정 ~36-37 범위 내 |
| T23 HAIN | quarters | null | **79** | 실측 (10-K405 시대 포함) |
| T24 CGI | quarters | null | **84** | 실측 |
| T25 GE | quarters | null | **94** | 실측 (제출 이력 3개 청크 전부 파싱) |
| T26 MDXG | quarters | null | **38** | 실측 — 구기록 추정 ~38 일치 |

### B-2. 일치 확인 (변경 없음, 신뢰도 상향)

| ID | 필드 | 기록값 | 실측 | 비고 |
|---|---|---|---|---|
| T01 RINO | quarters/xbrl | 11 / false | 11 / false | 완전 일치 |
| T03 CCME | quarters | 4 | raw 12 / 운영기 5 | 기록 4 = **보고기간 기준** 운영기(합병 2009-10 이후 rpt): 2009-11-16 10-Q는 SPAC기(rpt 2009-09-30) 커버라 제외 — 규약 일관, 변경 없음 |
| T05 KEYP | quarters | 3 | raw 12 | §A 참조 — Q1 2010 10-Q(2010-04-19 제출)가 역합병(2010-04) 전 쉘 제출물인지가 관건. 원문 소장의 합병일 확인 후 확정 |
| T14 PWE | quarters | null | null 유지 | FPI: 40-F 8건 + 6-K 276건 (폼 타입만으로 분기 실적 6-K 분리 불가) — 구기록 서술과 **정확히 일치** |
| T15 RATE | quarters/xbrl | 13 / true | 13 / true | 완전 일치 (전 13건 isXBRL=1) |
| T20 BRX | quarters | 9 | 9 | 구기록 "8일 수도"의 불확실성 해소 — Q3 2013 10-Q 실재 |
| T21 SCOR | quarters | 34 | 34 | cadence 추정이 실측과 일치 |
| T27 WAGE | quarters/xbrl | 22 / true | 22 / true | 완전 일치 (5 10-K + 17 10-Q, 전건 XBRL) |
| T28 KHC | quarters | 14 | 14 | 완전 일치 |
| T29 UAA | quarters | 55 | 55 | 완전 일치 |
| T30 LK | quarters | 2 | 6-K 6건 중 실적 2건 | count 유지. **6-K furnish일 정정**: 2019-08-14(Q2)·2019-11-20(Q3) — 기록된 08-06/11-13은 보도자료일 (도시에 자체 발견 확정) |
| T05/T06 | xbrl | false | false | isXBRL 전건 0 — T06 구기록의 "잘림, 검증 필요" 플래그 해소 |
| T08 MILL | xbrl | false | false | 확정 |
| T13 HTZ | xbrl | true | true | 전신 CIK 제출물에 XBRL 실재 |

### B-3. 폭로일 주변 EDGAR 제출물 실측 (폭로 vehicle 검증)

| ID | 기록된 폭로 vehicle | EDGAR 실측 (±14일) | 판정 |
|---|---|---|---|
| T02 CSC | 8-K 2011-02-01 (사건일 2011-01-28) | 8-K@2011-02-01 실재 | 일치 |
| T04 WFT | 12b-25 (2011-03-01) | **NT 10-K@2011-03-01 + 8-K@2011-03-01** 실재; 10-K@2011-03-08 (First Restatement) | 일치 — vehicle 이중 확인 |
| T05 KEYP | 8-K 2011-04-01 | 8-K@2011-04-01 + NT 10-K@2011-04-01 | 일치 |
| T13 HTZ | 8-K (Item 4.02) 2014-06-06 | 8-K@2014-06-06 실재 | 일치 |
| T16 ICON | Q2-2015 공시 2015-08-10 | NT 10-Q@2015-08-10, 10-Q@2015-08-12 | 일치 (Q2 10-Q 지연 맥락 포함) |
| T17 MRVL | 8-K 2015-09-11 | 8-K@2015-09-11 + NT 10-Q@2015-09-11 | 일치 |
| T19 OSIR | "2015-11-16 8-K" | **그날 8-K 없음 — 10-Q@2015-11-16.** 체인: 8-K@2015-11-06(Q3 실적, 리뷰 최초 공시) → NT 10-Q@2015-11-10 → 10-Q@2015-11-16(정정 반영) → **8-K Item 4.02@2015-11-20** | **정정** (§B-4) |
| T21 SCOR | NT 10-K 2016-02-29 | NT 10-K@2016-02-29 실재 | 일치 |
| T22 TNGO | 8-K Item 4.02 (2016-03-07 제출) | 8-K@2016-03-07 실재 | 일치 |
| T27 WAGE | 3/1 발표 + 3/2 12b-25 | **EDGAR 최초 신호는 NT 10-K@2018-03-02** (3/1은 보도자료, 당일 EDGAR 제출물 없음) | 기록 유지 — 보도자료일 vs 제출일 원칙은 월요일 안건 (§C) |
| T30 LK | Muddy Waters 트윗 2020-01-31 (비EDGAR) | 직전 6-K 2020-01-17, 다음 6-K 2020-02-03(회사 반박) | 일치 (비EDGAR 폭로) |

### B-4. T19 OSIR revelation_source 정정 (객관 — vehicle/URL 오류)

- **구값**: "November 16, 2015 8-K/disclosure … https://www.sec.gov/Archives/edgar/data/1360886/000110465916105218/a16-6447_18k.htm"
- **문제 2건 (EDGAR 실측)**:
  1. 2015-11-16에 8-K는 없다. 그날 제출물은 **Q3 2015 Form 10-Q**(accession 0001558370-15-002707)이고, 정정을 서술한 8-K(Item 4.02)는 **2015-11-20**(accession 0001104659-15-080467).
  2. 인용된 URL(accession 0001104659-**16**-105218)은 **2016-03-15 제출 8-K**(Items 3.01, 4.02, 8.01)로, 기록된 폭로일보다 4개월 뒤 문서.
- **신값**(적용): vehicle을 "Q3 2015 10-Q(2015-11-16 제출, 정정 반영) + 8-K Item 4.02(2015-11-20)"로, URL을 11-20 8-K로 교체.
- **원문 인용** (8-K 2015-11-20, Item 4.02(a)): "As a result of this review, the Company determined to correct the revenue recognition for three contracts, which resulted in a decrease in product revenues of $1.8 million in the first quarter of 2015, a decrease in product revenues of $1.0 million in the second quarter of 2015, an increase in product revenues of $0.8 million in the third quarter of 2015 and a decrease in product revenues of $1.1 million in 2014. … These corrections were reflected in the Third Quarter 2015 Form 10-Q filed with the Securities and Exchange Commission (the 'SEC') on November 16, 2015."
- **판단 의존 잔여 쟁점 → §C**: 더 이른 공개 신호 존재 — 8-K@2015-11-06(Q3 실적 릴리스가 유통계약 회계 리뷰 최초 공시) + NT 10-Q@2015-11-10 ("continuing to review its accounting for a particular contract with a distributor … currently does not expect that this review will have a material impact"). 11-06/11-10/11-16 중 어느 것이 '시장이 처음 알게 된 날'인지는 폭로일 원칙(REVIEW 항목 2)의 적용 대상.

## C. 판단 의존 — 정정하지 않고 월요일 안건에 추가/보강

REVIEW.md 항목 2(폭로일 원칙 + 편입 기준)의 기존 안건에 이번 재검증이 **추가하는 사실**:

1. **T17 MRVL 조작기간 (기존 안건, 근거 고도화)**: 이제 세 가지 창이 원문 문단으로 고정됨 —
   기소 2분기(¶12 Q4FY15 $24M + ¶18 Q1FY16 $64M = $88M) / 사용 3분기(¶10, ¶21 Q2FY16 $77M 포함;
   합 $165M은 산술이지 인쇄 수치 아님) / 명령 자체 Relevant Period "approximately January 2015
   through July 2015"(¶2). 어느 정의를 쓸지 원칙 결정.
2. **T19 OSIR 폭로일 (신규 대안)**: vehicle 정정(§B-4)과 별개로, 더 이른 공개 신호 존재 —
   8-K 2015-11-06(Q3 실적 릴리스가 유통계약 회계 리뷰 최초 공시) → NT 10-Q 2015-11-10("does not
   expect … material impact") → 10-Q 2015-11-16(정정 반영) → 8-K 4.02 2015-11-20. '조사 공시'를
   폭로로 보는 원칙(T02/T12와 동일 축)이면 11-06이 옳을 수 있음.
3. **T13 HTZ 폭로일 (신규 대안)**: 명령 ¶33이 2014-05-13 공개 신호(Q1-2014 10-Q 제출불능 +
   FY2011 정정 가능성 공표)를 서술 — 기록된 2014-06-06(¶34, 비신뢰 결정)보다 3주 이름.
4. **T26 MDXG 폭로일 (기존 안건, 제3 데이터포인트)**: 소장 ¶9는 공개 폭로를 2018-02~07 연쇄로
   서술(-73%). 후보가 2016-12-15(내부고발 소송 보도) / 2017-09-20(공매도 리포트, 현 기록) /
   2018-02(10-K 지연 공시)로 3개가 됨.
5. **T16 ICON aaer_no (편입 기준 안건 직결)**: Clamen 명령(33-10730)에 AAER-4105 인쇄 확인 —
   '임원 단독 AAER' 케이스가 T27 WAGE(4202, Jackson/Callan)와 2건이 됨. 편입 기준을 '피고 기준'으로
   할지 '조작된 재무제표의 발행 주체 기준'으로 할지에 따라 T16의 aaer_no 기입 여부 결정.
   (결정되면 AAER 없는 후보는 5건 → 4건: T22/T24/T26/T30.)
6. **T18 VRX 조작기간 시작의 원칙 의존성**: 2014-07 정정(§A-1)은 '오도 보고 창' 기준. 'scheme
   conduct' 기준이면 2013(Philidor 설립·지원, ¶2/¶8)이 대안. 30건 일관 원칙 필요.
7. **T05 KEYP quarters=2의 전제**: '운영기업 제출물만 집계' 규약 하의 정정. 역합병 일자는 소장에
   월 정밀도뿐(¶14 "In April 2010")이나, 2010-04-19 10-Q가 쉘(Silver Pearl) 명의임은 EDGAR
   formerNames(개명 2010-05-10)와 제출문서 파일명(sp10q33110.htm)으로 객관 확정.
8. **폭로일이 SEC 문서 밖 소스에 의존하는 케이스 (원칙 확정 시 재확인 대상)**: T02(8-K는 EDGAR
   확정, 조사 개시일 자체는 8-K 본문), T03(Citron — SEC 문서 무언급), T05(4/1 8-K — EDGAR 확정),
   T07(2011-06-29 — 원문 미기재), T08(TheStreetSweeper — 원문 무언급), T11(7/29 발표 — 8-K
   7/30 EDGAR 확정), T12(5/21 발표 — 원문 미기재), T15(9/15 8-K — EDGAR 확정), T16(8/10 공시 —
   NT 10-Q 8/10 EDGAR 확정), T24(Prescience — SEC 문서 무언급), T26(§C-4), T28/T29(명령 미서술,
   동시대 시장 소스), T30(Muddy Waters 트윗 — LR은 '연차감사 중 발견'으로 서술).

## D. 한계 (정직 기록)

- **T30 LK 소장 PDF 텍스트 추출 불가**: comp-pr2020-319.pdf는 폰트 인코딩 손상(ToUnicode 부재)으로
  pypdf·PyMuPDF 모두 실패. 모든 수치는 LR-24987 + SEC 보도자료 2020-319(둘 다 sec.gov 1차 발행물)로
  검증 완료(>$300M/>$190M/28%/45%/$180M 전부 축어 확인). 소장 문단 번호 인용만 불가 — 월요일 원문
  대조 시 PDF를 직접 열람할 것(사람 눈으로는 읽힘).
- 명령문이 폭로 사건을 서술하지 않는 케이스(§C-8)의 폭로일은 이번 재검증의 대상 밖(동시대 시장
  소스 기반 유지) — 폭로일 원칙 확정 후 필요 시 개별 8-K 본문 검증.
- 본 결과는 Claude 기반 단일 파이프라인의 수집물 검증에 한정되며, 검증 주체도 채점 보조 Claude다.
  모든 정정의 최종 확정은 인간 서명 사항(PROJECT.md §7).
