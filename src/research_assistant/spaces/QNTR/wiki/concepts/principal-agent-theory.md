---
type: concept
title: "Principal-Agent Theory"
aliases: ["agency theory", "principal-agent problem", "principal-agent relationship", "PA theory"]
first_seen: sources/berente-2021-managing-ai
maturity: working
created: 2026-05-03
originating_space: QNTR
applicable_to: [research_paper, term_paper, literature_review, thesis_chapter]
sources:
  - sources/berente-2021-managing-ai
  - sources/jarrahi-2025-principal-agent
  - sources/eulerich-2024-dark-side-rpa
tags: [governance, economic-theory, ai-governance, delegation, information-asymmetry]
origin_discipline: economics
extension_to_ai: sources/jarrahi-2025-principal-agent
cross_space_relevance:
  - space: DBA
    relevance: high
    reason: "Core theoretical lens for any governance or delegation-themed dissertation chapter"
  - space: CRO
    relevance: high
    reason: "Applies to any industry case involving contractor relationships, outsourcing, or AI vendor management"
  - space: CW
    relevance: medium
    reason: "Relevant to case studies on corporate governance, manager-employee relationships, board oversight"
promotion_candidate: true
promotion_target: data/wiki/shared/concepts/principal-agent-theory.md
promotion_rationale: "Foundational theory cited in 3+ spaces. Space-specific applications (AI governance, dissertation chapters, industry cases) would reference the shared version plus add space-specific annotations."
last_updated: 2026-05-03
---

<!--
DRAFT TEMPLATE: FOR USER REVIEW BEFORE FINALIZATION

This is a hand-written reference concept page. Purpose:
1. Validate the concept page schema before automating ingest
2. Serve as the "gold standard" for concept pages across all spaces

IMPORTANT: This concept (principal-agent theory) is a STRONG CANDIDATE for promotion to data/wiki/shared/ because it appears in:
- QNTR research (Agentic AI Governance term paper, P1 and P3)
- DBA dissertation work (any AI governance chapter)
- CRO cases (any principal-agent relationship in industry)
The Cross-Space Relevance section below is the mechanism that triggers that promotion during lint.

Review checklist:
- [ ] Definition is precise and sourced
- [ ] Aliases cover the terms papers actually use
- [ ] Each source's contribution is distinct (not redundant summaries)
- [ ] Tensions and Debates section is honest (not sanitized)
- [ ] Cross-references to related concepts are bidirectional (this page links out, those pages link back)
- [ ] Cross-space relevance is specific, not generic
- [ ] Our Research Use section names specific propositions
-->

## Definition

<!-- GUIDANCE
WHAT GOES HERE: One precise definition (2-3 sentences). The definition every source in our corpus would roughly agree on. Use a canonical citation.
WHAT DOES NOT: Multiple competing definitions. Those belong in "How Different Sources Define It".
RULE: Canonical definition comes first. Variations come later.
-->

Principal-agent theory describes the relationship that arises when one party (the principal) delegates a task or decision to another party (the agent) who is expected to act on the principal's behalf. The theory focuses on the problems that emerge from this delegation when the agent's interests diverge from the principal's, when the principal cannot fully observe what the agent is doing, and when contracts cannot specify every contingency. In the AI context, Jarrahi and Ritala (2025, p. 3) recast this as the relationship between human principals and AI systems "designed to fulfill specific objectives while operating within human-defined constraints."

## Origin and Canonical References

<!-- GUIDANCE
WHAT GOES HERE: Where the theory came from. Original authors, seminal papers, the discipline (economics in this case). 2-3 sentences.
WHAT DOES NOT: Our sources' use of the theory. Those come in "How Different Sources Define It".
EXAMPLE: "Principal-agent theory emerged from Jensen and Meckling (1976) in the context of corporate governance and managerial delegation. Canonical treatment: Eisenhardt (1989) 'Agency Theory: An Assessment and Review' Academy of Management Review 14(1)."
-->

Principal-agent theory emerged from economics in the 1970s, with Jensen and Meckling (1976) formalizing the framework in the context of corporate governance and shareholder-manager delegation. Eisenhardt (1989), "Agency Theory: An Assessment and Review" in *Academy of Management Review* 14(1), remains the canonical management-discipline treatment and established the two dominant research streams: positivist agency theory (focused on governance mechanisms) and principal-agent research (focused on the general logic of delegation). [NOT YET VERIFIED in corpus: these canonical references are drawn from economics background rather than the three-paper corpus covered on this page. The corpus sources cited below treat principal-agent theory as an established lens without re-deriving its origins.]

## How Different Sources Define It

<!-- GUIDANCE
WHAT GOES HERE: Each source's specific framing of the concept. What they emphasize, what they add, what they leave out. One paragraph per source.
WHAT DOES NOT: Full paper summaries (those live in source pages). Just the part about THIS concept.
FORMAT: Subsection per source. Link to the source page at the start.
-->

### [Berente et al. 2021](../sources/berente-2021-managing-ai.md)

Berente and colleagues do not frame their MIS Quarterly editorial around principal-agent theory directly. The theory enters through the managing-autonomy discussion, where the authors cite Baird and Maruping (2021) on delegation to autonomous agents as a way of understanding the automation-augmentation tension (p. 1439). The implicit framing is that when humans delegate decisions to AI, the governance problem is no longer purely technical: it becomes a sociotechnical coordination problem where the principal must decide how much latitude to grant, under what monitoring, and with what override rights. Berente et al. emphasize that inscrutability (being unintelligible to specific audiences, pp. 1441-1442) makes this delegation harder than classical principal-agent delegation because the principal often cannot even interpret what the agent is doing, not just whether the agent is acting in good faith.

### [Jarrahi and Ritala 2025](../sources/jarrahi-2025-principal-agent.md)

Jarrahi and Ritala are the only source in the current corpus that commits to principal-agent theory as the primary analytical lens for AI agents. They position AI agents as "systems designed to fulfill specific objectives while operating within human-defined constraints" (p. 3) and argue that viewing AI agents as agents of human principals is more actionable than treating them as fully autonomous systems. Their Table 1 (pp. 7-9) identifies four principal-agent challenges specific to AI deployments: goal misalignment, information asymmetry, moral crumple zones in responsibility allocation, and multi-agent complexity. They also introduce "guided autonomy" with defined boundaries of delegation that "can grow as agents expand their learning" (p. 5), which operationalizes the classical trade-off between control and agent effectiveness in a way that accommodates continuous-learning systems. Mitigation strategies in Table 1 are prescriptive rather than empirically tested.

### [Eulerich et al. 2024](../sources/eulerich-2024-dark-side-rpa.md)

Eulerich and colleagues do not engage with principal-agent theory as a named framework. Their qualitative study of 26 RPA stakeholders at a Fortune 500 firm surfaces dynamics that are recognizably principal-agent in shape, even though the theory is not invoked. The centralized-versus-decentralized governance tension (p. 12), the problem of unknown bots that no principal has sight of (p. 10, "These are just the robots we know"), and the loss of process knowledge when bot creators leave (pp. 13-14) all describe information asymmetry, unmonitored agent behavior, and the erosion of principal capacity to evaluate agent output. This paper provides empirical grounding for the consequences that principal-agent theory predicts without adopting the theory's vocabulary.

## Evidence

<!-- GUIDANCE
WHAT GOES HERE: Specific claims from the corpus that use principal-agent theory, with citations and page references.
FORMAT: Bullet list. Each bullet is a claim with a citation.
EXAMPLE: "AI agents exhibit higher information asymmetry than human agents because their reasoning is partially inscrutable to principals (Jarrahi & Ritala 2025, p. 12)."
-->

- Viewing AI agents through a principal-agent lens is more actionable for business and organizational contexts than treating them as fully autonomous systems (Jarrahi and Ritala 2025, p. 3).
- Four principal-agent challenges apply to AI deployments: goal misalignment, information asymmetry, moral crumple zones in responsibility allocation, and multi-agent complexity (Jarrahi and Ritala 2025, Table 1, pp. 7-9).
- Guided autonomy with defined boundaries of delegation, where boundaries can expand as agents demonstrate learning, operationalizes the classical control-autonomy trade-off for continuously learning systems (Jarrahi and Ritala 2025, p. 5).
- Organization-wide governance regimes are needed to build guardrails for AI agents, extending principal oversight from the individual deployment to the enterprise (Jarrahi and Ritala 2025, p. 10).
- McKinsey's central review team evaluates every agent for risk, legal, and data policies before rollout, concretely implementing the principal's monitoring function (Jarrahi and Ritala 2025, p. 10).
- Managing delegation to autonomous AI involves an automation-augmentation tension: as the agent becomes more autonomous, humans risk losing their own autonomy and effectiveness, inverting the usual direction of principal-agent power (Berente et al. 2021, pp. 1439-1440).
- Inscrutability of AI agents (opacity, low transparency, limited explainability, limited interpretability) widens the information asymmetry beyond what classical principal-agent theory assumed, where agents were typically human and their reasoning could in principle be articulated (Berente et al. 2021, pp. 1441-1442).
- Empirically, RPA deployments produce "dark spots" of unknown, unregistered bots that no principal has visibility into, a direct manifestation of information asymmetry at scale (Eulerich et al. 2024, p. 10).
- The centralized-versus-decentralized governance tension in RPA is a principal-agent design choice in practice: heavy central governance reduces motivation, missing governance creates compliance failures (Eulerich et al. 2024, p. 12).

## Tensions and Debates

<!-- GUIDANCE
WHAT GOES HERE: Where sources in our corpus disagree about the theory or its applicability. With specific citations on each side.
WHAT DOES NOT: Generic "there are different views in the field." Be specific about which source says what.
EXAMPLE: "Berente et al. argue autonomy is a governance problem requiring human override mechanisms (p. 1438). Jarrahi and Ritala argue overriding autonomous agents defeats the purpose and propose outcome-based governance instead (p. 15). This tension is unresolved in the corpus."
CROSS-REFERENCE: If the tension is sharp, create a comparison page and link from here.
-->

**Is principal-agent theory the right lens, or a sufficient one?** Jarrahi and Ritala (2025, p. 3) commit to principal-agent theory as the primary framing for AI agents. Berente et al. (2021, p. 1438) prefer a broader sociotechnical emergence framing where delegation to autonomous agents is one concern among three (alongside learning and inscrutability). The papers do not directly argue with each other, but they represent a genuine choice in the literature: commit to a single economic-theoretic lens, or treat principal-agent dynamics as one input into a wider sociotechnical account. This choice is not resolved in the corpus.

**Prescriptive frameworks versus empirical outcomes.** Jarrahi and Ritala's Table 1 (pp. 7-9) proposes mitigation strategies for each principal-agent challenge, including responsibility allocation mechanisms for "moral crumple zones." Eulerich et al. (2024, pp. 13-14) find empirically that responsibility becomes diffuse in practice and that process knowledge is lost when bot creators leave, with no mechanism restoring principal capacity. The Jarrahi-Ritala prescriptions have not been tested against Eulerich's findings. A comparison page on prescriptive-versus-observed governance outcomes would be worth creating if this tension matters for the term paper. [NOT YET VERIFIED: cross-paper comparison not yet drafted in the corpus.]

**Does inscrutability break classical principal-agent assumptions?** Berente et al. (2021, pp. 1441-1442) argue that AI inscrutability creates information asymmetries that differ in kind from those in human delegation, because the principal often cannot interpret the agent's reasoning at all. Jarrahi and Ritala (2025, p. 3) treat information asymmetry as one of four challenges within the standard principal-agent frame. Whether AI inscrutability is a difference of degree or a difference of kind is an unresolved question that matters for whether classical principal-agent remedies (monitoring, outcome-based contracts, signaling) carry over to AI governance.

## Connections to Other Concepts

<!-- GUIDANCE
WHAT GOES HERE: Other concept pages that relate to this one. With a one-line explanation of the connection.
FORMAT: Bullet list with links.
WHY BIDIRECTIONAL: Every concept listed here should link back to principal-agent-theory from its own page. Lint checks for broken back-references.
-->

- [governance-maturity](./governance-maturity.md): Principal-agent theory explains why governance maturity matters. The more autonomous the agent, the wider the information asymmetry, and the more mature the governance regime must be to compensate. Back-link required on governance-maturity page.
- [inscrutability](./inscrutability.md): AI-specific extension of the information-asymmetry problem. The principal cannot interpret the agent's reasoning, not just the agent's motives. Back-link required on inscrutability page.
- [shadow-ai](./shadow-ai.md): Empirical consequence of unmanaged principal-agent relationships. Agents deployed without a registered principal, no monitoring, and no override path. Back-link required on shadow-ai page.
- [workflow-control-rigidity](./workflow-control-rigidity.md): The classical principal-agent control-autonomy trade-off, stated in process terms. Too much control suppresses agent effectiveness; too little produces unmanaged agent behavior. Back-link required on workflow-control-rigidity page.
- [information-asymmetry](./information-asymmetry.md): Core mechanism within principal-agent theory. Worth a dedicated page given how often it appears across the corpus. Back-link required if this page is created.

Bidirectional linking is enforced at lint time. If any of the pages listed above does not carry a back-reference to this page, the lint check fails and flags the broken symmetry.

## Our Research Use

<!-- GUIDANCE
WHAT GOES HERE: How the user is actually USING this theory in their research. Name specific propositions, hypotheses, or framework components.
WHAT DOES NOT: Generic relevance ("this theory is important to our work").
EXAMPLE: "Cited in Proposition 1 of the Agentic AI Governance term paper to ground the claim that agentic AI systems introduce novel agency risks. Also supports Proposition 3 on governance maturity as a moderator. The term paper positions principal-agent theory as the foundational lens, extended by Jarrahi's agentic framing."
-->

Principal-agent theory grounds the theoretical section of the Agentic AI Governance term paper (v2, submitted 2026-05-02). It supports two of the three propositions directly:

- **Proposition 1 (governance maturity reduces incident frequency and severity):** The theoretical warrant is that agentic AI introduces wider information asymmetry and weaker principal monitoring than classical delegation, so mature governance practices (registration, monitoring, override, post-hoc audit) compensate for the expanded agency gap. Jarrahi and Ritala (2025, Table 1) supplies the four-challenge taxonomy; Berente et al. (2021) supplies the inscrutability extension; Eulerich et al. (2024) supplies the empirical consequences when governance is weak.
- **Proposition 3 (shadow AI moderates the governance-risk relationship):** The theoretical warrant is that shadow AI breaks the principal-agent relationship entirely: there is no registered principal, no contract, no monitoring, no override. Eulerich et al. (2024, p. 10) provides the empirical anchor.

The term paper positions principal-agent theory as the foundational lens, with Jarrahi and Ritala (2025) providing the agentic-specific extension. Berente et al. (2021) supplies the sociotechnical complication: principal-agent theory in the AI setting cannot assume the agent is legible to the principal, so classical remedies need adjustment.

Proposition 2 (workflow control rigidity and the inverted-U relationship) draws less directly on principal-agent theory and more on human-automation-interaction research (Haase et al. 2024). See [workflow-control-rigidity](./workflow-control-rigidity.md) for that derivation.

## Cross-Space Applications

<!-- GUIDANCE
WHAT GOES HERE: How this concept applies in spaces OTHER than the current one. Specific use cases per space.
WHY IT MATTERS: This section is what triggers promotion to data/wiki/shared/. When lint sees high cross-space relevance and validated maturity, it proposes promotion.
FORMAT: Subsection per space with concrete use cases.
-->

### DBA (Doctoral Business Administration)

- Dissertation chapters on IT governance cite principal-agent theory as the base framework for any delegation-heavy chapter: AI governance, outsourcing, internal control, board oversight.
- Methodological discussions on measurement validity reference agency-cost literature when operationalizing monitoring effort or contract completeness as constructs.
- Qualifying-exam theory questions on governance almost always touch Jensen and Meckling (1976) and Eisenhardt (1989), so a shared concept page reduces re-derivation across chapters.

### CRO (Corporate Research & Operations)

- Industry cases involving outsourcing contracts, vendor management, and AI vendor selection use principal-agent theory to frame the client-vendor relationship and the risk that vendor incentives diverge from client interests.
- Board oversight cases (audit committee, risk committee, compensation committee) draw on the original Jensen-Meckling framing of shareholders-as-principals and executives-as-agents.
- Cases involving autonomous systems in operations (warehouse robotics, automated trading, algorithmic scheduling) benefit from the agentic-AI extension developed in Jarrahi and Ritala (2025).

### CW (Case Writing)

- Teaching cases on corporate governance scandals (earnings management, related-party transactions, expense fraud) have principal-agent theory as their natural theoretical lens.
- Manager-employee cases on incentive design, monitoring intensity, and delegation scope use the classical frame.
- Cases where the protagonist is a board member or audit partner need the shareholder-executive-auditor three-party extension of principal-agent theory, which warrants its own shared concept page if it appears more than twice.

The cross-space pattern is that this concept has different natural extensions in each space: agentic AI in QNTR, dissertation-theory and measurement in DBA, industry-case applications in CRO, teaching-case applications in CW. The shared page should hold the core theory and the classical references. Each space should maintain a thin annotation page that links to the shared page and adds space-specific extensions.

## Open Questions (Domain-Specific)

<!-- GUIDANCE
WHAT GOES HERE: Questions the corpus raises about principal-agent theory that are not answered yet. Research gaps specific to THIS theory.
DIFFERENT FROM: Our research questions (those live in synthesis pages).
EXAMPLE: "How does principal-agent theory extend to systems where the agent is non-human and partially inscrutable? Jarrahi and Ritala (2025) propose an extension but do not empirically test it."
-->

- How does principal-agent theory extend to agents that are non-human and partially inscrutable? Jarrahi and Ritala (2025) propose the extension but do not empirically test it, and Berente et al. (2021) flag inscrutability as a differentiator without resolving whether it breaks classical remedies.
- When multiple AI agents interact without a human in the loop, who is the principal, and to whom is each agent accountable? Jarrahi and Ritala (2025, p. 9) raise this as multi-agent complexity but stop at the warning.
- Do outcome-based contracts, a classical principal-agent remedy for unobservable effort, work when the agent's outputs are themselves inscrutable? The corpus does not address this directly.
- Can governance maturity be measured as an agency-cost reduction? No paper in the current corpus operationalizes this, which is a construct-validity gap for the term paper's quantitative phase.
- Does the empirical RPA evidence in Eulerich et al. (2024) generalize to agentic AI, where agents learn and act proactively rather than executing fixed rules? This is the central gap the term paper is positioned to address.

## Provenance

<!-- GUIDANCE
Same as source pages: first_seen, last_updated, ingested_by, reviewers.
Additional field for concepts: promotion_status (none | proposed | promoted-to-shared | declined).
-->

- **first_seen:** 2026-05-01, when Berente et al. (2021) was processed in the literature review analysis at `data/summaries/literature_review_7papers_analysis.md`.
- **last_updated:** 2026-05-03 (draft creation).
- **ingested_by:** Hand-authored by Kiro as a gold-standard template ahead of automated ingest. Not produced by a wiki-ingest workflow run.
- **reviewers:** Pending user review (this is a draft template). No second reviewer yet.
- **source artifacts consulted:**
  - `data/summaries/literature_review_7papers_analysis.md` (Paper 1 Berente, Paper 2 Jarrahi, Paper 5 Eulerich sections)
  - `docs/knowledge_base_design.md` (Concept Page schema, Sections "Page Types and Frontmatter" and "Knowledge Maturity States")
- **promotion_status:** proposed. This page is flagged `promotion_candidate: true` in frontmatter and should be promoted to `data/wiki/shared/concepts/principal-agent-theory.md` once it reaches `validated` maturity and at least one cross-space application has been drafted against it.
- **maturity transition criteria (per knowledge_base_design.md):** Currently `working` (three sources contribute, cross-references drafted). Advances to `validated` after user review confirms accuracy against the source papers and resolves the `[NOT YET VERIFIED]` flags in the Origin section.
