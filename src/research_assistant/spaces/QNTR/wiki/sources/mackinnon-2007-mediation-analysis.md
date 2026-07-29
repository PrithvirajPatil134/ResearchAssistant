---
type: source
title: "MacKinnon, Fairchild & Fritz (2007): Mediation Analysis"
maturity: seed
tags: [mediation, indirect-effect, single-mediator-model, causal-steps, product-of-coefficients, sobel-test, distribution-of-the-product, bootstrapping, statistical-power, longitudinal-mediation, multilevel-mediation, causal-inference, quantitative-methods]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [term_paper, research_paper, thesis, quantitative_study, literature_review]
draws_from: []
authors: ["MacKinnon, David P.", "Fairchild, Amanda J.", "Fritz, Matthew S."]
year: 2007
journal: "Annual Review of Psychology"
volume: "58"
pages: "593-614"
source_path: "src/research_assistant/spaces/QNTR/knowledge/Key method readings/2007 - MacKinnon et al - Medation analysis.pdf"
ingested: 2026-07-28
target_path: src/research_assistant/spaces/QNTR/wiki/sources/mackinnon-2007-mediation-analysis.md
---

# MacKinnon, Fairchild & Fritz (2007): Mediation Analysis

## What This Paper Is

A review article in the Annual Review of Psychology that surveys the theory, estimation, testing, and extensions of mediation analysis. A mediating variable transmits the effect of an independent variable on a dependent variable, so that X causes M and M causes Y (X to M to Y); mediation is one way a researcher explains the process or mechanism by which one variable affects another [source, pp.593-594]. The review distinguishes the mediator from three other roles a third variable can play, describes the statistical methods for the single-mediator case and their assumptions, then treats extensions (multilevel, categorical outcomes, multiple mediators, longitudinal, moderation-with-mediation, and causal inference) [source, p.595].

## The Third-Variable Distinctions

For a third variable Z added to an X-Y relation, the paper separates four roles [source, p.595]:

- **Mediator (M)**: sits in the causal sequence X to M to Y.
- **Confounder**: Z causes both X and Y, so ignoring Z gives incorrect inference about the X-Y relation.
- **Covariate**: Z relates to X and/or Y and improves prediction of Y, but does not substantially alter the X-Y relation when included.
- **Moderator (interaction)**: Z changes the X-Y relation across its levels; a moderator is not part of the causal sequence between the two variables.

The single-mediator path diagram (Figure 1) uses a for the X-to-M relation, b for the M-to-Y relation adjusted for X, and c' for the X-to-Y relation adjusted for M [source, p.595].

## The Single-Mediator Model: Three Estimation Approaches

Three regression equations underlie all methods [source, p.598]:

- Y = i1 + cX + e1
- Y = i2 + c'X + bM + e2
- M = i3 + aX + e3

There are three major approaches to statistical mediation analysis [source, p.598]:

1. **Causal steps** — the classic Baron & Kenny (1986) / Judd & Kenny (1981) four-step procedure (significant X-Y, significant X-M, significant M-Y controlling for X, and a reduced X-Y coefficient when M is added). The most widely used, but with several limitations discussed below.
2. **Difference in coefficients** — the mediated effect is c-hat minus c'-hat, the reduction in the X effect on Y when adjusted for M; divided by the SE of the difference and compared to a standard normal.
3. **Product of coefficients** — the mediated effect is a-hat times b-hat; divided by the SE of the product and compared to a standard normal.

The a-hat*b-hat and c-hat minus c'-hat estimators are algebraically equivalent for normal-theory OLS and maximum-likelihood estimation of the three equations (MacKinnon et al. 1995). For multilevel, logistic/probit, and survival models they are not always equivalent and a transformation is required [source, p.599].

## Standard Errors, Confidence Limits, and the Power Problem

- Sobel's (1982) multivariate delta-method standard error of the indirect effect is the most commonly used SE formula [source, p.599]. The Equation-4 estimator shows low bias for single-mediator samples of at least 50, and for multiple-mediator models needs 100-200 minimum [source, p.599].
- Normal-theory confidence limits for the mediated effect are often inaccurate; asymmetric limits based on the distribution of the product and on bootstrap estimation have better coverage [source, pp.600-601].
- A simulation of 14 methods found that the most widely used causal-steps methods had very low power to detect mediated effects and low Type I error; a joint test of the significance of a-hat and b-hat was a good compromise between Type I and Type II error [source, p.601].
- The requirement of a significant overall X-to-Y relation is a chief cause of the causal-steps test's low power, especially under complete mediation. Empirical work found that detecting a small-a, small-b mediated effect at .8 power via the causal-steps test required approximately 21,000 subjects (Fritz & MacKinnon 2007) [source, p.601].
- The product of two normal variables is not itself normal (excess kurtosis of six for two standard normals), which explains why normal-based significance tests for ab are inaccurate; the PRODCLIN program computes distribution-of-the-product critical values and confidence limits [source, p.601].
- Computer-intensive (resampling / bootstrap) methods generate a reference distribution from the observed data; they generalize to situations lacking analytic formulas and require fewer assumptions. AMOS, EQS, LISREL, and Mplus perform bootstrap resampling for the mediated effect [source, pp.601-602].

## Assumptions, Complete vs. Partial, Consistent vs. Inconsistent

- Assumptions for the a-hat*b-hat estimator include independent residuals in Equations 2 and 3, no XM interaction in Equation 3 (which can and should be tested), and no misspecification of causal order, causal direction, omitted causes, or measurement error. Many of these are hard or impossible to test, so proof of mediation is impossible; a program of research combining experiments, theory, and qualitative methods is the realistic route [source, p.602].
- **Complete vs. partial mediation**: tested via whether c' is significant. A significant c' alongside significant mediation indicates partial mediation. Because behaviors have many causes, complete mediation by a single mediator is often unrealistic [source, p.602].
- **Consistent vs. inconsistent models**: in inconsistent models at least one mediated effect has a different sign than other effects, so opposing mediational processes can produce a near-zero overall X-Y relation even when mediation exists (McFatter's 1979 widget example: intelligence, boredom, production) [source, p.602].

## Effect Size

Effect-size measures include the raw correlation for the a path and partial correlation for the b path, and standardized coefficients for individual paths. For the whole mediated effect, the proportion mediated [1 - (c'/c) = ab/(ab + c')] is common but often very small, can neglect additional mechanisms, and is unstable unless the sample is at least 500. The authors note that effect-size measurement for mediation needs more development [source, p.603].

## Extensions of the Single-Mediator Model

- **Multilevel mediation**: analyzing clustered data (individuals in schools, clinics, therapy groups) at the individual level inflates Type I error because within-cluster observations are dependent; a and b paths can be random effects that covary, requiring appropriate SEs [source, pp.603-604].
- **Categorical outcomes**: with a categorical Y, Equations 1-2 are rewritten for logistic or probit regression; because the residual variance is fixed, the c-hat minus c'-hat method is biased, so standardizing coefficients or using the product-of-coefficients test (a from OLS, b from logistic) is preferred [source, p.604].
- **Multiple mediators**: straightforward extensions of the single-mediator case, useful because programs typically target several mediators at once [source, p.604].
- **Longitudinal mediation**: three major model types are the autoregressive model (Gollob & Reichardt 1991; Cole & Maxwell 2003, with contemporaneous and cross-lagged variants), the latent-growth / parallel-process model, and the latent difference score model. Longitudinal data support the temporal-precedence condition for causality but bring measurement-timing and specification challenges [source, pp.604-605].

## Moderation and Mediation

The strength and form of mediated effects can depend on other variables. A nonzero XM interaction in Equation 2 indicates the b coefficient differs across levels of X [source, p.605]. Three models combine moderation and mediation [source, pp.605-606]:

- **Moderated mediation**: the mediated effect depends on the level of a moderator, so the mechanism differs across subgroups; the simplest version estimates the mediation model per subgroup and compares mediated effects.
- **Mediated moderation**: a mediator lies in the causal sequence from an interaction effect to the outcome; the aim is to find the mediator(s) that explain the interaction.
- **Mediated baseline by treatment moderation**: a special case where the mediated effect depends on the baseline level of the mediator, common in prevention/treatment research.

The authors present a general model (Equation 6) that adds XM and XMZ interactions to unify individual mediation and moderation equations, with the h coefficient testing whether the M-to-Y relation differs across X and the j coefficient testing the three-way interaction. This general model was in development and not yet empirically tested in applied research at the time of writing [source, p.606].

## Causal Inference

Observed-regression mediation has been criticized on causal grounds. With simultaneous measurement of X, M, and Y, equivalent models can fit the data equally well (e.g., M mediates the Y-to-X relation) [source, p.607]. Even when X is randomized, c-hat and a-hat are valid causal estimators, but the b coefficient (M-to-Y adjusted for X) is not an accurate causal estimator because that relation is correlational rather than randomized, and c' is likewise not an accurate direct-effect estimator [source, p.607]. Newer approaches use principal stratification (Frangakis & Rubin 2002) and instrumental-variable enhancements. The core lesson is the difficulty of interpreting the M-to-Y relation causally [source, p.607].

## Recommended Practice (Authors' Summary)

The recommended test assesses the statistical significance of the X-to-M (a) path and then the M-to-Y (b) path; if both are significant there is evidence of mediation. Confidence limits based on the distribution of the product or the bootstrap are recommended over normal-theory limits. Researchers should also consider opposing (inconsistent) mediated effects, since an overall X-Y relation can be nonsignificant while mediation still exists [source, pp.607-608].

## Position Relative to Existing Wiki Pages

- **Anchors** the estimation-and-testing side that `data/wiki/shared/methods/baron-kenny-moderation-mediation.md` introduces conceptually: where Baron & Kenny (1986) give the causal-steps procedure, MacKinnon et al. document its low statistical power and recommend the joint a-and-b significance test plus distribution-of-the-product or bootstrap confidence limits [source, p.601].
- **Provides the general-mediation backdrop** for `src/research_assistant/spaces/QNTR/wiki/sources/preacher-2007-moderated-mediation.md`: Preacher et al. formalize the conditional-indirect-effect (moderated-mediation) case; MacKinnon et al. situate moderated mediation, mediated moderation, and mediated baseline-by-treatment moderation within the wider mediation-methods landscape [source, pp.605-606].
- **Complements** `src/research_assistant/spaces/DBA/wiki/sources/wu-zumbo-2007-mediators-moderators.md`: both flag the low power of normal-theory / Sobel tests for the product; MacKinnon et al. add the distribution-of-the-product remedy (PRODCLIN), the 14-method simulation evidence, and the longitudinal / multilevel / causal-inference extensions [source, pp.601-607].

## Relevance to the QNTR Term Paper

If the agentic-AI-governance model (`src/research_assistant/spaces/QNTR/wiki/syntheses/agentic-ai-governance-term-paper.md`) posits an indirect (mediated) path, this is the reference for how to estimate and test it: use the product-of-coefficients estimate a-hat*b-hat with the joint significance test of both paths, and report bootstrap or distribution-of-the-product confidence limits rather than normal-theory limits [source, pp.598-601, 607-608]. Any causal claim about the mediator-to-outcome path must acknowledge that this path is correlational even if the antecedent is manipulated [source, p.607].
