---
type: source
title: "Evaluating SEM Model Fit with Small Degrees of Freedom"
maturity: seed
tags: [sem, structural-equation-modeling, model-fit, fit-indexes, rmsea, srmr, cfi, degrees-of-freedom, small-df, cutoff-criteria, confirmatory-factor-analysis, monte-carlo-simulation, quantitative-methods]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [research_paper, thesis, conference_paper, term_paper]
draws_from: []
authors: ["Shi, Dexin", "DiStefano, Christine", "Maydeu-Olivares, Alberto", "Lee, Taehun"]
year: 2021
journal: "Multivariate Behavioral Research"
volume: ""
pages: ""
doi: "10.1080/00273171.2020.1868965"
source_path: "src/research_assistant/spaces/QNTR/knowledge/Key method readings/2021 - Shi et al - Evaluating SEM model fit with small df.pdf"
ingested: 2026-07-28
target_path: src/research_assistant/spaces/QNTR/wiki/sources/shi-2021-sem-fit-small-df.md
---

## What this source is

A Monte Carlo simulation study asking which structural equation modeling (SEM) fit indices remain trustworthy when a model has small degrees of freedom (df). The paper reports that the root mean square error of approximation (RMSEA) performs sub-optimally with small df, often rejecting correctly specified or closely fitting models, and it recommends relying instead on the standardized root mean square residual (SRMR) and the comparative fit index (CFI) in that regime [source, p.2 (abstract)].

It is best read as the small-df refinement and partial critique of the fixed-cutoff regime established in `hu-bentler-1999-cutoff-criteria-fit-indexes.md`. Shi et al. do not reject the conventional cutoffs; they show the cutoffs behave differently across the three indices as df shrinks, and they cite Hu & Bentler (1999) for the conventional values of RMSEA close to .06, SRMR close to .08, and CFI at or above .95 [source, p.3; p.5; p.6].

## The problem with RMSEA at small df

RMSEA divides the discrepancy function by df in its formula, so it penalizes model complexity through df [source, p.3]. For a fixed nonzero discrepancy, the population RMSEA rises as df falls [source, p.3, Equation 1]. Consequently, at very small df a genuinely close-fitting model can produce a large population RMSEA, and the conventional cutoff can mislead at the population level [source, p.3]. Prior work reached a blunt conclusion the paper quotes directly: Kenny, Kaniskan, & McCoach (2015, p.486) "recommend not computing the RMSEA for small df models, especially those with small sample sizes" [source, p.3].

Small-df models are common in applied social science. The paper gives concrete cases: a three-wave latent growth model has df=1; the cross-lagged panel model and random intercept cross-lagged panel model have df=4 and df=1 respectively; and a one-factor model fit to a four-item short scale has only df=2 [source, p.3].

## Simulation design

- Correctly specified conditions fit a one-factor confirmatory factor analysis (CFA) model to one-factor population data; misspecified conditions fit a one-factor model to two-factor population data [source, p.5].
- Four factors were manipulated, giving 135 conditions = 5 sample sizes x 3 model sizes x 3 factor-loading levels x 3 inter-factor correlations, with 5,000 replications per condition generated with the simsem package in R [source, p.7-8].
- Model size: number of observed variables p = 4, 8, 12, giving fitted-model df from 2 (p=4) to 54 (p=12) [source, p.6].
- Standardized factor loadings: low (.40), medium (.60), high (.80) [source, p.6].
- Sample sizes: 50, 100, 200, 500, 1,000 [source, p.6].
- Misspecification via inter-factor correlation rho: correctly specified (rho=1.0), minor misfit (rho=0.90), severe misfit (rho=0.60); a smaller rho means greater misspecification [source, p.7].
- Estimation was maximum likelihood (ML) using the lavaan package; only converged replications were analysed, and an eta-squared above 5% flagged practically important sources of variability [source, p.8].
- The paper studies both a biased sample SRMR and an asymptotically unbiased sample SRMR (Maydeu-Olivares, 2017), and two sample CFI estimators, the usual ML estimator and Lai's (2019a) bias-corrected estimator [source, p.4; p.5-6].

## Key findings

- At the population level, holding misspecification fixed, RMSEA rises sharply as df falls, while population SRMR and CFI are far less sensitive to df. In the analysis-of-variance decomposition, model size (df) accounted for eta-squared = 0.07 of population RMSEA variability but under 0.01 for both population SRMR and population CFI [source, p.7; p.10; p.19].
- Applying the conventional RMSEA cutoff of .06 to small-df models over-rejects good models: with minor misspecification (rho=.90), N=200, high loadings (k=.80), df=2, sample RMSEA exceeded .06 in 80% of replications [source, p.15]. Even at df=2 with N=1,000, sample RMSEA still rejected close-fitting (rho=.90) models about 20% of the time [source, p.24].
- RMSEA also lacked power to reject severely misspecified models when loadings were low: at rho=.60, N=1,000, k=.40, df=2, only 37% of sample RMSEA values exceeded .06 [source, p.15].
- SRMR and CFI performed better with small df. As a rule of thumb, once N reaches 200 the unbiased sample SRMR and the ML-based sample CFI can be used with conventional cutoffs even for very small models (df=2), rejecting severe misspecification with power above 80% and Type I error below 10%, provided factor loadings are not very low [source, p.15-16; p.26].
- The unbiased SRMR estimator converged to its population value faster than the biased estimator at small samples [source, p.13; p.24].
- Low factor loadings (k <= .40) are a shared danger zone: with very low loadings, even SRMR and CFI at conventional cutoffs tend to reject correctly specified or close-fitting models unless the sample is very large (N > 1,000) [source, p.24].
- Applying the conventional SRMR cutoff of .08 to the unbiased SRMR often retained severely misspecified models unless loadings were high; the authors instead applied the measurement-quality-adjusted cutoff SRMR <= .10 x R-squared from Shi, Maydeu-Olivares, & DiStefano (2018), where R-squared is the average communality [source, p.5; p.16].
- Confidence intervals (CIs) and close-fit p-values were generally accurate for all three indices even at small df, but CI widths for RMSEA and SRMR became very wide at small df and small N (e.g., rho=.90, N=100, k=.60, df=2 gave average CI width of 0.18 for both), whereas CFI CI widths were largely insensitive to df [source, p.2; p.18; p.24]. For SRMR, median CI widths were much narrower than mean widths because a small fraction of replications produced extreme intervals [source, p.24-25].

## Numerical example (open-book closed-book data)

Using the open-book closed-book dataset (5 test scores, N=88; Mardia, Kent, & Bibby, 1979), a one-factor CFA (df=5) gave sample RMSEA=0.096 (90% CI 0 to 0.195), unbiased sample SRMR=0.039 (90% CI 0.004 to 0.074), and ML-based CFI=0.979 (90% CI 0.923 to 1) [source, p.17-18]. On conventional cutoffs, RMSEA flagged poor fit while SRMR and CFI met the good-fit criteria, illustrating the paper's core point that RMSEA can disagree with SRMR and CFI precisely when df is small [source, p.18].

## Headline recommendation

"When assessing very small models (e.g., df = 2), researchers should be cautious in interpreting RMSEA and should rely more on SRMR and CFI" [source, p.26]. The authors stress there are no golden rules for assessing fit and endorse evaluating fit with more than one index, explicitly aligning their advice with Hu & Bentler's (1999) two-index strategy of SRMR plus one supplementary index [source, p.27].

## Limitations stated by the authors

- All conclusions assume multivariate normal data; performance under non-normal data was not tested here and is left to future work [source, p.25-26].
- Only one type of misspecification was studied (misspecified dimensionality in factor analysis models); path-analysis misspecifications and omitted cross-loadings were not examined [source, p.26].

## Relationship to existing wiki pages

- Refines and partially critiques `hu-bentler-1999-cutoff-criteria-fit-indexes.md`: same three indices and same conventional cutoffs, but Shi et al. show those cutoffs behave unequally as df shrinks and that RMSEA in particular should be de-emphasized at small df [source, p.2; p.26]. Cross-reference, do not restate the Hu & Bentler derivation.
- Distinct from the model-size-effect line of work (Shi, Lee, & Terry, 2018; Shi, Lee, & Maydeu-Olivares, 2019), which this paper cites as background and which is captured in `shi-2017-model-size-effect-sem.md` [source, p.4; p.28-29 refs].
- Summarized alongside the fixed-cutoff, model-size-effect, and equivalence-testing approaches in the shared method page `data/wiki/shared/methods/sem-fit-index-evaluation.md`.

## Why this matters for QNTR work

The Prashar co-authored paper and the DBA thesis both use SEM (per ingest brief). Any SEM analysis in those deliverables that fits a small or short-scale model (a plausible situation when using brief survey instruments) should heed this paper: report SRMR and CFI as the primary fit evidence for small-df models and interpret RMSEA with caution or alongside its confidence interval [source, p.26]. Note: the link to those specific downstream deliverables is asserted by the ingest brief, not by this source; the paper itself makes no claim about any particular study in this workspace.
