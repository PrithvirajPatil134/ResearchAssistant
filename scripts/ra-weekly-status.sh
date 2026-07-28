#!/usr/bin/env bash
# ra-weekly-status.sh — Weekly observability report
# Writes: data/logs/status/weekly_YYYY-MM-DD.md
# Run on demand (housekeeping/report; no scheduler needed). Suggested cadence: Sunday 09:00 via cron.
# macOS bash 3.2 compatible

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TODAY="$(date +%Y-%m-%d)"
STATUS_DIR="${WORKSPACE_ROOT}/data/logs/status"
OUTPUT="${STATUS_DIR}/weekly_${TODAY}.md"

mkdir -p "$STATUS_DIR"

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is required but not found. Install with: brew install jq" >&2
  exit 1
fi

{
  echo "# Weekly Status Report — ${TODAY}"
  echo ""
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""

  # --- Agent Spawns ---
  echo "## Agent Spawns (Last 7 Days)"
  echo ""

  SENTINEL_DIR="${WORKSPACE_ROOT}/.kiro/.gpu-agent-done"
  if [ -d "$SENTINEL_DIR" ]; then
    total=0
    pass=0
    fail=0
    while IFS= read -r f; do
      if [ -z "$f" ]; then continue; fi
      mod_epoch=$(stat -f '%m' "$f" 2>/dev/null || echo 0)
      week_ago_epoch=$(date -v-7d +%s 2>/dev/null || date -d '7 days ago' +%s 2>/dev/null || echo 0)
      if [ "$mod_epoch" -ge "$week_ago_epoch" ]; then
        total=$((total + 1))
        ec=$(jq -r '.exit_code // 1' "$f" 2>/dev/null || echo 1)
        if [ "$ec" -eq 0 ]; then
          pass=$((pass + 1))
        else
          fail=$((fail + 1))
        fi
      fi
    done < <(find "$SENTINEL_DIR" -name "*.done" -type f 2>/dev/null)
    echo "- Total: ${total}"
    echo "- Pass (exit 0): ${pass}"
    echo "- Fail (exit != 0): ${fail}"
  else
    echo "- No sentinel directory found (no agents spawned yet)"
  fi
  echo ""

  # --- Wiki Growth ---
  echo "## Wiki Growth (Last 7 Days)"
  echo ""

  wiki_found=0
  for space_dir in "${WORKSPACE_ROOT}"/src/research_assistant/spaces/*/wiki; do
    if [ ! -d "$space_dir" ]; then continue; fi
    wiki_found=1
    space_name="$(basename "$(dirname "$space_dir")")"
    if [ -f "${STATUS_DIR}/.week-marker" ]; then
      added=$(find "$space_dir" -name "*.md" -newer "${STATUS_DIR}/.week-marker" -type f 2>/dev/null | wc -l | tr -d ' ')
    else
      added="(first run)"
    fi
    total_pages=$(find "$space_dir" -name "*.md" -not -name "_*" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "- **${space_name}**: ${total_pages} total pages (${added} new/modified this week)"
  done
  if [ "$wiki_found" -eq 0 ]; then
    echo "- No wiki directories found yet"
  fi
  echo ""

  # --- Auto-Capture Hook ---
  echo "## Auto-Capture Hook"
  echo ""

  hook_file="${WORKSPACE_ROOT}/.kiro/hooks/wiki-auto-ingest.kiro.hook"
  if [ -f "$hook_file" ]; then
    echo "- Hook file exists"
  else
    echo "- Hook file not yet created"
  fi
  echo ""

  # --- Orphan Images ---
  echo "## Orphan Images (>60 days, unreferenced)"
  echo ""

  orphan_count=0
  for img_dir in "${WORKSPACE_ROOT}"/src/research_assistant/spaces/*/communication/images; do
    if [ ! -d "$img_dir" ]; then continue; fi
    while IFS= read -r img; do
      if [ -z "$img" ]; then continue; fi
      img_name="$(basename "$img")"
      refs=$( (grep -rl "$img_name" "${WORKSPACE_ROOT}/spaces" "${WORKSPACE_ROOT}/data" 2>/dev/null || true) | wc -l | tr -d ' ')
      if [ "$refs" -eq 0 ]; then
        orphan_count=$((orphan_count + 1))
      fi
    done < <(find "$img_dir" -type f -mtime +60 2>/dev/null)
  done
  echo "- Orphan images (>60 days, unreferenced): ${orphan_count}"
  echo ""

  # --- Stale Seed Pages ---
  echo "## Stale Seed Pages (>30 days, still at seed maturity)"
  echo ""

  stale_count=0
  for space_dir in "${WORKSPACE_ROOT}"/src/research_assistant/spaces/*/wiki; do
    if [ ! -d "$space_dir" ]; then continue; fi
    while IFS= read -r page; do
      if [ -z "$page" ]; then continue; fi
      if grep -q "^maturity: seed" "$page" 2>/dev/null; then
        stale_count=$((stale_count + 1))
      fi
    done < <(find "$space_dir" -name "*.md" -not -name "_*" -type f -mtime +30 2>/dev/null)
  done
  echo "- Stale seed pages: ${stale_count}"
  echo ""

  # --- Storage Audit ---
  echo "## Storage Audit"
  echo ""

  print_size() {
    local dir="$1"
    local label="$2"
    if [ -d "$dir" ]; then
      size=$(du -sh "$dir" 2>/dev/null | cut -f1)
      echo "- ${label}: ${size}"
    elif [ -f "$dir" ]; then
      size=$(du -sh "$dir" 2>/dev/null | cut -f1)
      echo "- ${label}: ${size}"
    else
      echo "- ${label}: (not found)"
    fi
  }

  print_size "${WORKSPACE_ROOT}/data/logs/learner/runs" "Learner runs (Tier 1)"
  print_size "${WORKSPACE_ROOT}/data/logs/learner/archive" "Learner archive (Tier 2)"
  print_size "${WORKSPACE_ROOT}/data/logs/learner/summaries" "Learner summaries (Tier 3)"
  print_size "${WORKSPACE_ROOT}/data/drafts" "Session drafts"

  comp_log="${WORKSPACE_ROOT}/data/logs/backend_comparison.jsonl"
  if [ -f "$comp_log" ]; then
    lines=$(wc -l < "$comp_log" | tr -d ' ')
    size=$(du -sh "$comp_log" 2>/dev/null | cut -f1)
    echo "- Backend comparison log: ${size} (${lines} entries)"
  else
    echo "- Backend comparison log: (not found)"
  fi
  echo ""

  # --- Recent Failures ---
  echo "## Recent Failures (Last 7 Days)"
  echo ""

  if [ -f "$comp_log" ]; then
    week_ago=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d '7 days ago' +%Y-%m-%d 2>/dev/null || echo "0000-00-00")
    fail_lines=$( (jq -r "select(.timestamp >= \"${week_ago}\") | select(.exit_code != 0) | .agent_id // empty" "$comp_log" 2>/dev/null || true) | (grep -v '^$' || true) | head -10)
    if [ -n "$fail_lines" ]; then
      echo "$fail_lines" | while read -r line; do
        echo "- ${line}"
      done
    else
      echo "- No failures recorded"
    fi
  else
    echo "- No backend comparison log found"
  fi
  echo ""

  # --- Wiki Lint Summary ---
  echo "## Wiki Lint Summary"
  echo ""

  lint_script="${WORKSPACE_ROOT}/scripts/ra-wiki-lint.sh"
  if [ -f "$lint_script" ]; then
    lint_output=$(bash "$lint_script" 2>&1 || true)
    lint_errors=$(echo "$lint_output" | grep "^- Errors:" | sed 's/.*: //' || echo "0")
    lint_warnings=$(echo "$lint_output" | grep "^- Warnings:" | sed 's/.*: //' || echo "0")
    lint_pages=$(echo "$lint_output" | grep "^- Pages checked:" | sed 's/.*: //' || echo "0")
    lint_result=$(echo "$lint_output" | grep "^RESULT:" || echo "N/A")
    echo "- Pages checked: ${lint_pages}"
    echo "- Errors: ${lint_errors}"
    echo "- Warnings: ${lint_warnings}"
    echo "- Result: ${lint_result}"
  else
    echo "- ra-wiki-lint.sh not found, skipping"
  fi
  echo ""

  # --- Manifest Cleanup Summary ---
  echo "## Manifest Cleanup Summary"
  echo ""

  cleanup_script="${WORKSPACE_ROOT}/scripts/ra-manifest-cleanup.sh"
  if [ -f "$cleanup_script" ]; then
    cleanup_output=$(bash "$cleanup_script" 2>&1 || true)
    moved=$(echo "$cleanup_output" | grep -o 'Moved [0-9]*' | grep -o '[0-9]*' || echo "0")
    echo "- Manifests archived: ${moved}"
  else
    echo "- ra-manifest-cleanup.sh not found, skipping"
  fi
  echo ""

  # --- Learner Size Check ---
  echo "## Learner Size Check"
  echo ""

  size_script="${WORKSPACE_ROOT}/scripts/learner-size-check.sh"
  if [ -f "$size_script" ]; then
    size_output=$(bash "$size_script" 2>&1)
    size_rc=$?
    if [ "$size_rc" -eq 0 ]; then
      echo "- Status: All files within token caps"
    else
      echo "- Status: **VIOLATION** — files exceed token caps"
      echo "$size_output" | grep "^VIOLATION" | while read -r vline; do
        echo "  - ${vline}"
      done
    fi
  else
    echo "- learner-size-check.sh not found, skipping"
  fi
  echo ""

  # Update week marker for next run
  touch "${STATUS_DIR}/.week-marker"

} > "$OUTPUT"

echo "[ra-weekly-status] Report written to ${OUTPUT}"
