# Guide Workflow Guide - DBA

> **Workflow**: `guide`
> **Purpose**: Help students develop thesis components through guided discovery
> **Last Updated**: 2026-01-31

---

## Workflow Steps
```
1. ReaderAgent → Scans KB for relevant source materials
2. ThinkingModule → Generates structured guidance based on request type
3. ReviewerAgent → Validates output matches expected format for request type
4. OutputWriter → Saves to /output
```

## Expected Input
- `assignment`: The thesis task needing guidance (e.g., "generate an objective", "review my methodology")

## Request Type Detection

### Type 1: Generate Objective
**Triggers**: "generate objective", "create objective", "write objective", "thesis objective"
**Expected Output Structure**:
- Research Objective statement starting with "The objective of this research is to..."
- Business Context section
- Research Scope (general to specific)
- Suggested Title (aligned with objective)
- Rationale table against Prof. Cardasso criteria

**Prof. Cardasso Criteria for Objectives** (from class notes 01/24/2026):
1. Start with "The objective of this research is to..." or "The aim of this research is to..."
2. Avoid broad topics and terminologies
3. Include business context for professors
4. Title should use same/similar words as objective
5. Structure: General → Specific

### Type 2: Review Methodology  
**Triggers**: "review methodology", "check my methodology", "methodology feedback"
**Expected Output**: Guiding questions + relevant KB frameworks

### Type 3: Develop Research Question
**Triggers**: "research question", "develop question"
**Expected Output**: Question templates + positioning advice

### Type 4: General Guidance
**Triggers**: Default for unmatched requests
**Expected Output**: Understanding + approach + frameworks + reflection questions

---

## Grounding Rules

### MUST DO
- [ ] Detect request type from input keywords
- [ ] Apply type-specific output format
- [ ] Reference actual KB materials (Prof. Cardasso notes, thesis reference)
- [ ] For objectives: Follow Prof. Cardasso's exact structure requirements
- [ ] Provide frameworks grounded in course materials

### MUST NOT DO
- [ ] Use generic "topic is empty" responses
- [ ] Apply explain workflow template for guide requests
- [ ] Skip type-specific validation criteria
- [ ] Give vague guidance without KB grounding

---

## Output Format by Type

### Generate Objective Output Format
```markdown
# [Topic] Thesis Objective

*Following Prof. Cardasso's Guidelines*

---

## Research Objective
**The objective of this research is to** [specific statement]

## Business Context
[Why this matters - business relevance]

## Research Scope (General → Specific)
I would like to find out:
1. **How** [question]
2. **To what extent** [question]
3. **Why** [question]

## Suggested Title
**"[Title aligned with objective words]"**

## Objective Rationale (Prof. Cardasso Criteria)
| Criterion | How Met |
|-----------|---------|
| Starts with proper phrasing | ✓/✗ |
| Avoids broad topics | ✓/✗ |
| Has business context | ✓/✗ |
| Title uses objective words | ✓/✗ |
| General → Specific | ✓/✗ |
```

### General Guidance Output Format
```markdown
# Guidance: [Task]

## Understanding the Task
[What's being asked]

## Suggested Approach
[Steps without direct answers]

## Relevant KB Materials
- [Material 1]: [How it helps]
- [Material 2]: [How it helps]

## Reflection Questions
1. [Question to guide thinking]
2. [Question to guide thinking]
```

---

## Learned Patterns
### Pattern Log
| Date | Assignment Type | Approach | Score | Success Factor |
|------|-----------------|----------|-------|----------------|
| 2026-02-07 | Generate an appropriate respon... | Use clear section headers | 9.0 | Passed analyst scoring |
| 2026-02-07 | With taking context from outpu... | Use visual separators (━━━ lines) to cre | 9.0 | Passed analyst scoring |
| (Learner populates) | | | | |
