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
mechanical expansion and its result. The pre-registration and roster decision were
committed **before any score existed** (`9438b0c`), so the result (§5: conclusion
rule R4 fired) cannot be accused of post-hoc selection.

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

## 5. Result — conclusion rule **R4 (capability)** fired

Full pipeline executed (23 controls selected by the frozen pure function; 32 scored;
9 perturbed; 64 recognition/verbatim probes; 32 grades, all since human-finalized
— owner sign-off 2026-07-09, D24, via `review_packets/RP-13_grading_workbench.md`).
Standalone primary (9 fraud vs 23 control), reproducible via
`python analysis/wave2_analyze.py`:

- **R1 no** — permutation p = **0.00116** (mean diff +20.6pp, 55.2 vs 34.7).
- **R2 no** — Spearman ρ(LLM, M) = 0.337, ρ(LLM, F) = 0.265 (both < 0.7).
- **R3 no** — identity-perturbation crossed only **3/9** (CSC, BRX, UAA); below the
  memorization-majority bar. Wave-1 was 5/8.
- ⇒ **R4 fires**: capability demonstration on this curated set (AUC 0.829
  [0.616, 0.983], Cliff δ 0.657, flags 7/9 vs 5/23, FPR 21.7% CP [7.5%, 43.7%]).
  Framing constraint (R4): **no benchmark-comparable accuracy/AUC claim**.

**The contrast is the finding.** Wave-1's famous cases fired R3 (memorization
entangled). Wave-2's less-famous cases fire R4 — the separation survives both the
memorization check and the mechanical-baseline check, and the name-prediction probe
identifies only **25%** of wave-2 firms (vs wave-1's 50%), confirming weaker
memorization. Two misses (CSC, BRX) are themselves memorization-crossed cases.
Pooled secondary (17 vs 45, wave-1 frozen scores reused, **never a standalone
headline**): p = 3.0e-05, AUC 0.831. Full write-up: `analysis/wave2_summary.md`;
all grades human-finalized (owner sign-off 2026-07-09, D24 — 0 overrides, with
the Issue #0 rubber-stamp check explicitly confirmed).

## 6. Framing

Fraud-case descriptions restate SEC/AAER findings, not our allegations. We hold no
positions, sell nothing, used no non-public information. Educational/informational
only; not investment, legal, or accounting advice. Single Claude-based pipeline;
grading Claude-assisted with human finalization.

*Companion: Issue #0 (`analysis/ISSUE_0_DRAFT.md`) and Issue #2 (holdout). Gate
packet: `review_packets/RP-11_expansion_holdout.md`.*
</content>
