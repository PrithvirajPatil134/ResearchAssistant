---
title: "Responsible AI Pattern Catalogue: A Collection of Best Practices for AI Governance and Engineering"
type: source
maturity: seed
created: 2026-05-07
last_updated: 2026-05-07
originating_space: QNTR
applicable_to: [research_paper, term_paper]
schema_version: "1.0"
sources:
  - path: "knowledge/literature review/Agentic Governance/Relevant Readings/Literature Review Papers/Responsible AI Pattern Catalogue- A Collection of Best Practices for AI Governance and Engineering_ Lu-Zhu-Xu-Whittle_2024_A*_28.pdf"
    type: pdf
authors:
  - "Lu, Q."
  - "Zhu, L."
  - "Xu, X."
  - "Whittle, J."
  - "Zowghi, D."
  - "Jacquet, A."
year: 2024
journal: "ACM Computing Surveys"
volume: "56(7)"
pages: "Article 173, 1-35"
ingested: 2026-05-07
tags: [responsible-ai, design-patterns, multivocal-review, principle-gap]
draws_from: []
---

## Summary

This paper presents a Responsible AI (RAI) Pattern Catalogue developed through a systematic multivocal literature review (MLR) covering both academic and grey literature. The catalogue identifies 35 patterns organized into three groups: multi-level governance patterns, trustworthy process patterns, and RAI-by-design product patterns. The central argument is that existing AI ethics principles frameworks leave practitioners "with nothing much beyond truisms" (p. 1) and that a pattern-oriented approach can bridge the "principle-algorithmic gap" between high-level principles and algorithm-level solutions (p. 2).

## Key Arguments

1. **The principle-algorithmic gap**: Significant efforts in RAI have been placed at algorithm level, focusing on mathematics-amenable principles like fairness and privacy. However, ethical issues "can arise at any step of the development lifecycle, cutting across many AI and non-AI components of systems beyond AI algorithms and models" (p. 1). The gap between high-level principles and actionable implementation guidance remains largely unaddressed.

2. **System-level perspective**: Rather than staying at the principle or algorithm level, the catalogue focuses on patterns that "practitioners can utilize in practice to ensure that the developed AI systems are responsible throughout the entire software development lifecycle" (p. 3).

3. **Multi-level governance**: RAI governance requires structures at three levels: industry level (regulations, standards, certification), organization level (ethics committees, codes of ethics, risk assessment), and team level (customized agile processes, diverse teams) (pp. 6-13). This multi-level structure mirrors the governance hierarchy relevant to agentic AI governance research.

4. **Stakeholder complexity**: The paper identifies a detailed stakeholder taxonomy across three levels: industry-level stakeholders (AI technology producers/procurers, AI solution producers/procurers, AI users, AI-impacted subjects, AI consumers, RAI governors, RAI tool producers/procurers), organization-level stakeholders (management teams, employees), and team-level stakeholders (development teams) (pp. 6-7).

## Methodology

Multivocal Literature Review (MLR) combining:
- Academic literature via SLR guidelines from Kitchenham and Charters (p. 3)
- Grey literature via guidelines from Garousi et al. (p. 3)
- Search engines: ACM Digital Library, IEEE Xplore, Science Direct, Springer Link, Google Scholar (p. 4)
- Search period: up to July 31, 2022 (p. 4)
- Final corpus: 205 academic items and 69 grey items (p. 5)
- Australia's AI ethics principles used to derive supplementary search terms for "Responsible" (p. 4)
- Snowballing technique applied to both academic and grey literature (p. 5)
- Patterns documented following traditional pattern structure: context, problem, solution, benefits, drawbacks, related patterns, known uses (p. 5)

## Findings

The 35 patterns are classified into three groups:

**Governance Patterns (Industry, Organization, Team levels):**
- Industry: RAI Regulation, Regulatory Sandbox, Building Code, RAI Standard, RAI Maturity Model, RAI Certification, Trust Mark, Independent Oversight (pp. 7-10)
- Organization: Leadership Commitment, Ethics Committee, Code of Ethics, Ethical Risk Assessment, Standardized Reporting, Role-Level Accountability Contract, RAI Software Bill of Materials, Ethics Training (pp. 10-12)
- Team: Customized Agile Process, Tight Coupling of AI and Non-AI Development (p. 13)

**Process Patterns** (across development lifecycle stages):
- Patterns for design, implementation, testing, deployment, and operation stages (pp. 13-22)

**Product Patterns** (RAI-by-design):
- Patterns embedded into the architecture and design of AI systems themselves (pp. 22-28)
- Including: Ethical Knowledge Base, Ethical Digital Twin, AI Mode Switcher, Multi-Model Decision Maker (pp. 26-27)

## Relevance to Research

Directly relevant to the agentic AI governance research in several ways:

1. **Governance maturity framing**: The multi-level governance structure (industry, organization, team) provides a framework for operationalizing "AI governance maturity" as an independent variable. The patterns at each level could serve as indicators for a formative governance maturity construct.

2. **RAI Maturity Model pattern** (p. 9): Explicitly discusses organizational readiness assessment across dimensions, aligning with the governance maturity IV in the term paper's conceptual framework.

3. **Principle-algorithmic gap concept**: Maps directly to the argument that agentic AI governance is under-operationalized. The gap between what organizations aspire to (principles) and what they actually implement (algorithms and patterns) is the core tension.

4. **Pattern validation gap**: The patterns are identified from literature but "remain unvalidated in real organizations" (this is acknowledged in the limitations). This supports the argument that governance practices need empirical validation, which is the purpose of the proposed quantitative study.

5. **Stakeholder taxonomy**: Provides a detailed mapping of who is affected by AI governance decisions, relevant to operationalizing the "enterprise risk" dependent variable.

## Limitations

- Patterns are identified from literature, not empirically validated in organizational settings (acknowledged by authors)
- Grey literature quality varies; inclusion criteria may miss some industry practices
- Search period ends July 2022; rapid developments in AI governance since then (EU AI Act final text, executive orders) are not captured
- Focus on software engineering perspective may underweight organizational and strategic dimensions of governance
- No quantitative assessment of pattern adoption rates or effectiveness

## Key Quotes

- "Without further best practice guidance, practitioners are left with nothing much beyond truisms." (p. 1)
- "Issues (including ethical issues) can occur at any step of the development lifecycle, crosscutting many AI, non-AI, and data components of systems beyond AI algorithms and models." (p. 2)
- "To try to fill the principle-algorithmic gap, further guidance such as guidebooks, questions to generate discussions, checklists, and documentation templates have started to appear. Those efforts tend to be ad-hoc sets of more detailed prompts for practitioners to think about all the issues and come up with their own solutions." (p. 2)
- "Governance for RAI systems can be defined as the structures and processes that are employed to ensure that the development and use of AI systems meet AI ethics principles." (p. 5)
- "48% of organizations have already adopted or plan to adopt AI technologies within the next 12 months, whereas 21% of organizations have already deployed or plan to deploy RAI technologies within the next 12 months." (p. 2, citing 2022 Gartner CIO Survey)
