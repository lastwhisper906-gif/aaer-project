# AAER Evals — Backtesting a Conflict-Free Accounting-Quality Signal

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> Who did what: [CONTRIBUTIONS.md](CONTRIBUTIONS.md) (AI-vs-human table, D106 ⑤).
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

## Three tasks, three evidence tiers (D106 ④ — task separation)

This repository contains **three distinct benchmark tasks** (TASK 1 / TASK 2 /
TASK 3 below). They differ in label strength and memorization exposure, and
**performance claims are never aggregated across them** — every results
sentence below carries its task tag, and detections are never summed across
tiers into a headline number.

- **TASK 1 — AAER enforcement-linked historical benchmark** (wave-1 ①,
  wave-2 ②). Strong labels (SEC-enforcement-confirmed), but measured
  memorization risk: on the direct outcome-knowledge instrument the model
  recalls the enforcement/restatement event for **8 of 9 wave-2 treatment
  cases (88.9%)** (wave-1 unmeasured on that instrument; wave-1
  anonymized-payload name-identification **50%**, wave-2 **21.9%**). Task-1
  results are readings under disclosed residual contamination (L-1/L-5).
- **TASK 2 — Restatement/4.02 non-reliance early-warning benchmark**
  (post-cutoff holdout ③: HUBG·WMK·GNE). Provisional Big-R labels — **these
  are NOT confirmed fraud and not enforcement outcomes**; they are
  non-reliance restatement events. Low memorization risk (knows_event 0/5
  per case, pre-committed gate). N=3 — per-case evidence only.
- **TASK 3 — Earnings-quality monitoring** (GIL memo `output/GIL_memo_v1.md`,
  forward watchlist `specs/FORWARD_WATCHLIST_V1.md`). **Exploratory only — no
  performance claims are permitted on this task** until sealed prospective
  cycles resolve (first seal 2026-11-15).

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
- **Decision table** (owner-signed 2026-07-16, D94): what a threshold buys —
  detection, false positives, and cost per detection across four frozen data
  layers (L1/L2 = TASK 1 · L3 = TASK 2 · L4 = exploratory E2); cells are
  per-layer and never summed across layers. **No dominant single-threshold LLM
  strategy on the trajectory layer — CP95 intervals on every cell**.
  [`analysis/DECISION_TABLE.md`](analysis/DECISION_TABLE.md)
- **Citable freeze point**: release
  [v1.0.0](https://github.com/lastwhisper906-gif/aaer-evals/releases/tag/v1.0.0)
  (annotated tag; frozen numbers as published).

### Post-publication notice (2026-07-20) — partial de-identification of the v1 perturbed frame

v1 remains frozen; no original result is recomputed. The v1 perturbed frame
removed names/tickers/CIK and rescaled values but **retained original SEC
accession numbers and real filing chronology** — it is **partially
de-identified**, not fully identity-masked, so published recognition rates
cannot be attributed solely to financial-pattern reconstruction. Details:
[`docs/V1_PARTIAL_DEIDENTIFICATION_NOTE.md`](docs/V1_PARTIAL_DEIDENTIFICATION_NOTE.md).

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

**① [TASK 1] Famous cases (wave-1, 8 treatment vs 22 control) → R3 (memorization-entangled).**
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

**② [TASK 1] Less-famous cases (wave-2, 9 treatment vs 23 control) → R4 (residual ability).**
Weak memorization signal, R3 does not fire → separation suggests residual
ability not explained by memorization or mechanical signals:
- Standalone permutation p = **0.00116** / mean gap **+20.6pp** / flags 7/9.
- Name-identification **21.9%** (frozen name_match rule; human read 25% co-reported
  — single boundary case DAR, `analysis/synthesis.json` §reconcile) = **half of
  wave-1**. Identity-vs-perturbed dominance 3/9 (below majority) → R3 does not
  fire. **R4 framing constraint**: no benchmark-accuracy/AUC-comparison claims.
- **Outcome-recognition probe (identity-exposed, D34, branchless): the model
  recalls the enforcement/restatement event for 8 of 9 treatment cases (88.9%,
  CP [51.7%, 99.7%]) vs 0/23 controls.** The "half of wave-1" reading belongs
  to the name-ID instrument only; on the direct instrument the published
  identity-exposed frame operated with outcome knowledge broadly available.
  R4 unchanged (its input is perturbation dominance 3/9). Full scoping:
  `analysis/outcome_recognition_results.json` · `analysis/synthesis.md` §1.
- **Identity 3-arm experiment (D36)**: primary evidence is the b−a contrast
  (+6.0pp median; fabricated names, same perturbed payload); the c−b contrast
  (−2.0pp) is a **confounded** secondary observation (arm (c) restores name
  *and* numbers), and inter-arm deltas carry **draw noise** (≈±10pp per-case
  bands, E5 §7). Both medians under the pre-registered 10pp bar →
  reading (ii): directional-only, no causal claim.
  `analysis/identity_3arm_results.json` · `analysis/synthesis.md` · L-7.

**③ [TASK 2] Post-cutoff holdout (memorization structurally impossible; HUBG·WMK·GNE) → H2 (per-case, N=3).**
Recognition gate 3/3 non-recognition (demonstrated non-memorization of the
disclosure events; draw-1). **Gate elevated to k=5 (run 2026-07-10, rules
pre-committed): knows_event 0/5 for each of HUBG·WMK·GNE — holdout eligibility
robust to draw noise under the pre-committed ≤1/5 rule; positive control HTZ
re-verified True.** The signal **weakens but does not collapse**. All three
companies carry provisional (G2) restatement labels — all three Big R (Item 4.02
non-reliance), mechanically verified (`analysis/label_tags_holdout.json`) — not
confirmed enforcement:
- Per-case: **HUBG score 70 (0–100 ordinal; flagged)** · GNE 42 · WMK 32 — all G2-provisional
  restatement events, labels pending any 4.02/AAER upgrade.
- **k=5 redraw band (E5 §7, run 2026-07-09; published values remain draw-1):
  HUBG score 70 [5-draw range 58–76, ≥50 in 5/5 → robust under the pre-committed
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

**Memorization dose-response (secondary, gradient read — now two axes).**
*Task-tier note: this paragraph juxtaposes TASK 1 (waves) and TASK 2 (holdout)
solely to read the memorization gradient — it is not a pooled performance
claim, and detections are not summed across the two tasks.* On
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

- [TASK 1] wave-1 FPR **3/22 = 13.6%**, Clopper–Pearson 95% **[2.9%, 34.9%]** ·
  [TASK 1] wave-2 FPR **5/23 = 21.7%**, CP **[7.5%, 43.7%]** · [TASK 2] holdout
  matched controls (E1) FPR **2/9 = 22.2%**, CP **[2.8%, 60.0%]** — per-tier,
  never pooled (D106 ④ / CONTROL_CRITERIA_v3 §2). **We do not report an FPR of
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

## Mechanical baselines (R2 does not fire) — [TASK 1]

Same 30 companies, same point-in-time data: Beneish M p=0.498/AUC 0.510 ·
Dechow F p=0.268/AUC 0.573 — the quantitative screens show no separation on
this sample. LLM rankings are essentially uncorrelated with both (wave-1
ρ −0.075/−0.144; wave-2 0.337/0.265) and residual separation survives →
pre-committed R2 does **not** fire. The LLM is not reproducing the mechanical
formulas.

## Grading & finalization status

- Grading: **Claude-assisted + human final sign-off.** Evaluatee
  **claude-sonnet-5** (pinned, served-model verified, 0 pin mismatches);
  grader claude-fable-5. **All grades `human_finalized=true`** (owner
  sign-offs D24/D26, 0 overrides, rubber-stamp check confirmed). Ledger:
  `scoring/overrides.md` · workbench: `review_packets/RP-13_grading_workbench.md`.

## Extension experiments E1–E5 (pre-registered — freeze-then-run)

All pre-registered and committed before scoring (`analysis/*_PLAN.md`,
commit `c1b85a7`): **E1** holdout matched controls (executed, D26 — only HUBG
separates; 2/9 control flags) · **E2** earliness trajectory · **E3** wave-2
perturbation redraws (executed: 3/9 → R4 retained) · **E4** cross-model
(**EXPLORATORY**, claude-opus-4-8, footnote-only) · **E5** scoring redraw
bands (holdout arm executed, D27: HUBG ≥50 in 5/5 draws). Status & spend
gates: `docs/OWNER_QUEUE.md` · `docs/RESUME.md`. **No experiment result is
published without the owner gate.**

## Governance map (reading order)

`PROJECT.md` (single reference: methodology §5 · collaboration §7 · scope §8)
→ `CLAUDE.md` + `scoring/decisions_log.md` (ledger + freeze hashes)
→ `scoring/overrides.md` (signatures/gates) → `review_packets/INDEX.md`
(audit entry) → published issue source texts `analysis/ISSUE_{0,1,2}*_DRAFT.md`
(owner-signed, posted 2026-07-11, D40/D41; URLs in Publication above).

## Reproducing the numbers (third-party verification)

Reproduction is a **two-tier interface** (tiers assigned by actual code
behavior — audit: `analysis/REVIEW_CLAIMS_AUDIT.md`):

```bash
pip install -r requirements.txt
make verify-public   # tier 1 — strictly zero external data: committed artifacts only
make verify-full     # tier 2 — adds raw-corpus recomputation (~/aaer-data required)
```

**`verify-public`** recomputes every published number from committed
artifacts (0 API calls, no source corpus needed) — proven by executing in a
sandbox with `HOME` redirected to an empty temp dir
(`audit/verify_public_sandbox_transcript_20260722.txt`); CI runs it on every
push. **`verify-full`** additionally recomputes the deterministic baselines
(`analysis/synthesis.py` calls `screens.run_case` over the raw XBRL cache)
and checks the full corpus manifest; prerequisites and corpus layout:
`REPRODUCING.md` §2 — absent the corpus it fails closed with instructions.

<!-- BEGIN-GENERATED: repro-facts (refresh: make docs-refresh; CI: tools/lint_doc_counts.py) -->
- data manifest: **538 files** (`data/manifests/aaer_data_manifest.json` · `file_count`)
- pytest: **275 tests collected** (`pipeline tools scoring analysis`)
- `make verify-public` (zero external data):
  - `.venv/bin/python tools/reproduce_analysis.py`
  - `.venv/bin/python tools/lint_publication.py`
  - `.venv/bin/python tools/lint_doc_counts.py`
  - `.venv/bin/python -m pytest pipeline tools scoring analysis -q`
  - `.venv/bin/python tools/verify_manifest.py --schema-only`
  - `.venv/bin/python tools/verify_blindness.py`
- `make verify-full` (requires `~/aaer-data` corpus; see REPRODUCING.md §2):
  - `.venv/bin/python analysis/baselines.py`
  - `.venv/bin/python analysis/stats.py`
  - `.venv/bin/python analysis/synthesis.py`
  - `.venv/bin/python analysis/calibration_wave2.py`
  - `.venv/bin/python tools/verify_manifest.py`
  - `$(MAKE) verify-public`
<!-- END-GENERATED: repro-facts -->

Raw: `runs/` (sha256 manifest) · `scoring/grades*/` ·
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
