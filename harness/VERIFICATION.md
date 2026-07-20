# Harness Verification Record

Installed and verified 2026-07-20.

**Re-verification rule: re-run Phase 2 flag checks (`codex exec --help`,
`claude --help` against the table below) after any major CLI upgrade.**

## Environment (Phase 1, verified 2026-07-20)

- `claude` CLI **2.1.215** at `/opt/homebrew/bin/claude`; auth via `~/.claude`
  (no `CLAUDE_CODE_OAUTH_TOKEN` env var — keychain/dir auth).
- `codex` CLI **0.144.6** at `~/.local/bin/codex` (symlink →
  `~/.codex/packages/standalone/current/bin/codex`). `~/.local/bin` is added
  to PATH by `~/.zprofile` (login shells only).
- `~/.codex/auth.json` present (mode 600).
- No metered API keys in environment (ANTHROPIC/OPENAI/GEMINI/GOOGLE checked).
- `gtimeout` available (GNU coreutils 9.11, via Homebrew); `openssl` ok;
  `sha256sum` at /sbin.

## Flag verification table (Phase 2)

All HARD requirements exist verbatim — **zero flag adaptations were needed**;
`run_builder`/`run_reviewer` use the reference flags unchanged.

| Purpose | Reference | Installed | Result |
|---|---|---|---|
| Codex non-interactive | `codex exec "<prompt>"` | same | verbatim |
| Codex write sandbox | `--sandbox workspace-write` | same (`-s`; values: read-only, workspace-write, danger-full-access) | verbatim |
| Codex read-only sandbox | `--sandbox read-only` | same | verbatim |
| Codex working dir | `--cd <dir>` | same (`-C, --cd`) | verbatim |
| Claude non-interactive | `claude -p "<prompt>"` | same (`-p, --print`) | verbatim |
| Claude tool allowlist | `--allowedTools` | same (also `--allowed-tools`) | verbatim |
| Claude edit auto-accept | `--permission-mode acceptEdits` | same | verbatim |
| Claude JSON output | `--output-format json` | same (soft) | verbatim |
| Claude memory-file control | any CLAUDE.md-limiting flag | exists: `--bare`, `--safe-mode` | recorded, NOT relied on |

Also recorded (not required): codex `--skip-git-repo-check`,
`--output-last-message <FILE>`, `--json`; claude `--setting-sources`,
`--disallowedTools`, `--tools`.

## Offline verification (Phase 5, all executed 2026-07-20)

| Test | Result |
|---|---|
| `bash -n harness/run_task.sh` | PASS (syntax OK) |
| Metered-key guard (`ANTHROPIC_API_KEY=fake`) | PASS — "REFUSED", exit 2 |
| Dirty-tree guard (scratch repo, untracked file) | PASS — refusal, exit 2 |
| Lockfile guard (pre-created `.harness.lock/`, clean tree) | PASS — refusal, exit 2 |
| Sentinel spoof: log containing `VERDICT[FAKE]: APPROVE` + real `VERDICT[<S>]: REVISE` | PASS — parses as REVISE (sentinel line only) |
| Sentinel: real `VERDICT[<S>]: APPROVE` | PASS — parses as APPROVE |
| Sentinel: legacy `VERDICT: APPROVE` (no token) | PASS — does NOT parse (→ MALFORMED_REVIEW path) |
| Protected-path revert: tracked file modified | PASS — restored from BASE |
| Protected-path revert: new file created under `harness/` | PASS — deleted (git cat-file branch) |
| Protected-path revert: non-protected change | PASS — left untouched |
| `check:` extraction from task file | PASS — yields exact command |
| Per-cycle sentinel rendering (two seds) | PASS — outputs differ only in token (4 diff lines) |
| Stall detection (sha256 same/different) | PASS — same→trigger, different→no trigger |
| Stripped-env check (`env -i`, token set in parent) | PASS — prints EMPTY |
| `sync_context.sh` idempotency | PASS — re-run produces identical CLAUDE.md |

## Smoke test (Phase 6, the only model-call phase)

- Run dir: `harness/logs/hello_task_20260720_144103` (gitignored)
- Scratch repo in session scratchpad (/private/tmp), hello-world task with
  `check: python3 hello.py | grep -qx "hello harness"`.
- **Result: APPROVED at cycle 1, exit 0. Exactly 2 model calls**
  (1 codex build + 1 claude review). No retries.
- Deterministic check ran before the review; its PASSED result appears in
  `cycle_1_review_prompt.md`.
- Review log ends with the sentinel-bound verdict line
  (`VERDICT[405e55b27cfd8dc6]: APPROVE`).
- Run dir contains: prompt snapshots (builder + reviewer template),
  per-cycle rendered reviewer prompt, build/check/review logs, diff,
  meta.txt with both CLI versions and final_verdict.
- Note: the run used the default `--max-cycles 3` (spec suggested 2); the
  cap was never reached, so behavior is identical.

## AGENTS.md symlink test (Phase 3 question, answered in Phase 6)

`AGENTS.md → CLAUDE.md` symlink **works**: the scratch repo's CLAUDE.md
declared a marker convention (`# ctx-a7f3` first-line comment) that the task
never mentioned; AGENTS.md was a symlink; codex's hello.py began with the
marker. Therefore codex reads the symlinked content. The repo uses the
symlink (no dual-file sync needed for AGENTS.md; `harness/sync_context.sh`
still syncs CLAUDE.md's embedded block from PROJECT_INVARIANTS.md).

Incidental positive observation: the claude reviewer explicitly treated an
instruction-like sentence in the auto-loaded CLAUDE.md as data and judged
independently (see run log).

## Known limitations

- Inverted mode (claude builds, codex reviews) verified offline only —
  not smoke-tested end-to-end (by design: one-smoke-test budget).
- CLI flags drift with updates — re-run Phase 2 checks after upgrades.
- Subscription paths may silently fall back across models near usage
  limits — hence the hard dev-only boundary (see README): never run
  sealed/forward-cycle evaluations through this harness.
- The sentinel protocol depends on the reviewer emitting the exact line;
  the designed failure is MALFORMED_REVIEW (exit 5), not silent mis-parse.
- `claude -p` auto-loads CLAUDE.md; role-neutrality is maintained by the
  Phase 3 context audit (invariants only), not by a CLI flag (`--bare`
  exists but is deliberately not relied on).
