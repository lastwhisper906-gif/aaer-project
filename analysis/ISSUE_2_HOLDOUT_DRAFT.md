# Issue #2 — The clean test is now runnable: post-cutoff restatement events an LLM cannot have memorized

> **PUBLISHED 2026-07-11 (owner-signed, D40/D41)** →
> <https://github.com/lastwhisper906-gif/aaer-evals/issues/3>. This file is the
> frozen source text; the posted issue is the publication surface. Companion to Issue #0.
> Scoring: Claude-assisted, human-finalized (holdout grades owner-signed 2026-07-09,
> D24; matched-control grades D26). All criteria committed before the corresponding results
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

**Gate elevated to k=5 (2026-07-10; rules and interpretations pre-committed at
`analysis/GATE_K5_PLAN.md` before any probe call).** Re-probing each admitted
company four more times: knows_event **0/5 per case** (HUBG · WMK · GNE), with
the Hertz positive control re-verified True at high confidence. Under the
pre-committed rule (≥2/5 recognitions would have revoked eligibility), the
admission of all three cases is **robust to draw noise**. The published gate
value remains the draw-1 3/3; the k=5 band is co-reported, never a replacement.

## 3. What the scoring shows (conclusion rule H2)

Each admitted case was scored identity-visible (memorization of the revelation is
impossible by construction; the gate proved non-recognition) on pre-revelation
point-in-time data (cutoff = day before the 8-K). Results (`analysis/holdout_summary.md`):

| company (G2) | cutoff | LLM score (0–100, ordinal) | 5-draw band (k=5) | flagged (≥50)? | grade d1/d2 | Beneish M / Dechow F |
|---|---|---|---|---|---|---|
| **Hub Group** (unrecorded payables, exec terminations) | 2026-02-04 | **70** | [58–76], ≥50 in **5/5** | **yes** | 2 / 1 | uncomputable / uncomputable |
| Weis Markets (inventory overstatement, whistleblower) | 2026-02-19 | 32 | [28–42], 0/5 | no | 0 / 0 | uncomputable / 0.25 |
| Genie Energy (captive-insurance liability error) | 2026-03-11 | 42 | [30–42], 0/5 | no | 0 / 0 | −2.05 / 0.36 |

Published per-case values remain draw-1 (the pre-registered protocol; redraws form a
stability band, never a replacement). Under the pre-committed rule (§7 of
`analysis/W2_MAINSCORE_REDRAW_PLAN.md`, logged amendment committed before any redraw
call), Hub Group's flag is **robust to draw noise** (≥50 in 5/5 draws, threshold 4/5);
neither Weis nor Genie flipped to ≥50 in any draw.

- **H3's N<3 STOP does not fire** (N=3 admitted).
- **H1 not claimed**: at N=3, a fraud-vs-control permutation is structurally
  underpowered; we make no significance claim (H1's qualification isn't met).
- **H2 fires** (per-case, no pooling): Hub Group's 70 sits at the top of the
  treatment (confirmed-AAER) score range (wave-1 median 57.5, wave-2 58; controls
  ~34); Weis (32) reads control-like; Genie (42) is borderline. On genuinely
  unmemorizable events, **detection is real on the strongest misstatement-like case
  but modest and mixed** (1 of 3 flagged). The mechanical screens could not even
  compute Hub Group's M/F — so the LLM's flag is **not** a Beneish/Dechow echo.
  (Honest caveat, P1: HUBG's flag is tier-correct but mechanism-mismatched — dim2=1,
  anchored on a stale 2018 amendment cluster, not the 2026 event; risk-screening,
  not forensic-mechanism detection.)

This is the honest crux: strip memorization entirely, and the score does not
collapse to noise — the most misstatement-like case is still caught — but the signal
is weaker than on memorized cases. **After E1, the holdout evidence rests on a
single robust case (HUBG — above all three matched controls, ≥50 in 5/5 redraws);
the other two cases show no separation.** That independently confirms Issue #0's R3 headline
("separation is part memory, part analysis") on the axis where memory is impossible.
N is tiny; this is directional existence evidence, not a capability estimate.

### 3b. Matched controls (E1, pre-registered — run 2026-07-09 under supervision)

Each holdout case was paired with 3 size→SIC→fiscal-year-end matched, non-enforcement
2026-era companies (frozen pure-function selection; one candidate, Forward Air, was
dropped by the recognition gate — knows_event=true — and the next-ranked alternate
promoted). All 9 admitted controls scored under the identical identity frame and
cutoffs (`analysis/holdout_controls_results.json`):

| holdout case | its score | matched controls (score) | separates? |
|---|---|---|---|
| **Hub Group** | **70** | RXO 42 · Brink's 30 · XPO 20 | **yes — above all three** |
| Weis Markets | 32 | Grocery Outlet 58 · Sprouts 32 · Village Super Market 12 | no (tied/below) |
| Genie Energy | 42 | GridAI 78 · Via Renewables 35 · Unitil 20 | no (below top control) |

- Control false-positive rate: **2/9 = 22.2%**, Clopper-Pearson 95% **[2.8%, 60.0%]**
  — overlapping wave-1 (3/22) and wave-2 (5/23) intervals; no cross-wave comparison
  claimed. The two elevated controls are non-enforcement companies; their scores are
  opinions on risk posture, not findings of any kind.
- **The single highest score in the holdout tier belongs to a control false
  positive (GridAI, GRDX, 78)** — HUBG (70) tops its own matched controls but
  not the full nine-company control set. Any reading of the HUBG detection must
  carry this fact alongside it.
- Exact permutation p = 0.20, **context only** (N=3 is structurally underpowered —
  pre-declared; H1 remains unclaimed).
- Net honest reading: the matched-control comparison **strengthens the Hub Group
  detection specifically** (it tops its matched distribution) and leaves the other
  two cases without separation — consistent with §3's "modest and mixed."

## 4. Labeling honesty and limitations

- **All three are G2 provisional — and all three are Big R restatements** (an
  8-K Item 4.02 non-reliance determination accompanies each event; mechanically
  verified with accession-level evidence in `analysis/label_tags_holdout.json`).
  Item 4.02 is a company's own non-reliance determination, not an SEC finding —
  and base rates cut against over-reading it: only ~2.2% of restatements are
  linked to SEC enforcement (Karpoff et al., TAR 2017). Monthly re-scan
  retro-upgrades tiers (G1 AAER > G2 4.02 > G3 SEC complaint > G4 DOJ), with a
  pre-registered 4-year monitoring window per case (to 2030-02/02/03); window
  expiry without enforcement will itself be reported as label-noise data. Until
  then: "restatement / non-reliance event", never "fraud".
- Scheme-type honesty (recorded, not used to exclude): WMK (inventory overstatement
  + whistleblower) and HUBG (unrecorded payable / expense understatement + executive
  terminations) read misstatement-like (aggressive-accounting profile); GNE
  (captive-insurance liability accounting) reads more error-like. This matters for
  interpreting any future detection result. (G2 provisional — "fraud" not used, §6.)
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
