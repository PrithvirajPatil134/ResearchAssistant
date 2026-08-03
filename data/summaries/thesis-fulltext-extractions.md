# Thesis Full-Text Extraction Results

**Date**: 2026-07-08
**Purpose**: Extract replicable methodology from priority papers across three thesis foundations (AI Adoption Intensity, Punctuated Equilibrium, Archival Org Structure).
**Papers targeted**: 10
**Full text obtained**: 2
**Paywalled**: 8

---

## Section 1: Foundation 1 — AI Adoption Intensity

### McElheran, Li, Brynjolfsson, Kroff, Dinlersoz, Foster & Zolas (2024) — FULL TEXT OBTAINED

**Source**: NBER Working Paper 31788 (66 pages), published version in *Journal of Economics & Management Strategy*, 33(2), 375–415.

#### Construct: AI Adoption (Binary)

**Variable name**: "Use AI" (binary indicator)

**Definition**: "We collapse different technologies and intensities of use into a single binary indicator of *any* use of AI in production." [McElheran et al. 2023, p.13, §3.3]

**What counts as "Use"**: Having responded with "In use for less than 5% of production or service", "In use for between 5%–25% of production or service" or "In use for more than 25% of production or service" for any of the five AI-related Business Technologies. [McElheran et al. 2023, p.47, Table 7 notes]

#### The Five AI Technologies Measured

From Table 2 [McElheran et al. 2023, p.42]:

1. **Machine learning**: "Computer algorithms that use data to improve their predictive performance without being reprogrammed."
2. **Machine vision**: "Technology used to provide image-based automatic inspection, recognition or analysis."
3. **Natural language processing**: "Technology that allows a computer to process human speech or text."
4. **Voice recognition software**: "Software that converts speech to text or executes simple commands based on a limited vocabulary or executes more complex commands when combined with natural language processing."
5. **Automated guided vehicles (AGV)**: "A computer-controlled transport vehicle that operates without a human driver. AGVs navigate facilities through the use of software and sensors."

These definitions were "validated during cognitive testing of the survey instrument" [McElheran et al. 2023, p.42, Table 2 notes].

#### Response Scale (Intensity)

Response categories (from Figure 1 notes, p.48):
- "Testing"
- "In use for less than 5% of production or service"
- "In use for between 5%–25% of production or service"
- "In use for more than 25% of production or service"

#### Data Source

- **Primary survey**: 2018 Annual Business Survey (ABS), US Census Bureau + NCSES/NSF [p.3, §1]
- Sent to ~850,000 firms nationwide [p.62, §B.1]
- Covers all non-farm employer businesses filing IRS 941, 944, or 1120 tax forms
- **Administrative linkage**: Longitudinal Business Database (LBD) [p.3, §1]

#### Sample Construction

[McElheran et al. 2023, pp.11–12, §3.1]

1. ABS–LBD linked sample: ~573,000 firms
2. Baseline sample: ~447,000 firms (AI questions minimally complete)
3. Weighted representation: over 4 million firms nationwide
4. Response rate: 69%

**Weighting**: stratified by 19 two-digit NAICS sectors × 12 firm size groups × 12 firm age groups [p.42, Table 1 notes]

#### Key Thresholds and Classification Rules

- **AI adoption (extensive margin)**: Binary — any AI technology "In use" (not merely "Testing") [p.13, §3.3]
- **Testing separately tracked**: 1.1% of firms [p.13, §3.3]
- **Intensity thresholds**: <5%, 5–25%, >25% of production [p.48, Figure 1 notes]
- **"More-intensive use"** = >25% of production [p.4, §1]
- **Startup definition**: firms 5 years old or younger [p.16, §3.6]
- **Employment-weighted adoption**: 18.2% vs 5.8% firm-weighted [p.14, §3.3]

#### Enabling Technology Co-adoption Measures

[McElheran et al. 2023, pp.12–13, §3.2]

1. **Digitization**: ≥1 type of information in digital format (65% prevalence)
2. **Cloud computing**: purchased cloud services for ≥1 IT function (43% prevalence)
3. **Robotics**: 1.3% adoption; 57.5% of robotics adopters also used AI [p.16, §3.5]

#### Regression Specification

Linear probability model (OLS) with: State-by-6-digit-NAICS industry fixed effects, firm age controls, owner gender controls, employment percentile indicators (6 categories), age percentile indicators (6 categories). [pp.43–47, Tables 4–7]

#### Revenue Growth Variable

"Revenue growth refers to the three-year average of the log-difference measure of annual revenue growth." [p.45, Table 6a notes]

#### Limitations

- Binary collapses intensity information [p.13]
- Single year of survey data (2017 reference period) [p.5]
- Self-reported survey responses
- Does not capture development of AI, only use in production [p.4]

---

### Zahra & Covin (1993) — PAYWALLED

**Citation**: Zahra, S.A. & Covin, J.G. (1993). Business Strategy, Technology Policy, and Firm Performance. *Strategic Management Journal*, 14(6), 451–478. DOI: 10.1002/smj.4250140605

**Extraction**: None. Technology posture scale items, measurement of technology leader vs. follower status, and archival operationalization methodology not accessible.

---

### Mithas & Rust (2016) — PAYWALLED

**Citation**: Mithas, S. & Rust, R.T. (2016). How Information Technology Strategy and Investments Influence Firm Performance. *MIS Quarterly*, 40(1), 223–245.

**Extraction**: None. IT spending/revenue ratio construction, 3-item classification thresholds for dual-emphasis / revenue-expansion / cost-reduction strategies, and Harte-Hanks/InformationWeek data derivation not accessible.

---

### Alekseeva, Azar, Giné & Samila (2026) — PAYWALLED

**Citation**: Alekseeva, L., Azar, J., Giné, M., & Samila, S. (2026). Artificial Intelligence Adoption and the Demand for Managerial Expertise. *Strategic Management Journal*. DOI: 10.1002/smj.70099

**Extraction**: Minimal. Google Scholar snippet confirms data source is "Lightcast job postings" and time period is "2010 to 2022" [Google Scholar snippet, accessed 2026-07-08]. Specific variable construction, AI skill taxonomy, matching methodology to Compustat firms, and classification thresholds not accessible.

---

## Section 2: Foundation 2 — Punctuated Equilibrium Operationalization

### Girod & Whittington (2015) — FULL TEXT OBTAINED

**Citation**: Girod, S.J.G. and Whittington, R. (2015). Change Escalation Processes and Complex Adaptive Systems: From Incremental Reconfigurations to Discontinuous Restructuring. *Organization Science*, 26(5), 1520–1535. DOI: 10.1287/orsc.2015.0993

**Source**: Accepted manuscript from University of Reading CentAUR repository.

#### Operational Definitions

**Restructuring** (discontinuous change): "change in the core principles of organizational structure, i.e. change in number of layers (vertical restructuring) or number and type of structural axes (horizontal restructuring) that affect the whole company (corporate level)." [p.12]

**Reconfiguration** (incremental change): "changes affecting particular structural units, for instance mergers or splits, but which leave the overall organization structure basically intact" [p.5]. Operationalized as "additions, mergers, transfers, splits and deletions of organizational units" [p.14].

#### Data Source for Coding

"Our measure of restructuring relies on annual report data, as in Romanelli and Tushman (1994) and Barkema and Schijven (2008)." [p.12]

For reconfigurations: "we use a wide range of data-sources, including annual reports, SEC 10Ks and press announcements from the Lexis-Nexis database (under the standard key terms 'reorganization', 'restructuring', 'appointments', 'executive moves', 'mergers and acquisitions', 'demergers' and 'spin-offs')." [p.14]

#### Title Coding to Hierarchical Levels

"we coded all top managerial titles into categories to reflect the horizontal principles of structure: business area; geography; functional; customers; and technology. CEO, President and COO titles were coded General Managers." [p.12]

"Likewise, we coded all titles to a maximum of four levels: Level 1 is the CEO level; Level 2 is the COO or President, if present; Levels 3 and 4 are operational (e.g., a business unit, a geography, etc.) and functional (e.g. marketing, finance, etc.)." [p.12]

"Consistent with findings that many COOs are appointed to prepare them for promotion to CEO (Hambrick & Cannella, 2004), we excluded heir-apparent COOs in order to avoid inflating the structural change ratio." [p.12]

#### Structural Change Ratio Calculation (3-step process)

**Step 1**: "we computed for each firm and year the proportion of titles in each category by dividing the number in each category by the total number of titles coded. Since each title is counted twice, once for the horizontal dimension and once for the vertical dimension of structure, we divided each proportion by two to obtain a sum of proportions adding to 1 (or 100 percent)" [p.12-13]

**Step 2**: "we subtracted the value of each title category from its corresponding value in the previous year, taking the absolute value difference" [p.13]

**Step 3**: "we obtained the structural change ratio by summing each difference for a given firm-year" [p.13]

**Worked example**: "the number of geographic titles increased from zero in 1998 to three in 1999: the proportion in this category (after dividing by two) became 0.14. Meanwhile, the proportion of business area titles dropped from 0.17 to 0.045... The sum of all the various differences gives Ford a 1999 structural change ratio of 0.63." [p.13]

"In our dataset, the change ratio varies between 0 and 0.97." [p.13]

#### The 0.30 Threshold (Key Quantitative Cutoff)

"In order to focus on discontinuous change, we established a threshold excluding minor changes. As in Romanelli and Tushman (1994), we converted the structural change ratio into a dummy variable 'restructuring,' coded 1 above a 0.30 cut-off." [p.13]

**Validation of the 0.30 threshold**:

1. **Interview validation**: "We interviewed fourteen senior executives at twelve of our firms regarding all changes above 0.20 on our ratio; for two more firms we interviewed the client partners of a large international consulting company. Our interviewees confirmed all changes above 0.30 as restructurings, but were more ambivalent about those below: these often reflected simple reconfigurations or ad hominem changes." [p.13]

2. **Documentary validation**: "We also read all sampled companies' annual reports for mentions of significant structural change, and searched the Lexis-Nexis database, using the key terms 'restructuring', 'reorganizations', 'appointments' and 'executive moves'." [p.13-14]

3. **Robustness checks**: "our robustness checks will include variations around that level [0.30]" [p.14]

#### How Reconfigurations Were Counted

"we count additions, mergers, transfers, splits and deletions of organizational units (Brown and Eisenhardt, 1998; Karim, 2006)... Where two or more units are involved, we count the process as a single reconfiguration." [p.14]

Examples [p.14-15]:
- Ford's merger of Latin American and North American operations = 1 reconfiguration
- Ford's creation of Automotive Consumer Services division = addition
- Ford's transfer of Direct Market business into Automotive Operations = transfer
- Ford's 1996 split of Automotive Components from Automotive Operations = split
- Ford's 1992 closure of Diversified Products Group = deletion

Maximum reconfigurations in one year: 17 (Allied Signal/Honeywell International, 2003) [p.19]
Average rate: 3.182 per firm-year [p.19]

#### Key Finding: The 6-Reconfiguration Perturbation Threshold

"At three reconfigurations a year (close to the mean rate of reconfiguration), the estimated probability of restructuring three years later is a modest 0.30. But a doubling of this rate to six raises the probability of subsequent restructuring to 0.58. Six is thus the threshold where a subsequent restructuring becomes more likely than not." [p.24]

#### Sample and Temporal Window

- Top 50 publicly-listed industrial firms from 1985 US Fortune 500, tracked through 2004 [p.11]
- 644 firm-year observations (reconfiguration bursts test); 555 (cumulated reconfigurations test) [p.19]
- Average firm restructures once every 6 years (0.156 per firm-year) [p.19]
- Most significant perturbation lag: 3 years [p.21]

---

### Romanelli & Tushman (1994) — PAYWALLED

**Citation**: Romanelli, E. and Tushman, M.L. (1994). Organizational Transformation as Punctuated Equilibrium: An Empirical Test. *Academy of Management Journal*, 37(5), 1141–1166. DOI: 10.2307/256669

**Extraction**: Not accessible. The multi-domain coding scheme (strategy, structure, power distributions) requires institutional access via JSTOR.

**Secondary description from Girod & Whittington (2015)**: R&T's structural change ratio is the precursor to G&W's method. The 0.30 threshold originates with R&T. R&T's coding of strategy and power distributions is NOT described in G&W 2015. [Girod & Whittington 2015, p.12-13 — secondary source]

---

### Lant, Milliken & Batra (1992) — PAYWALLED

**Citation**: Lant, T.K., Milliken, F.J., and Batra, B. (1992). The Role of Managerial Learning and Interpretation in Strategic Persistence and Reorientation. *Strategic Management Journal*, 13(8), 585–608. DOI: 10.1002/smj.4250130803

**Extraction**: Not accessible. The "strategy change + at least one other domain" rule, domain definitions, and detection method require institutional access via Wiley.

**From CrossRef abstract**: "applies a managerial learning framework to model decisions about strategic reorientation... examines past performance, managerial interpretations, and top management team characteristics as predictors of reorientation across two environmental contexts" [CrossRef API, accessed 2026-07-08]

---

## Section 3: Foundation 3 — Archival Organizational Structure Coding

### Albert, Eklund & Tang (2026) — PAYWALLED

**Citation**: Albert, D., Eklund, J.C., & Tang, L. (2026). A new organizational structure database: Examining structure through top management team compositions. *Strategic Management Journal*. DOI: 10.1002/smj.70029

**Partial extraction from Drexel repository page** [researchdiscovery.drexel.edu, accessed 2026-07-08]:
- Data: S&P 500 TMT compositions from **10-K, 20-F, and DEF 14A** SEC filings, 1993–2020
- Method: Generative AI categorization into **6 role groups** × **12 hierarchical levels**
- Original executive titles provided alongside AI-generated classifications
- Validation: Won **SMS Annual Conference Research Methods Paper Prize, 2024**

**NOT extractable**: The exact 6 role group names, exact 12 hierarchical level definitions, AI prompt/classification rules, manual validation protocol, inter-rater reliability metrics, ambiguous title resolution rules.

---

### Lee, Sridhar, Henderson & Palmatier (2015) — PAYWALLED

**Citation**: Lee, J.Y., Sridhar, S., Henderson, C.M., & Palmatier, R.W. (2015). Effect of customer-centric structure on long-term financial performance. *Marketing Science*, 34(2), 250-268. DOI: 10.1287/mksc.2014.0878

**Partial extraction from Google Scholar abstract** [accessed 2026-07-08]:
- Data: Fortune 500, **10-K and 10-Q** segment reporting, 1998–2010
- Method: Structure classified from how business segments are reported
- Key category: "customer-centric" = business units aligned with distinct customer groups

**NOT extractable**: Full taxonomy of structure categories, exact coding rules, borderline case resolution, inter-coder reliability, specific segment reporting fields examined.

---

### Larcker, Richardson & Tuna (2007) — PAYWALLED

**Citation**: Larcker, D.F., Richardson, S.A., & Tuna, I. (2007). Corporate governance, accounting outcomes, and organizational performance. *The Accounting Review*, 82(4), 963-1008. DOI: 10.2308/accr.2007.82.4.963

**Partial extraction from Stanford GSB page** [gsb.stanford.edu, accessed 2026-07-08]:
- Data: 2,106 firms, **proxy statements**
- Method: **39 structural governance measures** → exploratory PCA → **14 dimensions**

**NOT extractable**: The 39 variable list, variable operationalization, PCA rotation method, eigenvalue cutoff, variance explained, 14 component labels, missing data handling, governance index formula.

---

## Section 4: Retrieval Status Table

**UPDATE 2026-07-29**: All eight previously-paywalled spine papers have now been
obtained via institutional library access and are on disk in
`src/research_assistant/spaces/DBA/knowledge/thesis-spine-papers/`. The PDFs are
full-text (page counts verified with `read_binary.py --meta`). Full-text
methodology extraction into this log is the NEXT step (not yet done for the seven
added on 2026-07-29). Future agents/sessions: read these PDFs directly with
`python3 scripts/read_binary.py <path>`; do not re-attempt web retrieval.

| # | Paper | Journal | DOI | Status | On-disk filename (in thesis-spine-papers/) |
|---|-------|---------|-----|--------|--------------------------------------------|
| 1 | Alekseeva, Azar, Giné & Samila (2026) | Strategic Management Journal | 10.1002/smj.70099 | DOWNLOADED (Gold OA, 2026-07-15) | `alekseeva-2026-ai-adoption-managerial-expertise.pdf` |
| 2 | Albert, Eklund & Tang (2026) | Strategic Management Journal | 10.1002/smj.70029 | DOWNLOADED (Gold OA, 2026-07-15) | `albert-2026-org-structure-database.pdf` |
| 3 | Romanelli & Tushman (1994) | Academy of Management Journal | 10.2307/256669 | DOWNLOADED 2026-07-29 (27 pp) | `romanelli-tushman-1994-pe-empirical-test.pdf` |
| 4 | Lee, Sridhar, Henderson & Palmatier (2015) | Marketing Science | 10.1287/mksc.2014.0878 | DOWNLOADED 2026-07-29 (20 pp) | `lee-2015-customer-centric-structure.pdf` |
| 5 | Larcker, Richardson & Tuna (2007) | The Accounting Review | 10.2308/accr.2007.82.4.963 | DOWNLOADED 2026-07-29 (47 pp, published version) | `larcker-2007-governance-index-published.pdf` (SSRN working-paper version also on disk: `larcker-2007-governance-index-ssrn.pdf`) |
| 6 | Lant, Milliken & Batra (1992) | Strategic Management Journal | 10.1002/smj.4250130803 | DOWNLOADED 2026-07-29 (25 pp) | `lant-1992-managerial-learning-reorientation.pdf` |
| 7 | Zahra & Covin (1993) | Strategic Management Journal | 10.1002/smj.4250140605 | DOWNLOADED 2026-07-29 (29 pp) | `zahra-covin-1993-technology-posture.pdf` |
| 8 | Mithas & Rust (2016) | MIS Quarterly | 10.25300/MISQ/2016/40.1.10 | DOWNLOADED 2026-07-29 (25 pp) | `mithas-rust-2016-it-strategy-investments.pdf` |

### Full-text methodology already extracted into this log (no re-read needed)

| Paper | Source | Pages | Extraction Completeness |
|-------|--------|-------|------------------------|
| McElheran et al. (2024) | NBER Working Paper 31788 | 66 | Complete: 5 AI technologies, 4-level intensity scale, 850K-firm survey, binary variable, full sample construction, regression specs |
| Girod & Whittington (2015) | CentAUR repository (U. of Reading) | 42 (manuscript) | Complete: 3-step structural change ratio, 0.30 threshold with interview validation, title-to-level coding, reconfiguration counting rules. NOTE: published Organization Science version now also on disk (`girod-whittington-2015-change-escalation.pdf`, 17 pp) if page-cite alignment to the published article is needed. |

### Extraction COMPLETE (2026-07-29) — all six new papers extracted

Full-text extractions of the six papers downloaded 2026-07-29 are complete and
verified (headline claims spot-checked against source pages). The authoritative
per-paper records live in `data/drafts/_staging/`:

| Paper | Extraction file | Verified headline finding |
|-------|-----------------|---------------------------|
| Romanelli & Tushman (1994) | `extract-romanelli-tushman-results.md` | Revolutionary transformation = change in **all three** of strategy/structure/power distribution within a two-year window; 87% raw coder agreement; N=25 minicomputer firms |
| Lant, Milliken & Batra (1992) | `extract-lant-results.md` | Strategy change **necessary but not sufficient**; +≥2 of 3 supporting domains = reorientation; 88% intercoder; furniture (stable) + software (turbulent) |
| Zahra & Covin (1993) | `extract-zahra-covin-results.md` | "Aggressive technological posture" = 3-item 7-pt **continuous scale** (α=0.75); N=103 survey; mature manufacturing |
| Lee et al. (2015) | `extract-lee-results.md` | **Binary** customer-centric dummy from 10-K segment disclosures (SFAS 131); N=137 firms / 1,241 obs; <7% coder disagreement |
| Mithas & Rust (2016) | `extract-mithas-rust-results.md` | IT spending / revenue ratio; 3-way strategy dummy (cost/revenue/dual); InformationWeek+Compustat; N=511 |
| Larcker et al. (2007), published | `extract-larcker-published-results.md` | 39 governance vars → 14 PCA components; N=2,106; reconciled with SSRN version, no material difference; published cites supersede WP cites |

### THREE CORRECTIONS to prior abstract-level claims (full text overturned them)

Recorded so future drafts do not repeat the errors that were in v1 / the master
search file:

1. **Romanelli & Tushman terminology.** R&T's actual dependent-variable label is
   "**revolutionary / nonrevolutionary transformation**," NOT "reorientation /
   convergence." The reorientation/convergence vocabulary comes from the earlier
   Tushman & Romanelli (1985) framework. Attribute the vocabulary correctly.
2. **Zahra & Covin is NOT binary leader/follower.** It is a continuous 3-item
   aggressive-technology-posture scale. "Leader/follower" is a single semantic-
   differential item inside the scale, not the classification.
3. **Lee et al. is BINARY, not five-way.** The master search file described it as
   classifying firms into customer/product/geographic/functional/hybrid. The paper
   actually codes a binary customer-centric dummy (internally-aligned firms are
   bundled into the 0 category; pure-geographic dropped).

### Domain-count clarification (R&T 5 vs. 3)

Tushman & Romanelli's 1985 framework proposed FIVE deep-structure domains
(culture, strategy, structure, power distribution, control systems). The 1994
empirical test collected all five but dropped culture and control systems because
firms "reported information about them infrequently and inconsistently"
[Romanelli & Tushman 1994, p.1147]; only three were coded. This data-availability
reduction is a candidate methodological contribution for the thesis: whether 2026
archival sources (earnings-call NLP, richer disclosure) can recover the two
dropped domains is worth testing.

---

## Section 5: Consolidated Search History Log

Prof. Priyanka format: all retrieval attempts across three parallel agents, merged chronologically by foundation.

### Foundation 1 (AI Adoption Intensity) — 27 searches

| # | Query String | Database/Tool | Filters | Results | Full Text? |
|---|---|---|---|---|---|
| F1-1 | Zahra Covin 1993 "Business Strategy Technology Policy" SMJ pdf | Google Search | None | Blocked | No |
| F1-2 | Mithas Rust 2016 "How IT Strategy and Investments Influence Firm Performance" MISQ pdf | Google Search | None | Blocked | No |
| F1-3 | Alekseeva Azar Giné 2024 "AI adoption firm performance" job postings SMJ pdf | Google Search | None | Blocked | No |
| F1-4 | McElheran Li Brynjolfsson 2024 "AI Adoption in America" Census BTOS pdf | Google Search | None | Blocked | No |
| F1-5 | NBER Working Paper 31788 | NBER.org | None | Metadata found | Partial |
| F1-6 | SSRN abstract_id=4577568 (McElheran et al.) | SSRN | None | HTTP 403 | No |
| F1-7 | SSRN abstract_id=3672875 (Alekseeva et al.) | SSRN | None | HTTP 403 | No |
| F1-8 | Census CES-WP-23-55 | Census.gov | None | Wrong paper | No |
| F1-9 | Wiley DOI 10.1111/jems.12572 (McElheran JEMS) | Wiley | None | HTTP 402 | No |
| F1-10 | ResearchGate Zahra Covin 1993 | ResearchGate | None | HTTP 403 | No |
| F1-11 | MIS Quarterly Mithas Rust direct URL | misq.umn.edu | None | HTTP 403 | No |
| F1-12 | NBER w31788 PDF direct | nber.org/system/files/ | None | **Full PDF (66pp)** | **YES** |
| F1-13 | Wiley DOI 10.1002/smj.70099 (Alekseeva) | Wiley | None | HTTP 402 | No |
| F1-14 | Wiley PDF direct smj.70099 | Wiley pdfdirect | None | HTTP 402 | No |
| F1-15 | CEPR DP18161 | cepr.org | None | HTTP 403 | No |
| F1-16 | Google Scholar: Alekseeva Azar Giné "artificial intelligence" "firm growth" "job postings" | Google Scholar | None | Snippet: "Lightcast job postings" 2010–2022 | Metadata only |
| F1-17 | Google Scholar: Mithas Rust 2016 "information technology strategy" misq | Google Scholar | None | Confirmed, no OA PDF | No |
| F1-18 | Google Scholar: Zahra Covin 1993 | Google Scholar | None | Publisher link only | No |
| F1-19 | IZA DP 15567 | iza.org | None | Wrong paper | No |
| F1-20 | SSRN abstract_id=3734851 | SSRN | None | HTTP 403 | No |
| F1-21 | lisaalekseeva.github.io/research | Author page | None | HTTP 404 | No |
| F1-22 | joseazar.com/research | Author page | None | HTTP 404 | No |
| F1-23 | samiliresearch.com/research | Author page | None | DNS not found | No |
| F1-24 | Brynjolfsson.com/papers | Author page | None | HTTP 404 | No |
| F1-25 | MIT IDE PDF attempt | ide.mit.edu | None | HTTP 404 | No |
| F1-26 | Wiley DOI 10.1002/smj.4250140605 (Zahra) | Google Scholar→Wiley | None | Paywall | No |
| F1-27 | NBER w30426 (speculative Alekseeva) | NBER.org | None | Wrong paper | No |

### Foundation 2 (Punctuated Equilibrium) — 24 searches

| # | Query String | Database/Tool | Filters | Results | Full Text? |
|---|---|---|---|---|---|
| F2-1 | "Romanelli Tushman 1994 organizational transformation punctuated equilibrium AMJ" | Google Scholar | None | 1 PDF link (NTNU) | No (NTNU down) |
| F2-2 | "Girod Whittington 2015 Reconfiguration Restructuring Organization Science" | Google Scholar | None | 1 PDF link (Wiley) | No (HTTP 402) |
| F2-3 | "Lant Milliken Batra 1992 role of managerial learning SMJ" | Google Scholar | None | 1 link (Academia.edu) | No (HTTP 403) |
| F2-4 | NTNU repository direct link | WebFetch | Direct URL | ECONNREFUSED | No |
| F2-5 | Academia.edu download link | WebFetch | Direct URL | HTTP 403 | No |
| F2-6 | Wiley SMJ PDF link (smj.2543) | WebFetch | Direct URL | HTTP 402 | No |
| F2-7 | ResearchGate — Romanelli & Tushman 1994 | WebFetch | Direct URL | HTTP 403 | No |
| F2-8 | ResearchGate — Lant, Milliken & Batra 1992 | WebFetch | Direct URL | HTTP 403 | No |
| F2-9 | ResearchGate — Girod & Whittington | WebFetch | Direct URL | HTTP 403 | No |
| F2-10 | JSTOR stable/256669 | WebFetch | Direct URL | HTTP 403 | No |
| F2-11 | Google Scholar filetype:pdf "Romanelli Tushman" 1994 | Google Scholar | filetype:pdf | No direct PDFs | No |
| F2-12 | CrossRef API — DOI 10.2307/256669 | CrossRef REST API | None | Metadata, no OA link | No |
| F2-13 | CrossRef API — Lant Milliken Batra query | CrossRef REST API | title+author | DOI confirmed, abstract excerpt | No |
| F2-14 | CrossRef API — Girod Whittington query | CrossRef REST API | title+author | DOI 10.1002/smj.2543 confirmed | No |
| F2-15 | Semantic Scholar API — all 3 papers | Semantic Scholar | openAccessPdf field | HTTP 429 rate limited | No |
| F2-16 | Academy of Management Journals DOI page | WebFetch | Direct URL | HTTP 403 | No |
| F2-17 | Wiley abstract page (Lant et al.) | WebFetch | Direct URL | HTTP 402 | No |
| F2-18 | HBS faculty page (Tushman) | WebFetch | Direct URL | HTTP 403 | No |
| F2-19 | CORE.ac.uk — all 3 papers | WebFetch | Search | HTTP 403 (all) | No |
| F2-20 | CentAUR Reading — Girod Whittington 2015 OrgSci | WebFetch/CentAUR | Search | **PDF found** | **YES** |
| F2-21 | CentAUR Reading — Girod Whittington 2017 SMJ | WebFetch/CentAUR | Search | Not in repository | No |
| F2-22 | Babson College course page | WebFetch | Direct URL | HTTP 404 | No |
| F2-23 | Semantic Scholar paper pages (direct) | WebFetch | Direct URL | Empty pages | No |
| F2-24 | ProQuest openview link | WebFetch | Direct URL | HTTP 500 | No |

### Foundation 3 (Archival Org Structure) — 26 searches

| # | Query String | Database/Tool | Filters | Results | Full Text? |
|---|---|---|---|---|---|
| F3-1 | SSRN: "Albert" "Eklund" "Tang" organizational structure SEC | SSRN | Keyword | HTTP 403 | No |
| F3-2 | SSRN: "Lee" "Sridhar" "Henderson" "Palmatier" segment reporting | SSRN | Keyword | HTTP 403 | No |
| F3-3 | SSRN: "Larcker" "Richardson" "Tuna" corporate governance proxy | SSRN | Keyword | HTTP 403 | No |
| F3-4 | Albert Eklund Tang 2026 org structure SEC 10-K SSRN pdf | Google Search | None | HTTP 403 (blocked) | No |
| F3-5 | Lee Sridhar Henderson Palmatier 2015 "Marketing Science" org structure pdf | Google Search | None | HTTP 403 (blocked) | No |
| F3-6 | Larcker Richardson Tuna 2007 "Accounting Review" corporate governance PCA pdf | Google Search | None | HTTP 403 (blocked) | No |
| F3-7 | Albert Eklund Tang organizational structure SEC strategic management | Google Scholar | None | Found paper | No (paywall) |
| F3-8 | "Lee" "Sridhar" "Henderson" "Palmatier" marketing science 2015 | Google Scholar | None | Found paper | No (paywall) |
| F3-9 | Larcker Richardson Tuna 2007 corporate governance accounting review | Google Scholar | None | Found paper | No (paywall) |
| F3-10 | Wiley PDF: doi/pdf/10.1002/smj.70029 | Wiley | Direct PDF | HTTP 402 | No |
| F3-11 | Academia.edu: download/53383154/CG_Larcker.pdf | Academia.edu | Direct PDF | HTTP 403 | No |
| F3-12 | Wiley full HTML: doi/full/10.1002/smj.70029 | Wiley | Full text HTML | HTTP 402 | No |
| F3-13 | Wiley abstract: doi/abs/10.1002/smj.70029 | Wiley | Abstract | HTTP 402 | No |
| F3-14 | INFORMS abstract: doi/abs/10.1287/mksc.2014.0878 | INFORMS | Abstract | HTTP 403 | No |
| F3-15 | INFORMS supplemental: doi/suppl/10.1287/mksc.2014.0878 | INFORMS | Supplementary | HTTP 403 | No |
| F3-16 | Google Scholar "All 5 versions" Albert Eklund Tang | Google Scholar | Cluster search | 5 versions (all paywalled) | No |
| F3-17 | SSRN abstract_id=5005458 (Albert et al. WP) | SSRN | Direct | HTTP 403 | No |
| F3-18 | Drexel repository: Albert et al. institutional copy | Drexel Univ. | Repository | **Extended abstract obtained** | Partial |
| F3-19 | Stanford GSB: Larcker et al. faculty publications | Stanford GSB | Faculty page | **Summary obtained** | Partial |
| F3-20 | SSRN abstract_id=976566 (Larcker et al.) | SSRN | Direct | HTTP 403 | No |
| F3-21 | JSTOR: stable/4093084 | JSTOR | Direct | HTTP 403 | No |
| F3-22 | AOM Proceedings: Albert et al. 2025 conference | AOM | DOI link | HTTP 403 | No |
| F3-23 | ResearchGate: all three papers | ResearchGate | Search | HTTP 403 (all) | No |
| F3-24 | DOI redirect: 10.1002/smj.70029 | DOI.org → Wiley | Redirect | HTTP 402 | No |
| F3-25 | Semantic Scholar API: Albert Eklund Tang | Semantic Scholar | API | HTTP 429 rate limited | No |
| F3-26 | Foster UW faculty page: Palmatier research | U. Washington | Faculty page | HTTP 403/404 | No |

---

**Total searches executed**: 77 across 3 parallel agents
**Full texts obtained**: 2 (McElheran et al. via NBER; Girod & Whittington via CentAUR)
**Partial metadata obtained**: 3 (Alekseeva via Google Scholar snippet; Albert via Drexel repository; Larcker via Stanford GSB)
**Fully paywalled with no extractable detail**: 5 (Zahra & Covin; Mithas & Rust; Romanelli & Tushman; Lant, Milliken & Batra; Lee, Sridhar, Henderson & Palmatier)


---

## Full-Text Update — 2026-07-15

Three papers previously listed as PAYWALLED above have now been obtained (legal Gold/Green OA) and fully read. Their complete, page-cited methodology extractions live in separate result files (the merge-into-one-doc step timed out twice on output size; the extractions themselves are complete and are the authoritative record).

### Updated paywall tally
- **Full text obtained and extracted: 5** — McElheran et al. (2024), Girod & Whittington (2015), plus the three below.
- **Still paywalled (need institutional access): 5** — Romanelli & Tushman (1994), Lee et al. (2015), Lant et al. (1992), Zahra & Covin (1993), Mithas & Rust (2016).

### Newly extracted (full text, page-cited)

| Paper | Role | PDF in workspace | Extraction detail file |
|-------|------|------------------|------------------------|
| Alekseeva, Azar, Giné & Samila (2026), SMJ | AI adoption intensity measure (IV analogue): Lightcast job postings matched to firms, 2010-2022 | `spaces/DBA/knowledge/thesis-spine-papers/alekseeva-2026-ai-adoption-managerial-expertise.pdf` | `data/drafts/_staging/extract-alekseeva-results.md` |
| Albert, Eklund & Tang (2026), SMJ | Org structure database method (DV): TMT titles from 10-K/20-F/DEF 14A coded into role groups × hierarchical levels | `spaces/DBA/knowledge/thesis-spine-papers/albert-2026-org-structure-database.pdf` | `data/drafts/_staging/extract-albert-results.md` |
| Larcker, Richardson & Tuna (2007), SSRN WP | Governance index via PCA on proxy-statement variables [SSRN working-paper version; verify against published Accounting Review article] | `spaces/DBA/knowledge/thesis-spine-papers/larcker-2007-governance-index-ssrn.pdf` | `data/drafts/_staging/extract-larcker-results.md` |

The three extraction files contain the exact variable definitions, coding schemes, thresholds, and sample details with page citations. They should be read directly when drafting the methodology section.
