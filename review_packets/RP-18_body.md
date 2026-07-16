### Exploratory appendix — decomposing the wave-1/wave-2 B3 asymmetry

**Status: exploratory arithmetic, not a finding.** This decomposes numbers
already published (B3 report); it adds no new runs, no new claims, and every
causal-sounding sentence below is deliberately phrased as a question.

The B3 filing-chronology baseline separates wave-1 strongly (AUC 0.7898,
attribution ratio 0.89 vs the LLM's 0.8239) but is near-uninformative on
wave-2 (AUC 0.5483, ratio 0.147 — the pre-registered decision tier). The
indicator-level arithmetic behind that asymmetry:

| indicator (W8) | w1 fraud (n=8) | w1 control (n=22) | w2 fraud (n=9) | w2 control (n=23) |
|---|---|---|---|---|
| NT 10-K/Q | 1/8 | 1/22 | 2/9 | 1/23 |
| **10-K/A** | **4/8** | **2/22** | **1/9** | **6/23** |
| 10-Q/A | 2/8 | 2/22 | 1/9 | 1/23 |
| 8-K item 4.01 (auditor change) | 0/8 | 1/22 | 1/9 | 0/23 |
| 8-K item 4.02 (non-reliance) | 1/8 | 0/22 | 0/9 | 0/23 |
| 8-K frequency spike | 2/8 | 1/22 | 0/9 | 1/23 |

The single largest wave-1 contributor is the 10-K/A indicator (50% of fraud
cases vs 9.1% of controls) — and the *same indicator inverts* on wave-2
(11.1% vs 26.1%).

**The label-circularity hypothesis (flagged as hypothesis, not conclusion):**
famous frauds may be famous partly *because* they restated — so a 10-K/A
indicator may be **selection showing through, not detection**. Wave-2's
inversion is consistent with the base rate that most amendments are benign
little-r corrections, which would make 10-K/A prevalence in any given sample
a property of how the sample was drawn rather than of misconduct.

Open questions we register but do not answer here: era effects on amendment
practice (wave-1 cutoffs are late-2000s–2010s vs wave-2's 2010s); control-pool
survivorship (registered separately as an audit item); and whether the LLM's
wave-1 rank order rode the same chronology signal or reached similar ranks by
different routes (undecidable without the earliness data).

*Limitations: N=8/9 fraud cases per tier; no single prevalence difference
here is a statistical claim on its own; results are scoped to a single
Claude-based pipeline (methodology limitations L-1…L-7 apply).*
