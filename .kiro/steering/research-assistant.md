---
inclusion: auto
---

# Research Assistant Development Standards

This workspace is a Python-based research assistant that orchestrates LLM calls through kiro-cli
to help PhD students with academic workflows: case studies, thesis writing, quant analysis, lit reviews, research papers.

## Core Mental Model

Every workflow follows the human researcher pattern — process one thing at a time, build understanding incrementally, synthesize. This applies to ALL LLM touchpoints:
- Document analysis: 1 doc at a time → extract → compare → synthesize (parallel when >5 docs)
- Content writing: 1 section at a time → each builds on previous
- Quality scoring: 1 dimension at a time → each informed by previous
- Review: strengths → issues → suggestions (each pass informed by previous)

## Architecture

- kiro-cli is a PURE TEXT GENERATOR (`--trust-tools=`), never an agent
- Python orchestrator handles file reading, scoring, caching, staging, and learning
- `IterativeProcessor` + `SharedWorkspace` manage the iterative mental model
- `workflow_sections.py` defines section templates per document type (case study, thesis, paper, lit review, quant)
- All intermediate results staged to `spaces/{PERSONA}/workspace/{workflow_id}/`
- Cached stages in `spaces/{PERSONA}/cache/{workflow_id}/` survive failures

## LLM Call Sites (all through LLMClient → kiro-cli)

1. `IterativeProcessor.analyze_documents()` — per-document extraction (parallel or sequential)
2. `IterativeProcessor._synthesize()` — cross-document synthesis
3. `IterativeProcessor.write_sections()` — per-section writing
4. `IterativeProcessor.run_parallel_tasks()` — independent parallel tasks
5. `invoker._generate_reasoning()` — single-call generation (simple queries)
6. `AnalystAgent._llm_evaluate()` — 4 sequential dimension evaluations
7. `ReviewerAgent._llm_review()` — 3 sequential review passes
8. `LearnerAgent.extract_lesson_with_llm()` — lesson extraction
9. `LearnerAgent._extract_strategies_with_llm()` — strategy extraction
10. `LearnerAgent._summarize_reasoning_with_llm()` — summary

## Key Files

- `src/research_assistant/workflows/invoker.py` — Main orchestrator
- `src/research_assistant/core/iterative_processor.py` — IterativeProcessor + SharedWorkspace
- `src/research_assistant/core/workflow_sections.py` — Section templates per document type
- `src/research_assistant/core/artifact_cache.py` — Stage caching for failure recovery
- `src/research_assistant/core/llm.py` — LLM client (kiro-cli, Anthropic, OpenAI, Perplexity)
- `src/research_assistant/agents/analyst.py` — LLM-powered iterative quality scoring
- `src/research_assistant/agents/reviewer.py` — LLM-powered iterative standards review
- `src/research_assistant/agents/reader.py` — KB file extraction (PDF via PyPDF2, DOCX, MD, XLSX)
- `src/research_assistant/agents/learner.py` — Pattern learning and lesson persistence
- `src/research_assistant/learnings/` — Design principles from Anthropic evals, agent capability patterns

## Code Standards

- All agents inherit from `BaseAgent` in `agents/base.py`
- New workflows: register in `_register_default_workflows()`, add prompt in `_build_workflow_prompt()`, add CLI command in `cli.py`
- New document types: add section template in `workflow_sections.py`, add review rubric in `reviewer.py` REVIEW_RUBRICS
- New extraction types: add extraction/synthesis prompts in `workflow_sections.py`
