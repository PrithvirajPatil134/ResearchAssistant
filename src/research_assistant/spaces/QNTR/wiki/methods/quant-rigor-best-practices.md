---
type: method
title: "Quantitative Research Rigor: Best-Practice Checklist"
maturity: seed
tags: [research-methods, quantitative-rigor, reproducibility, endogeneity, effect-size, reporting, research-design]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [research_paper, thesis, term_paper]
draws_from:
  QNTR:
    - wiki/sources/maula-stam-enhancing-rigor-quant-research
target_path: src/research_assistant/spaces/QNTR/wiki/methods/quant-rigor-best-practices.md
---

# Quantitative Research Rigor: Best-Practice Checklist

A design-to-reporting checklist for rigorous quantitative studies, drawn from Maula and Stam's ETP editorial [wiki/sources/maula-stam-enhancing-rigor-quant-research.md]. Organized as the seven recommendations plus the stage-specific concerns behind each.

## Design stage
- Let the research problem drive the design; state whether the study is exploratory or hypothesis-testing [source p.2-3].
- Match the unit of analysis to the level of theoretical argument before data collection [source p.4].
- Anticipate threats to validity and consider causal identification at the design stage; a well-designed study demands less post hoc repair [source p.3-4].
- Prefer designing for causal identification over post hoc statistical correction [source p.11-12].

## Data stage
- Justify the data source and explain how data were produced and their limitations [source p.3, p.5-6].
- Move beyond single-wave single-respondent surveys toward multi-wave and multi-informant designs where feasible [source p.5-6].
- For archival/commercial data, address backfilling, reclassification, survivorship, and sample-selection bias [source p.6].
- Report data overlap across papers from the same dataset (uniqueness analysis table) [source p.7-8].

## Measurement stage
- Define constructs clearly; use multi-item scales; report reliability and dimensionality; do not rely on the Cronbach alpha > .70 "myth" [source p.8-9].
- Justify any variable transformation on theoretical grounds and report it exactly [source p.9].
- Treat common method bias ex ante (CFA marker technique); Harman's single-factor test is insufficient [source p.9].
- Justify control variables theoretically; avoid "bad controls" [source p.9].

## Analysis stage
- Justify the analytical method against the hypothesis and setting [source p.10].
- For longitudinal data, use fixed-effects or hybrid models; the Hausman test is superseded by between- vs within-unit reasoning [source p.10].
- Address endogeneity theoretically and empirically (IV, RDD, DID, synthetic control); avoid known misuses (Heckman, PSM); prefer coarsened exact matching over PSM [source p.11-12].
- Interpret nonlinear-model effects carefully (marginal effects, plotting) [source p.12-13].
- Test moderation/mediation with best practices (no moderator dichotomization, control main effects, simple-slope tests) [source p.13]. For the estimation mechanics of mediation, see `data/wiki/shared/methods/baron-kenny-moderation-mediation.md` and `../sources/mackinnon-2007-mediation-analysis.md`.
- For SEM fit-index reporting, see `data/wiki/shared/methods/sem-fit-index-evaluation.md`.
- Prefer the simplest feasible model unless complexity is warranted [source p.14].

## Reporting stage
- Report exact p values; do not label results "statistically significant"; avoid asterisk/threshold reporting; consider FDR adjustment [source p.15].
- Report effect sizes with confidence intervals in original and standardized units [source p.15-16].
- Report statistical power, missing-data handling (MI/FIML), outlier treatment, and robustness checks transparently [source p.16-18].
- Document choices from major to minor to establish credibility [source p.18].

## Workflow stage
- Maintain a documented, reproducible workflow; share and cross-check code; use data-management plans, preregistration, and open-science practices; publish data/code where possible [source p.18].

## Guiding mnemonic
**ATOM**: Accept uncertainty. Be thoughtful, open, and modest [source p.20].
