---
title: "Relative Strategic Emphasis and Firm-Idiosyncratic Risk: The Moderating Role of Relative Performance and Demand Instability"
type: source
maturity: seed
created: 2026-05-07
last_updated: 2026-05-07
originating_space: QNTR
applicable_to: [research_paper, term_paper]
schema_version: "1.0"
sources:
  - path: "knowledge/Reference Material/2017 - (JM) Han et al - Relative Strategic Emphasis and Firm Idiosyncratic Risk.pdf"
    type: pdf
authors:
  - "Han, K."
  - "Mittal, V."
  - "Zhang, Y."
year: 2017
journal: "Journal of Marketing"
volume: "81(4)"
pages: "25-44"
ingested: 2026-05-07
tags: [gap-table, positioning, panel-data, journal-of-marketing]
draws_from: []
---

## Summary

This paper examines how a firm's relative strategic emphasis on value appropriation (advertising) versus value creation (R&D) is associated with firm-idiosyncratic risk, moderated by relative performance and demand instability. Using panel data of 13,880 firm-year observations from 2,403 firms across 59 industries over 15 years (2000-2014), the authors find that higher strategic emphasis on value appropriation reduces idiosyncratic risk, but this effect is contingent on both relative performance and demand instability.

The paper is referenced in Prof. Prashar's May 5, 2026 feedback as a model for Table 1 structure: a literature positioning table where the final row shows the current study's contribution relative to prior work.

## Key Arguments

1. **Joint rather than separate examination**: Prior research examined value creation (R&D) and value appropriation (advertising) separately. This study examines them jointly as "relative strategic emphasis" because "resource limitations may preclude firms from simultaneously pursuing both value-appropriation and value-creation strategies in an unconstrained manner" (p. 25).

2. **Risk rather than return**: Most prior studies focused on firm return as the outcome. This study focuses on firm-idiosyncratic risk because "executives today have a keen interest in reducing financial risk rather than focusing exclusively on return maximization" (p. 25).

3. **Contingency factors**: Unlike prior studies, the paper examines moderators: relative performance (firms exceeding or falling short of a reference point) and demand instability (environmental uncertainty). These frame executive perception and resource allocation decisions (pp. 27-28).

4. **Core finding**: Firms with higher strategic emphasis on value appropriation (vs. value creation) experience lower idiosyncratic risk. This association is weaker when firms have larger positive or negative relative performance. Industry demand instability amplifies these interactive effects (p. 2).

## Methodology

**Research Design**: Panel data regression with endogeneity controls

**Sample** (p. 12):
- 13,880 firm-year observations
- 2,403 firms
- 59 industries
- 15-year period (2000-2014)
- Data sources: Compustat, CRSP

**Key Variables**:
- DV: Firm-idiosyncratic risk (stock return volatility after removing market and industry effects)
- IV: Relative strategic emphasis = (Advertising - R&D) / (Advertising + R&D), following Mizik and Jacobson (2003) (p. 30)
- Moderators: Positive relative performance, Negative relative performance, Demand instability
- Controls: Firm size, leverage, sales growth, industry concentration, diversification, past risk

**Endogeneity Treatment** (pp. 33-35):
- Control function approach (Wooldridge, 2010; Petrin and Train, 2010)
- Heckman selection model (inverse Mills ratio) for sample selection bias
- Industry-average strategic emphasis as instrument
- Bootstrapped standard errors (1,000 samples) to correct for two-stage estimation
- Standard errors clustered at firm level

**Model Specification** (p. 35): Full model includes main effects, two-way interactions, three-way interactions, control function, inverse Mills ratio, year fixed effects, and industry fixed effects.

## Findings

All four hypotheses supported (pp. 35-37):
- **H1**: The negative association between strategic emphasis on value appropriation and risk is weaker when firms have larger positive relative performance (interaction: beta = .042, p < .01)
- **H2**: Same weakening effect for larger negative relative performance (beta = .015, p < .01)
- **H3**: The interactive effect of strategic emphasis and positive relative performance is stronger under high demand instability (three-way interaction: beta = 4.297, p < .01)
- **H4**: Same amplification for negative relative performance under high demand instability

## Table 1 Structure (Critical for Gap-Table Positioning)

Table 1 (pp. 26-27) presents a literature positioning table with the following structure:

**Columns**:
1. Study citation (Author, Year)
2. Advertising (VA) - checkmark if studied
3. R&D (VC) - checkmark if studied
4. Relative Strategic Emphasis on VA - checkmark if studied
5. Risk - checkmark if DV includes risk
6. Return - checkmark if DV includes return
7. Moderator(s) - what contingency factors are examined

**Row organization**:
- Main section: "Focus on Advertising, R&D, or Relative Strategic Emphasis" (23 studies listed)
- Secondary section: "Advertising and/or R&D as Covariates" (17 studies listed)
- **Final row**: "Current study" with checkmarks in all relevant columns and the specific moderators being tested

**Positioning technique**: The table visually demonstrates that no prior study has examined all three elements (relative strategic emphasis, risk, and dual moderators) simultaneously. The final row fills the gap. Each column acts as a dimension of the research space; the current study's row shows it occupies a previously empty cell.

**Note at bottom**: Superscript "a" marks studies that also examine advertising/R&D/strategic emphasis as a moderator (not focal IV). The table distinguishes between studies where these are the focal independent variable versus covariates.

## Relevance to Research

1. **Table 1 as positioning model**: Prof. Prashar's May 5 feedback explicitly recommends this paper's Table 1 structure for positioning the agentic AI governance study. The technique: list prior studies in rows, define key dimensions as columns (IV type, DV type, moderators, methodology), and show the current study fills an unoccupied cell.

2. **Panel data methodology**: The 13,880 firm-year observation structure across 2,403 firms provides a methodological template for the quantitative Phase 2. If firm-level governance maturity data can be assembled (via survey or secondary data), a similar panel approach could test governance-to-performance links.

3. **Endogeneity treatment**: The control function approach combined with Heckman selection addresses the same endogeneity concern that will arise in governance-performance research (firms that govern AI well may be systematically different from those that do not).

4. **Contingency approach**: The moderator structure (relative performance x demand instability) parallels the agentic AI governance study's need to examine boundary conditions on the governance-performance relationship.

5. **Risk as DV**: Strengthens the argument for including enterprise risk (not just financial performance) as a dependent variable, which is already central to the term paper's framework.

## Limitations

- Advertising and R&D expenditures are proxies for value appropriation and creation; they do not capture all strategic resource allocation decisions (p. 30)
- Compustat data excludes private firms and firms with missing data (sample selection concerns partially addressed by Heckman correction)
- Industry classification (two-digit SIC codes) may be too coarse for capturing competitive dynamics
- 2000-2014 period predates the current AI-driven transformation of both R&D and marketing

## Key Quotes

- "Firms may allocate scarce resources to two fundamental strategic processes: value creation and value appropriation. The relative investment in these processes (i.e., a firm's relative strategic emphasis) may be associated with firm-idiosyncratic risk." (p. 25)
- "Executives today have a keen interest in reducing financial risk rather than focusing exclusively on return maximization." (p. 25)
- "In many cases, focusing only on maximizing returns while ignoring risk may mislead managers into adopting pernicious strategies." (p. 25)
- "Returns from exploration are systematically less certain, more remote in time, and organizationally more distant from the locus of action and adaption." (p. 27, citing March, 1991)
