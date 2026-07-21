# REMEDIATION PROGRESS — external review (F1–F14)

- BASE_COMMIT: ca496fdc77c606a745b19c5e0387664459ec172d (local main, 11 ahead of origin/main db8b85f = reviewer's audit commit)
- Branch: remediation/external-review
- Worktree: ~/work/worktrees/forensic-project-remediation
- Invocation scope: Phase 0 + Phase 1 (Tasks 1–11)
- Harness model-call budget: 40 | **consumed: 3** (T03: 2 build + 1 review)

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
| Task 2 (verdict module) | HARNESS | IN_PROGRESS | task: ~/work/remediation-tasks/T02_verdict_module.md | – |
| Task 3 (statistics module) | HARNESS | COMMITTED (APPROVED cycle 2/3) | ~/tools/harness/logs/T03_statistics_module_20260721_150457 | see log |
| Task 4 (CI covers analysis/) | DIRECT+1 harness max | PENDING | – | – |
| Task 5 (wave2 rev2 rerun) | DIRECT | PENDING | – | – |
| Task 6 (schema unification) | HARNESS | PENDING | – | – |
| Task 7 (fingerprinted idempotency) | HARNESS | PENDING | – | – |
| Task 8 (dynamic blindness scanner) | HARNESS | PENDING | – | – |
| Task 9 (cutoff loader contract) | HARNESS (option chosen by orchestrator) | PENDING | – | – |
| Task 10 (exception swallowing) | HARNESS | PENDING | – | – |
| Task 11 (synthetic fixtures) | HARNESS | PENDING | – | – |

Tasks 12–18: NOT in this invocation (Phase 2/3 — owner re-invokes).
