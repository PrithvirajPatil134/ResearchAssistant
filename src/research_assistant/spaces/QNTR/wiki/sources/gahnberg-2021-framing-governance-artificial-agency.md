---
type: source
title: "What rules? Framing the governance of artificial agency"
maturity: seed
tags: [governance-framework, theoretical-lens, artificial-agency, material-agency, agent-properties, peas, policy-and-society, algorithmic-governance]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [research_paper, term_paper, thesis, literature_review]
draws_from: []
authors:
  - "Gahnberg, C."
year: 2021
journal: "Policy and Society"
volume: "40(2)"
pages: "194-210"
doi: "10.1080/14494035.2021.1929729"
source_path: "knowledge/literature review/Agentic Governance/Relevant Readings/Tech Paper Deep Dive (Round 1)/Framing Governance of Artificial Agency_Ganhberg_Q1+B_2021.pdf"
ingested: 2026-07-28
target_path: src/research_assistant/spaces/QNTR/wiki/sources/gahnberg-2021-framing-governance-artificial-agency.md
---

## Summary

Carl Gahnberg, then a PhD candidate at the Graduate Institute of International and Development Studies (IHEID) in Geneva, argues that an analysis of AI governance should build on understanding AI as the creation of "artificial agents," and that the challenge governance seeks to address is best understood as one of *material agency* rather than "intelligence" (p.1). The paper proposes a conceptual framework in which the fundamental properties of an artificial agent can be used to systematically analyze governance across the full range of AI applications, whether embodied as software in a digital environment or as robots in the physical world (p.1, p.3). It positions itself as a bridge between the literature on AI and the literature on governance, complementing existing work in two regards: reframing the governance challenge as material agency rather than absolute system capacity, and supplying a lens for systematic inquiry that earlier ethics-, law-, and application-specific work lacked (p.2).

The framework operationalizes the governance of AI as "intersubjectively recognized rules that define, constrain and shape expectations about the fundamental properties of an artificial agent" (p.8), paraphrasing Biersteker's (2009) definition of global governance.

## Key Arguments

- The governance challenge is not the system's absolute capacity or "intelligence" but the *material agency* it exhibits in a given context; "intelligence" is described as "simply a nebulous success metric for the system's performance" (p.2).
- The dominant approach to building AI conceptualizes the task as creating "artificial agents," defined (following Russell & Norvig 2009, p.34) as "anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators" (p.3).
- An artificial agent has four fundamental properties, drawn from Russell & Norvig's "PEAS" task-environment specification: Performance measure (what counts as good behavior), Environment (what the agent interacts with), Actuators (how it affects its environment), and Sensors (how it gets information). Varying any of the four changes the nature of the agent and the agency it asserts (p.3, pp.4-5). Table 1 (p.4) illustrates the four properties for an autonomous vehicle, an image classifier, and a part-picking robot (adapted from Russell & Norvig 2009, pp.40-42).
- Material agency draws on a social-science tradition (Latour 2005; Leander 2013; Pinch & Bijker 1984) treating material objects as explanatory variables in their own right. Citing Lehrer et al. (2018), "material agency describes a technology's capacity to act on its own, apart from human intervention, while human agency refers to humans' capacity to form and realize their goals"; this is not an anthropomorphic claim but a recognition that artifacts affect social ordering (p.5).
- Artificial agency is defined as the ability of artificial agents "to be delegated decision-making, to re-ontologize the world, and to regulate behavior in a manner that is both unpredictable and opaque" (p.7). This is the phenomenon that governance seeks to address.
- Opacity and unpredictability have two sources tied to autonomy: machine-learning agents define and modify their own decision rules from data, so their actions can be hard to predict or explain (the Google Photos image-classifier "gorillas" case, p.7), and their internal workings can be opaque even to their creators, yielding "black boxes" (Burrell 2016; Mittelstadt et al. 2016; Matthias 2004) (p.7).
- Governance is a relational concept describing a constituency's behavior toward a system of rules; the authorship of rules need not be the state but can come from private actors, provided the governed recognize them as legitimate (Hurd 1999) (p.8). Rules may be formal (laws, regulation) or informal (norms), and restrictive, prescriptive, or constitutive (Biersteker 2009; Finnemore & Sikkink 1998) (p.8).
- Governing artificial agency means governing the agent's design and deployment through rules bearing on each of the four fundamental properties. The paper illustrates this with public and private mechanisms for each property:
  - **Performance measure**: the proposed norm against "killer robots" (fully autonomous lethal weapons) under discussion by the UN Group of Governmental Experts, and the AI-researcher pledge against lethal autonomous weapons (Jenkins 2018); explainability requirements traceable from the 1970s US Equal Credit Opportunity Act and Fair Credit Reporting Act, through the 1995 EU Data Protection Directive, to the 2016 GDPR "right to explanation"; the German Ethics Commission on Automated Driving recommendations; and the IEEE P7001 transparency standard (pp.8-10).
  - **Environment**: autonomous-vehicle test-zone permissions (Volvo's Drive Me project, limited to 50 km around Gothenburg), poker sites (Full Tilt) banning bots in their terms of service, and the Algorithmic Justice League's work on "inclusive training sets" (founder Joy Buolamwini) as a solution-type mechanism (pp.10-11).
  - **Actions**: the SAE J3016 six-level taxonomy of driving automation (adopted by the US Department of Transportation), Twitter's bot-automation rules that permit bots but prohibit specific actions, and the IEEE P7009 fail-safe design standard (pp.11-12).
  - **Percepts**: privacy regulation such as GDPR constraining what information an agent may access, the W3C "Do Not Track" specification, and machine-readable privacy-statement standards (W3C P3P, IEEE P7012) as solution-type mechanisms (p.12).
- An artificial agent may itself be a multi-agent system: higher-level agents (e.g., a vehicle's driving agent) depend on lower-level sub-agents (e.g., an image classifier). Governing safe behavior may therefore require rules for sub-agents as well, and the framework helps identify the role of sub-agents in overall system performance (p.4, p.13).
- The framework exposes the "governors" of AI by identifying actors that perform authoritative rule-making functions, potentially including developer communities (e.g., Stack Overflow) and software libraries (e.g., TensorFlow) at the code-implementation level (p.13).

## Methodology

Conceptual/theoretical paper in political science and governance studies. It builds a framework by combining the technical definition of artificial agents (Russell & Norvig 2009) with the governance literature (Biersteker 2009; Bevir 2009, 2012; Stoker 1998; Hurd 1999). Rather than empirical data collection, it uses illustrative empirical examples of existing and emerging governance mechanisms to demonstrate the framework's applicability across physical and digital AI applications (p.2, p.12). The author explicitly flags these examples as "aspirational governance mechanisms" for illustration, noting that determining whether the identified rules actually govern requires a closer, more systematic look into whether they are adhered to and are in fact authoritative (pp.12-13).

## Findings

As a conceptual paper the contribution is the framework itself rather than empirical results:

- Reframing the governance object from "intelligence" to material/artificial agency makes the analysis applicable to all artificial agents regardless of their perceived intelligence, and thus encompasses both future developments and prior agent research not originally framed as AI (p.14).
- Structuring governance around the four fundamental properties yields a general framework usable both for cross-cutting rules applicable to all artificial agents and for detailed analysis of a specific application (e.g., autonomous vehicles in a given country, or information-curation algorithms), including identification of governance gaps (pp.12-13).
- The framework accommodates multi-agent systems and can help locate where in a system's agent hierarchy governance rules need to bite (p.13).

## Relevance to Research

Relevant to the Prashar co-authored agentic-AI-governance work as an *alternative agency lens*, distinct from the principal-agent lens already anchoring the term paper:

- The QNTR wiki's principal-agent pages (Kolt 2025 [wiki/sources/kolt-2025-governing-ai-agents.md]; Jarrahi & Ritala 2025 [wiki/sources/jarrahi-ritala-2025-principal-agent.md]) treat "agency" in the economic/legal sense of a principal delegating to an agent. Gahnberg treats "agency" in the material sense: the technology's own capacity to act and shape social ordering (p.5, p.7). Holding both lenses side by side sharpens the "agentic" distinction the research turns on.
- Gahnberg's four fundamental properties (performance measure, environment, actions, percepts) offer a candidate structure for decomposing governance mechanisms, which may inform how governance-maturity dimensions are defined in the qualitative phase. This is a possible use of the framework, not a claim the paper makes about enterprise risk.
- The paper's aim to "bridge insights across social science and technical perspectives on AI" (p.1) speaks directly to the CS-vs-management governance-gap thread [wiki/syntheses/cs-vs-management-governance-gap.md]: Gahnberg is a governance-studies scholar explicitly borrowing the technical agent definition, an example of a cross-perspective bridge.
- Its treatment of unpredictability and opacity as defining features of artificial agency (p.7) corroborates, from a political-science vantage, the same properties Kolt and Taeihagh identify as reasons conventional oversight fails.

## Limitations

- Conceptual and illustrative only; the paper presents no empirical test of whether the identified mechanisms actually govern, and explicitly frames its examples as "aspirational" pending systematic study of adherence and authority (pp.12-13).
- It addresses public-policy and societal governance and does not treat enterprise- or firm-level governance or enterprise-risk outcomes.
- It does not engage principal-agent theory or the economic/legal agency doctrine that anchors the term paper; the two agency framings are complementary but developed in separate literatures.
- Published in 2021, it predates the current wave of large-language-model "agentic AI"; its examples center on autonomous vehicles, online bots, search/ranking, and predictive analytics rather than LLM-based agents.

## Key Quotes

- "This paper argues that an analysis of the technology's governance is premised on an understanding of AI as the creation of 'artificial agents', and that the challenge that governance seeks to address is best understood as one of material agency." (p.1)
- "The notion of 'intelligence' is, in this regard, simply a nebulous success metric for the system's performance, while the key governance challenge is better described as one of artificial agency." (p.2)
- "[M]aterial agency describes a technology's capacity to act on its own, apart from human intervention, while human agency refers to humans' capacity to form and realize their goals." (p.5, quoting Lehrer et al. 2018)
- "[O]ne can therefore think of artificial agency as the ability of artificial agents to be delegated decision-making, to re-ontologize the world, and to regulate behavior in a manner that is both unpredictable and opaque. This agency is the phenomenon that governance seeks to address." (p.7)
- "[I]t operationalizes the governance of AI as those intersubjectively recognized rules that define, constrain and shape expectations about the fundamental properties of an artificial agent." (p.8)
