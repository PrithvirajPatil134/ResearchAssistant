---
name: ingest
description: Ingest a source (paper, email, feedback, image) into the wiki knowledge base via the atomic proposal-synthesize-review-commit pipeline.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
---

# Wiki ingest

Manual-only (`/ingest`). This mutates the wiki (creates/updates pages under
`spaces/{SPACE}/wiki/` or `data/wiki/shared/`). The user controls when knowledge
is committed, so never auto-run it.

## Source of truth

- `docs/knowledge_base_design.md` — the ingest operation, page types, what each
  source kind (paper / communication / feedback) updates.
- `data/wiki/_shared_schema.md` — frontmatter, maturity states, naming,
  cross-reference rules, the entity-page creation test.
- `WORKFLOW_GUIDE.md` (ingest pipeline section) — the atomic flow and agents.
- The scripts govern: `ingest-init.sh`, `ingest-commit.sh`, `ingest-rollback.sh`,
  `ingest-cleanup.sh`.

## The atomic flow (never write the wiki directly)

```
1. bash scripts/ingest-init.sh "<task-description>"        → prints an ingest id, creates .kiro/.ingest-pending/{id}/
2. ra-wiki-ingestor  (one per source)   → writes proposals to  {id}/proposals/
3. ra-synthesizer                        → merges proposals to  {id}/merged/
4. ra-wiki-reviewer                      → validates schema, cross-refs, sourcing
5. bash scripts/ingest-commit.sh <id>    → atomic batch-rename into the wiki
   (on failure: bash scripts/ingest-rollback.sh <id>)
```

Dispatch the `ra-*` agents via the Agent tool (they inherit 1M context). Only
`ra-orchestrator` should fan out sub-agents if orchestrating; researchers do not
call librarians directly.

## Hard rules

- Every wiki claim must cite a source per `.kiro/steering/no-assumption-rule.md`.
  Unsourced content is rejected by `ra-wiki-reviewer` — do not commit past it.
- Deduplicate first: check existing `wiki/sources/` by author-year and
  `data/summaries/` by title before creating a new page.
- Entity pages only for entities with relational/operational presence, NOT for
  cited-paper authors (schema's entity-creation test).
- Proposal model protects `validated` pages; `seed`/`working` pages edit in place.
- Raw sources in `knowledge/`, `communication/`, `feedback/` are immutable — read
  only. The wiki is derived content.

## After committing

Run `bash scripts/ra-wiki-lint.sh` to catch orphans, broken cross-refs, and
coverage gaps introduced by the new pages.
