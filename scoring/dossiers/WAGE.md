# Dossier T27 — WageWorks, Inc. (WAGE)

> **PENDING HUMAN SIGN-OFF** — 검증용 1차 대조 자료이며 검증된 사실이 아니다.
> 선정: 시드 20260703 고정 무작위 4건 중 1건 (선정 코드: COLLECTION 후 `random.Random(20260703).sample(ids, 4)`).
> 작성: 채점 보조 Claude. AAER 원문은 웹 세션에서 직접 열람 불가였으나(이그레스 차단, 33-10925.pdf 403),
> **2026-07-03 로컬 세션에서 원문 PDF를 직접 취득·전수 대조 완료** — 사본 `~/aaer-data/WAGE/33-10925.pdf`(+`.txt`).
> 아래 "1차 소스 재검증 결과" 및 `data/candidates/reverification_diff.md` 참조. 서명 주체는 여전히 인간.

기록 요약: 폭로일 **2018-03-01** / 컷오프 2018-02-28 / AAER AAER-4202 (2021-02-02) / scheme revenue_recognition

## 필드별 대조 (기록값 ↔ 직접 인용)

### aaer_no + aaer_date  —  판정: supports / 신뢰도: high
- **기록값**: AAER-4202, 2021-02-02
- **인용**: “Washington D.C., Feb. 2, 2021 — The Securities and Exchange Commission today charged Joseph Jackson and Colm Callan, respectively the former CEO and CFO of WageWorks Inc. ... [Release No.] 2021-23”
- **출처**: https://www.sec.gov/newsroom/press-releases/2021-23 (sec_press_release_text)
- **검증 노트**: Date (Feb 2, 2021) and order 33-10925 confirmed; the AAER-4202 serial number itself is NOT printed in the press release/order text — human should confirm '4202' on the SEC AAER index page for release 33-10925.

### respondents (executives-only caveat)  —  판정: supports / 신뢰도: high
- **기록값**: AAER charged the two former executives (Jackson, Callan), NOT WageWorks; company 'caused' to violate, no company penalty
- **인용**: “The SEC's order also finds that Callan and Jackson caused WageWorks to violate the reporting, books and records, and internal accounting controls provisions of the Exchange Act. ... The company wasn't charged with any wrongdoing.”
- **출처**: https://www.sec.gov/newsroom/press-releases/2021-23 ; https://www.cfodive.com/news/wageworks-sec-revenue-recognition-fine/594427/ (sec_press_release_text)
- **검증 노트**: Order caption names only Jackson and Callan as respondents; WageWorks was 'caused' to violate. 'The company wasn't charged with any wrongdoing' is CFO Dive's characterization. Human should verify caption/respondent list and absence of any company penalty on the primary PDF 33-10925.

### manipulation_period_start / end  —  판정: supports / 신뢰도: medium
- **기록값**: 2016-04-01 to 2016-12-31
- **인용**: “The March 1, 2016 contract required WageWorks to undertake development and transition work ... As early as April 2016, the SEC said in an administrative order, Jackson and Callan “were aware of [the client’s] position that it did not intend to pay for” the preparatory work. ... On February 23, 2017, WageWorks reported its financial results for fiscal year 2016 ... Those results improperly recognized more than $3.6 million in revenue related to Base Year 1 of the Contract.”
- **출처**: https://www.cfo.com/news/former-wageworks-cfo-ceo-settle-accounting-case/655828/ ; https://www.sec.gov/files/litigation/admin/2021/33-10925.pdf (Exa highlight, para 21) (secondary_quoting_order)
- **검증 노트**: April 2016 awareness and FY2016 (through Dec 31) revenue recognition align with the recorded window. Human should confirm exact dated paragraphs (client's April/June 2016 non-payment statements and Q2/Q3 amortization) in 33-10925.

### scheme_summary ($3.6M Client A)  —  판정: supports / 신뢰도: high
- **기록값**: False statements to internal accountants and outside auditor re public-sector Client A contract; improper $3.6M 2016 revenue not realizable/collectible; restatement of Q2/Q3/FY2016 filed 2019-03-18
- **인용**: “As a result of these false and misleading statements, WageWorks improperly recognized $3.6 million worth of revenue in 2016 from Client A that was not realizable and for which collectability was not reasonably assured. ... On March 18, 2019, WageWorks restated its year-end financial results for 2016 and its quarter-end financial results for the second and third quarters of 2016. The restated results reversed all revenue from Client A attributable to the Base Year 1 period.”
- **출처**: https://www.sec.gov/files/litigation/admin/2021/33-10925.pdf (Exa highlight, intro + para 45) (secondary_quoting_order)
- **검증 노트**: $3.6M, Client A public-sector, not realizable/collectible, and 2019-03-18 restatement of Q2/Q3/FY2016 all confirmed verbatim from order excerpts. Human should read full order PDF (currently 403 from sec.gov).

### first_revelation_date  —  판정: supports / 신뢰도: high
- **기록값**: 2018-03-01
- **인용**: “On March 1, 2018, WageWorks announced that it would delay filing its annual report on Form 10-K. On the news, shares of WAGE closed at $42.70 per share, down $9.75 per share, or 18.6%, on more than 10-times the stock’s average daily trading volume.”
- **출처**: https://www.einpresswire.com/article/436112192/barrack-rodos-bacine-files-securities-class-action-lawsuit-against-wageworks-inc ; https://www.prnewswire.com/news-releases/shareholder-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-wageworks-inc---wage-300607615.html (news_contemporaneous)
- **검증 노트**: March 1, 2018 10-K delay announcement confirmed by the company's own GlobeNewswire release and two class-action alerts. NOTE: the actual one-day drop was 18.6% ($9.75/share), materially larger than the recorded '>9%' (still technically satisfied since 18.6% > 9%).

### revelation_source  —  판정: supports / 신뢰도: high
- **기록값**: Mar 1-2, 2018: late FY2017 10-K + investigation of revenue recognition on a fiscal-2016 government contract; stock fell >9%
- **인용**: “On March 1, 2018, WageWorks announced ... it is delaying its Annual Report on Form 10-K ... On this news, WageWorks' share price fell $9.75 or over 18% to close at $42.70 per share on March 1, 2018. Then, on March 2, 2018, WageWorks ... concluded it has a material weakness ... its Audit Committee is investigating ... a review of revenue recognition ‘related to the accounting for a government contract during fiscal 2016 and associated issues with whether there was an open flow of information and appropriate tone at the top.’”
- **출처**: https://www.prnewswire.com/news-releases/shareholder-alert-pomerantz-law-firm-investigates-claims-on-behalf-of-investors-of-wageworks-inc---wage-300607615.html ; https://www.sec.gov/Archives/edgar/data/1158863/000119312518068117/d516397dnt10k.htm (Form 12b-25, filed 2018-03-02) (news_contemporaneous)
- **검증 노트**: Both the 10-K delay (3/1) and the government-contract revenue-recognition investigation disclosure (3/2 Form 12b-25) confirmed. Drop was ~18.6%, not ~9%. Human can verify Form 12b-25 language directly on EDGAR.

### pre_revelation_quarters_available  —  판정: supports / 신뢰도: high
- **기록값**: 22
- **인용**: “[data.sec.gov/submissions/CIK0001158863.json — company WAGEWORKS, INC.] Count of forms with filingDate < 2018-03-01: 10-K = 5, 10-Q = 17, total = 22 (earliest 2012-08-09 10-Q, latest 2017-11-08 10-Q); no additional older-filing chunks.”
- **출처**: https://data.sec.gov/submissions/CIK0001158863.json (edgar_api)
- **검증 노트**: Exact match: 5 annual + 17 quarterly periodic reports filed before the 2018-03-01 cutoff = 22. All filings were in the 'recent' array (no supplemental JSON chunks to add).

### xbrl_available  —  판정: supports / 신뢰도: medium
- **기록값**: true
- **인용**: “[data.sec.gov/submissions/CIK0001158863.json] WAGEWORKS, INC. filings begin 2012-08-09 (first 10-Q); all periodic reports post-IPO fall in the mandatory-XBRL era (SEC phased-in requirement complete by FY2011).”
- **출처**: https://data.sec.gov/submissions/CIK0001158863.json (edgar_api)
- **검증 노트**: WageWorks IPO'd May 2012; all 10-K/10-Q from 2012 onward carry XBRL exhibits under the SEC interactive-data mandate. Human can confirm by checking Financial Report / R-files (or /companyfacts/CIK0001158863.json) for a 2012-2017 10-K.

## 발견된 불일치/뉘앙스 (검증 우선순위)
- revelation_source / first_revelation_date magnitude: recorded 'stock fell >9%'; contemporaneous class-action alerts (Barrack Rodos & Bacine, Pomerantz) state the March 1, 2018 one-day decline was $9.75/share = 18.6% (close $42.70 from $52.45). Not a contradiction of '>9%' but the recorded figure appears to have transcribed the $9.75/share dollar amount as a '~9%' percentage; true magnitude was ~18.6%.

## 1차 소스 재검증 결과 (2026-07-03 로컬 세션 — 원문 PDF 직접 대조)

1. **도시에 가설 뒤집힘 — '>9%'는 오전사가 아니었다.** 명령문 ¶44 원문: "On March 1 and 2, 2018,
   WageWorks announced that it would be late in filing its fiscal-year 2017 Form 10-K and that it was
   conducting an investigation into revenue recognition related to the accounting for a government
   contract during fiscal 2016. **WageWorks's stock price declined more than 9% on the news.**"
   → 기록의 '>9%'는 **SEC 명령문 자체의 표현**. 2차 소스(집단소송 alert)의 -$9.75/-18.6%($52.45→$42.70)와
   병존하는 별개 서술이며, 둘 다 candidates.json notes에 기재함. 이 도시에의 "발견된 불일치" 1번 항목은
   '기록 오류' 가설로는 **기각**, '명령문 표현이 실제 하락폭을 과소 서술' 관찰로는 유효 — 어느 쪽을
   기록 기준으로 삼을지도 서명 사항.
2. 명령 캡션 확정: respondents는 **Jackson과 Callan뿐**, WageWorks는 "Other Relevant Entities"(¶4).
3. $3.6M Client A: ¶1 "WageWorks improperly recognized $3.6 million worth of revenue in 2016 from
   Client A that was not realizable and for which collectability was not reasonably assured." + ¶21.
4. 정정 공시: ¶45 "On March 18, 2019, WageWorks restated its year-end financial results for 2016 and
   its quarter-end financial results for the second and third quarters of 2016." — 확정.
5. **기간 뉘앙스(신규)**: ¶8 — Client A의 미지급 입장 인지는 **2016-03-29** ("On March 29, in reply,
   a Client A employee indicated that Client A would not pay WageWorks for Base Year 1"), 기록된 시작
   2016-04-01보다 사흘 이름; 수익 인식 개시는 2016-06(¶11). 계약 체결 2016-03-01(¶5) 확정.
6. AAER-4202 / 2021-02-02 헤더 인쇄 확정. pre_revelation_quarters_available 22 — EDGAR 재계산 완전 일치.

## 인간 검증 포인터 (원문 사본 로컬 보유 — 월요일 대조는 아래 로컬 파일/페이지로)
- https://www.sec.gov/files/litigation/admin/2021/33-10925.pdf — primary SEC order/AAER-4202 (Order Instituting Proceedings), currently 403 from sec.gov; confirm respondent caption (Jackson & Callan only), the $3.6M/Client A findings, dated April/June 2016 non-payment statements, and 2019-03-18 restatement paragraph (para 45).
- https://www.sec.gov/Archives/edgar/data/1158863/000119312518068117/d516397dnt10k.htm — WageWorks Form 12b-25 (NT 10-K) filed 2018-03-02, signed by CFO Colm Callan; primary source for the government-contract revenue-recognition investigation disclosure.
- https://www.sec.gov/Archives/edgar/data/1158863/000119312518108845/d564686d8k.htm — WageWorks 8-K (non-reliance / restatement scope: Q2 & Q3 2016, FY2016, Q1-Q3 2017) for restatement-period confirmation.
- https://data.sec.gov/api/xbrl/companyfacts/CIK0001158863.json — to affirmatively confirm XBRL structured financial data availability.
- https://www.wageworkssettlement.com/home/100028/DocumentHandler?docPath=%2FDocuments%2F130_Order.pdf — securities class-action court order (MPERS/GERS v. WageWorks) corroborating the $52.45→$42.70 price move and the fiscal-2016 government (OPM) contract facts.

## 학습 노트 (§10)
AAER의 명목 피고가 임원뿐이어도 사건의 실체는 발행사 재무제표 조작일 수 있다 — 검증할 것: '발행사 AAER' 기준의 문언(피고 기준인가, 조작된 재무제표의 발행 주체 기준인가).
