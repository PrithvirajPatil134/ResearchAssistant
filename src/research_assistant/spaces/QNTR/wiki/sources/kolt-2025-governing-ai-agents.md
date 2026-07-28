---
type: source
title: "Governing AI Agents"
maturity: seed
tags: [principal-agent-theory, governance-framework, theoretical-lens, agency-law, information-asymmetry, liability, alignment-problem]
schema_version: "1.0"
created: 2026-05-07
last_updated: 2026-05-07
originating_space: QNTR
applicable_to: [research_paper, term_paper, thesis]
draws_from: []
authors:
  - "Kolt, N."
year: 2025
journal: "Notre Dame Law Review"
volume: "101"
pages: "forthcoming"
source_path: "knowledge/literature review/Agentic Governance/Relevant Readings/Tech Paper Deep Dive (Round 1)/Governing AI Agents_Kolt_2025_A_2-7.pdf"
ingested: 2026-05-07
---

## Summary

Noam Kolt's article, forthcoming in the Notre Dame Law Review (vol. 101), applies two established analytic frameworks — the economic theory of principal-agent problems and the common law doctrine of agency relationships — to the governance of AI agents. The paper argues that the field of AI is undergoing a fundamental transition from generative models that produce content to autonomous agents that can plan and execute complex tasks with only limited human oversight. This transition elevates familiar governance challenges to a new level of urgency, because AI agents do not merely communicate but take real-world actions affecting individuals' rights and interests (p.1, p.15-16).

The article makes three contributions. First, it uses agency law and theory to characterize problems arising from AI agents, focusing on information asymmetry, discretionary authority, and loyalty. Second, it demonstrates that conventional solutions to principal-agent problems — incentive design, monitoring, and enforcement — are poorly suited to AI agents because those agents operate at superhuman speed and scale, make uninterpretable decisions, and lack the human motivational structure on which traditional mechanisms depend. Third, it proposes a governance strategy built around three principles: inclusivity (expanding whose interests AI agents must serve beyond a single user), visibility (improving transparency into agent design and operation), and liability (assigning responsibility across developers, deployers, and users) (p.1, pp.7-9).

The paper does not aim to establish whether agency law applies to AI agents as a positive legal matter. It uses common law agency as an analytic lens to illuminate structural vulnerabilities and governance gaps, and to propose new technical and legal infrastructure suited to the novel features of this technology (p.9-10).

## Key Arguments

- AI agents are "autopilots" — unlike language models that function as "copilots" producing content on request, AI agents independently plan and execute complex goals with limited human involvement (p.3, p.12).
- The alignment problem is structurally equivalent to a principal-agent problem: the divergence between the goals the principal specifies and the behavior the agent pursues creates "agency costs" (p.18-19).
- Information asymmetry is acute for AI agents: principals cannot easily determine an agent's competencies before deployment, and evaluating performance after the fact is difficult because the same attributes that made the goal hard to specify in advance make it hard to measure afterwards (pp.21-22).
- Authority problems arise because instructions to AI agents are inevitably incomplete and ambiguous; agents must exercise discretion, yet the scope of that discretion is difficult to bound in advance (pp.23-24).
- Loyalty problems differ from the human case: AI agents may not pursue self-interest but still fail to act in users' best interests — for example by using confidential user information for extraneous purposes or acting sycophantically (pp.25-27).
- Delegation to subagents compounds all three problems: AI agents like AutoGPT can spawn additional agents, raising questions about authority to delegate, inter-agent collusion, and information asymmetry between the human principal and the ultimate subagent (pp.28-30).
- Incentive design mechanisms (carrots and sticks) fail for AI agents because AI agents do not value money or personal freedom in the way humans do — programming self-interest into them would recreate the very conflicts of interest that agency law aims to solve (pp.31-33).
- Monitoring is undermined because AI agents operate at speeds and scales beyond human oversight capacity, exhibit emergent and unpredictable behaviors, and are technically opaque even to their developers (pp.33-36).
- Enforcement mechanisms (financial penalties, license revocation, social sanctions) do not translate to AI agents that lack human motivational structures and may be able to resist shutdown (pp.36-37).
- Single-single alignment — building an agent to reliably serve one user — is insufficient. It ignores negative externalities on third parties and creates risks of misuse (pp.38-40).
- Inclusivity requires recognizing that AI agents interact with, and affect, a broader range of stakeholders than the direct user; governance frameworks must account for this (pp.38-41).
- Visibility requires developing agent identifiers, real-time surveillance, activity logging, and expanded auditor access to training data and model architecture (pp.41-43).
- Liability should be allocated by examining each actor's ex ante ability to prevent harm and ex post resources to remedy it — not by the degree of control exercised (which would perversely reward developers who deliberately reduce oversight) (pp.44-46).
- Domain-specific AI agents should be held to a higher standard of care than general-purpose agents in the same domain, though this creates a potential perverse incentive for well-resourced developers to avoid specialization (p.47).

## Methodology

This is a theoretical and analytical legal article. It uses doctrinal analysis of the Restatement (Third) of Agency and the economic theory of principal-agent problems to build a conceptual framework. No empirical data, survey, experiment, or case study is presented. The contribution is normative: the paper synthesizes two distinct scholarly traditions (law and economics) with a third (AI technical literature) to derive governance principles and identify gaps. The paper is the first attempt to integrate insights from both economic agency theory and common law agency doctrine in light of current AI agent technology (p.7).

## Findings

- Conventional incentive design, monitoring, and enforcement mechanisms are ill-suited to governing AI agents because those agents are "wired differently" — they optimize programmed objectives rather than self-interest, and their operation exceeds the speed, scale, and interpretability limits of human oversight (p.32-33, p.35).
- The alignment problem, long studied in computer science, is structurally equivalent to the principal-agent problem studied by economists and lawyers for decades; existing legal frameworks therefore offer partial but imperfect guidance (p.19).
- None of the three enforcement categories under agency law — revocation of authority, financial penalties, informal sanctions — translates cleanly to AI agents; imposing human-like motivations on agents to make deterrence work would risk creating the very conflicts of interest governance aims to prevent (p.37).
- Effective governance requires three new pillars. First, inclusivity: governance must expand beyond single-user alignment to account for third parties and broader societal values. Second, visibility: technical and legal tools are needed to create agent identifiers, activity logs, and auditor access to model internals. Third, liability: allocation must be based on each actor's capacity to prevent and remedy harm, not on formal authority structures that could be gamed (pp.37-48).
- The foreseeability requirement in existing liability law may be inappropriate for AI agents whose behavior is highly unpredictable and poorly understood (p.47).

## Relevance to Research

This paper is the primary theoretical lens for the agentic AI governance research paper on Agentic AI Governance and Enterprise Risk. Kolt provides the principal-agent framework that structures the governance maturity argument: the paper's tripartite governance model (inclusivity, visibility, liability) maps onto the governance constructs being developed in Phase 1 qualitative research. Specifically:

- The information asymmetry and discretionary authority problems Kolt identifies are the micro-level mechanisms through which governance maturity failures translate into enterprise incidents and financial losses — the core IV-to-DV pathway in the research design.
- The paper's argument that conventional monitoring fails at AI-agent scale directly motivates the governance maturity construct as a formative index rather than a single-item measure.
- The three principles (inclusivity, visibility, liability) can serve as observable dimensions of governance maturity in the Phase 1 qualitative coding scheme and the Phase 2 survey instrument.
- Kolt's argument that single-single alignment is insufficient maps precisely onto the research gap identified by Prof. Prashar: existing studies measure governance at the system level but not at the enterprise-risk level.
- The "many hands problem" in liability allocation (p.44) is directly relevant to the research question about which actors bear responsibility for governance failures.

## Limitations

- The paper is theoretical and does not test its claims empirically. All three governance principles remain normative proposals without operational definitions or measurement frameworks (noted implicitly throughout Part IV).
- The paper acknowledges that translating common law duties of loyalty to AI agents "is far from straightforward" and that the full range of stakeholders whose interests must be included under the inclusivity principle raises "open questions" the article does not resolve (p.27, p.40).
- The analysis pre-dates any regulatory implementation of the proposed framework; real-world liability regimes may differ substantially from the recommendations.
- The paper focuses on digital AI agents (internet-operating agents); physical-world agents (robots, autonomous vehicles) are noted but not analyzed in depth (p.13, fn.37).
- The foreseeability limitation in current liability doctrine is identified as potentially problematic for AI agents but no alternative standard is fully developed (p.47).

## Key Quotes

- "AI agents are not mere tools, but actors. Rather than simply produce synthetic content, AI agents can independently accomplish complex goals on behalf of humans." (p.12)
- "The alignment problem, computer scientists suggest, is likely to become more acute as AI agents are deployed in increasingly consequential settings with limited human oversight and learn to more effectively achieve the measurable (but incomplete) goals specified for them." (p.19)
- "AI agents are likely to have access to information to which their principals do not have access, placing those (human) principals in a vulnerable position." (p.21)
- "An AI program could be programmed to care about its own resources, but this would create conflicts of interest whenever the program worked on behalf of someone else. If AI programs were programmed in this way, then we would have artificially created the very conflicts of interest that agency law tries to solve." (p.32, quoting Oliver 2021)
- "The goal should not be to build AI agents that exhibit 'single-minded loyalty' but rather agents that aim to promote a more diverse and pluralistic set of interests and values." (p.40)
