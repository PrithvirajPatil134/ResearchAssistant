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
# WIDENED (2026-08-03): the Prashar candidate-dimensions doc leaked a SECOND
# class the original patterns missed — a document written TO the co-author that
# (a) narrated his own instructions back at him with verbs outside the list
# ("You pointed me to Sheth"), (b) referred to him in the third person inside a
# doc he is the reader of ("Prashar and I agreed"), and (c) narrated the
# exercise itself ("the dimensions are candidates, offered for a co-author's
# challenge", "the more I work with it the more the method holds"). Added the
# second-person-instruction verbs, the "<Name> and I <verb>" form, and a
# process/framing-narration tier.
#
# This catches the PATTERN-MATCHABLE subset. Fuzzy process meta-narration that
# does not use these stock phrasings is still a judgment call the eval agent
# must review; grep cannot own all of it. See
# .kiro/steering/human-authored-writing.md "No meta-narration".
#
# Usage: scripts/check-meta-narration.sh <file> [file...]
# Exit: 0 clean, 1 = leak found (prints file:line:match).

set -euo pipefail

# MODES (added 2026-08-05): the register patterns below (advisor-address, exercise
# self-narration) are violations ONLY in standalone SCHOLARSHIP. In genuine
# CORRESPONDENCE (an email/feedback addressed TO a person) second-person address
# and "you suggested" / "for you to challenge" are the CORRECT register, not leaks.
# Applying the scholarship patterns to emails produced false positives on the
# Prashar cover email. So the gate now has two modes:
#   scholarship (default): all patterns  — for output/, papers, reviews, memos.
#   correspondence:        universal only — for emails and feedback replies.
# Auto-detected from the path (communication/ or *email*/*reply* → correspondence),
# overridable with --mode=scholarship|correspondence.
MODE=""
case "${1:-}" in
  --mode=scholarship)   MODE=scholarship; shift ;;
  --mode=correspondence) MODE=correspondence; shift ;;
esac

# (1) Internal framing-tag jargon (these are workspace scaffolding, never prose):
TAGS='FD[0-9]|PHENOMENON-EVIDENCE|METHOD-SPINE|brain package|brain-package|framing decision|framing-decision|contract criteria|hard requirement'

# (2) Supervisor / advisor relationship references (do not narrate the advisor's
#     instructions back into a document the advisor reads as scholarship).
#     Widened verb set (pointed/told/wanted/asked/suggested/offered/named/
#     mentioned/flagged/directed) + "you pointed me", "as you pointed".
ADVISOR='my supervisor|the supervisor asked|supervision meeting|Barneto asked|as (my |the )?(advisor|supervisor)|you (pointed|asked|suggested|offered|named|told|wanted|mentioned|flagged|directed|said)|(pointed|steered) me (to|toward)|per your|as you (asked|requested|suggested|pointed|mentioned|flagged)'

# (2b) Third-person reference to the named reader inside a doc they will read.
#     "<Capitalized Name> and I <agreed/decided/...>" is the tell that a working
#     note about the advisor got welded into a doc addressed to the advisor.
#     Matched case-SENSITIVELY (see the -a vs case note below): the leading
#     capital is the whole signal, so a lowercase "as the agreed" must not match.
ADVISOR_3P='[A-Z][a-z]+ and I (agreed|decided|discussed|settled|chose|aligned)|as [A-Z][a-z]+ (and I )?(agreed|suggested|noted|proposed)'

# (3) Internal-artifact references (unpublished scaffolding docs):
ARTIFACTS='two-page note|two-pager|the brain|prior draft|v1 draft|earlier draft|our earlier|this memo establishes|in this memo|carried (over )?from the|in the last draft|than it was in the'

# (4) Process / exercise self-narration (describing the deliverable's own purpose
#     or the author's working process, rather than making the scholarly claim):
PROCESS='offered for (a |the )?(co-author|reviewer|supervisor).{0,20}(challenge|review)|the dimensions are candidates|offered (them )?for .{0,15}challenge|the more I (work|worked) with it|before the frame is committed|these are the (exact )?(judgments|calls)|the (four )?calls I am least sure of|I put to you|where you can weigh in|for you to challenge'

if [ "$#" -eq 0 ]; then echo "usage: $0 [--mode=scholarship|correspondence] <file> [file...]" >&2; exit 2; fi

# Universal patterns (case-insensitive; wrong in every document type).
UNIVERSAL_CI="$TAGS|$ARTIFACTS"
# Register patterns (scholarship mode only). ADVISOR/PROCESS are case-insensitive;
# ADVISOR_3P is applied case-SENSITIVELY in a second grep so its capital-letter
# heuristic works.
REGISTER_CI="$ADVISOR|$PROCESS"

detect_mode() { # $1 = path
  case "$1" in
    */communication/*|*email*|*reply*|*feedback/response*) echo correspondence ;;
    *) echo scholarship ;;
  esac
}

found=0
for f in "$@"; do
  [ -f "$f" ] || { echo "skip (not a file): $f" >&2; continue; }
  m="${MODE:-$(detect_mode "$f")}"
  # -a: treat as text (read_binary output / some md carry null bytes).
  if grep -ainoE "$UNIVERSAL_CI" "$f" | sed "s|^|$f:|"; then found=1; fi
  if [ "$m" = "scholarship" ]; then
    if grep -ainoE "$REGISTER_CI" "$f" | sed "s|^|$f:|"; then found=1; fi
    if grep -noE "$ADVISOR_3P" "$f" | sed "s|^|$f:|"; then found=1; fi
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
