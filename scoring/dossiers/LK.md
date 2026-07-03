# Dossier T30 — Luckin Coffee Inc. (LK)

> **PENDING HUMAN SIGN-OFF** — 검증용 1차 대조 자료이며 검증된 사실이 아니다.
> 선정: 시드 20260703 고정 무작위 4건 중 1건 (선정 코드: COLLECTION 후 `random.Random(20260703).sample(ids, 4)`).
> 작성: 채점 보조 Claude. SEC 원문은 웹 세션에서 직접 열람 불가였으나(이그레스 차단),
> **2026-07-03 로컬 세션에서 LR-24987·보도자료 2020-319·소장 PDF·EDGAR 제출 이력을 직접 취득·대조 완료**
> — 사본 `~/aaer-data/LK/`. 아래 "1차 소스 재검증 결과" 및 `data/candidates/reverification_diff.md` 참조.
> 서명 주체는 여전히 인간.

기록 요약: 폭로일 **2020-01-31** / 컷오프 2020-01-30 / AAER 없음(민사소송) (-) / scheme revenue_recognition, related_party, document_forgery

## 필드별 대조 (기록값 ↔ 직접 인용)

### aaer_no (no-AAER status)  —  판정: supports / 신뢰도: high
- **기록값**: null (no AAER; SEC action is federal civil suit LR-24987)
- **인용**: “Litigation Release No. 24987 / December 16, 2020 ... Securities and Exchange Commission v. Luckin Coffee Inc., No. 1:20-cv-10631 (S.D.N.Y. filed Dec. 16, 2020) ... The SEC's complaint, filed today in the Southern District of New York, charges Luckin with violating the antifraud provisions of Section 17(a) of the Securities Act of 1933 and Section 10(b) of the Securities Exchange Act of 1934 and Rule 10b-5 thereunder.”
- **출처**: https://www.sec.gov/enforcement-litigation/litigation-releases/lr-24987 (sec_press_release_text)
- **검증 노트**: Action is a Litigation Release (federal civil complaint in SDNY, case 1:20-cv-10631), not an administrative proceeding; consistent with aaer_no=null. Human should confirm no corresponding entry exists in the SEC AAER index for Luckin.

### manipulation_period_start / manipulation_period_end  —  판정: supports / 신뢰도: high
- **기록값**: 2019-04-01 to 2020-01-31
- **인용**: “The SEC's complaint alleges that, from at least April 2019 through January 2020, Luckin intentionally fabricated more than $300 million in retail sales by using related parties to create false sales transactions through three separate purchasing schemes.”
- **출처**: https://www.sec.gov/newsroom/press-releases/2020-319 (sec_press_release_text)
- **검증 노트**: SEC frames period as 'from at least April 2019 through January 2020'; recorded start/end (Apr 1 2019 / Jan 31 2020) are the month boundaries. Human should verify exact dates in the complaint (SDNY 1:20-cv-10631).

### scheme_summary — fabricated retail sales (RMB2.12B / ~$300-311M) via related parties, three purchasing schemes  —  판정: supports / 신뢰도: high
- **기록값**: >RMB2.12B (~$311M) fabricated retail sales using related parties through three purchasing schemes
- **인용**: “The SEC's complaint alleges that, from at least April 2019 through January 2020, Luckin intentionally fabricated more than $300 million in retail sales by using related parties to create false sales transactions through three separate purchasing schemes. ... [Luckin internal investigation:] the Company's net revenue in 2019 was inflated by approximately RMB 2.12 billion (consisting of RMB 0.25 billion in the second quarter, RMB 0.70 billion in the third quarter, and RMB 1.17 billion in the fourth quarter.)”
- **출처**: https://www.sec.gov/newsroom/press-releases/2020-319 ; https://www.sec.gov/Archives/edgar/data/1767582/000110465920079446/a20-23914_1ex99d1.htm (sec_press_release_text)
- **검증 노트**: SEC quantifies fabricated retail sales as '>$300 million'; the RMB2.12 billion figure is from Luckin's own July 1 2020 Special Committee disclosure of 2019 net-revenue inflation. Both figures corroborate the recorded value (~$311M ≈ RMB2.12B). Human should cross-check the complaint's dollar figure vs internal-investigation RMB figure.

### scheme_summary — inflated expenses >$190M, fake operations database, altered records  —  판정: supports / 신뢰도: high
- **기록값**: inflated expenses by >$190M, created a fake operations database, and altered accounting/bank records
- **인용**: “According to the complaint, certain Luckin employees attempted to conceal the fraud by inflating the company's expenses by more than $190 million, creating a fake operations database, and altering accounting and bank records to reflect the false sales.”
- **출처**: https://www.sec.gov/newsroom/press-releases/2020-319 (sec_press_release_text)
- **검증 노트**: Verbatim match to recorded expense-inflation (>$190M), fake operations database, and altered accounting/bank records. Human should confirm exact expense figure in complaint.

### scheme_summary — overstatement ~28% (period ended 6/30/19) and ~45% (period ended 9/30/19)  —  판정: supports / 신뢰도: high
- **기록값**: overstated 2019 revenue ~28% (period ended 6/30/19) and ~45% (period ended 9/30/19)
- **인용**: “For example, Luckin allegedly materially overstated its reported revenue by approximately 28% for the period ending June 30, 2019, and by 45% for the period ending Sept. 30, 2019, in its publicly disclosed financial statements.”
- **출처**: https://www.sec.gov/newsroom/press-releases/2020-319 (sec_press_release_text)
- **검증 노트**: Direct match to both overstatement percentages and period-end dates. Human should verify these appear identically in the complaint body.

### first_revelation_date  —  판정: supports / 신뢰도: high
- **기록값**: 2020-01-31
- **인용**: “Published 01/31/2020, 11:38 AM ... Chinese coffee chain Luckin Coffee (NASDAQ: LK) plunged midday Friday after a prominent short-seller announced a position in the company. Shares of Luckin sank 12%. Muddy Waters Research tweeted that it is short the stock, saying: 'We received unattributed 89-page report alleging $LK is a fraud: number of items per store per day was inflated by at least 69% in 2019 3Q and 88% in 2019 4Q, supported by 11,260 hours of store traffic video. We view the work as credible.'”
- **출처**: https://www.investing.com/news/stock-market-news/luckin-coffee-sinks-after-short-position-revealed-2073168 (news_contemporaneous)
- **검증 노트**: Contemporaneous (timestamped Jan 31 2020, 11:38 AM ET) report of the Muddy Waters tweet and same-day stock drop. Corroborated by Motley Fool (Jan 31 2020) 'down 14.5%... as much as 26.5% earlier' and Bloomberg Law 'sank as much as 27%' same day.

### revelation_source  —  판정: supports / 신뢰도: high
- **기록값**: Jan 31, 2020 Muddy Waters tweet publicizing an unattributed 89-page short-seller report alleging fabricated sales volumes
- **인용**: “Luckin Coffee Inc. sank as much as 27% on Friday when Muddy Waters Capital tweeted that it has a short on the stock after it received an unattributed 89-page report that alleges accounting issues and a broken business model. ... Muddy Waters, founded by Carson Block, said that while the report was written by an anonymous author, the work appears 'credible.'”
- **출처**: https://news.bloomberglaw.com/esg/citron-muddy-waters-clash-on-twitter-over-chinese-coffee-chain (news_contemporaneous)
- **검증 노트**: Confirms revelation vehicle = Muddy Waters (Carson Block) tweet publicizing an unattributed/anonymous 89-page report. The Wire China ('The Big China Short') further confirms Block tweeted the report to 90,000 followers on Jan 31 and 'the stock immediately tumbled 27 percent.'

### later confirmation event — Apr 2 2020 self-disclosure  —  판정: supports / 신뢰도: high
- **기록값**: Apr 2 2020 self-disclosure (~RMB2.2B / $310M fabricated sales by COO)
- **인용**: “Luckin Coffee disclosed Thursday that an internal investigation has found that its chief operating officer fabricated 2019 sales by about 2.2 billion yuan ($310 million). Shares cratered more than 80% in premarket trading after the release of the regulatory filing. ... The investigation found that Jian Liu, Luckin's chief operating officer, and several employees who reported to him, had engaged in misconduct, including fabricating sales.”
- **출처**: https://www.cnbc.com/2020/04/02/luckin-coffee-stock-plummets-after-investigation-finds-coo-fabricated-sales.html (news_contemporaneous)
- **검증 노트**: Confirms Apr 2 2020 company self-disclosure of ~RMB2.2B/$310M fabricated sales as the later confirming event, distinct from the Jan 31 2020 first revelation. Consistent with SEC PR crediting self-reporting.

### pre_revelation_quarters_available  —  판정: supports / 신뢰도: high
- **기록값**: 2
- **인용**: “6-K ... Report of foreign issuer [Rules 13a-16 and 15d-16] ... Size: 549 KB | 2019-11-20 ... 6-K ... Report of foreign issuer ... Size: 536 KB | 2019-08-14 (EDGAR filing list, CIK 0001767582, type=6-K, prior to 20200131)”
- **출처**: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001767582&type=6-K&dateb=20200131&owner=include&count=40 (fetched via Exa; data.sec.gov submissions CIK0001767582.json) (edgar_api)
- **검증 노트**: Only two substantive (500KB+) quarterly-earnings 6-Ks precede the Jan 31 2020 revelation: Q2 2019 furnished 2019-08-14 and Q3 2019 furnished 2019-11-20 (the small 43-47KB Jan 2020 6-Ks are non-earnings). DISCREPANCY: recorded caveat lists filing dates 2019-08-06 and 2019-11-13, but EDGAR shows the earnings 6-Ks furnished 2019-08-14 and 2019-11-20 (Aug 6 / Nov 13 are likely the press-release/announcement dates). Count of 2 quarters is correct; human should reconcile the exact furnishing dates.

### xbrl_available  —  판정: supports / 신뢰도: medium
- **기록값**: false
- **인용**: “6-K ... Report of foreign issuer [Rules 13a-16 and 15d-16] ... (all pre-revelation quarterly financials furnished as 6-K by a foreign private issuer; entityType 'other', stateOfIncorporation 'E9' Cayman Islands, tickers ['LKNCY'], exchanges ['OTC'])”
- **출처**: https://data.sec.gov/submissions/CIK0001767582.json (edgar_api)
- **검증 노트**: Luckin is a foreign private issuer that furnished 2019 quarterly financials on Form 6-K (not 10-Q/20-F financial-statement XBRL); FPI 6-K earnings furnishings are not XBRL-tagged, consistent with xbrl_available=false. Human should confirm no XBRL financial data exists for the pre-revelation 6-Ks on the EDGAR filing index.

### penalty / settlement (context for LR-24987)  —  판정: supports / 신뢰도: high
- **기록값**: $180M penalty, SEC v. Luckin, SDNY, Dec 16 2020
- **인용**: “Luckin, whose American Depositary Shares traded on Nasdaq until July 13, 2020, has agreed to pay a $180 million penalty to resolve the charges. ... Without admitting or denying the allegations, Luckin has agreed to a settlement, subject to court approval, that includes permanent injunctions and the payment of a $180 million penalty.”
- **출처**: https://www.sec.gov/newsroom/press-releases/2020-319 (sec_press_release_text)
- **검증 노트**: Confirms $180M penalty and Dec 16 2020 SDNY settlement matching LR-24987. Corroborated by CNBC (2020-12-17) and Luckin's own Dec 16 2020 8-K exhibit.

## 발견된 불일치/뉘앙스 (검증 우선순위)
- pre_revelation_quarters_available: recorded caveat cites 6-K furnishing dates of 2019-08-06 (Q2) and 2019-11-13 (Q3), but EDGAR shows the substantive quarterly-earnings 6-Ks furnished 2019-08-14 and 2019-11-20 (the Aug 6 / Nov 13 dates appear to be the earnings press-release dates, not the EDGAR furnishing dates). Quote: '6-K ... Size: 536 KB | 2019-08-14' and '6-K ... Size: 549 KB | 2019-11-20'. The COUNT (2) is not contradicted; only the exact dates differ.
- scheme_summary dollar figure: recorded value says fabricated retail sales '>RMB2.12B (~$311M)'; SEC press release/complaint states 'more than $300 million in retail sales' (the RMB2.12B is Luckin's own internal-investigation net-revenue-inflation figure, not the SEC's retail-sales figure). Not a true contradiction but the two figures come from different documents and measure slightly different things — a human should confirm which figure the record intends.

## 1차 소스 재검증 결과 (2026-07-03 로컬 세션 — 원문 직접 대조)

1. **6-K furnish일 — 도시에 발견 확정, candidates.json notes 정정 반영.** EDGAR 제출 이력(data.sec.gov,
   CIK 0001767582) 실측: Q2 2019 6-K **2019-08-14** (accession 0001104659-19-045718), Q3 2019 6-K
   **2019-11-20** (accession 0001104659-19-065621). 구기록의 08-06/11-13은 보도자료일. 폭로 전 6-K는
   총 6건(실적 2 + 2020-01 비실적 4) — count 2 유지.
2. **RMB2.12B vs >$300M — 도시에 발견 확정, scheme_summary 정정 반영.** LR-24987/PR 2020-319 원문:
   "intentionally fabricated **more than $300 million** in retail sales … inflating the company's
   expenses by **more than $190 million** … overstated its reported revenue by approximately **28%**
   for the period ending June 30, 2019, and by **45%** for the period ending September 30, 2019."
   RMB2.12B는 Luckin 2020-07-01 특별위 공시의 '2019 순매출 과대계상' 수치로 측정 대상이 다름 —
   scheme_summary를 SEC 수치 주도 + RMB 병기로 재작성.
3. no-AAER 확정: LR-24987 페이지에 AAER 줄 무인쇄 (T22/T24/T26과 동일 패턴 — LR-only 케이스도
   AAER이 인쇄되는 경우(T19 OSIR)가 있으므로 페이지 확인이 유일한 판별법).
4. $180M 벌금, "from at least April 2019 through January 2020" 기간, 관련당사자 3개 구매 스킴 — 전부
   LR/PR 원문 축어 확정.
5. **한계**: 소장 PDF(comp-pr2020-319.pdf, 1.25MB)는 폰트 인코딩 손상으로 기계 추출 불가(pypdf·PyMuPDF
   모두 실패). 수치 검증은 LR+PR로 완료했으나 소장 문단 번호 인용은 불가 — 월요일 원문 대조 시 PDF를
   사람 눈으로 직접 열람할 것 (로컬 사본 있음).

## 인간 검증 포인터 (원문 사본 로컬 보유 — 월요일 대조는 아래 로컬 파일/페이지로)
- SEC complaint PDF (primary, for exact April 2019–January 2020 dates, >$300M / >$190M figures, 28%/45% overstatements): https://www.sec.gov/files/litigation/complaints/2020/comp-pr2020-319.pdf
- SEC Litigation Release LR-24987 (civil action, confirms no-AAER status): https://www.sec.gov/enforcement-litigation/litigation-releases/lr-24987
- SEC Press Release 2020-319: https://www.sec.gov/newsroom/press-releases/2020-319
- Luckin July 1 2020 Special Committee update (RMB2.12B net-revenue inflation, RMB1.34B expense inflation, per-quarter breakdown): https://www.sec.gov/Archives/edgar/data/1767582/000110465920079446/a20-23914_1ex99d1.htm
- Luckin Feb 3 2020 6-K response to the anonymous report (confirms report 'made public on January 31, 2020'): https://www.sec.gov/Archives/edgar/data/1767582/000110465920009486/a20-6511_1ex99d1.htm
- EDGAR 6-K filing list before 2020-01-31 (confirms the two pre-revelation quarterly-earnings 6-Ks): https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001767582&type=6-K&dateb=20200131&owner=include&count=40
- data.sec.gov submissions JSON (FPI status, CIK, ticker LKNCY, forms/dates arrays for XBRL and quarter-count verification): https://data.sec.gov/submissions/CIK0001767582.json
- Human with sec.gov access should confirm absence of any AAER number tied to Luckin in the SEC AAER index and verify the complaint's exact manipulation-period dates.

## 학습 노트 (§10)
AAER 부재는 '회계부정 아님'이 아니라 SEC의 절차 선택(민사소송)일 수 있다 — 검증할 것: 편입 기준을 'AAER 보유'로 유지할지 'SEC 회계부정 집행조치'로 넓힐지 (T16/T22/T24/T26도 같은 축).
