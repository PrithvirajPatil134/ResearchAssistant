#!/usr/bin/env python3
"""
rebuild-wiki-index.py — Regenerate a space wiki's _index.md from actual pages.

The _index.md catalog drifts out of sync with the filesystem (pages get added
without updating the index). A stale index is a reliability hazard: anything that
trusts it (instead of the filesystem) sees a false "empty wiki". This script
rebuilds the section counts and tables deterministically from the real page
frontmatter, so the index always reflects what is on disk.

Usage:
    python3 scripts/rebuild-wiki-index.py QNTR              # one space
    python3 scripts/rebuild-wiki-index.py --all             # all spaces
    python3 scripts/rebuild-wiki-index.py QNTR --dry-run    # preview, no write

Run with the project venv (needs pyyaml): .venv/bin/python3 scripts/rebuild-wiki-index.py --all

Only the per-type sections (Sources/Concepts/Entities/Syntheses/Methods/
Comparisons) and the header "Last updated" are rewritten. The "Recently Updated",
"Validation Tests", and any other prose sections are preserved verbatim.
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("error: PyYAML not available. Run via the project venv: "
          ".venv/bin/python3 scripts/rebuild-wiki-index.py", file=sys.stderr)
    sys.exit(1)

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SPACES_DIR = WORKSPACE_ROOT / "src" / "research_assistant" / "spaces"
SPACES = ["QNTR", "CRO", "DBA", "CW"]

# Section order and the page-type subdir each maps to.
SECTIONS = [
    ("Sources", "sources"),
    ("Concepts", "concepts"),
    ("Entities", "entities"),
    ("Syntheses", "syntheses"),
    ("Methods", "methods"),
    ("References", "references"),
    ("Comparisons", "comparisons"),
]


def read_frontmatter(path):
    """Return the parsed YAML frontmatter dict for a page (empty dict if none)."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    try:
        data = yaml.safe_load(block)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def fmt_authors(authors):
    if isinstance(authors, list):
        return ", ".join(str(a) for a in authors) if authors else "—"
    return str(authors) if authors else "—"


def render_row(kind, slug, fm):
    """Render one markdown table row for the given page kind."""
    link = f"[{slug}](./{kind}/{slug}.md)"
    mat = fm.get("maturity", "seed")
    if kind == "sources":
        tags = fm.get("tags") or []
        tag_s = ", ".join(str(t) for t in tags) if isinstance(tags, list) else str(tags)
        return f"| {link} | {fmt_authors(fm.get('authors'))} | {fm.get('year','—')} | {mat} | {tag_s or '—'} |"
    if kind == "concepts":
        aliases = fm.get("aliases") or []
        alias_s = ", ".join(aliases) if isinstance(aliases, list) else str(aliases)
        srcs = fm.get("sources") or []
        nsrc = len(srcs) if isinstance(srcs, list) else "—"
        return f"| {link} | {alias_s or '—'} | {nsrc} | {mat} |"
    if kind == "entities":
        return f"| {link} | {fm.get('entity_kind','—')} | {fm.get('role','—')} | {mat} |"
    if kind == "syntheses":
        return f"| {link} | {fm.get('target_deliverable', fm.get('title','—'))} | {fm.get('current_version','—')} | {mat} |"
    # methods, comparisons: simple
    return f"| {link} | {fm.get('title','—')} | {mat} |"


HEADERS = {
    "sources": "| Page | Authors | Year | Maturity | Tags |\n|------|---------|------|----------|------|",
    "concepts": "| Page | Aliases | Sources | Maturity |\n|------|---------|---------|----------|",
    "entities": "| Page | Kind | Role | Maturity |\n|------|------|------|----------|",
    "syntheses": "| Page | Target Deliverable | Current Version | Maturity |\n|------|-------------------|-----------------|----------|",
    "methods": "| Page | Title | Maturity |\n|------|-------|----------|",
    "references": "| Page | Title | Maturity |\n|------|-------|----------|",
    "comparisons": "| Page | Title | Maturity |\n|------|-------|----------|",
}
EMPTY_NOTE = {
    "sources": "_No source pages yet._",
    "concepts": "_No concept pages yet._",
    "entities": "_No entity pages yet._",
    "syntheses": "_No synthesis pages yet._",
    "methods": "_No method pages yet._",
    "references": "_No reference pages yet._",
    "comparisons": "_No comparison pages yet._",
}


def build_section(wiki_dir, label, kind):
    """Return (section_markdown, count) for one page type."""
    subdir = wiki_dir / kind
    pages = sorted(subdir.glob("*.md")) if subdir.is_dir() else []
    pages = [p for p in pages if not p.name.startswith("_")]
    count = len(pages)
    lines = [f"## {label} ({count})", ""]
    if count == 0:
        lines.append(EMPTY_NOTE[kind])
    else:
        lines.append(HEADERS[kind])
        for p in pages:
            lines.append(render_row(kind, p.stem, read_frontmatter(p)))
    lines.append("")
    return "\n".join(lines), count


def rebuild(space, dry_run=False, today="unknown"):
    wiki_dir = SPACES_DIR / space / "wiki"
    idx = wiki_dir / "_index.md"
    if not idx.is_file():
        print(f"  {space}: no _index.md, skipping")
        return False
    original = idx.read_text(encoding="utf-8")

    # Preserve everything before the first "## Sources" (header/preamble) and
    # everything from "## Recently Updated" onward (prose tail).
    head_end = original.find("## Sources")
    tail_start = original.find("## Recently Updated")
    if head_end == -1:
        print(f"  {space}: no '## Sources' anchor, skipping (non-standard index)")
        return False
    head = original[:head_end].rstrip() + "\n\n"
    tail = ("\n" + original[tail_start:]) if tail_start != -1 else "\n"

    body_parts, counts = [], {}
    for label, kind in SECTIONS:
        sec, n = build_section(wiki_dir, label, kind)
        body_parts.append(sec)
        counts[label] = n
    # separator before the preserved tail
    new = head + "\n".join(body_parts) + "\n---\n" + tail.lstrip("\n")
    # refresh "Last updated" if present
    import re
    new = re.sub(r"\*\*Last updated\*\*:.*", f"**Last updated**: {today} (auto-rebuilt)", new, count=1)

    summary = ", ".join(f"{k}={v}" for k, v in counts.items() if v)
    if dry_run:
        print(f"  {space}: would rebuild — {summary or 'all empty'}")
        return False
    idx.write_text(new, encoding="utf-8")
    print(f"  {space}: rebuilt — {summary or 'all empty'}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("space", nargs="?", help="space name (QNTR/CRO/DBA/CW)")
    ap.add_argument("--all", action="store_true", help="rebuild all spaces")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--date", default="unknown", help="date string for 'Last updated'")
    args = ap.parse_args()

    targets = SPACES if args.all else ([args.space] if args.space else [])
    if not targets:
        ap.error("provide a space name or --all")
    print(f"Rebuilding wiki index(es): {', '.join(targets)}")
    for sp in targets:
        rebuild(sp, dry_run=args.dry_run, today=args.date)


if __name__ == "__main__":
    main()
