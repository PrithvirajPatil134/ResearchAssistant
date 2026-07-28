---
title: "Governance Maturity"
type: concept
maturity: working
created: 2026-05-07
last_updated: 2026-05-07
originating_space: QNTR
applicable_to: [research_paper, term_paper, thesis]
schema_version: "1.0"
aliases: ["AI governance maturity", "governance maturity construct", "responsible AI governance practices"]
first_seen: sources/papagiannidis-2025-responsible-ai-governance
sources:
  - wiki/sources/papagiannidis-2025-responsible-ai-governance
  - wiki/sources/mikalef-2021-ai-capability
  - wiki/sources/berente-2021-managing-ai
tags: [governance-maturity, independent-variable, formative-construct, structural-relational-procedural]
draws_from:
  - wiki/sources/papagiannidis-2025-responsible-ai-governance.md
  - wiki/sources/mikalef-2021-ai-capability.md
  - wiki/sources/berente-2021-managing-ai.md
---

## Definition

Governance maturity describes an organization's capacity to develop, deploy, and monitor AI applications in a manner that manages risk and produces value. Papagiannidis et al. (2025) define responsible AI governance as "a set of practices for developing, deploying, and monitoring AI applications in a safe, trustworthy, and ethical manner that ensures appropriate functionality of AI over the entire lifecycle" (p.6). When applied specifically to agentic AI, governance maturity captures how well an organization's governance regime addresses the unique challenges of autonomous, goal-directed systems that exercise discretion and operate at superhuman speed.

This is the independent variable (IV) in the agentic AI governance research paper.

[Source: wiki/sources/papagiannidis-2025-responsible-ai-governance.md, §Summary]

## Key Dimensions

### Three Practice Categories (Papagiannidis et al. 2025)

Drawing on IT governance theory (Van Grembergen et al., 2004; Tallon et al., 2013), the framework identifies three interdependent practice types:

1. **Structural practices**: Define decision-makers, rights, responsibilities, governance committees, and decision-making protocols. Poorly understood regarding vertical power dynamics, horizontal coordination, and extended stakeholder ecosystems.

2. **Procedural practices**: Encompass data/model management, pipeline evaluation, human-AI interaction protocols, incident response, and strategic planning. Lack strategic-level integration; organizations struggle to harmonize competitive strategies with governance.

3. **Relational practices**: Establish internal and external links, develop responsible AI literacy, ensure stakeholder involvement. Require understanding how governance norms diffuse through informal channels.

[Source: wiki/sources/papagiannidis-2025-responsible-ai-governance.md, §Key Arguments, pp.10-14]

### AI Capability as Methodological Precedent (Mikalef and Gupta 2021)

Mikalef and Gupta conceptualize AI capability as a third-order formative construct comprising tangible resources, human skills, and intangible resources. The intangible dimension (inter-departmental coordination, organizational change capacity, risk proclivity) overlaps substantially with governance practices. Their finding that intangible resources (weight=0.407) and human skills (weight=0.410) contribute more to AI capability than tangible resources (weight=0.346) suggests governance-adjacent factors drive organizational AI performance more than technology investments.

[Source: wiki/sources/mikalef-2021-ai-capability.md, §Findings, Table 5]

### Three Facets Requiring Governance (Berente et al. 2021)

Berente et al. frame AI management through three interrelated facets: autonomy (acting without human intervention), learning (improving through data), and inscrutability (being unintelligible to audiences). Each facet demands governance attention. The inscrutability dimensions (opacity, transparency, explainability, interpretability) map directly onto governance mechanisms. The argument that managers who address all three facets "can avoid negative consequences" provides the foundational logic for the governance maturity-reduces-risk proposition.

[Source: wiki/sources/berente-2021-managing-ai.md, §Key Arguments; §Relevance to Research]

## How Sources Relate

These three sources construct governance maturity from different angles:

**Papagiannidis et al.** provide the *what*: a taxonomy of governance practice types (structural, relational, procedural) grounded in IT governance theory. Their contribution is organizational: what kinds of practices exist and how they interrelate.

**Mikalef and Gupta** provide the *how to measure*: a validated formative measurement approach for AI-related organizational constructs. Their AI capability instrument demonstrates that higher-order formative constructs with non-technical dimensions can be reliably measured via survey and linked to performance outcomes.

**Berente et al.** provide the *why governance matters*: three facets (autonomy, learning, inscrutability) that explain why AI systems resist conventional management and require dedicated governance mechanisms.

Together, they suggest governance maturity is: (1) multi-dimensional (structural + procedural + relational), (2) formative in measurement (practices constitute the construct rather than reflect it), and (3) justified by the unique properties of AI systems that make standard management insufficient.

## Application to Research

### Formative Construct Concern

Prof. Prashar's May 5 feedback explicitly flags this: "you are describing Agentic AI governance maturity as your IV. This sounds like a formative construct, which might require a different set of analysis techniques than the usual SEM and regression."

The formative nature follows from the definition: governance practices (policy completeness, oversight structure, audit frequency, training coverage, incident response protocols) are causes of maturity, not symptoms. Omitting any practice potentially alters the construct's meaning, which is Diamantopoulos's (2011) hallmark of formative measurement.

[Source: QNTR/feedback/response_prof_prashar_termpaper_review_20260505.md, §Method]

### Measurement Does Not Yet Exist

Prashar also notes: "I doubt the real measures of the construct exist. If they do, please cite the papers that developed those measures. If they do not, then developing the measures becomes a herculean task that should be the key aim of the qualitative study."

This positions Phase 1 qualitative research as construct development rather than hypothesis testing. The structural-relational-procedural taxonomy from Papagiannidis et al. provides candidate dimensions; Mikalef and Gupta's formative measurement approach provides the methodological template; but the specific indicators for agentic AI governance maturity must be developed from primary data.

[Source: QNTR/feedback/response_prof_prashar_termpaper_review_20260505.md, §Method]

### Operationalization Path

1. Phase 1 (qualitative): Code executive interviews against the structural-relational-procedural taxonomy. Identify which practices are specific to agentic AI vs. inherited from IT governance.
2. Phase 2 (quantitative): Build a formative measurement model following Mikalef and Gupta's MacKenzie et al. (2011) guidelines. Use CBSEM with MIMIC model (per Diamantopoulos 2011) rather than PLS if targeting A* journal publication.
3. Validation: expert panel for content validity, VIF checks for multicollinearity among formative indicators, at least two outgoing structural paths for identification.

## Open Questions

1. Is governance maturity unidimensional (a single formative index) or multidimensional (separate structural, relational, and procedural sub-constructs that interact)?
2. How does governance maturity for agentic AI differ from governance maturity for conventional AI (which Papagiannidis et al. address)? The key differentiators are likely autonomy-level and multi-agent coordination.
3. Can governance maturity be measured through secondary data (regulatory filings, incident reports, policy documents) or does it require primary survey data?
4. How does the Papagiannidis et al. framework interact with Kolt's three principles (inclusivity, visibility, liability)? Are these competing taxonomies or complementary levels of abstraction?

[Source: wiki/sources/papagiannidis-2025-responsible-ai-governance.md, §Limitations; wiki/sources/mikalef-2021-ai-capability.md, §Limitations]

---

<!-- OBSIDIAN-LINKS:START (auto-generated by scripts/obsidian-graph-linker.py, do not edit by hand) -->
## Related
- **Draws from**: [[src/research_assistant/spaces/QNTR/wiki/sources/berente-2021-managing-ai|berente-2021-managing-ai]] , [[src/research_assistant/spaces/QNTR/wiki/sources/mikalef-2021-ai-capability|mikalef-2021-ai-capability]] , [[src/research_assistant/spaces/QNTR/wiki/sources/papagiannidis-2025-responsible-ai-governance|papagiannidis-2025-responsible-ai-governance]]
- **First seen**: [[src/research_assistant/spaces/QNTR/wiki/sources/papagiannidis-2025-responsible-ai-governance|papagiannidis-2025-responsible-ai-governance]]
- **Sources**: [[src/research_assistant/spaces/QNTR/wiki/sources/berente-2021-managing-ai|berente-2021-managing-ai]] , [[src/research_assistant/spaces/QNTR/wiki/sources/mikalef-2021-ai-capability|mikalef-2021-ai-capability]] , [[src/research_assistant/spaces/QNTR/wiki/sources/papagiannidis-2025-responsible-ai-governance|papagiannidis-2025-responsible-ai-governance]]
<!-- OBSIDIAN-LINKS:END -->
