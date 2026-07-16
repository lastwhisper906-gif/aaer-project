# Do LLMs isolate accounting-misstatement signals through capability rather than memorization? — one-page summary

> Published 2026-07-11 (v1.0.0 freeze). Single Claude-based pipeline (evaluatee
> pinned to claude-sonnet-5); grading Claude-assisted, **human-finalized**. This
> result does not generalize to LLMs at large. No positions; educational /
> informational only — not investment advice.

**Question.** Given only pre-revelation public financial data (point-in-time
XBRL series and filing chronology), can an LLM distinguish companies later
charged with accounting fraud (SEC AAER ground truth) from matched
non-enforcement controls — and if it separates them, is that *analysis* or
*memory of the scandal*?

**Design.** Three tiers peeling along the memorization axis, all
**freeze-then-run**: every roster rule, grading rubric, and conclusion rule
(R1–R4, H1–H3) was committed before the corresponding scores existed — commit
hashes are the verification path. Look-ahead is blocked at code level
(`filed ≤ cutoff` per payload fact); controls run the identical protocol.

**Results (frozen).**

- **Tier 1 (wave-1: 8 famous frauds vs 22 matched controls).** Separation is
  real (permutation p = 0.00114) but pre-committed rule **R3 fired**:
  identity-perturbation deltas dominated 5/8 cases — the score is entangled
  with memorization.
- **Tier 2 (wave-2: 9 gate-decided, less-famous frauds vs 23 controls).**
  **R4 fired** (residual capability): p = 0.00116, AUC 0.829 [0.616, 0.983],
  flags 7/9 at FPR 21.7% CP [7.5%, 43.7%]. Direct probing shows the model
  *knows* the outcomes (8/9 = 88.9%), yet no pre-registered bar shows that
  knowledge functioning as score: identity-masked scores do not collapse
  (perturbation dominance 3–4/9 < 5/9 bar), and scores do not respond to
  identity manipulation (3-arm median(b−a) = +6.0pp < 10pp bar; the c-arm
  comparison is design-confounded and inter-arm deltas carry draw noise —
  directional evidence only).
- **Tier 3 (post-cutoff holdout: 3 restatement events the model cannot have
  memorized; recognition gate 0/5 per case at k=5).** One robust detection:
  Hub Group 70, ≥50 in 5/5 redraws, above all three matched controls — where
  mechanical screens (Beneish/Dechow) could not even compute. The other two
  cases show no separation (Weis 32, Genie 42), and the *highest* score in the
  holdout-era control pool is a false positive (**GRDX 78**). Directional
  existence evidence, not a capability estimate.

Name-identification gradient across tiers: 50% → 21.9% (frozen rule; 25% under
a rename-aware human reading) → 0%.

**Three-line limits.** (1) Memorization is *bounded* by four instruments with
tabulated bias directions, never eliminated (L-1, L-5). (2) Execution ran
through the Claude Code harness, single-model, with an intra-family grader
(L-2, L-6); non-determinism is banded by k=5 redraws, not removed (L-3).
(3) Holdout N=3 with one robust case; the 3-arm c-arm is design-confounded
(L-7) — full text in `docs/methodology_limitations.md` (L-1–L-7).

**What's new (2026-07-16).** First **Tier 2 live output**: an
earnings-quality memo on Gildan (GIL) built solely from filings submitted
before the 2026-06-16 short report (input cutoff code-enforced at 06-15;
selection background disclosed — a sealed pre-report replication, not a
random screening hit; 19 quotes machine-verified): **{ISSUE_URL}**.
Plus a threshold decision table: **no dominant single-threshold LLM strategy
on the trajectory layer — CP95 intervals on every cell** (detection, false
positives, and cost per detection at $0.53/screen measured;
`analysis/DECISION_TABLE.md`).

**Verify it yourself.** Repo: <https://github.com/lastwhisper906-gif/aaer-evals>
· Release (citable freeze):
<https://github.com/lastwhisper906-gif/aaer-evals/releases/tag/v1.0.0> ·
Issues 0/1/2 = GitHub issues 1/2/3 · EQ Memo #1 = {ISSUE_URL}.
`python tools/reproduce_analysis.py` recomputes every published number
(PASS 100/100).
