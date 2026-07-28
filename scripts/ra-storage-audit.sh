#!/usr/bin/env bash
# ra-storage-audit.sh — Storage size breakdown per tracked directory
# Usage: bash scripts/ra-storage-audit.sh [--json]
# macOS bash 3.2 compatible

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
JSON_MODE=0

if [ "${1:-}" = "--json" ]; then
  JSON_MODE=1
fi

get_size_bytes() {
  local path="$1"
  if [ -d "$path" ]; then
    du -sk "$path" 2>/dev/null | cut -f1
  elif [ -f "$path" ]; then
    du -sk "$path" 2>/dev/null | cut -f1
  else
    echo "0"
  fi
}

get_size_human() {
  local path="$1"
  if [ -d "$path" ] || [ -f "$path" ]; then
    du -sh "$path" 2>/dev/null | cut -f1
  else
    echo "0B"
  fi
}

get_line_count() {
  local path="$1"
  if [ -f "$path" ]; then
    wc -l < "$path" | tr -d ' '
  else
    echo "0"
  fi
}

DIRS=(
  "data/drafts"
  "data/drafts/archive"
  "data/logs/learner/runs"
  "data/logs/learner/archive"
  "data/logs/learner/summaries"
  ".kiro/.ingest-pending"
  ".kiro/.gpu-agent-done"
)

if [ "$JSON_MODE" -eq 1 ]; then
  echo "{"
  echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
  echo "  \"directories\": {"

  first=1
  for dir in "${DIRS[@]}"; do
    full_path="${WORKSPACE_ROOT}/${dir}"
    size_kb=$(get_size_bytes "$full_path")
    size_human=$(get_size_human "$full_path")
    if [ "$first" -eq 0 ]; then echo ","; fi
    printf '    "%s": {"size_kb": %s, "size_human": "%s", "exists": %s}' \
      "$dir" "$size_kb" "$size_human" \
      "$([ -d "$full_path" ] && echo "true" || echo "false")"
    first=0
  done
  echo ""
  echo "  },"

  # Backend comparison log
  comp_log="${WORKSPACE_ROOT}/data/logs/backend_comparison.jsonl"
  comp_lines=$(get_line_count "$comp_log")
  comp_size=$(get_size_human "$comp_log")
  echo "  \"backend_comparison_log\": {\"lines\": ${comp_lines}, \"size_human\": \"${comp_size}\", \"exists\": $([ -f "$comp_log" ] && echo "true" || echo "false")},"

  # Image directories
  echo "  \"image_directories\": {"
  first=1
  for img_dir in "${WORKSPACE_ROOT}"/src/research_assistant/spaces/*/communication/images; do
    if [ ! -d "$img_dir" ]; then continue; fi
    rel_path="${img_dir#${WORKSPACE_ROOT}/}"
    size_human=$(get_size_human "$img_dir")
    size_kb=$(get_size_bytes "$img_dir")
    if [ "$first" -eq 0 ]; then echo ","; fi
    printf '    "%s": {"size_kb": %s, "size_human": "%s"}' "$rel_path" "$size_kb" "$size_human"
    first=0
  done
  if [ "$first" -eq 1 ]; then
    printf '    "_none": {"note": "no image directories found"}'
  fi
  echo ""
  echo "  }"
  echo "}"
else
  echo "=== Storage Audit — $(date +%Y-%m-%d) ==="
  echo ""

  printf "%-45s %10s\n" "Directory" "Size"
  printf "%-45s %10s\n" "---------" "----"

  for dir in "${DIRS[@]}"; do
    full_path="${WORKSPACE_ROOT}/${dir}"
    if [ -d "$full_path" ]; then
      size_human=$(get_size_human "$full_path")
      printf "%-45s %10s\n" "$dir" "$size_human"
    else
      printf "%-45s %10s\n" "$dir" "(missing)"
    fi
  done

  # Backend comparison log
  comp_log="${WORKSPACE_ROOT}/data/logs/backend_comparison.jsonl"
  if [ -f "$comp_log" ]; then
    comp_lines=$(get_line_count "$comp_log")
    comp_size=$(get_size_human "$comp_log")
    printf "%-45s %10s (%s lines)\n" "data/logs/backend_comparison.jsonl" "$comp_size" "$comp_lines"
  else
    printf "%-45s %10s\n" "data/logs/backend_comparison.jsonl" "(missing)"
  fi

  # Image directories
  for img_dir in "${WORKSPACE_ROOT}"/src/research_assistant/spaces/*/communication/images; do
    if [ ! -d "$img_dir" ]; then continue; fi
    rel_path="${img_dir#${WORKSPACE_ROOT}/}"
    size_human=$(get_size_human "$img_dir")
    printf "%-45s %10s\n" "$rel_path" "$size_human"
  done

  echo ""
  echo "--- Size Growth Warning ---"

  # Check for directories that doubled in the last 30 days
  # Compare current size with a saved snapshot
  snapshot="${WORKSPACE_ROOT}/data/logs/status/.storage-snapshot"
  warned=0
  if [ -f "$snapshot" ]; then
    while IFS='|' read -r snap_dir snap_kb snap_date; do
      snap_epoch=$(date -jf "%Y-%m-%d" "$snap_date" +%s 2>/dev/null || echo 0)
      now_epoch=$(date +%s)
      days_diff=$(( (now_epoch - snap_epoch) / 86400 ))
      if [ "$days_diff" -le 30 ] && [ "$days_diff" -gt 0 ]; then
        full_path="${WORKSPACE_ROOT}/${snap_dir}"
        current_kb=$(get_size_bytes "$full_path")
        if [ "$snap_kb" -gt 0 ] && [ "$current_kb" -ge $((snap_kb * 2)) ]; then
          echo "WARNING: ${snap_dir} doubled from ${snap_kb}KB to ${current_kb}KB in ${days_diff} days"
          warned=1
        fi
      fi
    done < "$snapshot"
  fi
  if [ "$warned" -eq 0 ]; then
    echo "No directories have doubled in size in the last 30 days."
  fi

  # Save current snapshot for future comparison
  mkdir -p "$(dirname "$snapshot")"
  : > "$snapshot"
  for dir in "${DIRS[@]}"; do
    full_path="${WORKSPACE_ROOT}/${dir}"
    size_kb=$(get_size_bytes "$full_path")
    echo "${dir}|${size_kb}|${TODAY:-$(date +%Y-%m-%d)}" >> "$snapshot"
  done
fi
