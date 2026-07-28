# Audit Findings — Kiro → Claude Code Migration

Consolidated result of a five-cluster read-only audit run 2026-07-27 (dispatch,
ingest/wiki, hooks/config, learner/maintenance, agent definitions). Every claim
below is grounded in a file:line the audit agents verified. Two root causes
explain nearly every defect.

## Root cause A — incomplete `spaces/` → `src/research_assistant/spaces/` migration

An earlier migration to the canonical tree was applied to some paths and not
others, in the same files. `ra-content-evaluator` and `long-doc-orchestrate.sh:1179`
already use the canonical path; their siblings do not. Every location still on the
legacy 3-file tree fails silently (reads nothing / reports empty / restores nothing).

| Location | Line(s) | Effect | Fix |
|---|---|---|---|
| `scripts/long-doc-orchestrate.sh` | 290 | Brain assembler reads legacy 3-page tree; reads NOTHING for CRO/CW/DBA | in-place |
| `scripts/long-doc-orchestrate.sh` | 1019 | Devil's-advocate eval reads wrong tree | in-place |
| `scripts/long-doc-orchestrate.sh` | 1362 | Finished docs delivered to legacy tree | in-place, prefer-canonical/fallback pattern (owner sign-off) |
| `scripts/ra-wiki-lint.sh` | 224, 274 | Coverage-gap + image-orphan checks silently no-op (false "all clean") | in-place (completes today's partial fix) |
| `scripts/ingest-rollback.sh` | 99 | Rollback safety-net cannot restore canonical pages | in-place (add canonical glob) |
| `scripts/ra-storage-audit.sh` | 82, 125 | Image sizing silently empty | in-place |
| `scripts/ra-weekly-status.sh` | 63, 97, 116 | Wiki growth / orphans / stale seeds miss canonical | in-place |
| `scripts/image-orphan-scan.sh` | 32, 47 | Reports "no images" while images exist; duplicate of the correct `orphan-image-check.sh` | in-place or consolidate onto `orphan-image-check.sh` |
| `.claude/agents/ra-brain-assembler.md` | 51, 62, 100, 117, 129 | 5 operational reads of legacy tree (no `_index.md` there) | in-place |
| `.claude/agents/ra-wiki-reviewer.md` | 18, 20 | Validates pages against wrong tree | in-place |
| `.claude/agents/ra-wiki-linter.md` | 44-46 | Scans wrong tree; under-reports coverage/orphans | in-place |
| `.claude/agents/ra-email-drafter.md` | 33 | Writes drafts into legacy tree | in-place |
| `.claude/agents/ra-orchestrator.md` | 77 | Guard text references legacy tree | in-place (wording) |
| `.claude/agents/ra-wiki-ingestor.md` | 35, 40 | Ambiguous relative `wiki/_index.md`; must be canonical | in-place / contract |

Lower severity, same pass: 7 long-doc/writer agents embed legacy
`[spaces/{SPACE}/knowledge/...]` in citation-FORMAT examples (mismatched
provenance strings, not failed reads): ra-abstract-writer, ra-doc-stitcher,
ra-exhibit-producer, ra-post-stitch-eval, ra-pre-stitch-eval, ra-section-writer
(all around lines 20-22).

## Root cause B — Kiro→CC runtime switch orphaned the event/hook layer

Claude Code reads only `.claude/settings.json` (one hook: SessionStart). All 26
`.kiro/hooks/` are inert. Real functionality silently lost, worst first:

1. **`wiki-lookup-before-drafting` — HIGHEST.** Per-prompt gate that forced
   wiki/entity/index lookups before any drafting task. Fires on nothing. Steering
   covers fragments only; the proactive "read the wiki before drafting" routing is
   gone. Biggest grounding-reliability loss. → CC `UserPromptSubmit` hook.
2. **`check-agent-writing` + `check-submission-writing` — HIGH.** Post-write scan
   against `human-authored-writing.md` (banned words, em-dashes, tone). Standard is
   in context; enforcement is gone. → one consolidated CC `PostToolUse`
   (Edit|Write|MultiEdit) hook returning `decision:block`/`additionalContext`.
3. **`lint-agents` — MEDIUM.** `py_compile` on edited agent Python no longer runs.
   → CC `PostToolUse` command hook (reads `file_path` from stdin JSON).
4. **`check-agent-status` sentinel reconcile — LOW.** Only matters if the shell
   harness is used; Agent-tool completions are covered natively.

Already covered by always-loaded steering (no action): `async-task-gate`,
`no-assumption-chat-check`, `kiro-evolve-check-all`, interactive
`gpu-agent-completion`.

Obsolete / do not port: `jig-parallel-dispatch` (disabled placeholder), both
`kiro-evolve-save-*` (enabled:false; CC keeps its own transcripts).

Mechanism note: CC `PostToolUse` fires AFTER the tool runs and cannot block it;
parity is achieved via corrective feedback for next-turn self-correction, which
matches how Kiro's post-write agent actions also ran after the write.

## Related finding — evolve loop dead ~90 days (now OUT OF SCOPE)

Empirically confirmed: `~/.kiro/transcripts/*.md` are 28-byte stubs; markers
frozen at 2026-04-28. The transcript-reflection tier has not advanced since the
runtime switch. Decision: not reviving it. Claude Code's own memory + the
maintained wiki cover this role. The deterministic learner tier
(`learner-archive`, `learner-size-check`, `learner-summarize-month`,
`capture-user-edits`, `capture-user-verdict`) is alive and stays.

## Agent-definition systemic issues (beyond paths)

- **No agent pins a `model:` field** (all 23). They inherit the default. Heavy-input
  agents break first on large docs: ra-brain-assembler, ra-wiki-ingestor,
  ra-benchmark-comparator (full-text PDF/DOCX), ra-doc-stitcher, ra-section-writer,
  ra-post-stitch-eval, ra-abstract-writer (whole assembled doc). → pin 1M model on
  ALL 23 agents (decision 2026-07-27), so none can silently inherit a smaller default.
- **Sourcing contract inconsistent.** 15 of 23 carry a weakened one-line Hard Rule
  that drops "citation, source, quotation" and the override clause. NO agent
  restates the "No Absolute-Absence Claims" universal-negative rule — a real gap
  for ra-gap-table-builder, ra-litreview-builder, ra-methodology-advisor. → upgrade
  contracts; add absence guard to the gap/review agents.

## What is healthy (verified, do not re-audit)

- No model defects in any script — all dispatch uses `RA_AGENT_MODEL=claude-opus-4-8[1m]`.
- Zero Kiro dispatch verbs in any of the 23 agent bodies — no translation needed there.
- CC-compatible as-is: `spawn-gpu-agent.sh`, `claude-dispatch.sh`, `sentinel-lib.sh`,
  `sentinel-reconcile.sh`, `ingest-init.sh`, `ingest-commit.sh`, `ingest-cleanup.sh`,
  `autocapture-handler.sh` (targets canonical), the deterministic learner tier,
  `orphan-image-check.sh` (already canonical), `scratchpad-archive.sh`,
  `ra-manifest-cleanup.sh`.
- The atomic ingest init→commit→rollback flow is drivable end-to-end from Claude
  Code via the `ra-*` Agent-tool subagents.
