# Research Workflow Guide - DBA

> **Workflow**: `research`
> **Purpose**: Full research analysis with multi-step reasoning
> **Last Updated**: 2026-01-31

---

## Workflow Steps
```
1. ReaderAgent → Deep KB scan for research context
2. ThinkingModule → Multi-step analysis (Read → Explain → Review)
3. AnalystAgent → Scores research rigor
4. ReviewerAgent → Final validation
5. OutputWriter → Comprehensive output to /output
```

## Expected Input
- `task`: Research task requiring comprehensive analysis

## Expected Output
- Full research analysis with literature grounding
- Methodology recommendations
- Critical evaluation
- Next steps for the student

---

## Grounding Rules

### MUST DO
- [ ] Comprehensive KB search before reasoning
- [ ] Multi-perspective analysis (theoretical + practical)
- [ ] Connect to DRO thesis context when relevant
- [ ] Provide methodological guidance

### MUST NOT DO
- [ ] Shallow analysis without KB depth
- [ ] Skip critical evaluation component
- [ ] Ignore feasibility considerations

---

## Learned Patterns
### Pattern Log
| Date | Task Type | Approach | Score | Success Factor |
|------|-----------|----------|-------|----------------|
| (Learner populates) | | | | |
