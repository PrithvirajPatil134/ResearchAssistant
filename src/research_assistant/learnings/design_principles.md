# Design Principles for Research Assistant

Synthesized from external learnings and applied to our workflow architecture.

## Principle 1: Grade Outcomes, Not Process

From Anthropic's eval guide: "The outcome is whether a reservation exists in the database, not whether the agent said it was booked."

Our AnalystAgent and ReviewerAgent must verify:
- Content is non-empty and substantive (code-based check BEFORE model-based scoring)
- Content is grounded in KB materials (not hallucinated)
- Content addresses the user's actual query
- A score of 8+/10 on empty content is a system failure, not a success

## Principle 2: Fail Fast, Fail Loud

From eval best practices: "Mistakes propagate and compound across turns."

- If LLM returns empty content → raise error immediately, don't loop
- If all KB files fail to extract → stop and report, don't generate from nothing
- If timeout occurs → report clearly with actionable guidance (increase timeout, simplify prompt)
- Never write empty output files and call it success

## Principle 3: Adaptive Resource Allocation

From capability design: "Start simple. Add complexity only when the problem demands it."

- Estimate prompt complexity before choosing timeout and iteration count
- Simple explain query → 1-2 iterations, shorter timeout
- Complex multi-step case study → more iterations, longer timeout, progress heartbeats
- Don't run 5 reasoning iterations + 2 validation passes for a one-line question

## Principle 4: Progressive Disclosure of Context

From agent capability menu: "Keep context usage around 10%, avoid exceeding 40%."

- Don't dump all KB files into every prompt
- Load summaries/metadata first, then deep-dive into relevant files
- ContextGuard should actively manage the token budget
- For large prompts (like the case study), leave room for the LLM to actually reason

## Principle 5: Transparency Over Silence

From user experience: "Users need to know things are progressing."

- Show heartbeat/progress during long operations
- Report what stage the workflow is in (reading KB, reasoning iter 2/5, scoring)
- If an LLM call is taking long, show elapsed time
- Never let the user stare at a blank terminal wondering if it's stuck

## Principle 6: Every Failure Becomes a Test Case

From eval roadmap: "Start with what you already test manually. Convert user-reported failures into test cases."

- The timeout-with-empty-output bug → regression test: verify workflow fails when LLM returns empty
- The prompt-echoed-as-heading bug → regression test: verify heading is truncated for long queries
- The 8.6-score-on-nothing bug → regression test: verify analyst rejects empty content

## Principle 7: Composable Ingredients, Not Monoliths

From capability design: "Think of agent composition like cooking — ingredients combined into recipes."

- Reader, Analyst, Reviewer, Learner are ingredients (keep them focused)
- Workflow specs (explain, guide, review) are recipes (keep them composable)
- Don't bundle too much into one agent — a Reviewer shouldn't also be scoring
- Each agent should have a clear, testable responsibility
