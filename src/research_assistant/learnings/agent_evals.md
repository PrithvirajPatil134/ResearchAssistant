# Agent Evaluation Principles

Source: [Anthropic — Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

## Core Concepts

### Evaluation Structure
- A **task** is a single test with defined inputs and success criteria.
- A **trial** is one attempt at a task. Run multiple trials because model outputs vary between runs.
- A **grader** scores some aspect of performance. Combine multiple grader types per task.
- A **transcript** is the complete record of a trial (outputs, tool calls, reasoning, intermediate results).
- The **outcome** is the final state in the environment — not what the agent *said* it did, but what actually happened.

### Grader Types
1. **Code-based graders**: Fast, cheap, objective, reproducible. String match, binary tests, static analysis, outcome verification, tool call verification, transcript analysis (turns taken, token usage).
2. **Model-based graders**: Flexible, captures nuance, handles open-ended tasks. Rubric-based scoring, pairwise comparison, reference-based evaluation. Requires calibration with human graders.
3. **Human graders**: Gold standard quality. SME review, spot-check sampling, A/B testing. Expensive and slow.

### Capability vs Regression Evals
- **Capability evals**: "What can this agent do well?" Start at low pass rate, give teams a hill to climb.
- **Regression evals**: "Does the agent still handle what it used to?" Should have ~100% pass rate. Protects against backsliding.
- High-pass capability evals can "graduate" to regression suites.

## Key Principles for Our Workflow

### 1. Grade Outcomes, Not Transcripts
> "A flight-booking agent might say 'Your flight has been booked' but the outcome is whether a reservation exists in the database."

**Applied**: Our AnalystAgent should verify that actual content was generated (non-empty, grounded in KB), not just that the workflow completed without errors.

### 2. Fail Fast on Empty Content
> "Mistakes can propagate and compound across turns."

**Applied**: If the LLM returns empty content, stop immediately. Don't loop through 5 reasoning iterations scoring nothing.

### 3. Non-Determinism Requires Multiple Trials
- **pass@k**: Probability of at least one success in k attempts. Good for "find any solution."
- **pass^k**: Probability of all k trials succeeding. Good for "must be reliable every time."

**Applied**: For user-facing workflows, we care about pass^k (consistency). A workflow that sometimes produces empty output is unacceptable.

### 4. Design Graders Thoughtfully
> "Grade what the agent produced, not the path it took."
> "Build in partial credit — a support agent that identifies the problem but fails to process a refund is better than one that fails immediately."

**Applied**: Our AnalystAgent scoring should:
- Check content is non-empty and substantive (code-based grader)
- Check KB grounding (model-based grader)
- Award partial credit for structure even if depth is lacking
- NOT pass content that is clearly just the prompt echoed back

### 5. Evals as Communication
> "Evals can become the highest-bandwidth communication channel between product and research teams."

**Applied**: Quality scores should be meaningful to the user. A score of 8.6/10 on empty content destroys trust. Scores must correlate with actual output quality.

### 6. Start Simple, Iterate
> "20-50 simple tasks drawn from real failures is a great start."

**Applied**: Build eval cases from actual workflow failures (like this timeout incident). Each bug becomes a regression test.

### 7. Environment Isolation
> "Each trial should start from a clean environment. Unnecessary shared state between runs can cause correlated failures."

**Applied**: Each workflow execution should be independent. Don't let cached LLM client state or stale patterns affect new runs.
