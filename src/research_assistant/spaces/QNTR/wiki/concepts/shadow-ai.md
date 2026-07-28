---
title: "Shadow AI"
type: concept
maturity: working
created: 2026-05-07
last_updated: 2026-05-07
originating_space: QNTR
applicable_to: [research_paper, term_paper]
schema_version: "1.0"
aliases: ["shadow IT", "dark bots", "unregistered automation", "unauthorized AI"]
first_seen: sources/eulerich-2024-dark-side-rpa
sources:
  - wiki/sources/eulerich-2024-dark-side-rpa
  - wiki/sources/jarrahi-ritala-2025-principal-agent
tags: [shadow-ai, moderator-variable, governance-risk, dark-bots, uncontrolled-proliferation]
draws_from:
  - wiki/sources/eulerich-2024-dark-side-rpa.md
  - wiki/sources/jarrahi-ritala-2025-principal-agent.md
---

## Definition

Shadow AI refers to AI systems, agents, or automated processes operating within an organization without the knowledge, registration, or governance oversight of central IT or risk management functions. It extends the established concept of shadow IT (unsanctioned hardware or software) to autonomous systems that can take actions, access data, and interact with other systems without human awareness.

The term captures a specific risk category: organizations cannot govern what they cannot see. When AI agents proliferate outside governance perimeters, the principal-agent problem is compounded because the principal does not even know agents exist.

This is the P3 moderator variable in the agentic AI governance research paper's conceptual framework.

## Key Dimensions

### Empirical Evidence: "Dark Spots" (Eulerich et al. 2024)

Eulerich et al. provide the strongest empirical evidence of shadow AI in the literature review. At a Fortune 500 multinational (~300,000 employees), their interviews revealed:

- "Currently, we have collected 185 [bots]... These are just the robots we know" (p.10, P-2). External auditors discovered bots the organization itself could not account for.
- "It's easy to generate a robot, and therefore, it's not that easy to know where it was created" (p.10, P-2). The ease of creation (a feature) directly enables uncontrolled proliferation (a risk).
- Unknown bots constitute "dark spots" that undermine governance because they operate with privileged system access, bypass compliance requirements, and provide potentially incorrect data when underlying processes change.

Though this evidence comes from rule-based RPA (not agentic AI), the extrapolation is direct: if simple rule-based bots escape governance perimeters, autonomous goal-directed agents with broader capabilities will do so more readily.

[Source: wiki/sources/eulerich-2024-dark-side-rpa.md, §Key Arguments, §Shadow AI / Dark Bots]

### Multi-Agent Complexity (Jarrahi and Ritala 2025)

Jarrahi and Ritala identify multi-agent complexity as one of four principal-agent challenges. Their warning: "too many agents with too many tasks can result in overly complex and difficult-to-understand systems" (p.9). This is the mechanism by which shadow AI grows: as organizations deploy more agents, some inevitably escape centralized oversight. The Moderna example (3,000 tailored GPTs deployed) illustrates the scale at which tracking becomes infeasible without dedicated governance infrastructure.

[Source: wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Key Arguments]

### Connection to Shadow IT Literature

Shadow AI is a specific instantiation of the broader shadow IT phenomenon. The established literature on shadow IT documents:
- Employees adopting unauthorized cloud services to circumvent slow IT procurement
- Departmental databases that bypass enterprise data governance
- Unsanctioned communication tools that evade compliance monitoring

Shadow AI differs from shadow IT in three ways: (1) agents can act autonomously, compounding the consequences of invisibility; (2) agents can spawn sub-agents, multiplying themselves without human intervention; (3) agents may access sensitive data or take consequential actions, not merely store information.

[CONJECTURE: the shadow IT connection follows logically from the Eulerich et al. evidence and established IS literature, but no single source page makes this three-point comparison explicitly]

## How Sources Relate

Eulerich et al. and Jarrahi-Ritala approach shadow AI from opposite directions:

**Eulerich et al.** work inductively from empirical observation. They did not set out to study shadow AI; they discovered it while investigating RPA's dark side. The "dark spots" finding emerged from informant disclosure, not theoretical prediction. This grounds the concept in organizational reality rather than academic speculation.

**Jarrahi and Ritala** approach deductively from principal-agent theory. Multi-agent complexity is a predicted consequence of agency relationships at scale: as the number of agents grows, the principal's capacity to monitor them degrades. Shadow AI is what happens when monitoring capacity is overwhelmed.

The two sources converge on the same conclusion through different routes: uncontrolled proliferation is not an edge case but a structural tendency of low-cost, easy-to-deploy automation. Governance regimes that do not account for invisible agents will systematically underestimate organizational risk.

[Source: wiki/sources/eulerich-2024-dark-side-rpa.md, §Relevance to Research; wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Relevance to Research]

## Application to Research

### Role in Conceptual Framework

Shadow AI serves as a moderator (P3) of the governance maturity to enterprise risk relationship. The proposed logic: organizations with high governance maturity but high shadow AI prevalence experience more incidents than their governance level would predict, because governance mechanisms only protect against visible agents. Shadow AI prevalence weakens the governance-to-risk-reduction pathway.

### Operationalization Challenges

Measuring shadow AI presents a paradox: if the organization does not know the agents exist, it cannot report their prevalence on a survey. Possible measurement approaches:

1. **Indirect indicators**: Difference between registered/known AI deployments and total deployments discovered through audit (the Eulerich finding)
2. **Proxy measures**: Ease of self-service AI deployment, decentralization of AI budgets, absence of centralized registries
3. **Qualitative assessment**: Executive perception of whether "all AI is accounted for"

### Gap Being Addressed

The literature identifies shadow AI as a risk but does not test its moderating effect on governance outcomes. Eulerich et al. document its existence; Jarrahi and Ritala predict its growth; neither measures its impact on the governance-performance relationship. This is the gap the P3 proposition addresses.

[Source: wiki/sources/eulerich-2024-dark-side-rpa.md, §Relevance to Research; wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Relevance to Research]

## Open Questions

1. At what scale does shadow AI become a governance-level concern vs. an operational nuisance? Is there a threshold effect?
2. Can shadow AI be "beneficial" in some contexts (enabling experimentation, reducing bureaucratic friction) before becoming harmful? If so, this complicates the pure-moderator specification.
3. How does the agentic capability of AI systems change the shadow AI dynamic compared to shadow IT? Is the risk qualitatively different or merely quantitatively larger?
4. Is shadow AI prevalence itself a governance failure (endogenous to the IV) or an independent environmental condition (exogenous moderator)?

[Source: wiki/sources/eulerich-2024-dark-side-rpa.md, §Limitations; wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Limitations]

---

<!-- OBSIDIAN-LINKS:START (auto-generated by scripts/obsidian-graph-linker.py, do not edit by hand) -->
## Related
- **Draws from**: [[src/research_assistant/spaces/QNTR/wiki/sources/eulerich-2024-dark-side-rpa|eulerich-2024-dark-side-rpa]] , [[src/research_assistant/spaces/QNTR/wiki/sources/jarrahi-ritala-2025-principal-agent|jarrahi-ritala-2025-principal-agent]]
- **First seen**: [[src/research_assistant/spaces/QNTR/wiki/sources/eulerich-2024-dark-side-rpa|eulerich-2024-dark-side-rpa]]
- **Sources**: [[src/research_assistant/spaces/QNTR/wiki/sources/eulerich-2024-dark-side-rpa|eulerich-2024-dark-side-rpa]] , [[src/research_assistant/spaces/QNTR/wiki/sources/jarrahi-ritala-2025-principal-agent|jarrahi-ritala-2025-principal-agent]]
<!-- OBSIDIAN-LINKS:END -->
