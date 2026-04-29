#!/bin/bash
# Kiro Evolve — IDE hook: check if transcript cleanup is due
# Triggers on agentSpawn. Runs every 90 days, targets transcripts older than 90 days that have been reviewed.

set -euo pipefail

TRANSCRIPT_DIR="$HOME/.kiro/transcripts"
LAST_CLEANUP_FILE="$TRANSCRIPT_DIR/.last-cleanup-check"

# Thresholds
CLEANUP_INTERVAL_DAYS=90
OLD_THRESHOLD_DAYS=90

# Seed if not exists
if [[ ! -f "$LAST_CLEANUP_FILE" ]]; then
    date +%Y-%m-%d > "$LAST_CLEANUP_FILE"
    exit 0
fi

LAST_CLEANUP=$(cat "$LAST_CLEANUP_FILE")
TODAY=$(date +%Y-%m-%d)

# Gate: Days since last cleanup check
DAYS_SINCE=$(python3 -c "
from datetime import date
last = date.fromisoformat('$LAST_CLEANUP')
today = date.fromisoformat('$TODAY')
print((today - last).days)
")

if [[ "$DAYS_SINCE" -lt "$CLEANUP_INTERVAL_DAYS" ]]; then
    exit 0
fi

# Calculate cutoff date
CUTOFF=$(python3 -c "
from datetime import date, timedelta
today = date.fromisoformat('$TODAY')
cutoff = today - timedelta(days=$OLD_THRESHOLD_DAYS)
print(cutoff.isoformat())
")

# Find old transcripts (filename date before cutoff) with reviewed markers
REVIEWED_OLD=()
UNREVIEWED_OLD=0

for f in "$TRANSCRIPT_DIR"/*.md; do
    [[ -f "$f" ]] || continue
    FNAME=$(basename "$f" .md)
    [[ "$FNAME" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || continue
    
    if [[ "$FNAME" < "$CUTOFF" ]]; then
        if [[ -f "$TRANSCRIPT_DIR/.reviewed-$FNAME" ]]; then
            SIZE=$(wc -c < "$f" | tr -d ' ')
            REVIEWED_OLD+=("$FNAME ($(($SIZE / 1024))KB)")
        else
            UNREVIEWED_OLD=$((UNREVIEWED_OLD + 1))
        fi
    fi
done

# If nothing to clean up, reset timer and exit
if [[ "${#REVIEWED_OLD[@]}" -eq 0 ]]; then
    echo "$TODAY" > "$LAST_CLEANUP_FILE"
    exit 0
fi

# Output cleanup prompt
cat <<EOF
Kiro Evolve: Transcript cleanup is due ($DAYS_SINCE days since last check). ${#REVIEWED_OLD[@]} old reviewed transcripts are eligible for cleanup.

Eligible for cleanup (all already reviewed):
$(printf '  - %s\n' "${REVIEWED_OLD[@]}")

$(if [[ "$UNREVIEWED_OLD" -gt 0 ]]; then echo "Note: $UNREVIEWED_OLD additional old transcripts exist but have not been reviewed. They are protected. Consider running a review first."; fi)

Ask the user if they want to review old transcripts for cleanup. Let them pick individually. Never suggest deleting all. Require explicit per-file confirmation. When deleting a transcript, also delete the corresponding .reviewed-YYYY-MM-DD marker. After completion (whether user accepts or declines), update $LAST_CLEANUP_FILE with: $TODAY
EOF

exit 0
