# RP-13 채점 확정 워크벤치 — 소유자 서명대 (P3, OWNER-GATE-E 세션)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-08. **생성기: `tools/build_rp13_workbench.py` (결정론, verbatim 보증).**
> **용도**: 대기 채점 35건(wave-2 32 + 홀드아웃 3)의 인간 최종 확정(§7). E1/E2/E4/E5 채점은 실행 후 재생성으로 추가. 케이스당 ~30–60초 처리 목표.
> **읽는 법**: 피평가자 p·가설 → 채점 d1/d2/d4 → rationale 발췌(verbatim) → 제안 처분 → 서명란. 확정은 각 grade 파일 `human_finalized=true` + 오버라이드는 `scoring/overrides.md`.
> **루브릭**: 실험군 p≥70→d1=2 / 50–69→1 / <50→0 · 대조군 p≤30→2 / 31–49→1 / ≥50→0. d2: 0 무관 · 1 계정영역 · 2 +방향+유형 · 3 +케이스특이. d4: 증거품질.
> **mem-suspect 전건 false (35/35)** — wave-2/홀드아웃에 암기귀속 의심 0건 (R4/H2의 약한 암기와 정합, 그 자체가 발견).

**요약**: 총 35건 · 우선 검토(TIER A, 플래그) 13건 · 표준(TIER B) 22건. 아래는 플래그 우선 정렬.

---


## TIER A — 우선 검토

### case_65 = Weatherford International Ltd. (Switzerland) (WFT, T04) — FRAUD ⚑ 채점자-경계표시

- 피평가자: **p=74** · tier=elevated · 가설(확신순):
  1. [overstated] Revenues, ReceivablesNetCurrent, AllowanceForDoubtfulAccountsReceivableCurrent — Potential premature/aggressive revenue recognition or delayed write-down of receivables during a period of declining top-line, evidenced by receivables continuing to grow (ReceivablesNetCurrent=250487…
  2. [overstated] Goodwill, IntangibleAssetsNetExcludingGoodwill — Rapid goodwill build-up (+17.8% in a single quarter, Goodwill=3530915000 at 2008-12-31 to Goodwill=4159206000 at 2009-09-30) during a period of revenue contraction raises risk that acquisition-related…
- 채점(claude-fable-5): **d1=2** · d2=0 · d3=mixed/None · d4=3 · mem2=False
- 정답 키(채점측): Made unsupported manual post-closing income-tax 'plug' adjustments (intercompany 'dividend exclusion' entries booked to Luxembourg entities in FY2007-08 and a Bermuda entity in FY2009-10, all within Weatherford's corporate 'Eliminations reg…
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Dim1=2: treatment case, p=74 >= 70. Dim2=0: top-ranked hypothesis alleges premature revenue recognition / delayed write-down of trade receivables (Revenues, ReceivablesNetCurrent, Allowance) — unrelated to the answer key's mechanism of manu…
  > Coverage note: hypothesis #3 names 'Income tax accounts', direction NetIncomeLoss overstated / tax liabilities understated, which substantially matches account+direction and would likely score 2 if top-ranked, but rubric grades top-ranked o…
- **제안 처분**: finalize (실험군 정탐)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_61 = Celadon Group, Inc. (CGI, T24) — FRAUD ⚑ 채점자-경계표시

- 피평가자: **p=72** · tier=elevated · 가설(확신순):
  1. [overstated] OtherAssetsNoncurrent, PropertyPlantAndEquipmentNet, Goodwill — Capitalization of costs or gains associated with revenue-equipment transactions and acquisitions into non-current 'other assets'/goodwill rather than expensing, producing extreme, business-disproporti…
  2. [overstated] AccountsReceivableNetCurrent, Revenues, AllowanceForDoubtfulAccountsReceivableCurrent — Receivables (and implied revenue) grew consistently faster than revenue for three consecutive fiscal years (FY2013-FY2015), with days-sales-outstanding rising from ~38-40 days to ~48-51 days, while th…
- 채점(claude-fable-5): **d1=2** · d2=2 · d3=mixed/None · d4=3 · mem2=False
- 정답 키(채점측): Avoided recognizing at least ~$20M in used-truck impairment charges/losses (nearly two-thirds of 2016 pre-tax income) by buying and selling more than a thousand trucks at inflated prices (in cases 2-3x fair value) with a third-party dealer,…
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > DIM1 (=2): Treatment case per answer key. Output states misstatement_probability=72, which is >=70, so band score = 2.
  > DIM2 (=2): Top-ranked hypothesis targets OtherAssetsNoncurrent, PropertyPlantAndEquipmentNet, Goodwill, NetIncomeLoss, direction 'overstated', with treatment described as capitalization/deferral tied to 'revenue-equipment transactions... co…
  > DIM3 (mapped=mixed, score=null): Top hypothesis narrative combines an active-treatment element (capitalizing costs/gains into other assets/goodwill 'rather than expensing') with an omission/estimate element ('deferred recognition of losses,…
  > DIM4 (=3): Citations reference specific accession numbers with concrete numeric data points that genuinely support the claims: NI +$24.844M vs. operating cash flow -$5.211M for FY2016 (10-K 0001008886-16-000363) and NI +$11.367M vs. OCF -$2…
  > MEMORIZATION_SUSPECT_CONDITION2 (=false): (a) fails — the reasoning points extensively at concrete provided data content (specific XBRL values with periods and accessions), not bare document lists. (b) fails — no mention of post-cutoff fact…
- **제안 처분**: finalize (실험군 정탐)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_66 = Under Armour, Inc. (UAA, T29) — FRAUD ⚑ 채점자-경계표시

- 피평가자: **p=55** · tier=elevated · 가설(확신순):
  1. [overstated] Revenues/SalesRevenueNet, AccountsReceivableNetCurrent, InventoryNet — Possible premature/aggressive revenue recognition or 'sell-in' shipment to distributors/off-price channel ahead of end-customer demand, evidenced by receivables and inventory consistently outgrowing r…
  2. [overstated] NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, AccountsReceivableNetCurrent — Earnings recognized in FY2015 were not substantiated by cash generation (NetIncomeLoss=232,573,000 vs NetCashProvidedByUsedInOperatingActivities=14,541,000), suggesting revenue/profit booked on credit…
- 채점(claude-fable-5): **d1=1** · d2=2 · d3=active/1 · d4=3 · mem2=False
- 정답 키(채점측): Undisclosed 'pull forward' of ~$408M in existing customer orders over six consecutive quarters (Q3 2015-Q4 2016) to meet analysts' revenue estimates, while attributing revenue growth to other factors and not disclosing the practice or resul…
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > dim1=1: treatment case with p=55, falling in the 50<=p<70 band. dim2=2: the TOP-RANKED hypothesis targets Revenues/SalesRevenueNet and AccountsReceivableNetCurrent, direction 'overstated', with treatment 'premature/aggressive revenue recogn…
  > Coverage: the disclosure_only/omission component of the multi-part truth is uncovered by any hypothesis. dim3: top hypothesis narrative is active conduct (deliberate sell-in/premature recognition) -> mapped 'active'; key scheme is mixed (ac…
- **제안 처분**: finalize (실험군 정탐)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_49 = IOVANCE BIOTHERAPEUTICS, INC. (IOVA, W04) — control ⚑ 오류(출력≠정답)

- 피평가자: **p=58** · tier=elevated · 가설(확신순):
  1. [timing_shift] NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, AdditionalPaidInCapital/derivative or warrant liabilities (not separately provided) — Large non-cash charges (likely stock-based compensation, warrant/derivative revaluation, or beneficial conversion features typical of reverse-merger micro-cap biotechs) are driving a persistent, large…
  2. [understated] AccruedLiabilitiesCurrent, ResearchAndDevelopmentExpense, LiabilitiesCurrent — Accrued liabilities fell sharply (AccruedLiabilitiesCurrent 1,518,225 to 327,847) even as R&D spending roughly doubled, suggesting potential under-accrual of clinical trial/vendor liabilities (a commo…
- 채점(claude-fable-5): **d1=0** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Control case (answer_key.group=control). Dim1: output's misstatement_probability=58, which is >=50 on a control case -> 0 per rubric. Dim2/Dim3: treatment-only dimensions -> null for control. Dim4: consistency rule satisfied (p=58 in [40,70…
- **제안 처분**: finalize (오탐이나 채점 d1=0 정확 — trust boundary 데이터. §1 오류해부 참조)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_44 = ADAMAS TRUST, INC. (ADAM, W08) — control ⚑ 오류(출력≠정답)

- 피평가자: **p=55** · tier=elevated · 가설(확신순):
  1. [understated] InterestExpense, NetIncomeLoss/ProfitLoss, InterestExpense (annual aggregate) — Possible understatement/mis-tagging of annual interest expense relative to the much larger quarterly interest expense figures reported for the same fiscal years, which would understate a mortgage REIT…
  2. [overstated] NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities — Growing reliance on non-cash gains (e.g., unrealized mark-to-market gains on MBS/derivatives, premium amortization adjustments typical of mortgage REITs) to drive reported net income well above cash g…
- 채점(claude-fable-5): **d1=0** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Control case (answer key group='control'). Dim1: output gives misstatement_probability=55; control rubric assigns 0 for p>=50. Dim2: null (control). Dim3: nulls (control). Dim4: consistency check first — p=55 requires watch/elevated tier an…
- **제안 처분**: finalize (오탐이나 채점 d1=0 정확 — trust boundary 데이터. §1 오류해부 참조)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_48 = LIVEPERSON INC (LPSN, W09) — control ⚑ 오류(출력≠정답)

- 피평가자: **p=55** · tier=elevated · 가설(확신순):
  1. [overstated] AllowanceForDoubtfulAccountsReceivableCurrent, AccountsReceivableNetCurrent, BadDebtExpense (implied) — Under-provisioning of allowance for doubtful accounts while receivables grew substantially (allowance held flat at $708,000 for seven consecutive quarter-ends from 2012-03-31 through 2013-09-30 while …
  2. [timing_shift] Unspecified financial statement line items subject to SEC Corp Fin review, Prior period 10-K disclosures — An apparent SEC Division of Corporation Finance comment letter review (evidenced by CORRESP and UPLOAD filings from November 2015 through January 2016) culminating in a 10-K/A filed 2016-01-22, just b…
- 채점(claude-fable-5): **d1=0** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Control case (answer key group=control). dim1: output gives misstatement_probability=55; control rubric says p>=50 -> 0. dim2/dim3: control -> null per rubric. dim4: no consistency-cap violation (p=55 with risk_tier 'elevated' satisfies 40<…
  > Minor interpretive flaw noted (treating positive OCF > negative NI as an overstatement flag is the atypical direction) but citations are genuine and supportive. memorization_suspect_condition2: false - reasoning cites concrete provided data…
- **제안 처분**: finalize (오탐이나 채점 d1=0 정확 — trust boundary 데이터. §1 오류해부 참조)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_54 = LEVI STRAUSS & CO (LEVI, W21) — control ⚑ 약증거(d4=2) · 오류(출력≠정답)

- 피평가자: **p=55** · tier=elevated · 가설(확신순):
  1. [overstated] AccountsReceivableNetCurrent, RevenueFromContractWithCustomerExcludingAssessedTax, SalesRevenueNet — Potential premature/accelerated revenue recognition or extension of unusually generous credit terms to wholesale customers (e.g., bill-and-hold, channel loading ahead of quarter-end, or delayed collec…
  2. [understated] AllowanceForDoubtfulAccountsReceivableCurrent, AccountsReceivableNetCurrent, NetIncomeLoss — The allowance for doubtful accounts as a percentage of gross receivables has shrunk even as receivables balloon, suggesting the bad-debt reserve is not being built proportionally to the higher credit …
- 채점(claude-fable-5): **d1=0** · d2=None · d3=None/None · d4=2 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > DIM1 (=0): Answer key marks this a CONTROL case (group='control', no scheme). Output gives misstatement_probability=55. Control banding: p>=50 -> 0. 55 >= 50, so score 0.
  > DIM2 (=null): Control case; mechanism dimension is not graded per rubric.
  > DIM3 (=nulls): Control case; genre mapping not graded.
  > DIM4 (=2): Consistency rule check first: p=55 requires tier watch/elevated; declared risk_tier='elevated' is consistent, so no cap. The evidence is largely specific and arithmetically verifiable against the cited filings: e.g., CL1 cites Ac…
- **제안 처분**: finalize (오탐이나 채점 d1=0 정확 — trust boundary 데이터. §1 오류해부 참조)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_69 = ARTIVION, INC. (AORT, W18) — control ⚑ 오류(출력≠정답)

- 피평가자: **p=50** · tier=watch · 가설(확신순):
  1. [overstated] AccountsReceivableNetCurrent, Revenues, DeferredRevenueCurrent — Possible premature or accelerated revenue recognition: receivables grew far faster than revenue in 2013-2015 (AR +48.5% vs revenue +22% over the period) while deferred revenue simultaneously collapsed…
  2. [understated] AccruedLiabilitiesCurrent, NetIncomeLoss, OperatingIncomeLoss — Possible reserve/accrual release used to boost reported earnings: accrued liabilities fell from 5,131,000 (2011) to 2,411,000 (2013) even as revenue grew, and Q4 2013 net income spiked to 9,026,000 ve…
- 채점(claude-fable-5): **d1=0** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > dim1=0: Control case with misstatement_probability=50; rubric control bands are p<=30 -> 2, 30<p<50 -> 1, p>=50 -> 0, and p=50 falls in the p>=50 band. dim2=null and dim3=nulls: control case per rubric. dim4=3: No consistency cap triggered …
- **제안 처분**: finalize (오탐이나 채점 d1=0 정확 — trust boundary 데이터. §1 오류해부 참조)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_52 = Computer Sciences Corporation (CSC, T02) — FRAUD ⚑ 오류(출력≠정답)

- 피평가자: **p=40** · tier=watch · 가설(확신순):
  1. [overstated] OtherAssetsNoncurrent, Goodwill, Assets — Possible under-impairment or continued capitalization of costs (e.g., deferred contract costs, capitalized software, or transition/setup costs on outsourcing contracts) into Other Assets, Noncurrent, …
  2. [overstated] ReceivablesNetCurrent, Revenues — Potential revenue recognition timing acceleration (e.g., percentage-of-completion estimates on long-term outsourcing/systems-integration contracts) causing receivables to grow modestly (3786000000 to …
- 채점(claude-fable-5): **d1=0** · d2=2 · d3=mixed/None · d4=3 · mem2=False
- 정답 키(채점측): Overstated earnings and concealed losses on its UK NHS contract via improper percentage-of-completion models; Australian 'cookie jar' reserves and failure to record expenses; and Nordic misconduct including improper accounting for client di…
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Dim1=0: treatment case with misstatement_probability=40, which is <50 (band: p<50 -> 0). Dim2=2: top-ranked hypothesis asserts overstatement of OtherAssetsNoncurrent/Goodwill via 'continued capitalization of costs (deferred contract costs, …
  > Coverage note: revenue_recognition/POC appears only in the second-ranked hypothesis; reserves_smoothing is uncovered (CL6 = insufficient_data). Dim3: top hypothesis maps to 'mixed' (active capitalization of costs + omission-type failure to …
- **제안 처분**: finalize (미탐 — 채점 정확. CSC=보정 near-miss / BRX=구조적 미탐, §2 참조)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_67 = Brixmor Property Group Inc. (BRX, T20) — FRAUD ⚑ 오류(출력≠정답)

- 피평가자: **p=20** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=0** · d2=0 · d3=None/None · d4=3 · mem2=False
- 정답 키(채점측): Manipulated the non-GAAP 'same property net operating income' (SP NOI) growth rate by smoothing income up and down between quarters using a 'cookie jar' ledger account (the '2617 account'), including previously-excluded lease-termination in…
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > DIM1 (=0): This is a treatment case per the answer key (SEC Order 34-86538 / AAER-4061, SP NOI smoothing via the '2617' cookie-jar account, Jul-2013 to Sep-2015). The output gives misstatement_probability=20, which falls in the p<50 band fo…
  > DIM2 (=0): mechanism_hypotheses is an empty list. With p=20 (<40) a hypothesis was not strictly required by the rubric's parenthetical, but there is no top-ranked hypothesis touching the correct account area (SP NOI / lease-termination inco…
  > DIM3 (null/null): There is no top-ranked hypothesis narrative to map to active/omission-estimate/mixed, so genre mapping is ungradeable; the answer key's genre_tag_row is also null. Recorded as nulls rather than 0, since 0 denotes a wrong m…
  > DIM4 (=3): Citations are concrete provided data points that genuinely support the claims made: CL3 quotes exact NI vs OCF figures (e.g., NI=-160,713,000 vs OCF=268,847,000 for FY2012; NI=132,851,000 vs OCF=479,210,000 for FY2014) and pairs …
- **제안 처분**: finalize (미탐 — 채점 정확. CSC=보정 near-miss / BRX=구조적 미탐, §2 참조)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_73 = Genie Energy Ltd. (GNE, case_73) — HOLDOUT(G2) ⚑ 홀드아웃-미탐/경계 · G2-provisional

- 피평가자: **p=42** · tier=watch · 가설(확신순):
  1. [overstated] AllowanceForDoubtfulAccountsReceivableCurrent, AccountsReceivableNetCurrent, Bad debt expense (SG&A) — In FY2022, accounts receivable grew ~33% while revenue declined slightly and the allowance for doubtful accounts was cut ~21% (allowance/AR coverage fell from ~14.9% to ~8.8%). This pattern is consist…
  2. [overstated] OtherAssetsNoncurrent, OperatingIncomeLoss (via reduced expense recognition) — Other noncurrent assets grew roughly 150% (from $8.9M at 2021-12-31 to $22.4M at 2024-12-31) while revenue grew only ~31% over the same window, and while the company was expanding into capital-intensi…
- 채점(claude-fable-5): **d1=0** · d2=0 · d3=omission-estimate/None · d4=3 · mem2=False
- 정답 키(채점측): 8-K Item 4.02 (2026-03-12): captive-insurance subsidiary liability accounting error; FY2023-24 and prior quarters restated. G2 PROVISIONAL (non-reliance/restatement event, error-like, NOT confirmed fraud).
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > DIM1 (0): Treatment case; output gives misstatement_probability=42, which is <50, so per the treatment band table this scores 0.
  > DIM2 (0): p=42 >= 40, so a top-ranked hypothesis is required and one is provided; grading the TOP-RANKED hypothesis only. The top hypothesis targets AllowanceForDoubtfulAccountsReceivableCurrent / AccountsReceivableNetCurrent / bad debt exp…
  > DIM3 (mapped=omission-estimate, score=null): The top-ranked hypothesis (understated bad-debt reserve/estimate) maps to the omission-estimate genre. However, the answer key's genre_tag_row is null (G2 PROVISIONAL, error-like restatement, not…
  > DIM4 (3): Evidence is specific and genuine: exact XBRL-style values with dates and accession numbers (e.g., allowance 6,139,000 at 2021-12-31 vs 4,826,000 at 2022-12-31; AR 41,309,000 → 55,134,000; NI 19,538,000 vs CFO 62,478,000 in FY2023 …
  > MEMORIZATION_SUSPECT_CONDITION2 (false): The reasoning cites concrete provided data content throughout (not bare document lists), and nothing references post-cutoff facts — no mention of the 2026-03-12 Item 4.02 8-K, the captive-insurance s…
- **제안 처분**: finalize (G2 provisional 라벨 유지 — 4.02/AAER 상향 시 티어 갱신)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_72 = Weis Markets, Inc. (WMK, case_72) — HOLDOUT(G2) ⚑ 홀드아웃-미탐/경계 · G2-provisional

- 피평가자: **p=32** · tier=watch · 가설(확신순):
  1. [overstated] AccountsReceivableNetCurrent, Revenues — Possible slower recognition of allowance for doubtful accounts or expansion of receivable-generating programs (e.g., pharmacy/insurance billing, vendor allowances, fuel rewards) that outpaced core rev…
  2. [understated] AccruedLiabilitiesCurrent, NetIncomeLoss — Decline in accrued liabilities as a percentage of revenue (from ~1.22% in FY2022 to ~0.71% in FY2024) could reflect release or under-accrual of reserves (e.g., incentive compensation, insurance/self-i…
- 채점(claude-fable-5): **d1=0** · d2=0 · d3=omission-estimate/None · d4=3 · mem2=False
- 정답 키(채점측): 8-K Item 4.02 (2026-02-20): whistleblower-triggered; meat-processing plant inventory overstated up to ~$22M cumulative (FY2022-2025). G2 PROVISIONAL (non-reliance/restatement event, NOT confirmed fraud).
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > DIM1=0: Treatment case; output gives misstatement_probability=32, which is <50 (treatment band: p<50 -> 0).
  > DIM2=0: Answer key mechanism is inventory overstatement (~$22M cumulative, FY2022-2025, meat-processing plant). Top-ranked hypothesis targets AccountsReceivableNetCurrent/Revenues via allowance-for-doubtful-accounts under-recognition — an u…
  > DIM3=null: Top hypothesis narrative maps to omission-estimate (under-provisioning of allowance estimate), but the answer key genre_tag_row is null (G2 PROVISIONAL, non-reliance/restatement event, not confirmed fraud), so no key genre exists…
  > DIM4=3: Evidence cites specific provided data points with accession numbers (AR 50,863K->65,092K->81,567K vs flat revenue ~$4.71-4.79B; accrued liabilities 57,431K->34,196K; NI vs OCF for FY2022/FY2024), and top_signals combine them into co…
- **제안 처분**: finalize (G2 provisional 라벨 유지 — 4.02/AAER 상향 시 티어 갱신)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_71 = Hub Group, Inc. (HUBG, case_71) — HOLDOUT(G2) ⚑ G2-provisional

- 피평가자: **p=70** · tier=elevated · 가설(확신순):
  1. [timing_shift] Net income (multiple periods FY2013-FY2017), Operating income/cost of services (quarterly 2016-2017), Balance sheet accounts as of 2015-12-31 and interim 2016-2017 dates — Restatement/correction of an error under ASC 250 in previously issued financial statements. The simultaneous filing of a 10-K/A (covering FY2015, with FY2013-2014 comparatives) and three 10-Q/A filing…
  2. [overstated] Goodwill, IntangibleAssetsNetExcludingGoodwill — Purchase-accounting-driven goodwill/intangible build-up from a series of acquisitions (evidenced by step-changes in Goodwill: 2017 Q3 262,266,000->348,506,000; 2018 12-03 483,584,000; 2020 484,459,000…
- 채점(claude-fable-5): **d1=2** · d2=1 · d3=omission-estimate/None · d4=3 · mem2=False
- 정답 키(채점측): 8-K Item 4.02 (2026-02-05): purchased transportation costs ~$77M understated / unrecorded accounts payable; FY2023-24 10-Ks characterized as materially misstated; CFO and COO terminated. G2 PROVISIONAL (non-reliance/restatement event, NOT c…
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > DIM1 (=2): Treatment case; output gives misstatement_probability = 70, which meets the p>=70 band -> 2.
  > DIM2 (=1): Answer key mechanism: purchased transportation costs ~$77M understated / unrecorded accounts payable, FY2023-24 10-Ks misstated (8-K Item 4.02, 2026-02-05). The TOP-RANKED hypothesis instead centers on the historical 2018-01-05 a…
  > DIM3 (score=null, mapped_genre='omission-estimate'): Top-ranked narrative — a multi-period error correction / timing shift of expenses without any alleged active fabrication — maps most naturally to omission-estimate. However, the answer ke…
  > DIM4 (=3): Consistency rule satisfied: p=70 => elevated required; risk_tier='elevated', so no cap. Evidence is specific and verifiable against provided data: CL1/CL3/CL6 cite concrete XBRL values with accessions and period tags (e.g., FY202…
  > MEMORIZATION_SUSPECT_CONDITION2 (=false): (a) fails — the reasoning repeatedly points at concrete provided data content (specific XBRL values, filing dates, accession numbers), not bare document lists. (b) fails — no mention of any post-cut…
- **제안 처분**: finalize (G2 provisional 라벨 유지 — 4.02/AAER 상향 시 티어 갱신)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)


## TIER B — 표준

### case_60 = MiMedx Group, Inc. (MDXG, T26) — FRAUD

- 피평가자: **p=65** · tier=elevated · 가설(확신순):
  1. [overstated] AccountsReceivableNetCurrent, SalesRevenueGoodsNet/SalesRevenueNet — Potential premature or aggressive revenue recognition (e.g., recording sales to distributors/consignees as final revenue) leading to receivables growing much faster than revenue and a rising implied d…
  2. [overstated] NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities — Earnings quality concern where reported net income substantially outpaces cash generated from operations, potentially reflecting non-cash revenue recognition, working-capital-driven earnings, or aggre…
- 채점(claude-fable-5): **d1=1** · d2=2 · d3=active/2 · d4=3 · mem2=False
- 정답 키(채점측): Prematurely recognized revenue and exaggerated revenue growth through channel-stuffing to distributors and undisclosed side arrangements with five distributors (allowing product returns or conditioning distributors' payment on resale to end…
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Dim1=1: treatment case, p=65 falls in 50<=p<70 band. Dim2=2: top-ranked hypothesis names the correct account area (SalesRevenueGoodsNet/AR), correct direction (overstated), and correct treatment type ('premature or aggressive revenue recogn…
  > Coverage note: hypothesis 3 also flags channel-stuffing via the 2016 inventory build, reinforcing the same single-mechanism truth. Dim3=2: top hypothesis maps to 'active' (aggressive/premature revenue booking); answer-key scheme (channel-st…
- **제안 처분**: finalize (실험군 정탐)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_39 = Osiris Therapeutics, Inc. (OSIR, T19) — FRAUD

- 피평가자: **p=58** · tier=elevated · 가설(확신순):
  1. [overstated] AccountsReceivableNetCurrent, Revenues/SalesRevenueGoodsNet, AllowanceForDoubtfulAccountsReceivableCurrent — Potential premature or aggressive revenue recognition (e.g., extended payment terms, bill-and-hold, or channel stuffing to distributors) causing receivables to grow far faster than sales, combined wit…
  2. [overstated] InventoryNet, CostOfGoodsSold, GrossProfit — Inventory build-up (roughly 5.7x from 2013-12-31 to 2014-12-31) far outpacing revenue growth (~2.5x) may reflect capitalization of costs that should be expensed, failure to write down slow-moving/obso…
- 채점(claude-fable-5): **d1=1** · d2=2 · d3=mixed/1 · d4=3 · mem2=False
- 정답 키(채점측): Artificially inflated reported revenue by recognizing revenue at inflated prices, backdating documents to shift revenue into earlier periods, prematurely recognizing revenue on consignment deliveries, using pricing data known to be false, a…
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > DIM1=1: Treatment case; output gives misstatement_probability=58, which falls in the 50<=p<70 band -> 1 (not >=70, so not 2).
  > DIM2=2: Top-ranked hypothesis names 'premature or aggressive revenue recognition (extended payment terms, bill-and-hold, channel stuffing)' affecting AccountsReceivableNetCurrent/Revenues/SalesRevenueGoodsNet/NetIncomeLoss, direction 'overs…
  > DIM3=1: Top hypothesis narrative blends active manipulation (premature revenue recognition/channel stuffing) with an estimate omission element ('understating the allowance for doubtful accounts... thereby overstating net receivables and net…
  > DIM4=3: Evidence consists of specific provided data points with values/dates/accession numbers that genuinely support claims: AR $21.446M (2014-09-30, acc 0001104659-14-078750) to $38.598M (2015-06-30, acc 0001104659-15-057928) with implied…
- **제안 처분**: finalize (실험군 정탐)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_59 = The Hain Celestial Group, Inc. (HAIN, T23) — FRAUD

- 피평가자: **p=58** · tier=elevated · 가설(확신순):
  1. [overstated] Allowance for doubtful accounts, Accounts receivable, net, Bad debt expense (SG&A) — Reserve/allowance methodology: the allowance for doubtful accounts was cut roughly in half (2,661,000 to 896,000) while gross receivables grew ~92% (166,677,000 to 320,197,000) over FY2012-FY2015, sha…
  2. [overstated] Inventory, net, Cost of goods sold, Gross profit — Inventory build-up outpaced revenue growth in FY2013 (34.2% vs 25.9%) while gross margin steadily eroded from 27.75% (FY2012) to 23.01% (FY2015), consistent with either channel-stuffing of distributor…
- 채점(claude-fable-5): **d1=1** · d2=1 · d3=omission-estimate/0 · d4=3 · mem2=False
- 정답 키(채점측): Sales personnel offered the company's two largest distributors undocumented end-of-quarter incentives (return rights for spoiled/expired product, cash payments up to $500K, discounts, extended payment terms) to pull inventory forward and me…
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > DIM1=1: Treatment case; output p=58, which falls in 50<=p<70 band per rubric.
  > DIM2=1: Top-ranked hypothesis is under-reserving of the allowance for doubtful accounts (allowance $2.661M->$0.896M while AR grew $166.7M->$320.2M), overstating net receivables/net income. Answer key describes revenue recognition via undocu…
  > DIM3=0: Top hypothesis narrative is an estimate/reserve manipulation -> maps to omission-estimate; answer-key scheme is an active scheme (sales personnel affirmatively offering incentives to accelerate revenue). Omission-estimate vs active …
  > DIM4=3: Evidence cites specific provided data points with accession numbers and exact values (e.g., allowance vs AR trend FY2012-FY2015; gross margin 27.75%->23.01% FY2012-FY2015; inventory growth 34.2% vs revenue 25.9% in FY2013; intangibl…
- **제안 처분**: finalize (실험군 정탐)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_40 = Tangoe, Inc. (TNGO, T22) — FRAUD

- 피평가자: **p=55** · tier=watch · 가설(확신순):
  1. [overstated] AccountsReceivableNetCurrent, SalesRevenueServicesNet, AllowanceForDoubtfulAccountsReceivableCurrent — Potential premature or aggressive revenue recognition (e.g., billing ahead of service delivery, extended customer payment terms, or channel-stuffing) combined with an under-provisioned bad debt allowa…
  2. [understated] AllowanceForDoubtfulAccountsReceivableCurrent, NetIncomeLoss, GeneralAndAdministrativeExpense — Bad debt reserve/allowance for doubtful accounts was reduced or held flat while receivables grew rapidly (2010-2012), likely understating bad debt expense and overstating net income and net receivable…
- 채점(claude-fable-5): **d1=1** · d2=2 · d3=mixed/None · d4=3 · mem2=False
- 정답 키(채점측): Overstated revenue by ~$40M of $566M reported by prematurely recognizing revenue for unperformed work, booking customer prepayments and uncollectible/contingent-fee revenue, recording a business partner's loan as revenue, and violating bad-…
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > DIM1=1: Treatment case; output p=55, which falls in 50<=p<70 band.
  > DIM2=2: Top-ranked hypothesis names revenue (SalesRevenueServicesNet) and AR accounts, direction overstated, treatment 'premature or aggressive revenue recognition (billing ahead of service delivery)' plus under-provisioned bad-debt allowan…
  > DIM3: Top hypothesis maps to 'mixed' (active premature recognition + omission-estimate under-reserving), but the answer key's genre_tag_row is null, so there is no key genre to compare against; score set to null for the human auditor to fin…
  > DIM4=3: No cap — p=55 with risk_tier 'watch' satisfies the consistency rule. Evidence cites specific provided data points that genuinely support the mechanism claims: AR 43,273k->56,948k (+31.6%) vs revenue 188,914k->212,476k (+12.5%) FY201…
- **제안 처분**: finalize (실험군 정탐)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_43 = NABORS INDUSTRIES LTD (NBR, W01) — control

- 피평가자: **p=45** · tier=watch · 가설(확신순):
  1. [overstated] Goodwill, OtherAssetsNoncurrent — Purchase price allocation from a Q3 2010 acquisition (goodwill jumped from Goodwill=164078000 (2010-06-30) to Goodwill=463427000 (2010-09-30), and OtherAssetsNoncurrent rose from 253834000 (2010-06-30…
  2. [timing_shift] NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, DepreciationAndAmortization — A persistent, large gap between reported net income/loss and operating cash flow (NetIncomeLoss=-85546000 vs NetCashProvidedByUsedInOperatingActivities=1616972000 for 2009 annual) suggests heavy relia…
- 채점(claude-fable-5): **d1=1** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > dim1=1: Answer key group=control; output misstatement_probability=45, which falls in the 30<p<50 control band (not <=30 for full credit, not >=50 for zero). dim2=null and dim3 nulls: rubric mandates nulls for control cases. dim4=3: risk_tie…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_68 = REPLIGEN CORP (RGEN, W03) — control

- 피평가자: **p=45** · tier=watch · 가설(확신순):
  1. [overstated] AccountsReceivableNetCurrent, AllowanceForDoubtfulAccountsReceivableCurrent, Revenues — Potential premature revenue recognition and/or under-provisioning of the allowance for doubtful accounts, causing net accounts receivable to grow far faster than revenue (AR/quarterly-revenue ratio ri…
  2. [overstated] Goodwill, IntangibleAssetsNetExcludingGoodwill, Assets — Purchase accounting for the mid-2014 acquisition may have allocated an outsized portion of consideration to goodwill/intangibles relative to tangible/identifiable value, inflating non-current 'soft' a…
- 채점(claude-fable-5): **d1=1** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > DIM1 (band=1): Answer key group is 'control'. Output misstatement_probability=45, which falls in the control band 30<p<50 -> score 1. The output over-flags a clean company (5 of 7 substantive checklist items flagged) but stays below the 50 …
  > DIM2 (null): Control case -> mechanism dimension is null per rubric; the three mechanism hypotheses (AR/revenue recognition, purchase-accounting goodwill allocation, cutoff/timing) are not graded against any scheme since no scheme exists in…
  > DIM3 (nulls): Control case -> genre mapping is null/null per rubric (answer key genre_tag_row is null).
  > DIM4 (=3): Evidence is specific and internally coherent. Checklist items and mechanism assertions cite concrete provided data points with values, dates, accession numbers, and statement locations: e.g., CL1 combines AccountsReceivableNetCur…
  > MEMORIZATION_SUSPECT_CONDITION2 (false): The reasoning points extensively at concrete provided data content (specific XBRL-style values with periods and accessions), so condition (a) fails; and no post-cutoff facts (revelation, enforcement …
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_46 = UFP TECHNOLOGIES INC (UFPT, W19) — control

- 피평가자: **p=42** · tier=watch · 가설(확신순):
  1. [overstated] InventoryNet, CostOfGoodsSold, GrossProfit — Possible insufficient inventory reserves/write-downs for slow-moving or obsolete inventory as inventory grew 76.6% (InventoryNet=8,044,336 in FY2010 to InventoryNet=14,202,000 in FY2015) far outpacing…
  2. [overstated] ReceivablesNetCurrent, SalesRevenueNet — Possible premature revenue recognition, extended customer payment terms, or channel-stuffing in fiscal 2016, as accounts receivable grew 11.8%-17.9% year-over-year in Q1-Q3 2016 while revenue grew onl…
- 채점(claude-fable-5): **d1=1** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Dim1: Control case per answer key; output p=42, and control rule gives 1 for 30<p<50. Dim2/Dim3: null per rubric (control case); noted that the output nonetheless proposes mechanism hypotheses, graded only via dim4. Dim4: Consistency rule s…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_47 = HALOZYME THERAPEUTICS, INC. (HALO, W05) — control

- 피평가자: **p=42** · tier=watch · 가설(확신순):
  1. [timing_shift] Revenues, AccountsReceivableNetCurrent — Recognition of collaboration/license milestone or upfront revenue under multiple-element arrangement guidance (ASC 605-25) ahead of cash collection, producing a large receivable build in a year when r…
  2. [timing_shift] CostOfGoodsSold, GrossProfit, InventoryNet — Possible under-accrual or delayed recognition of product manufacturing/royalty costs in FY2013 (implying overstated gross margin that period) followed by a catch-up increase in COGS in FY2014, distort…
- 채점(claude-fable-5): **d1=1** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Control case per answer key (group=control, no scheme). Dim1: output states misstatement_probability=42; control band 30<p<50 -> 1. Dim2: control -> null. Dim3: control -> nulls. Dim4: risk_tier='watch' with p=42 satisfies the consistency r…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_62 = UNIVERSAL LOGISTICS HOLDINGS, INC. (ULH, W15) — control

- 피평가자: **p=42** · tier=watch · 가설(확신순):
  1. [overstated] Allowance for Doubtful Accounts, Bad Debt Expense (within SG&A), Net Income — Reduction of the allowance for doubtful accounts (reserve release) in Q4 2016 without a corresponding decline in gross receivables or revenue, which would reduce bad debt expense and boost reported ne…
  2. [overstated] Property, Plant & Equipment (gross/net), Depreciation expense, Operating expenses — Aggressive capitalization of costs into PP&E during a revenue downturn (capex nearly quadrupled year-over-year while revenue declined), potentially capitalizing items that should be expensed, inflatin…
- 채점(claude-fable-5): **d1=1** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > dim1=1: Answer key group=control; output misstatement_probability=42, which falls in the control band 30<p<50 → 1 (would need p<=30 for a 2). dim2=null and dim3=nulls: mandated for control cases. dim4=3: Consistency rule satisfied (p=42 wit…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_56 = BLACKSTONE MORTGAGE TRUST, INC. (BXMT, W07) — control

- 피평가자: **p=35** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=1** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > CONTROL case (answer key: group=control, no scheme). dim1: output gives misstatement_probability=35, which falls in the control band 30<p<50 -> score 1 (a probability <=30 would have earned 2; 35 is a near-miss). dim2/dim3: control case, so…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_63 = SITE Centers Corp. (SITC, W06) — control

- 피평가자: **p=30** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > DIM1 (=2): Answer key marks this a CONTROL case (group='control', no scheme). Output gives misstatement_probability=30, which satisfies the control band p<=30 -> 2 (exactly at the boundary, which the rubric includes via 'p<=30').
  > DIM2 (=null): Control case -> null per rubric. Note: output correctly lists mechanism_hypotheses as an empty array, consistent with p=30<40 (no hypothesis required), so there are also no unsupported mechanism assertions to penalize under di…
  > DIM3 (=nulls): Control case -> nulls per rubric; no top-ranked hypothesis exists to map.
  > DIM4 (=3): Consistency rule check first: p=30 (<40) requires tier clear/watch; declared risk_tier='watch' -> consistent, no cap. Evidence quality: citations point at concrete provided data content with specific values and dates, e.g., CL3 q…
  > MEMORIZATION_SUSPECT_CONDITION2 (=false): (a) fails - the output does not merely list documents; it cites concrete provided data values (specific NI/CFO/AR/Assets/Liabilities figures with dates). (b) fails - no mention of any revelation, en…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_45 = FLOWERS FOODS INC (FLO, W13) — control

- 피평가자: **p=28** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Dim1: Answer key marks this a control case; output's misstatement_probability=28, which is <=30, so band score = 2 per the control rule. Dim2: Control case -> null per rubric; note the output correctly provides no mechanism_hypotheses (none…
  > Minor flaw (CL2 first evidence cites one accession for two documents) is not fabrication and does not undermine the score. Memorization_condition2: false - reasoning points at concrete provided data content throughout (specific values/dates…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_70 = MARCHEX INC (MCHX, W11) — control

- 피평가자: **p=28** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > dim1=2: Answer key group is control; output misstatement_probability=28, which satisfies p<=30 → 2. dim2=null: control case per rubric (output also correctly lists no mechanism hypotheses; none required since p=28<40). dim3=nulls: control c…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_55 = BROWN FORMAN CORP (BF-A, W14) — control

- 피평가자: **p=25** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Control case (answer key: group=control, no scheme). Dim1: output gives misstatement_probability=25; control rule p<=30 -> 2. Dim2: control -> null; note the output correctly lists no mechanism hypotheses, consistent with p=25 (<40, so none…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_57 = DARLING INGREDIENTS INC. (DAR, W12) — control

- 피평가자: **p=25** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Control case per answer key. dim1: p=25 <=30 -> 2. dim2/dim3: control -> null (output correctly has empty mechanism_hypotheses, appropriate since p<40). dim4: evidence is specific and verifiably tied to provided data (e.g., CL3 NI=64,215,00…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_58 = CINTAS CORP (CTAS, W23) — control

- 피평가자: **p=25** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > dim1=2: control case with misstatement_probability=25, which is <=30 (control band for full credit). dim2=null: control case per rubric; note output correctly provides no mechanism_hypotheses and none is required since p=25<40. dim3=nulls: …
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_41 = HEALTHSTREAM INC (HSTM, W10) — control

- 피평가자: **p=22** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Control case (answer key: group=control). dim1: output gives misstatement_probability=22; control rule p<=30 -> 2. dim2/dim3: control -> null per rubric; output appropriately has an empty mechanism_hypotheses list, so no unsupported mechani…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_42 = RALPH LAUREN CORP (RL, W22) — control

- 피평가자: **p=20** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Control case (answer key group=control). Dim1: output p=20, control rule p<=30 -> 2. Dim2: control -> null; output correctly lists no mechanism_hypotheses (also consistent with p<40). Dim3: control -> nulls. Dim4: consistency rule satisfied…
  > Minor blemishes (CL7 accession 'n/a' for a 2005 NT 10-K from the chronology; fiscal-quarter labeling in CL1) are not fabrications. Memorization condition2: false - reasoning anchors on concrete provided data values throughout, and no post-c…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_51 = Valaris Ltd (VAL, W02) — control

- 피평가자: **p=20** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > dim1=2: Answer key group is control; output misstatement_probability=20, which is <=30, earning the top control band per rubric. dim2=null and dim3=nulls: control case per rubric; output correctly provides an empty mechanism_hypotheses list…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_64 = SAIA INC (SAIA, W16) — control

- 피평가자: **p=20** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > dim1: Answer key marks this a CONTROL case. Output gives misstatement_probability=20, which satisfies the control band p<=30, so dim1=2. dim2: Control case -> null per rubric; note the output correctly lists no mechanism_hypotheses (empty a…
  > Minor nit: CL7 evidence uses accession "n/a" for chronology items, but this is a chronology observation rather than a fabricated citation and does not undermine the score.
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_50 = AtriCure, Inc. (ATRC, W20) — control

- 피평가자: **p=15** · tier=watch · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Dim1: Answer key group=control; output misstatement_probability=15, which is <=30, so control band score = 2. Dim2: Control case -> null per rubric; output correctly provides an empty mechanism_hypotheses list, consistent with p=15 (<40, no…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)

### case_53 = MARTEN TRANSPORT LTD (MRTN, W17) — control

- 피평가자: **p=15** · tier=clear · 가설(확신순):
- 채점(claude-fable-5): **d1=2** · d2=None · d3=None/None · d4=3 · mem2=False
- 채점 rationale 발췌 (verbatim, ≤6줄):
  > Control case per answer key (group=control, no scheme/genre). dim1: output's misstatement_probability=15 <=30, so band score 2. dim2: null (control). dim3: nulls (control); note mechanism_hypotheses is empty, appropriately so given p<40. di…
- **제안 처분**: finalize (대조군 정탐, 근거 명확)
- **서명**: ☑ finalize   ☐ override (사유: __________ → overrides.md)
