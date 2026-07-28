---
title: "Building Block Search Strategy"
type: method
maturity: seed
created: 2026-05-07
originating_space: QNTR
applicable_to: [QNTR]
schema_version: "1.0"
draws_from:
  - spaces/QNTR/wiki/entities/prof-priyanka-suresh.md
tags: [literature-review, search-strategy, prisma, systematic-review]
---

## Overview

A systematic search methodology for interdisciplinary literature reviews, taught by Prof. Priyanka Suresh in the IIM Sambalpur DBA programme (March 28 session). The strategy starts with core concepts and combines them incrementally, moving from broad exploration to narrow precision. It is "useful when the topic is interdisciplinary in nature" because it prevents premature narrowing that would miss relevant work across discipline boundaries.

[Source: QNTR/wiki/entities/prof-priyanka-suresh.md, §Key Guidance, Search Strategy; `Prof. Priyanka Class Notes.docx`, paragraphs under "03/28"]

## Steps/Protocol

### Step 1: Identify Key Concepts

Break the research question into its essential components. Each component becomes a "building block" that will be searched independently before combination.

For a question like "How does agentic AI governance maturity affect enterprise risk and business performance?", the blocks are:
- Block A: Agentic AI / autonomous AI agents
- Block B: Governance / governance maturity
- Block C: Enterprise risk / operational risk / financial loss
- Block D: Business performance / firm performance

[Source: QNTR/wiki/entities/prof-priyanka-suresh.md, §Key Guidance, Search Strategy, Step 1; `Prof. Priyanka Class Notes.docx`, "Step 1: Identify Key Concepts"]

### Step 2: Find Synonyms and Related Terms

For each building block, identify synonyms, related terms, and variant phrasings. Use truncation and wildcards to capture morphological variations.

**Boolean operators** (must be uppercase):
- AND: narrows (both terms required)
- OR: broadens (either term sufficient)
- NOT: excludes (use sparingly; use `-` on Google Scholar instead of NOT)

**Special operators**:
- Quotation marks for exact phrase: `"agentic governance"`
- Truncation `*` for variations: `govern*` finds governance, governing, governed
- Wildcards `?` for single character: `wom?n` finds woman, women
- Parentheses for nesting: `(blockchain OR "distributed ledger") AND (education OR learning)`

Example blocks for agentic AI governance:
- Block A: `("agentic AI" OR "AI agent*" OR "autonomous AI" OR "goal-directed AI" OR "LLM agent*")`
- Block B: `(govern* OR oversight OR "risk management" OR compliance OR accountability)`
- Block C: `("enterprise risk" OR "operational risk" OR incident* OR "financial loss" OR breach*)`
- Block D: `("firm performance" OR "business value" OR "organizational performance" OR ROI)`

[Source: QNTR/wiki/entities/prof-priyanka-suresh.md, §Key Guidance, Search Strategy, Step 2; `Prof. Priyanka Class Notes.docx`, "Boolean Operators" and "Other Essential Operators"]

### Step 3: Broad Search (Each Block Separately)

Search each concept block independently to explore the landscape. This reveals the volume and character of literature in each domain before combining.

Run Block A alone, Block B alone, Block C alone, Block D alone. Record result counts per database. This stage identifies which databases have strong coverage of each block and whether the block terms need refinement.

[Source: QNTR/wiki/entities/prof-priyanka-suresh.md, §Key Guidance, Search Strategy, Step 3; `Prof. Priyanka Class Notes.docx`, "Step 3: Broad Search"]

### Step 4: Moderate Specificity (Combine Two Blocks)

Combine blocks pairwise using AND to find intersection literature:
- A AND B: agentic AI governance (core intersection)
- A AND C: agentic AI and enterprise risk
- B AND C: governance and enterprise risk (broader IT governance literature)
- A AND D: AI agents and business performance

Record result counts. The pairwise combinations reveal where literature is dense and where gaps exist. If A AND B yields fewer than 20 results in top databases, the gap is confirmed.

[Source: QNTR/wiki/entities/prof-priyanka-suresh.md, §Key Guidance, Search Strategy, Step 4; `Prof. Priyanka Class Notes.docx`, "Step 4: Moderate Specificity"]

### Step 5: Narrow the Search

Once foundational knowledge is established from Steps 3-4, narrow using three or four blocks combined:
- A AND B AND C: agentic AI governance affecting enterprise risk
- A AND B AND D: agentic AI governance affecting business performance
- A AND B AND C AND D: full intersection (likely near-zero results for a nascent topic)

The near-zero result for the full intersection is itself evidence of the gap.

Document every search executed with: database, date, exact query string, number of results, and number retained after title/abstract screening. "This will help in not iteratively searching the same combinations and being stuck in a limbo."

[Source: QNTR/wiki/entities/prof-priyanka-suresh.md, §Key Guidance, Search Strategy, Step 5; `Prof. Priyanka Class Notes.docx`, "Step 5" and documentation tip]

## When to Use

- Research question spans multiple disciplines (IS, law, management, computer science)
- Topic is interdisciplinary and no single database or keyword set captures the full landscape
- Need to document gap evidence systematically for a research positioning argument
- Conducting a systematic or semi-systematic literature review rather than a narrative review

For very new topics (like agentic AI governance), Prof. Priyanka recommends a **thematic review** or **semi-systematic review** rather than a full SLR, because the topic is not mature enough for a comprehensive systematic review. Conference papers are acceptable "if the field is nascent and doesn't have supporting research papers in top journals."

[Source: QNTR/wiki/entities/prof-priyanka-suresh.md, §Key Guidance, Literature Review Types; `Prof. Priyanka Class Notes.docx`, "03/21" and conference papers note]

## Application to Research

For the agentic AI governance systematic search:

**Databases**: Scopus, Web of Science, EBSCO (Business Source Complete), AIS eLibrary, IEEE Xplore, ACM Digital Library. Google Scholar for supplementary discovery only (not for systematic counts).

**Quality gate** (applied at screening stage):
- ABDC A*, A, or B rated journals (Management/Business)
- CORE A*, A, or B ranked venues (Computer Science)
- JCR Impact Factor at minimum 2.0, Q1 or Q2 quartile (cross-disciplinary)
- Conference papers acceptable only for nascent sub-topics (e.g., BPM 2025 for Vu et al.)

[Source: QNTR/wiki/entities/prof-priyanka-suresh.md, §Key Guidance, Quality Gates]

**PRISMA reporting**: Document the full flow from identification through screening, eligibility, and inclusion. Use the PRISMA checklist for the abstract and methods section. The flow diagram should show: records identified per database, duplicates removed, records screened, full-text assessed, and studies included with exclusion reasons at each stage.

[Source: QNTR/wiki/entities/prof-priyanka-suresh.md, §Key Guidance, PRISMA Framework]

**Synthesis approach** (from April 4 session): Synthesize, do not summarize. "Synthesizing is summarizing + critiquing + adding originality and your opinion on the birds eye view of the summary." Synthesis must be topic-based, not author-based. Use concept maps to visualise research gaps; journals favour concept maps in literature reviews.

[Source: QNTR/wiki/entities/prof-priyanka-suresh.md, §Key Guidance, Synthesis Approach; `Prof. Priyanka Class Notes.docx`, "04/04"]

## Limitations

- The strategy works best for interdisciplinary topics; for single-discipline reviews, simpler keyword searches may suffice.
- Boolean logic varies across databases (NOT behaves differently on Google Scholar vs. Scopus). Requires per-database adaptation.
- Truncation and wildcards are not universally supported (some databases require different syntax).
- The method does not prescribe how many results to retain at each stage or when to stop expanding; judgment is required.
- For a nascent topic like agentic AI governance, Step 5 may yield near-zero results, requiring backward citation tracking and snowballing as supplements.

[Source: QNTR/wiki/entities/prof-priyanka-suresh.md, §Key Guidance, Search Strategy; inferred from application to nascent topic]

## Key References

- Prof. Priyanka Suresh, Literature Review Workshop sessions (March 21, March 28, April 4, 2026), IIM Sambalpur DBA programme.
- PRISMA Statement: Moher, D. et al. (2009). Preferred Reporting Items for Systematic Reviews and Meta-Analyses: The PRISMA Statement.
- Kitchenham, B. and Charters, S. (2007). Guidelines for performing Systematic Literature Reviews in Software Engineering.

---

<!-- OBSIDIAN-LINKS:START (auto-generated by scripts/obsidian-graph-linker.py, do not edit by hand) -->
## Related
- **Draws from**: [[src/research_assistant/spaces/QNTR/wiki/entities/prof-priyanka-suresh|prof-priyanka-suresh]]
<!-- OBSIDIAN-LINKS:END -->
