#!/usr/bin/env bash
# install-crontab.sh — Idempotently install the ResearchAssistant maintenance
# schedule (crontab.example) into the current user's crontab.
#
# The deterministic maintenance/learner tier only runs if scheduled. This wraps
# the RA jobs in a marked block so re-running replaces (not duplicates) them, and
# `--uninstall` removes them cleanly. Other (non-RA) crontab entries are preserved.
#
# Usage:
#   bash scripts/install-crontab.sh            # install / update the RA block
#   bash scripts/install-crontab.sh --dry-run  # show the resulting crontab, no change
#   bash scripts/install-crontab.sh --uninstall
#
# macOS bash 3.2 compatible.

set -uo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXAMPLE="${WORKSPACE_ROOT}/crontab.example"
BEGIN="# >>> ResearchAssistant maintenance (managed by install-crontab.sh) >>>"
END="# <<< ResearchAssistant maintenance <<<"

MODE="install"
case "${1:-}" in
  --dry-run) MODE="dry-run" ;;
  --uninstall) MODE="uninstall" ;;
  "") MODE="install" ;;
  *) echo "usage: install-crontab.sh [--dry-run|--uninstall]" >&2; exit 2 ;;
esac

if [ ! -f "$EXAMPLE" ]; then
  echo "error: ${EXAMPLE} not found" >&2
  exit 1
fi

# Ensure the cron log dir exists (jobs redirect here).
mkdir -p "${WORKSPACE_ROOT}/data/logs"

# Current crontab (empty if none).
CURRENT="$(crontab -l 2>/dev/null || true)"

# Strip any existing RA-managed block (between markers) to make this idempotent.
WITHOUT_BLOCK="$(printf '%s\n' "$CURRENT" | awk -v b="$BEGIN" -v e="$END" '
  $0==b {skip=1; next}
  $0==e {skip=0; next}
  skip!=1 {print}
')"

if [ "$MODE" = "uninstall" ]; then
  printf '%s\n' "$WITHOUT_BLOCK" | sed '/^$/N;/^\n$/D' | crontab -
  echo "Removed the ResearchAssistant crontab block. Remaining entries preserved."
  exit 0
fi

# Build the new block: the non-comment, non-blank schedule lines from the example.
BLOCK_LINES="$(grep -vE '^\s*#' "$EXAMPLE" | grep -vE '^\s*$')"

NEW_CRONTAB="$(printf '%s\n%s\n%s\n%s\n%s\n' \
  "$WITHOUT_BLOCK" "$BEGIN" "$BLOCK_LINES" "$END" | sed '/^$/N;/^\n$/D')"

if [ "$MODE" = "dry-run" ]; then
  echo "=== crontab that WOULD be installed (no change made) ==="
  printf '%s\n' "$NEW_CRONTAB"
  exit 0
fi

printf '%s\n' "$NEW_CRONTAB" | crontab -
echo "Installed the ResearchAssistant maintenance schedule."
echo "Verify with: crontab -l | sed -n '/ResearchAssistant maintenance/,/<<</p'"
echo "Logs will accumulate under data/logs/."
