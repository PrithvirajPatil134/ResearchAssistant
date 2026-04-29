# Week 3 Homework — Literature Review Workshop
**Topic:** Agentic AI Governance and Its Impact on Enterprise Risk and Business Performance
**Student:** Atul Prashar Patil
**Date:** April 2026

---

## 1. Research Objective(s)

**Primary Research Objective:**
To examine how the maturity of organizational governance mechanisms for agentic AI systems influences enterprise risk exposure, and to identify the extent to which workflow control rigidity mediates this relationship, while accounting for the moderating effect of unsanctioned (shadow) AI agent usage.

**Secondary Research Objective:**
To bridge the gap between the technical governance frameworks proposed in computer science literature and the business-impact evidence established in management/IS literature, by providing the first firm-level empirical study at the intersection of agentic AI governance and quantifiable business outcomes.

**Research Questions:**
- RQ1: How does agentic AI governance maturity affect enterprise AI risk exposure (financial losses, operational incidents, compliance failures)?
- RQ2: Does workflow control rigidity (deterministic constraints on agent behavior) mediate the governance-risk relationship?
- RQ3: Does shadow AI prevalence weaken the effectiveness of governance mechanisms in reducing enterprise risk?

---

## 2. Search Strategy

### 2.1 Databases Used
- Web-based academic search (ResearchGate, arXiv, PubMed, ACM Digital Library, SSRN, Springer, Elsevier ScienceDirect)
- Note: Google Scholar queries are documented below for manual execution; direct programmatic access was not available.

### 2.2 Building Block Strategy (per Prof. Priyanka's Session 2)

| Block | Concept | Keywords & Synonyms |
|-------|---------|-------------------|
| Block 1 (Agentic AI Focus) | Agentic AI / AI Agents | ("agentic AI" OR "AI agents" OR "autonomous AI agents" OR "multi-agent systems" OR "LLM agents") |
| Block 2 (Governance Focus) | Governance / Accountability | ("AI governance" OR "AI accountability" OR "responsible AI" OR "governance framework" OR "AI orchestration" OR "AI oversight") |
| Block 3 (Business Impact Focus) | Enterprise Risk / Financial Impact | ("enterprise risk" OR "financial loss" OR "firm performance" OR "business value" OR "liability" OR "cost of breach" OR "ROI" OR "compliance failure") |

### 2.3 Boolean Search Queries (Building Block Progression)

**Step 3 — Broad (each block separately):**
- Block 1: `("agentic AI" OR "AI agents" OR "autonomous AI agents" OR "multi-agent systems")`
- Block 2: `("AI governance" OR "AI accountability" OR "responsible AI" OR "governance framework")`
- Block 3: `("enterprise risk" OR "financial loss" OR "firm performance" OR "liability" OR "ROI")`

**Step 4 — Moderate (two blocks combined with AND):**
- Block 1 AND Block 2: `("agentic AI" OR "AI agents" OR "autonomous AI agents") AND ("AI governance" OR "AI accountability" OR "responsible AI" OR "governance framework")`
- Block 1 AND Block 3: `("agentic AI" OR "AI agents" OR "autonomous AI agents") AND ("enterprise risk" OR "financial loss" OR "liability" OR "compliance failure")`
- Block 2 AND Block 3: `("AI governance" OR "responsible AI" OR "governance framework") AND ("firm performance" OR "business value" OR "financial loss" OR "ROI")`

**Step 5 — Narrow (all three blocks combined with AND):**
- `("agentic AI" OR "AI agents" OR "autonomous AI agents") AND ("governance" OR "accountability" OR "oversight") AND ("enterprise risk" OR "financial loss" OR "business value" OR "liability")`

### 2.4 Inclusion Criteria
- Published in peer-reviewed journals ranked ABDC A*/A/B, CORE A*/A/B, or JCR Q1/Q2 (Impact Factor ≥ 2.0)
- Conference papers accepted only from top-tier venues (NeurIPS, ICML, ACM FAccT, AIES) for nascent topics
- Industry reports accepted only if widely cited in academic literature (IBM Cost of Data Breach, Gartner surveys)
- Published 2020–2026 (with exceptions for foundational works like Weill & Ross 2004)
- English language only

### 2.5 Exclusion Criteria
- Blogs, white papers from vendors (unless widely cited)
- Predatory or unranked journals
- Papers focusing solely on algorithm-level fairness/bias without organizational governance perspective
- Duplicate versions (conference paper excluded if journal version exists)

---

## 3. Selected Articles (10 Papers)

### Classification: CS/Technical Side (How governance works technically)

| # | Paper | Authors | Year | Journal/Venue | Type |
|---|-------|---------|------|---------------|------|
| 1 | Governing AI Agents | Kolt, N. | 2025 | Notre Dame Law Review (Top 20 US Law Review) | Theoretical |
| 2 | Regulating Advanced Artificial Agents | Cohen, Kolt, Bengio, Hadfield, Russell | 2024 | Science (JIF 44.7) | Theoretical/Policy |
| 3 | Responsible AI Pattern Catalogue | Lu, Zhu, Xu, Whittle, Zowghi, Jacquet | 2024 | ACM Computing Surveys (ABDC A*, JIF 28.0) | Literature Review (MLR) |
| 4 | Lessons from Complex Systems Science for AI Governance | Kolt, Shur-Ofry, Cohen | 2025 | Patterns — Cell Press (JIF 6.7, Q1) | Theoretical |
| 5 | A Review of Trust, Risk, and Security Management in LLM-based Agentic Multi-Agent Systems | Multiple authors | 2025 | arXiv (under review, Horizon Europe funded) | Literature Review |

### Classification: Management/Business Side (What governance does for the business)

| # | Paper | Authors | Year | Journal/Venue | Type |
|---|-------|---------|------|---------------|------|
| 6 | Responsible AI Governance: A Review and Research Framework | Mikalef, Conboy, Lundström, Pateli | 2025 | Information & Management (ABDC A*, JIF 8.2) | Scoping Review + Empirical |
| 7 | AI Capability: Conceptualization, Measurement, and Impact on Firm Performance | Mikalef, Krogstie, Pappas, Krogstie | 2021 | Information & Management (ABDC A*, JIF 8.2) | Empirical (PLS-SEM) |
| 8 | AI in IS Research: A Systematic Literature Review and Research Agenda | Enholm, Papagiannidis, Mikalef, Krogstie | 2022 | Intl. Journal of Information Management (ABDC A*, JIF 27.0) | Systematic Review |
| 9 | ESG and Corporate Financial Performance: Aggregated Evidence from 2000+ Studies | Friede, Busch, Bassen | 2015 | Journal of Sustainable Finance & Investment (ABDC A) | Meta-Analysis |
| 10 | IT Governance: How Top Performers Manage IT Decision Rights for Superior Results | Weill, Ross | 2004 | Harvard Business School Press (5000+ citations) | Foundational Empirical |

---

## 4. Data Classification

| Paper | Domain | Theory | IV | Mediator/Moderator | DV | Method | Key Quantifiable Finding |
|-------|--------|--------|----|--------------------|-----|--------|------------------------|
| Kolt (2025) | Law/CS | Agency Theory | AI Agent Design | — | Governance Effectiveness | Theoretical | — (proposes principles) |
| Cohen et al. (2024) | CS/Policy | Safety Theory | Agent Capability | — | Regulatory Need | Theoretical | — (argues untestability) |
| Lu et al. (2024) | CS/SE | Pattern Theory | 35 RAI Patterns | — | Responsible AI | MLR | — (unvalidated patterns) |
| Kolt et al. (2025) | Law/Physics | Complex Systems | AI System Properties | — | Governance Design | Theoretical | — (proposes desiderata) |
| TRiSM Review (2025) | CS/Security | TRiSM Framework | Trust/Risk/Security | — | Agent Safety | Review | — (identifies org gaps) |
| Mikalef et al. (2025) | IS/Mgmt | Governance Theory | RAI Governance Practices | Knowledge Mgmt Capabilities | Competitive Performance | PLS-SEM (n=144) | Governance → performance (positive, p<0.05) |
| Mikalef et al. (2021) | IS/Mgmt | RBV, Dynamic Capabilities | AI Capability | Organizational Creativity | Firm Performance | PLS-SEM | AI capability → creativity → performance |
| Enholm et al. (2022) | IS/Mgmt | Multiple | AI in IS (broad mapping) | — | Research Agenda | SLR | Dark side understudied |
| Friede et al. (2015) | Finance | Stakeholder, Agency | ESG (incl. Governance) | — | Financial Performance | Meta-analysis (2200 studies) | 90% show governance → positive CFP |
| Weill & Ross (2004) | IS/Mgmt | Decision Rights | IT Governance Maturity | — | IT ROI, Profitability | Empirical (250+ firms) | 40% higher IT returns; 20% higher profits |

---

## 5. Concept Map / Conceptual Framework

```
                    CS/TECHNICAL SIDE                          MANAGEMENT/BUSINESS SIDE
                    ════════════════                           ═══════════════════════

    ┌──────────────────────┐                        ┌──────────────────────────┐
    │ Agentic AI Governance│                        │ IT Governance → IT Value │
    │ Principles           │                        │ (Weill & Ross, 2004)     │
    │ (Kolt, 2025)         │                        │ 40% higher returns       │
    │ • Inclusivity        │                        └────────────┬─────────────┘
    │ • Visibility         │                                     │
    │ • Liability          │                                     │ Extended by
    └──────────┬───────────┘                                     ▼
               │                                    ┌──────────────────────────┐
               │ Operationalized                    │ AI Governance →          │
               │ through                            │ Competitive Performance  │
               ▼                                    │ (Mikalef et al., 2025)   │
    ┌──────────────────────┐                        │ General AI only          │
    │ 35 RAI Patterns      │                        └────────────┬─────────────┘
    │ (Lu et al., 2024)    │                                     │
    │ • Kill switch        │                                     │ GAP: Not tested
    │ • Ethical sandbox    │                                     │ for agentic AI
    │ • Audit trail        │                                     │
    │ • Ethical blackbox   │                                     ▼
    │ NOT validated        │                        ┌──────────────────────────┐
    └──────────┬───────────┘                        │ ESG Governance →         │
               │                                    │ Financial Performance    │
               │ Risk context                       │ (Friede et al., 2015)    │
               │ from                               │ 2200 studies: 90%        │
               ▼                                    │ positive relationship    │
    ┌──────────────────────┐                        └──────────────────────────┘
    │ Agentic AI Risks     │
    │ • Cascading failures │                                 THE GAP
    │   (Kolt et al., 2025)│                        ╔══════════════════════════╗
    │ • Untestable agents  │                        ║                          ║
    │   (Cohen et al.,2024)│        ──────────►     ║  OUR RESEARCH SITS HERE  ║
    │ • Org factors missing│                        ║                          ║
    │   (TRiSM Review,2025)│       ◄──────────     ║  Agentic AI Governance   ║
    └──────────────────────┘                        ║  → Enterprise Risk       ║
                                                    ║  → Business Outcomes     ║
                                                    ║  (Empirical, firm-level) ║
                                                    ╚══════════════════════════╝

    PROPOSED MODEL:

    ┌─────────────────┐         ┌──────────────┐         ┌──────────────────┐
    │ Agentic AI      │  H1(+)  │ Workflow     │  H2(-)  │ Enterprise AI    │
    │ Governance      │────────►│ Control      │────────►│ Risk Exposure    │
    │ Maturity (IV)   │         │ Rigidity     │         │ (DV)             │
    └─────────────────┘         │ (Mediator)   │         │ • Financial loss │
                                └──────────────┘         │ • Incidents      │
                                                         │ • Compliance     │
                                        ▲                └────────┬─────────┘
                                        │                         │
                                ┌───────┴────────┐               │
                                │ Shadow AI      │               │
                                │ Prevalence     │ H4 (weakens   │
                                │ (Moderator)    │  H2 effect)   │
                                └────────────────┘               │
```

---

## 6. Literature Review Synthesis (~300 words)

Two research communities are talking past each other on AI governance. Computer science researchers have built the technical blueprints. Management researchers have proved governance pays off financially. Neither side has connected the two for agentic AI.

On the technical side, Kolt (2025) grounds AI agent governance in agency theory, proposing three principles: inclusivity, visibility, and liability. Lu et al. (2024) go further, cataloguing 35 responsible AI patterns across governance, process, and product levels, from kill switches to ethical sandboxes. But the authors themselves admit these patterns remain unvalidated in real organizations. Cohen et al. (2024) raise the stakes in *Science*, arguing that sufficiently capable autonomous agents cannot be reliably safety-tested at all. Kolt, Shur-Ofry, and Cohen (2025) apply complex systems theory to show why: AI systems scale nonlinearly, fail in cascades, and resist prediction. A 2025 review of trust, risk, and security in agentic multi-agent systems puts it bluntly: organizational and human factors are the weak link, and most governance controls have only been tested in labs.

The management side tells a different story. Governance works, and the numbers back it up. Weill and Ross (2004) found that top IT governance performers earn 40% higher returns on IT investments. Friede, Busch, and Bassen (2015) aggregated over 2,200 empirical studies and found 90% show a positive link between governance and financial performance. Mikalef et al. (2025) extended this into AI territory, showing that responsible AI governance practices drive competitive performance through knowledge management. Their sample, though, covers general AI in Nordic firms. Agentic AI is absent. Enholm et al. (2022) flag this directly: the "dark side" of AI, the risks, the failures, the costs, is barely studied in information systems research.

The gap sits at the intersection. Technical governance frameworks for agentic AI exist. The business case for governance is proven for traditional IT and general AI. What is missing is an empirical, firm-level study connecting the two: does agentic AI governance maturity actually reduce enterprise risk exposure in measurable terms?
