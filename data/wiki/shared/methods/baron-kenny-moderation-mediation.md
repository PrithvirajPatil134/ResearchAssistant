---
type: method
title: "Baron & Kenny: Moderator-Mediator Distinction"
citation: "Baron, R.M. and Kenny, D.A. (1986). The Moderator-Mediator Variable Distinction in Social Psychological Research. Journal of Personality and Social Psychology, 51(6), 1173-1182."
source_file: "src/research_assistant/spaces/CRO/knowledge/Session 6 /Baron_Kenny_86_updated.pdf"
applicable_to: [thesis, research_paper, quantitative_study]
maturity: working
originating_space: shared
created: 2026-05-23
last_updated: 2026-05-23
---

# Baron & Kenny: Moderation and Mediation

## What It Is

The foundational paper (60,000+ citations) defining the difference between moderators and mediators, with exact statistical testing procedures.

## When to Use

- Testing whether a third variable changes the STRENGTH of a relationship (moderation)
- Testing whether a third variable explains HOW a relationship works (mediation)
- Any quantitative study with IV, DV, and a proposed mechanism or boundary condition

## Core Distinction

**Moderator**: Changes when or for whom an effect holds.
- "X affects Y, but only when Z is high."
- Tested via interaction term (X * Z) in regression.
- Moderator is at the same causal level as the IV (both are antecedents).

**Mediator**: Explains how or why an effect occurs.
- "X affects Y, but through M."
- Tested via three regressions: (1) IV → Mediator, (2) IV → DV, (3) IV + Mediator → DV. Full mediation = IV effect disappears when mediator is controlled.
- Mediator is causally between IV and DV.

## The Four Cases for Moderation Testing

1. Both moderator and IV categorical: 2x2 ANOVA, test interaction
2. Moderator categorical, IV continuous: compare regression slopes across groups
3. Moderator continuous, IV categorical: product term (XZ) in regression
4. Both continuous: product term approach (Cohen & Cohen 1983)

## Key Requirements for Mediation

1. IV must significantly affect the mediator (Path a)
2. IV must significantly affect the DV (Path c)
3. Mediator must significantly affect the DV when controlling for IV (Path b)
4. The effect of IV on DV must be reduced (partial mediation) or eliminated (full mediation) when mediator is controlled

## Relevance to DBA Thesis (Org Restructuring)

If the quantitative Phase 2 tests whether structural change predicts financial performance:
- A **mediator** question: "Does structural change improve performance THROUGH improved operational efficiency?" (structural change → efficiency → performance)
- A **moderator** question: "Does structural change improve performance only for firms in certain competitive positions?" (competitive intensity moderates the structural change → performance link)

Prof. Prashar thinks in these terms. His feedback on the Agentic AI paper used moderation language explicitly.

## Cardoso Connection

Cardoso's causal language hierarchy (correlation < influence < impact < moderation) maps directly to this framework. Using "moderation" in your objective signals you understand the analytical requirements.

## Contemporary Extensions (Wu & Zumbo 2007)

Wu and Zumbo (2007), "Understanding and Using Mediators and Moderators" (Social Indicators Research 87:367-392), provide a review that extends the Baron & Kenny framework in several directions. Full source page: `src/research_assistant/spaces/DBA/wiki/sources/wu-zumbo-2007-mediators-moderators.md`.

### Integrated Research Design Requirement

The core argument: mediation and moderation are causal models requiring an "integrated research plan from articulating the theoretical rationale, choosing a research design, analyzing the data, to drawing conclusions," not merely data analytic techniques [src/research_assistant/spaces/DBA/knowledge/Marketing & Commerce in Intnl Context/Understanding and Using Mediators and Moderators.pdf, p.1]. Implications:

- A variable's role (mediator vs. moderator) should be determined by substantive theory and operationalization, not post-hoc testing [Understanding and Using Mediators and Moderators.pdf, p.3]
- "It is non-sensical to test an operationalized variable for both mediation and moderation effects" [Understanding and Using Mediators and Moderators.pdf, p.23]

### Four Levels of Design Control for Causal Claims

A hierarchy that determines what causal inferences are legitimate [Understanding and Using Mediators and Moderators.pdf, pp.5-6]:

1. Observation (correlational inference only)
2. Precedence (temporal ordering of measurement)
3. Manipulation (assignment to conditions)
4. Randomization (strongest causal inference)

Kenny's approach achieves manipulation of the IV but only observation of the mediator, limiting causal claims about the Me→Y link [Understanding and Using Mediators and Moderators.pdf, p.9].

### Moderated Mediation and Mediated Moderation

Two distinct elaborated models beyond simple mediation/moderation [Understanding and Using Mediators and Moderators.pdf, pp.18-20]:

- **Moderated mediation**: The mediation effect (ab or c-c') depends on the level of a moderator. Foundation is mediational; moderator is secondary. Requires mediation to have been shown first.
- **Mediated moderation**: A moderation effect (interaction) is itself mediated by a fourth variable. Foundation is moderational; mediator is secondary. Requires moderation to have been shown first.

### Statistical Power and Testing Concerns

- Sobel test for mediation has low statistical power when the sample is small because the ab distribution departs from normal [Understanding and Using Mediators and Moderators.pdf, p.9]
- Alternatives: MacKinnon's Z' statistic (empirical distribution), bootstrapping SE of ab [Understanding and Using Mediators and Moderators.pdf, p.9]
- Moderation detection power typically ranges .20 to .34, far below the .80 recommended level (Aguinis et al. 2001; Cohen 1988) [Understanding and Using Mediators and Moderators.pdf, p.15]
- Power analysis and sample size estimation before data collection is "crucial" for a true moderation effect to be detected [Understanding and Using Mediators and Moderators.pdf, p.15]

### SEM for Mediation/Moderation

Regression approaches assume perfect measurement reliability. SEM with latent variables corrects for measurement error and allows multiple causes/mediators/moderators in one model. However, SEM's covariance structure is correlational: "drawing directional arrows from one construct to another does not render the power to make causal claims" [Understanding and Using Mediators and Moderators.pdf, p.21].

### Model Misspecification Warnings

- Alternative models may fit data equally well [Understanding and Using Mediators and Moderators.pdf, p.22]
- Causal language in correlational data requires explicit justification [Understanding and Using Mediators and Moderators.pdf, p.22]
- Omitted variables can bias mediation/moderation estimates [Understanding and Using Mediators and Moderators.pdf, pp.22-23]
- The linearity assumption is seldom checked in practice [Understanding and Using Mediators and Moderators.pdf, p.22]

### Centering Recommendation

Center continuous moderators before creating product terms: produces meaningful main-effect interpretations, eliminates non-essential multicollinearity, and does not alter the moderation test significance or the c coefficient [Understanding and Using Mediators and Moderators.pdf, p.15].
