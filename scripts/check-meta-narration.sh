#!/usr/bin/env bash
# check-meta-narration.sh — gate against document scaffolding leaking into an
# EXTERNAL / supervisor-facing / reviewer-facing deliverable.
#
# WHY (2026-08-02): the v2 Barneto memo leaked (a) the supervisor's own meeting
# instructions back at the supervisor ("my supervisor asked me on 17 June"),
# (b) internal planning artifacts ("the two-page note"), and (c) internal
# framing tags ("FD1 tag", "PHENOMENON-EVIDENCE", "METHOD-SPINE") printed in an
# exhibit. None of these belong in a document a human reviewer reads as finished
# scholarship. No existing writing rule caught them because none banned them.
#
# This catches the PATTERN-MATCHABLE subset. Fuzzy process meta-narration
# ("I read X as...", "so I keep this lens conceptual", "as the next section
# shows") is a judgment call the eval agent must still review; grep cannot own
# that. See .kiro/steering/human-authored-writing.md "No meta-narration".
#
# Usage: scripts/check-meta-narration.sh <file> [file...]
# Exit: 0 clean, 1 = leak found (prints file:line:match).

set -euo pipefail

# (1) Internal framing-tag jargon (these are workspace scaffolding, never prose):
TAGS='FD[0-9]|PHENOMENON-EVIDENCE|METHOD-SPINE|brain package|brain-package|framing decision|framing-decision|contract criteria|hard requirement'

# (2) Supervisor / advisor relationship references (do not narrate the advisor's
#     instructions back into a document the advisor reads as scholarship):
ADVISOR='my supervisor|the supervisor asked|supervision meeting|Barneto asked|as (my |the )?(advisor|supervisor)|you (asked|suggested|offered|named)|per your|as you (asked|requested|suggested)'

# (3) Internal-artifact references (unpublished scaffolding docs):
ARTIFACTS='two-page note|two-pager|the brain|prior draft|v1 draft|earlier draft|our earlier|this memo establishes|in this memo|carried (over )?from the'

PATTERN="$TAGS|$ADVISOR|$ARTIFACTS"

if [ "$#" -eq 0 ]; then echo "usage: $0 <file> [file...]" >&2; exit 2; fi

found=0
for f in "$@"; do
  [ -f "$f" ] || { echo "skip (not a file): $f" >&2; continue; }
  if grep -ainoE "$PATTERN" "$f" | sed "s|^|$f:|"; then
    found=1
  fi
done

if [ "$found" -eq 1 ]; then
  echo "" >&2
  echo "FAIL: document-scaffolding leak above. An external/reviewer-facing deliverable" >&2
  echo "must not name the supervisor's instructions, internal planning artifacts, or" >&2
  echo "internal framing tags. State the scholarly claim directly. (Fuzzy process" >&2
  echo "meta-narration is also banned but not fully grep-catchable; see the rule.)" >&2
  exit 1
fi
echo "PASS: no scaffolding-leak patterns in $# file(s)."
exit 0
