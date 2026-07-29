---
type: source
title: "Enhancing Rigor in Quantitative Entrepreneurship Research"
maturity: seed
tags: [research-methods, quantitative-rigor, reproducibility, endogeneity, measurement-validity, effect-size, editorial]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [research_paper, thesis, term_paper, literature_review]
draws_from: []
authors: ["Maula, Markku", "Stam, Wouter"]
year: 2019
journal: "Entrepreneurship Theory and Practice"
volume: "00(0)"
pages: "1-32"
source_path: "knowledge/Session 1-4/S1-2 QNTR 2025 - Enhancing rigor in quant research.pdf"
doi: "10.1177/1042258719891388"
ingested: 2026-07-28
target_path: src/research_assistant/spaces/QNTR/wiki/sources/maula-stam-enhancing-rigor-quant-research.md
---

# Enhancing Rigor in Quantitative Entrepreneurship Research

An *Entrepreneurship Theory and Practice* (ETP) editorial by Maula and Stam that reviews recurring empirical concerns in quantitative entrepreneurship research, connects them to recent methodological guidelines in the social sciences, and closes with seven best-practice recommendations [p.1, Abstract]. The authors write as journal editors summarizing "common key concerns of editors and reviewers" alongside newer methods [p.1]. (The filename contains "QNTR 2025", the course-session label; the article's own copyright line and DOI 10.1177/1042258719891388 place it in 2019 [p.1].)

## Why the push for rigor

Three developments drive the call for more rigor: growing recognition that popular empirical approaches have important limitations, a broad concern about reproducibility of prior findings in social science, and rapid advances in methods that enable more rigorous studies [p.1]. The "replication crisis" has been acknowledged in economics, sociology, political science, and psychology, and business and management is "not immune" [p.2]. Many leading journals have revised editorial policies to ban poor practices and promote transparency [p.2]. Entrepreneurship poses distinctive difficulty because of the uncertainty, heterogeneity, and disequilibrium in entrepreneurial phenomena and the common focus on new ventures for which reliable data are often unavailable [p.2, p.4].

## The seven recommendations (Table 1)

Summarized from Table 1 [p.2-3]:

1. Match the research design with the research problem. The research problem should drive design and method choice; be clear whether the study is exploratory or hypothesis-testing; consider causal identification at the design stage [p.2-3].
2. Understand the advantages and limitations of particular data sources, whether self-collected or from a provider; consider novel sources such as web-scraped and video data [p.3].
3. Ensure the measures measure what they are supposed to measure; be transparent about how measures were constructed, adapted, and validated; consider novel techniques such as text mining [p.3].
4. Select appropriate analytical tool(s) given the research question and setting (type of measures, endogeneity, longitudinal structure); consider newer approaches such as Bayesian statistics [p.3].
5. Report methods and results transparently and reproducibly; probe interaction, mediation, and nonlinear effects with best practices; avoid the term "statistically significant"; consider practical significance; use visualizations [p.3].
6. Develop a robust, reproducible workflow to facilitate error detection/correction and replication [p.3].
7. Continue lifelong learning about evolving methods [p.3].

## Data sources (detailed)

- Survey data: allows direct measurement of complex latent constructs through multi-item scales, but is prone to nonresponse, retrospective, and common-method bias; single-survey single-respondent designs are increasingly not accepted; multi-wave surveys and multiple informants are "becoming the new standard" [p.5-6].
- Archival data: enables large repeated measures across levels but variables are rarely ideal; merging sources is non-trivial; watch backfilling, reclassification, survivorship, and sample-selection bias in commercial databases [p.5-6].
- Website-scraped data: fast, unobtrusive, large-scale, but requires theory-driven design and attention to ethics and weaknesses [p.6-7].
- Video data: captures bodily expression, emotion, decision-making, identity; used both by coding existing video and creating artificial video for experiments [p.6-7].
- Experimental data: can overcome endogeneity but is under-used in ETP submissions; student/MTurk samples may not capture entrepreneurial stakes; vignette methodology and field experiments raise realism [p.7].
- Triangulating multiple data sources / mixed methods: combining quantitative and qualitative data can offset single-method weaknesses, but requires justification and clear reporting of how techniques were combined [p.7].
- Data transparency: report data overlap across papers from the same dataset; ETP requires a separate document detailing variable differences; a "uniqueness analysis table" (Kirkman & Chen, 2011) in the cover letter helps; guard against "salami sliced" publications, though repeating a validated predictor across studies can be legitimate [p.7-8].

## Measurement

- Construct validity: provide clear construct definitions, show indicators reflect constructs, prefer multi-item scales over single/categorical indicators, and report reliability and dimensionality [p.8-9].
- Methodological myths: many "rules of thumb" and cutoffs have been dismissed, including the false notion that Cronbach's alpha above .70 establishes internal consistency [p.8-9].
- Transforming variables: give a theoretical rationale for any (nonlinear) transformation, report exactly how variables were transformed, and adjust visualizations accordingly [p.9].
- Common method bias: Harman's single-factor test is generally not sufficient; the CFA marker technique with appropriate marker variables is preferred; post hoc tests cannot fully compensate for a poor ex-ante design [p.9].
- Control variables: select on theoretical grounds and justify inclusion; unnecessary or "bad controls" (outcomes of the focal predictor) can bias estimates [p.9].
- Novel measurement: computer-aided text analysis (CATA), topic modeling, and NLP via machine learning derive measures from text but require explicit treatment of measurement error [p.9].

## Analyses

- Choice of method: justify the analytical method with theory and/or evidence; consider combining techniques [p.10].
- Longitudinal analysis: longitudinal data alone does not control unobserved heterogeneity without fixed effects or another appropriate method; the Hausman test for random-vs-fixed effects has been superseded by focus on between- vs within-unit variance, with hybrid models often preferable; other options include GMM dynamic panel models, event-history/survival models, latent growth curve models, and difference-in-differences [p.10].
- Endogeneity: establishing causality requires correlation, temporal precedence, and ruling out other causes; omitted-variable bias is a prime source; correction methods include instrumental variables, regression discontinuity design, difference-in-differences, synthetic control, and structural econometric models; Heckman models are frequently misused (Certo et al., 2016); propensity score matching has limitations, with coarsened exact matching recommended as a robust alternative; SEM and the potential-outcomes framework are equivalent (not inferior), and DAGs help identify required assumptions; post hoc correction cannot fix a poor ex-ante design, and endogeneity can never be fully solved [p.11-12].
- Nonlinear models: limited dependent variables need logit, probit, tobit, Poisson, negative binomial, or survival models (LPM sometimes used for interpretability); common pitfalls are misinterpreting coefficients, modeling interactions, comparing coefficients across groups, and model-fit measures (Hoetker, 2007) [p.12-13].
- Moderation and mediation: common errors include dichotomizing moderators, not controlling main effects, claiming centering reduces collinearity, inaccurate interaction plotting, and failing to run simple-slope tests; special care for U-shaped relationships and turning points outside the data range [p.13].
- Multilevel analyses: use HLM/RCM, mixed-effects, or multilevel SEM to handle nested data; report multilevel properties and take care with cross-level interactions [p.13-14].
- Bayesian approaches: suited to building on prior findings and quantifying evidence for any hypothesis (including the null); use with care; software integration (e.g. Stata) has removed prior computational barriers [p.14].
- The authors note the simplest feasible analysis is generally preferable unless a more complex model is specifically warranted [p.14].

## Reporting

- Statistical significance: report exact p values as continuous measures and interpret in context; do not label findings "statistically significant" or "nonsignificant"; asterisks and threshold-based publication are discouraged (p-hacking); consider false-discovery-rate adjustment for multiple tests; clarify one- vs two-tailed tests [p.15].
- Effect size: a low p value does not imply a large or important effect; report effect sizes with confidence intervals, in original units and standardized (Cohen's d, Pearson's r); use marginal effects (especially average marginal effects), often plotted; avoid arbitrary cutoffs and incorporate practical/qualitative judgment [p.15-16].
- Visualizations: graphs communicate distribution and uncertainty; creativity encouraged (heat maps), aided by ggplot2 (R), Matplotlib/Seaborn/Plotly/Bokeh (Python), PROC SGPLOT (SAS) [p.16].
- Statistical power: rarely reported; provide a power analysis and discuss how power may have affected conclusions [p.16-17].
- Missing data: avoid uncritical listwise deletion; use multiple imputation or full-information maximum likelihood; report extent and handling [p.17].
- Outliers and influential cases: report how outliers were defined, identified, and handled; some outliers carry theoretical value (rare events such as VC backing or IPOs) [p.17].
- Robustness analyses: run and transparently report alternative models (online appendix if needed); choose the main model and robustness checks by justified priority [p.17-18].
- Transparency and attention to detail: document choices from major to minor; typos and small errors undermine credibility [p.18].

## Workflow and data management

Rigorous analysis combines many data sources, derived variables, and many tables/plots; without careful planning, code becomes error-prone [p.18]. Recommendations: careful data-management workflow and documentation, sharing and cross-checking code within the author team ("two pairs of eyes usually spot more errors than one"), data-management plans, study preregistration, and open-science practices; publishing data and analysis code (as online appendices) facilitates replication [p.18].

## Conclusion

Expectations for rigor are growing; the field can learn from other disciplines improving their practices [p.19]. There is no perfect empirical study that can "confirm" a hypothesis; evidence can at best reject one, and causal identification is best achieved through a cumulative body of research with replications [p.19]. The American Statistical Association has moved to discourage the term "statistically significant" [p.19-20]. The authors summarize the guidance with the mnemonic **ATOM**: "Accept uncertainty. Be thoughtful, open, and modest." [p.20].

## Relevance to current deliverables

This editorial functions as a design-and-reporting rigor checklist for quantitative work. It applies to the QNTR term paper / agentic-AI-governance research thread and to DBA thesis design where quantitative hypothesis testing, measurement validity, endogeneity, and reproducible reporting are in scope. Specific applications should be grounded in the deliverable's own design decisions rather than asserted here. The consolidated checklist form of this guidance lives at `../methods/quant-rigor-best-practices.md`.
