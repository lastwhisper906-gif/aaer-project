# Dossier T17 — Marvell Technology Group, Ltd. (MRVL)

> **PENDING HUMAN SIGN-OFF** — 검증용 1차 대조 자료이며 검증된 사실이 아니다.
> 선정: 시드 20260703 고정 무작위 4건 중 1건 (선정 코드: COLLECTION 후 `random.Random(20260703).sample(ids, 4)`).
> 작성: 채점 보조 Claude. AAER 원문은 웹 세션에서 직접 열람 불가였으나(이그레스 차단),
> **2026-07-03 로컬 세션에서 원문 PDF를 직접 취득·전수 대조 완료** — 사본 `~/aaer-data/MRVL/33-10684.pdf`(+`.txt`).
> 아래 "1차 소스 재검증 결과" 및 `data/candidates/reverification_diff.md` 참조. 서명 주체는 여전히 인간.

기록 요약: 폭로일 **2015-09-11** / 컷오프 2015-09-10 / AAER AAER-4076 (2019-09-16) / scheme revenue_recognition, disclosure_only

## 필드별 대조 (기록값 ↔ 직접 인용)

### aaer_no  —  판정: supports / 신뢰도: high
- **기록값**: AAER-4076
- **인용**: “AAER 4076 ... 33-10684 16-Sep-2019 Administrative Proceeding Order Instituting Cease-and-Desist Proceedings Pursuant to Section 8A of the Securities Act of 1933 and Section 21C of the Securities Exchange Act of 1934, Making Findings and Imposing a Cease-and-Desist Order”
- **출처**: https://research.seed.law.nyu.edu/Search/ActionDetail/3133/5038 (database)
- **검증 노트**: NYU SEED explicitly ties AAER 4076 to order 33-10684 / File No. 3-19454; human should confirm the AAER number on the AAER index page at sec.gov.

### aaer_date  —  판정: supports / 신뢰도: high
- **기록값**: 2019-09-16
- **인용**: “Washington D.C., Sept. 16, 2019 — The Securities and Exchange Commission today announced that Marvell Technology Group, Ltd. will pay $5.5 million to settle charges ... On September 16, 2019, the SEC instituted settled cease-and-desist proceedings against Marvell Technology Group, Ltd.”
- **출처**: https://www.sec.gov/newsroom/press-releases/2019-175 (sec_press_release_text)
- **검증 노트**: Order date confirmed 16-Sep-2019 by both SEC press release 2019-175 and SEED; human should verify the order caption date on 33-10684.pdf.

### manipulation_period (fiscal quarters of pull-ins)  —  판정: supports / 신뢰도: high
- **기록값**: 2014-11 to 2015-05; ~$24M Q4 FY2015 and ~$64M Q1 FY2016
- **인용**: “the purpose of the pull-in sales, which took place during the fourth quarter of 2015 and first quarter of 2016, was to close the gap between actual and forecasted revenue and to meet publicly-issued revenue guidance. The pull-ins for these quarters amounted to $24 million and $64 million of the total quarterly revenues, or 5% and 16% of revenue in its key storage segment, respectively.”
- **출처**: https://www.sec.gov/newsroom/press-releases/2019-175 (sec_press_release_text)
- **검증 노트**: Charged pull-in quarters are Q4 FY2015 (~Nov 2014-Jan 2015) and Q1 FY2016 (~Feb-May 2015), matching recorded window; the $24M and $64M figures are exactly confirmed. NOTE: order/investigation language also references Q2 FY2016 as investigated (see discrepancy), so a human should check paragraphs on affected quarters in 33-10684.pdf for the precise charged vs. investigated distinction.

### scheme_summary  —  판정: supports / 신뢰도: high
- **기록값**: Undisclosed 'pull-in' revenue-management scheme accelerating sales into current quarter to close gap to guidance and mask declining demand; concealed from board and auditor; no restatement; $5.5M penalty
- **인용**: “This matter concerns an undisclosed revenue management scheme by Marvell Technology Group. Faced with a substantial decline in customer demand in its core product markets, and concerned about the adverse consequences that would result from missing its public guidance, Marvell orchestrated a plan to accelerate, or pull-in, sales that had originally been scheduled for future quarters to the current quarter in order to close the gap between actual and forecasted revenue, meet publicly-issued guidance, and mask declining sales.”
- **출처**: https://www.sec.gov/files/litigation/admin/2019/33-10684.pdf (secondary_quoting_order)
- **검증 노트**: Order paragraph 1 quoted verbatim (retrieved via Exa highlight of the PDF and corroborated word-for-word by NYU SEED). Concealment from Board/auditor confirmed by order para 22/37 ('Marvell's senior management also failed to inform ... Board of Directors or its independent auditor of its pull-in scheme'); Debevoise confirms SEC did NOT allege GAAP/revenue-recognition violation (no restatement) — human should confirm 'no restatement' by checking that the order alleges only disclosure/MD&A violations.

### first_revelation_date  —  판정: supports / 신뢰도: high
- **기록값**: 2015-09-11
- **인용**: “On September 11, 2015, Marvell announced a delay in filing its Form 10-Q for Q2 FY2016 and the commencement of an internal investigation to examine, among other things, the company's use of pull-ins. Shortly thereafter, Marvell's independent auditor resigned.”
- **출처**: https://www.sec.gov/files/litigation/admin/2019/33-10684.pdf (secondary_quoting_order)
- **검증 노트**: Order para 22 fixes the Sept 11, 2015 revelation. Contemporaneously corroborated by 24/7 Wall St (Sept 11, 2015: 'the board's audit committee is conducting an independent investigation of certain accounting and internal control matters ... sent the stock down about 22%') — human can cross-check the 8-K filed 9/11/2015 (accession 0001193125-15-317843).

### revelation_source  —  판정: supports / 신뢰도: high
- **기록값**: Sept 11, 2015 8-K/press release: Audit Committee announced independent investigation of revenue-recognition and internal-control matters and delayed the Q2 fiscal-2016 10-Q
- **인용**: “The Company also announced that the Audit Committee of the Company's Board of Directors is conducting an independent investigation of certain accounting and internal control matters in the second quarter of fiscal 2016. ... the investigation has focused on the approximately 7 to 8 percent of revenue recognized in the second quarter of fiscal 2016 that, based upon the original customer request date, would have been received and earned in the third quarter of fiscal 2016 and is now no longer available for receipt in that quarter. ... For these reasons the Company has experienced a delay in the completion of its financial statements, Management's Discussion and Analysis of Financial Condition and Results of Operations and other related components of the Quarterly Report.”
- **출처**: https://www.sec.gov/Archives/edgar/data/1058057/000119312515317843/d10775dex991.htm (news_contemporaneous)
- **검증 노트**: Sept 11, 2015 press release (Ex-99.1 to the 8-K) and the NT 10-Q both confirm the audit-committee investigation of revenue-recognition/internal-control matters plus the 10-Q delay; retrieved via Exa (Marvell investor site + EDGAR archive text). Human should open the 8-K at accession 0001193125-15-317843 and NT 10-Q at 0001193125-15-317840.

### pre_revelation_quarters_available  —  판정: not_found / 신뢰도: medium
- **기록값**: null
- **인용**: “{"start":"2009-02-01","end":"2009-05-02","val":521434000,"accn":"0001193125-10-134950","fy":2010,"fp":"Q1","form":"10-Q" ... } (Revenues concept populated for numerous consecutive 10-Q/10-K periods from FY2009 through pre-2015)”
- **출처**: https://data.sec.gov/api/xbrl/companyconcept/CIK0001058057/us-gaap/Revenues.json (edgar_api)
- **검증 노트**: Recorded null is acceptable; EDGAR XBRL shows continuous quarterly Revenues data from FY2009 onward, so many (>20) pre-revelation quarters of financials exist. Human should count 10-Q/10-K filings prior to 2015-09-11 in the submissions JSON (filings.recent + filings.files older-archive) to derive an exact number.

### xbrl_available  —  판정: supports / 신뢰도: high
- **기록값**: true
- **인용**: “{"cik":1058057,"taxonomy":"us-gaap","tag":"Revenues","label":"Revenues", ... "units":{"USD":[{"start":"2007-01-28","end":"2008-02-02","val":2894693000,"accn":"0001193125-10-073247","fy":2009,"fp":"FY","form":"10-K", ... }”
- **출처**: https://data.sec.gov/api/xbrl/companyconcept/CIK0001058057/us-gaap/Revenues.json (edgar_api)
- **검증 노트**: data.sec.gov companyconcept API returns populated XBRL facts for CIK 0001058057 across many periods, confirming XBRL is available; human can also load companyfacts.json for the full frame set.

## 발견된 불일치/뉘앙스 (검증 우선순위)
- Scope-of-quarters nuance (not a contradiction of the recorded charged period, but worth a human check): Debevoise states 'Marvell pulled in a total of $165 million in revenues across three quarters' and the Nov-2015 8-K (d100954dex991.htm) says the audit-committee revenue review 'has focused on and has been limited to revenue recognized in the first and second quarters of fiscal 2016 and the fourth quarter of fiscal 2015' — i.e., THREE quarters (adds Q2 FY2016, ending Aug 1 2015). The SEC's charged/disclosed pull-in figures, however, cover only TWO quarters: Q4 FY2015 ($24M) and Q1 FY2016 ($64M) = $88M. The recorded manipulation_period_end of 2015-05 captures the two charged quarters but not the Q2 FY2016 investigated quarter; confirm whether the record intends 'charged' vs 'investigated' scope.

## 1차 소스 재검증 결과 (2026-07-03 로컬 세션 — 원문 PDF 직접 대조)

핵심 쟁점(기소 범위 vs 조사 범위)을 원문 문단 번호로 고정 — **판정은 하지 않음, 월요일 원칙 결정 사항**:

1. **기소(charged) 2개 분기 — 원문 확정.** ¶1: "materially misleading public statements … regarding its financial results for the fourth quarter of fiscal year 2015 (Q4 FY2015) and first quarter of fiscal year 2016 (Q1 FY2016)." ¶12: "In Marvell's **Q4 FY2015, which ended January 31, 2015**, Marvell pulled-in **$24 million** of sales originally scheduled for future quarters, of which $20 million came from the storage segment." ¶18: "In Marvell's **Q1 FY2016, which ended May 2, 2015**, Marvell pulled-in **$64 million** of sales scheduled for future quarters, of which $55 million came from the storage segment." 위반 조항 문단(¶40–41)도 FY2015 10-K와 Q1 FY2016 10-Q만 지목.
2. **풀인 사용 3개 분기 — 원문 확정 (기소와 별개 사실).** ¶10: "Marvell used pull-ins in the following **three quarters**:" ¶21: "In Marvell's **Q2 FY2016, which ended August 1, 2015**, Marvell pulled-in a record amount of **$77 million** … The pull-ins totaled 11% of total revenue for the quarter."
3. **주의: '$165M'은 원문에 인쇄된 수치가 아님** — ¶12($24M)+¶18($64M)+¶21($77M)의 산술 합. 2차 소스(Debevoise)의 "~$165M across three quarters"는 이 합산을 지칭.
4. **원문의 자체 정의 기간**: ¶2 "From approximately **January 2015 through July 2015** (the 'Relevant Period')" — 기록된 2014-11~2015-05(기소 2개 분기의 달력 스팬)와도, 조사 3개 분기 스팬과도 다른 제3의 창. 조작기간 확정 시 세 가지 중 어느 정의를 쓸지 원칙 필요.
5. 폭로일 ¶22 확정: "On September 11, 2015, Marvell announced a delay in filing its Form 10-Q for Q2 FY2016 and the commencement of an internal investigation … Shortly thereafter, Marvell's independent auditor resigned." 이사회/감사인 은폐 ¶37, 벌금 $5.5M(IV.B), AAER-4076/2019-09-16 헤더 — 전부 원문 확정.
6. pre_revelation_quarters_available null → **60** 채움 (EDGAR 제출 이력 실측; 구추정 ~59에 근사).

## 인간 검증 포인터 (원문 사본 로컬 보유 — 월요일 대조는 아래 로컬 파일/페이지로)
- https://www.sec.gov/files/litigation/admin/2019/33-10684.pdf — primary SEC order/AAER-4076; verify order caption date (9/16/2019), paras 1 (scheme), 22 (Sept 11 2015 revelation + auditor resignation), 37 (concealment from Board/auditor), 41 (Reg S-K Item 303 / Section 13(a)), penalty section ($5,500,000), and the exact affected-quarter language ($24M Q4 FY2015 / $64M Q1 FY2016).
- https://www.sec.gov/newsroom/press-releases/2019-175 — SEC press release full text (Bandy quote; $24M/$64M; 5%/16% storage segment).
- https://www.sec.gov/Archives/edgar/data/1058057/000119312515317843/d10775d8k.htm — 8-K dated 9/11/2015 with Ex-99.1 press release (revelation source).
- https://www.sec.gov/Archives/edgar/data/1058057/000119312515317840/d64331dnt10q.htm — NT 10-Q (notification of late Q2 FY2016 10-Q filing).
- https://www.sec.gov/Archives/edgar/data/1058057/000119312515395976/d100954dex991.htm — later 2015 8-K exhibit describing the investigation scope as Q4 FY2015 + Q1 & Q2 FY2016 (three-quarter review) and SEC/US Attorney contact.
- https://data.sec.gov/submissions/CIK0001058057.json (+ older-archive entries under filings.files) — to count exact pre-2015-09-11 10-Q/10-K filings for pre_revelation_quarters_available.
- https://data.sec.gov/api/xbrl/companyfacts/CIK0001058057.json — full XBRL fact set to confirm xbrl_available and period coverage.

## 학습 노트 (§10)
SEC가 '기소한' 분기와 감사위가 '조사한' 분기는 다를 수 있다 — 검증할 것: 조작기간을 기소 범위(Q4FY15+Q1FY16, $88M)로 잡을지 조사 범위(Q2FY16 포함 3개 분기, ~$165M)로 잡을지의 원칙.
