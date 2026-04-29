#!/bin/bash
# Kiro Evolve — IDE hook: check if transcript review is due
# Triggers on agentSpawn/new session. Checks if enough prompts/days have passed
# to warrant suggesting a transcript review.

set -euo pipefail

TRANSCRIPT_DIR="$HOME/.kiro/transcripts"
KNOWLEDGE_DIR="$PWD/.kiro/steering/evolved"
STEERING_DIR="$PWD/.kiro/steering"
LAST_REVIEW_FILE="$TRANSCRIPT_DIR/.last-review"
FIRST_REVIEW_MARKER="$TRANSCRIPT_DIR/.first-review-done"

# Thresholds
MIN_PROMPTS=50
MIN_DAYS=2

# Seed if not exists
if [[ ! -f "$LAST_REVIEW_FILE" ]]; then
    date -v-${MIN_DAYS}d +%Y-%m-%d > "$LAST_REVIEW_FILE" 2>/dev/null || \
        date -d "${MIN_DAYS} days ago" +%Y-%m-%d > "$LAST_REVIEW_FILE" 2>/dev/null || \
        date +%Y-%m-%d > "$LAST_REVIEW_FILE"
    exit 0
fi

LAST_REVIEW=$(cat "$LAST_REVIEW_FILE")
TODAY=$(date +%Y-%m-%d)

# Gate 1: Days since last review
DAYS_SINCE=$(python3 -c "
from datetime import date
last = date.fromisoformat('$LAST_REVIEW')
today = date.fromisoformat('$TODAY')
print((today - last).days)
")

if [[ "$DAYS_SINCE" -lt "$MIN_DAYS" ]]; then
    exit 0
fi

# Gate 2: Count new prompts since last review
NEW_TRANSCRIPTS=()
PROMPT_COUNT=0

for f in "$TRANSCRIPT_DIR"/*.md; do
    [[ -f "$f" ]] || continue
    FNAME=$(basename "$f" .md)
    # Skip non-date files
    [[ "$FNAME" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || continue
    # Include only transcripts dated after last review
    if [[ "$FNAME" > "$LAST_REVIEW" ]]; then
        NEW_TRANSCRIPTS+=("$f")
        COUNT=$(grep -c "^## User" "$f" 2>/dev/null || echo 0)
        PROMPT_COUNT=$((PROMPT_COUNT + COUNT))
    fi
done

if [[ "$PROMPT_COUNT" -lt "$MIN_PROMPTS" ]]; then
    exit 0
fi

# Both gates passed. Determine first-review note.
FIRST_REVIEW_NOTE=""
if [[ ! -f "$FIRST_REVIEW_MARKER" ]]; then
    FIRST_REVIEW_NOTE="
Note: This is the user's first Kiro Evolve review. If the user completes this review and approves at least one file, congratulate them. Then create the marker file: touch $FIRST_REVIEW_MARKER"
fi

# Output the review prompt for the agent
cat <<EOF
Kiro Evolve: A transcript review is due ($DAYS_SINCE days since last review, $PROMPT_COUNT new prompts). At a natural point, suggest a review to the user.

When user agrees:
1. Read ALL existing files in $KNOWLEDGE_DIR/ AND $STEERING_DIR/ to understand what's already captured.
2. Read each transcript dated after $LAST_REVIEW:
$(printf '   - %s\n' "${NEW_TRANSCRIPTS[@]}")
3. Apply a filter gate: "Would this change how the assistant interacts in a future session?" Evolve IS for: preferences, domain context, stakeholder dynamics, calibration patterns, reusable frameworks, tone/voice refinements. Evolve is NOT for: debugging sessions, tool configuration, one-off scripts, prompt engineering fixes, task execution artifacts.
4. Analyze across all transcripts for:
   - Learning preferences (format, length, tone patterns)
   - What worked vs. didn't (first-try accepts vs. revision patterns)
   - Domain-specific context (research topics, academic standards, professor feedback patterns)
   - Calibration (over/under-explaining, wrong assumptions)
   - Recurring workflows and stakeholder-specific preferences
   - Reusable frameworks or templates
5. Convert all relative time references to absolute dates (e.g., "this week" becomes "week of $TODAY").
6. For each candidate, check whether it belongs as an update to an existing knowledge or steering file rather than a new file. Prefer updating existing files.
7. Show FULL FILE CONTENT for each proposal. For updates, show the complete updated file and note what changed.
8. Present proposals ONE AT A TIME. Ask "Approve, edit, or reject?" and WAIT. Maximum 5 proposals per review.
9. Write approved files to $KNOWLEDGE_DIR/.
10. May also propose edits to existing steering docs in $STEERING_DIR/.
11. After review: touch $TRANSCRIPT_DIR/.reviewed-FILENAME for each reviewed transcript (use the date portion of the filename).
12. Update $LAST_REVIEW_FILE with today's date: $TODAY
$FIRST_REVIEW_NOTE
EOF

exit 0
