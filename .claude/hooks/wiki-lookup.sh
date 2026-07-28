#!/usr/bin/env bash
# wiki-lookup.sh — Claude Code UserPromptSubmit hook.
#
# Claude Code equivalent of the Kiro hook `wiki-lookup-before-drafting`. On every
# user prompt, injects a task-classification protocol as additional context so
# the assistant grounds drafting/communication/infrastructure/research/ingest
# work in the wiki BEFORE responding. This is the highest grounding-reliability
# guardrail identified in the Kiro→CC audit (2026-07-27).
#
# Mechanism (per code.claude.com/docs/en/hooks): UserPromptSubmit ignores
# matchers and always fires; plain stdout on exit 0 is injected as context Claude
# can see. Text is phrased as factual statements, not imperatives, to avoid
# tripping prompt-injection defenses. Output stays well under the 10k cap.
#
# The Kiro original (.kiro/hooks/wiki-lookup-before-drafting.json) is preserved
# for the Kiro runtime; this is the CC-native path.

set -euo pipefail

# stdin carries the event JSON; this hook does not need to parse it (the protocol
# is prompt-agnostic). Drain stdin so the pipe closes cleanly.
cat >/dev/null 2>&1 || true

cat <<'CONTEXT'
Task-grounding protocol for this workspace (classify the request, then ground in the wiki before drafting):

1. COMMUNICATION (drafting/writing/sending to a named person): the person's history is in src/research_assistant/spaces/*/wiki/entities/ and src/research_assistant/spaces/*/communication/. Reading the entity page and prior communications first prevents asking questions the wiki already answers. A [Last communication: DATE — TOPIC — STATUS] line evidences that reading.

2. DOCUMENT (proposal, thesis, paper, deliverable): structural requirements live in data/wiki/shared/deliverables/_index.md and its requirement pages. Loading the relevant page before writing keeps the output on-structure.

3. INFRASTRUCTURE (how this system works, where to store things, or ANY claim about what our scripts/hooks/agents/dispatch/eval-gates/steering do): the authoritative answer is in ARCHITECTURE.md and the specific script/hook/agent files. A claim grounded in the actual files read this turn is reliable; one from prior context or assumption is not. Comparing an external tool requires reading both its docs and our corresponding files first.

4. RESEARCH (literature, papers, gaps, methodology, theory, search strategy, or drafting a prompt for research work): methods and concepts are in data/wiki/shared/methods/_index.md and data/wiki/shared/concepts/_index.md. Literature-search work also draws on the Building Block Strategy in src/research_assistant/spaces/QNTR/wiki/entities/prof-priyanka-suresh.md.

5. KNOWLEDGE INGEST (scan/review/assess/ingest new source material, or "what's your take on" new files): an overlap check against the target space's wiki/_index.md, data/wiki/shared/methods/_index.md, and .kiro/steering/literature-review-standards.md comes before any relevance assessment. The response includes an [Overlap Check] section listing already-captured, new-wiki-worthy, and operational-only topics.

6. GENERAL: proceed normally.

When a request sits between GENERAL and a specific category, the specific category applies: loading unnecessary context costs less than missing relevant context. A task that produces research output is a RESEARCH task; a task about new files in a knowledge/ directory is always KNOWLEDGE INGEST.
CONTEXT

exit 0
