#!/usr/bin/env bash
# ra-manifest-cleanup.sh — Move stale ingest manifests to archive
# Scans .kiro/.ingest-pending/ for manifests older than 7 days.
# Moves them to .kiro/.ingest-archive/ (not delete).
# Run on demand (housekeeping/report; no scheduler needed). Suggested cadence: Weekly Sunday 09:30.
# macOS bash 3.2 compatible

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PENDING_DIR="${WORKSPACE_ROOT}/.kiro/.ingest-pending"
ARCHIVE_DIR="${WORKSPACE_ROOT}/.kiro/.ingest-archive"

NOW_EPOCH="$(date +%s)"
SEVEN_DAYS=$((7 * 86400))

moved_count=0

if [ ! -d "$PENDING_DIR" ]; then
  echo "[ra-manifest-cleanup] No .kiro/.ingest-pending/ directory. Nothing to clean."
  exit 0
fi

mkdir -p "$ARCHIVE_DIR"

for manifest_dir in "$PENDING_DIR"/*/; do
  [ -d "$manifest_dir" ] || continue

  dir_name="$(basename "$manifest_dir")"

  # Skip non-directory entries
  case "$dir_name" in
    README.md|.) continue ;;
  esac

  # Get directory age from modification time
  if stat -f '%m' "$manifest_dir" >/dev/null 2>&1; then
    mod_epoch=$(stat -f '%m' "$manifest_dir")
  else
    mod_epoch=$(stat -c '%Y' "$manifest_dir" 2>/dev/null || echo "$NOW_EPOCH")
  fi

  age=$((NOW_EPOCH - mod_epoch))

  if [ "$age" -ge "$SEVEN_DAYS" ]; then
    mv "$manifest_dir" "${ARCHIVE_DIR}/${dir_name}"
    echo "  Archived: ${dir_name} (age: $((age / 86400)) days)"
    moved_count=$((moved_count + 1))
  fi
done

echo "[ra-manifest-cleanup] Moved ${moved_count} manifest(s) to .kiro/.ingest-archive/"
exit 0
