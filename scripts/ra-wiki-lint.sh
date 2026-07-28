#!/usr/bin/env bash
# ra-wiki-lint.sh — Comprehensive wiki health check
# Checks: schema compliance, cross-reference integrity, source citations,
#          orphan detection, staleness, coverage gaps, image orphans
# Exit 0 = no errors (warnings OK). Exit 1 = errors found.
# Schedule: Weekly Sunday 09:15 (see crontab.example)
# macOS bash 3.2 compatible

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

errors=0
warnings=0
pages_checked=0

REQUIRED_FIELDS="type title maturity created applicable_to originating_space"

log_error() {
  echo "  ERROR: $1"
  errors=$((errors + 1))
}

log_warning() {
  echo "  WARNING: $1"
  warnings=$((warnings + 1))
}

check_frontmatter_field() {
  local file="$1"
  local field="$2"
  if ! grep -q "^${field}:" "$file" 2>/dev/null; then
    log_error "${file##${WORKSPACE_ROOT}/}: missing required field '${field}'"
  fi
}

echo "# Wiki Lint Report"
echo ""
echo "Workspace: ${WORKSPACE_ROOT}"
echo "Date: $(date +%Y-%m-%d)"
echo ""

# Collect all wiki directories
wiki_dirs=""
# Canonical wiki lives under src/research_assistant/spaces/*/wiki plus the
# shared tree. The bare spaces/*/wiki path at the workspace root is legacy and
# is intentionally NOT scanned (see two-tree reconciliation, 2026-07-27).
for d in "${WORKSPACE_ROOT}"/src/research_assistant/spaces/*/wiki "${WORKSPACE_ROOT}"/data/wiki/shared; do
  if [ -d "$d" ]; then
    wiki_dirs="${wiki_dirs} ${d}"
  fi
done

if [ -z "$wiki_dirs" ]; then
  echo "No wiki directories found. 0 pages checked."
  echo ""
  echo "## Summary"
  echo "- Pages checked: 0"
  echo "- Errors: 0"
  echo "- Warnings: 0"
  exit 0
fi

# --- 1. Schema Compliance ---
echo "## 1. Schema Compliance"
echo ""

for wiki_dir in $wiki_dirs; do
  while IFS= read -r page; do
    if [ -z "$page" ]; then continue; fi

    # Skip learner memory files (different structure, not wiki content pages)
    case "$page" in
      */learner/*) continue ;;
    esac

    pages_checked=$((pages_checked + 1))

    has_frontmatter=0
    if head -1 "$page" | grep -q "^---" 2>/dev/null; then
      has_frontmatter=1
    fi

    if [ "$has_frontmatter" -eq 0 ]; then
      log_error "${page##${WORKSPACE_ROOT}/}: no YAML frontmatter found"
      continue
    fi

    for field in $REQUIRED_FIELDS; do
      check_frontmatter_field "$page" "$field"
    done
  done < <(find "$wiki_dir" -name "*.md" -not -name "_*" -type f 2>/dev/null)
done

if [ "$pages_checked" -eq 0 ]; then
  echo "  No wiki pages found (excluding _index.md, _log.md, _schema.md)."
fi
echo ""

# --- 2. Cross-Reference Integrity ---
echo "## 2. Cross-Reference Integrity"
echo ""

ref_errors=0
for wiki_dir in $wiki_dirs; do
  while IFS= read -r page; do
    if [ -z "$page" ]; then continue; fi
    page_dir="$(dirname "$page")"

    while IFS= read -r ref_line; do
      if [ -z "$ref_line" ]; then continue; fi
      # Extract path from [[...]] links, then drop any |label suffix
      # ([[path|label]] is the Obsidian-style alias form used across the wiki).
      ref_path="$(echo "$ref_line" | sed 's/.*\[\[//;s/\]\].*//;s/|.*//')"
      if [ -z "$ref_path" ]; then continue; fi

      # Resolve the reference. Three forms appear in practice:
      #   /abs/path            -> absolute, use as-is
      #   src/... or data/...  -> workspace-relative, anchor at WORKSPACE_ROOT
      #   plain-name           -> page-relative, anchor at the page's directory
      case "$ref_path" in
        /*)                         target="$ref_path" ;;
        src/* | data/* | spaces/*)  target="${WORKSPACE_ROOT}/${ref_path}" ;;
        *)                          target="${page_dir}/${ref_path}" ;;
      esac

      # Add .md extension if missing
      case "$target" in
        *.md) ;;
        *) target="${target}.md" ;;
      esac

      if [ ! -f "$target" ]; then
        log_error "${page##${WORKSPACE_ROOT}/}: broken ref [[${ref_path}]] -> target not found"
        ref_errors=$((ref_errors + 1))
      fi
    done < <(grep -o '\[\[[^]]*\]\]' "$page" 2>/dev/null || true)
  done < <(find "$wiki_dir" -name "*.md" -type f 2>/dev/null)
done

if [ "$ref_errors" -eq 0 ]; then
  echo "  All cross-references resolve."
fi
echo ""

# --- 3. Source Citation Check ---
echo "## 3. Source Citation Check (working+ pages)"
echo ""

for wiki_dir in $wiki_dirs; do
  while IFS= read -r page; do
    if [ -z "$page" ]; then continue; fi
    case "$page" in */learner/*) continue ;; esac

    maturity=""
    if grep -q "^maturity: working" "$page" 2>/dev/null; then
      maturity="working"
    elif grep -q "^maturity: validated" "$page" 2>/dev/null; then
      maturity="validated"
    fi

    if [ -z "$maturity" ]; then continue; fi

    if ! grep -q "^sources:" "$page" 2>/dev/null; then
      log_warning "${page##${WORKSPACE_ROOT}/}: maturity '${maturity}' but no 'sources:' field"
    fi
  done < <(find "$wiki_dir" -name "*.md" -not -name "_*" -type f 2>/dev/null)
done

echo ""

# --- 4. Orphan Detection ---
echo "## 4. Orphan Detection (pages not in _index.md)"
echo ""

orphan_pages=0
for wiki_dir in $wiki_dirs; do
  index_file="${wiki_dir}/_index.md"
  if [ ! -f "$index_file" ]; then
    # Skip warning for shared/learner (no index expected)
    case "$wiki_dir" in
      */learner) ;;
      *) log_warning "${wiki_dir##${WORKSPACE_ROOT}/}: no _index.md found" ;;
    esac
    continue
  fi

  while IFS= read -r page; do
    if [ -z "$page" ]; then continue; fi
    case "$page" in */learner/*) continue ;; esac
    page_basename="$(basename "$page" .md)"
    if ! grep -q "$page_basename" "$index_file" 2>/dev/null; then
      log_warning "${page##${WORKSPACE_ROOT}/}: not listed in _index.md"
      orphan_pages=$((orphan_pages + 1))
    fi
  done < <(find "$wiki_dir" -name "*.md" -not -name "_*" -type f 2>/dev/null)
done

echo ""

# --- 5. Staleness Check ---
echo "## 5. Staleness Check (>90 days unmodified)"
echo ""

stale_count=0
for wiki_dir in $wiki_dirs; do
  while IFS= read -r page; do
    if [ -z "$page" ]; then continue; fi
    log_warning "${page##${WORKSPACE_ROOT}/}: not modified in 90+ days"
    stale_count=$((stale_count + 1))
  done < <(find "$wiki_dir" -name "*.md" -not -name "_*" -type f -mtime +90 2>/dev/null)
done

if [ "$stale_count" -eq 0 ]; then
  echo "  No stale pages found."
fi
echo ""

# --- 6. Coverage Gap ---
echo "## 6. Coverage Gap (knowledge/communication files without wiki source pages)"
echo ""

gap_count=0
# Driver iterates the CANONICAL tree (knowledge/communication dirs live only
# there). alt_wiki_source is the legacy fallback for the source-page lookup.
for space_dir in "${WORKSPACE_ROOT}"/src/research_assistant/spaces/*/; do
  if [ ! -d "$space_dir" ]; then continue; fi
  space_name="$(basename "$space_dir")"

  wiki_source_dir="${space_dir}wiki/sources"
  alt_wiki_source="${WORKSPACE_ROOT}/spaces/${space_name}/wiki/sources"

  for src_dir in "${space_dir}knowledge" "${space_dir}communication"; do
    if [ ! -d "$src_dir" ]; then continue; fi

    while IFS= read -r src_file; do
      if [ -z "$src_file" ]; then continue; fi
      src_basename="$(basename "$src_file")"

      # Skip non-content files
      case "$src_basename" in
        .DS_Store|*.tmp|README.md) continue ;;
      esac

      # Check if any wiki source page references this file
      found=0
      for check_dir in "$wiki_source_dir" "$alt_wiki_source"; do
        if [ -d "$check_dir" ]; then
          if grep -rl "$src_basename" "$check_dir" >/dev/null 2>&1; then
            found=1
            break
          fi
        fi
      done

      if [ "$found" -eq 0 ]; then
        log_warning "${src_file##${WORKSPACE_ROOT}/}: no corresponding wiki source page"
        gap_count=$((gap_count + 1))
      fi
    done < <(find "$src_dir" -type f \( -name "*.pdf" -o -name "*.docx" -o -name "*.md" -o -name "*.xlsx" -o -name "*.pptx" \) 2>/dev/null)
  done
done

if [ "$gap_count" -eq 0 ]; then
  echo "  All knowledge/communication files have corresponding wiki pages."
fi
echo ""

# --- 7. Image Orphan Check ---
echo "## 7. Image Orphan Check"
echo ""

orphan_image_script="${WORKSPACE_ROOT}/scripts/image-orphan-scan.sh"
if [ -x "$orphan_image_script" ] || [ -f "$orphan_image_script" ]; then
  orphan_img_count=0
  for img_dir in "${WORKSPACE_ROOT}"/src/research_assistant/spaces/*/communication/images; do
    if [ ! -d "$img_dir" ]; then continue; fi
    while IFS= read -r img; do
      if [ -z "$img" ]; then continue; fi
      img_name="$(basename "$img")"
      refs=$( (grep -rl "$img_name" "${WORKSPACE_ROOT}/src/research_assistant/spaces" "${WORKSPACE_ROOT}/data" 2>/dev/null || true) | wc -l | tr -d ' ')
      if [ "$refs" -eq 0 ]; then
        orphan_img_count=$((orphan_img_count + 1))
        log_warning "Orphan image: ${img##${WORKSPACE_ROOT}/}"
      fi
    done < <(find "$img_dir" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" \) -mtime +60 2>/dev/null)
  done
  if [ "$orphan_img_count" -eq 0 ]; then
    echo "  No orphan images found."
  fi
else
  echo "  image-orphan-scan.sh not found, skipping."
fi
echo ""

# --- Summary ---
echo "## Summary"
echo ""
echo "- Pages checked: ${pages_checked}"
echo "- Errors: ${errors}"
echo "- Warnings: ${warnings}"
echo "- Orphan pages: ${orphan_pages}"
echo "- Stale pages (>90d): ${stale_count}"
echo "- Coverage gaps: ${gap_count}"

if [ "$errors" -gt 0 ]; then
  echo ""
  echo "RESULT: FAIL (${errors} errors)"
  exit 1
fi

echo ""
echo "RESULT: PASS (${warnings} warnings)"
exit 0
