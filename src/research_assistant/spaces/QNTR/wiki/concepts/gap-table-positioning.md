---
title: "Gap Table Positioning"
type: concept
maturity: seed
created: 2026-05-07
last_updated: 2026-05-07
originating_space: QNTR
applicable_to: [research_paper, term_paper, thesis]
schema_version: "1.0"
aliases: ["Table 1 positioning", "Han et al. table", "literature positioning table"]
first_seen: sources/han-2017-relative-strategic-emphasis
sources:
  - wiki/sources/han-2017-relative-strategic-emphasis
tags: [positioning, gap-table, research-craft, literature-review]
draws_from:
  - wiki/sources/han-2017-relative-strategic-emphasis.md
---

## Definition

A gap table is a literature positioning device where prior studies are listed as rows and key research dimensions as columns. The final row shows the current study's contribution, visually demonstrating that it occupies a previously empty cell in the research space. The technique is attributed to Han, Mittal, and Zhang (2017), who used it as Table 1 in their Journal of Marketing paper to show that no prior study had simultaneously examined relative strategic emphasis, risk (rather than return), and dual moderators.

Prof. Prashar explicitly recommended this technique in his May 5, 2026 feedback: "One good way to positioning your study is to give a table with studies that have been done in the past and last row could be what your study is doing and how it bridges the gap."

[Source: wiki/sources/han-2017-relative-strategic-emphasis.md, §Table 1 Structure; QNTR/feedback/response_prof_prashar_termpaper_review_20260505.md, §Argumentation and Positioning]

## Key Dimensions

### Structure of the Table

Han et al.'s Table 1 (pp.26-27) uses the following architecture:

**Columns** represent research dimensions, each a binary (checkmark or blank):
1. Study citation (Author, Year)
2. Whether it studies Advertising (Value Appropriation)
3. Whether it studies R&D (Value Creation)
4. Whether it studies Relative Strategic Emphasis
5. Whether the DV includes Risk
6. Whether the DV includes Return
7. What moderator(s) are examined

**Rows** are organized into two sections:
- "Focus on [focal IV]" (23 studies where the variable is the primary IV)
- "[Focal IV] as Covariates" (17 studies where it appears as a control)
- **Final row**: "Current study" with checkmarks in all relevant columns

**Positioning technique**: The table demonstrates that the combination of all checked dimensions in the final row has not appeared in any prior row. Each column is a dimension of the research space; the current study's unique configuration proves it fills a gap.

[Source: wiki/sources/han-2017-relative-strategic-emphasis.md, §Table 1 Structure]

### Design Principles

1. **Dimensions must be legitimate research choices**, not arbitrary splits. Each column should represent a meaningful conceptual or methodological distinction in the field.
2. **Prior studies must be real and representative**. The table's persuasive power depends on comprehensiveness; if obvious studies are omitted, reviewers will not trust the gap claim.
3. **The gap must be substantive, not trivial**. Combining random features that no one combined before does not justify a paper. The gap must arise from a theoretical or practical need.
4. **Superscript annotations** can distinguish nuances (e.g., Han et al. mark studies where the focal variable is a moderator vs. IV).

[Source: wiki/sources/han-2017-relative-strategic-emphasis.md, §Table 1 Structure, §Methodology]

## How Sources Relate

This is a single-source concept page. Han et al. (2017) is the exemplar paper; the concept's broader application comes from Prof. Prashar's pedagogical recommendation. The gap table technique is not unique to Han et al. (it appears in marketing, strategy, and IS literatures), but their implementation is particularly clean and is the specific model Prashar recommends.

## Application to Research

### Proposed Column Mapping for Agentic AI Governance Paper

Based on the research paper's constructs and the literature review structure:

| Column | Dimension | Logic |
|--------|-----------|-------|
| 1 | Study citation | Standard |
| 2 | AI Governance (general) | Does it study governance of AI systems? |
| 3 | Agentic AI (specifically) | Does it address autonomous, goal-directed agents? |
| 4 | Enterprise Risk as DV | Does it measure risk outcomes? |
| 5 | Business Performance as DV | Does it measure financial/operational performance? |
| 6 | Control/Autonomy Mechanism | Does it examine the autonomy-control tradeoff? |
| 7 | Uncontrolled/Shadow proliferation | Does it address shadow AI or unauthorized agents? |
| 8 | Methodology | Qual / Quant / Mixed |

**Final row**: Current study checks columns 2-8 (general AI governance, agentic specifically, risk DV, performance DV, control mechanism, shadow AI, mixed-methods). No prior study checks all of these simultaneously.

### Row Population

Studies to include (drawn from the literature review):
- Berente et al. (2021): Checks AI governance, not agentic specifically, no risk/performance DV
- Jarrahi and Ritala (2025): Checks AI governance, agentic, control mechanism, no DV measurement
- Kolt (2025): Checks AI governance, agentic, no empirical DV
- Eulerich et al. (2024): Checks governance, shadow AI, not agentic (RPA), no quant DV
- Haase et al. (2024): Checks control mechanism, not agentic specifically, no DV
- Papagiannidis et al. (2025): Checks AI governance, no agentic, no DV
- Mikalef and Gupta (2021): Checks AI capability, performance DV, not governance or agentic
- Taeihagh (2025): Checks AI governance, risk categories, not agentic, no empirical testing

### Prashar's Complementary Advice

Alongside the gap table, Prashar recommends "a lot of market evidence" for positioning: reports by McKinsey, Deloitte, etc. The gap table shows the academic gap; market evidence shows the practical urgency. Both are positioning ingredients.

[Source: QNTR/feedback/response_prof_prashar_termpaper_review_20260505.md, §Argumentation and Positioning]

## Open Questions

1. Should the table include only papers from the literature review (7-12 papers) or expand to a more comprehensive search (20-40 papers) as Han et al. did?
2. How to handle papers that are conceptual (no empirical DV) vs. empirical in the same table? Han et al. resolved this by separating "focus" from "covariate" sections; a parallel distinction might be "focal study" vs. "mentions the concept."
3. The column "Agentic AI specifically" may be too restrictive if the field is so nascent that almost nothing qualifies. Should it be softened to "autonomous systems" to include RPA and autonomous vehicle governance?

[Source: wiki/sources/han-2017-relative-strategic-emphasis.md, §Limitations]

---

<!-- OBSIDIAN-LINKS:START (auto-generated by scripts/obsidian-graph-linker.py, do not edit by hand) -->
## Related
- **Draws from**: [[src/research_assistant/spaces/QNTR/wiki/sources/han-2017-relative-strategic-emphasis|han-2017-relative-strategic-emphasis]]
- **First seen**: [[src/research_assistant/spaces/QNTR/wiki/sources/han-2017-relative-strategic-emphasis|han-2017-relative-strategic-emphasis]]
- **Sources**: [[src/research_assistant/spaces/QNTR/wiki/sources/han-2017-relative-strategic-emphasis|han-2017-relative-strategic-emphasis]]
<!-- OBSIDIAN-LINKS:END -->
