#!/usr/bin/env bash
# image-orphan-scan.sh — Detect unreferenced images older than 60 days
# Writes report to: data/logs/orphan-images-YYYY-MM-DD.md
# Does NOT auto-delete. Report only.
# Run on demand (housekeeping/report; no scheduler needed). Suggested cadence: Weekly Sunday 09:45.
# macOS bash 3.2 compatible

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TODAY="$(date +%Y-%m-%d)"
LOG_DIR="${WORKSPACE_ROOT}/data/logs"
OUTPUT="${LOG_DIR}/orphan-images-${TODAY}.md"

mkdir -p "$LOG_DIR"

orphan_count=0
total_size=0

{
  echo "# Orphan Image Scan — ${TODAY}"
  echo ""
  echo "Images in \`spaces/*/communication/images/\` that are:"
  echo "- Older than 60 days"
  echo "- Not referenced in any wiki page, scratchpad, or markdown file"
  echo ""
  echo "## Results"
  echo ""

  found_any=0

  for img_dir in "${WORKSPACE_ROOT}"/src/research_assistant/spaces/*/communication/images; do
    if [ ! -d "$img_dir" ]; then continue; fi

    space_name="$(basename "$(dirname "$(dirname "$img_dir")")")"

    while IFS= read -r img; do
      if [ -z "$img" ]; then continue; fi
      found_any=1

      img_name="$(basename "$img")"
      img_size=$(du -sh "$img" 2>/dev/null | cut -f1)
      img_size_kb=$(du -sk "$img" 2>/dev/null | cut -f1)

      # Search for references in wiki pages, drafts, and communication markdown
      refs=$(grep -rl "$img_name" \
        "${WORKSPACE_ROOT}/src/research_assistant/spaces" \
        "${WORKSPACE_ROOT}/data/drafts" \
        "${WORKSPACE_ROOT}/data/wiki" \
        2>/dev/null | grep -v "$(basename "$img")" | wc -l | tr -d ' ')

      if [ "$refs" -eq 0 ]; then
        orphan_count=$((orphan_count + 1))
        total_size=$((total_size + img_size_kb))
        echo "- \`${space_name}/communication/images/${img_name}\` — ${img_size}"
      fi

    done < <(find "$img_dir" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" \) -mtime +60 2>/dev/null)
  done

  if [ "$found_any" -eq 0 ]; then
    echo "No image directories found or no images older than 60 days."
  elif [ "$orphan_count" -eq 0 ]; then
    echo "All images older than 60 days are referenced. No orphans."
  fi

  echo ""
  echo "## Summary"
  echo ""
  echo "- Orphan images found: ${orphan_count}"
  echo "- Total orphan size: ${total_size}KB"
  echo "- Action: Manual review recommended. No auto-deletion."

} > "$OUTPUT"

if [ "$orphan_count" -gt 0 ]; then
  echo "[image-orphan-scan] Found ${orphan_count} orphan image(s). Report: ${OUTPUT}"
else
  echo "[image-orphan-scan] No orphans found. Report: ${OUTPUT}"
fi
