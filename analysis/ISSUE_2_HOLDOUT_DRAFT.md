# Issue #2 (DRAFT) — The clean test is now runnable: post-cutoff restatement events an LLM cannot have memorized

> **DRAFT — not published. Owner sign-off required. Companion to Issue #0.**
> Scoring: Claude-assisted, human-finalized (grades stay human_finalized=false until
> owner finalization). All criteria committed before the corresponding results
> existed; commit hashes are the reader's verification path. Single Claude-based
> pipeline (evaluatee: claude-sonnet-5, pinned). **Every company named here is
> labeled by a G2 provisional tier (8-K Item 4.02 non-reliance event) — we describe
> "restatement / non-reliance events", never "confirmed fraud".**

## 1. Why this issue exists

Issue #0's honest answer was constrained by rule R3: on known-fraud cases, a large
part of the LLM's score is **memory of the company, not analysis of the numbers**.
Issue #0 named the escape: a **post-training-cutoff holdout**, where the revelation
is *structurally impossible* to have been memorized because it did not exist when
the model was trained (claude-sonnet-5 knowledge cutoff: 2026-01).

As of 2026-07-07 that holdout is, for the first time, **runnable**. Three companies
announced Item 4.02 non-reliance / restatement events after the cutoff, and the
evaluatee demonstrably does **not** know about those events.

## 2. The recognition gate (the spine of the design)

Before a post-cutoff case can be used, we must *prove* the model has not memorized
its revelation. We asked the evaluatee (identity visible — this is the point) an
open, non-leaking recent-history question about each company — never stating or
hinting that any restatement occurred — and recorded whether it volunteered
knowledge of an accounting event. Transcripts: `runs/holdout/recognition/`.
Criteria pre-committed at `62d2fda` (`docs/HOLDOUT_CRITERIA.md`).

| company (ticker) | revelation | model knows the event? | admitted? |
|---|---|---|---|
| Hub Group (HUBG) | 2026-02-05 (8-K 4.02) | **No** (confidence: none) | ✅ |
| Weis Markets (WMK) | 2026-02-20 (8-K 4.02) | **No** — knew it as "a Pennsylvania supermarket chain", no knowledge of any accounting event | ✅ |
| Genie Energy (GNE) | 2026-03-12 (8-K 4.02) | **No** (confidence: none) | ✅ |

**The instrument is validated, not trivially answering "unknown".** Two positive
controls — companies with well-known *pre-cutoff* accounting events — were
recognized at high confidence with factually accurate detail:

- **Hertz (2014)**: the model correctly recounted the restatement of FY2011–2013,
  the nonfleet-cost capitalization error, Frissora's September 2014 resignation, and
  the $16M SEC penalty (Dec 2018).
- **Kraft Heinz (2019)**: it correctly recounted the October 2018 SEC subpoena, the
  ~$200M COGS understatement, the Item 4.02 non-reliance on FY2016–2017, the $15.4B
  goodwill charge, and the September 2021 SEC settlement with named executives.

So the model recognizes real accounting events when it has them — and reports
non-recognition only for the genuinely post-cutoff revelations. The critical
nuance WMK makes explicit: the model **knows the company** (identity is available)
but **not the revelation**. That is exactly the holdout premise — under this frame,
identity now adds information rather than contamination.

## 3. What this does and does not yet show

- **Shows**: three unmemorizable cases exist and pass the gate (N=3). The
  pre-committed rule H3 ("if N < 3 after gates, STOP the claim") therefore does
  **not** fire on N grounds. The clean test is feasible.
- **Does not yet show**: whether the LLM can *analytically detect* these from
  pre-revelation financials. That requires scoring each admitted case (identity
  frame primary) against matched clean controls that pass the same non-recognition
  gate, then the pre-committed small-N exact permutation test. **That scoring has
  not been run in this cycle (INCOMPLETE).** Conclusion rule H1 (permutation
  p < 0.05 → "analytical detection on unmemorizable events", G2-provisional caveat
  mandatory) / H2 (per-case scores reported beside wave-1 distributions, no
  pooling) will be evaluated after scoring.

## 4. Labeling honesty and limitations

- **All three are G2 provisional** (8-K Item 4.02). Item 4.02 is a company's own
  non-reliance determination, not an SEC finding. Monthly re-scan retro-upgrades
  tiers (G1 AAER > G2 4.02 > G3 SEC complaint > G4 DOJ). Until then: "restatement /
  non-reliance event", never "fraud".
- Scheme-type honesty (recorded, not used to exclude): WMK (inventory overstatement
  + whistleblower) and HUBG (unrecorded payable / expense understatement + executive
  terminations) read fraud-like; GNE (captive-insurance liability accounting) reads
  more error-like. This matters for interpreting any future detection result.
- HUBG sits only 5 days past the cutoff; it cleared the required direct
  recent-history screen (this gate), but the training-data boundary is inherently
  fuzzy and this caveat travels with any HUBG result.
- N is tiny and will stay tiny until more post-cutoff events accumulate — which is
  the design: `docs/FUTURE_HOLDOUT_CANDIDATES.md` is re-scanned monthly.

## 5. Framing

Opinions based solely on cited public filings (each company's 8-K). We hold no
positions, sell nothing, used no non-public information. Educational/informational
only — not investment, legal, or accounting advice. This is a single Claude-based
pipeline; the grading is Claude-assisted with human finalization.

*Companion: Issue #0 (`analysis/ISSUE_0_DRAFT.md`, the memorization finding this
holdout is designed to escape) and Issue #1 (wave-2 expansion). Gate packet:
`review_packets/RP-11_expansion_holdout.md`.*
</content>
