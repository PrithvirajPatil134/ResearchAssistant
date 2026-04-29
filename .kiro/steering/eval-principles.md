---
inclusion: fileMatch
fileMatchPattern: "**/agents/analyst.py,**/agents/reviewer.py,**/invoker.py"
---

# Evaluation Principles (from Anthropic's Agent Eval Framework)

When modifying the evaluation or review agents, follow these principles:

## Grade Outcomes, Not Process
- Check what was PRODUCED, not the path taken
- A score of 8+ on empty content is a system failure
- Verify content is non-empty and substantive BEFORE running LLM evaluation

## Fail Fast on Broken Output
- Empty content → score 0 immediately (heuristic pre-check)
- Prompt echoed back → score 0 immediately
- Tool call artifacts in output → score 0 immediately
- Don't waste LLM calls scoring obviously broken output

## LLM Evaluation Rubric
The AnalystAgent uses 4 dimensions (equal weight):
1. KB Grounding: Is content sourced from provided materials?
2. Completeness: Does it address all parts of the query?
3. Quality & Rigor: Does it meet academic standards?
4. Structure & Clarity: Is it well-organized?

## Workflow-Specific Review Rubrics
The ReviewerAgent uses different rubrics per workflow type.
When adding a new workflow, add its rubric to `REVIEW_RUBRICS` dict in reviewer.py.

## Every Failure Becomes a Test Case
When a workflow fails in a new way, add a regression test in `tests/`.
