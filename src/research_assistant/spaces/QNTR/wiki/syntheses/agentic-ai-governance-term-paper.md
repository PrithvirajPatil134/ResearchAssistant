---
type: deliverable_synthesis
title: "Agentic AI Governance Term Paper"
maturity: working
tags: [term-paper, agentic-ai, governance, enterprise-risk, qntr]
schema_version: "1.0"
created: 2026-05-07
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [term_paper, research_paper, thesis]
target_deliverable: "Agentic AI Governance and Its Impact on Enterprise Risk and Business Performance"
current_version: "v2"
version_history:
  - version: "v1"
    completed: 2026-04-15
    changes: "Initial draft with literature review and conceptual framework"
  - version: "v2"
    completed: 2026-05-02
    changes: "Simplified framework to three propositions, integrated Jarrahi-Ritala 2025 and Berente 2021, addressed Suresh feedback on synthesis and gap justification"
draws_from:
  QNTR:
    - wiki/entities/prof-prashar
    - wiki/entities/prof-priyanka-suresh
    - wiki/sources/deng-2025-ai-agents-security-survey
target_path: src/research_assistant/spaces/QNTR/wiki/syntheses/agentic-ai-governance-term-paper.md
---

## Current State

v2 submitted to Prof. Prashar on May 2, 2026. Feedback received May 3, 2026. Term paper grade evaluation pending separately. The paper is also being developed as a longer research programme (DBA thesis direction).
[Source: `communication/email_prof_prashar_submission_date_20260502.md`; `feedback/response_prof_prashar_termpaper_review_20260505.md`]

## Core Research Question

Do firms that adopt more mature governance practices for agentic AI experience fewer reportable incidents, lower financial losses, and fewer compliance failures?
[Source: `communication/email_prof_prashar_submission_date_20260502.md`, description of v2 scope]

## Theoretical Anchors

1. Principal-agent theory applied to AI agents (Kolt, 2025, Notre Dame Law Review)
2. IT governance-to-business-value lineage (Weill and Ross, 2004)
3. Responsible AI governance frameworks (Mikalef et al., 2025, Information and Management)

[Source: `spaces/DBA/communication/email_dr_trebucq_research_topic_20260427.md`, lines 15-16]

_Framing reference (not a model anchor):_ Dafoe (2018), "AI Governance: A Research Agenda" (Centre for the Governance of AI, University of Oxford), supplies the field-level definition of AI governance and the AI-safety-vs-AI-governance distinction used to frame the literature review's opening. It operates at the societal/global level and does not inform the enterprise-level IV-to-DV design; it is cited for scope-setting and for the neglectedness framing of the gap (Dafoe's important/tractable/neglected heuristic, p.13). Provenance: provided by Dr. Trebucq (DBA), May 1 2026, per the correction note below.

[Source: QNTR/wiki/sources/dafoe-2018-ai-governance-research-agenda.md, p.5, p.6, p.13]

_Available alternative lens (not an adopted anchor):_ Gahnberg (2021, *Policy and Society*) offers an alternative agency lens the paper could draw on. It frames the governance object as the *material agency* of artificial agents and structures governance as rules over four agent properties (performance measure, environment, actions, percepts). It is complementary to, not a substitute for, the principal-agent anchor (Kolt 2025). Whether to adopt this framing is a decision for the author; it is recorded here as available literature, not as part of the chosen theoretical model.

[Source: QNTR/wiki/sources/gahnberg-2021-framing-governance-artificial-agency.md, p.2, p.7, p.8]

## Evidence Base for the Dependent Variable

Deng et al. (2025), "AI Agents Under Threat" (ACM Computing Surveys 57(7), Article 182), supplies the technical catalog of AI-agent failure modes that the dependent variable (reportable incidents, financial losses, compliance failures) is meant to capture. Their six-class threat taxonomy (perception, brain, action, agent2environment, agent2agent, agent2memory) provides candidate incident categories, and the survey documents quantified and real-world harms usable as enterprise-risk exhibits: multi-million-dollar losses from imitation attacks via prompt injection, the Character.AI chatbot-suicide case, the Morris II self-replicating worm, Meta's Cicero deception, and a warning about automated trading agents colluding at scale.

[Source: `wiki/sources/deng-2025-ai-agents-security-survey.md`; underlying pages `[source_path, p.8, p.10, p.21-24]`]

## Method (as proposed in v2)

Exploratory sequential mixed-methods: Phase 1 qualitative (build governance constructs from public discourse and practitioner data), Phase 2 quantitative (binary logistic regression on firm-level survey).
[Source: `spaces/DBA/communication/email_dr_trebucq_research_topic_20260427.md`, line 16]

## Version History Detail

### v1 (completed ~April 15, 2026)

Initial draft with three-stream literature review and conceptual framework. Submitted to Prof. Priyanka Suresh for literature review feedback.
[CONJECTURE: date approximated from the v2 submission timeline; no source file pins exact v1 date]

### v2 (submitted May 2, 2026)

Changes from v1:
- Addressed Prof. Suresh's feedback: stronger synthesis across the three literature streams, clearer gap justification, tighter dependent variable operationalisation.
- Integrated two additional papers: Jarrahi and Ritala (2025) in California Management Review; Berente et al. (2021) in MIS Quarterly.
- Simplified conceptual framework to three propositions.

[Source: `communication/email_prof_prashar_submission_date_20260502.md`, para 2]

## Feedback Received

### Prof. Priyanka Suresh (pre-v2, ~late April 2026)

- Stronger synthesis across streams
- Clearer gap justification
- Tighter DV operationalisation

[Source: `communication/email_prof_prashar_submission_date_20260502.md`, para 2, referencing Suresh feedback]

### Prof. Prashar (May 3, 2026, on v2)

Key revision areas identified:

1. **Argumentation**: soften direct negatives; position via what past studies could improve; add gap table (Han et al. 2017 Table 1 style).
2. **Market evidence**: add evidence from McKinsey, Deloitte and similar reports.
3. **Literature review**: should be 20-30% of thesis write-up.
4. **Method**: Phase 1 should explicitly be a literature review step (SLR/narrative/meta-analysis). Construct measures likely do not exist; developing them is the qualitative study's key aim.
5. **Formative construct**: "Agentic AI governance maturity" as IV is likely formative, requiring different analysis techniques (not standard CB-SEM/regression).
6. **Contribution structure**: must start with "Discussion" (compare with past work, reason contradictions), then Theoretical Contribution, then Managerial Implications.
7. **Speed**: "anything related to AI is progressing with the speed of light, you must move forward faster."

[Source: `feedback/response_prof_prashar_termpaper_review_20260505.md`, all sections]

### Attachments received with Prashar feedback

- Han et al. (2017) — Journal of Marketing (gap table exemplar)
- Diamantopoulos (2011) — MIS Quarterly (formative measures in CB-SEM)
- Diamantopoulos and Siguaw (2006) — formative vs reflective indicators
- Hildebrandt and Temme (2006) — problematic SEM models

[Source: `feedback/response_prof_prashar_termpaper_review_20260505.md`, attachments field]
[NOTE: GovAI Research Agenda (Dafoe 2018) was previously listed here in error. That PDF was provided by Dr. Trebucq (DBA space, May 1 2026), not Prashar. Corrected 2026-05-09.]

## Pending Revision Areas (for v3)

| Area | Action Required | Priority |
|------|----------------|----------|
| Gap table | Build Han et al. 2017 Table 1 style comparison | High |
| Market evidence | Find McKinsey/Deloitte reports on AI governance ROI | High |
| Formative construct | Read Diamantopoulos refs; decide PLS-SEM vs CB-SEM | High |
| Contribution restructure | Discussion first, then theoretical/managerial | Medium |
| Tone softening | Remove direct negatives in positioning | Medium |
| Lit review expansion | Scale to 20-30% for thesis version | Low (term paper OK) |

## Related Entities

- [Prof. Prashar](../entities/prof-prashar.md): term paper advisor, provided May 3 feedback
- [Prof. Priyanka Suresh](../entities/prof-priyanka-suresh.md): literature review feedback, pre-v2
- [Dr. Trebucq](../../DBA/wiki/entities/dr-trebucq.md): potential thesis supervisor, separate feedback track

## File Locations

- v2 markdown: `spaces/QNTR/output/QNTR_TermPaper_Agentic_AI_Governance_v2.md`
- v2 docx: `spaces/QNTR/output/QNTR_TermPaper_Agentic_AI_Governance_v2.docx`

---

<!-- OBSIDIAN-LINKS:START (auto-generated by scripts/obsidian-graph-linker.py, do not edit by hand) -->
## Related
- **Draws from**: [[src/research_assistant/spaces/QNTR/wiki/entities/prof-prashar|prof-prashar]] , [[src/research_assistant/spaces/QNTR/wiki/entities/prof-priyanka-suresh|prof-priyanka-suresh]]
<!-- OBSIDIAN-LINKS:END -->
