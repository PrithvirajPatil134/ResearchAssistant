---
type: reference
title: "JCR Impact Factor List 2025"
maturity: seed
tags: [journal-ranking, impact-factor, jcr, quality-gate, literature-search, quartile]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [literature_review, research_paper, term_paper]
draws_from: []
source_path: "src/research_assistant/spaces/QNTR/knowledge/literature review/Reference Material/JCRI-mpact-Factors_2025.pdf"
target_path: src/research_assistant/spaces/QNTR/wiki/references/jcri-impact-factors-2025.md
---

**What it is**

A 500-page PDF titled "JCR IMPACT FACTOR LIST 2025", edited by Dr. Niaz Ali [JCRI-mpact-Factors_2025.pdf, p.1]. It is a ranked master list of journals by Journal Impact Factor (JIF).

**What it is for**

The cross-disciplinary journal-quality gate. `literature-review-standards.md` sets the cross-disciplinary bar at "JCR Impact Factor >= 2.0 and Q1/Q2 quartile" [literature-review-standards.md, §"Cross-disciplinary"]. This list is where you look up a journal's JIF and quartile to apply that bar (useful when a journal is outside the Management/Business ABDC scope, e.g. Computer Science, medical, or interdisciplinary venues).

**Structure** (from `--meta` + page peek)

- 500 pages [--meta]. Tabular, one row per journal, sorted by JIF descending. Columns: Rank, Journal Name, Publisher, ISSN, JIF, Quartile [JCRI-mpact-Factors_2025.pdf, p.1 header].
- Top of the list: rank 1 CA-A CANCER JOURNAL FOR CLINICIANS (Wiley, ISSN 0007-9235, JIF 232.4, Q1); rank 6 LANCET (JIF 88.5, Q1); rank 28 NATURE (JIF 48.5, Q1); rank 30 SCIENCE (JIF 45.8, Q1) [JCRI-mpact-Factors_2025.pdf, p.1-2]. The list spans all disciplines, not just business.
- Quartile column uses Q1 (and, further down the list, lower quartiles) [p.1].

**How to use**

Search the PDF for the journal name to read its JIF and Quartile. Apply the cross-disciplinary gate: include a paper only if the journal's JIF >= 2.0 and its quartile is Q1 or Q2, per the standard. Because it is a 500-page ranked file, use text search / `--pages` ranges rather than reading front to back.

**Caveat**: Editor-compiled JIF list (Dr. Niaz Ali), not the official Clarivate JCR portal; entries show duplicated rows in the extracted text (e.g. rank 10, 17 repeated) [JCRI-mpact-Factors_2025.pdf, p.1] which is an extraction artifact to ignore when reading a single value.

**File**: `src/research_assistant/spaces/QNTR/knowledge/literature review/Reference Material/JCRI-mpact-Factors_2025.pdf`
