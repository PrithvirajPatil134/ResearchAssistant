---
title: "Managing Artificial Intelligence"
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
  - "Berente, N."
  - "Gu, B."
  - "Recker, J."
  - "Santhanam, R."
year: 2021
venue: "MIS Quarterly"
volume: "45(3)"
pages: "1433-1450"
tags: [mis-quarterly, ai-governance, organizational-routines, autonomy, inscrutability, sociotechnical]
---

## Summary

Special issue editorial/introduction for MIS Quarterly that defines AI as "the frontier of computational advancements that references human intelligence in addressing ever more complex decision-making problems" (p. 1434). Argues that managing AI requires attending to three interrelated facets: autonomy, learning, and inscrutability. Frames AI management as a continuous sociotechnical process rather than a discrete technology adoption.

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 1 §Core Argument]

## Key Arguments

### Three Facets of AI Management

AI is defined through three facets (p. 1437, Table 1):
- **Autonomy**: acting without human intervention
- **Learning**: improving through data and experience
- **Inscrutability**: being unintelligible to specific audiences

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 1 §Key Findings]

### Managing Autonomy

Navigating the tension between automation and augmentation. As AI becomes more autonomous, "humans risk losing their own autonomy and effectiveness" (pp. 1439-1440). The discussion of delegation to autonomous agents (p. 1439, referencing Baird and Maruping 2021) connects to principal-agent theory.

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 1 §Key Findings]

### Managing Inscrutability

Four dimensions: opacity, transparency, explainability, and interpretability (pp. 1441-1442). These map directly onto governance mechanisms for oversight of AI systems.

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 1 §Key Findings]

### Managing Learning

AI that "feeds on data beyond organizational boundaries" raises privacy, trust, and governance issues (p. 1440).

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 1 §Key Findings]

### Board-Level Governance

"Boards must contain members who can scrutinize AI technologies to assess strategic impact" (p. 1442, referencing Li et al. 2021).

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 1 §Key Findings]

### Ethical Dimensions

Fairness, bias, privacy, and accountability cut across all three facets (pp. 1443-1444).

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 1 §Key Findings]

## Methodology

Conceptual synthesis: consolidates insights from seven papers in the special issue combined with literature review and conceptual framing. No empirical data collection by the authors themselves.

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 1 §Methodology]

## Relevance to Research

- **RQ1 (governance practices)**: The autonomy-learning-inscrutability framework provides conceptual vocabulary for categorizing governance practices. The inscrutability dimensions (opacity, transparency, explainability, interpretability) map directly onto governance mechanisms.
- **P1 (governance maturity reduces incidents)**: The argument that managers who understand and address the three facets "can avoid negative consequences" (p. 1434) supports governance maturity logic.
- **P2 (workflow control rigidity)**: The automation-augmentation tension speaks directly to control rigidity.
- **Theoretical lineage**: Framing of AI as requiring sociotechnical management aligns with IT governance-to-business-value lineage (Weill and Ross 2004).

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 1 §Direct Relevance]

## Limitations

- Does not provide empirical evidence on governance practices or their outcomes.
- Does not measure risk outcomes (incident frequency, financial loss, compliance failure).
- Does not address agentic AI specifically (focuses on AI broadly).
- Does not test propositions about governance maturity, control rigidity, or shadow AI.
- Does not use quantitative methods or propose measurable constructs.

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 1 §What It Does NOT Do]

## Key Quotes

- "The frontier of computational advancements that references human intelligence in addressing ever more complex decision-making problems." (p. 1434, definition of AI)
- "Boards must contain members who can scrutinize AI technologies to assess strategic impact." (p. 1442)

[Source: data/summaries/literature_review_7papers_analysis.md, Paper 1]

<!-- Merged 2026-07-27 from the legacy QNTR wiki copy during the Kiro→CC tree reconciliation (Wave 5). These sections were unique to the legacy validated copy. -->

## Open Questions


The paper opens several threads that its conceptual format cannot close.

How do specific governance practices map onto the three facets? The paper names the facets and argues that each must be managed, but does not enumerate practices. This is the gap the term paper addresses in RQ1.

How does the framework extend to agentic systems where multiple autonomous agents interact? Inscrutability at the single-model level differs from emergent inscrutability in multi-agent settings. Relevant to [syntheses/rpa-to-agentic-ai-gap](../syntheses/rpa-to-agentic-ai-gap.md) [CREATE SYNTHESIS PAGE].

What is the right boundary between human and AI autonomy for a given task? The automation-augmentation tension (pp. 1439-1440) is stated as a tradeoff, but the paper does not specify how managers should locate the boundary in practice. This connects directly to P2 (workflow control rigidity).

What organizational structures (roles, committees, reporting lines) support effective AI management? The board-member point (p. 1442) is made in passing. A fuller structural treatment is needed and is not in this paper.

## Tensions with Other Sources


Most other papers in the corpus are complementary rather than contradictory, but three genuine tensions are worth flagging.

**Scope of the governance problem: Berente et al. (2021) vs. Taeihagh (2025).** Berente frames AI management as a three-facet conceptual problem. Taeihagh (2025, pp. 3-5, Table 1) frames it as a seven-category risk taxonomy with eight governance strategy areas (Table 2, pp. 10-11). These taxonomies do not map cleanly onto each other. A comparison page would be useful. See [comparisons/berente-vs-taeihagh-risk-taxonomies](../comparisons/berente-vs-taeihagh-risk-taxonomies.md) [CREATE COMPARISON PAGE].

**Unit of analysis: Berente et al. (2021) vs. Eulerich et al. (2024).** Berente works at the level of managerial principles and sociotechnical framing. Eulerich et al. (2024, pp. 7-14) work at the level of specific governance failures in a single Fortune 500 firm, where unknown bots, bad data, and centralized-versus-decentralized control create concrete incidents. The tension is not a contradiction. It is a level-of-analysis gap. Berente explains why governance matters. Eulerich shows what breaks when it fails.

**Theoretical lens: Berente et al. (2021) vs. Jarrahi and Ritala (2025).** Berente uses a sociotechnical framing with a light engagement with delegation. Jarrahi and Ritala (2025, p. 3) apply principal-agent theory as a primary lens. The two framings are not incompatible, but they point toward different governance instruments. Sociotechnical framing emphasizes process redesign and human-AI configuration. Principal-agent framing emphasizes goal alignment, monitoring, and contracting. The term paper uses principal-agent theory as the dominant lens and Berente et al. as the conceptual backdrop. That choice should be stated explicitly when both are cited.

## Cross-Space Promotion Notes


This page is a strong promotion candidate for `data/wiki/shared/sources/`.

**DBA.** Any dissertation chapter on AI governance will need Berente et al. (2021) as a foundational citation. The three-facet framework is now a standard conceptual reference in IS research on AI management. Promoting the page prevents DBA work from re-ingesting the PDF and losing the cross-references already built here.

**CRO.** Industry case analyses that involve AI deployment (autonomous underwriting, algorithmic pricing, automated claims handling) benefit from the autonomy-learning-inscrutability lens when categorizing risks. The framework translates cleanly from academic framing to case-study diagnosis.

**QNTR.** This is the originating space. Promotion does not remove the page from QNTR; it moves the canonical copy to the shared directory with a redirect from QNTR. The term paper pipeline continues to resolve through QNTR indexing.

Recommendation: promote at the next lint cycle. Suggested target path: `data/wiki/shared/sources/berente-2021-managing-ai.md`.

