---
type: source
title: "Cutoff Criteria for Fit Indexes in Covariance Structure Analysis: Conventional Criteria Versus New Alternatives"
maturity: seed
tags: [sem, structural-equation-modeling, model-fit, fit-indexes, cfi, rmsea, srmr, tli, cutoff-criteria, confirmatory-factor-analysis, quantitative-methods]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [research_paper, thesis, conference_paper, term_paper]
draws_from: []
authors: ["Hu, Li-tze", "Bentler, Peter M."]
year: 1999
journal: "Structural Equation Modeling: A Multidisciplinary Journal"
volume: "6(1)"
pages: "1-55"
doi: "10.1080/10705519909540118"
source_path: "src/research_assistant/spaces/QNTR/knowledge/Key method readings/1999 - Hu and Bentler - Cutoff criteria for fit indexes in covariance structure analysis.pdf"
ingested: 2026-07-28
target_path: src/research_assistant/spaces/QNTR/wiki/sources/hu-bentler-1999-cutoff-criteria-fit-indexes.md
---

## What this source is

A Monte Carlo simulation study evaluating whether the conventional "rules of thumb" cutoff values for structural equation modeling (SEM) fit indexes are adequate, and proposing revised cutoffs plus a two-index reporting strategy [source, p.1 (abstract)]. It is the origin of the fit-index thresholds now routinely reported in SEM analyses.

## Headline cutoff recommendations

For the maximum likelihood (ML) method, the study concludes that the following cutoff values are needed before concluding there is a relatively good fit between the hypothesized model and the observed data [source, p.1 (abstract); restated p.27]:

- Tucker-Lewis Index (TLI), Bollen's 1989 Fit Index (BL89), Comparative Fit Index (CFI), Relative Noncentrality Index (RNI), and Gamma Hat: a cutoff value close to **.95** [source, p.1; p.27].
- McDonald's Centrality Index (Mc): a cutoff value close to **.90** [source, p.1; p.27].
- Standardized Root Mean Squared Residual (SRMR): a cutoff value close to **.08** [source, p.1; p.27].
- Root Mean Squared Error of Approximation (RMSEA): a cutoff value close to **.06** [source, p.1; p.27].

These raise the older convention. The prior rule of thumb treated any model with an incremental fit index above **.90** as acceptable (attributed to Bentler & Bonett, 1980; Bentler, 1989); the study shows a value above .90 leaves substantial Type II error (misspecified models wrongly accepted) [source, p.5].

## The two-index presentation strategy

A single fit index is not enough. The paper recommends reporting the ML-based SRMR together with one supplemental index (TLI, BL89, RNI, CFI, Gamma Hat, Mc, or RMSEA), because SRMR is the index most sensitive to misspecified factor covariances, while TLI/BL89/RNI/CFI/Gamma Hat/Mc/RMSEA are most sensitive to misspecified factor loadings [source, p.5]. The two-index combinational rules retained acceptable proportions of true-population models while rejecting reasonable proportions of misspecified models, and are preferred over single-index rules [source, p.16; p.27].

Specific recommended combinational rules from the Conclusion [source, p.27-28]:
- TLI (or BL89, RNI, CFI, Gamma Hat) close to .95 combined with SRMR close to .09.
- A cutoff of .96 for TLI/BL89/RNI/CFI/Gamma Hat with SRMR > .09 (or .10) gave the least sum of Type I and Type II error rates.
- RMSEA > .06 with SRMR > .09 (or .10) gave the least sum of error rates for the RMSEA-based rule.
- Mc < .90 with SRMR > .09 (or .10) yielded the minimum sum of Type I and Type II error rates for the Mc-based rule.

## Study design (basis for the cutoffs)

- Two confirmatory factor-analytic models, "simple" and "complex," each with 15 observed variables and 3 common factors [source, p.6].
- For each model type: one true-population model and two underparameterized misspecified models (misspecified factor covariances for the simple model; misspecified factor loadings for the complex model) [source, pp.8-9].
- Seven distributional conditions (one normal; three nonnormal-independent; three nonnormal-dependent, i.e., the "nonrobustness" conditions) [source, pp.7-8].
- Six sample sizes: N = 150, 250, 500, 1,000, 2,500, and 5,000, with 200 replications each. Per model this yields 7 x 6 x 200 = 8,400 samples [source, pp.8-9].
- Fit indexes computed via the ML method using EQS and SAS programs [source, p.8].

## Important caveats for practice

- At small sample size (N < 250), the ML-based TLI, Mc, and RMSEA tend to overreject true-population models and are therefore less preferable when N is small [source, p.1 (abstract); p.28].
- Under the nonrobustness condition with N < 250, there is a trade-off between Type I and Type II error rates for any recommended combinational rule; practitioners should choose the rule that minimizes the least-desirable error rate for their research area [source, p.28].
- The authors recommend using the Satorra-Bentler scaling-corrected (SCALED) test statistic alongside the combinational rules, because it performs well even under the nonrobustness condition [source, p.28].
- The authors state it is difficult to designate a single universal cutoff for each index because no value works equally well across all conditions; the recommended values are those that lower Type II error at acceptable Type I cost [source, p.27].

## Why this matters for QNTR work

These are the fit thresholds an SEM-based analysis is expected to report. The Prashar co-authored paper and the DBA thesis both use SEM (per ingest brief), so this source anchors the fit-reporting standard for those deliverables. Note: the cross-space applicability to the DBA thesis is asserted by the ingest brief, not by this source; the source itself makes no claim about any specific downstream study.

## Related SEM-methodology source in this wiki

`shi-2017-model-size-effect-sem.md` (Shi, Lee, & Terry, 2017) studies the raw likelihood ratio chi-square test statistic and how its Type I error rate inflates with model size (driven by the number of observed variables p and free parameters q). That paper explicitly flags the model size effect on practical, chi-square-based fit indexes (e.g., CFI) as future work, which is the territory this Hu & Bentler (1999) page covers. The two are complementary: the exact-fit test statistic (Shi et al.) versus the derived index cutoffs (Hu & Bentler).

**Citation**: [src/research_assistant/spaces/QNTR/knowledge/Key method readings/2017 - Shi et al - Revisiting the model size effect in SEM.pdf, p.20]

## Refinement: small degrees of freedom

Shi, DiStefano, Maydeu-Olivares, & Lee (2021), "Evaluating SEM Model Fit with Small Degrees of Freedom" (see `shi-2021-sem-fit-small-df.md`), show that the three indices do not behave equally as degrees of freedom (df) shrink. They report that RMSEA rises sharply and over-rejects correctly specified or close-fitting models at small df, while SRMR and CFI are far less sensitive to df, and they recommend relying more on SRMR and CFI when df is very small (e.g., df=2) [shi-2021-sem-fit-small-df.md, source p.2; p.26]. Their advice is consistent with the two-index strategy documented above, not a rejection of it [shi-2021-sem-fit-small-df.md, source p.27]. This is the second QNTR source to address SEM fit-index cutoffs, which cleared the two-source bar for the shared SEM fit-index method page now created at `data/wiki/shared/methods/sem-fit-index-evaluation.md`.

**Citation**: [src/research_assistant/spaces/QNTR/knowledge/Key method readings/2021 - Shi et al - Evaluating SEM model fit with small df.pdf, p.2; p.26; p.27]

## Related: equivalence-testing alternative

Marcoulides & Yuan (2016), "New Ways to Evaluate Goodness of Fit," proposes equivalence testing with T-size adjusted fit indexes as an alternative to judging fit by the fixed cutoffs this paper established; it cites Hu & Bentler (1998, 1999) as the guidelines being reconsidered. See `./marcoulides-yuan-2016-goodness-of-fit.md`.

**Citation**: [src/research_assistant/spaces/QNTR/knowledge/Key method readings/2016 - Marcoulides and Yuan - New Ways to Evaluate Goodness of Fit.pdf, p.2]

## Note on downstream method page

This source established the SEM fit-index cutoff standard. With Shi (2017), Shi (2021), and Marcoulides & Yuan (2016) now ingested in the same manifest, the shared method page on SEM fit-index evaluation was created at `data/wiki/shared/methods/sem-fit-index-evaluation.md`. It gathers the fixed-cutoff standard (this page), the model-size effect on the raw chi-square (Shi 2017), the small-df caveats (Shi 2021), and the equivalence-testing alternative (Marcoulides & Yuan 2016) into a single reference, cross-referencing each source page for detail.
