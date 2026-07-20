# TASK: <one-line title>

## Mode hint
<!-- default = codex builds, claude reviews (implementation-heavy work)
     inverted = claude builds, codex reviews (domain-judgment-heavy work:
     seal integrity logic, statistical tests, accounting semantics) -->
mode: default

## Objective

<What must exist after this task that does not exist now. One paragraph.>

## Files in scope

- <path> — <create | modify>
<!-- The builder must not touch files outside this list. -->

## Read-only / forbidden paths

- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md (always)
- v1 frozen artifacts, published results, historical governance records
- <add task-specific paths, esp. scoring-side secret locations>

## Check command
<!-- ONE shell command the harness runs mechanically after each build.
     Nonzero exit = automatic REVISE without spending a reviewer call.
     Line must start exactly with "check: ". Omit the line if none. -->
check: <e.g. python3 -m pytest tests/test_x.py -q>

## Acceptance criteria

<!-- The reviewer verifies these one by one. Each must be checkable from
     the diff or by reading files. No vague criteria. -->

1. <criterion>
2. <criterion>
3. A test exists at <path> that fails if <core behavior> is wrong.

## Explicitly out of scope

- <things a helpful builder might be tempted to add — forbid them here>

## Notes / context

<Optional. Links to specs, prior decisions, constraints.>
