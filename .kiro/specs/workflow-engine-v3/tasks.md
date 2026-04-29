# Workflow Engine v3 — Tasks

## REQ-1: Persona-Specific Eval Rubrics
- [ ] Create `rubrics.yaml` template in `spaces/_templates/`
- [ ] Add rubric loading to AnalystAgent (`_load_persona_rubric()`)
- [ ] Add rubric loading to ReviewerAgent
- [ ] Create CW-specific rubric for case study evaluation
- [ ] Create QNTR-specific rubric for quantitative analysis evaluation
- [ ] Test: custom rubric overrides default scoring dimensions

## REQ-2: Cross-Space Knowledge Sharing
- [ ] Create `src/research_assistant/learnings/global_lessons.md`
- [ ] Add `promote_to_global()` method in LearnerAgent
- [ ] Load global lessons in invoker alongside space lessons
- [ ] Filter persona-specific content from global lessons
- [ ] Test: lesson from CW space available in QNTR space

## REQ-3: Literature Survey Workflow
- [ ] Register `survey` workflow spec
- [ ] Add `_build_workflow_prompt()` case for survey
- [ ] Add `survey` review rubric to ReviewerAgent
- [ ] Add `ra survey` CLI command
- [ ] Test: survey workflow produces structured output

## REQ-4: Thesis Chapter Workflow
- [ ] Register `thesis` workflow spec
- [ ] Add `_build_workflow_prompt()` case for thesis (with chapter type detection)
- [ ] Add `thesis` review rubric to ReviewerAgent
- [ ] Add `ra thesis` CLI command
- [ ] Test: thesis workflow enforces chapter-specific structure

## REQ-5: Execution Observability
- [ ] Create `src/research_assistant/core/tracer.py`
- [ ] Emit trace events from invoker at each step
- [ ] Save trace to `spaces/{SPACE}/traces/{workflow_id}.json`
- [ ] Add `ra workflow trace` CLI command
- [ ] Test: trace file contains stage timings and scores

## REQ-6: Parallel Stage Execution
- [ ] Add dependency detection to `_detect_stages()`
- [ ] Implement ThreadPoolExecutor for independent stages
- [ ] Ensure cache works correctly with parallel writes
- [ ] Test: independent stages run concurrently, dependent stages wait
