# Two-AI Build/Review Harness

Development tooling that pairs two subscription CLIs in a build → review
loop: **Codex builds** (workspace-write sandbox) and **Claude reviews**
(mechanically read-only), or the inverse per task.

> **HARD BOUNDARY — never route forward-cycle evaluatee runs through this
> harness.** Sealed research runs require an explicitly pinned model in the
> dedicated sealed runner. Subscription dev paths may silently fall back
> across models near usage limits — acceptable for dev tooling, fatal for a
> sealed evaluation. This harness is dev tooling only.

## Usage

```bash
# Default mode: codex builds, claude reviews
harness/run_task.sh --task my_task.md

# Inverted mode (domain-judgment-heavy work: seal integrity logic,
# statistical tests, accounting semantics): claude builds, codex reviews
harness/run_task.sh --task my_task.md --mode inverted

# Auto-commit when the reviewer approves
harness/run_task.sh --task my_task.md --commit-on-approve

# Loop until APPROVE, hard ceiling 10 cycles, aborts on diff stall
harness/run_task.sh --task my_task.md --until-approve
```

Write tasks from `harness/TASK_TEMPLATE.md`. A `check:` line in the task
gives the harness a deterministic command to run after every build; a
nonzero exit triggers automatic REVISE without spending a reviewer call.

`--until-approve` has a hard ceiling of 10 cycles and aborts early
(STALLED) if the builder produces a byte-identical diff two cycles in a
row. There is deliberately **no truly unbounded mode**: two models can
deadlock — the reviewer keeps finding new objections, the builder keeps
disputing — and an unbounded loop converts that deadlock into quota
exhaustion.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | APPROVED |
| 2 | guard refused (metered key set, missing CLI, dirty tree, lock held) |
| 3 | CLI failure or timeout (builder or reviewer call) |
| 4 | cycle cap reached without approval — sharpen the task, don't raise the cap |
| 5 | malformed review (no sentinel-bound verdict line) |
| 6 | git-history tampering by the builder — manual inspection required |
| 7 | stalled — identical diff two cycles running |

## Design guarantees

- **Mechanically read-only reviewer.** Default mode: `claude -p` with
  `--allowedTools "Read,Grep,Glob"`. Inverted: `codex exec --sandbox
  read-only`. Never prompt-level discipline.
- **Prompt snapshots.** Prompts are copied into the run dir at start and
  only the snapshots are used, so a builder that edits `harness/prompts/`
  cannot influence the current run's reviewer.
- **Per-cycle sentinel verdicts.** The reviewer must end with
  `VERDICT[<token>]: APPROVE|REVISE`, token regenerated every cycle —
  a builder that reads cycle N's logs learns nothing usable for cycle N+1.
  Any `VERDICT[` string appearing in the diff mechanically fails the cycle.
- **Protected-path auto-revert.** Changes to `harness/`, `CLAUDE.md`,
  `AGENTS.md`, `PROJECT_INVARIANTS.md` are reverted (tracked files restored
  from base, new files deleted) and the cycle fails with feedback.
- **Deterministic pre-check in a stripped environment.** The `check:`
  command runs builder-authored code outside any sandbox, so it executes
  under `env -i` — it cannot read `CLAUDE_CODE_OAUTH_TOKEN` or other
  credentials from the harness process.
- **Single-run lock** (`.harness.lock/`) — one run per workdir at a time.
- **No auto-retry.** A failed or timed-out CLI call exits immediately: a
  retry loop burns quota on a call that already failed once; a human should
  look first.

## Quota discipline

Both CLIs draw from the same subscription pools you use interactively —
harness cycles compete with your own sessions. Schedule heavy harness use
away from the November forward cycle. Small tasks produce small diffs,
review well, and converge in 1–2 cycles; big vague tasks burn cycles.

**When NOT to use the harness:** one-line edits, docs typos, config
tweaks — direct edits are cheaper. The harness earns its 2+ model calls
only for multi-file logic, integrity-critical code, or scope-drift-prone
work.

## Practical notes

- **Use a dedicated git worktree** for harness runs. Guard 3 requires a
  clean tree, and a worktree keeps builder output away from your own
  uncommitted work.
- **Logs are sensitive.** `harness/logs/` (gitignored) contains full
  prompts and diffs. Never paste run logs into public issues without
  review.
- `harness/sync_context.sh` regenerates the shared-invariants block in
  `CLAUDE.md` from `PROJECT_INVARIANTS.md` — edit the source file, then
  run it; never hand-edit the block.
