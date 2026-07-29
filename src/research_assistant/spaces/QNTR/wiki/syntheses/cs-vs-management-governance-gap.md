---
title: "The CS-vs-Management Governance Gap"
type: synthesis
maturity: seed
created: 2026-05-07
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [QNTR, DBA]
schema_version: "1.0"
draws_from:
  - spaces/QNTR/wiki/sources/kolt-2025-governing-ai-agents.md
  - spaces/QNTR/wiki/sources/lu-2024-responsible-ai-pattern-catalogue.md
  - spaces/QNTR/wiki/sources/mikalef-2021-ai-capability.md
  - spaces/QNTR/wiki/sources/papagiannidis-2025-responsible-ai-governance.md
  - spaces/QNTR/wiki/sources/vu-2025-agentic-bpm-governance.md
  - spaces/QNTR/wiki/sources/enholm-2022-ai-in-is-research.md
  - spaces/QNTR/wiki/sources/dafoe-2018-ai-governance-research-agenda.md
tags: [research-gap, positioning, governance-to-risk, bridge-paper]
target_path: src/research_assistant/spaces/QNTR/wiki/syntheses/cs-vs-management-governance-gap.md
---

## Thesis Statement

Computer science has produced governance frameworks for AI agents (Lu et al. 2024; Kolt 2025). Management research has produced empirical evidence that AI capabilities drive business value (Mikalef and Gupta 2021) and that responsible AI governance practices can be taxonomized (Papagiannidis et al. 2025). But the bridge paper connecting agentic governance maturity to firm-level risk and performance outcomes does not exist. Vu et al. (2025) come closest but lack quantitative validation and draw from participants with no actual agentic AI experience. Collins et al. (2022) confirm that the "dark side" of AI remains substantially understudied in IS. This is the gap the agentic AI governance research fills: it connects what CS prescribes (governance architecture) with what management measures (enterprise outcomes) for a category of AI systems (autonomous, goal-directed agents) that neither field has empirically addressed.

## Evidence From Sources

### CS Side: Governance Architectures Without Outcome Evidence

**Kolt (2025)** proposes three governance principles for AI agents: inclusivity, visibility, and liability. These are normative: they specify what governance *should* look like but provide no operational definitions, no measurement frameworks, and no empirical test. The contribution is "theoretical and analytical" with "no empirical data, survey, experiment, or case study" (Kolt, §Methodology). The three principles remain "normative proposals without operational definitions or measurement frameworks" (Kolt, §Limitations).

[Source: QNTR/wiki/sources/kolt-2025-governing-ai-agents.md, §Methodology, §Limitations]

**Lu et al. (2024)** catalogue 35 responsible AI patterns across governance, process, and product levels. They include an "RAI Maturity Model" pattern (p. 9) and multi-level governance structures (industry, organization, team). However, the patterns are "identified from literature, not empirically validated in organizational settings" (Lu et al., §Limitations). There is "no quantitative assessment of pattern adoption rates or effectiveness" (Lu et al., §Limitations).

[Source: QNTR/wiki/sources/lu-2024-responsible-ai-pattern-catalogue.md, §Findings, §Limitations]

Both papers prescribe governance architecture. Neither tests whether that architecture reduces incidents, lowers losses, or improves compliance.

### Management Side: Business Value Evidence Without Agentic Specificity

**Mikalef and Gupta (2021)** demonstrate that AI capability (a formative construct encompassing tangible, human, and intangible resources) positively influences firm performance (beta=0.561, p<0.001) and organisational creativity (beta=0.573, p<0.001). The model explains 51.3% of variance in performance. Intangible resources (inter-departmental coordination, change capacity) carry higher formative weights than technical resources.

[Source: QNTR/wiki/sources/mikalef-2021-ai-capability.md, §Findings, Table 5]

But this construct captures "AI capability" broadly. It does not distinguish between passive ML models and autonomous agents. It measures the *capability to deploy AI*, not the *governance of AI after deployment*. The governance-to-risk pathway is absent from the model.

**Papagiannidis et al. (2025)** synthesize 48 papers into a framework of structural, relational, and procedural governance practices, with effects mapped to business value and social assessment. The framework draws on IT governance theory (Van Grembergen et al. 2004) and proposes that responsible AI governance "can generate value for companies by legitimizing their presence in a broader societal context and improving morale, productivity, and employee loyalty" (p. 14).

[Source: QNTR/wiki/sources/papagiannidis-2025-responsible-ai-governance.md, §Summary, §Key Arguments, §Key Quotes]

Yet the proposed relationships "require empirical testing" (Papagiannidis et al., §Limitations). The framework addresses AI generally, not specifically agentic AI systems with autonomous goal-pursuit. The governance-to-risk pathway exists as a research question in their agenda (Table 5) but remains unanswered.

### The Near-Bridge: Vu et al. (2025)

**Vu et al. (2025)** come closest to bridging the gap. They investigate governance of AI agents within business processes, interview 22 practitioners, and propose six governance recommendations plus four BPM alignment actions. The recommendations (business context definition, ethical guardrails, human-agent collaboration, customised autonomy levels, risk management, fallback mechanisms) are concrete governance dimensions that could inform construct development.

[Source: QNTR/wiki/sources/vu-2025-agentic-bpm-governance.md, §Key Arguments, §Findings]

But two critical weaknesses prevent Vu et al. from being the bridge paper:
1. "None of the 22 participants reported having actual practical experience with agentic AI. Their assessments are based on expectations, often against the backdrop of existing RPA technologies" (§Summary, citing §4).
2. The study is purely qualitative with no quantitative validation. No relationship to enterprise risk outcomes is tested.

[Source: QNTR/wiki/sources/vu-2025-agentic-bpm-governance.md, §Summary, §Limitations]

### The Dark-Side Gap: Collins et al. (2022)

**Collins et al. (2022)** review 98 primary IS studies on AI (2005-2020) and find that "much of the work that has been published to date remains untheoretical" (p. 12). Process automation dominates (49 of 98 studies); higher-order AI applications (decision-making, autonomous action) are under-researched. The "dark side" of AI (governance, risk, societal impacts) is explicitly identified as a gap: "There is a relative lack of research into societal or governmental implications of machine learning and its recent advancements" (p. 11).

[Source: QNTR/wiki/sources/enholm-2022-ai-in-is-research.md, §Key Arguments, §Key Quotes]

This confirms the gap from within the IS discipline's own self-assessment.

### The Macro Frame: Dafoe (2018)

**Dafoe (2018)** predates both the CS-architecture and management-outcome literatures and defines the field they both sit inside. He frames "the AI governance problem" as "the problem of devising global norms, policies, and institutions to best ensure the beneficial development and use of advanced AI" (p.i), and separates AI governance (institutions and contexts) from AI safety (how AI is technically built) (p.6). This gives the gap synthesis a third level of analysis above the CS-vs-management axis: Kolt and Lu prescribe architecture, Mikalef and Papagiannidis measure organizational outcomes, and Dafoe defines the field and its risk structure at the societal scale.

Dafoe does not close the enterprise-level bridge. He operates at the civilizational level and offers no firm-level measurement (p.i, pp.2-3). But two of his framings strengthen the gap argument without resorting to absence claims. First, his important/tractable/neglected heuristic explains why the enterprise-outcome question is under-studied: cross-cutting governance questions "do not directly and exclusively contribute to an actor's profit or power" (p.13). Second, his alignment-in-capitalism analogy (Enron, Deepwater Horizon, Theranos, Volkswagen) frames misaligned AI as a corporate-governance failure, which is the mechanism the enterprise-risk pathway assumes but does not yet measure (p.27).

[Source: QNTR/wiki/sources/dafoe-2018-ai-governance-research-agenda.md, p.i, p.6, p.13, p.27]

## How Sources Connect

The sources form a supply chain with a missing link:

```
CS governance prescriptions     Management outcome evidence
(Kolt, Lu et al.)               (Mikalef, Papagiannidis)
         |                                |
         |   [MISSING: empirical link]    |
         |                                |
         v                                v
   Governance architecture  ------->  Enterprise risk / performance
   for agentic AI                     outcomes
```

Kolt defines the governance problem (information asymmetry, discretionary authority, loyalty failures in AI agents). Lu et al. catalogue patterns that address it. Papagiannidis et al. provide the practice taxonomy (structural, relational, procedural). Mikalef and Gupta demonstrate that AI-related organisational constructs can predict firm performance using formative measurement. Collins et al. confirm that nobody has filled the centre of this chain for autonomous AI systems.

Vu et al. occupy a partial position: they have the right phenomenon (agentic AI governance) but neither quantitative evidence nor participants with actual experience.

The gap is not merely "more research needed." It is a specific missing empirical link: does the adoption of governance practices for autonomous AI agents (the IV, formatively measured) predict fewer incidents, lower financial losses, and fewer compliance failures (the DVs) at the enterprise level?

## Implications for Research

1. **The research fills a documented gap** confirmed by multiple sources across disciplines. It is not an invented positioning.

2. **Phase 1 qualitative work must produce governance constructs that pass the Vu et al. threshold**: participants with actual agentic AI experience (not RPA-benchmarked expectations), yielding dimensions that can be operationalised into formative indicators.

3. **Phase 2 quantitative work follows Mikalef and Gupta's methodological precedent**: formative higher-order construct, PLS-SEM or CBSEM, linked to performance outcomes. The difference: governance maturity (not capability), enterprise risk (not creativity), and agentic AI specifically (not AI broadly).

4. **Papagiannidis et al.'s three-category taxonomy** (structural, relational, procedural) can serve as the organising frame for governance maturity sub-dimensions, grounded in IT governance theory.

5. **Kolt's three principles** (inclusivity, visibility, liability) can serve as observable indicators within those sub-dimensions during Phase 1 qualitative coding.

## Open Questions

- Does the formative governance maturity construct need a fourth sub-dimension beyond structural, relational, and procedural? Kolt's "liability" dimension sits awkwardly in the Papagiannidis taxonomy.
- How do Vu et al.'s six recommendations map onto the structural/relational/procedural taxonomy? Some span categories.
- Is the governance-to-risk relationship direct, or mediated by factors like "control rigidity" (over-governance reducing agility)?
- What is the minimum sample size for a third-order formative model in CBSEM? Mikalef and Gupta managed with 143 respondents in PLS-SEM, but Diamantopoulos recommends CBSEM with 200+.
- Can the meta-analysis co-authored with Prof. Prashar produce the systematic evidence base that Steps 3-5 of this synthesis assume is missing?

[Source: QNTR/wiki/sources/mikalef-2021-ai-capability.md, §Methodology; QNTR/wiki/sources/papagiannidis-2025-responsible-ai-governance.md, §Key Arguments; QNTR/wiki/sources/vu-2025-agentic-bpm-governance.md, §Key Arguments]

---

<!-- OBSIDIAN-LINKS:START (auto-generated by scripts/obsidian-graph-linker.py, do not edit by hand) -->
## Related
- **Draws from**: [[src/research_assistant/spaces/QNTR/wiki/sources/enholm-2022-ai-in-is-research|enholm-2022-ai-in-is-research]] , [[src/research_assistant/spaces/QNTR/wiki/sources/kolt-2025-governing-ai-agents|kolt-2025-governing-ai-agents]] , [[src/research_assistant/spaces/QNTR/wiki/sources/lu-2024-responsible-ai-pattern-catalogue|lu-2024-responsible-ai-pattern-catalogue]] , [[src/research_assistant/spaces/QNTR/wiki/sources/mikalef-2021-ai-capability|mikalef-2021-ai-capability]] , [[src/research_assistant/spaces/QNTR/wiki/sources/papagiannidis-2025-responsible-ai-governance|papagiannidis-2025-responsible-ai-governance]] , [[src/research_assistant/spaces/QNTR/wiki/sources/vu-2025-agentic-bpm-governance|vu-2025-agentic-bpm-governance]]
<!-- OBSIDIAN-LINKS:END -->
