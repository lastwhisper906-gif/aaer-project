# REMEDIATION PROGRESS — external review (F1–F14)

- BASE_COMMIT: ca496fdc77c606a745b19c5e0387664459ec172d (local main, 11 ahead of origin/main db8b85f = reviewer's audit commit)
- Branch: remediation/external-review
- Worktree: ~/work/worktrees/forensic-project-remediation
- Invocation scope: Phase 0 + Phase 1 (Tasks 1–11)
- Harness model-call budget: 40 | **consumed: 27 FINAL** (T03: 2b+1r; T02: 3b+2r; T06: 1b+1r; T07: 2b+1b+1r; T08: 3b+1r STOPPED; T09: 3b+2r STOPPED; T10: 1b+1r; T11: 1b+1r)

## Preflight (2026-07-21)

- Metered keys: NONE in env (ANTHROPIC/OPENAI/GEMINI/GOOGLE checked precisely)
- claude CLI 2.1.216 (VERIFICATION.md records 2.1.215 — patch bump; Phase-2 flag checks re-run: -p/--allowedTools/--permission-mode/--output-format and codex -s/--cd all present verbatim)
- codex CLI 0.144.6 — exact match; ~/.codex/auth.json present, mode 600
- No stale .harness.lock/ anywhere
- `~/.claude/commands/harness.md` ABSENT — standing rules taken from ~/tools/harness/README.md + protocol deltas
- git fetch origin done; local main ahead 11 (not behind — fetch-first stop condition not triggered)
- TCC test: detached background process CAN access ~/Documents git metadata this session (BG-TCC-OK)

## Task table

| Task | Lane | Status | Run dir | Commit |
|---|---|---|---|---|
| Phase 0 (V1–V11 verification) | DIRECT | COMMITTED (all 11 CONFIRMED) | – | 80e5290 |
| Task 1 (ERRATA entry) | DIRECT | COMMITTED (E-001) | – | c3a396c |
| Task 2 (verdict module) | HARNESS | COMMITTED (APPROVED cycle 3/3; c2 caught dropped perturbed-frame + sealed-runs test dep) | ~/tools/harness/logs/T02_verdict_module_20260721_150952 | see log |
| Task 3 (statistics module) | HARNESS | COMMITTED (APPROVED cycle 2/3) | ~/tools/harness/logs/T03_statistics_module_20260721_150457 | see log |
| Task 4 (CI covers analysis/) | DIRECT+1 harness max | COMMITTED (pytest now covers analysis/; 0 failures; coverage floor DEFERRED — pytest-cov vs 5-dep invariant → batched decision) | – | (this commit) |
| Task 5 (wave2 rev2 rerun) | DIRECT | QUARANTINED (rule 1): verdict R4 UNCHANGED, primary stats identical, but tie-aware Spearman shifts published rho_M 0.337→0.333, rho_F 0.265→0.293 → E-002 held as DRAFT in final packet; rev2 artifact committed (deterministic, v1 untouched) | – | (this commit) |
| Task 6 (schema unification) | HARNESS | COMMITTED (APPROVED cycle 1/3) | ~/tools/harness/logs/T06_schema_unification_20260721_152549 | see log |
| Task 7 (fingerprinted idempotency) | HARNESS | COMMITTED (run 1 killed mid-cycle-2 → reset+relaunched once per protocol; relaunch APPROVED cycle 1) | ~/tools/harness/logs/T07_fingerprint_idempotency_20260721_153703 | see log |
| Task 8 (dynamic blindness scanner) | HARNESS | STOPPED (max-cycles 3, QUARANTINE rule 3 — root cause: orchestrator-supplied registry omitted scoring/probe_results_v2*/v2ds_* surfaces; discovery guarantee worked and caught it; c2 review also flagged fail-open carve-outs + name-variant weakening; worktree reverted, diffs preserved in run dir; RECOMMEND accepted — owner D3) → RELAUNCH IN_PROGRESS: ~/work/remediation-tasks/T08v2_blindness_scanner.md (registry v2 pre-validated: 940 files, 0 uncovered) | ~/tools/harness/logs/T08_blindness_scanner_20260721_154259 | – |
| Task 9 (cutoff loader contract) | HARNESS Option B | STOPPED (max-cycles 3, rule 3 — c3 review: registry-weakening guard needed for fixture mode; un-editable caller scoring/probe_verdict.py:62 breaks on signature change; coverage-metadata regression; fixture-mode writes to DEFAULT access log. Worktree reverted, diffs in run dir. RECOMMEND: relaunch with sharpened spec covering string-ticker compat + fixture-mode logging isolation) | ~/tools/harness/logs/T09_cutoff_loader_contract_20260721_155721 | – |
| Task 10 (exception swallowing) | HARNESS | COMMITTED (APPROVED cycle 1/3) | ~/tools/harness/logs/T10_exception_swallowing_20260721_162559 | see log |
| Task 11 (synthetic fixtures) | HARNESS | COMMITTED (APPROVED cycle 1/3; synthetic tier runs corpus-free, real tier iterates ALL cases) | ~/tools/harness/logs/T11_synthetic_fixtures_20260721_163048 | see log |

Tasks 12–18: NOT in this invocation (Phase 2/3 — owner re-invokes).

## Phase 1 exit (2026-07-21)

- Suite at exit: 255 passed (pipeline tools scoring analysis).
- COMMITTED: Phase 0, T1, T2, T3, T4(partial — coverage floor deferred), T5(artifact only — presentation QUARANTINED), T6, T7, T10, T11.
- STOPPED: T8, T9 (max-cycles, rule 3; relaunch recommendations in final packet).
- QUARANTINED: T5 presentation (E-002 DRAFT in final packet).
- Owner-queue (NOT done, per spec): reader dispatch, human graders, draw re-runs, sealed cycle arming, synthesis.py real-data rerun, forward cycle_001 hash re-pin decision.
