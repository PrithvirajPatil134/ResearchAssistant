---
type: source
target_path: src/research_assistant/spaces/DBA/wiki/sources/albert-2026-org-structure-database.md
title: "A New Organizational Structure Database: Examining Structure Through Top Management Team Compositions"
maturity: working
tags: [organizational-structure, top-management-team, tmt, generative-ai, gpt-4o, fine-tuning, sec-filings, 10-k, def14a, archival-data, s-and-p-500, thesis-spine, coding-method]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: DBA
applicable_to: [thesis, research_paper, literature_review]
draws_from: []
authors: ["Albert, Daniel", "Eklund, John C.", "Tang, Lisa"]
year: 2026
journal: "Strategic Management Journal"
volume: "47(3), 860-892"
doi: "10.1002/smj.70029"
pages: "33 pages (journal pp. 860-892)"
source_path: "src/research_assistant/spaces/DBA/knowledge/thesis-spine-papers/albert-2026-org-structure-database.pdf"
ingested: 2026-07-28
license: "CC-BY-NC-ND (open access)"
data_availability: "https://organizationdesign.github.io/homepage/"
---

## Why This Paper Matters to the Thesis

This is a thesis-spine paper. The DBA thesis on organizational restructuring and generative AI replicates the executive-title coding method documented here. The paper is both a data paper (introducing a public dataset) and a documented precedent for using fine-tuned generative AI to code archival organizational data from SEC filings. [albert-2026-org-structure-database.pdf, p.1 (Abstract); p.4]

The authors (Daniel Albert, Drexel LeBow; John C. Eklund, USC Marshall; Lisa Tang, NUS) contributed equally and are listed alphabetically. The paper received the SMS Annual Conference Research Methods Paper Prize in 2024. [albert-2026-org-structure-database.pdf, p.1; p.30 (Acknowledgments)]

## Research Summary

Studies using archival organizational structure data are less prevalent than expected for such a central strategy topic. The authors introduce a hand-collected dataset of top management team (TMT) compositions of S&P 500 firms between 1993 and 2020, providing original role titles and using generative AI to categorize executive titles into 6 role groups and 12 hierarchical levels. [albert-2026-org-structure-database.pdf, p.1 (Abstract)]

According to Joseph and Sengul (2025), during the 2000-2023 renaissance in organizational structure research only 23% of studies used archival data, with over 50% using proprietary firm data, qualitative data, or simulations. [albert-2026-org-structure-database.pdf, p.2]

## Dataset at a Glance

- 521 S&P 500 firms over three decades (1993-2020). [albert-2026-org-structure-database.pdf, p.3; p.13]
- 161,028 unique executive-firm-year observations across 11,658 firm-years. [albert-2026-org-structure-database.pdf, p.3; p.16]
- Average of 13.8 executives per firm-year and 22.4 years of data per firm. [albert-2026-org-structure-database.pdf, p.16]
- 18 total categories: 6 managerial role groups and 12 hierarchical levels. [albert-2026-org-structure-database.pdf, p.1; p.4]
- Development cost: roughly 5 years, about 5,800 hours of researcher time, and over USD 60,000 in RA and AI-related expenses. [albert-2026-org-structure-database.pdf, p.3; p.28 (footnote 9)]
- Eight research assistants collected data. [albert-2026-org-structure-database.pdf, p.12]
- Matchable to Compustat and other datasets via gvkey, cusip, ticker, and CIK identifiers. [albert-2026-org-structure-database.pdf, p.11]

## Four-Step Database Development Process (Figure 1)

The construction encompassed four steps: (1) developing a study plan, (2) data collection, (3) labeling strategy (initial labeling techniques followed by generative-AI labeling), and (4) analysis and data complementation. [albert-2026-org-structure-database.pdf, p.10; p.12 (Figure 1)]

The detailed coding methodology is captured in the proposed method page `wiki/methods/generative-ai-title-labeling`. This source page summarizes; the method page carries the replicable procedure.

## Comparison With Prior Data Collection Efforts

Drawing on Kretschmer (2024), the authors evaluate their dataset against five criteria capturing key trade-offs: (1) breadth versus depth, (2) uniqueness versus readily available, (3) direct versus indirect measures, (4) self-contained versus extendable, and (5) objective versus subjective measures. [albert-2026-org-structure-database.pdf, p.4-5]

They compare against five types of prior efforts: survey-based, indirect proxy measures, privileged internal firm data, single-industry public filings, and multiple-industry public filings. Their own dataset most resembles the multiple-industry public-filings type. [albert-2026-org-structure-database.pdf, p.5 (Table 1)]

## Comparison With ExecuComp

The dataset has more executives than ExecuComp in 83.0% of firm-years, equal numbers in 7.1%, and fewer in only 9.9%. [albert-2026-org-structure-database.pdf, p.10] ExecuComp has 72,041 observations versus this dataset's 161,028, and averages 6.06 observations per firm-year versus 13.81. Beyond the CEO and CFO, ExecuComp provides no additional labeling of executive roles beyond the raw title. [albert-2026-org-structure-database.pdf, p.11 (Table 2)]

## Exploratory Findings

- **TMT hierarchy declined**: mean TMT Hierarchy (of six most common rank levels) held at about 3.5 out of 6 between 1993 and 2010, then declined to approximately 3.2 by 2020. [albert-2026-org-structure-database.pdf, p.18]
- **Rise of CXO roles**: the proportion of CXOs within executive teams rose from 0.1 to over 0.4 between 1993 and 2020, driven primarily by support CXO roles. [albert-2026-org-structure-database.pdf, p.18-19]
- **Title inflation**: evidence that VP/SVP roles converted to SEVP/EVP or Chief Officer positions over time, possibly driven by competitive executive labor markets. [albert-2026-org-structure-database.pdf, p.19]
- **Industry variation**: Utilities (GICS 55) tend to have the most hierarchical TMTs; Financial Services (GICS 40) the least. Support roles dominate across all industries. [albert-2026-org-structure-database.pdf, p.19-20]
- **Firm-level reorganizations**: illustrated with Hewlett Packard (functional shift under Carly Fiorina, 1999-2005) and General Electric (functional shift under Jeff Immelt, then re-divisionalization under John Flannery and Larry Culp, 2017-2020). [albert-2026-org-structure-database.pdf, p.21]

## Application to Strategy Research (Quasi-Replications)

The authors quasi-replicate, refine, and extend three well-cited TMT studies to demonstrate the dataset's uses: Guadalupe et al. (2014) on diversification and executive-team composition, Zhang (2006) on prior performance and strategic change moderated by the presence of a COO, and Menz and Scheef (2014) on strategic actions/diversification and the presence of a Chief Strategy Officer. These are described as quasi-replications (following Bettis et al., 2016) because they do not use the same samples as the original studies. [albert-2026-org-structure-database.pdf, p.22-23 (Table 3)]

## Limitations Stated by the Authors

- The database may omit executives not listed in public filings and may not capture changes between filing dates; firms have discretion in how broadly they define their executive team beyond SEC minimums. [albert-2026-org-structure-database.pdf, p.29]
- The dataset covers only large US publicly listed firms, raising representativeness questions for non-US or private firms. [albert-2026-org-structure-database.pdf, p.29]
- The role and rank categories are offered as a useful but generic starting point; future work can refine them using the full job titles in the dataset. [albert-2026-org-structure-database.pdf, p.29]

## SEC Disclosure Basis

Executive disclosure rests on SEC requirements: Item 401 of Regulation S-K requires public companies to disclose information about their executive officers, and Rule 3b-7 of the Securities Exchange Act of 1934 defines an executive officer. These requirements specify only a minimum for disclosure, producing heterogeneity across firms. [albert-2026-org-structure-database.pdf, p.3 (footnote 1)]
