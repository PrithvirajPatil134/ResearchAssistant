# Shared Wiki Schema

**Scope**: Conventions that apply to ALL spaces (QNTR, CRO, DBA, CW, future spaces).
**Space-specific extensions**: live at `spaces/{SPACE}/wiki/_schema.md` and reference this file.
**Last updated**: 2026-05-07.

Related: `docs/knowledge_base_design.md`, `.kiro/steering/no-assumption-rule.md`.

---

## Directory Layout (per space)

```
spaces/{SPACE}/wiki/
├── _schema.md       # Space-specific extensions only. References this file.
├── _index.md        # Content catalog for this space.
├── _log.md          # Append-only operation log.
├── sources/         # One page per ingested source
├── concepts/        # One page per key concept in this space
├── entities/        # People, organizations, frameworks, datasets
├── syntheses/       # Cross-source arguments
├── methods/         # Methodology reference pages
├── comparisons/     # Head-to-head source comparisons
└── references/      # Pointer pages for lookup/reference artifacts
```

## Cross-Space Directory

```
data/wiki/shared/
├── _index.md                  # Shared content catalog
├── _log.md                    # Shared-wiki operation log
├── concepts/                  # Concepts relevant to 2+ spaces
├── methods/                   # Methods relevant to 2+ spaces
├── entities/                  # Entities relevant to 2+ spaces
├── deliverables/              # Cross-space deliverable synthesis pages
└── learner/                   # Orchestrator patterns, failure memory
```

## Page Types

| Type | When to create | One-per |
|------|----------------|---------|
| source | A PDF, paper, book, slide deck, or similar is ingested | Source artifact |
| concept | A concept appears in 2+ sources | Concept name |
| entity | A person, organization, framework, or dataset is referenced | Entity |
| synthesis | Multi-source argument identified during research | Research thread |
| method | A statistical or analytical method is used in the research | Method |
| comparison | Two or more sources address the same question differently | Question-pair |
| reference | A lookup/reference artifact (journal-ranking sheet, impact-factor list, supplementary teaching material) needs a pointer page describing its purpose, structure, and how to use it — NOT a full-text transcription | Reference artifact |
| deliverable_synthesis | A paper/thesis/case that draws from multiple spaces | Deliverable |

## Required Frontmatter (all page types)

```yaml
---
type: <source|concept|entity|synthesis|method|comparison|reference|deliverable_synthesis>
title: "<human-readable title>"
maturity: <seed|working|validated|deprecated>
tags: [kebab-case, tag, list]
schema_version: "1.0"
created: 2026-05-07
last_updated: 2026-05-07
originating_space: <QNTR|CRO|DBA|CW|shared>
applicable_to: [research_paper, thesis, case_study, teaching_note, term_paper]
draws_from: []
---
```

### Field-Specific Rules

- `schema_version`: bumped when schema changes; enables bulk migrations.
- `originating_space`: the space where the page was first created. For shared-directory pages, use `shared`.
- `applicable_to`: list of deliverable kinds this page could support. Keep the vocabulary small: `research_paper`, `thesis`, `case_study`, `teaching_note`, `term_paper`, `literature_review`, `conference_paper`, `email`. Extend only when a new deliverable kind genuinely exists.
- `draws_from`: for synthesis and deliverable_synthesis pages, a structured list of sources by space:

```yaml
draws_from:
  QNTR:
    - wiki/sources/berente-2021-managing-ai
    - wiki/methods/sem-structural-equation-modeling
  CRO:
    - wiki/methods/eisenhardt-theory-building
  shared:
    - concepts/principal-agent-theory
```

## Type-Specific Frontmatter Extensions

### source
```yaml
authors: ["Berente, N.", "Gu, B."]
year: 2021
journal: "MIS Quarterly"
volume: "45(3)"
pages: "1433-1450"
source_path: "knowledge/research_papers/berente_2021_managing_ai.pdf"
ingested: 2026-05-07
```

### concept
```yaml
aliases: ["alt name 1", "alt name 2"]
first_seen: sources/eulerich-2024-dark-side-rpa
sources: [sources/berente-2021, sources/jarrahi-2025]
```

### entity (person)
```yaml
entity_kind: person
aliases: ["Prashar", "Prof. Prashar"]
role: "QNTR Course Mentor"
institution: "IIM Sambalpur"
relationship_to_user: "Course mentor and term paper advisor"
mentions_in_sources: []
mentions_in_syntheses: []
mentions_in_communications: []
cross_space_presence: []
```

**Entity page creation rule** (applies to all entity_kinds, especially person):

An entity page exists ONLY when the entity has a relational or operational presence in your research, not when they are a citation. Concretely:

- **YES, entity page**: people you correspond with (advisors, committee, collaborators, editors, referees), people referred to you for potential collaboration (with a named relationship, not just a lookup), institutions whose affiliation you carry or interact with, datasets you actively analyze, named frameworks you apply across multiple sources.
- **NO, no entity page**: authors of papers you cite (their names live in the source page's `authors:` field), historical figures mentioned only for attribution (Weber, Merton), people mentioned once in a source you read.

**The test**: "Will I refer to this entity by name in a future chat or query without explaining who they are?" If yes, entity page. If no, the source page's author field is sufficient.

When in doubt, do NOT create an entity page. They are for the relational graph, not the bibliography.

### entity (framework, dataset, organization)
```yaml
entity_kind: <framework|dataset|organization>
origin: "<short attribution>"
```

### synthesis
```yaml
sources: [...]
propositions_supported: [P1, P2, P3]
```

### comparison
```yaml
sources: [<source-a>, <source-b>]
question: "<the specific question both sources address>"
```

### reference
```yaml
source_path: "src/research_assistant/spaces/QNTR/knowledge/.../artifact.xlsx"
```
A `reference` page points to a lookup artifact rather than transcribing it. The body describes what the artifact is, what it is for, its structure (sheet/page layout from `--meta`), and how to use it, with every claim traced to a cell/row/page. It does not reproduce the artifact's contents. Filed under `references/`. Example pages: `spaces/QNTR/wiki/references/abdc-jql-2022-journal-ranking.md` (a journal-quality gate) and `qntr-variability-supp-material.md` (a statistics teaching aid).

### deliverable_synthesis
```yaml
target_deliverable: "<Agentic AI Governance Term Paper>"
current_version: "v2"
version_history:
  - version: "v1"
    completed: 2026-04-15
  - version: "v2"
    completed: 2026-05-02
    changes: "Simplified framework to three propositions, added two papers"
```

## Maturity States

| State | Meaning | Transition criteria |
|-------|---------|---------------------|
| seed | Single source, not cross-referenced | Default on creation |
| working | 2+ sources, cross-refs built | Multi-source coverage |
| validated | User-approved or reviewer-verified | Explicit approval |
| deprecated | Superseded or incorrect | Flagged and confirmed |

Query behavior prefers `validated`, uses `working` with caveat, ignores `deprecated`, includes `seed` only when no better source exists.

## Change Model

- Pages at `seed` or `working`: direct edits allowed.
- Pages at `validated`: no direct edits. Append `## Change Proposal` blocks with proposed changes, source, and date. A reviewer or orchestrator-synthesizer incorporates accepted proposals.
- Pages at `deprecated`: no direct edits. Create a new page; update `_index.md` to point to the replacement; set `superseded_by: ../<new-path>` in deprecated page frontmatter.

## Naming Conventions

- Files: kebab-case, lowercase.
- Source pages: `{first-author-lastname}-{year}-{short-slug}.md`.
- Entity pages (person): `{honorific-optional}-{lastname}.md`, e.g. `prof-prashar.md`.
- Synthesis pages: kebab-case research thread name.

## Cross-References

Use relative paths from the page's directory. A concept page in QNTR referencing a shared method:
```
../../../shared/methods/sem-structural-equation-modeling.md
```

All cross-references must target existing pages. Broken refs are caught by `ra-wiki-linter`.

## Cross-Space Promotion

Triggered when a page is referenced by deliverables from 2+ spaces (`applicable_to` includes deliverables whose `originating_space` differs).

Process (handled by `ra-wiki-linter` proposing, user approving):
1. Move the page to `data/wiki/shared/{type}/`.
2. In the original location, leave a stub with frontmatter `superseded_by: ../../../shared/{type}/{slug}.md` and `maturity: deprecated`.
3. Update all cross-references workspace-wide to point to the shared location.

## Space-Specific Extensions

A space schema (`spaces/{SPACE}/wiki/_schema.md`) may:
- Add new page types relevant only to that space (e.g., CW might add `case_styles/`).
- Add space-specific frontmatter fields.
- Specify space-specific sections required in page bodies.

A space schema may NOT:
- Remove or contradict required frontmatter from this shared schema.
- Override naming conventions.
- Override maturity rules.

## Quality Bar for Page Creation

Before writing a new page:
- **source**: the source file exists in `knowledge/` and was fully extracted.
- **concept**: the concept appears in 2+ sources already in the wiki.
- **entity**: the entity appears in 1+ source, email, feedback, or workflow output already in the wiki.
- **synthesis**: the argument draws on 2+ source pages already in the wiki.
- **method**: the method is referenced in 1+ source page or requested by a workflow.
- **comparison**: 2+ source pages exist and address the same question differently.
- **reference**: the lookup artifact exists in `knowledge/` and is used as a gate or aid (e.g., a journal-ranking list consulted during literature search), warranting a pointer page rather than a full source-page treatment.
- **deliverable_synthesis**: a real deliverable exists or is actively being drafted.

Unsatisfied? Do not create. Log the deferred creation to `_log.md`.
