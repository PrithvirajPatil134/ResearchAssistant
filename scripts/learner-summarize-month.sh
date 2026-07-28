#!/usr/bin/env bash
# learner-summarize-month.sh — Monthly summary of learner logs
# Processes the month that just ended (previous month)
# Writes: data/logs/learner/summaries/YYYY-MM.md (≤10KB)
# Run on demand (housekeeping/report; no scheduler needed). Suggested cadence: 1st of month 03:00.
# macOS bash 3.2 compatible

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ARCHIVE_DIR="${WORKSPACE_ROOT}/data/logs/learner/archive"
SUMMARIES_DIR="${WORKSPACE_ROOT}/data/logs/learner/summaries"

mkdir -p "$SUMMARIES_DIR"

# Determine the previous month
if date -v-1m +%Y-%m >/dev/null 2>&1; then
  PREV_MONTH=$(date -v-1m +%Y-%m)
else
  PREV_MONTH=$(date -d '1 month ago' +%Y-%m)
fi

TARBALL="${ARCHIVE_DIR}/${PREV_MONTH}/runs.tar.gz"
OUTPUT="${SUMMARIES_DIR}/${PREV_MONTH}.md"

if [ -f "$OUTPUT" ]; then
  echo "[learner-summarize-month] Summary for ${PREV_MONTH} already exists. Skipping."
  exit 0
fi

{
  echo "# Learner Summary — ${PREV_MONTH}"
  echo ""
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""

  if [ ! -f "$TARBALL" ]; then
    echo "## No Data"
    echo ""
    echo "No archived runs found for ${PREV_MONTH}."
    echo "This month may not have had any learner runs, or the archive has not been created yet."
  else
    # Extract tarball to temp dir for analysis
    tmp_dir=$(mktemp -d)
    tar -xzf "$TARBALL" -C "$tmp_dir" 2>/dev/null || true

    total_runs=$(find "$tmp_dir" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')

    echo "## Overview"
    echo ""
    echo "- Total runs: ${total_runs}"

    # Count pass/fail by scanning for score indicators
    pass_count=0
    fail_count=0
    for f in "$tmp_dir"/*.md; do
      if [ ! -f "$f" ]; then continue; fi
      if grep -qi "pass\|score.*[89]\|score.*10" "$f" 2>/dev/null; then
        pass_count=$((pass_count + 1))
      elif grep -qi "fail\|score.*[0-4]\|retry\|escalat" "$f" 2>/dev/null; then
        fail_count=$((fail_count + 1))
      fi
    done

    if [ "$total_runs" -gt 0 ]; then
      pass_rate=$(( (pass_count * 100) / total_runs ))
      echo "- Estimated pass rate: ${pass_rate}% (${pass_count}/${total_runs})"
      echo "- Estimated failures: ${fail_count}"
    fi
    echo ""

    echo "## Top Patterns"
    echo ""

    # Extract patterns mentioned across runs (look for Trigger/Diagnosis/Action blocks)
    patterns_file=$(mktemp)
    for f in "$tmp_dir"/*.md; do
      if [ ! -f "$f" ]; then continue; fi
      grep -i "trigger\|pattern\|lesson" "$f" 2>/dev/null >> "$patterns_file" || true
    done

    if [ -s "$patterns_file" ]; then
      # Show top 5 most common pattern keywords
      echo "Frequently mentioned patterns:"
      echo ""
      sort "$patterns_file" | uniq -c | sort -rn | head -5 | while read -r count line; do
        echo "- (${count}x) ${line}"
      done
    else
      echo "- No structured patterns extracted from this month's runs"
    fi
    rm -f "$patterns_file"
    echo ""

    echo "## Failures That Did Not Repeat"
    echo ""

    # Look for unique failure patterns (appear only once)
    failures_file=$(mktemp)
    for f in "$tmp_dir"/*.md; do
      if [ ! -f "$f" ]; then continue; fi
      grep -i "fail\|error\|retry" "$f" 2>/dev/null >> "$failures_file" || true
    done

    if [ -s "$failures_file" ]; then
      sort "$failures_file" | uniq -c | sort -n | head -3 | while read -r count line; do
        if [ "$count" -eq 1 ]; then
          echo "- ${line}"
        fi
      done
    else
      echo "- No failure patterns found"
    fi
    rm -f "$failures_file"

    # Cleanup temp dir
    rm -rf "$tmp_dir"
  fi

} > "$OUTPUT"

# Enforce ≤10KB cap
output_size=$(wc -c < "$OUTPUT" | tr -d ' ')
if [ "$output_size" -gt 10240 ]; then
  # Truncate to 10KB with a note at the end
  head -c 10000 "$OUTPUT" > "${OUTPUT}.tmp"
  echo "" >> "${OUTPUT}.tmp"
  echo "[TRUNCATED: summary exceeded 10KB cap]" >> "${OUTPUT}.tmp"
  mv "${OUTPUT}.tmp" "$OUTPUT"
fi

echo "[learner-summarize-month] Summary written to ${OUTPUT}"
