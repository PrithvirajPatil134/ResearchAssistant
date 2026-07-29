---
type: source
target_path: src/research_assistant/spaces/DBA/wiki/sources/alekseeva-2026-ai-adoption-managerial-expertise.md
title: "AI adoption and the demand for managerial expertise"
maturity: seed
tags: [ai-adoption, managerial-demand, shift-share-iv, job-postings, lightcast, skills, organizational-change, strategic-management, thesis-spine]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: DBA
applicable_to: [thesis, literature_review, research_paper]
draws_from: []
authors: ["Alekseeva, L.", "Azar, J.", "Giné, M.", "Samila, S."]
year: 2026
journal: "Strategic Management Journal"
volume: "1-27 (early view)"
pages: "1-27"
doi: "10.1002/smj.70099"
source_path: "knowledge/thesis-spine-papers/alekseeva-2026-ai-adoption-managerial-expertise.pdf"
ingested: 2026-07-28
---

# AI adoption and the demand for managerial expertise

Alekseeva, Azar, Giné & Samila (2026), *Strategic Management Journal*, DOI 10.1002/smj.70099. Open access under CC-BY. Received 30 September 2024, revised 20 March 2026, accepted 30 March 2026. [source_path, p.1]

## Research question and summary

The paper asks two questions: do firms that invest more in AI require more or fewer managers, and how does the nature of the managerial role change? [source_path, p.3] Using a US firm-year panel from 2010 to 2022 that links Lightcast job postings to Compustat financials, the authors find that firms with greater AI adoption post a higher share of managerial vacancies and more managerial vacancies, with the strongest relationships in manufacturing and among firms with higher R&D intensity. [source_path, p.1, p.3] Greater AI adoption is also associated with a shift in managerial skill requirements toward interpersonal and growth-oriented skills (stakeholder management, creativity, sales management) and away from routine administrative skills (budgeting, planning, staff management, customer service). [source_path, p.1]

## Independent variable: the AI Share measure (measurement approach)

This is the paper's firm-level AI-adoption-intensity measure and the reason it is a thesis-spine source. The measure is a **skill-based measure of AI adoption** built from job postings, motivated by the argument that many pre-generative AI technologies require specialized human capital to deploy. [source_path, p.8]

AI-related vacancies are identified using a **data-driven skill co-occurrence approach following Babina et al. (2024)**, which infers AI-relatedness from the data rather than defining AI skills ex ante. The procedure has four steps: [source_path, p.8]
1. Flag vacancies that explicitly mention core AI terms: "Machine Learning," "Natural Language Processing," "Computer Vision," or "Artificial Intelligence."
2. For each skill, compute the share of its occurrences in AI-flagged vacancies relative to its total occurrences, yielding a measure of that skill's AI-relatedness.
3. For each posting, calculate the average AI-relatedness across its listed skills, excluding rare skills.
4. Classify a vacancy as AI-related if this average exceeds a 10% threshold.

Firm-level AI adoption is then the proportion of a firm's annual postings that are AI-related: [source_path, p.10]

> AI Share(i,t) = Number of AI-related vacancies(i,t) / Total number of vacancies(i,t)

In the regressions, AI Share is multiplied by 100, so a coefficient is read as the change in the dependent variable for a 1%-point change in AI adoption. [source_path, p.13] Average AI Share rose more than tenfold between 2010 and 2022, from below 0.1% to about 1% of firms' vacancies (growth was slow initially, accelerated after 2012, and rose further after 2016). [source_path, p.10] The authors report that continuous or keyword-based alternatives to this measure give similar results (Supporting Information S1: Appendix Table A1 and Figure A1 — reported by authors, not in this PDF). [source_path, p.8, fn.8]

## Dependent variables

- **Managers Share**: the share of a firm's vacancies in management occupations, defined by 2-digit Standard Occupational Classification (SOC) code 11. Managers Share(i,t) = Number of vacancies in management occupation(i,t) / Total number of vacancies(i,t). [source_path, p.10]
- **Number of managerial vacancies** (used in log form as ln(managerial vacancies)). [source_path, p.10]
- **Managerial skill shares**: for skill j, Managerial Skill_j Share(i,t) = Number of managerial vacancies requiring skill j(i,t) / Total number of managerial vacancies(i,t). The analysis focuses on the 100 most prevalent managerial skills and on skill clusters constructed following Deming and Kahn (2018) and Deming (2021). [source_path, p.10]

The full dataset contains more than 16,000 unique skills. [source_path, p.10, fn.11] Because postings capture stated demand regardless of whether positions are filled, the authors interpret these as intended organizational needs rather than realized employment. [source_path, p.10-11]

## Empirical methodology

Baseline specification (Equation 1), estimated with within-firm variation: [source_path, p.13]

> Managers Share(i,t) = β·AI Share(i,t) + γ·X(i,t) + δ_i + θ_(s,t) + ε(i,t)

where δ_i are firm fixed effects, θ_(s,t) are 2-digit NAICS industry-year fixed effects, and X(i,t) is a vector of firm-level controls. All main specifications control for the natural logarithm of total vacancies. [source_path, p.13] Equation 2 replaces the dependent variable with managerial skill (or skill-cluster) shares. [source_path, p.14]

**Shift-share instrumental variable.** To address endogeneity from omitted time-varying firm factors and measurement error in AI Share, the authors use a shift-share (Bartik-style) IV. [source_path, p.14] The instrument interacts a firm's pre-period (2010) occupational structure with national occupation-level AI adoption rates: [source_path, p.3, p.14]

> B(i,t) = Σ over occupations o of s(i,o,2010) × AI Share(o,t)

where s(i,o,2010) is the share of occupation o in firm i in 2010 (measured at the 5-digit SOC level and held fixed) and AI Share(o,t) is the national AI adoption rate in occupation o at time t. [source_path, p.14] The identifying variation comes from firms' differential exposure to occupation-level AI adoption shocks driven by pre-existing workforce structures. [source_path, p.3] Industries that produce AI or provide AI implementation services (2-digit NAICS 51 and 54) are excluded. [source_path, p.11, p.14]

**Instrument diagnostics** (following Borusyak et al. 2022, 2025): first-stage coefficient on the instrument is 1.087 with a first-stage F-statistic of 89.8, well above the conventional relevance threshold of 10. [source_path, p.15] The inverse Herfindahl-Hirschman Index for exposure shares is 778, the largest 5-digit SOC weight is 0.5%, and there are 782 five-digit SOC codes, supporting the claim that the instrument aggregates many distinct shocks. [source_path, p.12, p.15] Pre-trend analyses using 2007-2010 vacancy data find no differential pre-period trends between higher- and lower-exposure firms (Supporting Information S1: Appendix Table A6 — reported by authors). [source_path, p.15] The authors state explicitly that they cannot fully rule out violations of the exclusion restriction and therefore do not interpret the IV estimates as definitive causal effects. [source_path, p.3, p.15]

## Data and sample

Lightcast (formerly Burning Glass Technologies) online job postings covering nearly 388 million US vacancies in 2007 and from 2010 to 2022. [source_path, p.8] After dropping postings without employer names and internships, 277 million vacancies are matched to Compustat firms. [source_path, p.11] Matching uses firm names with manual verification, augmented by a Bing Web Search API algorithm following Autor et al. (2020). [source_path, p.11, fn.13] The final regression sample is a balanced panel of firms appearing every year 2010-2022 with at least 50 vacancies per year and full Compustat characteristics for 2011-2022: **823 unique firms, 9,876 firm-year observations, and about 51 million vacancies**; main regressions cover 2011-2022. [source_path, p.11] All ratios are winsorized at the 1st and 99th percentiles. [source_path, p.13] Mean AI Share is 0.5% (SD 1.2%) and mean Managers Share is 16.1% (SD 9.4%). [source_path, p.12]

## Key findings

- **Level of managerial demand.** OLS: a 1%-point increase in AI Share is associated with a 0.3%-point increase in Managers Share (about 2% relative to the mean) and about 3% more managerial vacancies. IV: a 1%-point increase in AI Share is associated with a 1.2%-point increase in Managers Share (about 7.5%) and about 9% more managerial vacancies. [source_path, p.16] Moving from zero AI adoption to the 95th percentile of AI Share corresponds to roughly a 26% increase in managerial vacancies. [source_path, p.16] IV estimates exceed OLS, which the authors attribute to attenuation bias from measurement error and offsetting omitted factors. [source_path, p.16, fn.18]
- **Industry heterogeneity.** The association is strongest in manufacturing: IV estimates imply a 1.8%-point increase in Managers Share (about 10%) and a 12% increase in managerial vacancies per 1%-point AI Share. Finance, Trade, and Other show less consistent, imprecise patterns (the Trade first-stage F-statistic is below conventional thresholds). [source_path, p.17]
- **Firm heterogeneity.** The AI Share × R&D-intensity interaction is positive and precisely estimated (stronger association in more R&D-intensive firms). Interactions with baseline computer-skill intensity and with firm size (log sales) are negative and precise (weaker association in firms with codified digital routines and in larger firms). Data-skill and software-skill interactions are imprecise or near zero. [source_path, p.17-18, p.20]
- **Managerial occupation type.** No single 3-digit SOC managerial category (executives 11-1, marketing/sales 11-2, operations 11-3, other 11-9) shows a notably larger increase; the rise is broad-based across management functions. [source_path, p.20]
- **Skill content.** Positively associated with AI adoption: sales, sales management, sales goals, procurement, listening, written communication. Negatively associated: budgeting, Microsoft Office proficiency, staff management, customer service, strategic planning, physical abilities, and building effective relationships. [source_path, p.20] At the cluster level, demand declines for people-management, finance, and decision-making clusters, is stable for customer-facing/cognitive/communication clusters, and rises for creativity. [source_path, p.22] Patterns are most pronounced in manufacturing, shifting toward creativity, teamwork/collaboration, stakeholder management, training programs, and sales-related skills. [source_path, p.22]
- **Wages.** AI Share is positively correlated with managerial pay in OLS, but the IV estimate is close to zero, and there is no increase in relative managerial-to-non-managerial wages, consistent with role reconfiguration rather than a uniform rise in the price of managerial work. [source_path, p.23-24]

## Contributions and scope conditions

The paper makes two contributions: (1) large-sample, firm-level evidence that greater AI adoption is associated with higher managerial intensity, varying across organizational types; and (2) evidence of systematic changes in the skill content of managerial demand. [source_path, p.4] It complements and extends Babina et al. (2024), who study AI adoption's relationship with firm growth and product innovation using similar data. [source_path, p.4]

**Scope condition (important for the GenAI thesis thread).** The analysis focuses on the diffusion of **predictive AI** (systems that classify, forecast, and optimize using machine learning, computer vision, and NLP) and predates the widespread adoption of **generative or agentic AI**. The authors state their findings speak most directly to predictive AI and may not fully capture the implications of newer generative/agentic tools. [source_path, p.4, p.24]

## AI-tool use disclosure

The authors disclose that AI tools (specifically Claude Opus 4.5 and GPT-5.2) assisted in editing some parts of the text, and were not used in design, data work, analysis, or interpretation of results. [source_path, p.15, fn.17]

## Data availability

Data supporting the findings are available from Lightcast under license; restrictions apply. [source_path, p.24]

## Relevance to the DBA thesis

The existing DBA thesis synthesis is on organizational restructuring and GenAI. [wiki/syntheses/dba-thesis-proposal-2026.md] This paper supplies a validated, published template for a firm-level AI-adoption-intensity independent variable (the AI Share measure) and a shift-share IV identification strategy, both directly usable as measurement and methodology references in the literature review and empirical-study sections. The predictive-vs-generative scope condition (above) is a caveat the thesis must carry when borrowing this measure for a GenAI-focused argument. [source_path, p.4, p.24]
