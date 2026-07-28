#!/usr/bin/env bash
# claude-dispatch.sh — Wraps spawn-gpu-agent.sh with contract enforcement,
# heuristic pre-check, evaluation, retry logic, and hard kiro-cli fallback.
#
# macOS bash 3.2 compatible (no mapfile, no associative arrays).
#
# Usage:
#   bash scripts/claude-dispatch.sh <agent-id> <output-file> <task-name> \
#     <workflow-name> [--agent <name>] [--model opus] \
#     [--allowed-tools "..."] --prompt-file <path>
#
# Flow:
#   1. Build dispatch contract (prepend to prompt)
#   2. Spawn agent via spawn-gpu-agent.sh
#   3. Heuristic pre-check output
#   4. Run eval (heuristic scoring)
#   5. Pass → done. Fail → retry once with feedback. Fail again → escalate.
#   6. Log A/B comparison entry.
#   7. Hard fallback to kiro-cli on hard failures.

set -uo pipefail

# --- Parse required positional arguments ---
AGENT_ID="${1:?Usage: claude-dispatch.sh <agent-id> <output-file> <task-name> <workflow-name> [opts] --prompt-file <path>}"
OUTPUT_FILE="${2:?Usage: claude-dispatch.sh <agent-id> <output-file> <task-name> <workflow-name> [opts] --prompt-file <path>}"
TASK_NAME="${3:?Usage: claude-dispatch.sh <agent-id> <output-file> <task-name> <workflow-name> [opts] --prompt-file <path>}"
WORKFLOW_NAME="${4:?Usage: claude-dispatch.sh <agent-id> <output-file> <task-name> <workflow-name> [opts] --prompt-file <path>}"
shift 4

# --- Resolve workspace root ---
WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="${WORKSPACE_ROOT}/scripts"

# --- Resolve Python: prefer the project venv (has the research_assistant package
# + pyyaml/click installed editable); fall back to system python3. The eval tools
# (build_contract.py, run_eval.py) import the package and REQUIRE the venv. ---
if [ -x "${WORKSPACE_ROOT}/.venv/bin/python3" ]; then
  RA_PYTHON="${WORKSPACE_ROOT}/.venv/bin/python3"
else
  RA_PYTHON="python3"
fi

# --- SENTINEL_V2: guarantee a terminal sentinel even if dispatch dies mid-eval ---
SENTINEL_V2="${SENTINEL_V2:-1}"   # on by default (smoke-tested 2026-07-13); set SENTINEL_V2=0 to fall back to legacy
SENTINEL_DIR_CD="${WORKSPACE_ROOT}/.kiro/.gpu-agent-done"
_cd_final_written=0
if [ "$SENTINEL_V2" = "1" ] && [ -f "${SCRIPTS_DIR}/sentinel-lib.sh" ]; then
  # shellcheck source=/dev/null
  . "${SCRIPTS_DIR}/sentinel-lib.sh"
  # Inner spawn writes a provisional "awaiting_eval" sentinel; claude-dispatch owns
  # the final one (written atomically in Step 8). If we die before that, the trap
  # still leaves a terminal sentinel so the reconciler is never left waiting.
  export SENTINEL_DEFER=1
  _cd_trap() {
    [ "$_cd_final_written" = "1" ] && return 0
    local c
    c="$(printf '{\n  "agent_id": "%s",\n  "status": "dispatch_aborted",\n  "exit_code": 1,\n  "finished_at": "%s"\n}\n' \
      "$AGENT_ID" "$(date -u +%Y-%m-%dT%H:%M:%SZ)")"
    sentinel_write_atomic "${SENTINEL_DIR_CD}/${AGENT_ID}.done" "$c"
    sentinel_clear_running "$SENTINEL_DIR_CD" "$AGENT_ID"
  }
  trap '_cd_trap' EXIT INT TERM
fi

# --- Parse remaining arguments (backend args + --prompt-file) ---
PROMPT_FILE=""
BACKEND_ARGS=()

args=("$@")
i=0
while [ "$i" -lt "${#args[@]}" ]; do
  arg="${args[$i]}"
  if [ "$arg" = "--prompt-file" ]; then
    i=$((i + 1))
    PROMPT_FILE="${args[$i]:?--prompt-file requires a path}"
  else
    BACKEND_ARGS+=("$arg")
  fi
  i=$((i + 1))
done

if [ -z "$PROMPT_FILE" ]; then
  echo "error: --prompt-file is required for claude-dispatch.sh" >&2
  exit 2
fi

if [ ! -f "$PROMPT_FILE" ]; then
  echo "error: prompt file not found: $PROMPT_FILE" >&2
  exit 2
fi

# --- Step 1: Build dispatch contract and prepend to prompt ---
echo "[claude-dispatch] Building dispatch contract for task=${TASK_NAME}, workflow=${WORKFLOW_NAME}..."

CONTRACT_YAML=""
CONTRACT_JSON=$(printf '{"query": "%s", "workflow_name": "%s", "extracted_content": [], "persona_name": ""}' \
  "$(printf '%s' "$TASK_NAME" | sed 's/"/\\"/g')" \
  "$(printf '%s' "$WORKFLOW_NAME" | sed 's/"/\\"/g')")

CONTRACT_BUILD_ERR="/tmp/claude-dispatch-${AGENT_ID}-contract.err"
CONTRACT_YAML=$(printf '%s' "$CONTRACT_JSON" | "$RA_PYTHON" "${SCRIPTS_DIR}/build_contract.py" 2>"$CONTRACT_BUILD_ERR") || true
if [ -z "$CONTRACT_YAML" ]; then
  # Do NOT silently proceed with an empty contract — that would weaken the eval
  # gate invisibly. Warn loudly so a broken dependency/venv is caught, not masked.
  echo "[claude-dispatch] WARNING: contract build produced NO contract — the eval gate will run WITHOUT a dispatch contract. Check ${CONTRACT_BUILD_ERR} and the .venv (run: .venv/bin/python3 -m pip install -e .)." >&2
  [ -s "$CONTRACT_BUILD_ERR" ] && sed 's/^/[claude-dispatch]   /' "$CONTRACT_BUILD_ERR" >&2
fi

# Create enriched prompt file (contract + original prompt)
ENRICHED_PROMPT_FILE="/tmp/claude-dispatch-${AGENT_ID}-enriched.md"
CONTRACT_FILE="/tmp/claude-dispatch-${AGENT_ID}-contract.yaml"

if [ -n "$CONTRACT_YAML" ]; then
  printf '%s\n\n' "$CONTRACT_YAML" > "$ENRICHED_PROMPT_FILE"
  cat "$PROMPT_FILE" >> "$ENRICHED_PROMPT_FILE"
  printf '%s' "$CONTRACT_YAML" > "$CONTRACT_FILE"
  echo "[claude-dispatch] Contract prepended to prompt."
else
  cp "$PROMPT_FILE" "$ENRICHED_PROMPT_FILE"
  printf '' > "$CONTRACT_FILE"
  echo "[claude-dispatch] Contract generation failed; using original prompt."
fi

# --- Step 2: Spawn agent ---
START_TIME=$(date +%s)

echo "[claude-dispatch] Spawning agent ${AGENT_ID} (backend=claude)..."

SPAWN_EXIT=0
bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$AGENT_ID" "$OUTPUT_FILE" \
  "${BACKEND_ARGS[@]}" --prompt-file "$ENRICHED_PROMPT_FILE" || SPAWN_EXIT=$?

END_TIME=$(date +%s)
RUNTIME=$((END_TIME - START_TIME))

# --- Step 3: Heuristic pre-check ---
echo "[claude-dispatch] Running heuristic pre-check..."

# If the agent wrote a deliverable file (docs/*.md, spaces/*/output/*.md),
# evaluate that instead of the raw CLI output log.
EVAL_TARGET="$OUTPUT_FILE"
if [ -f "$OUTPUT_FILE" ]; then
  # Look for the most recently modified .md file in docs/ or spaces/*/output/
  DELIVERABLE=$(find "${WORKSPACE_ROOT}/docs" "${WORKSPACE_ROOT}/spaces" -name "*.md" -newer "$OUTPUT_FILE" -type f 2>/dev/null | head -1)
  if [ -n "$DELIVERABLE" ] && [ -f "$DELIVERABLE" ]; then
    EVAL_TARGET="$DELIVERABLE"
    echo "[claude-dispatch] Evaluating deliverable: ${DELIVERABLE}"
  fi
fi

PRECHECK_PASS=1
PRECHECK_REASON=""

# Check: hard failure (non-zero exit, or output file missing)
if [ "$SPAWN_EXIT" -ne 0 ]; then
  PRECHECK_PASS=0
  PRECHECK_REASON="spawn exited with code ${SPAWN_EXIT}"
fi

if [ ! -f "$OUTPUT_FILE" ]; then
  PRECHECK_PASS=0
  PRECHECK_REASON="output file not found"
fi

if [ "$PRECHECK_PASS" -eq 1 ]; then
  OUTPUT_SIZE=$(wc -c < "$EVAL_TARGET" | tr -d ' ')
  if [ "$OUTPUT_SIZE" -lt 100 ]; then
    PRECHECK_PASS=0
    PRECHECK_REASON="output too short (${OUTPUT_SIZE} bytes, need >=100)"
  fi
fi

# Check: echoed prompt (first 200 chars of output match first 200 chars of prompt)
if [ "$PRECHECK_PASS" -eq 1 ]; then
  PROMPT_HEAD=$(head -c 200 "$PROMPT_FILE" | tr -d '\n')
  OUTPUT_HEAD=$(head -c 200 "$EVAL_TARGET" | tr -d '\n')
  if [ "$PROMPT_HEAD" = "$OUTPUT_HEAD" ] && [ -n "$PROMPT_HEAD" ]; then
    PRECHECK_PASS=0
    PRECHECK_REASON="output echoes the prompt"
  fi
fi

# Check: tool-call noise (output is mostly tool call artifacts)
if [ "$PRECHECK_PASS" -eq 1 ]; then
  TOOLCALL_LINES=$(grep -c '^\s*<tool_' "$EVAL_TARGET" 2>/dev/null || true)
  TOOLCALL_LINES="${TOOLCALL_LINES:-0}"
  TOOLCALL_LINES=$(printf '%s' "$TOOLCALL_LINES" | tr -dc '0-9')
  TOOLCALL_LINES="${TOOLCALL_LINES:-0}"
  TOTAL_LINES=$(wc -l < "$EVAL_TARGET" | tr -dc '0-9')
  TOTAL_LINES="${TOTAL_LINES:-0}"
  if [ "$TOTAL_LINES" -gt 0 ] && [ "$TOOLCALL_LINES" -gt 0 ]; then
    RATIO=$((TOOLCALL_LINES * 100 / TOTAL_LINES))
    if [ "$RATIO" -gt 60 ]; then
      PRECHECK_PASS=0
      PRECHECK_REASON="output is mostly tool-call artifacts (${RATIO}%)"
    fi
  fi
fi

# --- Hard fallback check ---
FALLBACK_TRIGGERED=0
FALLBACK_STATUS=""
FALLBACK_SCORE=0
FALLBACK_RUNTIME=0

if [ "$PRECHECK_PASS" -eq 0 ] && [ "$SPAWN_EXIT" -ne 0 ]; then
  echo "[claude-dispatch] Hard failure detected (${PRECHECK_REASON}). Triggering kiro-cli fallback..."
  FALLBACK_TRIGGERED=1

  FB_START=$(date +%s)
  SPAWN_BACKEND=kiro-cli bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" \
    "${AGENT_ID}-fallback" "$OUTPUT_FILE" \
    "${BACKEND_ARGS[@]}" --prompt-file "$PROMPT_FILE" || true
  FB_END=$(date +%s)
  FALLBACK_RUNTIME=$((FB_END - FB_START))

  # Re-check output after fallback
  if [ -f "$OUTPUT_FILE" ]; then
    FB_SIZE=$(wc -c < "$OUTPUT_FILE" | tr -d ' ')
    if [ "$FB_SIZE" -ge 100 ]; then
      PRECHECK_PASS=1
      PRECHECK_REASON=""
    fi
  fi
fi

# --- Step 4: Run evaluation ---
EVAL_SCORE=0
EVAL_PASS=0
EVAL_REVISION_PROMPT=""

if [ "$PRECHECK_PASS" -eq 1 ]; then
  echo "[claude-dispatch] Running evaluation..."

  EVAL_OUTPUT=$("$RA_PYTHON" "${SCRIPTS_DIR}/run_eval.py" \
    --content-path "$EVAL_TARGET" \
    --query "$TASK_NAME" \
    --contract-file "$CONTRACT_FILE" \
    --workflow-name "$WORKFLOW_NAME" 2>/dev/null) || true

  if [ -n "$EVAL_OUTPUT" ]; then
    EVAL_PASS=$(printf '%s' "$EVAL_OUTPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(1 if d.get('overall_pass') else 0)" 2>/dev/null || echo "0")
    EVAL_SCORE=$(printf '%s' "$EVAL_OUTPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('analyst_score',0))" 2>/dev/null || echo "0")
    EVAL_REVISION_PROMPT=$(printf '%s' "$EVAL_OUTPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('revision_prompt',''))" 2>/dev/null || echo "")
  fi
else
  echo "[claude-dispatch] Pre-check failed (${PRECHECK_REASON}). Score=0, skipping LLM eval."
  EVAL_SCORE=0
  EVAL_PASS=0
fi

# --- Step 5: Retry logic (one retry if eval fails) ---
RETRY_COUNT=0
FINAL_STATUS="pass"

if [ "$PRECHECK_PASS" -eq 1 ] && [ "$EVAL_PASS" -eq 0 ] && [ -n "$EVAL_REVISION_PROMPT" ]; then
  echo "[claude-dispatch] Evaluation failed (score=${EVAL_SCORE}). Retrying with feedback..."
  RETRY_COUNT=1

  # Build revision prompt
  REVISION_FILE="/tmp/claude-dispatch-${AGENT_ID}-revision.md"
  {
    cat "$ENRICHED_PROMPT_FILE"
    printf '\n\n## REVISION REQUIRED\n\nYour previous attempt scored %s and failed evaluation.\n\n%s\n\nPlease revise your output addressing the feedback above.\n' \
      "$EVAL_SCORE" "$EVAL_REVISION_PROMPT"
  } > "$REVISION_FILE"

  # Clear old sentinel
  rm -f "${WORKSPACE_ROOT}/.kiro/.gpu-agent-done/${AGENT_ID}.done"

  RETRY_START=$(date +%s)
  bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "${AGENT_ID}" "$OUTPUT_FILE" \
    "${BACKEND_ARGS[@]}" --prompt-file "$REVISION_FILE" || true
  RETRY_END=$(date +%s)
  RUNTIME=$((RUNTIME + RETRY_END - RETRY_START))

  # Re-evaluate
  if [ -f "$OUTPUT_FILE" ]; then
    RETRY_SIZE=$(wc -c < "$OUTPUT_FILE" | tr -d ' ')
    if [ "$RETRY_SIZE" -ge 100 ]; then
      EVAL_OUTPUT2=$("$RA_PYTHON" "${SCRIPTS_DIR}/run_eval.py" \
        --content-path "$EVAL_TARGET" \
        --query "$TASK_NAME" \
        --contract-file "$CONTRACT_FILE" \
        --workflow-name "$WORKFLOW_NAME" 2>/dev/null) || true
      if [ -n "$EVAL_OUTPUT2" ]; then
        EVAL_PASS=$(printf '%s' "$EVAL_OUTPUT2" | python3 -c "import sys,json; d=json.load(sys.stdin); print(1 if d.get('overall_pass') else 0)" 2>/dev/null || echo "0")
        EVAL_SCORE=$(printf '%s' "$EVAL_OUTPUT2" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('analyst_score',0))" 2>/dev/null || echo "0")
      fi
    fi
  fi

  rm -f "$REVISION_FILE"
fi

# --- Step 6: Determine final status ---
if [ "$PRECHECK_PASS" -eq 0 ] && [ "$FALLBACK_TRIGGERED" -eq 0 ]; then
  FINAL_STATUS="hard_fail"
elif [ "$EVAL_PASS" -eq 1 ]; then
  FINAL_STATUS="pass"
else
  FINAL_STATUS="fail"
fi

# --- Step 7: Escalation on double failure ---
if [ "$FINAL_STATUS" = "fail" ] && [ "$RETRY_COUNT" -gt 0 ]; then
  echo "[claude-dispatch] Retry also failed. Escalating to user."
  FINAL_STATUS="escalated"

  ESCALATION_DIR="${WORKSPACE_ROOT}/.kiro/.ingest-pending/${AGENT_ID}"
  mkdir -p "$ESCALATION_DIR"
  cat > "${ESCALATION_DIR}/escalation.md" <<ESCALATION_EOF
# Escalation: ${AGENT_ID}

**Task**: ${TASK_NAME}
**Workflow**: ${WORKFLOW_NAME}
**Status**: Failed after 1 retry
**Eval Score**: ${EVAL_SCORE}
**Runtime**: ${RUNTIME}s

## Output Location
${OUTPUT_FILE}

## Revision Feedback Given
${EVAL_REVISION_PROMPT}

## Action Required
Review the output and decide: proceed, revise manually, or kill.
ESCALATION_EOF
fi

# --- Step 8: Update sentinel with evaluation data ---
SENTINEL_FILE="${WORKSPACE_ROOT}/.kiro/.gpu-agent-done/${AGENT_ID}.done"
if [ -f "$SENTINEL_FILE" ]; then
  # Append eval data to sentinel JSON (replace closing brace). Also flip any
  # provisional "awaiting_eval" status left by the deferred inner spawn.
  SENTINEL_CONTENT=$(cat "$SENTINEL_FILE")
  UPDATED_SENTINEL=$(printf '%s' "$SENTINEL_CONTENT" | sed 's/}$//' | sed 's/"status": "awaiting_eval"/"status": "'"$FINAL_STATUS"'"/')
  FINAL_SENTINEL="$(printf '%s,\n  "evaluation_score": %s,\n  "eval_passed": %s,\n  "retry_count": %s,\n  "fallback_triggered": %s,\n  "final_status": "%s",\n  "runtime_sec": %s\n}\n' \
    "$UPDATED_SENTINEL" "$EVAL_SCORE" "$EVAL_PASS" "$RETRY_COUNT" \
    "$FALLBACK_TRIGGERED" "$FINAL_STATUS" "$RUNTIME")"
  if [ "$SENTINEL_V2" = "1" ] && command -v sentinel_write_atomic >/dev/null 2>&1; then
    sentinel_write_atomic "$SENTINEL_FILE" "$FINAL_SENTINEL"
    _cd_final_written=1
    trap - EXIT INT TERM
  else
    printf '%s' "$FINAL_SENTINEL" > "$SENTINEL_FILE"
  fi
fi

# --- Step 9: Log A/B comparison ---
FALLBACK_STATUS_ARG=""
if [ "$FALLBACK_TRIGGERED" -eq 1 ]; then
  if [ "$EVAL_PASS" -eq 1 ]; then
    FALLBACK_STATUS_ARG="pass"
  else
    FALLBACK_STATUS_ARG="fail"
  fi
fi

AB_ARGS=(
  --run-id "$AGENT_ID"
  --task-type "$WORKFLOW_NAME"
  --primary-backend "claude"
  --primary-status "$FINAL_STATUS"
  --primary-score "$EVAL_SCORE"
  --primary-runtime "$RUNTIME"
)

if [ "$FALLBACK_TRIGGERED" -eq 1 ]; then
  AB_ARGS+=(
    --fallback-triggered
    --fallback-backend "kiro-cli"
    --fallback-status "$FALLBACK_STATUS_ARG"
    --fallback-score "$FALLBACK_SCORE"
    --fallback-runtime "$FALLBACK_RUNTIME"
  )
fi

"$RA_PYTHON" "${SCRIPTS_DIR}/ab_log.py" "${AB_ARGS[@]}" 2>/dev/null || true

# --- Cleanup temp files ---
rm -f "$ENRICHED_PROMPT_FILE"
rm -f "$CONTRACT_FILE"

# --- Summary ---
echo "[claude-dispatch] === DISPATCH COMPLETE ==="
echo "[claude-dispatch]   Agent: ${AGENT_ID}"
echo "[claude-dispatch]   Status: ${FINAL_STATUS}"
echo "[claude-dispatch]   Eval Score: ${EVAL_SCORE}"
echo "[claude-dispatch]   Retry Count: ${RETRY_COUNT}"
echo "[claude-dispatch]   Fallback: ${FALLBACK_TRIGGERED}"
echo "[claude-dispatch]   Runtime: ${RUNTIME}s"
