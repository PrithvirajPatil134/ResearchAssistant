#!/usr/bin/env bash
# py-lint.sh — Claude Code PostToolUse hook (matcher: Edit|Write|MultiEdit).
#
# Claude Code equivalent of the Kiro hook `lint-agents`. When an agent, workflow,
# or core Python file is written, run `python3 -m py_compile` to catch syntax
# errors before a workflow run hits them.
#
# Mechanism (per code.claude.com/docs/en/hooks): PostToolUse cannot block the
# write (it already happened), but exit 2 feeds stderr back to Claude as an error
# message it must address. On a clean compile we exit 0 silently. Only the three
# Kiro-scoped directories are linted; everything else is a no-op.
#
# Kiro original preserved for the Kiro runtime; this is the CC-native path.

set -euo pipefail

INPUT="$(cat)"

fp=""
if command -v jq >/dev/null 2>&1; then
  fp="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)"
fi
if [ -z "$fp" ]; then
  fp="$(printf '%s' "$INPUT" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed -E 's/.*:[[:space:]]*"([^"]*)"/\1/' || true)"
fi

[ -z "$fp" ] && exit 0

# Only lint agent / workflow / core Python (mirrors the Kiro matcher).
case "$fp" in
  *src/research_assistant/agents/*.py|*src/research_assistant/workflows/*.py|*src/research_assistant/core/*.py) ;;
  *) exit 0 ;;
esac

# File must exist (write succeeded) to compile.
[ -f "$fp" ] || exit 0

if err="$(python3 -m py_compile "$fp" 2>&1)"; then
  exit 0
else
  echo "py_compile failed for ${fp}:" >&2
  echo "$err" >&2
  exit 2
fi
