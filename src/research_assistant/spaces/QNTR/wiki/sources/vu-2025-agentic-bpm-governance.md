---
type: source
title: "Agentic Business Process Management: Practitioner Perspectives on Agent Governance in Business Processes"
maturity: seed
tags: [bpm, governance-recommendations, qualitative, practitioner-interviews]
schema_version: "1.0"
created: 2026-05-07
last_updated: 2026-05-07
originating_space: QNTR
applicable_to: [research_paper, term_paper]
draws_from: []
authors:
  - "Vu, H."
  - "Klievtsova, N."
  - "Leopold, H."
  - "Rinderle-Ma, S."
  - "Kampik, T."
year: 2025
journal: "LNBIP"
volume: "565"
pages: "29-43"
source_path: "knowledge/literature review/Agentic Governance/Relevant Readings/Mgmt-Side Papers (Round 2)/Vu_et_al_2025_FULL_TEXT.md"
ingested: 2026-05-07
---

## Summary

This paper introduces the concept of Agentic Business Process Management (ABPM) and investigates how organizations can govern AI agents deployed within business processes. Based on 22 semi-structured interviews with BPM practitioners across diverse industries, the study identifies anticipated benefits, risks, and governance challenges associated with agentic AI. The authors propose six recommendations for responsible agent adoption and four actions to align traditional BPM with agentic AI (§Abstract, §1).

The study is grounded in the evolution from early 1990s multi-agent systems in BPM, through Robotic Process Automation (RPA) in the late 2010s, to current Large Language Model-based agents. The authors formally define ABPM as describing "(i) the deployment and execution of autonomous software agents to achieve business process goals and (ii) the application of agent-based abstractions for the process-oriented design and analysis of autonomous software agents" (§2.4).

A critical finding: none of the 22 participants reported having actual practical experience with agentic AI. Their assessments are based on expectations, often against the backdrop of existing RPA technologies (§4, Understanding section).

## Key Arguments

- ABPM represents a new paradigm that combines the autonomy and adaptability of LLM-based agents with BPM's focus on structured, controlled process execution (§2.4)
- Practitioners anticipate five key benefits: enhanced efficiency, improved data quality, better compliance, scalability, and democratization of process data (§4, Benefits)
- Six identified risks: bias from flawed training data, over-reliance diminishing human judgment, lack of transparency, cybersecurity threats, job displacement, and unauthorized decision-making (§4, Risks)
- Human oversight is considered essential for critical decisions; configurable autonomy is recommended with graduated trust-building from simple to complex tasks (§4, Autonomy and Adaptability)
- Responsibility for AI agent failures should be shared across organizations, developers, and business leaders, with organizations deploying agents bearing ultimate responsibility (§4, Human Involvement)
- The six governance recommendations cover: business context definition, legal/ethical guardrails, human-agent collaboration design, customization of autonomy levels, risk management, and safe integration with fallback mechanisms (§5)
- Four BPM alignment actions address: balancing human-agent roles, redefining human involvement (peers vs. supervisors), evolving beyond static process models, and developing agent-specific performance metrics (§5)

## Methodology

Qualitative research design using semi-structured interviews with 22 BPM practitioners. Interviews lasted 60-90 minutes, some conducted in pairs or groups. Analysis followed a qualitative content analysis approach (Mayring and Fenzl, 2019) with deductive-inductive coding: open coding (labeling segments), axial coding (grouping into categories), and selective coding (integrating into coherent framework) (§3).

Participants had experience with automation and AI technologies from various industries and roles. The study uses an interpretivist epistemology suitable for exploring nascent phenomena where practical experience is limited (§3).

## Findings

- 10 of 22 participants were familiar with the term "agentic AI," describing it as self-learning technology that operates autonomously (§4, Understanding)
- Key use cases identified: process monitoring, predictive analytics, task automation (data entry, document processing), master data maintenance, customer service, supply chain optimization, fraud detection (§4, Use Cases)
- Practitioners stressed requirements for: clear ethical guidelines, audit logs, adherence to corporate policies, defined roles and limitations, compliance with data protection, seamless integration, comprehensive training, and cost management (§4, Requirements)
- On autonomy: "It shouldn't make changes in source systems or install new apps autonomously. That crosses the line because those areas are managed by different teams and require coordination." (§4, Autonomy)
- On responsibility: "For complex decisions, the [agentic] AI should provide full context; how it arrived at the decision, what data it used, and the potential consequences; just like how humans consult colleagues for advice." (§4, Human Involvement)

## Relevance to Research

This paper provides practitioner-grounded governance recommendations that complement the theoretical lens of Kolt (2025). While Kolt derives governance principles from agency law and economics, Vu et al. surface what organizations actually worry about from a process management perspective. The six recommendations and four BPM alignment actions offer candidate dimensions for operationalizing "AI governance maturity" as a formative construct.

The critical limitation (no participant had actual agentic AI experience) is directly relevant: it positions the paper as capturing anticipatory governance needs rather than validated practices, supporting the argument that governance constructs for agentic AI are still being developed and require qualitative exploration before quantitative measurement.

## Limitations

- Sample is relatively small and predominantly drawn from selected multinational organizations (§6)
- Concept of agentic AI is still formative; participants used varied terminology and definitions (§6)
- No participant had actual practical experience with agentic AI; assessments are expectation-based, often benchmarked against RPA (§4, Understanding; §6)
- Limited to BPM practitioners; does not capture perspectives of IT governance boards, compliance officers, or end users
- Published as a conference paper (LNBIP), not a journal article, though the venue (BPM conference) is top-tier in its field

## Key Quotes

- "More employees could initiate changes or optimizations if the software supports them directly, reducing dependency on specialized roles." (§4, Benefits)
- "[The agent] would basically replace an FTE, let's just put it that way; you also have to provide it with the same framework that the employee would be confronted with because what would the employee do if they encounter difficulties?" (§4, Requirements)
- "It's a cultural thing to be able to accept autonomy and decision making being taken away from a human." (§4, Risks)
- "If it's routine, the decision itself should be documented. The more complex the task, the more I want to see how the process was developed." (§4, Autonomy)
- "Processes often get stuck due to errors in master data, such as mismatched product codes or pricing issues. [Agentic] AI could analyze and fix these autonomously." (§4, Use Cases)
