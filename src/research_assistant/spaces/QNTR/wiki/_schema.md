# QNTR Wiki Schema

**Status**: Draft. Co-evolved with wiki content. Last updated 2026-05-06.

This file defines the conventions for the QNTR wiki. Every agent, human, or workflow that writes to this wiki must read this file first.

Related: [`docs/knowledge_base_design.md`](../../../../../docs/knowledge_base_design.md), [`docs/multi_agent_knowledge_patterns_reference.md`](../../../../../docs/multi_agent_knowledge_patterns_reference.md).

---

## Directory Layout

```
wiki/
├── _schema.md       # This file. Conventions.
├── _index.md        # Content catalog. Every page must be listed here.
├── _log.md          # Chronological append-only operation log.
│
├── sources/         # One page per ingested source (paper, book, slide deck)
├── concepts/        # One page per key concept that appears across sources
├── entities/        # One page per recurring person, org, framework, dataset
├── syntheses/       # Cross-source analysis pages, research arguments
├── methods/         # Methodology reference pages (SEM, regression, coding)
└── comparisons/     # Head-to-head source comparisons
```

## Page Types

| Type | When to create | One-per |
|------|----------------|---------|
| source | A PDF, paper, book, or slide deck is ingested into `knowledge/` | Source artifact |
| concept | A concept appears in 2+ sources | Concept |
| entity | A person, org, framework, or dataset is referenced across the research | Entity |
| synthesis | Multi-source argument or gap identified during research | Research thread |
| method | A statistical or analytical method is used in the research | Method |
| comparison | Two or more sources address the same question differently | Question-pair |

## Naming Conventions

- **Files**: kebab-case, lowercase. `berente-2021-managing-ai.md`, not `Berente_2021.md`.
- **Source pages**: `{first-author-lastname}-{year}-{short-slug}.md`. Example: `jarrahi-2025-principal-agent.md`.
- **Concept pages**: kebab-case concept name. `principal-agent-theory.md`, `shadow-ai.md`.
- **Entity pages**: kebab-case entity name. Person: `prof-prashar.md`. Org: `iim-sambalpur.md`. Dataset: `hatco-dataset.md`.
- **Synthesis pages**: kebab-case research thread. `agentic-ai-governance-term-paper.md`, `rpa-to-agentic-ai-gap.md`.
- **Method pages**: kebab-case method name. `sem-structural-equation-modeling.md`, `qualitative-interview-coding.md`.
- **Comparison pages**: `{source-a}-vs-{source-b}-{topic}.md`. Example: `berente-vs-taeihagh-risk-taxonomies.md`.

## Frontmatter

Every page starts with YAML frontmatter. Fields vary by type. Common fields across all types:

| Field | Required | Notes |
|-------|----------|-------|
| type | Yes | source, concept, entity, synthesis, method, comparison |
| title | Yes | Human-readable title in quotes |
| maturity | Yes | seed, working, validated, deprecated |
| tags | Yes | Array of kebab-case tags for faceted search |
| created | No | ISO date. Auto-filled on creation. |
| last_updated | No | ISO date. Auto-filled on update. |

### Type-specific fields

**source**: authors, year, journal, volume, pages, source_path, ingested, related.
**concept**: aliases, first_seen, sources.
**entity**: entity_kind (person, organization, framework, dataset), aliases, role, institution, relationship_to_user, mentions_in_sources, mentions_in_syntheses, mentions_in_communications, cross_space_presence.
**synthesis**: sources, propositions_supported, created, last_updated.
**method**: sources.
**comparison**: sources.

See `entities/prof-prashar.md` for a complete entity frontmatter example.

## Maturity States

| State | Meaning | Transition criteria |
|-------|---------|---------------------|
| seed | Initial extraction, single source, not cross-referenced | Default on creation |
| working | Multiple sources contribute, cross-references built | 2+ sources reference it, or updated by a second run |
| validated | Reviewed by user or confirmed against source material | User approval, or ReviewerAgent verification |
| deprecated | Superseded or found incorrect | Flagged during lint, confirmed by user. Kept for audit. |

Query behavior prefers `validated` pages, uses `working` with caveat, ignores `deprecated`, includes `seed` only when no better source exists.

## Cross-References

- Use relative paths from the page's directory: `../concepts/shadow-ai.md`.
- All `related`, `sources`, `mentions_in_*` fields must point to existing pages. Lint checks this.
- A missing cross-reference target is an error, not a warning.

## Page Structure Conventions

Each page type has required sections. The ingest operation and wiki-ingestor agent must produce these sections, in this order.

### Source page
1. Core Argument
2. Methodology
3. Key Findings (with page references, format: `p.7, Section 3.2`)
4. Relevance to Current Research
5. Limitations
6. Open Questions

### Concept page
1. Definition
2. How Different Sources Define It
3. Evidence (with citations, format: `[Berente et al., 2021, p.1437]`)
4. Tensions and Debates
5. Connections to Other Concepts

### Entity page (person)
1. Identity (role, institution, how we work together)
2. Communication History (one entry per interaction, with substance, not just "we talked")
3. Key Guidance (what they have actually said)
4. Preferences (inferred from interactions, not invented)
5. Cross-Space Presence (if relevant)

### Entity page (framework or dataset)
1. Origin
2. Core Components
3. Applications in Our Research

### Synthesis page
1. Argument
2. Supporting Evidence (per source, with page refs)
3. Counter-Evidence
4. Gaps in the Literature
5. Implications for Our Research

### Comparison page
1. What Each Source Says
2. Where They Agree
3. Where They Diverge
4. Which Framework Fits Our Research Better
5. Reconciliation (if possible)

### Method page
1. When to Use
2. Key Assumptions
3. Sample Size Requirements
4. Software Options
5. Application in Our Research
6. Prof. Prashar's Guidance (if any)

## Proposal-Based Change Model

- **Pages at seed or working maturity**: Direct edits allowed.
- **Pages at validated maturity**: Never edit directly. Append a `## Change Proposal` section at the bottom with the proposed change, source, and date. A reviewer or the lead incorporates accepted proposals.
- **Deprecated pages**: Never edit. Create a new page and update the `_index.md` to point to the replacement.

## Communication History Convention

For person entity pages, the Communication History section is the retrieval backbone. Each entry must include enough substance that a future query resolves the reference without re-reading the raw email. Bad: "May 2, 2026. Emailed Prashar." Good: "May 2, 2026. Submitted v2 of Agentic AI Governance term paper. Referenced Prof. Suresh's literature review feedback on stronger cross-stream synthesis, tighter DV operationalization. Integrated Jarrahi and Ritala (2025) and Berente et al. (2021). Simplified framework to three propositions. Awaiting Prashar's review."

## Quality Bar for Page Creation

Before writing a new page, the agent must satisfy at least one of:
- For **source**: the source file exists in `knowledge/` and was fully extracted (not truncated).
- For **concept**: the concept appears in 2+ sources already in the wiki.
- For **entity**: the entity appears in 1+ source, email, feedback, or workflow output already in the wiki.
- For **synthesis**: the argument draws on 2+ source pages already in the wiki.
- For **method**: the method is referenced in 1+ source page, or requested by a workflow run.
- For **comparison**: two or more source pages exist and address the same question with different answers.

If none of these are satisfied, do not create the page. Instead, add a note to `_log.md` explaining why the creation was deferred.

## When In Doubt

- Prefer updating an existing page over creating a new one.
- Check `_index.md` before creating any new page.
- If two plausible page types fit (e.g., is this a concept or a method?), check whether the item is a process the researcher performs (method) or an idea the research discusses (concept).
- Keep page titles short (under 60 characters).
- Keep page bodies focused. If a page grows past ~2000 words, consider splitting into a synthesis or comparison page.
