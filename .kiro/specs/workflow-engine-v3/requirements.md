# Workflow Engine v3 — Requirements

## Context
The Research Assistant workflow engine orchestrates LLM calls through kiro-cli to help with
academic workflows. v2 added LLM-powered evaluation, staged execution, artifact caching,
and lessons learning. v3 focuses on cross-space reusability and deeper analysis capabilities.

## Requirements

### REQ-1: Persona-Specific Eval Rubrics
- MUST: Each persona/space can define custom eval rubrics in `spaces/{SPACE}/config/rubrics.yaml`
- MUST: Rubrics override the default workflow rubrics when present
- SHOULD: Include rubric templates for common academic tasks (thesis chapter, lit review, case study)
- Example: CW space rubric for case studies checks for protagonist development, exhibit quality, decision point tension

### REQ-2: Cross-Space Knowledge Sharing
- MUST: Lessons learned in one space should be accessible to other spaces when relevant
- SHOULD: Global lessons stored in `src/research_assistant/learnings/global_lessons.md`
- SHOULD: Space-specific lessons remain in `spaces/{SPACE}/doc/lessons_learned.md`
- MUST NOT: Leak persona-specific context (e.g., professor names) into global lessons

### REQ-3: Literature Survey Workflow
- MUST: New `survey` workflow type for systematic literature reviews
- MUST: Accept search terms, inclusion/exclusion criteria, and date range
- SHOULD: Generate PRISMA-style flow diagram data
- SHOULD: Output structured summary table (author, year, method, findings, relevance)

### REQ-4: Thesis Chapter Workflow
- MUST: New `thesis` workflow type for drafting thesis chapters
- MUST: Accept chapter type (intro, lit review, methodology, results, discussion)
- SHOULD: Enforce chapter-specific structure from KB templates
- SHOULD: Cross-reference with other chapters if available in KB

### REQ-5: Execution Observability
- MUST: Each workflow execution produces a structured trace log (JSON)
- MUST: Trace includes: stage timings, LLM call durations, token counts, scores, cache hits
- SHOULD: Trace viewable via `ra workflow trace {workflow_id}`
- SHOULD: Aggregate traces for performance trending

### REQ-6: Parallel Stage Execution
- SHOULD: Independent stages (e.g., benchmark analysis + context ingestion) run in parallel
- MUST: Dependent stages wait for prerequisites
- MUST: Cache still works correctly with parallel execution
