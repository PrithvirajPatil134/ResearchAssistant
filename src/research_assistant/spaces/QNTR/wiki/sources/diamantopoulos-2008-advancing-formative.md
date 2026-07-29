---
type: source
title: "Advancing Formative Measurement Models"
maturity: seed
tags: [formative-constructs, measurement-model, misspecification, higher-order-constructs, causal-indicators, methodology]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [research_paper, term_paper, thesis]
sources:
  - path: "knowledge/Reference Material/2008 - JBR - Diamantopoulos et al - Advancing Formative Measurement Models.pdf"
    type: pdf
authors:
  - "Diamantopoulos, A."
  - "Riefler, P."
  - "Roth, K. P."
year: 2008
journal: "Journal of Business Research"
volume: "61(12)"
pages: "1203-1218"
ingested: 2026-07-28
draws_from: []
related_sources:
  - wiki/sources/diamantopoulos-2011-formative-measures-cbsem
target_path: src/research_assistant/spaces/QNTR/wiki/sources/diamantopoulos-2008-advancing-formative.md
---

## Summary

A state-of-the-art review that merges contributions from the psychology, management, and marketing literatures on formative measurement. The paper has two aims: (a) to highlight the consequences of measurement-model misspecification, and (b) to review key unresolved issues in the conceptualization, estimation, and validation of formative measures [source, Abstract, p.1203]. It argues that although formative (cause) indicators were introduced more than forty years ago, empirical application remains scarce, and Bollen's (1989) observation that "cause indicators are neglected despite their appropriateness in many instances" still holds [source, §1, p.1204].

This paper is the review-and-evidence companion to the already-ingested Diamantopoulos (2011) MISQ commentary, which is a LISREL/CSA how-to guide. The 2011 paper tells you *how* to estimate a formative model; this 2008 paper tells you *why misspecification is costly* and surveys the *open problems*. See `wiki/sources/diamantopoulos-2011-formative-measures-cbsem.md` for the estimation mechanics that this paper does not walk through.

Relevance: Prof. Prashar's May 5 feedback flagged "Agentic AI governance maturity" as likely a formative construct [QNTR/feedback/response_prof_prashar_termpaper_review_20260505.md, §Method, as recorded in wiki/concepts/formative-construct-measurement.md]. This paper supplies the argument for why specifying it correctly matters and how a multidimensional governance-maturity construct would be modelled.

## Key Arguments

1. **Formative and reflective models differ in the direction of causality.** In a reflective model each measure is an effect of the construct (x_i = lambda_i*eta + epsilon_i), all measures must be positively intercorrelated, and a model with 3+ indicators is identified [source, §2, pp.1204–1205]. In a formative model the indicators are causes of the construct (eta = sum(gamma_i*x_i) + zeta); indicators need not correlate (positively, negatively, or not at all), carry no individual measurement error, the disturbance zeta sits at the construct level, and the model in isolation is underidentified [source, §2, p.1205].

2. **Omitting a formative indicator changes the construct.** Because each indicator captures a distinct facet, "omitting an indicator potentially alters the nature of the construct" (Bollen and Lennox, 1991), so a census of indicators is required, not a sample [source, §2 p.1205; §4.2 p.1210].

3. **Higher-order (multidimensional) formative constructs come in three usable types** (adapting Jarvis et al. 2003) [source, §3, pp.1205–1208]:
   - **Type I** (formative first-order, formative second-order; "aggregate/composite/emergent" model): dimensions form the second-order construct; error terms exist at both dimension and construct level. Example: Yi and Davis' (2003) "observational learning processes" formed by four dimensions.
   - **Type II** (reflective first-order, formative second-order): each dimension is measured reflectively but the dimensions form the second-order construct; error at both the manifest-indicator level (measurement error) and the second-order level. Example: Lin et al.'s (2005) "customer perceived value."
   - **Type III** (formative first-order, reflective second-order): virtually no empirical examples; the error term is hard to interpret, indicator meaning is ambiguous, and the model cannot be estimated with current identification procedures. The authors conclude Type III "do not represent an appealing option" [source, §3, p.1208].

4. **Misspecification is common.** Applying the Jarvis et al. (2003) audit approach, about one third of studies in four major marketing journals are misspecified; Fassot (2006) reports 35% in German management journals; Fassot and Eggert (2005) report ~80% in a German marketing journal; Podsakoff et al. (2006) report 62% of constructs in three strategic-management journals; and 47% is reported for leadership research [source, §4, pp.1208–1209]. The dominant error is the Type I error of using reflective indicators where formative would be appropriate; the reverse (Type II error) is negligible [source, §4, p.1208].

5. **Misspecification biases structural estimates in a direction that depends on construct position** [source, §4.1, pp.1208–1210]:
   - Wrongly reflective specification of an **exogenous** construct **overestimates** its structural effect on other constructs. Simulated overestimation ranged 335%–555% (Jarvis et al. 2003) and averaged 429% (MacKenzie et al. 2005).
   - Wrongly reflective specification of an **endogenous** construct **underestimates** the effect of its antecedents. Underestimation ran 88%–93% (Jarvis) and averaged 84% (MacKenzie).
   - The mechanism: a reflective treatment of a formative construct reduces its variance (a reflective construct's variance = common variance of its measures, whereas a formative construct's variance = total variance of its measures) [source, §4.1, p.1210].

6. **Incorrect item purification is a second, distinct source of bias.** Applying reflective purification rules (dropping low item-total-correlation items) to formative indicators removes "precisely those items that would most alter the empirical meaning of the construct" (Jarvis et al. 2003). In Diamantopoulos and Siguaw's (2006) illustration, reflective vs. formative purification of the same 30-item pool shared only two final items [source, §4.2, p.1210].

7. **Fit indices do not detect misspecification.** Across the six studies reviewed, CFI, GFI, SRMR, and RMSEA for misspecified models were "highly acceptable" and similar to correctly specified models; MacKenzie et al. (2005) concluded "each of the four goodness-of-fit indices failed to detect the misspecification." Only chi-square per degree of freedom was consistently higher in the wrongly reflective models [source, §4.3, pp.1210–1211].

8. **The construct-level error term represents omitted causes, not measurement error.** Diamantopoulos (2006) is cited to correct earlier interpretations: because formative indicators are specified as error-free, the disturbance cannot be measurement error; it is "the impact of all remaining causes other than those represented by the indicators." The more comprehensive the indicator set, the smaller the error term's influence; as its variance grows, "the meaning of the construct becomes progressively ambiguous" (Williams et al. 2003) [source, §5.2, pp.1211–1212].

9. **Identification requires the 2+ emitted paths rule, achievable three ways.** Beyond the t-rule and scaling rule (three scaling options: fix a formative path, fix a path to a reflective endogenous variable, or standardize construct variance to unity), identifying the construct-level disturbance requires the formative construct to emit at least two paths to other reflective constructs/indicators. The three approaches are: (a) add two reflective indicators (yields a MIMIC-type model); (b) add two reflectively-measured outcome constructs; (c) a mixture — one reflective indicator plus one reflective construct [source, §5.3.3, pp.1213–1214]. If a construct emits only one path, identification requires fixing the disturbance variance to zero, which imposes the untenable assumption that indicators completely capture the construct [source, §5.3.3.3, p.1215].

10. **Reliability and validity assessment for formative measures differ from reflective.** Internal-consistency reliability is not meaningful because indicators may correlate negatively or not at all [source, §5.4.1, p.1215]. Recommended instead: test-retest reliability (Bagozzi 1994; Diamantopoulos 2005); individual-indicator validity via the significance of gamma-parameters and correlation with an external/global measure; construct validity via nomological and criterion-related relationships (formative constructs "are not invalidated by low internal consistency" — Bollen and Lennox 1991); using the error-term variance as a validity indicator (lower variance = more valid); and confirmatory tetrad analysis (CTA) as a test of whether a formative vs. reflective specification is appropriate [source, §5.4.2, pp.1215–1216].

## Methodology

This is a conceptual/integrative review, not an empirical study. It (a) tabulates six empirical studies on the consequences of misspecification, classified by source of bias (reversed causality vs. incorrect item purification) and by construct position (exogenous vs. endogenous) — Table 2, p.1209; and (b) tabulates examples of formatively-measured constructs across consumer-behaviour, IT, management, and marketing literatures with their estimation methods (SEM/PLS, MIMIC, regression) — Table 1, pp.1206–1207. It does not report primary data or a worked estimation example.

## Findings

- Direction of bias is position-dependent: exogenous misspecification overestimates (335%–555%; avg 429%), endogenous misspecification underestimates (88%–93%; avg 84%) [source, Table 2 / §4.1, pp.1209–1210].
- Goodness-of-fit indices are not diagnostic of misspecification; only chi-square/df gives a weak signal [source, §4.3, pp.1210–1211].
- Reflective vs. formative purification of the same item pool can produce almost entirely non-overlapping final scales (2 of 30 shared items in the cited example) [source, §4.2, p.1210].
- Type III higher-order formative models are effectively non-estimable and not recommended [source, §3, p.1208].

## Relevance to Research

1. **Why correct specification of governance maturity matters (not just how).** If "agentic AI governance maturity" is formative but modelled reflectively, and it sits as the *exogenous* driver of enterprise risk and business performance, this paper predicts its structural effects would be *overestimated* — and standard fit indices would not warn you [source, §4.1 & §4.3, pp.1209–1211]. This strengthens the case, already noted in the 2011 page, for treating the construct as formative from the outset.

2. **Governance maturity is plausibly a Type I higher-order formative construct.** If governance maturity is composed of dimensions such as structural, procedural, and relational governance practices — each itself formed by specific practices — the Type I aggregate model (formative first-order, formative second-order) is the matching structure, with error at both levels [source, §3, pp.1205–1208]. This is a modelling detail the 2011 CBSEM page does not develop.

3. **Identification via two outgoing paths is directly satisfied by the term-paper model.** The three-proposition framework (governance -> risk; governance -> performance) gives the formative governance construct two emitted paths, satisfying the 2+ emitted paths rule without the zero-error constraint [source, §5.3.3, pp.1213–1214]. This corroborates the identification strategy in the 2011 page from a second, independent source.

4. **Validity plan for the construct.** Because internal-consistency reliability does not apply, the validation plan should use test-retest reliability, gamma-significance and external-measure correlation for indicator validity, nomological/criterion validity at the construct level, and optionally CTA to confirm the formative specification empirically [source, §5.4, pp.1215–1216].

5. **Caution flag for endogenous / moderator use.** If a later model places a formative construct in an endogenous or moderator position (e.g., control rigidity as a formative mediator), the paper's future-research section flags this as conceptually unsettled: Wiley (2005) argues there is "no mechanism by which an antecedent variable can influence a formative index," and modelling formative moderators needs more research [source, §6, p.1216]. This is a live caveat for the DBA thesis measurement design.

## Limitations

- A review, not an empirical test; it synthesizes others' evidence rather than generating new estimates.
- It surveys "sometimes contradicting" views and leaves several debates explicitly open (error-term interpretation, validity assessment, endogenous formative constructs, whether formative measurement should be used at all — Bagozzi 2007 and Howell et al. 2007 are cited as skeptics; the authors and Bollen 2007 defend it) [source, §5 & §6, pp.1211, 1216].
- No software-specific or step-by-step estimation guidance (that is the domain of the 2011 MISQ companion page).
- Does not resolve identification for higher-order formative models, referring readers elsewhere [source, §5.3.3, p.1215].

## Key Quotes

- "[M]ost researchers in the social sciences assume that indicators are effect indicators. Cause indicators are neglected despite their appropriateness in many instances." (Bollen 1989, quoted p.1204)
- "omitting an indicator potentially alters the nature of the construct" (Bollen and Lennox 1991, quoted p.1205)
- "each of the four goodness-of-fit indices failed to detect the misspecification of the measurement model" (MacKenzie et al. 2005, quoted p.1211)
- "following standard scale development procedures — for example dropping items that possess low item-to-total correlations — will remove precisely those items that would most alter the empirical meaning of the construct" (Jarvis et al. 2003, quoted p.1210)
- "the error term in a formative measurement model represents the impact of all remaining causes other than those represented by the indicators included in the model" (Diamantopoulos 2006, quoted p.1211)
- "causal indicators are not invalidated by low internal consistency, so to assess validity we need to examine other variables that are effects of the latent variable" (Bollen and Lennox 1991, quoted p.1215)
- "there is no mechanism by which an antecedent variable can influence a formative index" (Wiley 2005, quoted p.1216)

## Cross-Reference

- Companion estimation guide: `wiki/sources/diamantopoulos-2011-formative-measures-cbsem.md` (LISREL/CSA how-to; MIMIC worked example; PLS vs CBSEM decision).
- Concept: `wiki/concepts/formative-construct-measurement.md` (this source is its 2nd source).
