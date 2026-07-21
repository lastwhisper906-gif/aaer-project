# AAER Evals — Backtesting a Conflict-Free Accounting-Quality Signal

[![ci](https://github.com/lastwhisper906-gif/aaer-evals/actions/workflows/ci.yml/badge.svg)](https://github.com/lastwhisper906-gif/aaer-evals/actions/workflows/ci.yml)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> Who did what: [CONTRIBUTIONS.md](CONTRIBUTIONS.md) (AI-vs-human table, D106 ⑤).
> All results are scoped to a single Claude-based pipeline (evaluatee pinned to
> claude-sonnet-5; PROJECT.md §5-5). Grading: Claude-assisted, human-finalized.
> 한국어 원문(전체 서사): [README.ko.md](README.ko.md).

## What this is

This repository backtests one question — **can an LLM screen for misstatement
risk from point-in-time structured disclosure data alone?** — against SEC
enforcement (AAER) confirmed cases with matched non-enforcement controls, plus
a post-training-cutoff holdout where memorization is structurally impossible.
It is an existence-proof record with its full audit trail, not a product:
no positions · educational/informational · not investment advice.

## The headline finding, with its limits

**There is no dominant single-threshold LLM strategy on the trajectory layer
(exploratory E2).** At threshold T≥50 that layer detects 12/12 treatment cases
(CP95 [73.5%, 100%]) but false-alarms on 5/7 controls (**71.4%**, CP95
[29.0%, 96.3%]); tightening to T=70 kills detection first (1/12). Cost per
detection and every cell's CP95 interval: [`analysis/DECISION_TABLE.md`](analysis/DECISION_TABLE.md)
(owner-signed, D94).

What survives honest scrutiny is narrower: **within each layer independently,
treatment/control separation significance survives as memorization is
progressively removed** — wave-1 perturbed permutation p=0.0021 (N=8 vs 22;
identity-exposed upper line p=0.00114), wave-2 standalone p=0.00116, AUC 0.829
[0.616, 0.983] (N=9 vs 23), and per-case persistence in the post-cutoff
holdout (N=3 — per-case evidence only, no significance claim; the single top
score in that tier is a control false positive, GridAI **GRDX 78**).

The limits, inline: false positives are real — [TASK 1] wave-1 FPR 3/22 =
**13.6%** CP95 [2.9%, 34.9%], wave-2 FPR 5/23 = **21.7%** CP95 [7.5%, 43.7%];
[TASK 2] holdout controls (E1) 2/9 = 22.2% CP95 [2.8%, 60.0%] — never summed
across tiers. Scores are **ordinal (0–100), not probabilities** (wave-2 ECE
**0.179**, wave-1 0.209 — uncalibrated). Residual memorization is measured,
not eliminated (name-ID **21.9%** on wave-2, frozen rule; 50% on wave-1).
Controls mean "not enforced against," not "clean." Every published number with
its row-level limit: [`RESULTS.md`](RESULTS.md).

## Quickstart (5 minutes, zero external data)

```bash
git clone https://github.com/lastwhisper906-gif/aaer-evals && cd aaer-evals
python3.12 -m venv .venv
.venv/bin/pip install --require-hashes -r requirements.lock
make verify-public   # recomputes every published number from committed artifacts
```

`verify-public` needs no corpus, no API key, no network — proven by a
clean-HOME sandbox transcript (`audit/verify_public_sandbox_transcript_20260722.txt`).
Corpus-dependent full reproduction: `make verify-full` (`REPRODUCING.md`).

<!-- BEGIN-GENERATED: repro-facts (refresh: make docs-refresh; CI: tools/lint_doc_counts.py) -->
- data manifest: **538 files** (`data/manifests/aaer_data_manifest.json` · `file_count`)
- pytest: **279 tests collected** (`pipeline tools scoring analysis`)
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

## Where to go next

- **[METHOD.md](METHOD.md)** — the pipeline on one page: payload assembly,
  fail-closed cutoff guard, isolated single call, schema-forced output,
  deterministic citation verification, human adjudication; the leakage threat
  model; the role-split contract (Python computes, the LLM judges
  qualitatively, a human signs).
- **[RESULTS.md](RESULTS.md)** — one table of published numbers, each row
  carrying its own limit.
- **[AUDIT_INDEX.md](AUDIT_INDEX.md)** — what D/Q/RP/FREEZE_REV identifiers
  mean, where each ledger lives, one real decision traced end-to-end.
- **[Licensing](#licensing)** — license status (below).

Detailed narrative (three-task separation, three-layer headline, false
positives, baselines, limitations — relocated copies):
[`docs/README_DETAIL.md`](docs/README_DETAIL.md).

## Publication (v1.0 — 2026-07-11, owner-signed D40/D41)

Published as GitHub Issues (series 0/1/2 = GitHub #1/#2/#3); the posted issues
are the publication surface, `analysis/ISSUE_*_DRAFT.md` the frozen sources.

- **Issue 0** (wave-1, R3 — memorization-entangled): <https://github.com/lastwhisper906-gif/aaer-evals/issues/1>
- **Issue 1** (wave-2, R4 — residual capability, scoped): <https://github.com/lastwhisper906-gif/aaer-evals/issues/2>
- **Issue 2** (post-cutoff holdout, H2): <https://github.com/lastwhisper906-gif/aaer-evals/issues/3>
- **Citable freeze point**: release [v1.0.0](https://github.com/lastwhisper906-gif/aaer-evals/releases/tag/v1.0.0).
- **Post-publication notices**: partial de-identification of the v1 perturbed
  frame ([`docs/V1_PARTIAL_DEIDENTIFICATION_NOTE.md`](docs/V1_PARTIAL_DEIDENTIFICATION_NOTE.md));
  errata ([`ERRATA.md`](ERRATA.md)).

## Licensing

**License selection is pending an owner decision (Q-O10,
`docs/OWNER_QUEUE.md`)** — no LICENSE file exists yet; until one lands, default
copyright applies and reuse requires permission. The planned split under
consideration: permissive code license + attribution docs license, so published
memos stay verifiable with attribution. `CITATION.cff` is present (DOI pending
Q-R03).
