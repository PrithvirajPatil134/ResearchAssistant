---
title: "The Dark Side of Robotic Process Automation"
type: source
maturity: working
created: 2026-05-07
originating_space: QNTR
applicable_to: [research_paper, term_paper, literature_review]
schema_version: "1.0"
sources:
  - path: "data/summaries/literature_review_7papers_analysis.md"
    type: md
authors:
  - "Eulerich, M."
  - "Waddoups, N."
  - "Wagener, M."
  - "Wood, D. A."
year: 2024
venue: "SSRN (Working Paper)"
tags: [rpa, shadow-ai, governance-tension, dark-bots, centralized-vs-decentralized, fortune-500]
---

## Summary

Through 26 interviews with RPA stakeholders at a Fortune 500 multinational, the paper identifies five key problems with RPA that stem from its very advantages (ease of use, low cost, minimal IT integration): RPA as a band-aid, control and security issues, misunderstood costs, governance challenges, and loss of process knowledge (p. 3). Provides the closest empirical evidence to the term paper's propositions on shadow AI and governance tensions.

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 5 §Core Argument]

## Key Arguments

### Five Problems of RPA

1. **RPA as band-aid** (pp. 7-8): Patches suboptimal processes rather than fixing root causes, slowing process improvement. "RPA is almost like a drug. It relieves the pain...but it does not address the underlying root cause" (p. 3, Chief Auditor quote).

2. **Control and security issues** (pp. 9-11): Uncontrolled/unknown bots ("dark spots"), failure to assess bot risk, bots as hacking targets due to privileged access, bots providing bad data when underlying processes change. "Currently, we have collected 185 [bots]...These are just the robots we know" (p. 10, P-2).

3. **Misunderstood costs** (pp. 11-12): Total cost of ownership understated; ongoing monitoring, assurance, and security costs ignored.

4. **Governance challenges** (p. 12): Tension between centralized control (assurance) and decentralized autonomy (motivation). "The biggest challenge...is getting compliance right for all of your bots, especially if you do this decentralized" (p. 12, P-14).

5. **Loss of process knowledge** (pp. 13-14): Domain knowledge erodes as bots take over; knowledge of bot functionality lost when creators leave.

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 5 §Key Findings]

### Shadow AI / Dark Bots

The "dark spots" of unknown, unregistered bots (p. 10) are a direct empirical manifestation of shadow AI/shadow IT. "It's easy to generate a robot, and therefore, it's not that easy to know where it was created" (p. 10, P-2). External auditors discovered unknown bots that the organization itself could not account for.

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 5 §Key Findings and §Direct Relevance]

### Governance Tension (Inverted U-Shape Evidence)

The tension between "heavy governance" killing motivation and "missing governance" creating risk (p. 12, P-6) provides qualitative evidence for an inverted U-shape: too much control stifles adoption; too little creates uncontrolled proliferation.

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 5 §Direct Relevance]

## Methodology

Qualitative interview study. 26 semi-structured interviews with RPA stakeholders at a Fortune 500 multinational conglomerate (~300,000 employees, >$60 billion revenue). Interviewees averaged 18.3 years of experience across six functions: top management, accounting, assurance, risk/internal control, cybersecurity, other. Conducted March-April 2021 via video conferencing, averaging 32 minutes. Coded using MAXQDA software. Validated with chief audit executives of 16 corporations and 22 IT auditors at an IIA chapter meeting (pp. 5-7).

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 5 §Methodology]

## Relevance to Research

- **RQ1 (governance practices and risk categories)**: Directly relevant. Five problems map onto risk categories. Centralized vs. decentralized governance (p. 12) is a concrete governance practice dimension.
- **P1 (governance maturity reduces incidents)**: Evidence that weak governance leads to incidents (unknown bots, security breaches, incorrect data). External auditor discovering unknown bots is a concrete incident example.
- **P2 (workflow control rigidity)**: Centralized vs. decentralized governance tension directly operationalizes control rigidity.
- **P3 (shadow AI)**: "Dark spots" of unknown bots (p. 10) are the strongest empirical manifestation of shadow AI in the literature review.
- **P4 (inverted U-shape)**: Governance tension between killing motivation vs. creating risk provides qualitative support.
- **Gap the term paper addresses**: RPA bots are rule-based, not agentic. The extrapolation from RPA governance challenges to agentic AI governance is precisely the gap.

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 5 §Direct Relevance]

## Limitations

- Does not address agentic AI specifically (focuses on rule-based RPA bots).
- Does not use quantitative methods or measure firm-level risk outcomes statistically.
- Does not engage with principal-agent theory explicitly.
- Does not test propositions about governance maturity or control rigidity.
- Single-firm study limits generalizability.
- Journal publication venue not explicitly stated in extracted text (SSRN working paper format).

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 5 §What It Does NOT Do and §Validity]

## Key Quotes

- "RPA is almost like a drug. It relieves the pain...but it does not address the underlying root cause." (p. 3, Chief Auditor)
- "Currently, we have collected 185 [bots]...These are just the robots we know." (p. 10, P-2)
- "It's easy to generate a robot, and therefore, it's not that easy to know where it was created." (p. 10, P-2)
- "The biggest challenge...is getting compliance right for all of your bots, especially if you do this decentralized." (p. 12, P-14)

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 5]
