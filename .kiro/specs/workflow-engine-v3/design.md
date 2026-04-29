# Workflow Engine v3 — Design

## REQ-1: Persona-Specific Eval Rubrics

### Implementation
- Add `spaces/{SPACE}/config/rubrics.yaml` with structure:
```yaml
workflows:
  guide:
    dimensions:
      - name: protagonist_development
        weight: 0.3
        description: "Is the protagonist three-dimensional with clear motivations?"
      - name: exhibit_quality
        weight: 0.2
        description: "Are exhibits data-driven with real numbers from source materials?"
    pass_threshold: 7.5
```
- AnalystAgent loads persona rubric if available, falls back to default
- ReviewerAgent uses persona rubric for workflow-specific review

### Files to modify
- `src/research_assistant/agents/analyst.py` — load rubric from persona config
- `src/research_assistant/agents/reviewer.py` — load rubric from persona config
- Create template: `src/research_assistant/spaces/_templates/rubrics.yaml`

## REQ-2: Cross-Space Knowledge Sharing

### Implementation
- Global lessons: `src/research_assistant/learnings/global_lessons.md`
- LearnerAgent checks if lesson is persona-specific or generalizable
- Generalizable lessons promoted to global file
- All spaces load global lessons + their own space lessons

### Files to modify
- `src/research_assistant/agents/learner.py` — add global lesson storage
- `src/research_assistant/workflows/invoker.py` — load global + space lessons

## REQ-3-4: Literature Survey & Thesis Workflows

### Implementation
- Register new workflow specs in `_register_default_workflows()`
- Add prompts in `_build_workflow_prompt()`
- Add CLI commands in `cli.py`
- Add review rubrics in `reviewer.py` REVIEW_RUBRICS dict

## REQ-5: Execution Observability

### Implementation
- New `src/research_assistant/core/tracer.py` module
- Each workflow step emits trace events
- Trace saved to `spaces/{SPACE}/traces/{workflow_id}.json`
- CLI command: `ra workflow trace {id}`

## REQ-6: Parallel Stage Execution

### Implementation
- Use `concurrent.futures.ThreadPoolExecutor` for independent stages
- Stage dependency graph from `_detect_stages()` + explicit `depends_on` markers
- Cache-aware: check cache before spawning thread
