---
title: "Incorporating Formative Measures into Covariance-Based Structural Equation Models"
type: source
maturity: seed
created: 2026-05-07
last_updated: 2026-05-07
originating_space: QNTR
applicable_to: [research_paper, term_paper]
schema_version: "1.0"
sources:
  - path: "knowledge/Reference Material/2011 - MISQ - Diamantopoulos - Incorporating formative measures into covariance based SEM.pdf"
    type: pdf
authors:
  - "Diamantopoulos, A."
year: 2011
journal: "MIS Quarterly"
volume: "35(2)"
pages: "335-358"
ingested: 2026-05-07
tags: [formative-constructs, cbsem, measurement-model, methodology]
draws_from: []
---

## Summary

This research commentary provides practical guidelines for specifying, estimating, and evaluating formative measurement models using covariance structure analysis (CSA/CBSEM) with the LISREL program. The paper argues that IS researchers have overwhelmingly relied on PLS for formative constructs due to convenience, but CSA offers important advantages: global model fit assessment, modification indices for diagnosing misspecification, and the ability to empirically compare models with and without error terms. The paper walks through MIMIC model specification, identification requirements, scaling options, and full structural model estimation with formative constructs.

This paper is directly relevant because Prof. Prashar's May 5 feedback noted that "Agentic AI governance maturity" sounds like a formative construct, which "might require a different set of analysis techniques than the usual SEM and regression."

## Key Arguments

1. **PLS limitations for formative constructs**: PLS assumes the formative construct is "completely determined by its indicators" (i.e., error variance = 0), which is rarely theoretically defensible. CSA allows estimation and testing of the error term, enabling researchers to "empirically compare the model specifications... in terms of fit" (p. 338).

2. **Three types of formative specification** (pp. 336-337):
   - **Composite latent variable** (Equation 1): eta = gamma1*x1 + gamma2*x2 + ... + gamman*xn + zeta. The construct exists independently of its indicators; the error term (zeta) captures remaining causes. Parameters are estimated.
   - **Composite variable** (Equation 2): eta = gamma1*x1 + ... + gamman*xn. No error term; construct fully determined by indicators. This is what PLS uses.
   - **Fixed-weight composite** (Equation 3): eta = w1*x1 + ... + wn*xn. Weights are pre-defined by expert judgment, not estimated. Not testable; "simply a mathematical identity" (p. 338).

3. **CSA advantages over PLS** (pp. 338-339):
   - Ability to estimate models with error terms (assess explained variance in the construct)
   - Global fit assessment (chi-square, RMSEA, CFI, SRMR)
   - Modification indices for detecting misspecification
   - Ability to compare nested model structures via chi-square difference tests
   - "Testing one's auxiliary theory is often an important research objective in its own right" (p. 338)

4. **Identification requirements**: A formative measurement model is inherently underidentified on its own (p. 336, citing Bollen and Lennox, 1991). Identification requires either:
   - Linking the formative construct to at least two reflective indicators (MIMIC model) (p. 341)
   - Linking it to at least two other constructs in a structural model (p. 347)
   - Setting error variance to zero (as PLS implicitly does) (p. 347)

5. **Proportionality constraint**: In a MIMIC model, the ratio of formative indicator effects on each reflective outcome must be proportional. If gamma_i/gamma_j for one outcome differs from the same ratio for another outcome, it suggests the formative indicators have direct effects on outcomes beyond those mediated by the construct (pp. 340-341).

## Methodology

The paper uses illustrative examples with simulated/real data:

- **MIMIC model** (Multiple Indicators, Multiple Causes): 4 formative indicators (causes) + 2 reflective indicators (effects) of a single construct (p. 341)
- **Two-construct model**: Formative construct linked to a reflective construct via a single structural path (p. 347)
- **Three-construct model**: Formative construct linked to two reflective constructs (p. 348)
- Software: LISREL 8.80 (p. 336)
- All models estimated using covariance matrices
- Fit indices reported: chi-square, RMSEA, CFI, SRMR

## Findings

**MIMIC Model Results** (Table 2, p. 343):
- Demonstrates two scaling options: fixing one gamma to 1 vs. standardizing construct variance
- Both yield identical fit statistics but different unstandardized parameter values
- Standardized estimates are identical regardless of scaling choice

**Two-Construct Model** (Table 4, p. 348):
- With error variance set to zero (paralleling PLS assumption), model yields: chi-square = 39.594, df = 14, RMSEA = 0.084, CFI = 0.985, SRMR = 0.029
- Structural path from formative to reflective construct: beta = 0.229 (p < 0.01), R-squared = 0.453
- Results identical to expanded MIMIC model (models are equivalent per MacCallum et al., 1993)

**Key practical finding**: When a formative construct has only one outgoing path, its error variance cannot be separately identified from the outcome's residual. Setting error variance to zero solves identification but imposes a strong assumption. Having two or more outgoing paths resolves this without the zero-error constraint (p. 347).

## Relevance to Research

1. **Direct applicability to governance maturity construct**: Prof. Prashar's May 5 feedback explicitly identifies "Agentic AI governance maturity" as likely formative. If governance maturity is measured by indicators like "policy completeness," "oversight structure," "audit frequency," and "training coverage," these are causes (not symptoms) of governance maturity. Dropping one indicator changes the construct's meaning, which is the hallmark of formative measurement (p. 336).

2. **Measurement model choice**: If governance maturity is formative, the analysis cannot rely on standard reflective SEM (Cronbach's alpha, factor loadings). Instead:
   - Use MIMIC model approach with at least two reflective outcomes
   - Or embed in a full structural model with at least two dependent paths
   - Address multicollinearity among governance indicators
   - Ensure comprehensive indicator coverage (content validity via "census" not "sample," p. 337)

3. **PLS vs. CBSEM decision**: The paper provides a clear rationale for choosing CBSEM over PLS: global fit, modification indices, model comparison. If the quantitative phase aims for publication in A* journals (MISQ, ISR), CBSEM is the expected estimation approach.

4. **Identification strategy**: For the governance-risk-performance model, the governance maturity construct needs at least two outgoing paths (to risk and to performance) to avoid the zero-error-variance constraint. The term paper's three-proposition framework (governance -> risk, governance -> performance, risk -> performance) satisfies this.

5. **Proportionality constraint implications**: If governance maturity indicators have direct effects on risk or performance beyond those mediated through the governance construct, the MIMIC proportionality test will flag this. This informs whether a formative or reflective specification is appropriate.

## Limitations

- Illustrative examples use relatively small sample sizes (exact N not specified for the simulated data)
- Focus on LISREL-specific implementation; other CSA software (Mplus, AMOS) may differ in syntax
- Does not address longitudinal or multi-level formative models
- The zero-error-variance constraint (necessary when only one outgoing path exists) may not be tenable for complex real-world constructs
- Does not discuss formative constructs in the context of moderation or mediation models (which the governance study would require)

## Key Quotes

- "Formatively measured constructs have been increasingly used in information systems research. With few exceptions, however, extant studies have been relying on the partial least squares (PLS) approach." (p. 335)
- "With causal indicators we need a census of indicators, not a sample. That is, all indicators that form eta should be included." (p. 337, citing Bollen and Lennox, 1991)
- "There is a very real danger of model misspecification at the indicator specification stage if the omitted indicators are, in fact, correlated with those included in the formative measure." (p. 337)
- "As the amount of variance of the residual increases, the meaning of the construct becomes progressively ambiguous. Certainly the meaning of a construct is elusive when most of its variance is attributable to unknown factors." (p. 338, citing Williams et al., 2003)
- "Uncritical application of a reflective model to oversimplify the measurement of constructs risks reducing the rigor of business theory and its relevance for managerial decision making." (p. 336, citing Coltman et al., 2008)
