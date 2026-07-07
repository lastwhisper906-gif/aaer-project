# Issue #1 (DRAFT) — Wave 2: expanding the fraud case set from 8 to a gate-decided roster

> **DRAFT — not published. Owner sign-off required. Companion to Issue #0.**
> Scoring: Claude-assisted, human-finalized. All roster rules and the analysis plan
> were committed **before any wave-2 score existed** (`9438b0c`); commit hashes are
> the reader's verification path. Single Claude-based pipeline (evaluatee:
> claude-sonnet-5, pinned). Wave-2 is an **independent sample**; frozen wave-1
> (8-vs-22) results are neither re-scored nor pooled as a headline.

## 1. The question this issue will answer (and its honest current status)

Issue #0 rests on N = 8 fraud cases. The obvious first strengthening is more cases,
drawn by the *same* frozen rules — no cherry-picking. This issue records the
mechanical expansion. **Its statistical result is not yet in: the wave-2 scoring
has not been run in this cycle (INCOMPLETE).** What *is* done is the part that must
precede any score — the pre-registration and the roster decision — so that the
eventual result cannot be accused of post-hoc selection.

## 2. The roster is a rule, not a choice

Committed before any score (`EXCLUSION.md`, `9438b0c`):

1. Start from the frozen kill-switch A-type list of **23** (all owner-signed,
   `data/candidates/candidates.json`).
2. Minus the **8** already scored in wave-1.
3. Minus **2** worked-example-contaminated cases (**Valeant, General Electric**) —
   the scoring criteria were built while studying these with answer keys; scoring
   them would test on tuning data. This exclusion protects the *value* of the
   result, not process.
4. Apply the frozen gates (XBRL availability + pre-cutoff coverage, revelation-date
   verification, document integrity). **We let the gates decide — no case was
   pre-judged.**

## 3. What the gates decided

The G-XBRL gate was run empirically: fetch each candidate's SEC companyfacts, then
assemble the pre-cutoff point-in-time series with the frozen loader and measure
coverage (`190783b`). Result — **9 survive, 4 fail, each for a demonstrated
reason**:

| outcome | tickers | reason |
|---|---|---|
| **survive (9)** | BRX, CGI, CSC, HAIN, MDXG, OSIR, TNGO, UAA, WFT | usable pre-cutoff PIT series |
| fail | PUDA | no companyfacts at all (China-RTO, not in data.sec.gov) |
| fail | MILL | first us-gaap fact filed 70 days *after* cutoff (XBRL adoption postdates the scheme window) |
| fail | DMND | first fact filed ~1 year after cutoff ("hand-extracted cost" flag, confirmed) |
| fail | PWE | Canadian 40-F / IFRS filer — no us-gaap tags before 2018 |

Two coverage caveats travel with the survivors: **BRX** (a REIT) lacks the standard
Revenues tag and passes on net-income + assets; **OSIR** has thin quarterly
net-income coverage and passes on revenue. Both are flagged for scoring
interpretation. The China-RTO memorization-risk pre-tag applies to no survivor
(the only China-RTO case, PUDA, failed the XBRL gate).

Combined with wave-1's 8, a completed wave-2 would bring the fraud set to **~17**.

## 4. The analysis plan is the frozen plan, re-applied

`analysis/ANALYSIS_PLAN_WAVE2.md` (committed `9438b0c`) invents no new test: it
re-applies wave-1's permutation test (100k, seed-fixed), Fisher exact at the frozen
p ≥ 50 flag threshold, Cliff's δ, unstable-labeled bootstrap AUC, and the
rule-of-three FPR language, with conclusion rules R1–R4 **verbatim**. Wave-2
STANDALONE is the primary; a pooled wave1+wave2 secondary is reported only
alongside standalone, never as a headline. Scoring order is committed alphabetical,
so any time-truncation is outcome-independent. One identity-perturbed draw per
fraud case is pre-committed (first casualty of the time-degradation ladder). A
memorization-stratified comparison (perturbation Δ, recognition + name-prediction
probes) is pre-specified.

## 5. Status and next step (honest)

- **Done**: pre-registration, worked-example exclusions, gate-decided roster of 9,
  survivor XBRL fetched and integrity-manifested.
- **INCOMPLETE**: control selection (frozen pure function, 2–3 per case, deduped
  against the existing 22), payload build, scoring + probes + graders
  (human_finalized=false), and the standalone/pooled analysis. Resume procedure:
  `review_packets/RP-11_expansion_holdout.md` §6. Until scored, **no conclusion
  rule has fired** and this issue makes no separation claim.

## 6. Framing

Fraud-case descriptions restate SEC/AAER findings, not our allegations. We hold no
positions, sell nothing, used no non-public information. Educational/informational
only; not investment, legal, or accounting advice. Single Claude-based pipeline;
grading Claude-assisted with human finalization.

*Companion: Issue #0 (`analysis/ISSUE_0_DRAFT.md`) and Issue #2 (holdout). Gate
packet: `review_packets/RP-11_expansion_holdout.md`.*
</content>
