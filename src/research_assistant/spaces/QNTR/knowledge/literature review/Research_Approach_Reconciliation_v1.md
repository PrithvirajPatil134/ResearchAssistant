# Research Approach Reconciliation: Agentic AI Governance and Business Impact

**Author:** Prithviraj Patil
**Date:** April 2026
**Status:** Working document, v1
**Target venue:** Business Process Management Journal (BPMJ), building on Vu et al. (2025)

---

## 1. What we reconciled

The Week 3 submission framed the research as a positivist hypothesis-testing study with IV, mediator, moderator, and DV, closed with H1, H2, H3 and a PLS-SEM design in mind. After reading the management-side and CS-side papers in the Agentic Governance reading list and cross-checking against the current peer-reviewed state of the field, the framing needs to shift.

The reason is substantive, not philosophical. The literature says:

- Mikalef and Gupta (2021) built their AI Capability constructs through qualitative practitioner interviews before running PLS-SEM. Even the landmark quantitative paper in this space started qualitatively.
- Papagiannidis, Mikalef, and Conboy (2025) produced a scoping review with a conceptual framework for responsible AI governance and explicitly called for extending to specific AI types and studying what happens when governance fails.
- Lu et al. (2024) catalogued 35 responsible AI patterns but wrote in their own future work section that empirical validation in organizations is missing.
- Kolt (2025), Cohen et al. (2024), and Gahnberg (2021) are theoretical or legal, with no empirical firm-level data.
- Vu et al. (2025) produced the first empirical study on agent governance in business processes using qualitative semi-structured interviews with 22 practitioners. They built six governance recommendations and four BPM alignment actions.

No one has yet combined qualitative discovery of constructs with quantitative testing of their business impact for agentic AI specifically. That is the seam to publish in.

## 2. Chosen approach: single-paper mixed-methods sequential exploratory design

The research will be a single paper with two integrated phases:

**Phase 1 (qualitative, theory-building):** Thematic analysis of publicly available discourse and, where feasible, a small set of targeted practitioner interviews. Output: a set of propositions connecting agentic AI governance practices to enterprise risk and business outcomes.

**Phase 2 (quantitative, testing):** Logistic regression operationalizing the Phase 1 propositions. Output: statistical evidence of which governance practices predict measurable firm-level outcomes.

This is well-precedented. The design follows Creswell and Plano Clark (2018) for exploratory sequential mixed methods and uses Venkatesh, Brown, and Bala (2013, MIS Quarterly) as the methodological anchor for mixed methods in IS research. BPMJ publishes both qualitative and mixed-methods papers.

## 3. Why this works for the topic

- **Matches the state of the literature.** The field is in a theory-building phase. A pure PLS-SEM study would assume validated instruments that do not yet exist.
- **Uses available data sources.** Public discourse (podcast transcripts, keynote talks, conference presentations, published interviews, 10-K disclosures) is accessible without institutional gatekeeping. Targeted interviews can supplement.
- **Produces two contributions in one paper.** A conceptual framework with propositions, plus an initial empirical test of those propositions.
- **Extends a paper already published in the target venue.** Vu et al. (2025) sit in the BPM community. This paper picks up where they left off by moving from perceptions to measurable outcomes.

## 4. Philosophical stance

The paper is pragmatic with a qualitative-first orientation. Phase 1 is interpretive and inductive. Phase 2 is post-positivist and deductive on the propositions generated in Phase 1. The two phases draw on different philosophical commitments, which is the defining feature of mixed-methods research. The paper must be explicit about this and cite Creswell and Plano Clark as the methodological authority.

## 5. Paper structure (target BPMJ)

1. **Introduction.** Motivation, research questions, gap, contribution. Position against Vu et al. (2025) and Papagiannidis et al. (2025).
2. **Theoretical background.** Principal-agent theory (Kolt 2025), Responsible AI governance constructs (Papagiannidis et al. 2025), IT governance-to-business-value lineage (Weill and Ross 2004; Mikalef and Gupta 2021). Frame the gap: no study links agentic AI governance practices to measurable firm-level risk outcomes.
3. **Methodology.**
   - 3.1 Research design: exploratory sequential mixed-methods (Creswell and Plano Clark 2018)
   - 3.2 Phase 1: qualitative data sources, coding approach, trustworthiness criteria
   - 3.3 Phase 2: survey instrument derived from Phase 1, sampling frame, logistic regression specification
4. **Findings.**
   - 4.1 Phase 1 themes and propositions P1, P2, P3
   - 4.2 Phase 2 descriptive statistics and logistic regression results (odds ratios, marginal effects, goodness-of-fit)
5. **Discussion.** Integrate Phase 1 themes with Phase 2 statistical results. Explain which propositions were supported and why.
6. **Implications.** Theory, practice, policy.
7. **Limitations and future research.** Sample size, selection bias in public discourse, cross-sectional design.
8. **Conclusion.**
9. **References.**
10. **Appendices.** Interview protocol, coding scheme, survey instrument.

## 6. Phase 1 detailed plan

**Objective:** Identify governance practices, risk categories, and contextual factors relevant to agentic AI in enterprise settings. Produce propositions.

**Data sources:**
- Publicly available executive discourse: earnings calls, keynote talks, podcast transcripts, published interviews with leaders at Anthropic, OpenAI, Microsoft, Google DeepMind, Salesforce, IBM, NVIDIA, Accenture, Deloitte, McKinsey
- Regulatory disclosures: 10-K risk factors mentioning AI, 8-K incident disclosures, SEC filings
- Industry reports: Gartner, Forrester, McKinsey State of AI, Wharton AI Adoption Report
- Published articles in governance and policy forums: Kolt, Bengio, Hinton, Mikalef
- Optional: 5-10 targeted anonymous practitioner interviews with CISOs, AI governance leads, or risk officers if access is available

**Method:** Thematic analysis (Braun and Clarke 2006) with open and axial coding. Inter-rater reliability with a second coder on a subset. Document analysis protocol from Bowen (2009) for filings and reports.

**Trustworthiness:** Credibility through triangulation across source types. Transferability through thick description. Dependability through audit trail. Confirmability through reflexivity notes.

**Output:** Three to five propositions. Example form:

> P1: Firms with higher agentic AI governance maturity experience fewer reportable AI incidents than firms with lower maturity.
> P2: The effect of governance maturity on incident frequency is moderated by shadow AI prevalence.
> P3: Firms with formal human-in-the-loop controls report lower financial loss per incident than firms without.

## 7. Phase 2 detailed plan

**Objective:** Test the Phase 1 propositions quantitatively on a firm-level sample.

**Design:** Cross-sectional firm-level survey.

**Unit of analysis:** Firm.

**Respondent:** Senior IT, risk, governance, or compliance officer (one per firm).

**Sample target:** 100 to 200 firms. Drawn from industry panels, professional networks, or a targeted LinkedIn-based approach.

**Dependent variable (binary):** One of:
- "Has your firm experienced a reportable agentic AI incident in the last 12 months?" (Y/N)
- "Does your firm have a formal agentic AI governance function?" (Y/N)
- "Has agentic AI use contributed to a financial loss or operational incident at your firm?" (Y/N)

**Independent variables (derived from Phase 1 themes):**
- Governance maturity index (count of adopted practices)
- Human-in-the-loop control presence
- Shadow AI prevalence (estimated percentage)
- Industry (categorical)
- Firm size (log revenue or log employees)
- Agent deployment depth (number of agentic workflows in production)
- Existing IT governance maturity (from validated IT governance scales, Weill and Ross)

**Analysis:** Binary logistic regression. Report odds ratios, Wald chi-square, pseudo-R squared (McFadden, Nagelkerke), Hosmer-Lemeshow goodness-of-fit, classification accuracy. Test interaction between governance maturity and shadow AI prevalence to address P2.

**Validation:** Multicollinearity check (VIF), outlier diagnostics (hat values, Cook's distance), sensitivity analysis on sample composition.

## 8. Publication plan

**Primary target:** Business Process Management Journal. Emerald. Scopus Q1. ABDC A. Publishes both qualitative and mixed-methods BPM research. Vu et al. (2025) positions the topic as BPMJ-relevant.

**Secondary targets:**
- Information and Management (ABDC A*, JIF 8.2). Mikalef's home journal.
- Information Systems Frontiers (ABDC A, JIF 8.3). Publishes mixed methods with PLS-SEM and logistic regression precedents.
- Journal of the Association for Information Systems. Broader IS scope.

## 9. Structural differences between positivist and interpretive papers (reference)

Both paradigms share Introduction, Literature Review, Methodology, Findings, Discussion, Implications, Limitations, and References sections. The differences sit inside those sections.

| Section | Positivist | Interpretive |
|---|---|---|
| Literature Review | Builds to hypotheses with expected directions | Builds to research questions or propositions without directional commitment |
| Theory | Named theory with defined constructs, operationalized and measured | Theory as lens or emerging from data |
| Model diagram | Box-and-arrow model with labeled hypotheses | Conceptual framework, often without arrows |
| Methodology | Sampling, instrument design, scale validation, statistical technique | Case selection, interview protocol, coding approach, trustworthiness |
| Equations | Regression and structural models | Rare |
| Findings | Tables of descriptive statistics, model fit, path coefficients, hypothesis tests | Narrative by theme with verbatim quotes |
| Validity language | Internal, external, construct, reliability, objectivity | Credibility, transferability, dependability, confirmability |
| Generalization | Statistical to population | Analytical to theory |

For a mixed-methods paper, both styles appear: Phase 1 follows the interpretive column, Phase 2 follows the positivist column, and the overall paper uses Creswell and Plano Clark (2018) as the bridging methodology citation.

## 10. Immediate next steps

1. **Rewrite the research questions** to match the mixed-methods framing. Move from "does X cause Y" to "what governance practices are used in agentic AI deployments (Phase 1), and do these practices predict firm-level risk outcomes (Phase 2)".
2. **Build the Phase 1 corpus.** Identify 20 to 30 public-discourse sources. Include earnings call transcripts, podcast transcripts, keynote talks, executive articles, and 10-K disclosures. Log sources in the Literature_Search_Log.xlsx.
3. **Draft the thematic coding scheme.** Use the six recommendations from Vu et al. (2025) and the seven responsible-AI principles from Papagiannidis et al. (2025) as starting codes.
4. **Identify 5 to 10 targeted practitioner interviewees.** CISOs, AI governance leads, compliance officers. Anonymous interviews with IRB or institutional approval.
5. **Draft the Phase 2 survey instrument** based on Phase 1 themes. Pilot with 10 respondents for reliability.
6. **Revise the Week 3 deck** to reflect the mixed-methods design. Replace the H1-H3 structure with propositions P1-P3 and a two-phase methodology flow diagram.
7. **Draft the BPMJ cover letter** positioning the paper against Vu et al. (2025) and Papagiannidis et al. (2025).

## 11. References (working list)

- Bowen, G. A. (2009). Document analysis as a qualitative research method. *Qualitative Research Journal*, 9(2), 27-40.
- Braun, V., and Clarke, V. (2006). Using thematic analysis in psychology. *Qualitative Research in Psychology*, 3(2), 77-101.
- Creswell, J. W., and Plano Clark, V. L. (2018). *Designing and Conducting Mixed Methods Research* (3rd ed.). Sage.
- Guba, E. G., and Lincoln, Y. S. (1994). Competing paradigms in qualitative research. In *Handbook of Qualitative Research*.
- Kolt, N. (2025). Governing AI agents. *Notre Dame Law Review*.
- Lu, Q., Zhu, L., Xu, X., Whittle, J., Zowghi, D., and Jacquet, A. (2024). Responsible AI pattern catalogue. *ACM Computing Surveys*.
- Mikalef, P., and Gupta, M. (2021). Artificial intelligence capability. *Information and Management*, 58(3), 103434.
- Papagiannidis, E., Mikalef, P., and Conboy, K. (2025). Responsible artificial intelligence governance: A review and research framework. *Journal of Strategic Information Systems*, 34, 101885.
- Venkatesh, V., Brown, S. A., and Bala, H. (2013). Bridging the qualitative-quantitative divide: Guidelines for conducting mixed methods research in information systems. *MIS Quarterly*, 37(1), 21-54.
- Vu, H., Revoredo, K., Leopold, H., and Mendling, J. (2025). Agentic business process management: Practitioner perspectives on agent governance in business processes. arXiv:2504.03693.
- Weill, P., and Ross, J. W. (2004). *IT Governance: How Top Performers Manage IT Decision Rights for Superior Results*. Harvard Business School Press.

---

*End of v1. Update as the Phase 1 corpus, coding scheme, and survey instrument take shape.*
