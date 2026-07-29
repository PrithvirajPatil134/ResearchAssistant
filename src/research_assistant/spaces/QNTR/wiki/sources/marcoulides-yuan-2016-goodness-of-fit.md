---
type: source
title: "New Ways to Evaluate Goodness of Fit: A Note on Using Equivalence Testing to Assess Structural Equation Models"
maturity: seed
tags: [sem, structural-equation-modeling, model-fit, goodness-of-fit, equivalence-testing, t-size, adjusted-fit-indexes, cfi, rmsea, confirmatory-factor-analysis, quantitative-methods]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [research_paper, thesis, conference_paper, term_paper]
draws_from: []
authors: ["Marcoulides, Katerina M.", "Yuan, Ke-Hai"]
year: 2016
journal: "Structural Equation Modeling: A Multidisciplinary Journal"
volume: "23(6)"
pages: "1-6"
doi: "10.1080/10705511.2016.1225260"
source_path: "src/research_assistant/spaces/QNTR/knowledge/Key method readings/2016 - Marcoulides and Yuan - New Ways to Evaluate Goodness of Fit.pdf"
ingested: 2026-07-28
target_path: src/research_assistant/spaces/QNTR/wiki/sources/marcoulides-yuan-2016-goodness-of-fit.md
---

## What this source is

A short "Teacher's Corner" didactic article that introduces equivalence testing as a way to assess the goodness of fit of structural equation models (SEM), positioned as a superior alternative to deciding model acceptance or rejection by fixed goodness-of-fit cutoff values [source, p.1 (abstract)]. Katerina M. Marcoulides is at Arizona State University; Ke-Hai Yuan is at the University of Notre Dame [source, p.1]. The method it teaches is the operational front end of Yuan, Chan, Marcoulides, and Bentler (2016), "Assessing structural equation models by equivalence testing with adjusted fit indexes" [source, p.2, p.6 (references)].

## The problem it addresses

SEM fit is conventionally judged with a chi-square test plus descriptive indexes such as RMSEA and CFI (Bentler, 1990; Steiger & Lind, 1980), and most SEM software (AMOS, EQS, LISREL, Lavaan, Mplus, OpenMx) prints dozens of these automatically [source, p.1]. The commonly cited support criteria are a nonsignificant chi-square, CFI > .90, and RMSEA below .05 with the left endpoint of its 95% confidence interval including 0 (Browne & Cudeck, 1992; Raykov & Marcoulides, 2006) [source, p.1]. The paper's central complaint: there is long-standing disagreement over what cutoff values these indexes must reach to confidently accept or reject a model, with cutoffs such as RMSEA {0.01, 0.05, 0.08, 0.10} and CFI {0.99, 0.95, 0.92, 0.90} used to label models excellent/close/fair/mediocre-or-poor [source, pp.1-2].

Two limitations motivate the alternative:
- Despite Hu and Bentler's (1998, 1999) cautions and those of others (Marsh, Balla, & Hau, 1996; Marsh, Hau, & Wen, 2004), many researchers misapply the cutoff guidelines; some have argued the indices should be raised, or banned outright (Barrett, 2007, is quoted recommending "banning ALL such indices," p.821) [source, p.2].
- A nonsignificant chi-square only means there is not enough evidence to reject the null that the model reproduces the population covariance matrix perfectly. It does not license a claim that the model is correctly specified or of good quality [source, p.2].

## The method: equivalence testing with T-size fit indexes

Rather than compare an index to a fixed cutoff, equivalence testing computes the "T-size" (minimum tolerable size) of misspecification, єt, corresponding to the observed maximum-likelihood likelihood ratio test statistic (TML) [source, p.2]. Kept to CFI and RMSEA to match Yuan et al. (2016), the T-size versions are denoted CFIt and RMSEAt [source, pp.2-3]. Interpreted as one-sided 95% bounds, they let a researcher state, with confidence, that the population CFI is at least some value and that misspecification is no larger than some value [source, pp.3, 5].

The paper further supplies *adjusted* cutoff values for the T-size indexes that are recalculated for the specific model (they depend on df and N), replacing the one-size-fits-all thresholds [source, pp.3-4]. These adjusted cutoffs carry the same excellent/close/fair/mediocre/poor labels but shift with the study design.

Tooling (operational): a public R program at `http://www3.nd.edu/~kyuan/EquivalenceTesting/T-size_RMSEA_CFI.R` computes both T-size indexes; its inputs are TML, df, the independence-model statistic (TML-Independence), sample size N, number of observed variables p, and significance level α (df for the independence model is derived from p, not entered) [source, p.3]. Companion programs `CFI_e.R` and `RMSEA_e.R` return the adjusted cutoffs from only df and N [source, p.3]. Results in the article were produced with R and Mplus [source, pp.2-3].

## The worked demonstration (why it matters)

The authors simulate N = 600 cases from a two-factor structure (k = 2, with seven and five observed variables, 12 in total; factor correlation ρ = .75), following the simulation design of Raykov, Marcoulides, and Tong (2015) [source, p.3].

**One-factor model (deliberately misspecified).** Conventional output: χ²(54) = 140.089, CFI = 0.941, RMSEA = .052 (90% CI [.041, .062]) — read conventionally as a tenable, close-fitting model [source, p.3]. Equivalence testing output: T-size RMSEA = 0.0622 and T-size CFI = 0.8996, i.e., 95% confidence that population CFI is above ~0.90 and misspecification is no more than ~0.062 [source, p.3]. Against the adjusted cutoffs (CFI_e labels ≈ poor .867 / mediocre .891 / fair .927 / close .978; RMSEA_e labels ≈ excellent .028 / close .060 / fair .089 / mediocre .109), the model lands at only "fair" fit and is judged not plausible [source, p.4]. This is the paper's key illustration: a misspecified one-factor model that conventional cutoffs would not reject is correctly flagged as not plausible by equivalence testing [source, p.4].

**Two-factor model (correctly specified).** Conventional output: χ²(53) = 58.374 (p = .2845), CFI = 0.996, RMSEA = .013 (90% CI [0, .030]) — excellent/close [source, p.4]. Equivalence testing: T-size RMSEA = 0.0298, T-size CFI = 0.9750, judged tenable with close fit [source, pp.4-5]. Even where the two approaches agree, the paper stresses the implications differ: equivalence testing yields a 95%-confidence statement about the degree of misspecification and about how far CFI is from its population value, whereas conventional criteria give no information about whether the model is correctly specified or about the degree of misspecification if it is not [source, p.5].

## Recommendation

Whenever SEM model fit is assessed, researchers should examine the equivalence-testing T-size values in addition to (not instead of) conventional fit indexes, because for the same data and model equivalence testing conveys more information [source, pp.1, 5]. The authors frame this, quoting Yuan et al. (2016), as giving SEM "the needed property to be a scientific methodology" (Yuan et al., 2016, p.327) [source, pp.2, 5].

## Relation to the SEM-fit cluster

- Complements `hu-bentler-1999-cutoff-criteria-fit-indexes.md`: Hu & Bentler establish the fixed-cutoff standard (CFI ≈ .95, RMSEA ≈ .06); this source is the equivalence-testing / adjusted-cutoff alternative to fixed cutoffs and cites Hu & Bentler (1998, 1999) as the guidelines being reconsidered [source, p.2]. See `./hu-bentler-1999-cutoff-criteria-fit-indexes.md`.
- Sibling cluster members `./shi-2017-model-size-effect-sem.md` (model-size effect on the raw LRT statistic) and `./shi-2021-sem-fit-small-df.md` (small-df behaviour of RMSEA/SRMR/CFI) were ingested in the same manifest. All four are summarized together in the shared method page `data/wiki/shared/methods/sem-fit-index-evaluation.md`.

## What this source does NOT establish

It makes no claim about any specific downstream QNTR or DBA study; any link to the Prashar co-authored paper or a DBA thesis is a workspace/manifest assertion, not this source's. The article is limited to normally distributed data in its examples, and notes that other distributions may need robust transformations or normal approximations (per Yuan et al., 2016) [source, p.2, footnote 4].
