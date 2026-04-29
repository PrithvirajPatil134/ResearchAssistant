# Week 3 Homework — Feedback & Iteration Notes (v2)

## Feedback Received

1. Search blocks need proper Boolean structure: AND between blocks, OR within blocks, parentheses throughout
2. Focus is on agentic AI specifically — not generic AI. Agents take actions with real financial consequences
3. Need peer-reviewed journal papers or top conference papers (ABDC/CORE/JCR quality rings), not industry reports
4. Need empirical papers showing how agents cause real costs/losses AND how governance influences business capital
5. Literature survey papers in our scope would validate the direction with peer-reviewed authority
6. The "gap" can't just be "no empirical study exists" — need to show what the business/management side has already established and where it stops
7. Qualitative research is to be avoided if possible. Need quantitative empirical foundation papers to steer the research in a quantitative direction

---

## Corrected Search Blocks (Boolean Structure)

### Block 1 — Agentic AI Focus
```
("agentic AI" OR "AI agents" OR "autonomous AI agents" OR "multi-agent systems" OR "LLM agents" OR "intelligent agents")
```

### Block 2 — Governance / Accountability Focus
```
("AI governance" OR "AI accountability" OR "responsible AI" OR "governance framework" OR "AI oversight" OR "AI orchestration" OR "AI audit")
```

### Block 3 — Business Impact / Financial Consequences Focus
```
("enterprise risk" OR "financial loss" OR "firm performance" OR "business value" OR "liability" OR "cost of breach" OR "ROI" OR "compliance failure" OR "operational risk" OR "capital loss")
```

### Search Progression (Building Block Strategy)

**Step 3 — Broad (each block separately):**
- Block 1 alone: `("agentic AI" OR "AI agents" OR "autonomous AI agents" OR "multi-agent systems")`
- Block 2 alone: `("AI governance" OR "AI accountability" OR "responsible AI" OR "governance framework")`
- Block 3 alone: `("enterprise risk" OR "financial loss" OR "firm performance" OR "liability" OR "ROI")`

**Step 4 — Moderate (two blocks combined with AND):**
- Block 1 AND Block 2:
  `("agentic AI" OR "AI agents" OR "autonomous AI agents") AND ("AI governance" OR "AI accountability" OR "responsible AI" OR "governance framework")`
- Block 1 AND Block 3:
  `("agentic AI" OR "AI agents" OR "autonomous AI agents") AND ("enterprise risk" OR "financial loss" OR "liability" OR "compliance failure")`
- Block 2 AND Block 3:
  `("AI governance" OR "responsible AI" OR "governance framework") AND ("firm performance" OR "business value" OR "financial loss" OR "ROI")`

**Step 5 — Narrow (all three blocks combined with AND):**
```
("agentic AI" OR "AI agents" OR "autonomous AI agents")
AND ("governance" OR "accountability" OR "oversight" OR "audit")
AND ("enterprise risk" OR "financial loss" OR "business value" OR "liability")
```

---

## Papers Found — Peer-Reviewed / Top Conference

### A. CS/Technical Side (already identified in v1, confirmed peer-reviewed)

| # | Paper | Venue | Quality | Year |
|---|-------|-------|---------|------|
| 1 | Governing AI Agents (Kolt) | Notre Dame Law Review | Top 20 US Law Review | 2025 |
| 2 | Regulating Advanced Artificial Agents (Cohen, Bengio et al.) | Science | JIF 44.7, A* | 2024 |
| 3 | Responsible AI Pattern Catalogue (Lu et al.) | ACM Computing Surveys | ABDC A*, CORE A*, JIF 28.0 | 2024 |
| 4 | Lessons from Complex Systems Science (Kolt et al.) | Patterns (Cell Press) | JIF 6.7, Q1 | 2025 |
| 5 | Managing Extreme AI Risks (Bengio, Hinton et al.) | Science | JIF 44.7, A* | 2024 |
| 6 | Harms from Increasingly Agentic Algorithmic Systems (Chan et al.) | ACM FAccT 2023 | CORE A, top-tier conference | 2023 |
| 7 | Visibility into AI Agents (Chan et al.) | ACM FAccT 2024 | CORE A, top-tier conference | 2024 |

### B. Management/Business Side (peer-reviewed, ABDC A*/A)

| # | Paper | Venue | Quality | Year |
|---|-------|-------|---------|------|
| 8 | Responsible AI Governance: Review & Framework (Mikalef et al.) | Information & Management | ABDC A*, JIF 8.2 | 2025 |
| 9 | AI Capability & Firm Performance (Mikalef et al.) | Information & Management | ABDC A*, JIF 8.2 | 2021 |
| 10 | AI in IS Research: SLR & Agenda (Enholm et al.) | Intl. J. of Information Management | ABDC A*, JIF 27.0 | 2022 |
| 11 | IT Governance: Top Performers (Weill & Ross) | Harvard Business School Press | Foundational (5000+ citations) | 2004 |
| 12 | ESG & Corporate Financial Performance (Friede et al.) | J. Sustainable Finance & Investment | ABDC A | 2015 |

### C. Agentic AI + Business Impact (NEW — peer-reviewed / top conference)

| # | Paper | Venue | Quality | Year | Key Finding |
|---|-------|-------|---------|------|-------------|
| 13 | Harms from Increasingly Agentic Algorithmic Systems (Chan et al.) | ACM FAccT 2023 | CORE A | 2023 | Taxonomy of harms from agentic systems across finance, healthcare, policing. Argues harms scale with agency level. |
| 14 | Visibility into AI Agents (Chan, Kolt et al.) | ACM FAccT 2024 | CORE A | 2024 | Proposes agent identifiers, real-time monitoring, activity logging. Argues visibility is prerequisite for governance. |
| 15 | AI Capability and Firm Performance: Sustainable Development (multiple) | Information Systems Frontiers | ABDC A, JIF 8.3 | 2024 | AI capability → firm performance mediated by data-driven culture. PLS-SEM + fsQCA. Validates methodology. |

### D. Papers Still Needed (for Google Scholar manual search)

The following gaps remain and should be searched on Google Scholar with the corrected Boolean queries:

1. **Algorithmic trading agent failures + financial cost**: Papers from Journal of Finance, Review of Financial Studies, or Journal of Financial Economics documenting autonomous trading agent losses (flash crashes, rogue algorithms). These exist — the 2010 Flash Crash alone generated significant academic literature.

2. **RPA governance + business value**: Papers from Decision Support Systems, EJIS, or JSIS on how robotic process automation governance affects firm outcomes. RPA is the predecessor to agentic AI and has a 5+ year empirical track record.

3. **Shadow IT + organizational risk**: Papers from Information Systems Journal, EJIS, or Computers & Security on how unsanctioned technology use creates measurable business risk. Shadow IT literature is mature and directly maps to our Shadow AI construct.

4. **Autonomous vehicle liability + governance**: Papers from transportation or law journals documenting the financial/legal impact of autonomous system failures and how governance frameworks mitigate them.

5. **AI incident cost quantification**: Papers from Computers & Security, JMIS, or ISR that quantify the financial cost of AI-related incidents in enterprises.

---

## What the Literature Tells Us So Far

### The business case for governance is proven (for traditional IT and general AI):
- IT governance → 40% higher IT returns (Weill & Ross, 2004)
- ESG governance → positive financial performance in 90% of 2,200 studies (Friede et al., 2015)
- AI governance → competitive performance via knowledge management (Mikalef et al., 2025)
- AI capability → firm performance via organizational creativity (Mikalef et al., 2021)

### The risk from agentic AI is documented (but not yet connected to business outcomes):
- Agentic systems create agency problems: information asymmetry, authority, loyalty, delegation (Kolt, 2025)
- Advanced agents cannot be reliably safety-tested (Cohen et al., 2024)
- Harms scale with agency level across finance, healthcare, policing (Chan et al., 2023)
- Visibility into agent behavior is a prerequisite for governance (Chan et al., 2024)
- 35 governance patterns exist but none validated in organizations (Lu et al., 2024)
- Organizational factors are the weak link (TRiSM Review, 2025)

### The gap:
Nobody has empirically connected agentic AI governance maturity to measurable business outcomes (cost reduction, risk mitigation, ROI). The CS side has the governance mechanisms. The management side has the business value evidence. The bridge paper — connecting governance of agents to financial impact on the firm — does not exist yet.

---

## Next Steps

1. Run the corrected Boolean queries on Google Scholar manually
2. Focus on finding peer-reviewed papers in the "Papers Still Needed" categories above
3. For each paper found, extract: constructs, theory, method, key quantitative finding, limitations
4. Update the Excel search log with new papers
5. Once we have 25-30 papers mapped, build the concept map and finalize the model
6. Convert finalized version to .pptx for submission
