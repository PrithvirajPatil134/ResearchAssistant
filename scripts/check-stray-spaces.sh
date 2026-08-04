#!/usr/bin/env bash
# check-stray-spaces.sh — deterministic guard against the stray-tree bug.
#
# WHY THIS EXISTS (2026-08-03): The canonical spaces root is
# `src/research_assistant/spaces/` (config.py / ARCHITECTURE.md line 679:
# `spaces_dir: src/research_assistant/spaces`). But README.md, ARCHITECTURE.md,
# and WORKFLOW_GUIDE.md write the output path in shorthand as
# `spaces/{SPACE}/output/...`. An agent following the docs literally creates a
# REAL directory `spaces/` at the repo root, and deliverables silently land
# there instead of the canonical tree (and are git-ignored, so they never get
# committed). This happened to the Prashar candidate-dimensions v1/v2 docs.
#
# The fix is a repo-root symlink `spaces -> src/research_assistant/spaces`, so
# the doc-literal path resolves to the canonical tree. This guard FAILS LOUDLY
# if that symlink is ever replaced by a real directory (i.e. the bug recurs).
#
# Usage: scripts/check-stray-spaces.sh
# Exit: 0 = clean (symlink intact, or absent with no stray tree)
#       1 = FAIL: a real `spaces/` directory exists at repo root (stray tree)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANONICAL="src/research_assistant/spaces"
LINK="$REPO_ROOT/spaces"

# Case 1: no `spaces` entry at root at all — nothing stray, symlink just missing.
if [ ! -e "$LINK" ] && [ ! -L "$LINK" ]; then
  echo "WARN: repo-root 'spaces' symlink is missing. Recreate with:" >&2
  echo "  ln -s $CANONICAL spaces" >&2
  echo "(Not a failure: no stray tree exists. But doc-literal 'spaces/...' writes will create one.)" >&2
  exit 0
fi

# Case 2: it's a symlink — verify it points at the canonical tree.
if [ -L "$LINK" ]; then
  target="$(readlink "$LINK")"
  if [ "$target" = "$CANONICAL" ]; then
    echo "PASS: repo-root 'spaces' -> $CANONICAL (canonical, no stray tree)."
    exit 0
  fi
  echo "FAIL: repo-root 'spaces' symlink points at '$target', expected '$CANONICAL'." >&2
  exit 1
fi

# Case 3: it's a REAL directory — this is the bug.
echo "FAIL: '$LINK' is a real directory, not the expected symlink to $CANONICAL." >&2
echo "This is the stray-tree bug: deliverables written here bypass the canonical" >&2
echo "tree and are git-ignored. Move its contents into $CANONICAL and replace it" >&2
echo "with the symlink:" >&2
echo "  # move real files, then:" >&2
echo "  rm -rf spaces && ln -s $CANONICAL spaces" >&2
echo "" >&2
echo "Files currently stranded:" >&2
find "$LINK" -type f ! -name ".DS_Store" 2>/dev/null | sed 's/^/  /' >&2
exit 1
