#!/usr/bin/env bash
# scratchpad-archive.sh — Archive session scratchpads older than 90 days
# Moves data/drafts/ide_session_*.md → data/drafts/archive/YYYY/ (gzipped)
# Run on demand (housekeeping/report; no scheduler needed). Suggested cadence: Weekly Sunday 09:45.
# macOS bash 3.2 compatible

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DRAFTS_DIR="${WORKSPACE_ROOT}/data/drafts"
ARCHIVE_BASE="${DRAFTS_DIR}/archive"

archived_count=0

if [ ! -d "$DRAFTS_DIR" ]; then
  echo "[scratchpad-archive] No drafts directory found. Nothing to do."
  exit 0
fi

while IFS= read -r scratchpad; do
  if [ -z "$scratchpad" ]; then continue; fi

  # Extract year from the file's modification date
  file_year=$(stat -f '%Sm' -t '%Y' "$scratchpad" 2>/dev/null)
  if [ -z "$file_year" ]; then continue; fi

  year_dir="${ARCHIVE_BASE}/${file_year}"
  mkdir -p "$year_dir"

  basename_file="$(basename "$scratchpad")"
  gzip -c "$scratchpad" > "${year_dir}/${basename_file}.gz"
  rm "$scratchpad"
  archived_count=$((archived_count + 1))

done < <(find "$DRAFTS_DIR" -maxdepth 1 -name "ide_session_*.md" -type f -mtime +90 2>/dev/null)

echo "[scratchpad-archive] Archived ${archived_count} scratchpad(s)."
