#!/usr/bin/env bash
# writing-gate.sh — Claude Code PostToolUse hook (matcher: Edit|Write|MultiEdit).
#
# Claude Code equivalent of the Kiro hooks `check-agent-writing` +
# `check-submission-writing` (consolidated). After a write to submission-ready
# academic content, it asks the assistant to scan the file against
# .kiro/steering/human-authored-writing.md and fix any violations.
#
# Mechanism (per code.claude.com/docs/en/hooks): PostToolUse fires AFTER the tool
# runs and cannot block it. Parity with Kiro's post-write agent action is achieved
# by returning additionalContext (non-blocking feedback Claude acts on next turn).
# We use additionalContext rather than decision:block so routine writes are not
# interrupted; the correction happens in the normal flow.
#
# The path filter mirrors the Kiro original: only submission-ready content
# triggers the scan; code/config/steering/logs are skipped.
#
# Kiro originals preserved for the Kiro runtime; this is the CC-native path.

set -euo pipefail

INPUT="$(cat)"

# Extract the written file path. jq if available; fall back to grep.
fp=""
if command -v jq >/dev/null 2>&1; then
  fp="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)"
fi
if [ -z "$fp" ]; then
  fp="$(printf '%s' "$INPUT" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed -E 's/.*:[[:space:]]*"([^"]*)"/\1/' || true)"
fi

# No path (e.g. MultiEdit shape differs) → nothing to gate.
[ -z "$fp" ] && exit 0

base="$(basename "$fp")"

# Submission-ready filter (union of the two Kiro hooks' path rules):
#   dir contains workspace/ | output/ | assignment/   OR
#   filename contains Submission|Paper|Teaching|Case|revised
is_submission=0
case "$fp" in
  */workspace/*|*/output/*|*/assignment/*) is_submission=1 ;;
esac
case "$base" in
  *Submission*|*Paper*|*Teaching*|*Case*|*revised*) is_submission=1 ;;
esac

# Skip obvious non-prose even if the path matched (code/config/steering/logs).
case "$base" in
  *.py|*.sh|*.json|*.yaml|*.yml|*.toml|*.cfg|*.log|*.lock) is_submission=0 ;;
esac

[ "$is_submission" -eq 0 ] && exit 0

# Emit non-blocking feedback pointing at the standard and the specific file.
if command -v jq >/dev/null 2>&1; then
  jq -n --arg f "$fp" '{
    hookSpecificOutput: {
      hookEventName: "PostToolUse",
      additionalContext: ("Submission-ready file just written: \($f). Before treating it as done, scan it against .kiro/steering/human-authored-writing.md and fix any violations: banned vocabulary (delve, leverage, utilize, robust, comprehensive, pivotal, crucial, significant, underscores, myriad, etc.), banned phrases and sentence openers, uniform sentence rhythm, narrator/structure-announcing voice, and the zero-tolerance em-dash ban (search for the — character; there must be zero). Also flag casual/colloquial phrasing and keep a formal academic register.")
    }
  }'
else
  # Fallback: plain-text feedback (PostToolUse stdout on exit 0 is best-effort).
  echo "Submission-ready file written: $fp. Scan against .kiro/steering/human-authored-writing.md (banned words/phrases/openers, sentence rhythm, narrator voice, zero em dashes) and fix violations."
fi

exit 0
