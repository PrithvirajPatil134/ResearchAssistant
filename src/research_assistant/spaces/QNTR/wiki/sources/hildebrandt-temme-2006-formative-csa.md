---
type: source
title: "Formative Measurement Models in Covariance Structure Analysis: Specification and Identification"
maturity: seed
tags: [formative-constructs, measurement-model, cbsem, csa, identification, structural-equation-modeling, methodology]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [research_paper, term_paper, thesis]
source_path: "knowledge/Reference Material/2006 - Hildebrandt and Temme - Formative measurement models in Covariance sturcture analysis.pdf"
authors:
  - "Hildebrandt, L."
  - "Temme, D."
year: 2006
journal: "SFB 649 Discussion Paper 2006-083, Humboldt-Universität zu Berlin"
volume: "2006-083"
pages: "1-14"
ingested: 2026-07-28
draws_from: []
related:
  - wiki/sources/diamantopoulos-2011-formative-measures-cbsem
  - wiki/sources/diamantopoulos-2008-advancing-formative
target_path: src/research_assistant/spaces/QNTR/wiki/sources/hildebrandt-temme-2006-formative-csa.md
---

## Summary

An SFB 649 discussion paper aimed at researchers who are "unsure about how to specify formative measurement models in software programs like LISREL or AMOS and to establish identification of the corresponding structural equation model" [source, PDF p.2, Abstract]. It makes two contributions. First, it introduces a mainly graphically-oriented procedure to establish the identification status of a specific class of recursive models with formative indicators, and uses it to show that some models "have erroneously been considered underidentified" [source, PDF p.2, Abstract]. Second, it argues that specifying formative indicators as exogenous variables "rises serious conceptual and substantial issues" when the formative construct is truly endogenous, i.e. influenced by more remote causes, and proposes specifying both the direct and the indirect (via the indicators) effects of those remote causes [source, PDF p.2, Abstract; PDF p.5, §1]. An empirical study on the causes and effects of brand competence illustrates the point [source, PDF p.2, Abstract].

This paper is the covariance-structure-analysis (CSA) specification-and-identification treatment that complements the two Diamantopoulos pages already in the wiki. Where Diamantopoulos (2011) is the LISREL estimation how-to and Diamantopoulos, Riefler & Roth (2008) is the review-and-evidence case for why misspecification is costly, Hildebrandt & Temme add an operational method to *check* whether a given larger model is identified and a distinct specification problem for endogenous formative constructs. See `wiki/sources/diamantopoulos-2011-formative-measures-cbsem.md`, `wiki/sources/diamantopoulos-2008-advancing-formative.md`, and the shared concept `wiki/concepts/formative-construct-measurement.md` (this source is its 3rd source).

Relevance: Prof. Prashar's May 5 feedback flagged "Agentic AI governance maturity" as likely a formative construct [as recorded in wiki/concepts/formative-construct-measurement.md]. This paper supplies (a) a way to verify the identification of the term-paper's governance-risk-performance model and (b) a caution about how to specify the effects of any remote causes of governance maturity.

## Key Arguments

1. **Why not just default to PLS.** The broadened view of measurement models has pushed researchers toward partial least squares (PLS; Wold 1966) for formative constructs, largely because PLS avoids the identification problem and estimation is easy; the "Churchill paradigm" (Churchill 1979) had tied reflective constructs to CSA [source, PDF pp.3-4, §1]. H&T give three reasons not to abandon CSA: (a) PLS unbiasedness rests on the "consistency at large" condition with respect to the number of indicators (Wold 1980), which "is almost never fulfilled in empirical studies," so PLS estimates are "typically biased to a certain degree" (Dijkstra 1984; McDonald 1996); (b) beyond the linear predictor specification PLS imposes no restrictions on the data, so "no overall test of model fit is available so far"; (c) PLS is restricted to recursive models, with no feedback loops or reciprocal relationships [source, PDF pp.4-5, §1].

2. **The two basic identification conditions (necessary but insufficient).** As with reflective constructs, identification is bound to (i) the t-rule — the number of free parameters must not exceed the non-redundant elements of the empirical variance-covariance matrix (Bollen 1989); and (ii) scaling each latent variable, e.g. by fixing the CLV's path to a reflective indicator or fixing the CLV variance to 1 (Bollen & Davis 1994; MacCallum & Browne 1993) [source, PDF p.5, §2].

3. **Established identification rules can be misleading.** Jarvis, MacKenzie & Podsakoff (2003, p.213) state that for a formative construct's error term to be identified it must emit paths to "at least two unrelated latent constructs with reflective indicators," or two reflective indicators, or one reflective indicator plus one reflective-indicator construct. Relying on the "unrelated" wording, MacKenzie, Podsakoff & Jarvis (2005) concluded that the job-perception construct in Law & Wong's (1999) model was not identified because "the two constructs were causally related" (p.716). H&T counter: at least two emitted paths are indeed necessary, but "the former need not be unrelated in a larger model" [source, PDF pp.5-6, §2].

4. **A graphical three-step identification procedure.** For recursive models (no feedback loops, no correlated disturbances) in which structural relationships hold among the variables directly dependent on the CLV, identification can be checked by: (I) transform the original model into a model without CLVs; (II) check identification of the transformed model; (III) verify that the original model's parameters can be unambiguously derived from the transformed model's parameters [source, PDF p.6, §2]. The transformation uses five substeps: (1) choose a CLV; (2) connect all variables directly influenced by that CLV with double-headed arrows; (3) eliminate all arrows emanating from the CLV; (4) substitute the CLV by its formative indicators; (5) draw an arrow from each indicator to the variables originally influenced by the CLV; repeat while any CLV remains [source, PDF p.6, §2]. (A related but fully algebraic procedure is Cantaluppi 2002.)

5. **Worked identification of the Law & Wong (1999) model.** After transformation, the graph shows a "bow-pattern" (Brito & Pearl 2002) and is not identified per se, so H&T apply Rigdon's (1995) identification rules for nonrecursive blocks of two endogenous variables. The transformed model resembles Rigdon's case 8; because the formative indicators influence both job satisfaction and turnover intention they do not contribute to identification, and removing them yields Rigdon's case 3, which is identified. The original parameters can then be unambiguously recovered, so the original model is identified — contradicting the earlier "underidentified" verdict [source, PDF pp.6-7, §2].

6. **Quasi-exogenous vs. endogenous CLV.** Formative indicators are almost always specified as exogenous regardless of the construct's causal status, yet formative constructs are by definition endogenous. H&T distinguish: a **quasi-exogenous** CLV is determined only by its indicators plus a disturbance (covariances between its formative indicators and other exogenous variables are then freely estimated; MacCallum & Browne 1993); an **endogenous** CLV is additionally influenced by more remote causes such as reflective latent constructs or a quasi-exogenous CLV. Treating the indicators of a truly endogenous CLV as exogenous is the problematic habit [source, PDF p.8, §3].

7. **The specification error for endogenous CLVs (conceptual and substantial).** Conceptually, if remote causes are assumed to influence the CLV while its indicators are specified as exogenous, "it remains unclear how a causal process can actually take place"; the effect should operate through some or all of the formative indicators, turning them endogenous (illustrated by a salary increase raising job satisfaction via pay satisfaction, one of its components) [source, PDF p.8, §3]. Substantially, specifying only the "direct" effect of a remote cause on the CLV "will almost inevitably lead to a biased estimate." In Model A the exogenous latent variable xi1 has a direct effect (gamma31) on the endogenous CLV plus effects on the formative indicators (gamma11, gamma21), giving a total effect of gamma31 + gamma11*beta31 + gamma21*beta32; Model B (the common approach) estimates only covariances between xi1 and the "exogenous" indicators, restricting xi1's influence to the direct effect gamma31. Depending on the signs of the coefficients, the true impact of xi1 is then under- or over-estimated. Critically, the two specifications "are empirically undistinguishable (i.e. they show the same overall fit)," so fit statistics cannot detect the error [source, PDF pp.8-9, §3].

## Methodology

The identification argument is analytical/graphical, worked on the Law & Wong (1999) job-perception model [source, PDF pp.5-7, §2]. The specification argument is illustrated by an empirical covariance-structure study of brand competence [source, PDF pp.9-11, §4]:

- Data: survey responses from 261 consumers collected by GfK Market Research, evaluating brands in the fixatives and denture cleansers market [source, PDF p.9, §4].
- Constructs: perceived brand competence (defined via Lau & Lee 2000 as "the ability to solve a consumer's problem and to meet his or her need") is **formed by four formative indicators** (e.g. "stands for hygiene and cleanliness," "stands for attractiveness and beauty"); the two exogenous causes, advertising ("really advertises a lot") and recommendations ("is recommended by dentists"), are each measured by a single indicator; brand strength is reflectively measured by eight indicators (affective, cognitive, intentional responses). To identify the model, brand competence is additionally measured by two reflective indicators [source, PDF p.9, §4].
- Estimation: maximum likelihood in LISREL 8.72 [source, PDF p.10, §4].
- Three model variants are compared: Model 1 (formative indicators endogenous, direct + indirect effects), Model 2 (formative indicators specified as exogenous, direct effects only), Model 3 (Model 1 with the recommendation direct effect and gamma41 fixed to zero) [source, PDF pp.10-11, §4, Tables 1-2].

## Findings

- **Model 1 fit** (endogenous formative-indicator specification): chi-square = 158.05, df = 87, RMSEA = 0.052, CFI = 0.987 — described as "excellent" [source, PDF p.10, §4]. Advertising has a significant positive direct effect on brand competence (gamma51) and on one component (gamma21), yielding a significant positive total effect. Recommendations exert only an indirect effect (raising two indicators, significant at 5%); the indirect effect is significantly positive but the total effect is not significant, because the (non-significant) direct effect is negative [source, PDF p.10, §4; Tables 1-2, PDF p.11].
- **Model 2** (formative indicators specified as exogenous): only direct effects of the two exogenous variables are estimated, so — the indirect effects having been shown positive — the total effects are underestimated relative to Model 1 [source, PDF p.10, §4; Table 2, PDF p.11].
- **Model 3** (recommendation direct effect and gamma41 fixed to zero): model fit deteriorates almost not at all (chi-square = 158.66, df = 89), justifying the conclusion that "dentists recommending a brand indeed exert a positive influence on brand competence" [source, PDF p.10, §4]. The authors note that the standard exogenous-indicator specification "might have led managers to undervalue the positive effect recommendations by dentists have on the perceived competence of a brand" [source, PDF p.12, §5].

## Relevance to Research

1. **Verifying identification of the governance model.** The term-paper's governance-risk-performance model has the formative governance-maturity construct emitting paths to enterprise risk and to business performance. Diamantopoulos already establishes that two emitted paths satisfy the identification rule; H&T add that, for a recursive model, one can *check* identification via the transform-and-reclassify procedure, and that two paths leading to *causally related* downstream constructs (risk and performance are related) do not by themselves make the construct underidentified [source, PDF pp.5-7, §2]. This directly answers the concern the MacKenzie et al. (2005) reading would raise about the risk-performance sub-structure.
2. **How to specify remote causes of governance maturity.** If governance maturity is a truly endogenous formative construct (driven by more remote causes such as organizational or regulatory antecedents), H&T warn against the common practice of only estimating covariances between those antecedents and the "exogenous" formative indicators. Specifying both the direct effect on the construct and the indirect effects through the indicators avoids under-/over-estimating the antecedent's total effect — an error that fit indices will not catch because the two specifications fit identically [source, PDF pp.8-9, §3].
3. **CSA vs. PLS decision, sharpened.** The "consistency at large" argument (Wold 1980; PLS bias when indicator counts are small, per Dijkstra 1984 and McDonald 1996) gives an estimation-quality reason, beyond global fit and model comparison, to prefer CSA/CBSEM for the formative governance construct if sample and indicator counts permit [source, PDF pp.4-5, §1].

## Limitations

- The graphical identification procedure is explicitly restricted to **recursive** models (no feedback loops, no correlated disturbances); the authors flag nonrecursive models as a target for future research [source, PDF p.6, §2; PDF p.12, §5].
- Step III (unambiguous derivation of the original parameters from the transformed model) is asserted for the Law & Wong example but "not shown here because of space limitations" [source, PDF p.7, §2].
- The empirical illustration is a single marketing dataset (brand competence, N=261); generalization to other domains is not tested [source, PDF p.9, §4].
- It is an SFB 649 discussion paper (working-paper series 2006-083), not a peer-reviewed journal article, so it should be cited at that status [source, PDF p.1; PDF p.18].

## Key Quotes

- "Many researchers seem to be unsure about how to specify formative measurement models in software programs like LISREL or AMOS and to establish identification of the corresponding structural equation model." [source, PDF p.2, Abstract]
- "Although it is true that at least two paths leading to other variables are necessary for a CLV to be identified, the former need not be unrelated in a larger model." [source, PDF p.6, §2]
- "If we take the view that formative indicators produce the CLV serious, such an effect should mainly operate via all or some of the formative indicators, thus turning the latter into endogenous variables." [source, PDF p.8, §3]
- "It should be noted that the two alternative specifications are empirically undistinguishable (i.e. they show the same overall fit)." [source, PDF p.8, §3, footnote 4]
- "Even two related variables influenced by a formative construct can suffice to identify that construct if it is embedded in a larger network." [source, PDF p.12, §5]

## Cross-Reference

- Estimation how-to companion: `wiki/sources/diamantopoulos-2011-formative-measures-cbsem.md` (LISREL MIMIC worked example; PLS vs CBSEM decision).
- Review-and-evidence companion: `wiki/sources/diamantopoulos-2008-advancing-formative.md` (misspecification bias by construct position; higher-order formative typology).
- Concept: `wiki/concepts/formative-construct-measurement.md` (this source is its 3rd source; adds the graphical identification procedure and the endogenous-CLV specification issue).
