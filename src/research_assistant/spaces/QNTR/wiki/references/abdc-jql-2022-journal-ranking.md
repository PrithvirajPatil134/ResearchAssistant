---
type: reference
title: "ABDC Journal Quality List 2022 (with 2010-2019 back-lists)"
maturity: seed
tags: [journal-ranking, abdc, quality-gate, literature-search, business-management]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [literature_review, research_paper, term_paper]
draws_from: []
source_path: "src/research_assistant/spaces/QNTR/knowledge/Session 1-4/S1-2 QNTR 2025 - ABDC JQL 2022 v3.xlsx"
target_path: src/research_assistant/spaces/QNTR/wiki/references/abdc-jql-2022-journal-ranking.md
---

**What it is**

The Australian Business Deans Council (ABDC) Journal Quality List, 2022 edition, distributed as QNTR Session 1-2 material. The workbook is titled "2022 ABDC Journal Quality List" and is marked "Current to the review finalised 15 March 2023 including minor textual changes" [S1-2 QNTR 2025 - ABDC JQL 2022 v3.xlsx, sheet '2022 JQL', rows 6-7].

**What it is for**

The ABDC list is the journal-quality gate for Management / Business sources in QNTR literature search. `.kiro/steering/literature-review-standards.md` restricts searches to "top quality ring journals (A*, A, or B rated)" and names the "ABDC Journal Quality List (A*, A, B minimum)" as the Management/Business standard [literature-review-standards.md, §"top quality ring journals"]. Use this sheet to confirm a candidate journal's ABDC rating before including a paper.

**Structure** (from `--meta` + header-row peek)

Seven sheets [S1-2 QNTR 2025 - ABDC JQL 2022 v3.xlsx, --meta]:
- `2022 JQL` (2689 rows x 8 cols) — the main list. Header row: Journal Title, Publisher, ISSN, ISSN Online, Year Inception, FoR code, FoR title, 2022 rating [sheet '2022 JQL', row 8]. Ratings observed include A*, A, B (e.g. Abacus = A, FoR 3501 Accounting) [sheet '2022 JQL', row 11].
- `2019 JQL` (2688 x 7), `2016 JQL` (2785 x 9), `2013 JQL` (2766 x 7), `2010 JQL` (2664 x 7) — prior-edition back-lists for historical rating checks.
- `2022 Quick check` (55 x 2) — a filtered view for a single Field of Research; the copy on disk is set to FoR title "Marketing" and lists journals grouped under rating labels (A*, A, ...) [sheet '2022 Quick check', rows 0-19].
- `FoRs` (41 x 18) — summary by Field of Research code: FoR, Description, Total Journals, A* %, A %, B %, C % (e.g. 3501 "Accounting, auditing and accountability", 156 journals, 8.3% A*) [sheet 'FoRs', rows 15-16].

**How to use**

To gate a Management/Business paper: find the journal in `2022 JQL` by title, read the `2022 rating` column, and include only if A*, A, or B per the standard. Use `2022 Quick check` when working within one FoR (adjust its filter to the target field). Use the year-suffixed back-list sheets only when a historical rating is needed.

**Caveat**: The rating scheme in this workbook uses A*, A, B, C (C appears in the `FoRs` percentage columns) [sheet 'FoRs', row 15]. The QNTR standard admits A*, A, B; C-rated journals fall below the gate.

**File**: `src/research_assistant/spaces/QNTR/knowledge/Session 1-4/S1-2 QNTR 2025 - ABDC JQL 2022 v3.xlsx`
