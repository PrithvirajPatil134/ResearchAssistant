# Workspace Upgrade: Kiro IDE → Claude Code

This folder tracks the migration of the ResearchAssistant workspace from its
original Kiro IDE runtime to Claude Code. Everything related to this upgrade
lives here so progress is auditable and survives context compaction.

## Why this exists

The workspace was built for Kiro IDE and is now run under Claude Code. A
five-cluster read-only audit (2026-07-27) found that the runtime switch, plus an
earlier half-finished directory migration, left several capabilities silently
broken or inert. This upgrade restores full functionality under Claude Code with
no loss of capability, and adds regression guards so the failures cannot recur
undetected.

## Files in this folder

- `README.md` — this file: scope, principles, folder contract.
- `upgrade-plan.md` — the master plan. Waves, tasks, acceptance criteria, decisions.
- `audit-findings.md` — the consolidated audit result (the two root causes and
  every defect, with file:line evidence).
- `progress-log.md` — dated, append-only log of what was changed, verified, and
  what remains. Update this after every wave.

## Scope

In scope: make every capability the Kiro version had operable and understood
under Claude Code, fix the incomplete directory migration, rebuild the
enforcement layer as Claude Code hooks, harden the agent definitions, reconcile
the legacy wiki tree, and add regression guards.

Out of scope: reviving the Kiro "Evolve" transcript-reflection loop (Wave 3 in
early drafts). Claude Code maintains its own transcripts and persistent memory,
and the wiki is the maintained knowledge base, so a parallel Kiro-style
transcript-capture loop is redundant. The deterministic learner tier
(`learner-*`, `capture-*` scripts) stays; only the transcript-reflection tier is
dropped.

## Working principles (carried from the workspace standards)

1. Reliability is not negotiable. A guardrail that reports false results is worse
   than none. Verify before concluding: a tool result is a signal about the tool,
   not a fact about the world.
2. Fix-in-place only when the blast radius is clearly gaugeable. Otherwise create
   a new Claude-Code-native file alongside the Kiro one and preserve the Kiro path
   for cron/headless use.
3. No destructive action without an explicit diff and approval.
4. New files land in their correct place in the hierarchy:
   - Claude Code hook wrapper scripts → `.claude/hooks/`
   - Claude Code runtime config → `.claude/settings.json`
   - Skills → `.claude/skills/<name>/SKILL.md`
   - Kiro-era / cron shell scripts → `scripts/` (unchanged home)
   - This upgrade's plan and logs → `docs/workspace-upgrade/`

## Canonical facts (verified 2026-07-27, do not re-derive)

- Canonical wiki/space tree: `src/research_assistant/spaces/*` (4 spaces incl. CW,
  67 wiki pages, has `_index.md`).
- Legacy tree: `spaces/*` at workspace root (3 stray files, no `_index.md`). To be
  reconciled and removed in Wave 5.
- Dispatch model everywhere: `RA_AGENT_MODEL=claude-opus-4-8[1m]`, registered in
  `~/.claude/settings.json`. No script-level model defects.
- Claude Code fires one hook today: `SessionStart → scripts/discover-claude-context.sh`.
  All 26 `.kiro/hooks/` are inert under Claude Code.
