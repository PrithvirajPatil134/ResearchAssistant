#!/usr/bin/env bash
# long-doc-orchestrate.sh — Coordinates the full long document production pipeline.
# Dispatches agents in sequence with eval gates between phases.
#
# macOS bash 3.2 compatible (no mapfile, no associative arrays).
#
# Usage:
#   bash scripts/long-doc-orchestrate.sh <doc-id> <space> <doc-type> <prompt-file> [options]
#
# Options:
#   --mode parallel|sequential|both   (default: both for first 5 runs, then learned)
#   --pause-after outline|sections|stitch
#   --resume-from outline|sections|stitch|eval
#   --simulate-reviewers name1,name2
#   --venue "Journal Name"
#   --no-abstract          Skip abstract writer phase
#   --no-benchmark         Skip benchmark comparison phase
#   --no-learner           Skip writing team learner phase
#
# Phases:
#   1. Brain Assembly (ra-brain-assembler)
#   2. Outline Eval (heuristic gate)
#   3. Section Dispatch (parallel or sequential)
#   4. Pre-Stitch Eval (heuristic fast-filter + ra-pre-stitch-eval agent)
#   5. Stitch (ra-doc-stitcher, concatenation fallback on failure)
#   5.5. Abstract Writer (ra-abstract-writer)
#   6. Post-Stitch Eval (ra-post-stitch-eval devil's advocate gate)
#   6.5. Benchmark Comparison (ra-benchmark-comparator)
#   7. Deliver
#   7.5. Writing Team Learner (ra-writing-learner, fire-and-forget)

set -o pipefail

# --- Model for dispatched agents ---
# 1M-context model so section writers / evaluators never fall back to 200k and
# fail with "Prompt is too long". Bare id must be in ~/.claude/settings.json
# availableModels (enforceAvailableModels: true). Override via RA_AGENT_MODEL.
RA_AGENT_MODEL="${RA_AGENT_MODEL:-claude-opus-4-8[1m]}"

# --- Parse required positional arguments ---
DOC_ID="${1:?Usage: long-doc-orchestrate.sh <doc-id> <space> <doc-type> <prompt-file> [options]}"
SPACE="${2:?Usage: long-doc-orchestrate.sh <doc-id> <space> <doc-type> <prompt-file> [options]}"
DOC_TYPE="${3:?Usage: long-doc-orchestrate.sh <doc-id> <space> <doc-type> <prompt-file> [options]}"
PROMPT_FILE="${4:?Usage: long-doc-orchestrate.sh <doc-id> <space> <doc-type> <prompt-file> [options]}"
shift 4

# --- Resolve workspace root ---
WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="${WORKSPACE_ROOT}/scripts"
SENTINEL_DIR="${WORKSPACE_ROOT}/.kiro/.gpu-agent-done"
LONG_DOC_DIR="${WORKSPACE_ROOT}/.kiro/.long-doc/${DOC_ID}"
LEARNER_DIR="${WORKSPACE_ROOT}/data/wiki/shared/learner/writing-team"

# --- Parse options ---
MODE=""
PAUSE_AFTER=""
RESUME_FROM=""
SIMULATE_REVIEWERS=""
VENUE=""
SKIP_ABSTRACT=0
SKIP_BENCHMARK=0
SKIP_LEARNER=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --mode)
      shift; MODE="${1:?--mode requires a value (parallel|sequential|both)}"
      ;;
    --pause-after)
      shift; PAUSE_AFTER="${1:?--pause-after requires a value (outline|sections|stitch)}"
      ;;
    --resume-from)
      shift; RESUME_FROM="${1:?--resume-from requires a value (outline|sections|stitch|eval)}"
      ;;
    --simulate-reviewers)
      shift; SIMULATE_REVIEWERS="${1:?--simulate-reviewers requires comma-separated names}"
      ;;
    --venue)
      shift; VENUE="${1:?--venue requires a journal name}"
      ;;
    --no-abstract)
      SKIP_ABSTRACT=1
      ;;
    --no-benchmark)
      SKIP_BENCHMARK=1
      ;;
    --no-learner)
      SKIP_LEARNER=1
      ;;
    *)
      echo "error: unknown option '$1'" >&2
      exit 2
      ;;
  esac
  shift
done

# --- Determine mode if not specified ---
if [ -z "$MODE" ]; then
  # STEP 1: Check document word budget from prompt file.
  # If the prompt specifies a target word count, use it to select mode.
  # This prevents routing short papers (2600 words) to parallel/sequential splitting.
  WORD_BUDGET=0
  if [ -f "$PROMPT_FILE" ]; then
    # Look for patterns like "~2,600 words", "approximately 5000 words", "2600 words total"
    WORD_BUDGET=$(grep -oiE '~?[0-9,]+\s*words\s*(total|excluding)?' "$PROMPT_FILE" | head -1 | \
      grep -oE '[0-9,]+' | head -1 | tr -d ',' || echo "0")
    WORD_BUDGET="${WORD_BUDGET:-0}"
    # If no explicit total found, try summing section word targets like "(~350 words)"
    if [ "$WORD_BUDGET" -eq 0 ] 2>/dev/null; then
      WORD_BUDGET=$(grep -oE '~[0-9]+\s*words' "$PROMPT_FILE" | grep -oE '[0-9]+' | \
        python3 -c "import sys; print(sum(int(l) for l in sys.stdin))" 2>/dev/null || echo "0")
      WORD_BUDGET="${WORD_BUDGET:-0}"
    fi
  fi

  if [ "$WORD_BUDGET" -gt 0 ] && [ "$WORD_BUDGET" -lt 2000 ]; then
    MODE="single-raw"
    log "Mode auto-selected: single-raw (word budget=${WORD_BUDGET}, <2000)"
  elif [ "$WORD_BUDGET" -ge 2000 ] && [ "$WORD_BUDGET" -le 8000 ]; then
    MODE="single-brain"
    log "Mode auto-selected: single-brain (word budget=${WORD_BUDGET}, 2000-8000)"
  else
    # STEP 2: For long documents (>8000 or unknown), use learning-based selection.
    MODE_LOG="${LEARNER_DIR}/mode_comparison.jsonl"
    if [ -f "$MODE_LOG" ]; then
      RUN_COUNT=$(wc -l < "$MODE_LOG" | tr -d ' ')
    else
      RUN_COUNT=0
    fi
    if [ "$RUN_COUNT" -lt 10 ]; then
      MODE="both"
    else
      PARALLEL_AVG=$(grep '"mode":"parallel"' "$MODE_LOG" 2>/dev/null | tail -5 | \
        python3 -c "import sys,json; lines=[json.loads(l) for l in sys.stdin]; print(sum(d.get('score',0) for d in lines)/max(len(lines),1))" 2>/dev/null || echo "0")
      SEQUENTIAL_AVG=$(grep '"mode":"sequential"' "$MODE_LOG" 2>/dev/null | tail -5 | \
        python3 -c "import sys,json; lines=[json.loads(l) for l in sys.stdin]; print(sum(d.get('score',0) for d in lines)/max(len(lines),1))" 2>/dev/null || echo "0")
      if python3 -c "exit(0 if float('${PARALLEL_AVG}') >= float('${SEQUENTIAL_AVG}') else 1)" 2>/dev/null; then
        MODE="parallel"
      else
        MODE="sequential"
      fi
      log "Mode auto-selected: ${MODE} (parallel_avg=${PARALLEL_AVG}, sequential_avg=${SEQUENTIAL_AVG})"
    fi
  fi
fi

# --- Constants ---
AGENT_TIMEOUT=900        # 15 minutes per agent (default: stitcher, evaluators)
AGENT_TIMEOUT_LONG=1200  # 20 minutes for heavy agents (brain assembler, section writers)
AGENT_TIMEOUT_SHORT=300  # 5 minutes for lightweight agents (abstract writer)
POLL_INTERVAL=30         # seconds between sentinel checks
BRAIN_FILES="voice.md argument-map.md terminology.md methodology-context.md advisor-guidance.md literature-map.md constraints.md exhibits-plan.md outline.md"

# --- Utilities ---

log() {
  local msg="[long-doc $(date +%H:%M:%S)] $1"
  echo "$msg"
  echo "$msg" >> "${LONG_DOC_DIR}/orchestration.log" 2>/dev/null || true
}

# Step-level JSONL trace for determinism verification
TRACE_DIR="${WORKSPACE_ROOT}/data/logs/traces"
mkdir -p "$TRACE_DIR"
LONGDOC_TRACE_FILE="${TRACE_DIR}/longdoc-$(date +%Y-%m-%d).jsonl"

trace_step() {
  local phase="$1"
  local step_name="$2"
  local duration_ms="$3"
  local status="$4"
  printf '{"timestamp":"%s","doc_id":"%s","space":"%s","mode":"%s","phase":"%s","step":"%s","duration_ms":%d,"status":"%s"}\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$DOC_ID" "$SPACE" "$MODE" "$phase" "$step_name" "$duration_ms" "$status" \
    >> "$LONGDOC_TRACE_FILE"
}

wait_for_sentinel() {
  local agent_id="$1"
  local timeout="${2:-$AGENT_TIMEOUT}"
  local sentinel_path="${SENTINEL_DIR}/${agent_id}.done"
  local elapsed=0
  local step_start
  step_start=$(date +%s)

  while [ ! -f "$sentinel_path" ]; do
    if [ "$elapsed" -ge "$timeout" ]; then
      log "TIMEOUT: agent ${agent_id} exceeded ${timeout}s"
      local step_dur=$(( ($(date +%s) - step_start) * 1000 ))
      trace_step "wait" "$agent_id" "$step_dur" "timeout"
      return 1
    fi
    sleep "$POLL_INTERVAL"
    elapsed=$((elapsed + POLL_INTERVAL))
  done

  local exit_code
  exit_code=$(python3 -c "import json; print(json.load(open('${sentinel_path}')).get('exit_code', 1))" 2>/dev/null || echo "1")
  local step_dur=$(( ($(date +%s) - step_start) * 1000 ))
  if [ "$exit_code" -ne 0 ]; then
    log "FAILURE: agent ${agent_id} exited with code ${exit_code}"
    trace_step "wait" "$agent_id" "$step_dur" "failed"
    return 1
  fi
  trace_step "wait" "$agent_id" "$step_dur" "success"
  return 0
}

clear_sentinel() {
  local agent_id="$1"
  rm -f "${SENTINEL_DIR}/${agent_id}.done"
}

write_state() {
  local phase="$1"
  cat > "${LONG_DOC_DIR}/state.json" <<EOF
{
  "doc_id": "${DOC_ID}",
  "space": "${SPACE}",
  "doc_type": "${DOC_TYPE}",
  "mode": "${MODE}",
  "paused_after": "${phase}",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
}

count_sections() {
  local outline="$1"
  grep -c '^## ' "$outline" 2>/dev/null || echo "0"
}

extract_section_titles() {
  local outline="$1"
  # Skip References/Bibliography sections (compiled mechanically, not written by section agents)
  grep '^## ' "$outline" 2>/dev/null | sed 's/^## //' | grep -viE '(references|bibliography|works cited|reference list)'
}

# --- Setup working directory ---
if [ "$RESUME_FROM" = "" ]; then
  mkdir -p "${LONG_DOC_DIR}/brain"
  mkdir -p "${LONG_DOC_DIR}/sections"
  mkdir -p "${LONG_DOC_DIR}/exhibits"
  mkdir -p "${LONG_DOC_DIR}/eval"
  mkdir -p "${LONG_DOC_DIR}/prompts"
  touch "${LONG_DOC_DIR}/orchestration.log"
  log "Starting long document production: doc_id=${DOC_ID}, space=${SPACE}, type=${DOC_TYPE}, mode=${MODE}"
else
  if [ ! -d "$LONG_DOC_DIR" ]; then
    echo "error: cannot resume — working directory not found: ${LONG_DOC_DIR}" >&2
    exit 1
  fi
  log "Resuming from phase: ${RESUME_FROM}"
fi

# --- Validate prompt file ---
if [ ! -f "$PROMPT_FILE" ]; then
  echo "error: prompt file not found: ${PROMPT_FILE}" >&2
  exit 2
fi

# ============================================================================
# PHASE 1: BRAIN ASSEMBLY
# ============================================================================

run_brain_assembly() {
  log "PHASE 1: Brain Assembly"

  local brain_agent_id="longdoc-${DOC_ID}-brain"
  local brain_output="/tmp/${brain_agent_id}.out"
  local brain_prompt="${LONG_DOC_DIR}/prompts/brain_prompt.md"

  cat > "$brain_prompt" <<BRAIN_EOF
# Brain Assembly Task

You are the brain assembler for a long document production pipeline.

## Document Request
$(cat "$PROMPT_FILE")

## Document Metadata
- Doc ID: ${DOC_ID}
- Space: ${SPACE}
- Document Type: ${DOC_TYPE}
$([ -n "$VENUE" ] && echo "- Target Venue: ${VENUE}")
$([ -n "$SIMULATE_REVIEWERS" ] && echo "- Simulate Reviewers: ${SIMULATE_REVIEWERS}")

## Your Task

Read the wiki knowledge base at src/research_assistant/spaces/${SPACE}/wiki/ and data/wiki/shared/ to assemble a brain package.

Write the following files to .kiro/.long-doc/${DOC_ID}/brain/:

1. **voice.md** — Tone, person, rhythm, formality (3-4 sentences)
2. **argument-map.md** — Thesis → evidence chains → conclusion (logical flow)
3. **terminology.md** — Canonical terms extracted from wiki concept pages (lookup table)
4. **methodology-context.md** — Research design, paradigm, method choices and WHY
5. **advisor-guidance.md** — Relevant feedback from advisors (sourced from wiki entities)
6. **literature-map.md** — Which papers say what, how they relate, where gaps are
7. **constraints.md** — Word targets per section, citation style, formatting rules
8. **exhibits-plan.md** — Tables and figures: content source, target section, format
9. **outline.md** — Section structure with argument per section + source assignments

## Outline Format Requirements

The outline.md must use this format for each section:

\`\`\`
## Section Title
- Word target: N words
- Argument: one sentence stating what this section argues
- Sources: wiki/sources/page1.md, wiki/sources/page2.md
\`\`\`

Total word targets should sum to a range appropriate for the document type:
- Research paper: 8000-12000 words
- Literature review: 10000-15000 words
- Thesis chapter: 8000-12000 words

## Rules

- Every claim in the brain package must cite a wiki source page or raw knowledge file.
- The terminology table must extract canonical terms from wiki concept pages (title field = canonical term).
- Source assignments in the outline must reference actual wiki pages that exist.
- Read ${LEARNER_DIR}/outline_patterns.md for learned patterns about good outlines.
BRAIN_EOF

  clear_sentinel "$brain_agent_id"

  log "Dispatching ra-brain-assembler..."
  bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$brain_agent_id" "$brain_output" \
    --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
    --prompt-file "$brain_prompt" &

  if ! wait_for_sentinel "$brain_agent_id" "$AGENT_TIMEOUT_LONG"; then
    log "Brain assembly failed."
    return 1
  fi

  local missing_files=""
  for f in $BRAIN_FILES; do
    if [ ! -f "${LONG_DOC_DIR}/brain/${f}" ]; then
      missing_files="${missing_files} ${f}"
    fi
  done

  if [ -n "$missing_files" ]; then
    log "Brain assembly incomplete. Missing:${missing_files}"
    return 1
  fi

  log "Brain assembly complete. All 9 files present."
  return 0
}

# ============================================================================
# PHASE 2: OUTLINE EVAL
# ============================================================================

run_outline_eval() {
  log "PHASE 2: Outline Eval"

  local outline="${LONG_DOC_DIR}/brain/outline.md"
  local issues=""
  local pass=1

  if [ ! -f "$outline" ]; then
    log "OUTLINE EVAL FAIL: outline.md not found"
    return 1
  fi

  # Check: has section headings
  local section_count
  section_count=$(grep -c '^## ' "$outline" 2>/dev/null || echo "0")
  if [ "$section_count" -lt 3 ]; then
    issues="${issues}Too few sections (${section_count}, need >=3). "
    pass=0
  fi

  # Check: has word targets
  local target_count
  target_count=$(grep -ci 'word target\|target.*[0-9]' "$outline" 2>/dev/null || echo "0")
  local min_targets=$((section_count * 3 / 4))
  if [ "$min_targets" -lt 1 ]; then min_targets=1; fi
  if [ "$target_count" -lt "$min_targets" ]; then
    issues="${issues}Missing word targets in some sections (found ${target_count}, need at least ${min_targets} for ${section_count} sections). "
    pass=0
  fi

  # Check: has source assignments (at least 50% of sections should have sources;
  # procedural sections like "Environment Verification" may not need wiki sources)
  # Count any file reference pattern: wiki/, sources/, knowledge/, docs/, scripts/, .kiro/, .md, .sh, .py
  local source_refs
  source_refs=$(grep -c 'wiki/\|sources/\|knowledge/\|docs/\|scripts/\|\.kiro/\|\.md\|\.sh\|\.py' "$outline" 2>/dev/null || echo "0")
  local min_sources=$((section_count / 2))
  if [ "$min_sources" -lt 1 ]; then min_sources=1; fi
  if [ "$source_refs" -lt "$min_sources" ]; then
    issues="${issues}Too few source assignments (${source_refs} refs for ${section_count} sections, need at least ${min_sources}). "
    pass=0
  fi

  # Check: total word target in reasonable range (mode-aware floor)
  local total_words
  total_words=$(grep -oi '[0-9]\+ words\|[0-9]\+words' "$outline" 2>/dev/null | \
    grep -o '[0-9]\+' | python3 -c "import sys; print(sum(int(l) for l in sys.stdin))" 2>/dev/null || echo "0")
  local word_floor=2000
  if [ "$MODE" = "single-raw" ]; then word_floor=400; fi
  if [ "$total_words" -lt "$word_floor" ] || [ "$total_words" -gt 25000 ]; then
    issues="${issues}Total word target (${total_words}) outside ${word_floor}-25000 range. "
    pass=0
  fi

  # Check: advisor-mandated items appear in outline OR exhibits-plan
  local advisor_file="${LONG_DOC_DIR}/brain/advisor-guidance.md"
  local exhibits_file="${LONG_DOC_DIR}/brain/exhibits-plan.md"
  if [ -f "$advisor_file" ] && [ "$pass" -eq 1 ]; then
    # Extract mandatory/high-priority items from advisor guidance
    local advisor_items
    advisor_items=$(grep -iE '(add|include|must|required|gap table|market evidence)' "$advisor_file" 2>/dev/null | \
      grep -ivE '^\s*#\|^\s*$\|source:\|^\[' | head -10)
    if [ -n "$advisor_items" ]; then
      local outline_lower
      outline_lower=$(tr '[:upper:]' '[:lower:]' < "$outline")
      # Also check exhibits-plan for items that belong there
      local exhibits_lower=""
      if [ -f "$exhibits_file" ]; then
        exhibits_lower=$(tr '[:upper:]' '[:lower:]' < "$exhibits_file")
      fi
      local combined_lower="${outline_lower} ${exhibits_lower}"
      local missing_items=""
      # Check for specific high-signal advisor requests that are STRUCTURAL (tables, exhibits)
      # Content items (market evidence, specific citations) are checked by post-stitch eval, not outline eval
      if echo "$advisor_items" | grep -qi "gap table" && ! echo "$combined_lower" | grep -qi "gap table\|gap.table\|han et al\|comparison table\|literature comparison"; then
        missing_items="${missing_items}Gap table (advisor-mandated) not assigned to any section. "
      fi
      if [ -n "$missing_items" ]; then
        issues="${issues}${missing_items}"
        pass=0
      fi
    fi
  fi

  # Write eval result
  cat > "${LONG_DOC_DIR}/eval/outline_eval.json" <<EOF
{
  "pass": $([ "$pass" -eq 1 ] && echo "true" || echo "false"),
  "section_count": ${section_count},
  "source_refs": ${source_refs},
  "total_word_target": ${total_words},
  "issues": "$(printf '%s' "$issues" | sed 's/"/\\"/g')",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

  if [ "$pass" -eq 1 ]; then
    log "Outline eval PASSED: ${section_count} sections, ${total_words} words targeted, ${source_refs} source refs."
    return 0
  else
    log "Outline eval FAILED: ${issues}"
    return 1
  fi
}

# ============================================================================
# PHASE 3: SECTION DISPATCH
# ============================================================================

dispatch_sections() {
  local run_mode="$1"
  local suffix="${2:-}"

  local outline="${LONG_DOC_DIR}/brain/outline.md"
  local section_count
  section_count=$(extract_section_titles "$outline" | wc -l | tr -d ' ')

  log "PHASE 3: Section Dispatch (mode=${run_mode}, sections=${section_count}${suffix:+, suffix=${suffix}})"

  local output_dir="${LONG_DOC_DIR}/sections"
  if [ -n "$suffix" ]; then
    output_dir="${LONG_DOC_DIR}/sections-${suffix}"
    mkdir -p "$output_dir"
  fi

  # Extract section info and build prompts
  local i=1
  local prev_section_file=""
  local section_titles=""

  while IFS= read -r title; do
    [ -z "$title" ] && continue

    # Skip References/Bibliography sections — these are compiled mechanically, not written
    if echo "$title" | grep -qiE '(references|bibliography|works cited|reference list)'; then
      log "  Skipping section ${i}: ${title} (compiled mechanically after stitching)"
      i=$((i + 1))
      continue
    fi

    local agent_id="longdoc-${DOC_ID}${suffix:+-${suffix}}-section-${i}"
    local section_output="/tmp/${agent_id}.out"
    local section_prompt="${LONG_DOC_DIR}/prompts/section_${i}${suffix:+_${suffix}}_prompt.md"

    # Extract section-specific info from outline
    local word_target
    word_target=$(sed -n "/^## ${title}/,/^## /{ /[Ww]ord/p; }" "$outline" 2>/dev/null | \
      grep -oi '[0-9]\+' | head -1 || echo "1500")
    [ -z "$word_target" ] && word_target="1500"

    local sources_line
    sources_line=$(sed -n "/^## ${title}/,/^## /{ /[Ss]ource/p; }" "$outline" 2>/dev/null | head -1 || echo "")

    cat > "$section_prompt" <<SECTION_EOF
# Section Writing Task

You are a section writer for a long document production pipeline.

## Brain Package Location
Read ALL files in: .kiro/.long-doc/${DOC_ID}/brain/
These define your voice, argument structure, terminology, and constraints.

## Your Section
- Section number: ${i} of ${section_count}
- Title: ${title}
- Word target: ${word_target} words
- Sources to draw from: ${sources_line}

## Output
Write ONLY your section content (with the section heading) to:
.kiro/.long-doc/${DOC_ID}/${output_dir##*/}/section_${i}.md

## Rules
- Follow the voice defined in brain/voice.md exactly
- Use only canonical terms from brain/terminology.md
- Cite sources with [wiki/sources/author-year.md, Section/Page] format
- Stay within +/- 20% of word target
- Do not write content for other sections
- Read ${LEARNER_DIR}/section_patterns.md for learned patterns
- **CRITICAL: Read brain/constraints.md. Check the "Hard Requirements" section. If ANY requirement is assigned to YOUR section (by section number or title), you MUST produce that deliverable. A missing hard requirement is a pipeline failure. Produce required deliverables FIRST, then fill in the remaining content.**
SECTION_EOF

    # Sequential mode: add previous section context
    if [ "$run_mode" = "sequential" ] && [ -n "$prev_section_file" ] && [ -f "$prev_section_file" ]; then
      {
        echo ""
        echo "## Previous Section (last 200 words for continuity)"
        echo ""
        tail -c 1200 "$prev_section_file" | tail -200c
      } >> "$section_prompt"
    fi

    clear_sentinel "$agent_id"

    if [ "$run_mode" = "parallel" ]; then
      log "  Dispatching section ${i}: ${title} (parallel)"
      bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$agent_id" "$section_output" \
        --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
        --prompt-file "$section_prompt" &

      # 10-second stagger between parallel dispatches
      if [ "$i" -lt "$section_count" ]; then
        sleep 10
      fi
    else
      log "  Dispatching section ${i}: ${title} (sequential)"
      bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$agent_id" "$section_output" \
        --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
        --prompt-file "$section_prompt" &

      if ! wait_for_sentinel "$agent_id" "$AGENT_TIMEOUT_LONG"; then
        log "  Section ${i} FAILED."
        return 1
      fi
      log "  Section ${i} complete."
      prev_section_file="${output_dir}/section_${i}.md"
    fi

    section_titles="${section_titles}${title}
"
    i=$((i + 1))
  done <<< "$(extract_section_titles "$outline")"

  # For parallel mode: wait for all sentinels
  if [ "$run_mode" = "parallel" ]; then
    log "  Waiting for all ${section_count} parallel sections..."
    local all_done=1
    i=1
    while [ "$i" -le "$section_count" ]; do
      local agent_id="longdoc-${DOC_ID}${suffix:+-${suffix}}-section-${i}"
      if ! wait_for_sentinel "$agent_id" "$AGENT_TIMEOUT_LONG"; then
        log "  Section ${i} FAILED (parallel)."
        all_done=0
      fi
      i=$((i + 1))
    done
    if [ "$all_done" -eq 0 ]; then
      return 1
    fi
  fi

  log "All ${section_count} sections dispatched and completed (${run_mode})."
  return 0
}

# ============================================================================
# PHASE 4: PRE-STITCH EVAL
# ============================================================================

run_pre_stitch_eval() {
  local sections_dir="${1:-${LONG_DOC_DIR}/sections}"

  log "PHASE 4: Pre-Stitch Eval (dir=${sections_dir})"

  local outline="${LONG_DOC_DIR}/brain/outline.md"
  local section_count
  section_count=$(grep -c '^## ' "$outline" 2>/dev/null || echo "0")

  local pass=1
  local issues=""
  local i=1

  # --- Heuristic fast-filter (runs in <1 second) ---
  local banned_words="delve tapestry nuanced landscape multifaceted leverage utilize streamline foster facilitate harness robust seamless scalable comprehensive pivotal groundbreaking transformative revolutionary game-changing cutting-edge remarkable crucial significant aforementioned underscores underpin elucidate myriad plethora paradigm"

  while [ "$i" -le "$section_count" ]; do
    local section_file="${sections_dir}/section_${i}.md"

    if [ ! -f "$section_file" ]; then
      issues="${issues}Section ${i}: file missing. "
      pass=0
      i=$((i + 1))
      continue
    fi

    local word_count
    word_count=$(wc -w < "$section_file" | tr -d ' ')

    local word_target
    word_target=$(sed -n "/^## /{n;}" "$outline" 2>/dev/null | sed -n "${i}p" | \
      grep -oi '[0-9]\+' | head -1 || echo "")
    if [ -z "$word_target" ] || [ "$word_target" -eq 0 ] 2>/dev/null; then
      # Derive from total word budget / section count (from constraints.md or WORD_BUDGET)
      if [ "$WORD_BUDGET" -gt 0 ] 2>/dev/null && [ "$section_count" -gt 0 ]; then
        word_target=$((WORD_BUDGET / section_count))
      else
        word_target="1500"
      fi
    fi

    local low_bound=$((word_target * 80 / 100))
    local high_bound=$((word_target * 120 / 100))

    if [ "$word_count" -lt "$low_bound" ] || [ "$word_count" -gt "$high_bound" ]; then
      issues="${issues}Section ${i}: word count ${word_count} outside target range ${low_bound}-${high_bound}. "
    fi

    local citation_count
    citation_count=$(grep -c '\[' "$section_file" 2>/dev/null || echo "0")
    if [ "$citation_count" -lt 1 ]; then
      issues="${issues}Section ${i}: no citations found. "
      pass=0
    fi

    for word in $banned_words; do
      if grep -qi "\b${word}\b" "$section_file" 2>/dev/null; then
        issues="${issues}Section ${i}: banned word '${word}'. "
        pass=0
        break
      fi
    done

    i=$((i + 1))
  done

  # If heuristic fast-filter fails, skip the agent (save time)
  if [ "$pass" -eq 0 ]; then
    cat > "${LONG_DOC_DIR}/eval/pre_stitch_eval.json" <<EOF
{
  "verdict": "fail",
  "source": "heuristic",
  "sections_dir": "${sections_dir}",
  "issues": "$(printf '%s' "$issues" | sed 's/"/\\"/g')",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
    log "Pre-stitch eval FAILED (heuristic fast-filter): ${issues}"
    return 1
  fi

  log "Heuristic fast-filter passed. Dispatching ra-pre-stitch-eval agent for deeper analysis..."

  # --- Agent dispatch for deeper eval ---
  local pre_eval_agent_id="longdoc-${DOC_ID}-pre-stitch-eval"
  local pre_eval_output="/tmp/${pre_eval_agent_id}.out"
  local pre_eval_prompt="${LONG_DOC_DIR}/prompts/pre_stitch_eval_prompt.md"

  cat > "$pre_eval_prompt" <<PRE_EVAL_EOF
# Pre-Stitch Evaluation Task

You are the pre-stitch evaluator for a long document production pipeline.

## Sections Directory
Read all section files in: ${sections_dir}/

## Brain Package
Read ALL files in: .kiro/.long-doc/${DOC_ID}/brain/
Pay special attention to: terminology.md, outline.md, constraints.md

## Writing Standards
Read: .kiro/steering/human-authored-writing.md

## Your Task

Evaluate all section files BEFORE stitching. Check for:
1. Terminology drift (non-canonical terms)
2. Citation coverage (analytical sections need citations)
3. Word target adherence
4. Argument continuity (does each section argue what outline.md says it should?)
5. Writing standard violations (banned vocabulary, phrases, openers, em dashes)
6. Contradictions between sections

## Output

Write your evaluation to: .kiro/.long-doc/${DOC_ID}/eval/pre_stitch_eval.json

Use the format specified in your agent spec:
- "verdict": "pass" or "fail"
- "sections_checked": N
- "flags": [...] (each with section, check, severity, detail)
- "summary": { total_flags, total_warns, sections_needing_rewrite, rewrite_feedback }

Pass = zero flags. Warns are informational only.
PRE_EVAL_EOF

  clear_sentinel "$pre_eval_agent_id"

  bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$pre_eval_agent_id" "$pre_eval_output" \
    --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
    --prompt-file "$pre_eval_prompt" &

  if ! wait_for_sentinel "$pre_eval_agent_id"; then
    log "Pre-stitch eval agent failed. Using heuristic result (pass with warnings)."
    cat > "${LONG_DOC_DIR}/eval/pre_stitch_eval.json" <<EOF
{
  "verdict": "pass",
  "source": "heuristic_fallback",
  "sections_dir": "${sections_dir}",
  "issues": "$(printf '%s' "$issues" | sed 's/"/\\"/g')",
  "note": "Agent dispatch failed; heuristic fast-filter passed.",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
    if [ -n "$issues" ]; then
      log "Pre-stitch eval PASSED with heuristic warnings (agent unavailable): ${issues}"
    else
      log "Pre-stitch eval PASSED (heuristic only, agent unavailable)."
    fi
    return 0
  fi

  # Read the agent's verdict
  local agent_verdict=""
  if [ -f "${LONG_DOC_DIR}/eval/pre_stitch_eval.json" ]; then
    agent_verdict=$(python3 -c "import json; print(json.load(open('${LONG_DOC_DIR}/eval/pre_stitch_eval.json')).get('verdict', 'unknown'))" 2>/dev/null || echo "unknown")
  fi

  if [ "$agent_verdict" = "pass" ]; then
    log "Pre-stitch eval PASSED (agent-verified)."
    return 0
  elif [ "$agent_verdict" = "fail" ]; then
    local agent_flags
    agent_flags=$(python3 -c "import json; d=json.load(open('${LONG_DOC_DIR}/eval/pre_stitch_eval.json')); print(d.get('summary',{}).get('total_flags',0))" 2>/dev/null || echo "?")
    log "Pre-stitch eval FAILED (agent found ${agent_flags} flags)."
    return 1
  else
    log "Pre-stitch eval agent produced unreadable verdict. Treating as pass (heuristics passed)."
    return 0
  fi
}

# ============================================================================
# PHASE 5: STITCH
# ============================================================================

run_stitch() {
  local sections_dir="${1:-${LONG_DOC_DIR}/sections}"
  local output_file="${LONG_DOC_DIR}/assembled.md"

  log "PHASE 5: Stitch (ra-doc-stitcher)"

  local stitch_agent_id="longdoc-${DOC_ID}-stitcher"
  local stitch_output="/tmp/${stitch_agent_id}.out"
  local stitch_prompt="${LONG_DOC_DIR}/prompts/stitch_prompt.md"

  # Calculate total word count
  local total_words=0
  for section_file in "${sections_dir}"/section_*.md; do
    [ -f "$section_file" ] || continue
    local wc_val
    wc_val=$(wc -w < "$section_file" | tr -d ' ')
    total_words=$((total_words + wc_val))
  done

  local stitching_patterns_path="${LEARNER_DIR}/stitching_patterns.md"

  cat > "$stitch_prompt" <<STITCH_EOF
# Stitching Task

You are the document stitcher for a long document production pipeline.

## Brain Package
Read ALL files in: .kiro/.long-doc/${DOC_ID}/brain/

## Sections
Read all section files in: ${sections_dir}/
Total estimated words: ${total_words}

## Stitching Patterns
$(if [ -f "$stitching_patterns_path" ]; then echo "Read learned patterns at: ${stitching_patterns_path}"; else echo "No stitching patterns file exists yet."; fi)

## Task
$(if [ "$total_words" -gt 10000 ]; then
echo "This document exceeds 10,000 words. Use sliding window processing:"
echo "- Pass 1: Read sections 1-3, fix transitions, write chunk 1"
echo "- Pass 2: Read chunk 1 (last 500 words) + sections 4-6, write chunk 2"
echo "- Continue until all sections processed"
echo "- Final: verify joins between chunks"
else
echo "Assemble all sections into a single coherent document."
fi)

## Exhibits
$(if [ -d "${LONG_DOC_DIR}/exhibits" ] && ls "${LONG_DOC_DIR}/exhibits"/*.md >/dev/null 2>&1; then
echo "Exhibits directory: .kiro/.long-doc/${DOC_ID}/exhibits/"
echo "Place exhibit content at [INSERT Table/Figure N] markers."
else
echo "No exhibits directory or no exhibit files found."
fi)

## Output
Write the assembled document to: .kiro/.long-doc/${DOC_ID}/assembled.md

## Rules
- Fix transitions between sections (smooth, not abrupt)
- Normalize voice across all sections per brain/voice.md
- Resolve cross-references between sections
- Place exhibits at [INSERT Table/Figure N] markers
- Do NOT remove content. Every sentence from section files must appear.
- No em dashes anywhere in the output.
STITCH_EOF

  clear_sentinel "$stitch_agent_id"

  log "Dispatching ra-doc-stitcher (total_words=${total_words})..."
  bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$stitch_agent_id" "$stitch_output" \
    --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
    --prompt-file "$stitch_prompt" &

  if wait_for_sentinel "$stitch_agent_id" && [ -f "$output_file" ]; then
    local assembled_words
    assembled_words=$(wc -w < "$output_file" | tr -d ' ')
    if [ "$assembled_words" -gt 100 ]; then
      log "Stitch complete (agent-driven, ${assembled_words} words)."
      return 0
    fi
    log "Stitcher produced near-empty output (${assembled_words} words). Falling back to concatenation."
  else
    log "Stitcher failed. Falling back to concatenation."
  fi

  # Concatenation fallback
  log "Using concatenation fallback."
  : > "$output_file"

  local outline="${LONG_DOC_DIR}/brain/outline.md"
  local section_count
  section_count=$(grep -c '^## ' "$outline" 2>/dev/null || echo "0")

  local i=1
  while [ "$i" -le "$section_count" ]; do
    local section_file="${sections_dir}/section_${i}.md"
    if [ -f "$section_file" ]; then
      cat "$section_file" >> "$output_file"
      echo "" >> "$output_file"
      if [ "$i" -lt "$section_count" ]; then
        echo "---" >> "$output_file"
        echo "" >> "$output_file"
      fi
    fi
    i=$((i + 1))
  done

  log "Stitch complete (concatenation fallback)."
  return 0
}

# ============================================================================
# PHASE 5.5: ABSTRACT WRITER
# ============================================================================

run_abstract_writer() {
  if [ "$SKIP_ABSTRACT" -eq 1 ]; then
    log "PHASE 5.5: Abstract Writer — SKIPPED (--no-abstract)"
    return 0
  fi

  local assembled="${LONG_DOC_DIR}/assembled.md"
  if [ ! -f "$assembled" ]; then
    log "PHASE 5.5: Abstract Writer — SKIPPED (assembled.md not found)"
    return 0
  fi

  log "PHASE 5.5: Abstract Writer (ra-abstract-writer)"

  local abstract_agent_id="longdoc-${DOC_ID}-abstract"
  local abstract_output="/tmp/${abstract_agent_id}.out"
  local abstract_prompt="${LONG_DOC_DIR}/prompts/abstract_prompt.md"

  local venue_fingerprints_path="${LEARNER_DIR}/venue_fingerprints.md"

  cat > "$abstract_prompt" <<ABSTRACT_EOF
# Abstract Writing Task

You are the abstract writer for a long document production pipeline.

## Assembled Document
Read the full assembled document at: .kiro/.long-doc/${DOC_ID}/assembled.md

## Brain Package
Read from: .kiro/.long-doc/${DOC_ID}/brain/
Key files: constraints.md (for word limits, venue), argument-map.md (for thesis structure), voice.md (for tone)

## Venue Fingerprints
$(if [ -f "$venue_fingerprints_path" ]; then echo "Read: ${venue_fingerprints_path}"; else echo "No venue fingerprints file exists yet. Use defaults."; fi)

## Doc ID
${DOC_ID}

## Your Task

1. Determine abstract word limit from constraints.md or venue fingerprints (default: 150 words)
2. Read the full assembled document
3. Read the argument map for thesis structure
4. Generate a structured abstract (background, gap, method, finding, implication)
5. Insert the abstract at the top of the assembled document (after YAML frontmatter, before Section 1)
6. Write the modified document back to: .kiro/.long-doc/${DOC_ID}/assembled.md

## Rules
- Abstract must contain ONLY information from the assembled document
- Do not use banned vocabulary (human-authored-writing.md)
- Do not start with "This paper..." or "This study..."
- Respect word limit strictly
- No em dashes
ABSTRACT_EOF

  clear_sentinel "$abstract_agent_id"

  log "Dispatching ra-abstract-writer..."
  bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$abstract_agent_id" "$abstract_output" \
    --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
    --prompt-file "$abstract_prompt" &

  if ! wait_for_sentinel "$abstract_agent_id" "$AGENT_TIMEOUT_SHORT"; then
    log "Abstract writer failed. Proceeding without abstract (non-blocking)."
    return 0
  fi

  # Verify the abstract was actually inserted
  if grep -q '## Abstract' "$assembled" 2>/dev/null; then
    log "Abstract successfully inserted."
  else
    log "Abstract writer completed but abstract not found in assembled.md. Proceeding without."
  fi

  return 0
}

# ============================================================================
# PHASE 6: POST-STITCH EVAL (Devil's Advocate Gate)
# ============================================================================

run_post_stitch_eval() {
  log "PHASE 6: Post-Stitch Eval (ra-post-stitch-eval)"

  local assembled="${LONG_DOC_DIR}/assembled.md"
  if [ ! -f "$assembled" ]; then
    log "POST-STITCH EVAL FAIL: assembled.md not found"
    return 1
  fi

  local eval_agent_id="longdoc-${DOC_ID}-post-eval"
  local eval_output="/tmp/${eval_agent_id}.out"
  local eval_prompt="${LONG_DOC_DIR}/prompts/post_eval_prompt.md"

  cat > "$eval_prompt" <<EVAL_EOF
# Post-Stitch Evaluation (Devil's Advocate)

You are the post-stitch evaluator (devil's advocate) for a long document production pipeline.

## Assembled Document
Read: .kiro/.long-doc/${DOC_ID}/assembled.md

## Brain Package
Read ALL files in: .kiro/.long-doc/${DOC_ID}/brain/
Key files: outline.md, voice.md, terminology.md, constraints.md, advisor-guidance.md

## Eval Calibration (learn from past mistakes)
Read if exists: data/wiki/shared/learner/writing-team/eval_calibration.md
This file records past cases where the eval PASSED but the user FAILED the document. Each entry shows what the eval missed. Do NOT repeat those patterns.

## Original Request
Read: ${PROMPT_FILE}

## Writing Standards
Read: .kiro/steering/human-authored-writing.md

$(if [ -n "$SIMULATE_REVIEWERS" ]; then
echo "## Advisor Persona Mode"
echo "Simulate these reviewers: ${SIMULATE_REVIEWERS}"
echo "Read their entity pages from src/research_assistant/spaces/${SPACE}/wiki/entities/ if they exist."
fi)

## Your Task

**PRIMARY AXIS: Contract Compliance (do this FIRST, before anything else)**

1. Read brain/advisor-guidance.md. Extract every item an advisor explicitly requested (tables, evidence types, structural changes, specific citations, section restructuring).
2. For EACH item, check: is it present in the assembled document? Not mentioned in passing. Actually present as a deliverable (a table exists, a section exists, a citation appears, data is quoted).
3. Score: PASS only if ALL advisor-mandated items are present. If ANY are missing, the verdict is FAIL regardless of prose quality. List each missing item explicitly.

**SECONDARY AXIS: Quality (only if contract compliance passes)**

4. Run gate checks (unresolved markers, banned vocabulary, em dashes, voice, terminology, word count, citation coverage)
5. Produce the devil's advocate analysis (strongest argument against, weakest section, missing counterargument, tone risk, enhancement opportunities)

**THE RULE: A beautifully written document that ignores advisor requirements FAILS. A rough document that addresses all requirements PASSES (with enhancement notes). Contract compliance is binary. Quality is a spectrum.**
3. Write verdict and full analysis to: .kiro/.long-doc/${DOC_ID}/eval/post_stitch_eval.json

## Output Format
{
  "verdict": "pass|fail",
  "reasoning": { "document_goal": "...", "first_weakness_noticed": "...", "reviewer_first_criticism": "..." },
  "gate_checks": { ... },
  "gate_issues": [...],
  "devils_advocate": {
    "strongest_argument_against": "...",
    "weakest_section": {"section": "...", "why": "...", "suggested_fix": "..."},
    "missing_counterargument": "...",
    "tone_risk": "...",
    "enhancement_opportunities": [{"priority": "high|medium|low", "description": "..."}]
  }
}
EVAL_EOF

  clear_sentinel "$eval_agent_id"

  log "Dispatching ra-post-stitch-eval (devil's advocate)..."
  bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$eval_agent_id" "$eval_output" \
    --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
    --prompt-file "$eval_prompt" &

  if ! wait_for_sentinel "$eval_agent_id"; then
    log "Post-stitch eval agent failed. Falling back to heuristic eval only."
    # Run heuristic eval as fallback
    run_heuristic_outer_eval
    return $?
  fi

  # Read the agent's verdict
  local post_eval_file="${LONG_DOC_DIR}/eval/post_stitch_eval.json"
  if [ ! -f "$post_eval_file" ]; then
    log "Post-stitch eval agent completed but did not write eval JSON. Falling back to heuristic."
    run_heuristic_outer_eval
    return $?
  fi

  local agent_verdict
  agent_verdict=$(python3 -c "import json; print(json.load(open('${post_eval_file}')).get('verdict', 'unknown'))" 2>/dev/null || echo "unknown")

  if [ "$agent_verdict" = "pass" ]; then
    log "Post-stitch eval PASSED (agent-verified, devil's advocate notes included)."
    # Also run heuristic outer eval for the outer_eval.json (used by mode comparison)
    run_heuristic_outer_eval
    return 0
  elif [ "$agent_verdict" = "fail" ]; then
    local gate_issues_count
    gate_issues_count=$(python3 -c "import json; d=json.load(open('${post_eval_file}')); print(len(d.get('gate_issues',[])))" 2>/dev/null || echo "?")
    log "Post-stitch eval FAILED (${gate_issues_count} gate issues)."
    run_heuristic_outer_eval
    return 1
  else
    log "Post-stitch eval agent produced unreadable verdict (${agent_verdict}). Running heuristic fallback."
    run_heuristic_outer_eval
    return $?
  fi
}

# Heuristic outer eval (lightweight, always runs for mode comparison scoring)
run_heuristic_outer_eval() {
  local assembled="${LONG_DOC_DIR}/assembled.md"

  local word_count
  word_count=$(wc -w < "$assembled" | tr -d ' ')
  local citation_count
  citation_count=$(grep -c '\[' "$assembled" 2>/dev/null || echo "0")

  local outer_pass=1
  local outer_issues=""

  local word_floor=2000
  if [ "$MODE" = "single-raw" ]; then word_floor=400; fi
  if [ "$word_count" -lt "$word_floor" ]; then
    outer_issues="${outer_issues}Document too short (${word_count} words, floor ${word_floor}). "
    outer_pass=0
  fi

  local citation_floor=5
  if [ "$MODE" = "single-raw" ]; then citation_floor=1; fi
  if [ "$citation_count" -lt "$citation_floor" ]; then
    outer_issues="${outer_issues}Too few citations (${citation_count}). "
    outer_pass=0
  fi

  local em_dash_count
  em_dash_count=$(grep -c '—' "$assembled" 2>/dev/null || echo "0")
  if [ "$em_dash_count" -gt 0 ]; then
    outer_issues="${outer_issues}Contains ${em_dash_count} em dashes (banned). "
  fi

  local absence_count
  absence_count=$(grep -oniE 'no study has|no studies have|no paper exists|no research (addresses|has|exists)|nobody has done|no peer-reviewed study|no (prior |existing )?(work|literature) (has|exists)|has never been studied|for the first time|the first study to' "$assembled" 2>/dev/null | wc -l | tr -d ' ')
  [ -z "$absence_count" ] && absence_count=0
  if [ "$absence_count" -gt 0 ]; then
    outer_issues="${outer_issues}Contains ${absence_count} absolute-absence claim(s) (banned by no-assumption-rule; frame gaps as insufficiency). "
    outer_pass=0
  fi

  cat > "${LONG_DOC_DIR}/eval/outer_eval.json" <<EOF
{
  "pass": $([ "$outer_pass" -eq 1 ] && echo "true" || echo "false"),
  "word_count": ${word_count},
  "citation_count": ${citation_count},
  "em_dash_count": ${em_dash_count},
  "issues": "$(printf '%s' "$outer_issues" | sed 's/"/\\"/g')",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

  if [ "$outer_pass" -eq 1 ]; then
    log "Heuristic outer eval PASSED: ${word_count} words, ${citation_count} citations."
  else
    log "Heuristic outer eval FAILED: ${outer_issues}"
  fi
  return $([ "$outer_pass" -eq 1 ] && echo 0 || echo 1)
}

# ============================================================================
# PHASE 6.5: BENCHMARK COMPARISON
# ============================================================================

run_benchmark_comparison() {
  if [ "$SKIP_BENCHMARK" -eq 1 ]; then
    log "PHASE 6.5: Benchmark Comparison — SKIPPED (--no-benchmark)"
    return 0
  fi

  local assembled="${LONG_DOC_DIR}/assembled.md"
  if [ ! -f "$assembled" ]; then
    log "PHASE 6.5: Benchmark Comparison — SKIPPED (assembled.md not found)"
    return 0
  fi

  log "PHASE 6.5: Benchmark Comparison (ra-benchmark-comparator)"

  local bench_agent_id="longdoc-${DOC_ID}-benchmark"
  local bench_output="/tmp/${bench_agent_id}.out"
  local bench_prompt="${LONG_DOC_DIR}/prompts/benchmark_prompt.md"

  local venue_fingerprints_path="${LEARNER_DIR}/venue_fingerprints.md"
  local knowledge_dir="${WORKSPACE_ROOT}/src/research_assistant/spaces/${SPACE}/knowledge"
  local alt_knowledge_dir="${WORKSPACE_ROOT}/spaces/${SPACE}/knowledge"

  # Find the knowledge directory that exists
  local actual_knowledge_dir=""
  if [ -d "$knowledge_dir" ]; then
    actual_knowledge_dir="$knowledge_dir"
  elif [ -d "$alt_knowledge_dir" ]; then
    actual_knowledge_dir="$alt_knowledge_dir"
  fi

  cat > "$bench_prompt" <<BENCH_EOF
# Benchmark Comparison Task

You are the benchmark comparator for a long document production pipeline.

## Assembled Document
Read: .kiro/.long-doc/${DOC_ID}/assembled.md

## Document Metadata
- Document type: ${DOC_TYPE}
$([ -n "$VENUE" ] && echo "- Target venue: ${VENUE}")
- Target domain: IS, AI governance, management

## Knowledge Directories (for comparison papers)
$(if [ -n "$actual_knowledge_dir" ]; then echo "Primary: ${actual_knowledge_dir}"; else echo "No knowledge directory found for space ${SPACE}."; fi)

## Venue Fingerprints
$(if [ -f "$venue_fingerprints_path" ]; then echo "Read: ${venue_fingerprints_path}"; else echo "No venue fingerprints file exists yet. This is the first run."; fi)

## Your Task

1. Select 3 comparison papers from the knowledge directory (same venue/tier/domain/type)
2. Extract structural fingerprints from each (section order, ratios, citation density, abstract length)
3. Extract same metrics from our assembled document
4. Compare and flag deviations
5. Update venue_fingerprints.md if a target venue is specified

## Output
Write to: .kiro/.long-doc/${DOC_ID}/eval/benchmark_report.json

Use the format from your agent spec:
- comparison_papers, structural_comparison, total_flags, total_warns, recommendations, venue_fingerprint_updated, limitations

## Pass/Fail Logic
- 0-2 flags: PASS
- 3+ flags: FAIL (specific sections need revision)
BENCH_EOF

  clear_sentinel "$bench_agent_id"

  log "Dispatching ra-benchmark-comparator..."
  bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$bench_agent_id" "$bench_output" \
    --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
    --prompt-file "$bench_prompt" &

  if ! wait_for_sentinel "$bench_agent_id"; then
    log "Benchmark comparator failed. Proceeding without benchmark (non-blocking for delivery)."
    return 0
  fi

  # Read the benchmark result
  local bench_report="${LONG_DOC_DIR}/eval/benchmark_report.json"
  if [ ! -f "$bench_report" ]; then
    log "Benchmark agent completed but did not write report JSON. Proceeding."
    return 0
  fi

  local total_flags
  total_flags=$(python3 -c "import json; print(json.load(open('${bench_report}')).get('total_flags', 0))" 2>/dev/null || echo "0")

  if [ "$total_flags" -ge 3 ]; then
    log "Benchmark comparison: ${total_flags} flags (threshold: 3). Sections may need revision."
    # Return 1 to signal the orchestrator that revision may be needed
    return 1
  else
    log "Benchmark comparison PASSED: ${total_flags} flags (threshold: 3)."
    return 0
  fi
}

# ============================================================================
# PHASE 7.5: WRITING TEAM LEARNER (fire-and-forget)
# ============================================================================

run_writing_learner() {
  if [ "$SKIP_LEARNER" -eq 1 ]; then
    log "PHASE 7.5: Writing Team Learner — SKIPPED (--no-learner)"
    return 0
  fi

  log "PHASE 7.5: Writing Team Learner (ra-writing-learner, fire-and-forget)"

  local learner_agent_id="longdoc-${DOC_ID}-learner"
  local learner_output="/tmp/${learner_agent_id}.out"
  local learner_prompt="${LONG_DOC_DIR}/prompts/learner_prompt.md"

  # Gather metadata
  local total_words=0
  if [ -f "${LONG_DOC_DIR}/assembled.md" ]; then
    total_words=$(wc -w < "${LONG_DOC_DIR}/assembled.md" | tr -d ' ')
  fi

  local section_count=0
  local outline="${LONG_DOC_DIR}/brain/outline.md"
  if [ -f "$outline" ]; then
    section_count=$(grep -c '^## ' "$outline" 2>/dev/null || echo "0")
  fi

  cat > "$learner_prompt" <<LEARNER_EOF
# Writing Team Learner Task

You are the writing team learner. You run after every long document production run to capture patterns.

## Working Directory
Read ALL files in: .kiro/.long-doc/${DOC_ID}/

Key files:
- orchestration.log (sequence of events, timing, retries)
- eval/outline_eval.json
- eval/pre_stitch_eval.json
- eval/post_stitch_eval.json
- eval/outer_eval.json
- eval/benchmark_report.json (if exists)
- brain/outline.md
- sections/ (all section files)

## Writing Team Learner Directory
Read and update files in: ${LEARNER_DIR}/

## Document Metadata
- doc_id: ${DOC_ID}
- doc_type: ${DOC_TYPE}
- mode_used: ${MODE}
- total_words: ${total_words}
- sections_count: ${section_count}
- space: ${SPACE}
$([ -n "$VENUE" ] && echo "- venue: ${VENUE}")

## Your Task

Follow the full 9-step process from your agent spec:
1. Read the run trace
2. Extract observations (Trigger/Diagnosis/Action)
3. Check against existing patterns
4. Graduate patterns (3+ observations)
5. Retire stale patterns
6. Update mode comparison
7. Update venue fingerprints (if benchmark data exists)
8. Self-check all entries for actionability (score < 3 = rewrite or drop)
9. Enforce token caps

## Output

1. Updated files in ${LEARNER_DIR}/
2. Per-run trace at data/logs/writing-team/runs/${DOC_ID}_$(date +%Y%m%d-%H%M%S).md

Create data/logs/writing-team/runs/ if it does not exist.
LEARNER_EOF

  clear_sentinel "$learner_agent_id"

  # Fire-and-forget: dispatch but do not wait
  log "Dispatching ra-writing-learner (fire-and-forget)..."
  bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$learner_agent_id" "$learner_output" \
    --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
    --prompt-file "$learner_prompt" &

  # Do NOT wait for sentinel — learner runs in background
  log "Writing team learner dispatched. Will complete asynchronously."
  return 0
}

# ============================================================================
# PHASE 7: DELIVER
# ============================================================================

deliver() {
  local assembled="${1:-${LONG_DOC_DIR}/assembled.md}"
  local mode_label="${2:-}"

  log "PHASE 7: Deliver"

  # Prefer the canonical tree; fall back to the legacy tree only if a canonical
  # space dir does not exist (mirrors the knowledge-dir pattern above). New
  # deliverables land under src/research_assistant/spaces; legacy output dirs
  # are still honored so past deliverables remain discoverable.
  local output_dir="${WORKSPACE_ROOT}/src/research_assistant/spaces/${SPACE}/output"
  if [ ! -d "${WORKSPACE_ROOT}/src/research_assistant/spaces/${SPACE}" ] && [ -d "${WORKSPACE_ROOT}/spaces/${SPACE}" ]; then
    output_dir="${WORKSPACE_ROOT}/spaces/${SPACE}/output"
  fi
  mkdir -p "$output_dir"

  # Determine version number
  local version=1
  while [ -f "${output_dir}/${DOC_ID}_v${version}.md" ]; do
    version=$((version + 1))
  done

  local final_path="${output_dir}/${DOC_ID}_v${version}.md"
  cp "$assembled" "$final_path"

  log "Delivered to: ${final_path}"
  echo ""
  echo "============================================"
  echo "DOCUMENT DELIVERED"
  echo "============================================"
  echo "  Path: ${final_path}"
  echo "  Words: $(wc -w < "$final_path" | tr -d ' ')"
  echo "  Mode: ${mode_label:-${MODE}}"
  echo "  Version: v${version}"
  echo "============================================"

  # Show devil's advocate notes if available
  local post_eval="${LONG_DOC_DIR}/eval/post_stitch_eval.json"
  if [ -f "$post_eval" ]; then
    local da_summary
    da_summary=$(python3 -c "
import json, sys
d = json.load(open('${post_eval}'))
da = d.get('devils_advocate', {})
if da:
    print('  Devil\\'s Advocate Notes:')
    if da.get('strongest_argument_against'):
        print('    Strongest counter: ' + da['strongest_argument_against'][:120])
    ws = da.get('weakest_section', {})
    if ws and ws.get('section'):
        print('    Weakest section: ' + ws['section'])
    enhancements = da.get('enhancement_opportunities', [])
    high_priority = [e for e in enhancements if e.get('priority') == 'high']
    if high_priority:
        print('    High-priority enhancements: ' + str(len(high_priority)))
" 2>/dev/null || true)
    if [ -n "$da_summary" ]; then
      echo "$da_summary"
    fi
  fi

  # Show benchmark notes if available
  local bench_report="${LONG_DOC_DIR}/eval/benchmark_report.json"
  if [ -f "$bench_report" ]; then
    local bench_summary
    bench_summary=$(python3 -c "
import json
d = json.load(open('${bench_report}'))
flags = d.get('total_flags', 0)
warns = d.get('total_warns', 0)
print('  Benchmark: %d flags, %d warns' % (flags, warns))
" 2>/dev/null || true)
    if [ -n "$bench_summary" ]; then
      echo "$bench_summary"
    fi
  fi

  echo "============================================"

  # Log to mode comparison if applicable
  if [ -n "$mode_label" ]; then
    local score
    score=$(python3 -c "import json; d=json.load(open('${LONG_DOC_DIR}/eval/outer_eval.json')); print(d.get('word_count',0)/1000 + d.get('citation_count',0)/5)" 2>/dev/null || echo "5")

    mkdir -p "$LEARNER_DIR"
    echo "{\"doc_id\":\"${DOC_ID}\",\"doc_type\":\"${DOC_TYPE}\",\"mode\":\"${mode_label}\",\"score\":${score},\"words\":$(wc -w < "$final_path" | tr -d ' '),\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> "${LEARNER_DIR}/mode_comparison.jsonl"
  fi

  return 0
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

# Skip to resume point if specified
CURRENT_PHASE="brain"
if [ -n "$RESUME_FROM" ]; then
  case "$RESUME_FROM" in
    outline|sections) CURRENT_PHASE="sections" ;;
    stitch) CURRENT_PHASE="stitch" ;;
    eval) CURRENT_PHASE="eval" ;;
    *) echo "error: invalid --resume-from value: ${RESUME_FROM}" >&2; exit 2 ;;
  esac
fi

# ============================================================================
# SINGLE-RAW PATH (short documents <2000 words)
# One writer agent, no brain package, no outline eval, no stitch. The brain and
# outline phases (and their 2000-word floor) are designed for long documents and
# do not apply to short briefings. This path produces the document directly.
# ============================================================================

run_single_raw() {
  log "SINGLE-RAW: short-document path (no brain, no outline, no stitch)"
  mkdir -p "$LONG_DOC_DIR" "${LONG_DOC_DIR}/prompts" "${LONG_DOC_DIR}/eval"

  local assembled="${LONG_DOC_DIR}/assembled.md"
  local writer_prompt="${LONG_DOC_DIR}/prompts/single_raw_prompt.md"
  local writer_agent_id="longdoc-${DOC_ID}-single-raw"
  local writer_output="/tmp/${writer_agent_id}.out"

  # Build the writer prompt: the original task prompt plus an explicit, overriding
  # instruction to write the finished document to the pipeline's assembled.md path.
  cp "$PROMPT_FILE" "$writer_prompt"
  cat >> "$writer_prompt" <<SR_EOF

---

## OUTPUT LOCATION (pipeline override; takes precedence over any earlier output path)

Write the COMPLETE finished document to exactly this path:
\`${assembled}\`

Write the document content only (no commentary, no notes about the task). The pipeline
will copy this file to the space output directory with a version number.
SR_EOF

  clear_sentinel "$writer_agent_id"
  log "Dispatching single-raw writer agent..."
  bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$writer_agent_id" "$writer_output" \
    --category document \
    --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
    --prompt-file "$writer_prompt" &

  if ! wait_for_sentinel "$writer_agent_id" "$AGENT_TIMEOUT_LONG"; then
    log "Single-raw writer FAILED (no sentinel)."
    return 1
  fi

  if [ ! -f "$assembled" ] || [ ! -s "$assembled" ]; then
    log "Single-raw writer produced no document at ${assembled}. Aborting."
    return 1
  fi

  # Lightweight checks appropriate for a short document (no 2000-word floor).
  local word_count em_dash_count absence_hits
  word_count=$(wc -w < "$assembled" | tr -d ' ')
  em_dash_count=$(grep -o '—' "$assembled" 2>/dev/null | wc -l | tr -d ' ')
  [ -z "$em_dash_count" ] && em_dash_count=0
  absence_hits=$(grep -oniE 'no study has|no studies have|no paper exists|no research (addresses|has|exists)|nobody has done|no peer-reviewed study|no (prior |existing )?(work|literature) (has|exists)|has never been studied|for the first time|the first study to' "$assembled" 2>/dev/null || true)
  log "Single-raw document: ${word_count} words, ${em_dash_count} em dashes."
  if [ "$em_dash_count" -gt 0 ]; then
    log "WARNING: document contains ${em_dash_count} em dashes (banned by writing standard). Flagging for review."
  fi
  if [ -n "$absence_hits" ]; then
    log "WARNING: absolute-absence phrasing detected (banned by no-assumption-rule; frame gaps as insufficiency):"
    printf '%s\n' "$absence_hits" | while IFS= read -r line; do log "    ${line}"; done
  fi

  deliver "$assembled" "single-raw"
  return 0
}

# Short-document bypass: skip brain/outline/sections/stitch entirely.
if [ "$MODE" = "single-raw" ] && [ "$CURRENT_PHASE" = "brain" ]; then
  run_single_raw || { log "Single-raw path failed. Aborting."; exit 1; }
  run_writing_learner || true
  exit 0
fi

# --- Phase 1: Brain Assembly ---
if [ "$CURRENT_PHASE" = "brain" ]; then
  RETRY=0
  while [ "$RETRY" -le 2 ]; do
    if run_brain_assembly; then
      break
    fi
    RETRY=$((RETRY + 1))
    if [ "$RETRY" -le 2 ]; then
      log "Retrying brain assembly (attempt ${RETRY}/2)..."
    else
      log "Brain assembly failed after 2 retries. Aborting."
      exit 1
    fi
  done

  # Phase 2: Outline Eval
  RETRY=0
  while [ "$RETRY" -le 2 ]; do
    if run_outline_eval; then
      break
    fi
    RETRY=$((RETRY + 1))
    if [ "$RETRY" -le 2 ]; then
      log "Re-dispatching brain assembler with outline feedback (attempt ${RETRY}/2)..."
      run_brain_assembly || true
    else
      log "Outline eval failed after 2 retries. Aborting."
      exit 1
    fi
  done

  if [ "$PAUSE_AFTER" = "outline" ]; then
    write_state "outline"
    log "PAUSED after outline. Review .kiro/.long-doc/${DOC_ID}/brain/ then run with --resume-from sections"
    exit 0
  fi
  CURRENT_PHASE="sections"
fi

# --- Phase 3: Section Dispatch ---
if [ "$CURRENT_PHASE" = "sections" ]; then
  if [ "$MODE" = "both" ]; then
    log "Running BOTH modes for comparison."

    # Parallel run
    dispatch_sections "parallel" "parallel" || log "Parallel mode had failures."

    # Sequential run
    dispatch_sections "sequential" "sequential" || log "Sequential mode had failures."
  else
    dispatch_sections "$MODE" || {
      log "Section dispatch failed. Aborting."
      exit 1
    }
  fi

  if [ "$PAUSE_AFTER" = "sections" ]; then
    write_state "sections"
    log "PAUSED after sections. Review .kiro/.long-doc/${DOC_ID}/sections/ then run with --resume-from stitch"
    exit 0
  fi
  CURRENT_PHASE="stitch"
fi

# --- Phase 4 + 5 + 5.5: Pre-Stitch Eval + Stitch + Abstract ---
if [ "$CURRENT_PHASE" = "stitch" ]; then
  if [ "$MODE" = "both" ]; then
    # Eval and stitch both versions
    log "Evaluating parallel sections..."
    run_pre_stitch_eval "${LONG_DOC_DIR}/sections-parallel"
    PARALLEL_PRE_PASS=$?

    log "Evaluating sequential sections..."
    run_pre_stitch_eval "${LONG_DOC_DIR}/sections-sequential"
    SEQUENTIAL_PRE_PASS=$?

    # Stitch whichever passed (or both)
    if [ "$PARALLEL_PRE_PASS" -eq 0 ]; then
      run_stitch "${LONG_DOC_DIR}/sections-parallel"
      if [ -f "${LONG_DOC_DIR}/assembled.md" ]; then
        run_abstract_writer
        cp "${LONG_DOC_DIR}/assembled.md" "${LONG_DOC_DIR}/assembled-parallel.md"
      fi
    fi

    if [ "$SEQUENTIAL_PRE_PASS" -eq 0 ]; then
      run_stitch "${LONG_DOC_DIR}/sections-sequential"
      if [ -f "${LONG_DOC_DIR}/assembled.md" ]; then
        run_abstract_writer
        cp "${LONG_DOC_DIR}/assembled.md" "${LONG_DOC_DIR}/assembled-sequential.md"
      fi
    fi
  else
    run_pre_stitch_eval || {
      log "Pre-stitch eval failed. Attempting delivery with existing sections."
    }
    run_stitch
    run_abstract_writer
  fi

  if [ "$PAUSE_AFTER" = "stitch" ]; then
    write_state "stitch"
    log "PAUSED after stitch. Review .kiro/.long-doc/${DOC_ID}/assembled.md then run with --resume-from eval"
    exit 0
  fi
  CURRENT_PHASE="eval"
fi

# --- Phase 6 + 6.5 + 7 + 7.5: Post-Stitch Eval + Benchmark + Deliver + Learner ---
if [ "$CURRENT_PHASE" = "eval" ]; then
  if [ "$MODE" = "both" ]; then
    # Eval both and deliver the better one
    PARALLEL_SCORE=0
    SEQUENTIAL_SCORE=0

    if [ -f "${LONG_DOC_DIR}/assembled-parallel.md" ]; then
      cp "${LONG_DOC_DIR}/assembled-parallel.md" "${LONG_DOC_DIR}/assembled.md"
      if run_post_stitch_eval; then
        PARALLEL_SCORE=$(python3 -c "import json; d=json.load(open('${LONG_DOC_DIR}/eval/outer_eval.json')); print(d.get('word_count',0) + d.get('citation_count',0)*100)" 2>/dev/null || echo "0")
      fi
      cp "${LONG_DOC_DIR}/eval/outer_eval.json" "${LONG_DOC_DIR}/eval/outer_eval_parallel.json" 2>/dev/null || true
      cp "${LONG_DOC_DIR}/eval/post_stitch_eval.json" "${LONG_DOC_DIR}/eval/post_stitch_eval_parallel.json" 2>/dev/null || true
    fi

    if [ -f "${LONG_DOC_DIR}/assembled-sequential.md" ]; then
      cp "${LONG_DOC_DIR}/assembled-sequential.md" "${LONG_DOC_DIR}/assembled.md"
      if run_post_stitch_eval; then
        SEQUENTIAL_SCORE=$(python3 -c "import json; d=json.load(open('${LONG_DOC_DIR}/eval/outer_eval.json')); print(d.get('word_count',0) + d.get('citation_count',0)*100)" 2>/dev/null || echo "0")
      fi
      cp "${LONG_DOC_DIR}/eval/outer_eval.json" "${LONG_DOC_DIR}/eval/outer_eval_sequential.json" 2>/dev/null || true
      cp "${LONG_DOC_DIR}/eval/post_stitch_eval.json" "${LONG_DOC_DIR}/eval/post_stitch_eval_sequential.json" 2>/dev/null || true
    fi

    log "Mode comparison: parallel=${PARALLEL_SCORE}, sequential=${SEQUENTIAL_SCORE}"

    if [ "$PARALLEL_SCORE" -ge "$SEQUENTIAL_SCORE" ] && [ -f "${LONG_DOC_DIR}/assembled-parallel.md" ]; then
      cp "${LONG_DOC_DIR}/assembled-parallel.md" "${LONG_DOC_DIR}/assembled.md"
      cp "${LONG_DOC_DIR}/eval/post_stitch_eval_parallel.json" "${LONG_DOC_DIR}/eval/post_stitch_eval.json" 2>/dev/null || true
      run_benchmark_comparison || log "Benchmark flagged issues (informational for both mode)."
      deliver "${LONG_DOC_DIR}/assembled-parallel.md" "parallel"
    elif [ -f "${LONG_DOC_DIR}/assembled-sequential.md" ]; then
      cp "${LONG_DOC_DIR}/assembled-sequential.md" "${LONG_DOC_DIR}/assembled.md"
      cp "${LONG_DOC_DIR}/eval/post_stitch_eval_sequential.json" "${LONG_DOC_DIR}/eval/post_stitch_eval.json" 2>/dev/null || true
      run_benchmark_comparison || log "Benchmark flagged issues (informational for both mode)."
      deliver "${LONG_DOC_DIR}/assembled-sequential.md" "sequential"
    else
      log "Neither mode produced a deliverable document."
      exit 1
    fi
  else
    # Single-mode flow with retry on post-stitch failure
    post_stitch_retries=0
    post_stitch_passed=0

    while [ "$post_stitch_retries" -le 2 ]; do
      if run_post_stitch_eval; then
        post_stitch_passed=1
        break
      fi

      post_stitch_retries=$((post_stitch_retries + 1))
      if [ "$post_stitch_retries" -le 2 ]; then
        log "Post-stitch eval failed. Re-stitching with gate feedback (attempt ${post_stitch_retries}/2)..."

        # Extract gate issues for the stitcher
        gate_feedback=""
        if [ -f "${LONG_DOC_DIR}/eval/post_stitch_eval.json" ]; then
          gate_feedback=$(python3 -c "
import json
d = json.load(open('${LONG_DOC_DIR}/eval/post_stitch_eval.json'))
issues = d.get('gate_issues', [])
if issues:
    print('\\n'.join('- ' + str(i) for i in issues[:5]))
" 2>/dev/null || echo "Gate check failures detected.")
        fi

        # Append feedback to the stitch prompt and re-run
        retry_stitch_prompt="${LONG_DOC_DIR}/prompts/stitch_retry_${post_stitch_retries}_prompt.md"
        if [ -f "${LONG_DOC_DIR}/prompts/stitch_prompt.md" ]; then
          cp "${LONG_DOC_DIR}/prompts/stitch_prompt.md" "$retry_stitch_prompt"
          {
            echo ""
            echo "## REVISION REQUIRED (attempt ${post_stitch_retries})"
            echo ""
            echo "The previous assembly FAILED post-stitch evaluation. Fix these gate issues:"
            echo ""
            echo "$gate_feedback"
            echo ""
            echo "Re-read voice.md and terminology.md. Fix all issues listed above."
          } >> "$retry_stitch_prompt"
        fi

        # Clear old assembled file and re-stitch
        rm -f "${LONG_DOC_DIR}/assembled.md"

        retry_agent_id="longdoc-${DOC_ID}-stitcher-retry${post_stitch_retries}"
        retry_output="/tmp/${retry_agent_id}.out"
        clear_sentinel "$retry_agent_id"

        bash "${SCRIPTS_DIR}/spawn-gpu-agent.sh" "$retry_agent_id" "$retry_output" \
          --model "$RA_AGENT_MODEL" --allowed-tools "Read,Write,Edit,Bash,Glob,Grep" \
          --prompt-file "$retry_stitch_prompt" &

        if wait_for_sentinel "$retry_agent_id" && [ -f "${LONG_DOC_DIR}/assembled.md" ]; then
          log "Re-stitch complete (attempt ${post_stitch_retries})."
          run_abstract_writer
        else
          log "Re-stitch failed (attempt ${post_stitch_retries}). Using previous version."
          break
        fi
      fi
    done

    if [ "$post_stitch_passed" -eq 1 ]; then
      # Benchmark comparison (non-blocking for delivery but informational)
      run_benchmark_comparison || log "Benchmark flagged issues. Consider revising flagged sections."
      deliver "${LONG_DOC_DIR}/assembled.md" "${MODE}"
    else
      log "Post-stitch eval failed after ${post_stitch_retries} retries. Delivering with manual review required."
      deliver "${LONG_DOC_DIR}/assembled.md" "${MODE}"
    fi
  fi

  # Fire-and-forget: writing team learner
  run_writing_learner
fi

log "Pipeline complete for doc_id=${DOC_ID}."
