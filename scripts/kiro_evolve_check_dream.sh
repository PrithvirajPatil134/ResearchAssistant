#!/bin/bash
# Kiro Evolve — IDE hook: check if knowledge consolidation (dream) is due
# Triggers on agentSpawn. Dual-gate: 14 days since last dream AND 5+ evolved files.

set -euo pipefail

TRANSCRIPT_DIR="$HOME/.kiro/transcripts"
KNOWLEDGE_DIR="$PWD/.kiro/steering/evolved"
STEERING_DIR="$PWD/.kiro/steering"
LAST_DREAM_FILE="$TRANSCRIPT_DIR/.last-dream"

# Thresholds
DREAM_INTERVAL_DAYS=14
MIN_EVOLVED_FILES=5

# Seed if not exists
if [[ ! -f "$LAST_DREAM_FILE" ]]; then
    date +%Y-%m-%d > "$LAST_DREAM_FILE"
    exit 0
fi

LAST_DREAM=$(cat "$LAST_DREAM_FILE")
TODAY=$(date +%Y-%m-%d)

# Gate 1: Days since last dream
DAYS_SINCE=$(python3 -c "
from datetime import date
last = date.fromisoformat('$LAST_DREAM')
today = date.fromisoformat('$TODAY')
print((today - last).days)
")

if [[ "$DAYS_SINCE" -lt "$DREAM_INTERVAL_DAYS" ]]; then
    exit 0
fi

# Gate 2: Count evolved knowledge files
if [[ ! -d "$KNOWLEDGE_DIR" ]]; then
    exit 0
fi

FILE_COUNT=$(find "$KNOWLEDGE_DIR" -maxdepth 1 -name "*.md" -type f | wc -l | tr -d ' ')

if [[ "$FILE_COUNT" -lt "$MIN_EVOLVED_FILES" ]]; then
    exit 0
fi

# Both gates passed. Output the dream prompt.
cat <<EOF
Kiro Evolve: Knowledge consolidation (dream) is due ($DAYS_SINCE days since last dream, $FILE_COUNT evolved files). At a natural point, suggest a consolidation pass to the user.

When user agrees:
1. Read ALL files in $KNOWLEDGE_DIR/ AND $STEERING_DIR/.
2. Analyze evolved files for:
   - Staleness (relative dates, outdated references, superseded decisions)
   - Contradictions (between evolved files or against steering files)
   - Overlap and bloat (files covering the same topic, files over ~50 lines)
   - Accuracy (evolved content that duplicates or conflicts with steering)
3. For each issue, propose a specific change with FULL file content shown. For merges, show the consolidated file and note which files it replaces. For deletions, explain why.
4. Present proposals ONE AT A TIME. Ask "Approve, edit, or reject?" and WAIT. Maximum 5 proposals per dream.
5. After consolidation: update $LAST_DREAM_FILE with today's date: $TODAY

Important: This is a CONSOLIDATION pass, not a review. Do not analyze transcripts or propose new knowledge. Focus only on improving what has already graduated.
EOF

exit 0
