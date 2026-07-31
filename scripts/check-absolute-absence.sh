#!/usr/bin/env bash
# check-absolute-absence.sh — deterministic gate for the no-assumption rule's
# "No Absolute-Absence Claims" clause (.kiro/steering/no-assumption-rule.md).
#
# WHY THIS EXISTS (2026-07-30): A 20-memo eval experiment showed the LLM-judge
# (ra-content-evaluator) cannot reliably tell FORBIDDEN absolute-absence claims
# ("no study has", "first to") from the REQUIRED insufficiency framing
# ("the literature remains limited", "has not yet been applied"). It flagged all
# 20 memos as violators when direct grep found only 4. For a binary, pattern-
# matchable rule, a grep-gate is more reliable than a judge. Use this to gate;
# spend the judge on grounding/coherence, which it scores consistently.
#
# Usage: scripts/check-absolute-absence.sh <file-or-glob> [more files...]
# Exit: 0 = clean, 1 = at least one forbidden phrase found (prints file:line:match).

set -euo pipefail

# FORBIDDEN forms only. Deliberately narrow: these assert a universal negative
# that cannot be sourced. Insufficiency phrasings are NOT matched here on purpose.
FORBIDDEN='no study has|no paper (exists|has)|no research (has|addresses)|nobody has|no peer-reviewed study has|the first study to|for the first time|first to (test|apply|join|code|examine|study|address)|has never been (studied|tested|examined)|no published (operationalization|study|work|measure)[a-z ]*(codes|exists|has|addresses)?|no prior (study|work|research) has'

# PERMITTED (documented here so future editors do not "fix" the gate to catch them):
#   "few studies have examined" / "the literature remains limited on" /
#   "existing work has not yet sufficiently addressed" / "systematic evidence is
#   scarce on" / "does not yet exist" / "has not yet been applied".

if [ "$#" -eq 0 ]; then
  echo "usage: $0 <file> [file...]" >&2
  exit 2
fi

found=0
for f in "$@"; do
  [ -f "$f" ] || { echo "skip (not a file): $f" >&2; continue; }
  # -a: treat as text (read_binary output and some md carry null bytes; see
  #     no-assumption-rule "tool results are not facts" — a silent-skip bug).
  if grep -ainoE "$FORBIDDEN" "$f" | sed "s|^|$f:|"; then
    found=1
  fi
done

if [ "$found" -eq 1 ]; then
  echo "" >&2
  echo "FAIL: forbidden absolute-absence phrasing above. Reframe as insufficiency" >&2
  echo "(e.g. 'the literature remains limited on X', 'has not yet been applied to X')." >&2
  exit 1
fi
echo "PASS: no absolute-absence phrasing found in $# file(s)."
exit 0
