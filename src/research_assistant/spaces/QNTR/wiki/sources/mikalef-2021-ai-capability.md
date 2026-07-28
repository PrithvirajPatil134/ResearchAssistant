---
type: source
title: "Artificial Intelligence Capability: Conceptualization, Measurement Calibration, and Empirical Study on Its Impact on Organizational Creativity and Firm Performance"
maturity: seed
tags: [ai-capability, pls-sem, construct-development, resource-based-theory]
schema_version: "1.0"
created: 2026-05-07
last_updated: 2026-05-07
originating_space: QNTR
applicable_to: [research_paper, term_paper]
draws_from: []
authors:
  - "Mikalef, P."
  - "Gupta, M."
year: 2021
journal: "Information & Management"
volume: "58"
pages: "103434"
source_path: "knowledge/literature review/Agentic Governance/Relevant Readings/Mgmt-Side Papers (Round 2)/Artificial Intelligence Capability- Conceptualization, Measurement Calibration, and Empirical Study on Its Impact on Organizational Creativity and Firm Performance_Mikalef-Krogstie_2021_A*_8-2.pdf"
ingested: 2026-05-07
---

## Summary

This study develops and validates a measurement instrument for "AI capability," defined as "the ability of a firm to select, orchestrate, and leverage its AI-specific resources" (p.4). Grounded in the Resource-Based Theory (RBT) of the firm, it identifies eight AI-specific resources grouped into three categories (tangible, human skills, intangible) that jointly create an AI capability, then tests the construct's relationship with organizational creativity and firm performance using PLS-SEM on a sample of 143 senior technology managers (pp.1-2).

The paper makes three contributions: (1) a theoretical framework identifying AI-specific resources that form an AI capability, (2) a validated survey instrument to measure organizational AI capability as a third-order formative construct, and (3) empirical evidence that AI capability positively influences organizational creativity (beta=0.573, p<0.001) and firm performance (beta=0.561, p<0.001) (pp.13-14). This is the first large-scale empirical study linking a theoretically grounded AI capability conceptualization with key business indicators (p.14).

## Key Arguments

- AI technologies alone will not deliver competitive gains because they are easily acquired and subject to replication; organizations need complementary resources to build hard-to-imitate AI capabilities (pp.1-2)
- Eight resources jointly form an AI capability, categorized by Grant's (1991) framework (pp.4-6):
  - **Tangible**: Data (access, integration, quality, granularity), Technology (processing power, cloud services, parallel computing, storage, security), Basic Resources (funding, team size, time allocation)
  - **Human skills**: Technical Skills (data science, ML/NLP capabilities, training), Business Skills (understanding where to apply AI, leadership, planning deployments, coordinating with technical staff)
  - **Intangible**: Inter-departmental Coordination (collaboration, shared vision, teamwork), Organizational Change Capacity (anticipating resistance, managing politics, communicating reasons for change), Risk Proclivity (bold posture, high-risk/high-return projects)
- AI capability is conceptualized as a third-order formative construct: the three categories form the construct, not manifest it. Dropping any dimension removes an essential facet that cannot be compensated by others (pp.7-8)
- Four decision rules confirm formative specification: no single dimension adequately captures AI capability alone; dimensions are distinct and non-overlapping; covariation is not required; antecedents of each dimension differ (p.8)
- AI capability influences firm performance both directly and indirectly through organizational creativity (H1-H3 all supported, p.13)
- Organizations with higher risk proclivity establish first-mover advantages in AI, making it harder for competitors to catch up (p.6)

## Methodology

Mixed-methods instrument development following MacKenzie et al. (2011) guidelines (pp.8-10):

**Content validity**: Expert panel of 9 (6 industry practitioners with 20+ years experience, 3 senior academics in IS) mapped items to constructs and recommended improvements (p.10).

**Survey**: Large-scale cross-sectional study. Respondents were members of the Artificial Intelligence and Business Analytics group on LinkedIn. After initial invitation and three reminders, 143 responses received from C-level technology managers (CIO, CTO, IT Director, Head of IT) across industries including technology (25%), banking/financials (20%), ICT/telecom (13%), consulting (11%) (Table 4, p.10).

**Analysis**: PLS-SEM via SmartPLS 3.0 with consistent PLS mode A for reflective constructs. Two-step approach for hierarchical model specification (Benitez et al., 2018). Bootstrap analysis with 500 resamples for significance testing. Confirmatory composite analysis via ADANCO 2.2.0 (pp.9, 12-13).

**Controls**: Firm size and industry. Only firm size had significant effect on performance (beta=0.141, p<0.05) (p.13).

**Validation**: VIF values below 3.3 (no multicollinearity), CR and Cronbach's alpha above 0.70, AVE above 0.50 (lowest: 0.58), HTMT below 0.85, SRMR=0.037 (below 0.080 threshold) (pp.11-12, Tables 5-7).

## Findings

- Model explains 49.2% of variance in organizational creativity and 51.3% in organizational performance (p.13)
- All three hypotheses supported:
  - H1: AI capability -> organizational creativity (beta=0.573, t=15.213, p<0.001)
  - H2: AI capability -> organizational performance (beta=0.561, t=12.569, p<0.001)
  - H3: Organizational creativity -> organizational performance (beta=0.294, t=6.946, p<0.001)
- Effect sizes (f2) all above 0.15, indicating moderate to high effects (p.13)
- Intangible resources (weight=0.407, p<0.001) and human skills (weight=0.410, p<0.001) contribute slightly more to AI capability than tangible resources (weight=0.346, p<0.001) (Table 5, p.11)
- Within intangibles, inter-departmental coordination has the highest weight (0.504), followed by organizational change capacity (0.420), then risk proclivity (0.230) (Table 5, p.11)
- Non-significant formative indicator weights (D2, D4, T1, T5, BR2) were retained based on theoretical justification and expert panel recommendation (p.10)
- Confirmatory composite analysis: SRMR=0.037, dULS and dG below HI95, confirming the measurement structure is correct (Table 7, p.12)

## Relevance to Research

This paper is a methodological precedent for the agentic AI governance research in three ways:

1. **Formative construct development**: It demonstrates how to build and validate a formative higher-order construct for an AI-related organizational capability, following MacKenzie et al. (2011). The agentic AI governance maturity construct is similarly formative (governance practices are constitutive, not manifestive).

2. **Qualitative-before-quantitative sequence**: The expert panel and literature review precede the survey instrument, mirroring the proposed Phase 1 (qualitative construct development) then Phase 2 (quantitative testing) research design.

3. **IT governance theoretical lineage**: The intangible resources (inter-departmental coordination, organizational change capacity) overlap with governance practices. This paper provides an empirical benchmark for how organizational-level AI constructs relate to firm performance, establishing that the AI-capability-to-performance path exists and that non-technical resources matter most.

Prof. Prashar's feedback on formative constructs is directly relevant: Mikalef and Gupta (2021) is a reference case for how to handle formative measurement in AI research, including VIF thresholds, weight interpretation, and the decision to retain non-significant indicators.

## Limitations

- Single respondent per firm introduces potential informant bias, though Harman's one-factor test and non-response bias checks were conducted (pp.10, 15)
- US-based sample; organizations in other regions or at different AI maturity stages may have different resource requirements (p.15)
- Cross-sectional design cannot establish causality; time-lagged or longitudinal designs would strengthen causal claims (p.15)
- AI capability construct may not be exhaustive; additional dimensions may emerge as AI adoption matures (p.15)
- Perceptual measures of organizational performance rather than objective financial indicators (p.15)
- The construct captures AI capability generally, not specifically the governance of autonomous agents; adaptation is needed for the agentic context

## Key Quotes

- "An AI capability is the ability of a firm to select, orchestrate, and leverage its AI-specific resources." (p.4)
- "AI techniques alone will be unlikely to deliver any competitive gains by their own right, as they are easily acquired in the market and are subject to replication." (p.1)
- "One in three managers do not understand how AI technologies work." (p.5, citing Davenport and Ronanki, 2018)
- "Organizations that embrace risk proclivity deepen their commitments to AI, and in doing so establish their position, which makes it harder for others to catch up." (p.6, citing Ransbotham et al., 2018)
- "Functional silos are one of the most important barriers in deriving business value from AI investments as they constrain end-to-end solutions being developed." (p.6, citing McKinsey, 2018)
