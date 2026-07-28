#!/usr/bin/env bash
# ingest-rollback.sh — Restore any partial commits from an ingest manifest.
#
# Usage:
#   bash scripts/ingest-rollback.sh <id>
#
# Reads .kiro/.ingest-pending/{id}/rollback/ and restores backed-up files
# to their original wiki locations. Sets manifest status to rolled_back.

set -euo pipefail

ID="${1:?Usage: ingest-rollback.sh <id>}"

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PENDING_DIR="${WORKSPACE_ROOT}/.kiro/.ingest-pending/${ID}"

if [ ! -d "$PENDING_DIR" ]; then
  echo "error: ingest manifest not found: ${ID}" >&2
  exit 1
fi

MANIFEST="${PENDING_DIR}/manifest.json"
ROLLBACK_DIR="${PENDING_DIR}/rollback"
MERGED_DIR="${PENDING_DIR}/merged"

if [ ! -d "$ROLLBACK_DIR" ]; then
  echo "No rollback directory found for ${ID}. Nothing to restore." >&2
  exit 0
fi

restored=0

# Strategy for finding targets:
# 1. Check manifest.json for committed_files array (set by ingest-commit.sh)
# 2. If merged/ still exists, extract target_path from matching files
# 3. Fallback: search wiki tree by basename

get_target_from_manifest() {
  local basename_to_find="$1"
  if command -v python3 >/dev/null 2>&1; then
    python3 -c "
import json, os
with open('${MANIFEST}') as f:
    m = json.load(f)
for path in m.get('committed_files', []):
    if os.path.basename(path) == '${basename_to_find}':
        print(path)
        break
" 2>/dev/null
  fi
}

extract_target_path_from_merged() {
  local basename_to_find="$1"
  if [ -d "$MERGED_DIR" ]; then
    for f in "$MERGED_DIR"/*; do
      [ -f "$f" ] || continue
      if [ "$(basename "$f")" = "$basename_to_find" ]; then
        local in_frontmatter=0
        while IFS= read -r line; do
          if [ "$in_frontmatter" -eq 0 ] && [ "$line" = "---" ]; then
            in_frontmatter=1
            continue
          fi
          if [ "$in_frontmatter" -eq 1 ] && [ "$line" = "---" ]; then
            break
          fi
          if [ "$in_frontmatter" -eq 1 ]; then
            case "$line" in
              target_path:*)
                printf '%s' "$line" | sed 's/^target_path:[[:space:]]*//' | sed 's/^"//;s/"$//' | sed "s/^'//;s/'$//"
                return 0
                ;;
            esac
          fi
        done < "$f"
      fi
    done
  fi
  return 1
}

for backup_file in "$ROLLBACK_DIR"/*; do
  [ -f "$backup_file" ] || continue

  basename_file="$(basename "$backup_file")"
  target_path=""

  # Method 1: manifest committed_files
  target_path="$(get_target_from_manifest "$basename_file")"

  # Method 2: merged/ directory (if still present)
  if [ -z "$target_path" ]; then
    target_path="$(extract_target_path_from_merged "$basename_file")" || true
  fi

  # Method 3: search wiki tree
  if [ -z "$target_path" ]; then
    for wiki_root in "$WORKSPACE_ROOT"/src/research_assistant/spaces/*/wiki "$WORKSPACE_ROOT"/spaces/*/wiki "$WORKSPACE_ROOT"/data/wiki/shared; do
      if [ -d "$wiki_root" ]; then
        match="$(find "$wiki_root" -name "$basename_file" -type f 2>/dev/null | head -1)"
        if [ -n "$match" ]; then
          target_path="${match#"$WORKSPACE_ROOT"/}"
          break
        fi
      fi
    done
  fi

  if [ -n "$target_path" ]; then
    full_target="${WORKSPACE_ROOT}/${target_path}"
    cp "$backup_file" "$full_target"
    echo "  restored: ${target_path}"
    restored=$((restored + 1))
  else
    echo "  warning: could not find target for ${basename_file}, left in rollback/" >&2
  fi
done

# Update manifest status
if command -v python3 >/dev/null 2>&1; then
  python3 -c "
import json
with open('${MANIFEST}', 'r') as f:
    m = json.load(f)
m['status'] = 'rolled_back'
with open('${MANIFEST}', 'w') as f:
    json.dump(m, f, indent=2)
"
else
  sed -i '' 's/"status": "[^"]*"/"status": "rolled_back"/' "$MANIFEST" 2>/dev/null || \
    sed -i 's/"status": "[^"]*"/"status": "rolled_back"/' "$MANIFEST" 2>/dev/null || true
fi

echo "Rollback complete for ${ID}: ${restored} file(s) restored."
