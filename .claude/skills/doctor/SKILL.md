---
name: doctor
description: Check context-management health — verify 1M model on all dispatch sites, lean CLAUDE.md base context, and the auto-gen marker. Run when context feels heavy, after editing dispatch scripts or discover-claude-context.sh, or to confirm the harness is aligned.
allowed-tools: Bash(bash scripts/harness-doctor.sh), Read
---

# Harness doctor

Read-only context-management health check. Safe to auto-invoke.

## What it does

Runs `scripts/harness-doctor.sh`, which asserts three invariants:

1. No dispatch script passes a non-1M `--model` (would drop subagents to 200k and
   cause "Prompt is too long").
2. CLAUDE.md resident `@import` bytes stay under budget (lean base; heavy docs
   must be on-demand pointers, not `@import`ed).
3. CLAUDE.md carries the auto-gen marker (`discover-claude-context.sh` owns it).

## How to run

```
bash scripts/harness-doctor.sh
```

Exit 0 = all green. Exit 1 = violations (see the FAIL lines). If it fails on the
model check, a dispatch script reintroduced `--model opus` (or another non-`[1m]`
model) — fix it to use `$RA_AGENT_MODEL`. If it fails on the budget, a heavy doc
was `@import`ed into CLAUDE.md instead of listed as an on-demand pointer — fix
`scripts/discover-claude-context.sh`.

## Source of truth

- `scripts/harness-doctor.sh` — the checks themselves.
- `scripts/discover-claude-context.sh` — generates the lean CLAUDE.md and runs
  this doctor warn-only at every SessionStart.
