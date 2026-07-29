---
type: source
title: "Multi-Agent Systems (Editorial, Special Issue of Applied Sciences)"
maturity: seed
tags: [multi-agent-systems, foundational-cs, agent-architecture, accountability-by-design, editorial, tangential]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [research_paper, literature_review, term_paper, thesis]
draws_from: []
authors: ["Julian, Vicente", "Botti, Vicente"]
year: 2019
journal: "Applied Sciences"
volume: "9(7)"
pages: "1402"
source_path: "knowledge/literature review/Agentic Governance/Relevant Readings/Tech Paper Deep Dive (Round 1)/Multi-Agent Systems_Julian_Botti_2019_Q2.pdf"
doi: "10.3390/app9071402"
ingested: 2026-07-28
target_path: src/research_assistant/spaces/QNTR/wiki/sources/julian-botti-2019-multi-agent-systems.md
---

# Multi-Agent Systems (Editorial, Special Issue of Applied Sciences)

Guest-editorial introduction to a Special Issue of *Applied Sciences* (MDPI), by Vicente Julian and Vicente Botti of the Departamento de Sistemas Informáticos y Computación, Universitat Politècnica de València, Spain. Received and accepted 29 March 2019; published 3 April 2019 [source_path, p.1]. Open access under CC BY [source_path, p.7]. This is an editorial, not a primary study: it frames the field and then summarizes the Special Issue's accepted contributions.

## Key Arguments

The editorial situates the intelligent agent as a concept "born from the area of artificial intelligence," where AI is described as the analysis and design of "autonomous entities capable of exhibiting intelligent behavior"; an intelligent agent is expected to perceive its environment, reason about how to achieve its objectives, act toward them under "some principle of rationality," and interact with other agents (artificial or human) [source_path, p.1]. The attribution for this framing is to Russell & Norvig, *Artificial Intelligence: A Modern Approach*, 3rd ed. (2009) [source_path, p.1, ref. 1; p.6].

It defines a multi-agent system (MAS) as "a particular case of a distributed system" whose particularity is that "the components of the system are autonomous and selfish, seeking to satisfy their own objectives," and that these are "open systems without a centralized design" [source_path, p.1]. That framing is attributed to Wooldridge, *An Introduction to MultiAgent Systems*, 2nd ed. (2009) [source_path, p.1, ref. 2; p.6]. The editorial argues MAS drew interest as "an enabling technology for complex applications that require distributed and parallel processing of data and operate autonomously in complex and dynamic domains" [source_path, p.1], and lists application domains where agent-based applications are "becoming a standard": e-commerce, logistics, supply chain management, telecommunications, healthcare, and manufacturing [source_path, p.1, Abstract].

On the engineering side, the editorial states that agent architectures must include "reactivity, proactivity, and sociability," properties it calls hard to program in dynamic, complex environments, and it identifies coordination of coalitions or teams of agents (including the need for agents "to reach agreements") as the focus of most current MAS research [source_path, pp.1-2]. It notes that building MAS integrates three technology areas: software-engineering techniques, AI techniques, and concurrent programming [source_path, p.2].

A governance-adjacent point worth flagging: in surveying agent-oriented software engineering, the editorial highlights a contribution in which "accountability plays a central role in MAS engineering," proposing agent systems "where accountability is a property that is guaranteed by design," realized through an interaction protocol called ADOPT and implemented on the JaCaMo platform [source_path, p.2]. This "accountability by design" framing is the single strand in the editorial that touches the governance concerns of the QNTR program.

## Methodology

Not applicable in the empirical sense. As an editorial, the piece presents no data, sample, or analysis of its own. Its "method" is curation: it organizes the Special Issue's accepted papers into four themes: MAS and methodologies (agent-oriented software engineering), MAS and learning, MAS in ambient intelligence, MAS and simulation, and MAS in smart cities, describing each accepted paper in turn [source_path, pp.2-5]. Those accepted-paper summaries cover application areas (coordinated hovercraft control via radial-basis-function neural networks, behavior-tree learning tested on Pac-Man, accessibility tooling, museum-exhibition interaction agents, online double-auction markets for perishable goods, bike-sharing demand prediction in Salamanca, EV charging-station placement, agreement technologies for emergency medical coordination) that are outside the QNTR research scope [source_path, pp.2-5].

## Key Findings

None in the empirical-results sense; an editorial reports no effect sizes, tables, or measured outcomes. The editors' summative claim is that MAS research "continues to provide technological solutions in a wide variety of domains" and shows "excellent health after more than two decades of research," concluding that the goal of the Special Issue was "more than reached" [source_path, p.5].

## Relevance to Research

Thin and tangential. This editorial is a classic distributed-systems / AI treatment of multi-agent systems and predates the large-language-model "agentic AI" wave that the QNTR governance research targets. It contributes to the QNTR wiki in two limited ways:

1. **Lineage anchor for the term "multi-agent system."** It provides a citable, pre-LLM CS definition (autonomous, self-interested agents; open, non-centralized systems; reactivity/proactivity/sociability), attributed to Wooldridge (2009) and Russell & Norvig (2009) [source_path, p.1]. This is useful only as historical grounding for the modern usage captured in `sources/sapkota-2025-ai-agents-vs-agentic-ai.md`, whose "multiplicity" property (multi-agent collaboration and coordination) is the direct descendant of this classic MAS framing. This editorial is the older, disciplinary-origin end of that lineage; it is not a substitute for the agentic-AI-specific evidence.

2. **"Accountability by design" hook.** The editorial's note that accountability can be a designed-in property of MAS organizations (ADOPT / JaCaMo) [source_path, p.2] is the one point that intersects the CS-side governance-architecture position already documented in `syntheses/cs-vs-management-governance-gap.md`. It reinforces, but does not extend, that position: like Kolt (2025) and Lu et al. (2024) in that synthesis, it prescribes an engineering/architectural property and offers no enterprise-level outcome evidence.

What this source does NOT provide, and should not be cited for: any empirical governance-to-risk or governance-to-performance evidence; any organizational or management-level analysis; any treatment of agentic AI in the LLM sense; any measurement framework. It is an application-and-methods editorial in computer science.
