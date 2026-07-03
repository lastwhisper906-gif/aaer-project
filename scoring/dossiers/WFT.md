# Dossier T04 — Weatherford International Ltd. (Switzerland); n/k/a Weatherford International plc (WFT)

> **PENDING HUMAN SIGN-OFF** — 검증용 1차 대조 자료이며 검증된 사실이 아니다.
> 선정: 시드 20260703 고정 무작위 4건 중 1건 (선정 코드: COLLECTION 후 `random.Random(20260703).sample(ids, 4)`).
> 작성: 채점 보조 Claude. AAER 원문은 웹 세션에서 직접 열람 불가였으나(이그레스 차단),
> **2026-07-03 로컬 세션에서 원문 PDF를 직접 취득·전수 대조 완료** — 사본 `~/aaer-data/WFT/33-10221.pdf`(+`.txt`).
> 아래 "1차 소스 재검증 결과" 및 `data/candidates/reverification_diff.md` 참조. 서명 주체는 여전히 인간.

기록 요약: 폭로일 **2011-03-01** / 컷오프 2011-02-28 / AAER AAER-3806 (2016-09-27) / scheme liability_understatement, asset_overstatement

## 필드별 대조 (기록값 ↔ 직접 인용)

### aaer_no + aaer_date  —  판정: supports / 신뢰도: high
- **기록값**: AAER-3806, 2016-09-27
- **인용**: “SECURITIES ACT OF 1933 Release No. 10221 / September 27, 2016 SECURITIES EXCHANGE ACT OF 1934 Release No. 78944 / September 27, 2016 ACCOUNTING AND AUDITING ENFORCEMENT Release No. 3806 / September 27, 2016 ADMINISTRATIVE PROCEEDING File No. 3-17582”
- **출처**: https://www.sec.gov/files/litigation/admin/2016/33-10221.pdf (sec_press_release_text)
- **검증 노트**: Order header (fetched via Exa) confirms AAER Rel. No. 3806 dated Sept 27, 2016, tied to Securities Act Rel. 10221; human should confirm on the primary sec.gov PDF header.

### manipulation_period_start/end  —  판정: supports / 신뢰도: high
- **기록값**: 2007 to 2012
- **인용**: “Between 2007 and 2012, Weatherford, a large multinational provider of oil and natural gas equipment and services, issued false financial statements that inflated its earnings by over $900 million in violation of U.S. Generally Accepted Accounting Principles ("GAAP").”
- **출처**: https://www.sec.gov/files/litigation/admin/2016/33-10221.pdf (sec_press_release_text)
- **검증 노트**: Order para 1; also mirrored verbatim by NYU SEED and SEC harmed-investors page. Note: the four-year TAX FRAUD 'plug' specifically spanned FY2007-2010 (para 23); the 2007-2012 window is the full false-statements/restatement period.

### scheme_summary  —  판정: supports / 신뢰도: high
- **기록값**: Unsupported manual post-closing income-tax 'plug' adjustments (dividend-exclusion entries in a Bermuda 'Eliminations' entity) lowering the year-end tax provision by $100M-$154M/year, understating tax expense/ETR and creating a phantom ~$461M income-tax receivable
- **인용**: “Throughout 2007-2010, Hudgins and Kitay made these manual post-closing adjustments within a line item on the consolidated tax provision labeled intercompany "dividend exclusion." These dividend exclusion adjustments, which ranged from $286 million to $439 million per year, involved different Weatherford entities within Weatherford's corporate elimination account, which was known as the "Eliminations region." These adjustments were then tax effected at 35%, which falsely lowered Weatherford's year-end provision for income taxes by $100 million to $154 million each year. These dividend exclusion adjustments also overstated net income, understated ETR and tax expense, and ultimately created a $461 million phantom income tax receivable.”
- **출처**: https://www.sec.gov/files/litigation/admin/2016/33-10221.pdf (sec_press_release_text)
- **검증 노트**: Order para 24 confirms $100M-$154M/yr, Eliminations region, $461M phantom receivable, dividend-exclusion plug. Human should verify the 'Bermuda' locus: order paras 30/39 place the plugs in Luxembourg entities within the Eliminations region, with E&Y proposing to reclassify the 2008 plug to a Bermuda entity within Eliminations — so the entity was 'Eliminations region' (Luxembourg/Bermuda), not strictly a single Bermuda entity.

### first_revelation_date  —  판정: supports / 신뢰도: high
- **기록값**: 2011-03-01 (announcement of restatement + ICFR material weakness; stock fell ~11% next day)
- **인용**: “On March 1, 2011, Weatherford filed a Form 8-K with the Commission, in which it made public for the first time that it would be restating its financial results for 2007-2010 and that a material weakness existed in its ICFR for the accounting of income taxes. Weatherford's stock price dropped nearly 11% to $21.14 on the news. ... After announcing the First Restatement, Weatherford's stock price declined nearly 11% in one trading day ($2.38 per share), closing at $21.14 per share on March 2, 2011. The decline eliminated over $1.7 billion from Weatherford's market capitalization.”
- **출처**: https://www.sec.gov/files/litigation/admin/2016/33-10221.pdf (sec_press_release_text)
- **검증 노트**: Order paras 55 and 3. Contemporaneous corroboration: shareholder class-action amended complaint para 39 ('After the market closed on March 1, 2011, Weatherford announced that it would not timely file its 2010 fiscal year Form 10-K ... investors should no longer rely on the Company's financial statements for the fiscal years 2007 through 2010') and Going Concern (2011-03-02) reporting >$500M tax error. Note: the ~11% drop closed on the March 2, 2011 trading day following the after-close March 1 announcement.

### revelation_source  —  판정: supports / 신뢰도: high
- **기록값**: 2011-03-01 Form 12b-25 late-filing notification announcing restatement and income-tax ICFR material weakness; stock fell ~11% next day
- **인용**: “the material weakness in our internal control over financial reporting for income taxes that was disclosed in a notification of late filing on Form 12b-25 filed on March 1, 2011 and in current reports on Form 8-K filed on February 21, 2012 and on July 24, 2012 and subsequent restatements of our historical financial statements.”
- **출처**: https://www.sec.gov/Archives/edgar/data/1603923/000160392316000247/a8-ksecinvestigationsettle.htm (news_contemporaneous)
- **검증 노트**: Weatherford's own 2016 8-K confirms the revelation vehicle was a Form 12b-25 filed March 1, 2011 disclosing the income-tax ICFR material weakness. Contemporaneous Going Concern (NT 10-K) quotes the 12b-25 text verbatim. Human should open the primary NT 10-K/8-K filed 2011-03-01 under EDGAR CIK 1453090.

### cik  —  판정: supports / 신뢰도: medium
- **기록값**: 0001453090
- **인용**: “"cik":"0001603923", ... "name":"Weatherford International plc","tickers":["WFRD"] ... "formerNames":[{"name":"Weatherford International Ltd","from":"2014-04-02...","to":"2014-06-19..."}]”
- **출처**: https://data.sec.gov/submissions/CIK0001603923.json (edgar_api)
- **검증 노트**: Multi-CIK: CIK 1453090 = 'Weatherford International Ltd.' (Switzerland-domiciled, ticker WFT) is the registrant that filed ALL the 2011-2012 fraudulent/restated statements (every restatement filing is under EDGAR data/1453090 — NT 10-K, 10-K/A, 8-K, 10-Q/A). CIK 1603923 = the current 'Weatherford International plc' (Ireland, now Nasdaq:WFRD), the post-2014 successor named in the order caption ('plc f/k/a Weatherford International Ltd.'). Recorded 1453090 is correct as the period-of-conduct filer. A pre-2009 Bermuda predecessor (Weatherford International Ltd., Bermuda, old WFT) has a separate legacy CIK; human should confirm which CIK holds the 2007-2008 pre-redomestication 10-Ks. Could not fetch CIK0001453090.json (data.sec.gov timeout via Exa) — verify entity name directly.

### xbrl_available  —  판정: supports / 신뢰도: medium
- **기록값**: true
- **인용**: “originally filed on August 3, 2010 (the Form 10-Q) and then amended on September 1, 2010 to attach our extensible business reporting language (XBRL) files, to restate financial information for the three and six months ended June 30, 2010 and 2009 due to errors in the Company's accounting for income taxes.”
- **출처**: https://www.sec.gov/Archives/edgar/data/1453090/000095012311035389/h80875e10vqza.htm (edgar_api)
- **검증 노트**: Weatherford's own 10-Q/A confirms XBRL files were attached to its 2010-era filings (CIK 1453090), consistent with xbrl_available=true. The 2011 restated 10-K/A (wft2011-10ka.htm) also lists exhibit 101 (XBRL). Human can confirm XBRL exhibit 101 presence on the specific pre-revelation filings needed.

## 발견된 불일치/뉘앙스 (검증 우선순위)
- scheme_summary locus: record says the plug entries were in 'a Bermuda "Eliminations" entity'; the SEC order places the actual plug adjustments in LUXEMBOURG entities within the 'Eliminations region' (paras 30, 39), noting only that E&Y 'proposed reclassifying the [2008] adjustment to a Bermuda entity within the Eliminations region' — quote: 'The improper adjustment was made to different Luxembourg entities within Weatherford's Eliminations region ... Although Ernst & Young repeatedly questioned this adjustment ... and proposed reclassifying the adjustment to a Bermuda entity within the Eliminations region ...' Not a numeric contradiction, but the 'Bermuda entity' characterization is imprecise.
- manipulation_period nuance (not a contradiction): the tax-fraud 'plug' scheme itself was a 'four-year income tax accounting fraud' covering FY2007-2010 (order paras 2, 23); the recorded 2007-2012 span reflects the broader false-statement/restatement period (three restatements ending Dec 17, 2012).

## 1차 소스 재검증 결과 (2026-07-03 로컬 세션 — 원문 PDF 직접 대조)

도시에가 플래그했던 2건 모두 원문에서 확정, candidates.json에 정정 반영:

1. **'Bermuda 엔티티' 표현 → MISMATCH 확정.** 원문 ¶30(FY2007): "making an unsubstantiated manual $439.7 million post-closing 'plug' adjustment to **two different Weatherford Luxembourg entities within Weatherford's Eliminations region**." ¶39(FY2008): "The improper adjustment was made to **different Luxembourg entities** … and proposed reclassifying the adjustment to **a Bermuda entity** within the Eliminations region." ¶43(FY2009–10): "These plug adjustments, which were made in 2009 and 2010 using **a Bermuda entity** within Weatherford's Eliminations region." ¶44 엔티티 표: WFT Luxembourg SARL·WFT Financing (Luxembourg) SARL (2007), WFT Luxembourg SARL·WFT Investment (Luxembourg) SARL (2008), **WFT Bermuda Ltd. (2009, 2010)**. → 정정문: "룩셈부르크(FY2007-08)·버뮤다(FY2009-10) 엔티티, 모두 'Eliminations region' 내".
2. **조작기간 2중 구조 확정.** ¶1: "Between 2007 and 2012, Weatherford … issued false financial statements that inflated its earnings by over $900 million." ¶23: "In connection with **fiscal years 2007 through 2010**, Hudgins and Kitay engaged in fraudulent practices relating to income tax accounting." → 기록(2007–2012 전체 기간 + 노트에 플러그 사기 FY2007-10)은 원문 구조와 일치, 변경 없음.
3. **(신규 발견) 폭로 vehicle: 원문은 8-K.** ¶55: "On March 1, 2011, Weatherford **filed a Form 8-K** with the Commission, in which it made public for the first time that it would be restating its financial results for 2007-2010." 기록의 "Form 12b-25"와 상이 — EDGAR 실측으로는 2011-03-01에 **NT 10-K와 8-K 둘 다** 제출됨(당일 Form 4 다수 제외). revelation_source 정정 반영. ~11%/$2.38 하락(¶3, 2011-03-02 종가 $21.14)·시총 $1.7B 소실 확정.
4. $100M–$154M/yr·$461M 팬텀 수취채권(¶24), ETR 가이던스 동기(¶25), AAER-3806/2016-09-27 헤더 — 전부 원문 확정.
5. pre_revelation_quarters_available null → **34** 채움: 버뮤다 전신 CIK 0001170565 27건(2002~2009-02) + 스위스 CIK 0001453090 7건(2009-05~2010-11). FY2007·FY2008 10-K는 버뮤다 CIK 제출 확인(2008-02-21, 2009-02-24) — 도시에 하단의 "전신 CIK 확인" 항목 해소.

## 인간 검증 포인터 (원문 사본 로컬 보유 — 월요일 대조는 아래 로컬 파일/페이지로)
- Primary order PDF (AAER-3806): https://www.sec.gov/files/litigation/admin/2016/33-10221.pdf — verify paras 1-3 (period/$900M), 23-24 (scheme/$461M), 30-39 (Luxembourg/Bermuda Eliminations), 55-56 (March 1 & March 8, 2011 First Restatement, 11% drop).
- SEC press release 2016-194: https://www.sec.gov/newsroom/press-releases/2016-194 (and law-firm mirror https://business.cch.com/srd/2016-194-092716.pdf) — $140M penalty, $100M-$154M/yr, ETR.
- SEC harmed-investors summary page: https://www.sec.gov/enforcement/information-for-harmed-investors/weatherford-international — confirms Rel. No. 33-10221, File No. 3-17582, related E&Y order 34-79109.
- Original 2011-03-01 late-filing disclosure under EDGAR CIK 1453090 (NT 10-K / Form 8-K) — confirm the 12b-25 text and 2007-2010 non-reliance; First Restatement 10-K filed 2011-03-08.
- Weatherford 2016 settlement 8-K: https://www.sec.gov/Archives/edgar/data/1603923/000160392316000247/a8-ksecinvestigationsettle.htm — confirms 12b-25 (2011-03-01) revelation vehicle and $140M terms.
- Restated 10-K/A: https://www.sec.gov/Archives/edgar/data/1453090/000145309012000016/wft2011-10ka.htm — confirm XBRL exhibit 101 and restatement scope.
- Shareholder class action (Dobina v. Weatherford, S.D.N.Y. 1:12-cv-02121-LAK) amended complaint: https://lkswebstorageaccount.blob.core.windows.net/weatherford/36-2012-09-14-AMENDED-COMPLAINT-w-Exhibits.pdf — para 39 corroborates the March 1, 2011 after-close announcement and ~11% drop.
- Verify the pre-2009 Bermuda predecessor CIK (Weatherford International Ltd., Bermuda) for FY2007-2008 pre-redomestication filings vs. Switzerland CIK 1453090 vs. Ireland plc CIK 1603923.

## 학습 노트 (§10)
다중 CIK 기업은 '회사 이름'이 아니라 '그 공시를 낸 registrant'가 케이스의 단위다 — 검증할 것: 조작 당시 공시가 어느 CIK로 나왔는가 (1453090=스위스 시절 filer, 1603923=현 아일랜드 plc, FY2007-08은 버뮤다 전신일 수 있음).
