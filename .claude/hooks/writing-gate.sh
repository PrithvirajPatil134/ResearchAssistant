#!/usr/bin/env bash
# writing-gate.sh — Claude Code PostToolUse hook (matcher: Edit|Write|MultiEdit).
#
# Claude Code equivalent of the Kiro hooks `check-agent-writing` +
# `check-submission-writing` (consolidated). After a write to reviewer-facing
# academic content, it (1) RUNS the deterministic content gates and reports any
# real violations, and (2) asks the assistant to scan the file against
# .kiro/steering/human-authored-writing.md for the fuzzy issues grep can't own.
#
# Mechanism (per code.claude.com/docs/en/hooks): PostToolUse fires AFTER the tool
# runs and cannot block it. Parity with Kiro's post-write agent action is achieved
# by returning additionalContext (non-blocking feedback Claude acts on next turn).
#
# WHY THIS WAS HARDENED (2026-08-03): the prior version only emitted a generic
# "scan for banned vocab / em-dashes" reminder. It did NOT run the deterministic
# gates and never named meta-narration or audience/register consistency. Result:
# the Prashar candidate-dimensions v2 shipped with the advisor's own instructions
# narrated back at him ("You pointed me to Sheth"), a third-person reference to
# the reader ("Prashar and I agreed"), and exercise self-narration ("the
# dimensions are candidates, offered for a co-author's challenge") — none caught.
# Now the hook actually invokes check-meta-narration.sh + check-absolute-absence.sh
# and surfaces their output, and the path filter includes communication/.

set -euo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
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

# Reviewer-facing filter (union of the two Kiro hooks' rules + communication/):
#   dir contains workspace/ | output/ | assignment/ | communication/ | feedback/  OR
#   filename contains Submission|Paper|Teaching|Case|revised|email|memo
is_submission=0
case "$fp" in
  */workspace/*|*/output/*|*/assignment/*|*/communication/*|*/feedback/*) is_submission=1 ;;
esac
case "$base" in
  *Submission*|*Paper*|*Teaching*|*Case*|*revised*|*email*|*memo*) is_submission=1 ;;
esac

# Skip obvious non-prose even if the path matched (code/config/steering/logs).
case "$base" in
  *.py|*.sh|*.json|*.yaml|*.yml|*.toml|*.cfg|*.log|*.lock) is_submission=0 ;;
esac

[ "$is_submission" -eq 0 ] && exit 0

# --- Run the deterministic gates on the file and collect real violations ------
gate_report=""
if [ -f "$fp" ]; then
  meta_out="$(bash "$ROOT/scripts/check-meta-narration.sh" "$fp" 2>&1 || true)"
  case "$meta_out" in
    PASS*) : ;;
    *) gate_report="${gate_report}\n[check-meta-narration.sh] FAILED:\n${meta_out}\n" ;;
  esac
  abs_out="$(bash "$ROOT/scripts/check-absolute-absence.sh" "$fp" 2>&1 || true)"
  case "$abs_out" in
    PASS*) : ;;
    *) gate_report="${gate_report}\n[check-absolute-absence.sh] FAILED:\n${abs_out}\n" ;;
  esac
  # Deterministic em-dash count (zero-tolerance rule).
  # (|| true: grep exits 1 on no-match, which set -e/pipefail would abort on.)
  emdash="$( { grep -o '—' "$fp" 2>/dev/null || true; } | wc -l | tr -d ' ')"
  if [ "${emdash:-0}" -gt 0 ]; then
    gate_report="${gate_report}\n[em-dash] ${emdash} em-dash character(s) found; the standard is zero.\n"
  fi
fi

msg="Reviewer-facing file just written: ${fp}. Before treating it as done, you MUST:
1. RESOLVE the deterministic-gate output below (if any) — these are confirmed violations, not suggestions.
2. Confirm AUDIENCE + REGISTER consistency: identify who reads this doc, then verify the voice never breaks it. A doc addressed TO a person must not refer to that person in the third person, narrate their instructions back at them, or describe the exercise/assignment itself. A standalone scholarly artifact must not use second-person 'you' at all.
3. Scan against .kiro/steering/human-authored-writing.md: banned vocabulary (delve, leverage, utilize, robust, comprehensive, pivotal, crucial, significant, underscores, myriad, etc.), banned phrases/openers, uniform sentence rhythm, narrator/structure-announcing voice, and the zero-tolerance em-dash ban.
4. For a substantive reviewer-facing deliverable, do NOT hand-finalize: run it through ra-prose-editor and ra-content-evaluator before calling it done."

if [ -n "$gate_report" ]; then
  msg="${msg}

=== DETERMINISTIC GATE OUTPUT (must fix) ===${gate_report}"
fi

if command -v jq >/dev/null 2>&1; then
  jq -n --arg m "$msg" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $m}}'
else
  printf '%b\n' "$msg"
fi

exit 0
