# REVIEW_VERIFICATION — external review claims V1–V11 vs actual code

Verified 2026-07-21 against branch `remediation/external-review` @ ca496fd
(local main; reviewer audited origin/main db8b85f — none of the 11 target
files differ between the two commits' relevant regions; evidence line
numbers are from ca496fd).

Method: DIRECT read of each cited file; evidence quoted verbatim below the
table. Gate per REMEDIATION_SPEC Phase 0: only CONFIRMED/PARTIAL claims'
fix tasks proceed.

| ID | Reviewer claim (abbrev.) | File(s) | Verdict | Evidence (file:line) | Linked fix task |
|---|---|---|---|---|---|
| V1 | wave2 R2 uses `abs(rho)>=0.7`, no residual test, contradicting plan | analysis/wave2_analyze.py, analysis/ANALYSIS_PLAN_WAVE2.md | **CONFIRMED** | wave2_analyze.py:101; plan §4 (ANALYSIS_PLAN_WAVE2.md:49–52); no residual code anywhere in wave2_analyze.py | Task 1, 2, 5 |
| V2 | wave2 omits Fisher exact, Clopper–Pearson, worst-case substitution; only flag counts + raw FPR | analysis/wave2_analyze.py | **CONFIRMED** | wave2_analyze.py:63–66 (flag counts + `fpr_pct` only); plan §2 (:36–37), §3 (:43–44), §1 (:27–29) | Task 1, 2, 5 |
| V3 | Payload builders bypass cutoff_guard.load_document (own filter, no accession cross-check, no logging); bypass test doesn't enforce loader | pipeline/build_payload.py, pipeline/payload_v2_extract.py, pipeline/test_no_guard_bypass.py | **CONFIRMED** | build_payload.py:87 (`path.read_text`), :90–91 (own filter, "유일한 look-ahead 필터 지점"), :123; payload_v2_extract.py:84,124; test_no_guard_bypass.py:19–29 (patterns cover network/candidates/id_mapping/scoring only) | Task 9 |
| V4 | MODEL_SCHEMA: bare integer probability, no mech max-3, no p≥40 conditional, no evidence minItems; no full-schema validation before write | pipeline/runner.py, schemas/llm_output.json | **CONFIRMED** | runner.py:80 (`{"type": "integer"}`), :81 (no maxItems), :73 (no minItems), no if/then in MODEL_SCHEMA (:60–100); write at :151 with no validation of `full`. Canonical llm_output.json HAS min 0/max 100, maxItems 3, p≥40 allOf — divergence is real | Task 6 |
| V5 | Idempotency skip checks only schema-validity of existing output | pipeline/runner.py | **CONFIRMED** | runner.py:107–108 (`output_is_valid(out_path, FULL_OUTPUT_SCHEMA)` → skip); no prompt/model/input/cutoff/version comparison; docstring :13 confirms design | Task 7 |
| V6 | Blindness semantic scan paths hardcoded (wave2/holdout/e2/e4 only SHA-manifest-covered); ancestry check hardcoded to one wave-1 commit; inline name list | tools/verify_blindness.py | **CONFIRMED** | verify_blindness.py:108 (roots `runs/main, runs/perturbed, pilot/runs`), :121–123 (fixed scoring dirs), :46 (`GRADING_COMMIT = "03b91aa"`), :52–54 (inline 8 wave-1 names/tickers), :161 (manifest walks runs/** by SHA only) | Task 8 |
| V7 | CI pytest excludes analysis/ despite tests there | .github/workflows/ci.yml, analysis/test_*.py | **CONFIRMED** | ci.yml pytest step: `python -m pytest pipeline/ tools/ scoring/ -q`; analysis/ contains test_b3_compute.py, test_engine_verdict.py, test_decision_table.py, test_b4_short_interest.py, test_buyer_metrics.py, test_draw_k3_analysis.py, test_e2_interface_contract.py | Task 4 |
| V8 | Stats functions duplicated across files; wave2 Spearman not tie-aware while stats.py is | analysis/wave2_analyze.py, analysis/stats.py, others | **CONFIRMED** | wave2_analyze.py:42–50 (rank = enumerate positions, ties get arbitrary distinct ranks) vs stats.py:85–102 (tie-averaged `(i+j)/2+1`); own stat/rng implementations also in b3_compute.py, b4_short_interest.py, draw_k3_analysis.py, identity_3arm_analyze.py, synthesis.py | Task 3 |
| V9 | Wave-2 baseline catches all Exception, drops companies silently; synthesis.py swallows baseline errors, hardcodes holdout recognized=False | analysis/wave2_analyze.py, analysis/synthesis.py | **CONFIRMED** | wave2_analyze.py:77–78 (`except Exception: continue`); synthesis.py:41–44 (`except Exception: return None, None`); synthesis.py:114 (`recognized=False,  # recognition gate…`) — value matches frozen gate result but is hardcoded, not read from result files | Task 10 |
| V10 | Real-XBRL payload tests skip entirely without ~/aaer-data; leakage scan first-4; perturbation check first-1 | pipeline/test_build_payload.py | **CONFIRMED** | test_build_payload.py:16–18 (module-level `pytestmark = pytest.mark.skipif(...aaer-data...)`), :46 (`_cases()[:4]`), :53 and :66 (`_cases()[0]`) | Task 11 |
| V11 | Publication claims "R1–R4 verbatim" and that `python analysis/wave2_analyze.py` reproduces the published result | analysis/ISSUE_1_WAVE2_DRAFT.md, analysis/wave2_summary.md | **CONFIRMED** | ISSUE_1_WAVE2_DRAFT.md:63 ("conclusion rules R1–R4 **verbatim**"), :77–78 ("reproducible via `python analysis/wave2_analyze.py`"); wave2_summary.md:4–5 (재현 명령). Aggravating: draft quotes "FPR 21.7% CP [7.5%, 43.7%]" and Fisher-exact framing that wave2_analyze.py does not compute — those numbers are not produced by the stated reproduction command | Task 1 |

## Notes

1. **All 11 claims CONFIRMED; none REFUTED.** No fix task is
   DEFERRED-REFUTED by the Phase 0 gate.
2. **V4 nuance**: the canonical `schemas/llm_output.json` already encodes
   the correct constraints (probability 0–100, mechanism maxItems 3,
   p≥40→mechanism≥1 allOf, evidence minItems). The defect is that the
   hand-maintained MODEL_SCHEMA in runner.py silently dropped them and
   nothing re-validates the written file against the canonical schema.
   Existing-file idempotency checks (runner.py:107) DO use the canonical
   schema — so an out-of-bounds output would be caught on the NEXT run's
   skip check, not at write time.
3. **V9 nuance**: the hardcoded `recognized=False` (synthesis.py:114)
   matches the frozen recognition-gate result (knows_event=False 3/3) —
   the published value is not wrong, but the mechanism is as the reviewer
   describes: it would silently stay False if holdout probe results
   changed.
4. **V11 aggravating detail**: the published CP interval
   (21.7% [7.5%, 43.7%]) and Fisher-exact framing in
   ISSUE_1_WAVE2_DRAFT.md §5 cannot come from `wave2_analyze.py` (V2) —
   the reproduction claim fails not only for the R2 rule shape but for
   pre-registered statistics quoted in the publication itself.
5. **Wave-1 is clean on V1/V2**: `analysis/stats.py` (wave-1) implements
   signed rho + residual permutation correctly (stats.py:202
   `rho >= RHO_HIGH and p_res >= ALPHA`, residuals :105–111, Fisher
   :44–54, Clopper–Pearson :114–142). The divergence is wave-2-specific
   re-implementation drift — exactly the duplication failure mode V8
   names.
