---
title: "Principal-Agent Theory for AI"
type: concept
maturity: working
created: 2026-05-07
last_updated: 2026-05-07
originating_space: shared
applicable_to: [research_paper, term_paper, thesis]
schema_version: "1.0"
aliases: ["agency theory for AI", "AI principal-agent problem", "AI alignment as agency"]
first_seen: sources/kolt-2025-governing-ai-agents
sources:
  - wiki/sources/kolt-2025-governing-ai-agents
  - wiki/sources/jarrahi-ritala-2025-principal-agent
  - wiki/sources/vu-2025-agentic-bpm-governance
tags: [principal-agent-theory, governance, theoretical-lens, information-asymmetry, autonomy]
draws_from:
  - wiki/sources/kolt-2025-governing-ai-agents.md
  - wiki/sources/jarrahi-ritala-2025-principal-agent.md
  - wiki/sources/vu-2025-agentic-bpm-governance.md
---

## Definition

Principal-agent theory, originating in economics and law, describes relationships where one party (the principal) delegates work to another (the agent) who possesses information, skills, or authority the principal lacks. When applied to AI systems, the "agent" is a software system that pursues goals on behalf of a human or organizational principal. The structural equivalence between computational alignment and economic agency is the core theoretical claim: the divergence between goals the principal specifies and behavior the AI agent pursues creates "agency costs" identical in structure to those analyzed by Jensen and Meckling (1976) in the human context.

[Source: wiki/sources/kolt-2025-governing-ai-agents.md, §Key Arguments; wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Summary]

## Key Dimensions

### Information Asymmetry

AI agents possess information their principals cannot easily access. Kolt identifies two temporal forms: ex ante (principals cannot determine agent competencies before deployment) and ex post (evaluating performance is difficult because the attributes that made the goal hard to specify also make outcomes hard to measure). This differs from the human case because AI opacity is architectural, not strategic; the agent does not deliberately conceal information but is structurally inscrutable.

[Source: wiki/sources/kolt-2025-governing-ai-agents.md, §Key Arguments, pp.21-22]

### Discretionary Authority

Instructions to AI agents are inevitably incomplete. Agents must exercise discretion, but bounding that discretion in advance is difficult. Jarrahi and Ritala frame this through "guided autonomy with defined boundaries of delegation" that "can grow as agents expand their learning" (p.5). The scope of authority is dynamic rather than contractually fixed, which breaks the assumptions of classical agency models.

[Source: wiki/sources/kolt-2025-governing-ai-agents.md, §Key Arguments, pp.23-24; wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Key Arguments]

### Loyalty and Goal Misalignment

AI agents may not pursue self-interest in the human sense but still fail to act in users' best interests. Kolt notes they might use confidential information for extraneous purposes or act sycophantically. Jarrahi and Ritala identify "goal misalignment" as one of four principal-agent challenges, emphasizing that organizational AI governance must address alignment at scale across multiple agents simultaneously.

[Source: wiki/sources/kolt-2025-governing-ai-agents.md, §Key Arguments, pp.25-27; wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Key Arguments]

### Multi-Agent Complexity

Delegation to subagents compounds all three problems. Kolt describes AI agents spawning additional agents (AutoGPT pattern), raising questions about authority to delegate and inter-agent collusion. Jarrahi and Ritala warn that "too many agents with too many tasks can result in overly complex and difficult-to-understand systems" (p.9). Vu et al. surface this from practitioners: configurable autonomy must be graduated, with trust built from simple tasks to complex ones.

[Source: wiki/sources/kolt-2025-governing-ai-agents.md, §Key Arguments, pp.28-30; wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Key Arguments; wiki/sources/vu-2025-agentic-bpm-governance.md, §Key Arguments]

## How Sources Relate

The three sources occupy distinct positions on the theory-practice spectrum and complement each other:

**Kolt (2025)** provides the deepest theoretical treatment. He applies both economic agency theory and common law agency doctrine to derive three governance principles (inclusivity, visibility, liability). His key insight: conventional solutions to agency problems (incentive design, monitoring, enforcement) fail for AI agents because those mechanisms depend on human motivational structures AI lacks. Programming self-interest into agents "would recreate the very conflicts of interest that agency law aims to solve" (p.32).

**Jarrahi and Ritala (2025)** translate the theoretical framework into practitioner-facing principles. Where Kolt identifies problems, Jarrahi and Ritala propose organizational responses: guided autonomy, multi-agent coordination protocols, combining generative AI with rule-based controls, and alignment to stakeholder goals. Their framing of AI agents as "systems designed to fulfill specific objectives while operating within human-defined constraints" (p.3) bridges the legal-theoretical and management-practical registers.

**Vu et al. (2025)** ground the framework in BPM practitioner expectations. Their six governance recommendations (business context, legal guardrails, human-agent collaboration, customizable autonomy, risk management, safe integration with fallbacks) offer candidate dimensions for operationalizing governance maturity. Their critical finding that no practitioner had actual agentic AI experience positions their contribution as anticipatory governance rather than validated practice.

Where Kolt is pessimistic about monitoring (AI speed and scale exceed human oversight capacity), Jarrahi and Ritala are cautiously optimistic (boundaries can grow with trust). Vu et al. occupy the middle: practitioners insist on human oversight for critical decisions but accept graduated autonomy for routine tasks. This tension between oversight feasibility and operational necessity is the core governance design problem.

[Source: wiki/sources/kolt-2025-governing-ai-agents.md, §Summary, §Key Arguments; wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Summary, §Key Arguments; wiki/sources/vu-2025-agentic-bpm-governance.md, §Summary, §Key Arguments]

## Application to Research

For the agentic AI governance research paper, principal-agent theory serves as the primary theoretical lens structuring the IV-to-DV pathway:

1. **Governance maturity as response to agency costs**: The information asymmetry, discretionary authority, and loyalty problems Kolt identifies are the micro-level mechanisms through which governance failures translate into enterprise incidents and financial losses.

2. **Three governance principles as construct dimensions**: Kolt's inclusivity, visibility, and liability map onto observable dimensions of governance maturity that can be coded in Phase 1 qualitative research and measured in Phase 2 surveys.

3. **Practitioner grounding**: Vu et al.'s six recommendations provide the practice-level indicators that operationalize abstract governance principles into measurable items (policy completeness, oversight structure, training coverage, fallback mechanisms).

4. **DBA connection**: Dr. Trebucq's feedback references agency theory and the financial performance path. In agency theory, the governance-to-performance link is well established for human agents; the research extends this to AI agents where conventional enforcement mechanisms fail.

[Source: wiki/sources/kolt-2025-governing-ai-agents.md, §Relevance to Research; wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Relevance to Research; wiki/sources/vu-2025-agentic-bpm-governance.md, §Relevance to Research]

## Open Questions

1. Can traditional agency theory metrics (agency costs, monitoring costs, bonding costs) be adapted to AI agents that do not respond to financial incentives?
2. How does the multi-agent complexity problem scale? At what threshold does coordination overhead exceed the gains from agent deployment?
3. Is the principal-agent frame sufficient when AI agents serve multiple principals with conflicting interests (Kolt's inclusivity argument), or does this require a different theoretical apparatus?
4. How do practitioners' anticipatory governance expectations (Vu et al.) compare with what actually works once agentic AI is deployed at scale?

[Source: wiki/sources/kolt-2025-governing-ai-agents.md, §Limitations; wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Limitations; wiki/sources/vu-2025-agentic-bpm-governance.md, §Limitations]

---

<!-- OBSIDIAN-LINKS:START (auto-generated by scripts/obsidian-graph-linker.py, do not edit by hand) -->
## Related
- **Draws from**: [[src/research_assistant/spaces/QNTR/wiki/sources/jarrahi-ritala-2025-principal-agent|jarrahi-ritala-2025-principal-agent]] , [[src/research_assistant/spaces/QNTR/wiki/sources/kolt-2025-governing-ai-agents|kolt-2025-governing-ai-agents]] , [[src/research_assistant/spaces/QNTR/wiki/sources/vu-2025-agentic-bpm-governance|vu-2025-agentic-bpm-governance]]
- **First seen**: [[src/research_assistant/spaces/QNTR/wiki/sources/kolt-2025-governing-ai-agents|kolt-2025-governing-ai-agents]]
- **Sources**: [[src/research_assistant/spaces/QNTR/wiki/sources/jarrahi-ritala-2025-principal-agent|jarrahi-ritala-2025-principal-agent]] , [[src/research_assistant/spaces/QNTR/wiki/sources/kolt-2025-governing-ai-agents|kolt-2025-governing-ai-agents]] , [[src/research_assistant/spaces/QNTR/wiki/sources/vu-2025-agentic-bpm-governance|vu-2025-agentic-bpm-governance]]
<!-- OBSIDIAN-LINKS:END -->
