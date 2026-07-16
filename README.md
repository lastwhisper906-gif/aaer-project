# AAER Evals — Backtesting a Conflict-Free Accounting-Quality Signal

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> All results are scoped to a single Claude-based pipeline (evaluatee pinned to
> claude-sonnet-5; PROJECT.md §5-5). **These controls BOUND memorization risk;
> they do not eliminate it.** 한국어 원문: [README.ko.md](README.ko.md).

## What this is

Independent signals on public-company accounting quality are a structural gap:
auditors are paid by the auditee, sell-side analysts have banking relationships,
rating agencies are paid by issuers. This repository is a backtest of one device
aimed at that gap — **can an LLM screen for misstatement risk from point-in-time
structured disclosure data alone?** — measured against SEC enforcement (AAER)
confirmed cases with matched non-enforcement controls, and independently
validated on a post-training-cutoff holdout where memorization is structurally
impossible. No positions · educational/informational · not investment advice.

## Publication (v1.0 — 2026-07-11, owner-signed D40/D41)

The three-issue series is published as GitHub Issues (series numbering 0/1/2;
GitHub numbers 1/2/3). The posted issues are the publication surface; the
`analysis/ISSUE_*_DRAFT.md` files are their frozen source texts.

- **Issue 0** (wave-1, R3 — memorization-entangled separation):
  <https://github.com/lastwhisper906-gif/aaer-evals/issues/1>
- **Issue 1** (wave-2, R4 — residual capability, scoped):
  <https://github.com/lastwhisper906-gif/aaer-evals/issues/2>
- **Issue 2** (post-cutoff holdout, H2 — the un-memorizable axis):
  <https://github.com/lastwhisper906-gif/aaer-evals/issues/3>
- **Citable freeze point**: release
  [v1.0.0](https://github.com/lastwhisper906-gif/aaer-evals/releases/tag/v1.0.0)
  (annotated tag; frozen numbers as published).

## Headline — three layers, peeling along the memorization axis

Conclusions fire by **pre-committed** machine rules R1–R4 / H1–H3, committed
before any score existed (freeze-commit-then-run). The three layers are ordered
by "how memorizable are these cases":

**The backbone claim is deliberately not an AUC comparison.** It is this:
**separation significance survives standalone, within each layer independently,
as the memorization signal is progressively removed** — wave-1 perturbed
(identity-masked) permutation p = 0.0021; wave-2 standalone permutation
p = 0.00116; and in the post-cutoff holdout, detection persists where
memorization is impossible (recognition gate 3/3 non-recognition, draw-1;
k=5 re-probe: knows_event 0/5 per case). Each layer's
p-value is computed on that layer alone; no layer borrows significance from
another. (Pooled wave-1+wave-2 figures such as p=3.0e-05 are secondary,
reported only alongside the standalone per-wave numbers.)

**① Famous cases (wave-1, 8 treatment vs 22 control) → R3 (memorization-entangled).**
The LLM separates confirmed misstatement cases from controls, but its scores are
entangled with what the model *remembers* about each company. **Read the
perturbed (identity-masked) frame first** — it is the *less-contaminated*
measurement, **not a clean lower bound** of ability: residual identity
recognition persists after perturbation (5–6 of 8 treatment cases named across
recognition-probe draws — L-5). The only structural lower bound in this design
is the post-cutoff holdout (layer ③):
- Perturbed frame: permutation p = **0.0021** / AUC 0.864 [0.722, 0.969] / flags 4/8.
- Identity-exposed (original, entangled upper line): p = **0.00114** (100k,
  one-sided) / mean gap **+19.8pp** (median 57.5 vs 33.0).
- Memorization decomposition: 5 of 8 cases exceed the R3 threshold; anonymized-
  payload name-identification rate **50%**.

**② Less-famous cases (wave-2, 9 treatment vs 23 control) → R4 (residual ability).**
Weak memorization signal, R3 does not fire → separation suggests residual
ability not explained by memorization or mechanical signals:
- Standalone permutation p = **0.00116** / mean gap **+20.6pp** / flags 7/9.
- Name-identification **21.9%** (frozen name_match rule; human read 25% co-reported
  — single boundary case DAR, `analysis/synthesis.json` §reconcile) = **half of
  wave-1**. Identity-vs-perturbed dominance 3/9 (below majority) → R3 does not
  fire. **R4 framing constraint**: no benchmark-accuracy/AUC-comparison claims.
- **Outcome-recognition probe (identity-exposed, run 2026-07-10, pre-registered
  D34 — branchless, not an R/H input): the model recalls the
  enforcement/restatement event for 8 of 9 treatment cases (88.9%, CP
  [51.7%, 99.7%]) vs 0/23 controls (CP [0%, 14.8%]).** Five cases are
  event-known-but-not-nameable from the anonymized payload (name-ID
  false-negative direction). Honest scoping: the "half of wave-1" reading
  belongs to the name-ID instrument only — on the direct instrument, the
  identity-exposed frame (the published primary) operated with outcome
  knowledge broadly available. R4 is unchanged (its input is perturbation
  dominance 3/9, not this probe). `analysis/outcome_recognition_results.json`.
- **Identity 3-arm experiment (pre-registered D36, run 2026-07-10)**: scoring
  the same perturbed payloads under fabricated company names (collision-screened
  against all 1,049,982 EDGAR filer names). **The primary evidence is the b−a
  contrast (+6.0pp median)** — same perturbed payload, only the name tokens
  differ: the single clean causal contrast in the design. **The c−b contrast
  (−2.0pp median) is a secondary, confounded observation** — arm (c) restores
  both the real name and the real (unperturbed) numbers, blending the identity
  effect with a scale-restoration effect. Resolution limit: arms (a) and (c)
  are past frozen draws while (b) is a new draw, so inter-arm comparisons carry
  draw noise (per-case 5-draw bands span 12–18pp ≈ ±10pp, E5 §7) — the ±6pp
  median is a directional readout within that resolution. Both medians sit
  under the pre-registered 10pp bar → pre-registered reading **(ii):
  directional evidence that memorization's score contribution is small on this
  set (a≈b≈c; N=9, directional only — no causal claim)**.
  `analysis/identity_3arm_results.json` · limitation L-7.

**③ Post-cutoff holdout (memorization structurally impossible; HUBG·WMK·GNE) → H2 (per-case, N=3).**
Recognition gate 3/3 non-recognition (demonstrated non-memorization of the
disclosure events; draw-1). **Gate elevated to k=5 (run 2026-07-10, rules
pre-committed): knows_event 0/5 for each of HUBG·WMK·GNE — holdout eligibility
robust to draw noise under the pre-committed ≤1/5 rule; positive control HTZ
re-verified True.** The signal **weakens but does not collapse**. All three
companies carry provisional (G2) restatement labels — all three Big R (Item 4.02
non-reliance), mechanically verified (`analysis/label_tags_holdout.json`) — not
confirmed enforcement:
- Per-case: **HUBG p=70 (flagged)** · GNE 42 · WMK 32 — all G2-provisional
  restatement events, labels pending any 4.02/AAER upgrade.
- **k=5 redraw band (E5 §7, run 2026-07-09; published values remain draw-1):
  HUBG p=70 [5-draw range 58–76, ≥50 in 5/5 → robust under the pre-committed
  ≥4/5 rule]** · WMK 32 [28–42, 0/5] · GNE 42 [30–42, 0/5] — zero flips.
- **Matched controls (E1, run 2026-07-09 under supervision, D26)**: HUBG's 70
  sits **above all three of its matched controls** (RXO 42 · Brink's 30 ·
  XPO 20); WMK and GNE show no separation from theirs (1 of 3 cases separates;
  `analysis/holdout_controls_results.json`). Control flag rate 2/9 = 22.2%,
  Clopper-Pearson 95% [2.8%, 60.0%]. Exact permutation p = 0.20 is context
  only (N=3, under-powered — pre-declared). **The single highest score in the
  holdout tier belongs to a control false positive (GridAI, GRDX, 78)** —
  HUBG (70) tops its own matched controls but not the pooled control set.
- **HUBG was detected where the mechanical screens (Beneish M, Dechow F) could
  not even be computed due to missing inputs** → the LLM signal is not a
  replica of M/F.
- Honesty note (error-anatomy P1): the HUBG hit is **tier-correct /
  mechanism-missed** (dim2=1 — anchored to the 2018 restatement cluster, not
  the 2026 restatement's actual mechanism). Risk screening ≠ forensic
  mechanism detection.
- **H1 (permutation significance) is not claimed at N=3** (under-powered).

**Memorization dose-response (secondary, gradient read — now two axes).** On
the name-ID proxy, the axis halves and vanishes (50% → 21.9% → 0%) while the
separation AUC point estimates barely move — 0.824 [0.599, 0.983] → 0.829
[0.616, 0.983] — and holdout detection persists. **On the direct
outcome-knowledge instrument (aligned with the holdout gate; wave-1 unmeasured),
the axis reads wave-2 88.9% → holdout 0% — memorization removal happens between
wave-2 and the holdout, not between wave-1 and wave-2** (`analysis/synthesis.md`
§1, two-axis table).
**The CI widths forbid any statistical equivalence claim about the AUCs**; this
is a gradient reading across three samples that differ in era, fame, and label
tier — not a controlled experiment. The load-bearing evidence is the standalone
per-layer significance above, not this AUC comparison
(`analysis/synthesis.md`, `fig_memorization_doseresponse.png`).

## False positives — over-interpretation, not hallucination (honesty record)

- wave-1 FPR **3/22 = 13.6%**, Clopper–Pearson 95% **[2.9%, 34.9%]** · wave-2
  FPR **5/23 = 21.7%**, CP **[7.5%, 43.7%]** · holdout matched controls (E1)
  FPR **2/9 = 22.2%**, CP **[2.8%, 60.0%]**. **We do not report an FPR of
  "0%."** The point estimates worsen, but the CP intervals overlap heavily
  — worse-but-not-provably.
- All 5 wave-2 false positives are grader-verified as evidence-grounded (dim4
  upper band) — **not fabricated numbers (hallucination) but positive
  misreadings of real figures** (normal structural/ratio divergence promoted to
  risk). The E1 control flags (2/9) follow the same pattern. The trust boundary
  is base-rate/calibration, not hallucination
  (`analysis/error_analysis_wave2_holdout.md`).
- Calibration: wave-2 ECE **0.179** (same order as wave-1's 0.209 — no
  improvement, null-ish).

## Mechanical baselines (R2 does not fire)

Same 30 companies, same point-in-time data: Beneish M p=0.498/AUC 0.510 ·
Dechow F p=0.268/AUC 0.573 — the quantitative screens show no separation on
this sample. LLM rankings are essentially uncorrelated with both (wave-1
ρ −0.075/−0.144; wave-2 0.337/0.265) and residual separation survives →
pre-committed R2 does **not** fire. The LLM is not reproducing the mechanical
formulas.

## Grading & finalization status

- Grading: **Claude-assisted + human final sign-off.** Evaluatee
  **claude-sonnet-5** (pinned, served-model verified per call, 0 pin
  mismatches). Grader claude-fable-5.
- **All grades are `human_finalized=true`**: wave-1 26 (frozen earlier) +
  wave-1 controls 22 + wave-2 32 + holdout 3 (owner sign-off 2026-07-09, D24 —
  0 overrides, with the Issue #0 §9 rubber-stamp check explicitly confirmed) +
  holdout matched controls 9 (D26). Overrides ledger: `scoring/overrides.md`;
  workbench: `review_packets/RP-13_grading_workbench.md`.

## Extension experiments E1–E5 (pre-registered — freeze-then-run)

All experiments were pre-registered and committed before scoring
(`analysis/*_PLAN.md`, commit `c1b85a7`):
- **E1** Holdout matched controls — **executed under supervision 2026-07-09
  (D26)**: of 3 holdout cases, only HUBG separates from its matched controls;
  control flag rate 2/9 (H1 still not claimed at N=3).
- **E2** Earliness (quarterly detection lead time, filing-aligned snapshots).
- **E3** wave-2 perturbation redraws (defends R4 against draw noise —
  median-dominance ≥5/9 would let R3 supersede R4; rule decides). **Executed:
  3/9 → R4 retained.**
- **E4** Cross-model (**EXPLORATORY** — claude-opus-4-8, limitations-footnote only).
- **E5** wave-2 main-scoring redraw (stability band; published draw-1
  immutable) — **§7 holdout arm executed 2026-07-09 (D27): HUBG ≥50 in 5/5
  draws → robust**; the wave-2 arm remains lowest priority.

Execution status & metered spend gates: `docs/OWNER_QUEUE.md` (Q-E01) ·
`docs/RESUME.md`. **No experiment result is published without the owner gate.**

## Governance map (reading order)

1. `PROJECT.md` — single reference document (methodology §5, collaboration
   model §7, scope guard §8)
2. `CLAUDE.md` — session guardrails · `scoring/decisions_log.md` — decision
   ledger + freeze hashes
3. `scoring/overrides.md` — overrides/signatures/gates (incl. OWNER-GATE-E)
4. `review_packets/INDEX.md` · `RP-11_expansion_holdout.md` · `RP-10_final.md`
   — audit entry points
5. Published issue source texts: `analysis/ISSUE_0_DRAFT.md`
   (wave-1) · `ISSUE_1_WAVE2_DRAFT.md` (R4) · `ISSUE_2_HOLDOUT_DRAFT.md` (H2)
   — owner-signed and posted 2026-07-11 (D40/D41; URLs in the Publication
   section above).

## Reproducing the numbers (third-party verification)

```bash
pip install -r requirements.txt
python tools/reproduce_analysis.py   # recompute every published number → PASS/FAIL (100/100)
python tools/verify_blindness.py     # grading-precedence proof · name/canary scan · runs/ sha256
python tools/verify_manifest.py      # data manifest check (429 files)
python analysis/synthesis.py         # cross-wave synthesis (deterministic, seed 20260708)
```

All four use committed artifacts only (0 API calls, no source corpus needed) —
CI verifies every push. Raw: `runs/` (sha256 manifest) · `scoring/grades*/` ·
`scoring/probe_results*/` · `logs/run_*/` (per-call served model, isolation
flags, freeze hashes).

## Limitations (full text: docs/methodology_limitations.md)

L-1 Model-internal knowledge cannot be blocked — only measured and disclosed.
L-2 The execution layer runs through the Claude Code harness (not the raw API).
L-3 Sampling parameters cannot be pinned — each case judgment is a point
estimate from a non-deterministic sample. L-4 Isolation is verified per-run by
gates. **L-5 Perturbation scatters memorized NUMBERS; it does not remove
IDENTITY recognition** — the name-ID rate is the evidence, and every positive
result is a value under residual contamination. L-6 Grader (claude-fable-5) and
evaluatee (claude-sonnet-5) are the same model family — same-family leniency
cannot be excluded; mitigated by 100% human sign-off (§7) and prospectively by
E4 cross-model (EXPLORATORY). **L-7 In the identity 3-arm experiment, the c−b
contrast is design-confounded** (arm (c) restores real name *and* real numbers
— identity effect blended with scale restoration); only b−a is a clean
contrast, and inter-arm deltas carry draw noise (≈±10pp per-case bands).
Selection/survivorship: the treatment group is a
survivor sample of "cases that reached enforcement"; control labels mean
"non-enforcement," not "clean" (Dyck–Morse–Zingales: ~10% of large firms in
securities fraud annually, only ~⅓ detected — specificity is biased downward,
so false-positive results are conservative by that amount).

## What this is NOT

An existence proof attempt, not a performance estimate (precision/recall %
headlines deliberately absent — wide confidence intervals, no comparable
real-company benchmark, R4 framing constraint). Single-analyst (+AI) output,
prior to external replication/audit. Evaluatee calls run through a harness and
may differ from raw-API reproduction. Case judgments are non-deterministic
samples. Pooled wave-1+wave-2 figures (p=3.0e-05 etc.) are **secondary,
co-reported only** — standalone per-wave conclusions are the headline. This
makes no claims about any specific company — outputs about current/G2
companies never use "fraud/manipulation" language (§6) — and it is emphatically
not investment advice.
