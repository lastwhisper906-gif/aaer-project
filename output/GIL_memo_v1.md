# Forensic Filing Review Memo — Gildan Activewear Inc. (v1)

**Company:** Gildan Activewear Inc. (NYSE: GIL / TSX: GIL), SEC CIK 0001061894
**Filings analyzed:**
[Form 40-F](https://www.sec.gov/Archives/edgar/data/1061894/000106189426000006/) (fiscal year ended 2025-12-28), filed **2026-02-26**, acc. 0001061894-26-000006 — incl. Ex-99.1 MD&A, Ex-99.2 audited financial statements & notes, Ex-99.3 Annual Information Form (AIF) ·
[Form 6-K](https://www.sec.gov/Archives/edgar/data/1061894/000106189426000013/) (Q1 2026 interim report, quarter ended 2026-03-29), filed **2026-04-30**, acc. 0001061894-26-000013 — incl. Ex-99.1 interim MD&A, Ex-99.2 condensed interim financial statements & notes
**Analysis date:** 2026-07-15 · **Model:** claude-sonnet-5 (blind two-stage run — annual filing first, then interim filing + AIF as incremental context; structured output; no tools, no browsing)
**Analysis based solely on filings filed before 2026-06-16; no news or external data accessed.**
*Companion Korean-language publication draft (same underlying results): `runs/gil_memo_v1/memo_draft.md` (commit 08be4ee).*

> **Scope and disclaimers.** This memo identifies disclosed facts and analytical observations that warrant further verification. It separates filing facts (quoted verbatim, with location) from hypotheses (the model's interpretation). It is **not** an allegation of accounting impropriety or wrongdoing by the company. No position is held in GIL securities; this document is for educational and informational purposes only and is not investment advice. Analysis: Claude-assisted, **human-finalized** (owner-signed 2026-07-16 — Q-O01/Q-O03 incl. the citation adjudication in `runs/gil_memo_v1/citation_adjudication.md` and the $201.6M derived-value note; ledger D93). Results are limited to a single Claude-based pipeline.
>
> **Citation integrity status:** 19 verbatim quotes machine-checked against raw filing text — **14 VERIFIED (exact match)**; **⚠ 5 flagged by the checker (1 ALTERED, 4 NOT FOUND)**. Manual tracing found all 5 to be ellipsis-merged quotes whose individual fragments each match the filings exactly (`grep` exact match) — **zero fabricated citations** — but per protocol the machine verdicts are reported unmodified. Flagged quotes carry a ⚠ below; full table in the Appendix.

> **Selection background (hindsight disclosure).** GIL was not selected at random. At selection time the author was aware of a short-seller report on the company (Jehoshaphat Research, published **2026-06-16** — its claims are **allegations**, which the company has denied). The model's input, however, was **code-enforced to a 2026-06-15 cutoff** (look-ahead guard, access-logged): only filings submitted before the report were used, and the report itself, news, and the selection rationale were excluded from the input. This memo is therefore **not a "random screening hit"**; it is a **sealed pre-report replication** — could the same area of signal be reconstructed from pre-report filings alone? It neither confirms nor rebuts that report; readers can compare the five flags against the public claims directly via the filing links. Access log: cutoff-guard access-verdict log, snapshot 2026-07-16, sha256 `856d50f3984d` (hash-pinned; raw log retained locally).

Flag descriptions and verification paths below are condensed from the model's output; the full, unabridged output is preserved in `runs/gil_memo_v1/flags_combined.json`. No claims were added at assembly. Descriptive statistics on which signal types moved scores in the backtest (no new claims) are in `analysis/EVIDENCE_LINES.md`.

---

## Flag 1 — GAAP net loss and doubled operating cash outflow vs. large positive "adjusted" earnings (confidence: high)

**Anomaly.** In Q1 2026 Gildan reported a GAAP net loss of $65.8M while presenting adjusted net earnings from continuing operations of $80.0M — a ~$146M swing driven substantially by the Hanes inventory fair-value step-up addback ($106.3M expensed in the quarter, $95M residual guided to unwind within ~5 months). Simultaneously, cash used in operating activities nearly doubled year-over-year, so the divergence between adjusted earnings and cash generation is widening, not normalizing, post-acquisition.

**Quotes.**
- ✅ "Net earnings (loss) | $ | (65,789) | $ | 84,682" — 6-K Ex-99.2, Statements of Earnings
- ✅ "Cash flows from (used in) operating activities | (279,474) | (142,233)" — 6-K Ex-99.2, Statements of Cash Flows
- ✅ "Adjusted net earnings from continuing operations(2) | 80.0 | 89.9" — 6-K Ex-99.1 MD&A §5.5
- ⚠ NOT FOUND (merged quote; both fragments traced verbatim): "Inventory fair value step-up cost … 106.3 | — ... The residual step up cost, of $95 million, is expected to turn over within approximately five months." — 6-K Ex-99.1 MD&A §5.4.2 / §15.0

*Assembly note (figure check):* the model's description cites "$201.6 million" as the step-up estimated in the annual filing. The 40-F MD&A states the **total** step-up as **$237 million**, of which $35.4M was expensed in FY2025; $201.6M is the derived FY2026 remainder (237.0 − 35.4), arithmetically consistent with Q1's $106.3M + $95M residual, but it is not a verbatim filing figure.

**Verification path.** Track Q2/Q3 2026 filings for full unwind of the $95M residual and for any replacement addback categories; reconcile cumulative GAAP vs. adjusted earnings vs. operating cash flow across fiscal 2026; check whether the Q1 working-capital outflow (−$254.5M, dominated by a $211.5M payables decrease) recurs.
**Confidence would change with:** a return to GAAP profitability and positive operating cash flow as the step-up unwinds (transitory) vs. continued losses or new addback categories (structural).

## Flag 2 — Hanes (~45% of net sales, majority of balance sheet) excluded from ICFR/DC&P evaluation scope (confidence: high)

**Anomaly.** The Q1 2026 MD&A discloses that management excluded Hanes from the scope of both its internal-control-over-financial-reporting and disclosure-controls evaluations, while Hanes contributed ~45% of quarterly net sales and the majority of consolidated assets ($2.3B current + $3.8B non-current). Judgment-intensive integration accounting (restructuring, facility closures, purchase-price allocation) is flowing through the books precisely during this assurance gap.

**Quotes.**
- ✅ "…we have limited the scope of our evaluation of internal controls over financial reporting (ICFR) to exclude controls over financial reporting of Hanes… In addition, we have also limited the scope of our evaluation of disclosure controls and procedures (DC&P) to exclude disclosure controls and procedures of Hanes." — 6-K Ex-99.1 MD&A §13.0
- ✅ "The net sales originating from the financial records of Hanes … represented approximately 45% of total net sales. Hanes accounted for approximately $2,313 million of current assets, $3,809 million of non-current assets…" — 6-K Ex-99.1 MD&A §13.0
- ⚠ NOT FOUND (merged quote; all three fragments traced verbatim): "…primarily reflect expenses associated with the integration of Hanes… $27.1 million for severance…$14.5 million for the write-off of equipment…" — 6-K Ex-99.2 Note 8

**Verification path.** This exclusion is a recognized transition accommodation for recent acquisitions (typically up to one year) — confirm the committed date for bringing Hanes into scope; check the FY2026 annual ICFR assessment (incl. any material weaknesses once Hanes is in scope) and the auditor's report for scope-limitation language; watch for measurement-period adjustments or corrections arising from the exclusion window.
**Confidence would change with:** the disclosed timeline for inclusion and the eventual FY2026 ICFR outcome.

## Flag 3 — Three diverging leverage ratios; headline 3.3x vs. 3.8x on private-placement covenant basis, gap widening (confidence: high)

**Anomaly.** The headline non-GAAP "net debt leverage ratio" rose to 3.3x (from 3.0x at year-end), but the same MD&A footnote discloses 3.4x on the term-loan/revolver covenant basis and 3.8x on the U.S. private-placement-notes basis — a gap that widened from 0.4x to 0.5x in one quarter. The headline ratio rests on pro-forma adjusted EBITDA that includes $472.0M of pre-ownership Hanes EBITDA (~32% of the $1,453.3M pro-forma figure), i.e., unaudited, Hanes-supplied history rather than trailing results under Gildan ownership.

**Quotes.**
- ✅ "Gildan's net debt leverage ratio as at March 29, 2026 was 3.3 times (3.0 times at December 28, 2025)." — 6-K Ex-99.1 MD&A §8.2
- ✅ "The Company's net debt to EBITDA ratio for purposes of its term loans and revolving facility was 3.4x and for purposes of U.S. private placement notes was 3.8x at March 29, 2026 (3.1x and 3.4x respectively at December 28, 2025)." — 6-K Ex-99.1 MD&A §8.2 fn (2)
- ⚠ ALTERED (merged table rows; each row traced verbatim): "Adjusted EBITDA for the trailing twelve months … 981.3 | 926.3 ... Business acquisitions(3) | 472.0 | 564.8 ... Pro-forma adjusted EBITDA … 1,453.3 | 1,491.1" — 6-K Ex-99.1 MD&A §8.2 table
- ✅ "As a result of the closing of the Hanes acquisition, our net debt leverage ratio exceeded our stated target range. Accordingly, we paused our share repurchases starting in August 2025…" — 6-K Ex-99.1 MD&A §8.2

**Verification path.** Obtain covenant maximums to compute headroom at 3.4x/3.8x; recompute leverage on actual TTM adjusted EBITDA only ($981.3M vs. net debt $4,867.6M ≈ 5.0x) as a no-pro-forma reference point; watch the $472.0M pro-forma add-on shrink to zero by ~Q4 2026 as actual Hanes results roll into the trailing window.
**Confidence would change with:** covenant thresholds/headroom and whether actual Hanes-inclusive EBITDA supports the pro-forma assumption.

## Flag 4 — Receivables factoring: off-balance-sheet balance swung −14% QoQ, driving reported AR, payables, and operating-cash-flow optics (confidence: medium)

**Anomaly.** Off-balance-sheet sold receivables fell from $777.0M to $667.3M in the quarter, and management explicitly attributes part of the AR build to "lower sales of trade accounts receivables to financial institutions." The related one-week remittance-lag payable fell $120.1M → $39.9M, contributing to the $211.5M payables decrease that drove most of the negative working-capital swing — demonstrating how discretionary factoring volume moves reported operating cash flow.

**Quotes.**
- ✅ "As at March 29, 2026, trade accounts receivable being serviced under receivables purchase agreements amounted to $667.3 million (December 28, 2025 - $777.0 million)." — 6-K Ex-99.2 Note 5
- ⚠ NOT FOUND (mid-sentence ellipsis; flanking fragments traced verbatim): "The increase in trade accounts receivable … was mainly due to … lower sales of trade accounts receivables to financial institutions under receivables purchase agreements…" — 6-K Ex-99.1 MD&A §6.1
- ✅ "Accounts payable and accrued liabilities also include balances payable of $39.9 million (December 28, 2025 - $120.1) resulting mainly from a one-week timing difference…" — 6-K Ex-99.2 Note 10 fn (1)
- ⚠ NOT FOUND (model inserted "$ |" separators absent from extract; figures and caption traced verbatim): "Accounts payable and accrued liabilities | $ | (211,526) | $ | (32,220)" — 6-K Ex-99.2 Note 14(c)

*Assembly notes (fair presentation):* (i) the largest ($975M) receivables purchase agreement "expires on June 16, 2026, **subject to annual extensions**" (6-K Ex-99.2 Note 5; same language in 40-F Ex-99.2) — the expiry cited in the verification path is extendable, not a hard stop; (ii) the filings state the company "does not retain any credit risk with respect to any trade accounts receivables that have been sold" and that sold receivables qualify for de-recognition — the flag concerns cash-flow/working-capital optics and financing dependence, not credit-risk concealment.

**Verification path.** Track the factoring balance and remittance-lag payable over coming quarters (one-off vs. wind-down, incl. around the June 2026 renewal window); regress quarterly factoring-balance changes against operating-cash-flow swings to isolate the factoring contribution; monitor renewal terms/capacity of the $975M agreement.
**Confidence would change with:** the disclosed reason for the Q1 reduction and post-renewal program terms.

## Flag 5 — Customer concentration: largest customer 33.2% of total sales, top ten 72.5%, with no minimum-purchase contracts (confidence: medium)

**Anomaly.** The AIF discloses whole-company concentration: the largest customer took 33.2% of fiscal-2025 total sales (top ten: 72.5%), amplified by the October 2024 merger of Gildan's two largest wholesale distributors (~39% of fiscal-2024 net sales combined), with no minimum-purchase commitments. Q1 2026 wholesale sales fell 11.9% on "proactive inventory reduction across customer channels," consistent with a concentrated counterparty adjusting its own inventory.

**Quotes (all ✅ VERIFIED exact).**
- "In fiscal 2025, our largest customer accounted for 33.2% of our total sales, and our top ten customers accounted for 72.5% of our total sales." — 40-F Ex-99.3 AIF, Description of the Business
- "…our contracts with our customers do not require them to purchase a minimum quantity of our products." — 40-F Ex-99.3 AIF
- "On October 1, 2024, the Company's two largest wholesale distributor customers … closed a transaction combining their businesses… increased our customer sales concentration with the combined entity to approximately 39% of our fiscal 2024 net sales." — 40-F Ex-99.3 AIF, General Development of the Business
- "Wholesale sales were $552 million compared to $626 million, down 11.9%…" — 6-K Ex-99.1 MD&A §5.4.1

**Verification path.** Reconcile the AIF's total-sales concentration against the annual FS Note 28 receivables-based concentration; establish the merged distributor's identity and standalone credit profile from public sources; track whether the wholesale decline is destocking or structural.
**Confidence would change with:** the customer's identity/financial health and subsequent-quarter wholesale trends.

---

## Appendix — Citation verification table (programmatic, `tools/blind_memo_verify.py`)

Thresholds fixed before running: VERIFIED = exact or similarity ≥ 0.95 · ALTERED ≥ 0.80 · NOT FOUND < 0.80. **Result: 14/19 VERIFIED · 1 ALTERED · 4 NOT FOUND.** Manual adjudication of the 5 non-VERIFIED rows (`runs/gil_memo_v1/citation_adjudication.md`, human signature pending): all 5 are ellipsis-merged or separator-reformatted quotes whose fragments each exact-match the filing text — 0 hallucinated citations. Machine verdicts are reported unmodified below.

| # | Quote (truncated) | Claimed location | Status | Sim | Matched doc |
|---|---|---|---|---|---|
| 1.1 | Net earnings (loss) \| $ \| (65,789) \| $ \| 84,682 | 6-K Ex-99.2, Statements of Earnings | VERIFIED | 1.0 | 6K ex99-2 FS |
| 1.2 | Cash flows from (used in) operating activities \| (279,474)… | 6-K Ex-99.2, Statements of Cash Flows | VERIFIED | 1.0 | 6K ex99-2 FS |
| 1.3 | Adjusted net earnings from continuing operations(2) \| 80.0… | 6-K Ex-99.1 MD&A §5.5 | VERIFIED | 1.0 | 6K ex99-1 MD&A |
| 1.4 | Inventory fair value step-up cost … 106.3 \| — ... residual… | 6-K Ex-99.1 MD&A §5.4.2/§15.0 | **⚠ NOT FOUND** | 0.609 | 6K ex99-1 MD&A |
| 2.1 | …limited the scope of our evaluation of internal controls… | 6-K Ex-99.1 MD&A §13.0 | VERIFIED | 1.0 | 6K ex99-1 MD&A |
| 2.2 | The net sales originating from the financial records of Hanes… | 6-K Ex-99.1 MD&A §13.0 | VERIFIED | 1.0 | 6K ex99-1 MD&A |
| 2.3 | Restructuring and acquisition-related costs … $27.1 million… | 6-K Ex-99.2 Note 8 | **⚠ NOT FOUND** | 0.740 | 6K ex99-1 MD&A |
| 3.1 | Gildan's net debt leverage ratio … was 3.3 times (3.0 times… | 6-K Ex-99.1 MD&A §8.2 | VERIFIED | 1.0 | 6K ex99-1 MD&A |
| 3.2 | …net debt to EBITDA ratio … 3.4x … 3.8x at March 29, 2026… | 6-K Ex-99.1 MD&A §8.2 fn (2) | VERIFIED | 1.0 | 6K ex99-1 MD&A |
| 3.3 | Adjusted EBITDA for the trailing twelve months … 981.3… | 6-K Ex-99.1 MD&A §8.2 table | **⚠ ALTERED** | 0.846 | 6K ex99-1 MD&A |
| 3.4 | As a result of the closing of the Hanes acquisition… | 6-K Ex-99.1 MD&A §8.2 | VERIFIED | 1.0 | 6K ex99-1 MD&A |
| 4.1 | As at March 29, 2026, trade accounts receivable being serviced… | 6-K Ex-99.2 Note 5 | VERIFIED | 1.0 | 6K ex99-2 FS |
| 4.2 | The increase in trade accounts receivable … was mainly due to… | 6-K Ex-99.1 MD&A §6.1 | **⚠ NOT FOUND** | 0.781 | 6K ex99-1 MD&A |
| 4.3 | Accounts payable and accrued liabilities also include balances… | 6-K Ex-99.2 Note 10 fn (1) | VERIFIED | 1.0 | 6K ex99-2 FS |
| 4.4 | Accounts payable and accrued liabilities \| $ \| (211,526)… | 6-K Ex-99.2 Note 14(c) | **⚠ NOT FOUND** | 0.792 | 6K ex99-2 FS |
| 5.1 | …largest customer accounted for 33.2% of our total sales… | 40-F Ex-99.3 AIF | VERIFIED | 1.0 | 40F ex99-3 AIF |
| 5.2 | …contracts with our customers do not require them to purchase… | 40-F Ex-99.3 AIF | VERIFIED | 1.0 | 40F ex99-3 AIF |
| 5.3 | On October 1, 2024, the Company's two largest wholesale… | 40-F Ex-99.3 AIF | VERIFIED | 1.0 | 40F ex99-3 AIF |
| 5.4 | Wholesale sales were $552 million compared to $626 million… | 6-K Ex-99.1 MD&A §5.4.1 | VERIFIED | 1.0 | 6K ex99-1 MD&A |

*Learning note: without a schema constraint forcing each quote to be a single contiguous passage, the model produces "…"-merged quotes that a string verifier misclassifies as NOT FOUND — verifier v2 should split on ellipses and match fragments. This run's pre-fixed criteria were kept and the raw verdicts published.*
