# Explain Workflow Guide - DBA

> **Workflow**: `explain`
> **Purpose**: Explain thesis proposal concepts using Prof. Cardasso's teaching style
> **Last Updated**: 2026-01-31

---

## Workflow Steps

```
1. ReaderAgent → Scans DBA knowledge base
2. LearnerAgent → Checks for similar patterns
3. ThinkingModule → Generates explanation (MUST ground in KB)
4. AnalystAgent → Scores (target: 9.0+)
5. ReviewerAgent → Validates output
6. LearnerAgent → Stores successful pattern
7. OutputWriter → Saves to /output
```

## Expected Input
- `topic`: Thesis proposal concept to explain (e.g., "research methodology", "literature review")

## Expected Output
- Structured academic explanation
- Grounded in DBA Thesis Proposal Template
- References Prof. Cardasso's guidance
- Actionable for student's proposal

---

## Grounding Rules

### MUST DO
- [ ] Start with definition from KB materials
- [ ] Reference DBA Thesis Proposal Template sections
- [ ] Cite Prof. Cardasso's Class Notes when applicable
- [ ] Connect to student's DRO thesis when relevant
- [ ] Use academic language at doctoral level

### MUST NOT DO
- [ ] Give generic thesis advice without KB grounding
- [ ] Ignore template structure references
- [ ] Skip methodological considerations
- [ ] Provide unsubstantiated claims

### Priority Source Order
1. DBAThesis DissertationProposalTemplate.docx
2. Prof Cardasso Class Notes.docx
3. dro_thesis_reference.md

---

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Generic response | Reads like internet advice | Search KB first, cite sources |
| Missing template link | No proposal section reference | Map to Intro/LitReview/Methodology/etc. |
| Ignoring DRO context | Doesn't connect to student's thesis | Check if DRO/SaaS/capital efficiency relates |
| Over-academic | Too dense to be actionable | Add "How to apply" section |

---

## Learned Patterns

### Pattern Log
| Date | Topic | Approach | Score | Success Factor |
|------|-------|----------|-------|----------------|
| 2026-01-31 | digital resource orchestration... | Use hierarchical section numbering with  | 9.2 | Passed analyst scoring |
| 2026-01-31 | digital resource orchestration... | Use hierarchical numbered sections with  | 9.1 | Passed analyst scoring |
| 2026-02-02 | digital resource orchestration... | Use hierarchical structure with numbered | 9.0 | Passed analyst scoring |
| 2026-02-07 | research philosophy... | Use hierarchical numbered sections with  | 9.1 | Passed analyst scoring |
| 2026-02-07 | How do I write a research obje... | Use direct confrontation with empathy: A | 8.4 | Passed analyst scoring |
| (Learner populates) | | | | |

### High-Performing Approaches
*(Learner agent updates this section)*

---

## Change Log
| Date | Change | Reason |
|------|--------|--------|
| 2026-01-31 | Initial creation | Establish workflow doc |
