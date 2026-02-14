# Guide Workflow Guide - QNTR (Quantitative Research Methods)

> **Workflow**: `guide`
> **Purpose**: Help students develop research methodology skills through guided discovery
> **Last Updated**: 2026-02-02

---

## Workflow Steps
```
1. ReaderAgent → Scans KB for relevant methodology materials
2. ThinkingModule → Generates structured guidance based on request type
3. ReviewerAgent → Validates output matches expected format
4. OutputWriter → Saves to /output
```

## Expected Input
- `assignment`: Research task needing guidance (e.g., "design a questionnaire", "select statistical method")

## Request Type Detection

### Type 1: Research Design Guidance
**Triggers**: "research design", "methodology", "design study", "approach"
**Expected Output Structure**:
- Research question framing
- Design type recommendation (exploratory, descriptive, causal)
- Variables identification (IV, DV, mediators, moderators)
- Validity considerations

**Prof. Atul Prashar Criteria**:
1. Clear research question formulation
2. Theoretical grounding (RBV, ROT, Dynamic Capabilities)
3. Appropriate design for question type
4. Validity framework consideration

### Type 2: Questionnaire Development
**Triggers**: "questionnaire", "scale", "items", "measurement", "survey"
**Expected Output**:
- Item structure guidance
- Scale type recommendations (Likert, semantic differential)
- Section organization (demographics, constructs)
- Reference to DRO questionnaire as example

### Type 3: Statistical Method Selection
**Triggers**: "statistical", "analysis", "SPSS", "regression", "SEM", "factor"
**Expected Output**:
- Method recommendation with rationale
- Tool suggestion (SPSS/R/JASP/AMOS)
- Assumptions to check
- Course material references

### Type 4: General Guidance
**Triggers**: Default for unmatched requests
**Expected Output**: Understanding + approach + frameworks + reflection questions

---

## Grounding Rules

### MUST DO
- [ ] Detect request type from input keywords
- [ ] Apply type-specific output format
- [ ] Reference course slides and materials
- [ ] Connect to DRO research project examples
- [ ] Cite Prof. Prashar's frameworks
- [ ] Include validity considerations

### MUST NOT DO
- [ ] Give generic advice without KB grounding
- [ ] Skip statistical tool recommendations
- [ ] Ignore theoretical foundations
- [ ] Use explain template for guide requests

---

## Output Format by Type

### Research Design Guidance Format
```markdown
# Research Design Guidance: [Topic]

*Following Prof. Atul Prashar's Methodology Framework*

---

## Understanding Your Research Question
[Analysis of the question type]

## Recommended Design Approach
**Design Type**: [Exploratory/Descriptive/Causal]
**Rationale**: [Why this design fits]

## Variables Framework
| Variable Type | Construct | Measurement Consideration |
|---------------|-----------|---------------------------|
| Independent | [Name] | [Notes] |
| Dependent | [Name] | [Notes] |
| Mediator | [Name] | [Notes] |

## Theoretical Grounding
- **Primary Theory**: [Theory name and relevance]
- **Supporting Framework**: [Framework]

## Validity Considerations
- [ ] Internal validity: [Consideration]
- [ ] External validity: [Consideration]
- [ ] Construct validity: [Consideration]

## Questions to Reflect On
1. [Question]
2. [Question]
```

### Statistical Method Selection Format
```markdown
# Statistical Guidance: [Analysis Need]

## Recommended Method
**Method**: [Name]
**Tool**: [SPSS/R/JASP/AMOS]
**Rationale**: [Why appropriate]

## Assumptions to Check
- [ ] [Assumption 1]
- [ ] [Assumption 2]

## Course Reference
[Link to relevant slides/materials]

## Steps to Execute
1. [Step]
2. [Step]
```

---

## Priority Source Order
1. Class Slides (Session materials)
2. Course Materials (Prof. Prashar notes)
3. DRO Questionnaire (practical example)
4. Reference Materials
5. Research Papers

---

## Learned Patterns
### Pattern Log
| Date | Assignment Type | Approach | Score | Success Factor |
|------|-----------------|----------|-------|----------------|
| 2026-02-07 | Based on the class course outl... | Multi-source document analysis: Read all | 8.5 | Passed analyst scoring |
| 2026-02-09 | Based on the class course outl... | Read all source documents completely bef | 8.6 | Passed analyst scoring |
| (Learner populates) | | | | |
