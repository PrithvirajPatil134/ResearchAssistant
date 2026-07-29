---
type: reference
title: "ABDC Journal Quality List 2025 (Consultation Draft, 30 Jan 2025)"
maturity: seed
tags: [journal-ranking, abdc, quality-gate, literature-search, consultation-draft]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [literature_review, research_paper, term_paper]
draws_from: []
source_path: "src/research_assistant/spaces/QNTR/knowledge/literature review/Reference Material/ABDC_JQL_2025_consultation-draft-30.01.25A.xlsx"
target_path: src/research_assistant/spaces/QNTR/wiki/references/abdc-jql-2025-journal-ranking.md
---

**What it is**

The draft 2025 edition of the ABDC Journal Quality List, in consultation form. The workbook is titled "Draft 2025 ABDC Journal Quality List" and notes that the "2025 major review includes new journals, ranking, and textual changes" [ABDC_JQL_2025_consultation-draft-30.01.25A.xlsx, sheet '2025 JQL', rows 6-7]. The filename marks it a consultation draft dated 30.01.25.

**What it is for**

Same purpose as the 2022 list (Management/Business journal-quality gate for literature search per `literature-review-standards.md`), but forward-looking: it carries both the current 2022 rating and the proposed 2025 rating side by side, so you can see how a journal's standing may change.

**Structure** (from `--meta` + header-row peek)

Two sheets [ABDC_JQL_2025_consultation-draft-30.01.25A.xlsx, --meta]:
- `2025 JQL` (2668 rows x 10 cols) — main list. Header row: Journal Title, Publisher, ISSN, ISSNOnline, Year Inception, FoR, 2022 rating, 2025 proposed rating, Recommendation [sheet '2025 JQL', row 8]. Example: Abacus, FoR 3501, 2022 rating A, 2025 proposed rating A, Recommendation "No change" [sheet '2025 JQL', row 11].
- `Removed journals` (143 x 9) — journals proposed for removal, with header Journal Title, Publisher, ISSN, ISSNOnline, Year Inception, FoR, 2022 rating, 2025 proposed rating, Recommendation; the `2025 proposed rating` shows "-" and Recommendation "Remove" (e.g. ACM Transactions on Computer-Human Interaction, previously A*) [sheet 'Removed journals', rows 26-27].

**How to use**

Look up the journal in `2025 JQL` by title. Compare `2022 rating` against `2025 proposed rating` to anticipate a change. Check `Removed journals` if a journal is missing from the main list. Because this is a *consultation draft*, treat the 2022 rating (from the finalized 2022 list) as authoritative for gating and the 2025 proposed rating as provisional until the final 2025 list is published.

**File**: `src/research_assistant/spaces/QNTR/knowledge/literature review/Reference Material/ABDC_JQL_2025_consultation-draft-30.01.25A.xlsx`
