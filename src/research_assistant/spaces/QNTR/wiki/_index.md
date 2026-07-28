# QNTR Wiki Index

**Space**: QNTR (Quantitative Research Methods)
**Last updated**: 2026-05-07
**Schema**: [`_schema.md`](./_schema.md)
**Log**: [`_log.md`](./_log.md)

This file is the content catalog for the QNTR wiki. Every wiki page must be listed here under the correct section. Ingest and lint operations update this file. Query operations read this file first to understand what knowledge is available.

---

## Sources (0)

_No source pages yet. Run `ra ingest --persona QNTR --source <path>` to add one._

<!--
Entries go here as the 7 papers get ingested. Expected format:

| Page | Authors | Year | Tags | Maturity |
|------|---------|------|------|----------|
| [berente-2021-managing-ai](./sources/berente-2021-managing-ai.md) | Berente et al. | 2021 | ai-governance, autonomy, inscrutability | seed |
-->

## Concepts (0)

_No concept pages yet. Concept pages auto-create when a concept appears in 2+ sources._

<!--
| Page | Aliases | Sources | Maturity |
|------|---------|---------|----------|
| [principal-agent-theory](./concepts/principal-agent-theory.md) | PAT, agency theory | 3 | working |
-->

## Entities (2)

| Page | Kind | Role | Maturity |
|------|------|------|----------|
| [prof-prashar](./entities/prof-prashar.md) | person | QNTR Course Mentor, Term Paper Advisor | working |
| [prof-priyanka-suresh](./entities/prof-priyanka-suresh.md) | person | Literature Review Workshop Instructor | seed |

## Syntheses (1)

| Page | Target Deliverable | Current Version | Maturity |
|------|-------------------|-----------------|----------|
| [agentic-ai-governance-term-paper](./syntheses/agentic-ai-governance-term-paper.md) | Agentic AI Governance Term Paper | v2 | working |

## Methods (0)

_No method pages yet. Method pages appear when the `quant` workflow runs or when methods are referenced in sources._

## Comparisons (0)

_No comparison pages yet. Comparison pages appear during lint when two sources address the same question differently._

---

## Recently Updated

_Populated by ingest and workflow runs. Most recent 10 entries._

- 2026-05-07: `entities/prof-priyanka-suresh.md` created (Batch 2 ingest)
- 2026-05-07: `syntheses/agentic-ai-governance-term-paper.md` created (Batch 2 ingest)
- 2026-05-07: `entities/prof-prashar.md` updated with May 3 feedback (Batch 2 ingest)
- 2026-05-06: `_schema.md` created (wiki skeleton initialized)
- 2026-05-06: `_index.md` created (this file)
- 2026-05-06: `_log.md` created

## Validation Tests (from KB design Phase 1)

- [ ] Ingest 7 QNTR papers (literature review paper set). Output must match or exceed `data/summaries/literature_review_7papers_analysis.md`.
- [ ] Ingest Prashar email (`spaces/QNTR/communication/email_prof_prashar_submission_date_20260502.md`). After ingest, `entities/prof-prashar.md` must show the May 2 communication history entry, and `entities/prof-priyanka-suresh.md` must exist with her feedback.
- [ ] Reference resolution: query "the email to Prashar" resolves to the correct artifact without a file path.
