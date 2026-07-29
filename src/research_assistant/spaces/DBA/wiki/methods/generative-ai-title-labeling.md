---
type: method
target_path: src/research_assistant/spaces/DBA/wiki/methods/generative-ai-title-labeling.md
title: "Generative-AI Labeling of Executive Titles from SEC Filings (Albert, Eklund & Tang 2026)"
maturity: working
tags: [generative-ai, gpt-4o, fine-tuning, coding-method, labeling, tmt, sec-filings, 10-k, def14a, organizational-structure, llm, thesis-method]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: DBA
applicable_to: [thesis, research_paper]
draws_from:
  DBA:
    - wiki/sources/albert-2026-org-structure-database
---

# Generative-AI Labeling of Executive Titles from SEC Filings

The method the DBA thesis replicates: coding executives' job titles disclosed in SEC filings into consistent managerial-role and hierarchical-level categories using a fine-tuned large language model, after human/dictionary baselines proved insufficient at scale.

A terminology note from the authors: they use "labeling" (assigning predefined categories) rather than "coding," reserving "coding" for the qualitative interpretation sense and for writing software. Both writing and executing program code and assigning categories occur in their process, so they keep the terms distinct. [albert-2026-org-structure-database.pdf, p.13 (footnote 4)]

## Step 1: Study Plan

Select a sample meeting criteria of economic relevance and data availability. The authors used the S&P 500, which represents approximately 80% of the total market capitalization of the US equity market. Using Compustat via WRDS, they identified 614 firms under the index name "S&P 500 Comp-Ltd" present in the index between 2003 and 2007 inclusive, then narrowed to 521 firms across eight GICS sectors: 20 (Industrials), 25 (Consumer Discretionary), 30 (Consumer Staples), 35 (Health Care), 40 (Financials), 45 (Information Technology), 50 (Communication Services), and 55 (Utilities). GICS 10 (Energy), 15 (Materials), and 60 (Real Estate) were excluded due to time and funding constraints. The window 1993-2020 was chosen because corporate-document digitization increased in the 1990s (coverage before 1993 was very limited) and data collection began in 2019. [albert-2026-org-structure-database.pdf, p.10; p.12-13]

## Step 2: Manual Data Collection

Sources: firms' annual reports from Mergent Archives, company websites (current and historical via the Wayback Machine), and 10-K filings and DEF14A proxy statements from SEC EDGAR. A total of 9,668 reports were initially collected over the 28-year period. [albert-2026-org-structure-database.pdf, p.13]

Eight RAs extracted disclosed TMT data into standardized Excel worksheets. For each executive they recorded: first, last, and full name; job title and full role description; company name; fiscal year; and the specific data source (e.g., 10-K). RAs were trained to skim documents for the complete list of executives, including the CEO. [albert-2026-org-structure-database.pdf, p.13]

Data-quality practices during collection:
- Collect manually, because firms report executives heterogeneously even within the same firm across years (full team in an annual report or DEF14A in some years, only the top three-to-five officers in a 10-K in others), which defeats automated extraction and raises both false-positive risk (e.g., extracting board members) and false-negative risk. [albert-2026-org-structure-database.pdf, p.13]
- Use the same source for a given firm over time where possible, to keep within-firm comparisons consistent. [albert-2026-org-structure-database.pdf, p.13]
- Collect executive roles only, not board roles. [albert-2026-org-structure-database.pdf, p.13]
- Assign the same RA to compile all years for a firm, to build firm-specific familiarity with reporting patterns. [albert-2026-org-structure-database.pdf, p.13]

The initial raw dataset held 100,806 executive-firm-year observations. [albert-2026-org-structure-database.pdf, p.13]

## Step 3: Labeling Categories

Two category sets were developed over multiple iterative rounds of reviewing raw data and literature (detailed in Appendix 1, Data S1, not included in the PDF). [albert-2026-org-structure-database.pdf, p.14]

**Six managerial-role categories** (multiple allowed per executive), inspired by Guadalupe et al. (2014) and value-chain frameworks (Porter's primary and supporting activities; Chandler's value-creating and administrative distinction):
1. CEO of the company
2. CXO: any Chief Officer role other than the CEO
3. Primary value chain responsibilities (operations, sales and marketing, supply chain management)
4. Support roles (R&D, strategy, finance, IT, HR)
5. Business Unit responsibilities (role tied to a distinct operating subunit)
6. Board of Directors affiliation (e.g., Executive Chairman of the Board)
[albert-2026-org-structure-database.pdf, p.14]

**Twelve hierarchical rank/level categories**: (1) President, (2) Senior Vice Chairman, (3) Vice Chairman, (4) Senior Executive Vice President, (5) Executive Vice President, (6) Senior Vice President, (7) Vice President, (8) Senior Director, (9) Senior Managing Director, (10) Director, (11) Managing Director, (12) Senior Executive. 84.8% of executive-year roles fall into one of these 12 levels or into CEO/CXO; the remaining 15.2% cover roles such as Treasurer, Secretary, or business-unit-specific roles with no specified hierarchical level. For ranks that can be board or executive titles (President, Senior/Vice Chairman, Senior Director, Senior/Managing Director, Director), the team double-checked that they were executive rather than board roles. [albert-2026-org-structure-database.pdf, p.14]

## Step 3a: Why the Two Established Techniques Were Insufficient

**Dictionary matching**: semi-automated matching of titles to categories via perfect and root-word matches (e.g., "finance*" and "treasur*" for finance support roles). Weakness: errors of omission cannot easily be gauged. One can check whether assigned labels are correct but not whether additional categories should have been assigned. [albert-2026-org-structure-database.pdf, p.14-15]

**Human RA labeling**: RAs manually apply the dictionary rules. Strength: humans read context (e.g., "Chief of Financial Services" is a support role by root word but a Business Unit role in a US bank). Weakness: high variance in interpretation across multiple RAs and over time, especially given the scale and heterogeneity of firms and industries. [albert-2026-org-structure-database.pdf, p.15]

The dilemma: dictionaries carry omission errors; humans carry high variance. [albert-2026-org-structure-database.pdf, p.15]

## Step 3b: Generative-AI Labeling (The Core Method)

The authors fine-tuned an OpenAI GPT model, building on lessons from the dictionary and RA baselines. At the time, the most capable LLM available for individual fine-tuning was **GPT-4o-2024-08-06**. Fine-tuning is additional training on one's own data that adjusts the model's internal parameters to the specific terminology and contextual subtleties of management roles. [albert-2026-org-structure-database.pdf, p.15-16]

Training-data construction and parameters:
- **Training set**: 4,977 rows drawn from the database, randomly stratified across industries and years, reflecting the database's industry distribution. Broad representational coverage was prioritized over exact distributional precision. [albert-2026-org-structure-database.pdf, p.16 (and footnote 6)]
- **Human validation of training labels**: using labels previously assigned by dictionary and human approaches, the team reviewed every training row, corrected errors and omissions, and resolved disagreements in meetings involving all authors. [albert-2026-org-structure-database.pdf, p.16]
- **Row format**: each row = one firm-year individual's job title plus the final labels across the 6 role categories and 12 hierarchical levels. The firm name and fiscal year were passed to the LLM as additional context. [albert-2026-org-structure-database.pdf, p.16]
- **Split**: 75% training, 25% validation (within the fine-tuning process). [albert-2026-org-structure-database.pdf, p.16]
- **Epochs**: 3 (the training data was seen three times). [albert-2026-org-structure-database.pdf, p.16]
- **Holdout test set**: an additional 2,010 rows, non-overlapping with training/validation, labeled by the same procedure. [albert-2026-org-structure-database.pdf, p.16]

Accuracy results on the holdout:
- Initial labeling accuracy of the fine-tuned GPT-4o was 94.6%. [albert-2026-org-structure-database.pdf, p.16]
- Of the 108 apparent errors, 70 were subsequently found to be correct AI labels (the team's own labels had been wrong in those hard cases). This implies AI labeling accuracy of 98.1% and human labeling accuracy of 96.5%. [albert-2026-org-structure-database.pdf, p.16]

Reproducibility via open-source models: the authors also fine-tuned Meta's Llama 3.1 (8 billion parameters) and Mistral's Nemo (12 billion parameters) on the same training data. Both produce very similar labels to GPT-4o but with slightly lower accuracy (between 95% and 96%, versus about 98%). Fine-tuned OpenAI models are accessible only through the account that fine-tuned them, so the authors could not directly share the GPT-4o model. Repository links are in Appendix 3, Data S1 (not in the PDF). [albert-2026-org-structure-database.pdf, p.16-17 (and footnotes 7-8)]

## Step 4: Analysis and Data Complementation

The AI labeling models were run over all data and results inspected. Iterative recollection was triggered when a firm-year had an unusually low number of executives (fewer than 5), an unusually high number (more than 30), or when the executive count varied by more than 10 across years (a signal of a change in reporting or data source). Corrected data was re-labeled with the AI models for final analysis, yielding the final 161,028 executive-firm-year observations. [albert-2026-org-structure-database.pdf, p.17]

## Replication Notes for the Thesis

- The method is a documented human-plus-AI precedent: dictionary and human labeling establish and validate the ground-truth training labels; the fine-tuned LLM then scales the labeling. [albert-2026-org-structure-database.pdf, p.16; p.28-29]
- Source consistency (same filing type per firm over time) and executive-not-board discipline are prerequisites established during manual collection, before any AI is applied. [albert-2026-org-structure-database.pdf, p.13]
- The public dataset provides raw titles, so a replicating study can build its own categories rather than adopting the six-role / twelve-level scheme. [albert-2026-org-structure-database.pdf, p.4; p.14]
