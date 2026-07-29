---
type: source
target_path: src/research_assistant/spaces/DBA/wiki/sources/larcker-2007-governance-index-ssrn.md
title: "Corporate Governance, Accounting Outcomes, and Organizational Performance (SSRN working paper)"
maturity: seed
tags: [corporate-governance, principal-component-analysis, index-construction, construct-measurement, earnings-quality, archival]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: DBA
applicable_to: [thesis, literature_review, research_paper]
draws_from: []
authors: ["Larcker, D.F.", "Richardson, S.A.", "Tuna, İ."]
year: 2007
journal: "SSRN Working Paper (abstract 976566); published version in The Accounting Review"
volume: "n/a (working-paper version, revised February 21, 2007)"
pages: "~71pp (working-paper PDF)"
source_path: "knowledge/thesis-spine-papers/larcker-2007-governance-index-ssrn.pdf"
ingested: 2026-07-28
---

## Provenance Note (REQUIRED — read before using)

This is the SSRN working-paper version (abstract 976566), "Revised February 21, 2007" [p.1]. The header on every page reads "Electronic copy available at: https://ssrn.com/abstract=976566". A published version appears in The Accounting Review; the working-paper version may differ from the published article in sample counts, table numbering, and reported statistics. Any claim needed for the thesis at final-citation stage should be re-verified against the published article. Do NOT cite specific Accounting Review volume/issue/page numbers from this source page — those details are not in the extracted PDF. [UNSOURCED: published-version bibliographic details].

## Why this paper is in the DBA wiki

This is a thesis-spine paper: the empirical backbone for how a governance construct can be built from observable structural indicators rather than a single proxy or a naively summed index. The method (exploratory PCA to reduce many indicators to a smaller set of interpretable, reliability-checked indices) is the reusable contribution. [p.4-5]

## Research problem

Empirical work linking corporate governance to accounting and economic outcomes has not produced a consistent set of results. The authors argue the mixed results are partly a measurement problem: governance is a complex, multi-dimensional construct, but most studies use either a single indicator or an arbitrary index (they name the Gompers, Ishii & Metrick 2003 "G-score" as an example of a naively summed index). A single indicator for a complex construct introduces measurement error that makes regression coefficients inconsistent; a naive sum of indicators measuring different underlying constructs is hard to interpret and carries substantial measurement error. Using a limited subset of governance dimensions also creates correlated-omitted-variable problems. [p.3-4]

The paper is explicitly exploratory. The authors state there is no well-developed theory of the multi-dimensional nature of corporate governance to specify which characteristics belong in a structural model, so they treat the work as an initial attempt to describe linkages between multiple governance measures and outcome variables. [p.4-5]

## Sample and data

Final sample of 2,106 U.S. firms with complete data, formed by merging two commercial datasets: TrueCourse Inc. anti-takeover data (n = 3,651; U.S.-incorporated firms in major indices) and Equilar Inc. board/committee/ownership data (fiscal year ends June 2002 to May 2003; n = 3,000). The sample is about 70 percent of the market capitalization of the Russell 3000 as of end-2003 and skews toward larger, more profitable firms with lower book-to-market and more analyst following than the rest of Compustat. Institutional and activist ownership come from Spectrum 13F files; debt and preferred stock from Compustat; anti-takeover data from TrueCourse. [p.7-10]

## The 39 indicators, in seven categories

Governance indicators are collected in seven general categories: board-of-director characteristics, stock ownership by executives and board members, stock ownership by institutions, stock ownership by activist holders, debt and preferred-stock holdings, compensation-mix variables, and anti-takeover devices. [p.8] Representative indicators include board and committee meeting counts and sizes, fraction of insider/affiliated directors, busy-director and old-director fractions, lead-director and insider-chairman indicators, block-holder and activist ownership, debt-to-market and preferred-to-market ratios, the long-term vs accounting compensation mix, and anti-takeover devices (staggered board, supermajority, state of incorporation, unequal voting, poison pill). [p.8-11]

## The PCA index-construction method (the core methodology)

Principal component analysis (PCA) is used in exploratory mode to find the underlying dimensions of the 39 indicators. The construction procedure:

1. Run exploratory PCA on the 39 individual governance indicators. [p.12]
2. Retain all factors with an eigenvalue greater than unity (Kaiser criterion). This yields 14 factors retaining 61.7 percent of the total variance in the original data. [p.12]
3. Rotate the retained 14-factor solution using an oblique rotation that lets the factors be correlated, to improve interpretability. [p.12]
4. Assign indicators to factors: a variable is associated with a factor when its loading (the correlation between factor and indicator) exceeds 0.40 in absolute value AND is statistically significant at conventional levels. Significance uses bootstrapping — 1,000 samples with replacement — on the rotated 14-factor solution. [p.12]
5. Name each factor from the character of its associated indicators (e.g., the first factor loads on activist measures positively and outside-director ownership negatively, so it is named "Active"). The solution is described as interpretable with no significant cross-loadings. [p.12-13]
6. Compute index scores. For most factors the score is the average of the equal-weighted sum of the standardized indicators associated with that factor (citing Grice and Harris 1998). Because inputs are standardized, the mean score of every index equals zero. [p.13-14, Table 4 Panel A p.56]

**Four exception factors** contain substitute mechanisms or a mix of positive and negative loadings, so their scores explicitly encode the substitutability [p.14, Table 4 note p.56]:
- Active = (standardized #Activists + %Activists Own − %Outsiders Own) / 3
- Anti-Takeover I = (Staggered Board + Poison Pill − %Affiliated Own) / 3
- Compensation Mix = (%Accounting Mix − %Long Term Mix) / 2
- Lead Director = (Lead Director − Insider Chairman) / 2

## Reliability and construct validity of the indices

Reliability is measured with Cronbach's alpha per index. Mean (median) coefficient alpha is 0.532 (0.568). The authors concede these are lower than the Nunnally (1967) benchmarks but argue low reliability is common in early-stage measurement development, and that multi-indicator indices should still beat the single indicators common in the literature. For construct validity, none of the confidence intervals for correlations among the 14 indices include unity at conventional significance, which they read as evidence the indices are statistically distinct. [p.14]

## The 14 governance dimensions (Table 3, loadings; Table 4, variance)

In order of variance explained [Table 4 Panel A, p.56; loadings Table 3, p.55]:

| Factor | % variance | Illustrative loading indicators |
|---|---|---|
| Active | 10.72 | #Activists (0.654), %Activists Own (0.625), %Outsiders Own (−0.665) |
| Block | 7.41 | %Block Own (0.985), #Block (0.877), %Largest (0.848) |
| Affiliated | 5.86 | %AC Affiliated (0.822), AC Chair Affiliated (0.824), %CC Affiliated (0.627), CC Chair Affiliated (0.536) |
| Insider Appointed | 5.43 | %Affiliated Appointed (0.752), %Outsiders Appointed (0.768) |
| Compensation Mix | 4.85 | %Accounting Mix (0.896), %Long Term Mix (−0.824) |
| Meetings | 3.87 | #AC Meetings (0.762), #CC Meetings (0.678), #Board Meetings (0.695) |
| Lead Director | 3.53 | Lead Director (0.842), Insider Chairman (0.441) |
| Anti-Takeover I | 3.28 | Poison Pill (0.665), Staggered Board (0.476), %Affiliated Own (−0.517) |
| Old Directors | 3.03 | %Old Outsiders (0.688), %Old Insiders (0.605), %Old Affiliated (0.563) |
| Debt | 2.94 | Debt to Market (0.778), Preferred to Market (0.804) |
| Insider Power | 2.84 | %Executives Own excl. Top (0.737), %Top Exec Own (0.720), %Board Inside (0.467), Unequal Voting (0.396) |
| Board Size | 2.73 | CC Size (0.884), AC Size (0.872), Board Size (0.693) |
| Anti-Takeover II | 2.61 | State Incorporated (0.792), Supermajority (0.625) |
| Busy Directors | 2.61 | %Busy Affiliated (0.698), %Busy Insiders (0.452), %Busy Outsiders (0.424) |

## "Good" vs "bad" governance classification

To sign the outcome tests, the authors classify Board Size, Affiliated, Insider Appointed, Insider Power, Anti-Takeover I, Anti-Takeover II, Old Directors, and Busy Directors as increasing in "bad" governance, and Compensation Mix as weakly increasing in "bad." Active, Block, Meetings, Debt, and Lead Director are classified as increasing in "good" governance. They then make the traditional assumption that higher governance is associated with better accounting and economic outcomes. [p.15-16]

## Outcome tests and findings

The 14 indices are entered as regressors against four outcomes. Two model forms are used: equation (1) with control variables (governance assumed not to affect controls, giving conservative estimates) and equation (2) governance-only (which captures total direct-plus-indirect effects). [p.16-17]

- **Abnormal accruals** (earnings-quality proxy) via an extended modified Jones model: TA = α + β1(ΔSales−ΔREC) + β2 PPE + β3 BM + β4 CFO + ε, estimated by two-digit SIC group with ≥10 firms; residual = Abnormal Accruals. [p.18-19; Table 5 note p.59] Association with the indices is mixed and often opposite to prediction; adjusted R² is 1.60% (signed) and 5.34% (absolute). [p.20-21, Table 5 p.60-61]
- **Accounting restatements** (logistic): virtually no relation to the governance indices; governance-only pseudo-R² about 2.0%. [p.31-33, Table 6 p.63]
- **Future operating performance** (ROA t+1): governance-only adjusted R² 14.2%; Active and Compensation Mix are positive and significant; Debt is significant with the "wrong" sign. [p.33, Table 7 p.65]
- **Future excess stock returns** (Alpha, the intercept from a four-factor MKT/SMB/HML/UMD model): governance-only R² about 2.0%; Lead Director and Insider Power significant in the predicted direction; Compensation Mix, Insider Appointed and Debt also significant. [p.30-31, Table 8 p.67, note p.67]

Headline summary: firms with more block-holders, a compensation mix weighted toward accounting performance, a lead director, smaller boards, and fewer busy directors show superior future operating performance; higher future excess returns come with an accounting-weighted compensation mix, a lead director, and low insider power. Structural governance indicators explain "accounting manipulations" only modestly but have some ability to explain future operating and stock-price performance. [p.6]

## Robustness / extensions

- **Recursive partitioning (CHAID)** is run as a non-linear, interaction-capturing alternative to OLS. Results largely agree with the regressions, which the authors read as evidence their findings are not an artifact of method variance. Board Size is the first split for non-directional abnormal accruals; operating-performance partitioning gives R² of 16.2%. [p.31-34, Tables 5-8]
- **Single-period concern**: the data cover one year coinciding with the Sarbanes-Oxley Act of 2002. Using external time-series data (IRRC 1990-2004, The Corporate Library ratings, Linck-Netter-Yang 2005) they argue structural governance measures are temporally stable, so the single year is likely representative. [p.34-37, p.7 endnote 7]
- **Endogeneity**: governance choices are endogenous. They regress each index on firm size (log market value of equity) and two-digit-SIC industry, split the residual into positive and negative parts, and re-run the outcome models. Results are similar; operating performance is notably lower for firms whose governance is below the size-and-industry benchmark. [p.37-40]

## Limitations the authors state

Single year of data limiting generalizability; endogenous governance choices; possible non-linearities beyond linear models; potential correlated-omitted-variable bias and measurement error; and the acknowledgment that they do not have perfect measures of governance. Reliability (Cronbach's alpha) is modest. The indices are framed as an initial step toward reliable and valid governance measures, with refinement left to future research. [p.40-42]

## Relevance to the DBA thesis

Supports the thesis's construct-measurement strategy: building a multi-indicator governance construct from observable/archival proxy-statement variables via dimension reduction rather than a single proxy. Sits alongside the other construct-construction references logged in the thesis synthesis (Zahra & Covin 1993; Mithas & Rust 2016). [syntheses/dba-thesis-proposal-2026.md, line 274, 280-281]
