---
name: consensus-search
description: Systematic academic paper discovery via the Consensus MCP tool. Use when the user asks to find papers, fill gaps in a catalogue or literature review, verify whether a paper exists, check what the literature says about a construct, or identify validated measurement instruments.
allowed-tools: Read, Glob, Grep
---

# Consensus academic search

Run a systematic, constraint-compliant Consensus search. This skill is a thin
entry point: the authoritative procedure and constraints already live in the
workspace steering files. Follow them exactly rather than improvising.

## Before searching — read the sources of truth

1. `.kiro/steering/consensus-research-tool.md` — hard constraints: what you may
   and may NOT cite from an abstract, evidence-level tagging (`source_origin:
   consensus_abstract`), the deduplication mandate, and quality filtering rules.
2. `.kiro/steering/consensus-search-sop.md` — the 9-step SOP: define objective,
   construct queries (≥3 complementary, lead with construct names), execute,
   triage against inclusion/exclusion criteria, deduplicate against existing
   wiki + `data/summaries/`, extract metadata, persist output.

These files govern. If anything here conflicts with them, they win.

## Non-negotiable rules (from the steering files)

- Abstracts are the MINIMUM evidence level. Never cite effect sizes, scale items,
  methodology detail, or limitations unless the abstract states them verbatim.
  Mark abstract-derived claims `[Abstract-only; full text required for detail]`.
- Never fabricate a field. If the abstract does not state it, write
  `[Not stated in abstract]`. Obey `.kiro/steering/no-assumption-rule.md`.
- Never write a synthesis ("five studies found X") from abstracts alone — that
  requires full-text verification. Report existence only, with citations.
- Deduplicate before creating anything: check `spaces/{SPACE}/wiki/sources/` by
  first-author+year, `data/summaries/` by title keyword, and prior
  `data/drafts/consensus-search-*.md` logs.
- Quality gate: `sjr_max=2` as a Q1–Q2 proxy; flag ABDC ratings `[ABDC: VERIFY]`,
  never auto-assign. Relevance to the research question beats citation prestige.
- After each batch, state coverage limits: working papers, books, and
  non-indexed proceedings are not covered by Consensus.

## Rate limits

One query at a time, max 7 per session. 10 results per query (free tier) — use
multiple complementary queries and dedup across batches.

## Output

- Interactive: present the results table from SOP Step 7 and ask which papers to
  promote to wiki seeds or log for later.
- Wiki seeds only on explicit user approval (SOP Step 8 format).
