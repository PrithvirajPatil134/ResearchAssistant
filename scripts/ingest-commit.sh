#!/usr/bin/env bash
# ingest-commit.sh — Atomically commit merged wiki pages to the wiki tree.
#
# Usage:
#   bash scripts/ingest-commit.sh <id>
#
# Reads .kiro/.ingest-pending/{id}/merged/. Each file must contain a
# `target_path:` line in its YAML frontmatter specifying the destination
# relative to the workspace root.
#
# For validated pages: appends a Change Proposal block instead of overwriting.
# For seed/working pages: backs up to rollback/ then replaces.
# For new files: moves into place.
#
# On failure mid-commit: rolls back all prior file operations for this run.

set -eo pipefail

ID="${1:?Usage: ingest-commit.sh <id>}"

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PENDING_DIR="${WORKSPACE_ROOT}/.kiro/.ingest-pending/${ID}"

if [ ! -d "$PENDING_DIR" ]; then
  echo "error: ingest manifest not found: ${ID}" >&2
  exit 1
fi

MANIFEST="${PENDING_DIR}/manifest.json"
MERGED_DIR="${PENDING_DIR}/merged"
ROLLBACK_DIR="${PENDING_DIR}/rollback"

if [ ! -d "$MERGED_DIR" ]; then
  echo "error: merged/ directory not found for ${ID}" >&2
  exit 1
fi

MERGED_FILES=()
# Collect recursively: synthesizers may organize merged files flat OR under
# subdirs (sources/, methods/, syntheses/). find -type f handles both. The real
# destination is each file's frontmatter target_path, not its position here.
while IFS= read -r f; do
  [ -f "$f" ] || continue
  # Skip underscore-prefixed helper files (e.g. _index.md, _log_entry.md).
  # These are not content pages and carry no target_path: the wiki _index is
  # auto-rebuilt after commit, and _log_entry.md is appended to the space _log.
  case "$(basename "$f")" in
    _*) continue ;;
  esac
  MERGED_FILES+=("$f")
done < <(find "$MERGED_DIR" -type f -name '*.md' 2>/dev/null | sort)

if [ "${#MERGED_FILES[@]}" -eq 0 ]; then
  echo "error: no files in merged/ for ${ID}" >&2
  exit 1
fi

extract_target_path() {
  local file="$1"
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
  done < "$file"
  return 1
}

extract_maturity() {
  local file="$1"
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
        maturity:*)
          printf '%s' "$line" | sed 's/^maturity:[[:space:]]*//'
          return 0
          ;;
      esac
    fi
  done < "$file"
  printf 'unknown'
}

COMMITTED_TARGETS=()

rollback_all() {
  local count="${#COMMITTED_TARGETS[@]}"
  echo "Rolling back ${count} committed file(s)..." >&2
  if [ "$count" -eq 0 ]; then
    echo "Nothing to roll back." >&2
    return
  fi
  for target in "${COMMITTED_TARGETS[@]}"; do
    local basename_target
    basename_target="$(basename "$target")"
    local backup="${ROLLBACK_DIR}/${basename_target}"
    if [ -f "$backup" ]; then
      cp "$backup" "${WORKSPACE_ROOT}/${target}"
    else
      rm -f "${WORKSPACE_ROOT}/${target}"
    fi
  done
  # Update manifest status
  sed -i '' 's/"status": "initialized"/"status": "rolled_back"/' "$MANIFEST" 2>/dev/null || \
    sed -i 's/"status": "initialized"/"status": "rolled_back"/' "$MANIFEST" 2>/dev/null || true
  echo "Rollback complete." >&2
}

COMMIT_TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

for merged_file in "${MERGED_FILES[@]}"; do
  target_path="$(extract_target_path "$merged_file")" || {
    echo "error: no target_path in frontmatter of $(basename "$merged_file")" >&2
    rollback_all
    exit 1
  }

  full_target="${WORKSPACE_ROOT}/${target_path}"
  target_dir="$(dirname "$full_target")"

  mkdir -p "$target_dir"

  lock_dir="${target_dir}/.ingest-lock"
  lock_acquired=0
  for attempt in 1 2 3 4 5; do
    if mkdir "$lock_dir" 2>/dev/null; then
      lock_acquired=1
      break
    fi
    sleep 1
  done

  if [ "$lock_acquired" -eq 0 ]; then
    echo "error: could not acquire lock on ${target_dir}" >&2
    rollback_all
    exit 1
  fi

  commit_failed=0

  if [ -f "$full_target" ]; then
    existing_maturity="$(extract_maturity "$full_target")"

    if [ "$existing_maturity" = "validated" ]; then
      # Append as Change Proposal
      proposal_date="$(date +%Y-%m-%d)"
      {
        printf '\n## Change Proposal [%s]\n\n' "$proposal_date"
        printf '**Source**: ingest manifest %s\n\n' "$ID"
        # Strip frontmatter from merged file for the proposal body
        local_in_fm=0
        local_past_fm=0
        while IFS= read -r line; do
          if [ "$local_past_fm" -eq 1 ]; then
            printf '%s\n' "$line"
            continue
          fi
          if [ "$local_in_fm" -eq 0 ] && [ "$line" = "---" ]; then
            local_in_fm=1
            continue
          fi
          if [ "$local_in_fm" -eq 1 ] && [ "$line" = "---" ]; then
            local_past_fm=1
            continue
          fi
        done < "$merged_file"
      } >> "$full_target" || commit_failed=1
    else
      # Backup existing file then overwrite
      cp "$full_target" "${ROLLBACK_DIR}/$(basename "$full_target")" || commit_failed=1
      if [ "$commit_failed" -eq 0 ]; then
        cp "$merged_file" "$full_target" || commit_failed=1
      fi
    fi
  else
    # New file — just copy into place
    cp "$merged_file" "$full_target" || commit_failed=1
  fi

  rmdir "$lock_dir" 2>/dev/null || true

  if [ "$commit_failed" -ne 0 ]; then
    echo "error: failed to commit $(basename "$merged_file") to ${target_path}" >&2
    rollback_all
    exit 1
  fi

  COMMITTED_TARGETS+=("$target_path")
done

# Build committed_files JSON array for rollback reference
COMMITTED_JSON="["
first=1
for t in "${COMMITTED_TARGETS[@]}"; do
  if [ "$first" -eq 1 ]; then
    first=0
  else
    COMMITTED_JSON="${COMMITTED_JSON},"
  fi
  COMMITTED_JSON="${COMMITTED_JSON}\"${t}\""
done
COMMITTED_JSON="${COMMITTED_JSON}]"

# Update manifest with status, committed_at, and committed_files
if command -v python3 >/dev/null 2>&1; then
  python3 -c "
import json, sys
with open('${MANIFEST}', 'r') as f:
    m = json.load(f)
m['status'] = 'committed'
m['committed_at'] = '${COMMIT_TIMESTAMP}'
m['committed_files'] = json.loads('${COMMITTED_JSON}')
with open('${MANIFEST}', 'w') as f:
    json.dump(m, f, indent=2)
"
fi

# Clean up proposals/ and merged/ but keep manifest and decisions.log
rm -rf "$MERGED_DIR" "${PENDING_DIR}/proposals"

# --- Auto-heal wiki indexes for affected spaces (event-driven; no cron needed) ---
# Committing pages is the ONLY thing that drifts a space's _index.md, so rebuild
# it here, silently, for just the spaces we touched. Best-effort: a rebuild
# failure never fails the commit.
if [ -f "${WORKSPACE_ROOT}/scripts/rebuild-wiki-index.py" ]; then
  RA_PY="python3"
  [ -x "${WORKSPACE_ROOT}/.venv/bin/python3" ] && RA_PY="${WORKSPACE_ROOT}/.venv/bin/python3"
  AFFECTED_SPACES=""
  for t in "${COMMITTED_TARGETS[@]}"; do
    case "$t" in
      src/research_assistant/spaces/*/wiki/*)
        sp="$(printf '%s' "$t" | sed -E 's#^src/research_assistant/spaces/([^/]+)/wiki/.*#\1#')"
        case " $AFFECTED_SPACES " in *" $sp "*) : ;; *) AFFECTED_SPACES="$AFFECTED_SPACES $sp" ;; esac
        ;;
    esac
  done
  REBUILD_DATE="$(printf '%s' "$COMMIT_TIMESTAMP" | cut -dT -f1)"
  for sp in $AFFECTED_SPACES; do
    "$RA_PY" "${WORKSPACE_ROOT}/scripts/rebuild-wiki-index.py" "$sp" --date "$REBUILD_DATE" >/dev/null 2>&1 \
      && echo "  (index refreshed: ${sp})" || true
  done
fi

echo "Committed ${#COMMITTED_TARGETS[@]} file(s) for ingest ${ID}."
for t in "${COMMITTED_TARGETS[@]}"; do
  echo "  → ${t}"
done
