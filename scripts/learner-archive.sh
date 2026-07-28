#!/usr/bin/env bash
# learner-archive.sh — Implements 3-tier retention for learner logs
# Tier 1 → Tier 2: runs/*.md older than 7 days → archive/YYYY-MM/runs.tar.gz
# Tier 2 → delete: tarballs older than 90 days → only if monthly summary exists
# Run on demand (housekeeping/report; no scheduler needed). Suggested cadence: Weekly Sunday 09:30.
# macOS bash 3.2 compatible

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RUNS_DIR="${WORKSPACE_ROOT}/data/logs/learner/runs"
ARCHIVE_DIR="${WORKSPACE_ROOT}/data/logs/learner/archive"
SUMMARIES_DIR="${WORKSPACE_ROOT}/data/logs/learner/summaries"
LOG_DIR="${WORKSPACE_ROOT}/data/logs"
TODAY="$(date +%Y-%m-%d)"
LOG_FILE="${LOG_DIR}/learner-archive-${TODAY}.md"

mkdir -p "$ARCHIVE_DIR"
mkdir -p "$SUMMARIES_DIR"
mkdir -p "$RUNS_DIR"

{
  echo "# Learner Archive Run — ${TODAY}"
  echo ""
  echo "## Tier 1 → Tier 2 (runs older than 7 days)"
  echo ""

  archived_count=0

  if [ -d "$RUNS_DIR" ]; then
    while IFS= read -r run_file; do
      if [ -z "$run_file" ]; then continue; fi

      # Determine which month this file belongs to (by modification date)
      file_month=$(stat -f '%Sm' -t '%Y-%m' "$run_file" 2>/dev/null)
      if [ -z "$file_month" ]; then continue; fi

      month_dir="${ARCHIVE_DIR}/${file_month}"
      tarball="${month_dir}/runs.tar.gz"
      mkdir -p "$month_dir"

      if [ -f "$tarball" ]; then
        # Extract existing tarball, add new file, recompress
        tmp_dir=$(mktemp -d)
        tar -xzf "$tarball" -C "$tmp_dir" 2>/dev/null || true
        cp "$run_file" "$tmp_dir/"
        tar -czf "$tarball" -C "$tmp_dir" .
        rm -rf "$tmp_dir"
      else
        # Create new tarball with this file
        tar -czf "$tarball" -C "$(dirname "$run_file")" "$(basename "$run_file")"
      fi

      rm "$run_file"
      archived_count=$((archived_count + 1))
      echo "- Archived: $(basename "$run_file") → ${file_month}/runs.tar.gz"

    done < <(find "$RUNS_DIR" -name "*.md" -type f -mtime +7 2>/dev/null)
  fi

  if [ "$archived_count" -eq 0 ]; then
    echo "- No files older than 7 days to archive"
  fi
  echo ""
  echo "Total archived: ${archived_count}"
  echo ""

  # --- Tier 2 → Delete ---
  echo "## Tier 2 → Delete (tarballs older than 90 days with summary)"
  echo ""

  deleted_count=0

  if [ -d "$ARCHIVE_DIR" ]; then
    while IFS= read -r tarball; do
      if [ -z "$tarball" ]; then continue; fi

      # Extract YYYY-MM from path
      month_name=$(basename "$(dirname "$tarball")")
      summary_file="${SUMMARIES_DIR}/${month_name}.md"

      if [ -f "$summary_file" ]; then
        rm "$tarball"
        # Remove empty month directory
        rmdir "$(dirname "$tarball")" 2>/dev/null || true
        deleted_count=$((deleted_count + 1))
        echo "- Deleted: ${month_name}/runs.tar.gz (summary exists)"
      else
        echo "- Kept: ${month_name}/runs.tar.gz (no summary yet)"
      fi
    done < <(find "$ARCHIVE_DIR" -name "runs.tar.gz" -type f -mtime +90 2>/dev/null)
  fi

  if [ "$deleted_count" -eq 0 ]; then
    echo "- No tarballs eligible for deletion"
  fi
  echo ""
  echo "Total deleted: ${deleted_count}"

} > "$LOG_FILE"

echo "[learner-archive] Done. Archived=${archived_count}, Deleted=${deleted_count}. Log: ${LOG_FILE}"
