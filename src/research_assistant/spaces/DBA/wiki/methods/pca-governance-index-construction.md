---
type: method
target_path: src/research_assistant/spaces/DBA/wiki/methods/pca-governance-index-construction.md
title: "PCA-Based Multi-Indicator Index Construction (Larcker, Richardson & Tuna 2007)"
maturity: seed
tags: [principal-component-analysis, index-construction, construct-measurement, factor-analysis, reliability, archival]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: DBA
applicable_to: [thesis, research_paper, literature_review]
draws_from:
  DBA:
    - wiki/sources/larcker-2007-governance-index-ssrn
---

# PCA-Based Multi-Indicator Index Construction

## When to use
When a construct is complex and multi-dimensional, and you have many observable/archival indicators but no theory dictating a single proxy or a fixed weighting. The method reduces many indicators to a smaller set of interpretable, reliability-checked indices while mitigating the measurement error of single-indicator or naively-summed-index approaches. [larcker-2007-governance-index-ssrn.pdf, p.3-5]

## Procedure
1. Assemble the full indicator set from all relevant categories (do not restrict to one dimension — omitted dimensions create correlated-omitted-variable bias). [p.4, p.8]
2. Run exploratory PCA; retain factors with eigenvalue > 1 (Kaiser). [p.12]
3. Apply an oblique rotation (allow factor correlation) for interpretability. [p.12]
4. Assign an indicator to a factor when |loading| > 0.40 and the loading is significant; establish significance by bootstrapping (e.g., 1,000 resamples with replacement) on the rotated solution. [p.12]
5. Name factors from their loading indicators. [p.12-13]
6. Score each index as the average of the equal-weighted sum of its standardized indicators (Grice & Harris 1998); standardization sets each index mean to zero. Where a factor contains substitute mechanisms or mixed-sign loadings, build the substitutability into the score explicitly (subtract the offsetting standardized components before dividing by the component count). [p.13-14]
7. Report reliability (Cronbach's alpha per index) and check discriminant validity (confidence intervals of inter-index correlations should exclude unity). [p.14]

## Cautions
Reliability can be modest in early measurement development (Larcker et al. report mean alpha 0.532). The approach is exploratory and descriptive, not causal; governance/predictor endogeneity remains, and the authors address it separately via size-and-industry residualization. [p.14, p.37-42]
