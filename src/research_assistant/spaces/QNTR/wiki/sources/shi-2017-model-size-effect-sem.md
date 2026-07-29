---
type: source
title: "Revisiting the Model Size Effect in Structural Equation Modeling"
maturity: seed
tags: [sem, structural-equation-modeling, model-size-effect, likelihood-ratio-test, chi-square-test, type-i-error, model-fit, confirmatory-factor-analysis, monte-carlo-simulation, sample-size, quantitative-methods]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [research_paper, thesis, conference_paper, term_paper]
draws_from: []
authors: ["Shi, Dexin", "Lee, Taehun", "Terry, Robert A."]
year: 2017
journal: "Structural Equation Modeling: A Multidisciplinary Journal"
volume: "advance online publication"
pages: "1-20"
doi: "10.1080/10705511.2017.1369088"
source_path: "src/research_assistant/spaces/QNTR/knowledge/Key method readings/2017 - Shi et al - Revisiting the model size effect in SEM.pdf"
ingested: 2026-07-28
target_path: src/research_assistant/spaces/QNTR/wiki/sources/shi-2017-model-size-effect-sem.md
---

## What this source is

A two-study Monte Carlo simulation paper on the "model size effect" in structural equation modeling: the inflated Type I error rate of the likelihood ratio (chi-square) test statistic that occurs when a large SEM model is fitted with a moderate-to-small sample under the chi-square reference distribution [source, p.2 (abstract); p.3]. The paper decomposes model size into its constituent factors, shows that the number of observed variables (p) and the number of free parameters (q) each have a unique effect that degrees of freedom (df) do not fully capture, and compares four correctional statistics [source, p.2 (abstract)]. Published online 28 September 2017; DOI 10.1080/10705511.2017.1369088 [source, p.1]. Funded by a National Research Foundation of Korea grant (No. 2017R1C1B2012424) [source, p.20].

The likelihood ratio chi-square test under maximum likelihood is described here as the most commonly used statistic for assessing overall goodness of fit, and is quoted from Barrett (2007) as "the only substantive test of fit for SEM" [source, p.3]. The test statistic is T_ML = (N - 1)F_ML, which asymptotically follows a central chi-square distribution with df = p(p+1)/2 - q [source, pp.2-3]. The model size effect is attributed in prior work to Herzog, Boomsma, & Reinecke (2007), Moshagen (2012), and Shi, Lee, & Terry (2015) [source, p.3].

## The problem the paper addresses

Prior studies defined "model size" using factors that tended to move together: the number of observed variables (p), the ratio of observed variables to latent factors (p/f), the number of estimated parameters (q), or the degrees of freedom (df = p(p+1)/2 - q). Because these varied jointly, earlier researchers attributed the inflated Type I error rate to a single component without isolating it [source, pp.3-4]. Moshagen (2012) is described as the only prior simulation to explore the unique effects, and it concluded that p was the "only" influential factor while q and df could be neglected; the authors flag that Moshagen varied q and df within a narrow range and simultaneously with other factors [source, p.4].

## Study I: isolating the unique effects of p, q, df, and p/f

Design: data generated from CFA measurement models with continuous outcomes; all population factor loadings set to 0.7, residual variances to 0.51, factor variances fixed to 1; 1,000 data sets per condition; sample size fixed at N = 200 (to match Moshagen 2012); all simulations run in Mplus 7.11 [source, pp.4-5]. Outcomes were the absolute difference between the mean empirical chi-square and its expected value (Delta-mean = mean empirical chi-square - df) and the empirical rejection rates at nominal alpha of 10%, 5%, and 1% [source, pp.5-6].

Findings by factor:
- **p/f (ratio of observed variables to latent factors), 36 conditions**: holding p and q fixed, the three outcome variables changed very little across six p/f levels. The model size effect is not influenced by the number of latent factors (f) or p/f above and beyond p, q, and df [source, p.5, Table 1].
- **p (observed variables), 8 levels from 10 to 120, p/f fixed at 10, 16 conditions**: larger p meant larger discrepancies and higher rejection rates. With q = 1, as p rose from 10 to 90 the 1% empirical rejection rate rose from 1% to 100%, and the absolute mean difference rose from 0.48 to 842.86 [source, p.5, Table 2].
- **q (free parameters), 48 conditions, q manipulated up to 1,030 for p = 60**: increasing q reduced bias. Under p = 60, as q rose from 1 to 1,030 the 1% empirical rejection rate fell from 88.8% to 25.9%. The effect of q held across levels of p [source, p.5, Table 3].
- **df**: pairs of p and q were chosen to yield the same df. p and q retained unique effects beyond df. Example, two cases at df = 464: the 5% rejection rate rose from 23.4% (p = 30, q = 1) to 37.6% (p = 40, q = 365) [source, p.5, Table 4].

## Study II: comparing four correctional statistics

Design expanded to 396 conditions [source, p.8]. Manipulated: sample size N = 200, 400, 600, 800, 1,000, 2,000; observed variables p = 10, 20, 30, 40, 50, 60, 90, 120; six values of q per p (largest range 1 to 2,550 at p = 120); mostly single-factor CFA models plus three large-f conditions f = 20 (p = 60), f = 30 (p = 90), f = 40 (p = 120) [source, pp.6-8]. Empirical rejection rates between 2% and 8% were treated as acceptable [source, p.8].

The four corrections, each a multiplier on T_ML [source, pp.4-5]:
- Bartlett-corrected statistic (1950), a multiplier b that is a function of f, p, and N [source, p.5, Eqs. 2-3].
- Yuan-corrected statistic (2005), a modification of Bartlett's, function of f, p, N; identical to Bartlett's in the single-factor case [source, p.5, Eqs. 4-5].
- Swain-corrected statistic (1975), function of p, df, and N [source, p.5, Eqs. 6-8].
- Yuan, Tian, & Yanagihara (2015) empirical correction, e = [N - (2.381 + 0.361p + 0.006q)] / (N - 1), developed from simulations across 342 conditions [source, p.5, Eqs. 9-10].

Results:
- For uncorrected chi-square, p was the most important determinant of inflated Type I error rates. When p >= 40 all rejection rates were noticeably above nominal even at extremely large q. Inflation at p >= 60 persisted even at N = 2,000 [source, pp.8-10].
- All four corrections gave more reasonable rejection rates than no correction [source, p.8].
- Bartlett (1950) and Yuan (2005) were identical for one-factor models but were sensitive to f and overcorrected when f was large (e.g., under N = 200, p = 90, f = 30 the corrected means fell far below the theoretical means) [source, pp.8-9].
- Swain (1975) was generally superior to Bartlett and Yuan (2005) but performed inadequately once p >= 90, especially at small N (<= 400) [source, p.10].
- The Yuan et al. (2015) empirical statistic gave the best overall control of Type I error and the smallest mean differences. For N > 400 its largest Type I error rate at alpha = .05 was 9.0%. It failed only when p was very large (p >= 90) and N very small (N = 200), where it rejected correctly specified models too often, and it could overshrink the chi-square when N was small and q extremely large [source, p.10].

## Main conclusions

1. Bias in the likelihood ratio statistic is not substantially influenced by the number of latent factors (f) or the ratio p/f [source, p.10].
2. The model size effect is associated with the number of observed variables (p): a larger p gives a poorer approximation to the asymptotic chi-square distribution [source, p.10].
3. The effect is also a function of the number of estimated parameters (q): increasing q reduces the inflated Type I error rate [source, p.10].
4. p and q have unique effects on the LRT distribution even when df is held constant [source, p.10].
5. The Yuan et al. (2015) empirically corrected statistic generally performs best at controlling Type I error rates when fitting large SEM models [source, p.10; p.20].

## Practical guidance

- p and N can be used as indexes for the risk of inflated Type I error rates with the ML-based chi-square test. To reach acceptable Type I error rates the sample size should be much larger than p, roughly N >= p^2 [source, p.8; p.20].
- The finding that increasing q mitigates inflation conflicts with Moshagen (2012) and is the opposite of Jackson (2003), whose q range (2 to 40) was restricted so that the q effect was small; both p and q should be built into any correctional method [source, p.20].
- For the Yuan et al. (2015) empirical correction specifically, the authors suggest N >= 4p is a more reasonable guideline than the original N >= max(50, 2p), because Type I error can still inflate at very large p (e.g., p = 90) even when N >= 2p [source, p.20].

## Limitations and future directions (author-stated)

- The study covered only correctly specified models and therefore only Type I error, not power to reject misspecified models; whether the empirical correction reduces power is left open [source, p.20].
- The chi-square exact-fit test is sensitive to sample size and is "not always the final word in assessing fit" (West, Taylor, & Wu, 2012) [source, p.20].
- Many practical fit indexes are built directly on the chi-square statistic (e.g., CFI; Bentler, 1990); the authors call for future study of the model size effect on practical fit indexes (Xing & Yuan, 2017) [source, p.20].

## Relation to sibling SEM pages in this wiki

- The future direction on the last point connects directly to `hu-bentler-1999-cutoff-criteria-fit-indexes.md`, which sets cutoff thresholds for exactly those chi-square-based practical fit indexes (CFI, RMSEA, SRMR, TLI). Shi et al. (2017) studies the raw LRT statistic; Hu & Bentler (1999) studies the derived fit indexes. Read together they cover the exact-fit test and its index-based supplements. (This connection is asserted here on the basis of the shared subject matter; Shi et al. name CFI/Bentler 1990 as future-work targets, not Hu & Bentler 1999 specifically [source, p.20].)
- Distinct from the 2021 Shi small-df SEM paper (`shi-2021-sem-fit-small-df.md`, ingested in the same manifest), and from the earlier Shi, Lee, & Terry (2015) abstract that this article extends [source, p.21].

## Note on downstream concept and method pages

The "model size effect" concept remains deferred as a standalone concept page (see `_log.md`). A shared SEM fit-index evaluation method page now exists at `data/wiki/shared/methods/sem-fit-index-evaluation.md`, created during this manifest's synthesizer fan-in; it summarizes this source's model-size-effect finding on the raw LRT statistic alongside the derived-index and equivalence-testing approaches.
