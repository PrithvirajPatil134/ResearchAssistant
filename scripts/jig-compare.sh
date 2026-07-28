#!/usr/bin/env bash
# jig-compare.sh — Run a task through BOTH our pipeline and Jig, then compare.
#
# Usage:
#   bash scripts/jig-compare.sh <tier> <prompt-file> <space> [options]
#
# Tiers:
#   a — research-explore (maps to spawn-gpu-agent.sh)
#   b — docs-technical (maps to claude-dispatch.sh)
#   c — research-longdoc (maps to long-doc-orchestrate.sh)
#
# Example:
#   bash scripts/jig-compare.sh a data/drafts/test-prompt.md QNTR

set -uo pipefail

TIER="${1:?Usage: jig-compare.sh <tier> <prompt-file> <space> [options]}"
PROMPT_FILE="${2:?Usage: jig-compare.sh <tier> <prompt-file> <space> [options]}"
SPACE="${3:?Usage: jig-compare.sh <tier> <prompt-file> <space> [options]}"
shift 3

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="${WORKSPACE_ROOT}/scripts"

# Prefer the project venv (research_assistant + deps installed editable) for the
# eval tools; fall back to system python3.
if [ -x "${WORKSPACE_ROOT}/.venv/bin/python3" ]; then
  RA_PYTHON="${WORKSPACE_ROOT}/.venv/bin/python3"
else
  RA_PYTHON="python3"
fi
# 1M-context model for dispatched agents (see long-doc-orchestrate.sh). Override via RA_AGENT_MODEL.
RA_AGENT_MODEL="${RA_AGENT_MODEL:-claude-opus-4-8[1m]}"
LOG_DIR="${WORKSPACE_ROOT}/data/logs/jig-comparison"
JIG_BIN="${HOME}/.local/bin/jig"
JIG_DIR="${HOME}/workplace/Jig"
JIG_OUTPUT_DIR="${WORKSPACE_ROOT}/.jig-output/ra"

mkdir -p "$LOG_DIR" "$JIG_OUTPUT_DIR"

if [ ! -f "$PROMPT_FILE" ]; then
  echo "error: prompt file not found: ${PROMPT_FILE}" >&2
  exit 2
fi

if [ ! -x "$JIG_BIN" ] && [ ! -f "$JIG_BIN" ]; then
  echo "error: jig binary not found. Run 'bash scripts/jig-install.sh' first." >&2
  exit 2
fi

TIMESTAMP="$(date +%Y-%m-%d-%H-%M)"
COMPARE_ID="jig-compare-${TIER}-${TIMESTAMP}"

echo "[jig-compare] === Comparison: ${COMPARE_ID} ==="
echo "[jig-compare] Tier: ${TIER}"
echo "[jig-compare] Prompt: ${PROMPT_FILE}"
echo "[jig-compare] Space: ${SPACE}"
echo ""

# --- Step 1: Run OUR pipeline ---
echo "[jig-compare] Running our pipeline (tier ${TIER})..."
OUR_OUTPUT="/tmp/${COMPARE_ID}-ours.md"
OUR_START=$(date +%s)

case "$TIER" in
  a)
    bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "${COMPARE_ID}-ours" "$OUR_OUTPUT" \
      --model "$RA_AGENT_MODEL" --allowed-tools "Read,Glob,Grep,Bash" \
      --prompt-file "$PROMPT_FILE" || true
    ;;
  b)
    TASK_NAME="$(head -1 "$PROMPT_FILE" | sed 's/^#\s*//')"
    bash "${SCRIPTS_DIR}/claude-dispatch.sh" "${COMPARE_ID}-ours" "$OUR_OUTPUT" \
      "$TASK_NAME" "explain" --model "$RA_AGENT_MODEL" \
      --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
      --prompt-file "$PROMPT_FILE" || true
    ;;
  c)
    bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "${COMPARE_ID}-ours" "$OUR_OUTPUT" \
      --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
      --prompt-file "$PROMPT_FILE" || true
    ;;
  *)
    echo "error: unknown tier '${TIER}'. Use a, b, or c." >&2
    exit 2
    ;;
esac

OUR_END=$(date +%s)
OUR_TIME=$((OUR_END - OUR_START))
echo "[jig-compare] Our pipeline completed in ${OUR_TIME}s"

# --- Step 2: Wait for MCP stagger ---
echo "[jig-compare] Waiting 30 seconds (MCP stagger)..."
sleep 30

# --- Step 3: Run Jig workflow ---
echo "[jig-compare] Running Jig workflow (tier ${TIER})..."
JIG_OUTPUT="${JIG_OUTPUT_DIR}/${COMPARE_ID}.md"
JIG_START=$(date +%s)

JIG_WORKFLOW=""
case "$TIER" in
  a) JIG_WORKFLOW="ra/research-explore" ;;
  b) JIG_WORKFLOW="ra/docs-technical" ;;
  c) JIG_WORKFLOW="ra/research-longdoc" ;;
esac

JIG_TRACE_ID=""
JIG_TRACE_STEPS="[]"

if "$JIG_BIN" run "$JIG_WORKFLOW" \
  --input "prompt_file=${PROMPT_FILE}" \
  --input "space=${SPACE}" \
  --input "workspace_root=${WORKSPACE_ROOT}" \
  --output "$JIG_OUTPUT" 2>/tmp/jig-compare-stderr.log; then

  JIG_TRACE_ID=$("$JIG_BIN" trace --last --format json 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
  JIG_TRACE_STEPS=$("$JIG_BIN" trace --last --format json 2>/dev/null | python3 -c "import sys,json; print(json.dumps([s.get('name','') for s in json.load(sys.stdin).get('steps',[])]))" 2>/dev/null || echo "[]")
else
  echo "[jig-compare] WARNING: Jig workflow failed. Check /tmp/jig-compare-stderr.log"
fi

JIG_END=$(date +%s)
JIG_TIME=$((JIG_END - JIG_START))
echo "[jig-compare] Jig completed in ${JIG_TIME}s"

# --- Step 4: Generate contract ---
echo "[jig-compare] Generating evaluation contract..."
TASK_NAME="$(head -1 "$PROMPT_FILE" | sed 's/^#\s*//')"
CONTRACT_FILE="/tmp/${COMPARE_ID}-contract.yaml"

CONTRACT_JSON=$(printf '{"query": "%s", "workflow_name": "explain", "extracted_content": [], "persona_name": "%s"}' \
  "$(printf '%s' "$TASK_NAME" | sed 's/"/\\"/g')" "$SPACE")

printf '%s' "$CONTRACT_JSON" | "$RA_PYTHON" "${SCRIPTS_DIR}/build_contract.py" > "$CONTRACT_FILE" 2>/dev/null || true

# --- Step 5: Score both outputs ---
echo "[jig-compare] Scoring both outputs..."

OUR_SCORE="{}"
JIG_SCORE="{}"

if [ -f "$OUR_OUTPUT" ] && [ -s "$OUR_OUTPUT" ]; then
  OUR_SCORE=$("$RA_PYTHON" "${SCRIPTS_DIR}/run_eval.py" \
    --content-path "$OUR_OUTPUT" \
    --query "$TASK_NAME" \
    --contract-file "$CONTRACT_FILE" \
    --workflow-name "explain" 2>/dev/null) || OUR_SCORE="{}"
fi

if [ -f "$JIG_OUTPUT" ] && [ -s "$JIG_OUTPUT" ]; then
  JIG_SCORE=$("$RA_PYTHON" "${SCRIPTS_DIR}/run_eval.py" \
    --content-path "$JIG_OUTPUT" \
    --query "$TASK_NAME" \
    --contract-file "$CONTRACT_FILE" \
    --workflow-name "explain" 2>/dev/null) || JIG_SCORE="{}"
fi

# --- Step 6: Log results ---
echo "[jig-compare] Logging results..."

python3 -c "
import json, sys

our_score = json.loads('''${OUR_SCORE}''' if '''${OUR_SCORE}''' else '{}')
jig_score = json.loads('''${JIG_SCORE}''' if '''${JIG_SCORE}''' else '{}')

entry = {
    'id': '${COMPARE_ID}',
    'tier': '${TIER}',
    'prompt_file': '${PROMPT_FILE}',
    'space': '${SPACE}',
    'our_output': '${OUR_OUTPUT}',
    'our_score': {
        'structure': our_score.get('analyst_score', 0),
        'grounding': our_score.get('evaluator_evidence', 0),
        'completeness': our_score.get('evaluator_completeness', 0),
        'quality': our_score.get('reviewer_score', 0),
        'overall': our_score.get('analyst_score', 0),
        'passed': our_score.get('overall_pass', False)
    },
    'our_time_seconds': ${OUR_TIME},
    'jig_output': '${JIG_OUTPUT}',
    'jig_score': {
        'structure': jig_score.get('analyst_score', 0),
        'grounding': jig_score.get('evaluator_evidence', 0),
        'completeness': jig_score.get('evaluator_completeness', 0),
        'quality': jig_score.get('reviewer_score', 0),
        'overall': jig_score.get('analyst_score', 0),
        'passed': jig_score.get('overall_pass', False)
    },
    'jig_time_seconds': ${JIG_TIME},
    'jig_trace_steps': json.loads('${JIG_TRACE_STEPS}'),
    'jig_trace_id': '${JIG_TRACE_ID}',
    'date': '$(date +%Y-%m-%d)'
}

with open('${LOG_DIR}/comparison_log.jsonl', 'a') as f:
    f.write(json.dumps(entry) + '\n')

print(json.dumps(entry, indent=2))
" 2>/dev/null || echo "[jig-compare] WARNING: Failed to log results"

# --- Step 7: Print summary ---
echo ""
echo "[jig-compare] === COMPARISON SUMMARY ==="
echo "[jig-compare]   ID: ${COMPARE_ID}"
echo "[jig-compare]   Our pipeline: ${OUR_TIME}s"
echo "[jig-compare]   Jig pipeline: ${JIG_TIME}s"
echo "[jig-compare]   Our output: ${OUR_OUTPUT}"
echo "[jig-compare]   Jig output: ${JIG_OUTPUT}"
echo "[jig-compare]   Log: ${LOG_DIR}/comparison_log.jsonl"

# Cleanup
rm -f "$CONTRACT_FILE"
