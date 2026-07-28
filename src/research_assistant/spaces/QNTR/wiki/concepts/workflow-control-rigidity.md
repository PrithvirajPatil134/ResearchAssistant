---
title: "Workflow Control Rigidity"
type: concept
maturity: working
created: 2026-05-07
last_updated: 2026-05-07
originating_space: QNTR
applicable_to: [research_paper, term_paper]
schema_version: "1.0"
aliases: ["control rigidity", "autonomy-control balance", "degree of automation"]
first_seen: sources/jarrahi-ritala-2025-principal-agent
sources:
  - wiki/sources/jarrahi-ritala-2025-principal-agent
  - wiki/sources/vu-2025-agentic-bpm-governance
  - wiki/sources/haase-2024-interdisciplinary-directions
  - wiki/sources/eulerich-2024-dark-side-rpa
tags: [mediator-variable, autonomy-control, inverted-u-shape, guided-autonomy, workflow-control]
draws_from:
  - wiki/sources/jarrahi-ritala-2025-principal-agent.md
  - wiki/sources/vu-2025-agentic-bpm-governance.md
  - wiki/sources/haase-2024-interdisciplinary-directions.md
  - wiki/sources/eulerich-2024-dark-side-rpa.md
---

## Definition

Workflow control rigidity captures the degree to which an organization constrains the autonomous behavior of its AI agents through rules, boundaries, approvals, and oversight mechanisms. At one extreme, full rigidity means every agent action requires human approval. At the other extreme, full flexibility means agents operate without constraints. The construct occupies a continuum; the research question is whether an optimal point exists between over-control (which stifles value) and under-control (which creates risk).

This is the P2 mediator variable in the agentic AI governance research paper. The proposed mechanism: governance maturity determines the level of control rigidity, which in turn determines enterprise risk outcomes. More mature governance enables calibrated control, while immature governance leads to either excessive rigidity (value destruction) or insufficient rigidity (unmanaged risk).

## Key Dimensions

### Guided Autonomy (Jarrahi and Ritala 2025)

Jarrahi and Ritala operationalize control through "guided autonomy with defined boundaries of delegation" that "can grow as agents expand their learning" (p.5). The key insight is that boundaries are not static: they expand as trust builds. This introduces a temporal dimension to control rigidity; it is not a fixed organizational choice but an evolving calibration.

Their explicit statement that full autonomy is "not always feasible or desirable" (p.5) supports the mediator logic: governance maturity determines whether organizations can effectively calibrate these expanding boundaries.

[Source: wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Key Arguments]

### Configurable Autonomy (Vu et al. 2025)

BPM practitioners in Vu et al.'s study emphasize graduated trust-building: "customization of autonomy levels" is one of six governance recommendations. The principle is operational: start with simple tasks, expand to complex ones as the agent demonstrates reliability. One participant stated: "It shouldn't make changes in source systems or install new apps autonomously. That crosses the line because those areas are managed by different teams and require coordination" (§4, Autonomy).

This provides the practice-level manifestation of control rigidity: specific rules about what agents may and may not do, differentiated by task complexity and consequence severity.

[Source: wiki/sources/vu-2025-agentic-bpm-governance.md, §Key Arguments, §Findings]

### Degree-of-Automation Tradeoff (Haase et al. 2024)

Haase et al. contribute the most explicit empirical statement of the control-performance tradeoff from human-automation interaction (HAI) research: "Higher degrees of automation yield better performance under normal conditions but worse performance during failures due to increased complacency and skill degradation" (p.585).

This finding supports an inverted U-shape (P4): there exists an optimal automation level. Below it, humans do work that agents could handle more efficiently. Above it, humans lose the skills and attention needed to intervene during failures. The tradeoff is not abstract; HAI research demonstrates it empirically across domains.

The paper also identifies three specific mechanisms by which over-automation degrades performance:
1. **Automation bias**: Using automation output as a heuristic replacement for judgment
2. **Complacency**: Insufficient monitoring of automated processes
3. **Skill degradation**: Loss of the ability to execute processes manually when agents fail

[Source: wiki/sources/haase-2024-interdisciplinary-directions.md, §Key Arguments]

### Centralized vs. Decentralized Tension (Eulerich et al. 2024)

Eulerich et al. document the governance tension between centralized control (which provides assurance) and decentralized autonomy (which motivates adoption): "The biggest challenge... is getting compliance right for all of your bots, especially if you do this decentralized" (p.12, P-14).

One participant (P-6) explicitly frames this as a tension between "heavy governance" killing motivation and "missing governance" creating risk. This is qualitative evidence for the inverted U-shape and directly operationalizes the control rigidity construct at the organizational design level.

[Source: wiki/sources/eulerich-2024-dark-side-rpa.md, §Key Arguments, §Governance Tension]

## How Sources Relate

The four sources build the control rigidity construct from progressively concrete angles:

| Source | Contribution | Level of Analysis |
|--------|-------------|-------------------|
| Jarrahi and Ritala | Guided autonomy with expanding boundaries | Theoretical principle |
| Vu et al. | Configurable autonomy, graduated trust | Practitioner recommendation |
| Haase et al. | Degree-of-automation tradeoff, empirical from HAI | Empirical generalization |
| Eulerich et al. | Centralized vs. decentralized governance tension | Organizational observation |

They converge on a shared insight: control is not binary (on/off) but continuous, and the optimal point depends on context. Where they diverge is on whether the optimal point is knowable in advance:

- Jarrahi and Ritala are optimistic: boundaries "can grow" systematically with learning.
- Haase et al. are cautious: the optimal point involves irreducible tradeoffs ("always accompanied by positive and negative aspects").
- Eulerich et al. are pragmatic: organizations struggle to find the balance in practice.
- Vu et al. recommend a process: start constrained, expand deliberately.

This divergence is not a contradiction; it reflects different levels of abstraction (theory vs. psychology vs. organizational reality) addressing the same underlying phenomenon.

[Source: all four source pages, §Relevance to Research sections]

## Application to Research

### Mediator Specification (P2)

The proposed path: Governance Maturity -> Workflow Control Rigidity -> Enterprise Risk.

The mechanism: organizations with mature governance possess the knowledge, structures, and processes to calibrate control appropriately. They set boundaries that are neither so tight as to prevent agent value creation nor so loose as to allow unmanaged risk. Immature governance leads to miscalibrated control, which then leads to incidents (either through over-automation failures or through under-governance proliferation).

### Inverted U-Shape (P4)

The relationship between control rigidity and performance is proposed as curvilinear (inverted U-shape):
- Too much rigidity: stifles adoption, destroys value, creates workarounds (shadow AI as escape valve)
- Too little rigidity: uncontrolled proliferation, dark spots, incident accumulation
- Optimal rigidity: calibrated boundaries, graduated trust, effective monitoring

Haase et al.'s HAI evidence supports this proposition. Eulerich et al.'s qualitative observation ("heavy governance kills motivation, missing governance creates risk") provides real-world anchoring.

### Measurement Approach

Control rigidity could be measured through:
1. Number of approval gates per agent deployment
2. Scope of autonomous authority (what decisions agents can make without human sign-off)
3. Frequency and intrusiveness of monitoring
4. Time-to-expand (how quickly boundaries loosen as agents prove reliable)
5. Ratio of centralized to decentralized governance

## Open Questions

1. Is control rigidity a single dimension (rigid-flexible continuum) or multi-dimensional (different rigidity levels for different decision types)?
2. Does the inverted U-shape hold across industries and organizational sizes, or is the optimal point contextual?
3. How does control rigidity interact with shadow AI? If rigidity is too high, does shadow AI increase as users route around governance (creating an endogeneity problem)?
4. Can control rigidity be disentangled from governance maturity empirically, or is it so closely correlated with the IV that mediation is not identifiable?

[Source: wiki/sources/jarrahi-ritala-2025-principal-agent.md, §Limitations; wiki/sources/haase-2024-interdisciplinary-directions.md, §Limitations; wiki/sources/eulerich-2024-dark-side-rpa.md, §Limitations]

---

<!-- OBSIDIAN-LINKS:START (auto-generated by scripts/obsidian-graph-linker.py, do not edit by hand) -->
## Related
- **Draws from**: [[src/research_assistant/spaces/QNTR/wiki/sources/eulerich-2024-dark-side-rpa|eulerich-2024-dark-side-rpa]] , [[src/research_assistant/spaces/QNTR/wiki/sources/haase-2024-interdisciplinary-directions|haase-2024-interdisciplinary-directions]] , [[src/research_assistant/spaces/QNTR/wiki/sources/jarrahi-ritala-2025-principal-agent|jarrahi-ritala-2025-principal-agent]] , [[src/research_assistant/spaces/QNTR/wiki/sources/vu-2025-agentic-bpm-governance|vu-2025-agentic-bpm-governance]]
- **First seen**: [[src/research_assistant/spaces/QNTR/wiki/sources/jarrahi-ritala-2025-principal-agent|jarrahi-ritala-2025-principal-agent]]
- **Sources**: [[src/research_assistant/spaces/QNTR/wiki/sources/eulerich-2024-dark-side-rpa|eulerich-2024-dark-side-rpa]] , [[src/research_assistant/spaces/QNTR/wiki/sources/haase-2024-interdisciplinary-directions|haase-2024-interdisciplinary-directions]] , [[src/research_assistant/spaces/QNTR/wiki/sources/jarrahi-ritala-2025-principal-agent|jarrahi-ritala-2025-principal-agent]] , [[src/research_assistant/spaces/QNTR/wiki/sources/vu-2025-agentic-bpm-governance|vu-2025-agentic-bpm-governance]]
<!-- OBSIDIAN-LINKS:END -->
