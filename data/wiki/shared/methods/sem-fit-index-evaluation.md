---
type: method
title: "SEM Fit-Index Evaluation: Cutoffs, Model-Size Effects, Small-df Caveats, and Equivalence Testing"
maturity: working
tags: [sem, structural-equation-modeling, model-fit, fit-indexes, cfi, rmsea, srmr, chi-square, cutoff-criteria, equivalence-testing, quantitative-methods]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: shared
applicable_to: [research_paper, thesis, conference_paper, term_paper]
draws_from:
  QNTR:
    - wiki/sources/hu-bentler-1999-cutoff-criteria-fit-indexes
    - wiki/sources/shi-2017-model-size-effect-sem
    - wiki/sources/shi-2021-sem-fit-small-df
    - wiki/sources/marcoulides-yuan-2016-goodness-of-fit
target_path: data/wiki/shared/methods/sem-fit-index-evaluation.md
---

# SEM Fit-Index Evaluation

A reference hub for deciding how well a structural equation model (SEM) fits, drawing together four QNTR method sources that each address a different facet of the question. This page synthesizes and points to those source pages; it does not restate their derivations. For any specific number or claim, follow the cross-reference to the cited source page.

## The four pieces and how they fit together

The literature does not speak with one voice on how to judge SEM fit. Read together, these four sources move from a fixed standard, to two things that break the standard (large models and very small models), to an alternative that replaces fixed cutoffs entirely.

1. **The fixed-cutoff standard** — Hu & Bentler (1999). The origin of the thresholds now routinely reported: CFI/TLI close to .95, RMSEA close to .06, SRMR close to .08, plus the two-index reporting strategy (SRMR with one supplemental index). See `src/research_assistant/spaces/QNTR/wiki/sources/hu-bentler-1999-cutoff-criteria-fit-indexes.md`.

2. **When the raw chi-square breaks: large models** — Shi, Lee & Terry (2017). The likelihood ratio chi-square test over-rejects correctly specified models as model size grows, driven independently by the number of observed variables (p) and free parameters (q), not fully captured by degrees of freedom. Practical index: sample size should be much larger than p (roughly N ≥ p²); the Yuan, Tian & Yanagihara (2015) empirical correction gave the best Type I error control among four corrections tested [src/research_assistant/spaces/QNTR/knowledge/Key method readings/2017 - Shi et al - Revisiting the model size effect in SEM.pdf, p.8; p.10; p.20]. See `src/research_assistant/spaces/QNTR/wiki/sources/shi-2017-model-size-effect-sem.md`.

3. **When the derived indices break: very small df** — Shi, DiStefano, Maydeu-Olivares & Lee (2021). As degrees of freedom shrink, the three indices behave unequally: RMSEA rises sharply and over-rejects close-fitting models, while SRMR and CFI stay far less sensitive to df. Recommendation for small models (e.g. df = 2): rely more on SRMR and CFI, interpret RMSEA cautiously or via its confidence interval [src/research_assistant/spaces/QNTR/knowledge/Key method readings/2021 - Shi et al - Evaluating SEM model fit with small df.pdf, p.2; p.26]. Low factor loadings (≤ .40) are a shared danger zone for all three indices [same source, p.24]. See `src/research_assistant/spaces/QNTR/wiki/sources/shi-2021-sem-fit-small-df.md`.

4. **Replacing fixed cutoffs: equivalence testing** — Marcoulides & Yuan (2016). Rather than compare an index to a fixed threshold, compute the "T-size" (minimum tolerable size of misspecification) of RMSEA and CFI and read them against adjusted cutoffs recalculated from the model's own df and N. Their worked demonstration flags a misspecified one-factor model that conventional cutoffs would accept but equivalence testing judges "not plausible" [src/research_assistant/spaces/QNTR/knowledge/Key method readings/2016 - Marcoulides and Yuan - New Ways to Evaluate Goodness of Fit.pdf, p.3; p.4]. See `src/research_assistant/spaces/QNTR/wiki/sources/marcoulides-yuan-2016-goodness-of-fit.md`.

## An emergent point across the four sources

No single source states this outright, but read together they converge on it: the conventional fixed cutoffs are conditional, not universal. Hu & Bentler themselves warned that no single value works equally well across all conditions. Shi (2017) shows the underlying chi-square inflates with model size; Shi (2021) shows the derived RMSEA cutoff misleads at small df; Marcoulides & Yuan (2016) argue the fixed-cutoff logic itself gives no information about the degree of misspecification. The practical lesson for any SEM analysis in this workspace: report more than one index, check whether your model is large (p relative to N) or small (df), and treat a single index against a single threshold as the weakest possible fit evidence.

## Practical checklist for an SEM analysis

- Report at least two indices, following Hu & Bentler's SRMR-plus-one strategy.
- Check model size against sample size. If p is large relative to N (well below N ≈ p²), the raw chi-square is likely inflated; consider a correctional statistic (Shi 2017).
- If the model has small df (e.g. a short-scale one-factor model, a latent growth or cross-lagged panel model), de-emphasize RMSEA and lean on SRMR and CFI (Shi 2021).
- Watch factor loadings: with loadings ≤ .40, even SRMR and CFI can misbehave unless N is large (Shi 2021).
- For a stronger statement about the *degree* of misspecification, add equivalence-testing T-size RMSEA/CFI alongside the conventional indices (Marcoulides & Yuan 2016).

## Relevance to workspace deliverables

The Prashar co-authored paper and the DBA thesis both use SEM (per ingest brief). This page is the fit-reporting reference for those deliverables. The cross-space applicability is asserted by the ingest brief; none of the four sources makes a claim about any specific study in this workspace.

## Provenance basis (read before extending this page)

This method page was assembled by the synthesizer during manifest 20260728-191528-4d4d9b02 from four QNTR source pages ingested in the same manifest. The shi-2021 ingestor explicitly flagged a provenance caution about creating this page: it had read only the seed-maturity Hu & Bentler wiki page, not the underlying PDF, and warned a cross-source page must draw faithfully on Hu & Bentler primary content. This page handles that caution as follows:

- Claims about Shi (2017), Shi (2021), and Marcoulides & Yuan (2016) carry direct PDF page citations, taken from those sources' fully-extracted ingest proposals.
- Claims about Hu & Bentler (1999) are cross-referenced to the `hu-bentler-1999-cutoff-criteria-fit-indexes.md` source page (which carries its own PDF page citations) rather than re-asserted here with page numbers not independently verified against the PDF in this pass.
- No fit-index number, cutoff value, or finding on this page is original; each traces to one of the four source pages. Before promoting this page beyond `working`, a reviewer should verify the Hu & Bentler cutoff values against the underlying PDF.
