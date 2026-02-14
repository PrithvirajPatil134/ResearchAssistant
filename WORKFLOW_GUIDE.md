# Research Assistant Workflow Selection Guide

## Quick Reference

| Your Question Starts With | Use This Workflow | Example |
|---------------------------|-------------------|---------|
| "Explain...", "What is...", "Define..." | `explain` | Explain mediation analysis |
| "How do I...", "Help me...", "How would we..." | `guide` | How do I write an objective? |
| "Review my...", "Feedback on..." | `review` | Review my methodology section |
| "Research plan for...", "Design study..." | `research` | Research plan for SaaS governance |

## Detailed Workflow Descriptions

### 1. EXPLAIN Workflow

**Purpose**: Define and explain academic concepts, theories, and terminology

**When to Use**:
- You want to understand a concept, theory, or term
- Need definition with theoretical foundation
- Want to learn about a methodology or framework

**Query Patterns**:
- "Explain [concept]"
- "What is [term]?"
- "Define [theory]"
- "Tell me about [framework]"

**Output Includes**:
1. Conceptual definition (from KB)
2. Theoretical foundation
3. Key components
4. Practical application
5. Research considerations

**Examples**:
```bash
ra explain "mediation analysis" --persona QNTR
ra explain "research philosophy" --persona DBA
ra explain "case study methodology" --persona CW
```

### 2. GUIDE Workflow

**Purpose**: Provide step-by-step guidance for completing academic tasks

**When to Use**:
- Need help completing an assignment
- Want procedural guidance ("how to do X")
- Responding to professor feedback
- Developing thesis components

**Query Patterns**:
- "How do I [task]?"
- "Help me [action]"
- "How would we proceed with [task]?"
- "Generate response for professor's email"
- "How should I approach [assignment]?"

**Output Includes**:
1. Task understanding
2. Suggested approach/framework
3. Relevant KB materials
4. Step-by-step guidance
5. Reflection questions
6. Draft templates with placeholders
7. Optional clarification questions

**Examples**:
```bash
ra guide "How do I write a research objective?" --persona DBA
ra guide "Help me respond to professor's email at /path/to/email.eml" --persona DBA
ra guide "How would we analyze this case study?" --persona QNTR
```

### 3. REVIEW Workflow

**Purpose**: Get feedback on completed work

**When to Use**:
- Submitting completed draft for review
- Want constructive feedback
- Need evaluation against standards

**Query Patterns**:
- "Review my [submission]"
- "Feedback on my [work]"
- "Evaluate this [document]"

**Output Includes**:
1. Executive summary
2. Strengths identified
3. Areas for improvement
4. Detailed feedback
5. Assessment scores
6. Recommended next steps

**Examples**:
```bash
ra review "Review my research objective" --persona DBA
ra review "Feedback on my questionnaire items" --persona QNTR
```

### 4. RESEARCH Workflow

**Purpose**: Plan research strategy and methodology

**When to Use**:
- Planning a research project
- Designing methodology
- Literature strategy planning
- Research gap identification

**Query Patterns**:
- "Research plan for [topic]"
- "Design study on [subject]"
- "Methodology for investigating [phenomenon]"

**Output Includes**:
1. Research objective clarification
2. Theoretical framework mapping
3. Literature strategy
4. Methodology recommendations
5. Timeline and next steps

**Examples**:
```bash
ra research "Research plan for digital transformation" --persona DBA
```

## Common Mistakes

### ❌ Wrong: Using EXPLAIN for Procedural Questions
```bash
ra explain "How do I write an objective?"  # WRONG - this is procedural
```
**Why it fails**: Explain workflow expects a concept to define, not steps to provide

**✅ Correct**:
```bash
ra guide "How do I write an objective?" --persona DBA
```

### ❌ Wrong: Using GUIDE for Concept Questions
```bash
ra guide "mediation analysis" --persona QNTR  # WRONG - this is conceptual
```
**Why it fails**: Guide workflow expects a task/assignment, not a concept

**✅ Correct**:
```bash
ra explain "mediation analysis" --persona QNTR
```

## What Happens on Workflow Mismatch?

**As of v2.0**: The EXPLAIN workflow now detects procedural questions and provides helpful error:

```
⚠️ WORKFLOW MISMATCH DETECTED ⚠️

Your query asks "how to proceed" - this is PROCEDURAL/GUIDANCE.

Recommended: Re-run with GUIDE workflow:
ra guide "your question" --persona PERSONA
```

This helps you correct the mistake immediately instead of getting empty output.

## Tips for Best Results

1. **Be specific**: Include file paths when referencing documents
2. **Use guide for "how to"**: Any question about procedure or steps
3. **Use explain for "what is"**: Any question about concepts or definitions
4. **Check the output score**: ≥9.0/10 means good quality, <9.0 may need workflow change
5. **Read KB materials first**: Understanding course context improves query formulation

## Support

If you're unsure which workflow to use, look at your question:
- Starts with **"How"** → likely GUIDE
- Starts with **"What is"** or **"Explain"** → likely EXPLAIN
- Starts with **"Review"** → likely REVIEW

Still unsure? Try GUIDE first - it's more flexible for multi-part questions.
