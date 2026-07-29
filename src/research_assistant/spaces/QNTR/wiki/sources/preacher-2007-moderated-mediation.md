---
type: source
title: "Preacher, Rucker & Hayes (2007): Addressing Moderated Mediation Hypotheses"
maturity: seed
tags: [moderated-mediation, conditional-indirect-effects, mediation, moderation, bootstrapping, johnson-neyman, spss-macro, quantitative-methods]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [term_paper, research_paper, thesis, quantitative_study]
draws_from: []
authors: ["Preacher, K. J.", "Rucker, D. D.", "Hayes, A. F."]
year: 2007
journal: "Multivariate Behavioral Research"
volume: "42(1)"
pages: "185-227"
source_path: "src/research_assistant/spaces/QNTR/knowledge/Key method readings/2007 - Preacher et al - Addressing moderated mediation hypotheses.pdf"
ingested: 2026-07-28
target_path: src/research_assistant/spaces/QNTR/wiki/sources/preacher-2007-moderated-mediation.md
---

# Preacher, Rucker & Hayes (2007): Addressing Moderated Mediation Hypotheses

## What This Paper Is

A methods paper that gives applied researchers a guide to construe and conduct analyses of **conditional indirect effects**, commonly called **moderated mediation** effects. It disentangles conflicting definitions of moderated mediation, supplies standard errors for hypothesis tests and confidence intervals in large samples, advocates bootstrapping where possible, and provides an SPSS macro to run the recommended methods [source, p.185].

## Core Contribution: The "Conditional Indirect Effect" Rubric

Mediation (an indirect effect) occurs when the causal effect of an independent variable (X) on a dependent variable (Y) is transmitted by a mediator (M): X affects Y because X affects M, and M in turn affects Y [source, p.186]. Preacher et al. gather the family of mediation-plus-moderation effects under one general term, the **conditional indirect effect**, defined as the magnitude of an indirect effect at a particular value of a moderator (or at particular values of more than one moderator) [source, p.186].

Because several methodologists had defined "moderated mediation" in conflicting ways (James & Brett 1984, who coined the term; Muller, Judd & Yzerbyt 2005; Morgan-Lopez & MacKinnon 2006; Wegener & Fabrigar 2000), the paper resolves the confusion by treating all of them as instances of **systematic variation in conditional indirect effects**: the strength of a simple mediation effect is quantified by a1b1, so any moderation of that quantity yields an indirect effect conditional on another variable [source, pp.193-195].

The framework is developed within a regression / path-analytic framework with no latent variables, but the authors state the strategies extend readily to structural equation models [source, p.187].

## The Five Moderated-Mediation Models

Building on the simple-mediation path diagram (M = a0 + a1 X; Y = b0 + c' X + b1 M), the paper enumerates five ways an indirect effect can be conditional [source, pp.193-198]:

- **Model 1** — The independent variable X is itself the moderator of the b path. Conditional indirect effect estimate: a1(b1 + b2 X) [source, pp.195-196].
- **Model 2** — A fourth variable W moderates the a path (X to M). Estimate: (a1 + a3 W) b1. The same model addresses "mediated moderation" if instead the product a3 b1 is emphasized [source, pp.196-197].
- **Model 3** — W moderates the b path (M to Y). Estimate: a1(b1 + b3 W). This is the model used in the paper's worked example [source, p.197].
- **Model 4** — W moderates the a path and a different variable Z moderates the b path. Estimate: (a1 + a3 W)(b1 + b3 Z) [source, pp.197-198].
- **Model 5** — W moderates both the a and b paths. Estimate: (a1 + a3 W)(b1 + b2 W). This is the model Baron & Kenny (1986) described for moderated mediation and the one Muller et al. (2005) proposed for both mediated moderation and moderated mediation [source, p.198].

Mediated moderation (Baron & Kenny's coined term: first show an X-by-W interaction on Y, then introduce a mediator of it) is explicitly set aside because it does not require probing conditional indirect effects [source, p.193].

## Two Testing Approaches

1. **Bootstrapping (preferred).** Resample N units with replacement k times, compute the conditional indirect effect in each resample, sort, and take percentile-based confidence limits; because no symmetry is assumed the interval can be asymmetric, and bias-corrected or bias-corrected-and-accelerated (BCa) adjustments can improve accuracy. The null of no conditional indirect effect is rejected when the CI excludes 0. Bootstrapping works at virtually any sample size and, per the simulation, tends to show higher power and closer-to-accurate Type I error than delta-method tests [source, pp.190-191, 198-200, 204].
2. **Normal-theory delta-method standard errors.** First- and second-order multivariate delta-method SEs (Bollen 1987, 1989; Sobel 1982) are derived for each model; dividing the point estimate by its SE gives an asymptotic z-test, valid only when total sample size is large. Table 1 lists point estimates and second-order variances for Models 0-5; the underlined terms can be dropped for the first-order variance [source, pp.200-203].

## Probing Significant Conditional Indirect Effects

The paper extends two familiar interaction-probing tools to indirect effects [source, pp.191-192, 200-203]:

- **Simple slopes** — evaluate the conditional indirect effect at chosen moderator values (typically the mean and plus/minus 1 SD).
- **Johnson-Neyman (J-N) regions of significance** — rather than picking arbitrary moderator values, solve the reversed z-test (a quadratic; Table 2 gives the A, B, C terms for Models 1-3) for the moderator range over which the indirect effect is statistically significant.
- **Confidence bands** — plot the conditional indirect effect with continuous CIs across the moderator range; the effect is significant where the band excludes zero.

Bootstrapping cannot easily produce regions of significance, so the normal-theory approach is the route to J-N regions [source, p.200].

## The MODMED SPSS Macro

The authors wrote an SPSS macro that, once run, creates a MODMED command; the user names which variables are X, M, Y, and the moderator(s), and SPSS estimates whichever of the five models the variable listing implies. By default it reports conditional indirect effects at the moderator mean and plus/minus 1 SD, at increments across the observed range, and the J-N value where the effect becomes just significant, using second-order SEs; bootstrap CIs (percentile, bias-corrected, BCa) are requested via options. A MODMEDC variant allows covariates. The macro is at http://www.quantpsy.org/ [source, pp.207-210].

## Worked Example (MSALT, Model 3)

Using Michigan Study of Adolescent Life Transitions data (N = 609), the indirect effect of sixth-grade intrinsic interest in math (INTRINT) on eighth-grade math performance (MATH8) through seventh-grade teacher perceptions of talent (PERCTAL) was hypothesized to be moderated by eighth-grade math self-concept (SCMATH), because SCMATH moderates the PERCTAL-to-MATH8 (b) path [source, pp.210-211]. The SCMATH-by-PERCTAL interaction was significant (B = .142, SE = .060, z = 2.351, p = .019), the conditional indirect effect was larger at higher SCMATH, and the J-N technique found the indirect effect significant at alpha = .05 for any SCMATH above 1.99 on the 7-point scale [source, pp.211-213]. Bootstrap BCa CIs corroborated the normal-theory tests. A significant unconditional indirect effect is NOT a prerequisite for examining conditional indirect effects [source, p.211].

## Assumptions and Prescriptions

- These are causal models: conclusions rest on temporal precedence, concomitant variation, and elimination of spurious correlation; correct model specification (linearity, normal/homoscedastic/independent disturbances, no important omitted variables) is the key assumption [source, pp.216-217].
- If bootstrapping is used, the only assumptions when testing conditional indirect effects are linearity of the relationships and independence of observations [source, p.216].
- If SEM is used with missing data, data should be missing at random (MAR) or missing completely at random (MCAR) [source, p.216].
- Report confidence intervals, not just point tests; asymmetric (bootstrap) intervals are generally preferable because they incorporate the skew of product distributions [source, p.217].

## Position Relative to Existing Wiki Methods

- Extends `data/wiki/shared/methods/baron-kenny-moderation-mediation.md`: Baron & Kenny (1986) established the moderator-mediator distinction and the causal-steps test; Preacher et al. operationalize the harder case where a mediation effect is itself conditional on a moderator, with formal estimation and testing for five distinct model shapes [source, pp.193-198].
- Complements `src/research_assistant/spaces/DBA/wiki/sources/wu-zumbo-2007-mediators-moderators.md`: Wu & Zumbo (2007) define moderated mediation and mediated moderation conceptually and warn about Sobel-test power; Preacher et al. supply the matching estimation machinery (delta-method SEs, bootstrapped and J-N inference, the MODMED macro).

## Relevance to the QNTR Term Paper

The QNTR term-paper synthesis (`src/research_assistant/spaces/QNTR/wiki/syntheses/agentic-ai-governance-term-paper.md`) targets a model with combined mediation and moderation structure. Where a hypothesized indirect (mediation) path is expected to vary with a moderator, this paper is the methodological reference: it names that quantity (conditional indirect effect), gives the model shape to specify (Models 1-5), and prescribes bootstrapped CIs plus J-N probing for testing it [source, pp.186, 193-203]. Any use in the paper should follow the paper's own caution: state the causal-model assumptions and report confidence intervals [source, pp.216-217].
