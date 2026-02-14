# Guide Workflow Guide - CW (Case Writing)

> **Workflow**: `guide`
> **Purpose**: Help students develop case writing skills through guided discovery
> **Last Updated**: 2026-02-02

---

## Workflow Steps
```
1. ReaderAgent → Scans KB for relevant case templates and examples
2. ThinkingModule → Generates structured guidance based on request type
3. ReviewerAgent → Validates output matches expected format
4. OutputWriter → Saves to /output
```

## Expected Input
- `assignment`: The case writing task needing guidance (e.g., "generate a case idea", "structure my teaching note")

## Request Type Detection

### Type 1: Generate Case Idea
**Triggers**: "case idea", "generate case", "case concept", "new case"
**Expected Output Structure**:
- Case Idea statement following template structure
- Protagonist/Organization identification
- Decision point/dilemma
- Learning objectives
- Source data requirements

**Prof. Kakoli Sen Criteria for Case Ideas**:
1. Clear protagonist with decision authority
2. Real or realistic dilemma with time pressure
3. Relevant data availability
4. Teaching utility (learning objectives)
5. Narrative potential (story arc)

### Type 2: Develop Teaching Note
**Triggers**: "teaching note", "TN structure", "instructor guide"
**Expected Output**: 
- Synopsis framework
- Learning objectives guidance
- Discussion questions approach
- Board plan suggestions
- Analysis frameworks

### Type 3: Improve Case Narrative
**Triggers**: "narrative", "storytelling", "case flow", "case structure"
**Expected Output**: 
- Opening hook suggestions
- Protagonist development guidance
- Tension/conflict building
- Decision point framing

### Type 4: General Guidance
**Triggers**: Default for unmatched requests
**Expected Output**: Understanding + approach + frameworks + reflection questions

---

## Grounding Rules

### MUST DO
- [ ] Detect request type from input keywords
- [ ] Apply type-specific output format
- [ ] Reference Teaching Note Template structure
- [ ] Cite published case examples (C1-C15)
- [ ] Connect to Tesla Governance Case when relevant

### MUST NOT DO
- [ ] Give generic writing advice without KB grounding
- [ ] Skip narrative/storytelling considerations
- [ ] Use explain template for guide requests
- [ ] Give "topic is empty" responses when input provided

---

## Output Format by Type

### Generate Case Idea Output Format
```markdown
# Case Idea: [Title]

*Following Prof. Kakoli Sen's Case Idea Template*

---

## Case Concept
**The central dilemma is:** [Decision point statement]

## Protagonist Profile
- **Who**: [Name/Role]
- **Organization**: [Company/Context]
- **Decision Authority**: [What they control]

## Teaching Utility
**Primary Learning Objectives:**
1. [Objective 1]
2. [Objective 2]
3. [Objective 3]

## Data Requirements
- [ ] Financial data
- [ ] Interview access
- [ ] Industry context
- [ ] Competitor analysis

## Narrative Arc
- Opening hook: [Suggestion]
- Rising tension: [Key events]
- Decision point: [Climax]
```

### Teaching Note Guidance Format
```markdown
# Teaching Note Guidance: [Case Name]

## Synopsis Framework
[What to include/emphasize]

## Learning Objectives Approach
[How to frame objectives]

## Discussion Flow
1. [Opening question approach]
2. [Analysis framework suggestions]
3. [Closing synthesis]

## Board Plan Suggestions
[Visual organization guidance]
```

---

## Priority Source Order
1. Teaching Note Template
2. Case Idea Template
3. Tesla Case Template
4. Published Cases (C1-C15)

---

## Learned Patterns
### Pattern Log
| Date | Assignment Type | Approach | Score | Success Factor |
|------|-----------------|----------|-------|----------------|
| 2026-02-07 |  Here is an email thread ('/Us... | Begin with explicit context reconstructi | 8.9 | Passed analyst scoring |
| (Learner populates) | | | | |
