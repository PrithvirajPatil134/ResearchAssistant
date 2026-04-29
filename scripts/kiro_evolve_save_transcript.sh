#!/bin/bash
# Kiro Evolve — IDE hook: save transcript
# Captures user prompts and assistant responses to daily transcript files.
# Reads JSON event from stdin (supplied by Kiro IDE hook system).

set -euo pipefail

TRANSCRIPT_DIR="$HOME/.kiro/transcripts"
mkdir -p "$TRANSCRIPT_DIR"

TODAY=$(date +%Y-%m-%d)
TRANSCRIPT_FILE="$TRANSCRIPT_DIR/$TODAY.md"
TIMESTAMP=$(date +%H:%M:%S)

# Create file with header if new
if [[ ! -f "$TRANSCRIPT_FILE" ]]; then
    echo "# Transcript — $TODAY" > "$TRANSCRIPT_FILE"
fi

# Read JSON event from stdin
EVENT=$(cat)

# Determine event type and extract content
EVENT_TYPE=$(echo "$EVENT" | jq -r '.hook_event_name // empty')

case "$EVENT_TYPE" in
    "promptSubmit"|"userPromptSubmit")
        PROMPT=$(echo "$EVENT" | jq -r '.prompt // .user_prompt // empty')
        if [[ -n "$PROMPT" ]]; then
            {
                echo ""
                echo "## User — $TIMESTAMP"
                echo ""
                echo "$PROMPT"
            } >> "$TRANSCRIPT_FILE"
        fi
        ;;
    "agentStop"|"stop")
        RESPONSE=$(echo "$EVENT" | jq -r '.assistant_response // .response // empty')
        if [[ -n "$RESPONSE" ]]; then
            {
                echo ""
                echo "## Assistant — $TIMESTAMP"
                echo ""
                echo "$RESPONSE"
            } >> "$TRANSCRIPT_FILE"
        fi
        ;;
    *)
        # Unknown event, silently skip
        exit 0
        ;;
esac

exit 0
