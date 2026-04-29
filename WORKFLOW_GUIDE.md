# Research Assistant Workflow Guide

## Architecture (Level 3)

```
User → CLI → WorkflowInvoker (orchestrator)
                    │
         ┌──────────┼──────────────────────┐
         │          │          │            │
      Reader    Learner    Contract     Recitation
     (Python)  (Python+LLM) (LLM)      (checkpoint)
         │          │          │            │
         └──────────┼──────────┘            │
                    ▼                       │
         IterativeProcessor                 │
         ┌──────────────────┐               │
         │ SharedWorkspace  │               │
         │ (staged results) │               │
         └────────┬─────────┘               │
                  ▼                         │
           kiro-cli (Claude)                │
           pure text generation             │
                  │                         │
                  ▼                         │
         ┌──────────────────────────────────┘
         │  Parallel Evaluation (Level 3)
         │  ┌─────────┬──────────┬───────────┐
         │  │ Analyst  │ Reviewer │ Evaluator │
         │  │ (LLM x4) │ (LLM x3) │ (LLM x1) │
         │  └────┬─────┴────┬─────┴─────┬─────┘
         │       └──────────┼───────────┘
         │                  ▼
         │         UnifiedEvaluation
         │         (merged verdict)
         └──────────────────┘
```

All LLM calls go through `kiro-cli --trust-tools=` (pure text, no agent behavior).
Python handles orchestration, file reading, caching, contracts, and learning.

## The Mental Model

Every workflow follows the same human researcher pattern:

1. Read one thing at a time, not everything into one prompt
2. Define "done" before starting (dispatch contract)
3. Build understanding incrementally, each step on the previous
4. When tasks are independent, run them in parallel (documents AND evaluators)
5. Re-anchor before composing (recitation checkpoint prevents drift)
6. Evaluate from multiple angles simultaneously (analyst + reviewer + evaluator)
7. Learn from every run (extract lessons, avoid past mistakes)
8. Audit assumptions periodically (thresholds go stale when models improve)

## Quick Reference

| Task | Workflow | Command |
|------|----------|---------|
| Explain a concept | `explain` | `ra explain "..." -p PERSONA` |
| Step-by-step guidance | `guide` | `ra guide "..." -p PERSONA` |
| Review submitted work | `review` | `ra review path/to/file -p PERSONA` |
| Research planning | `research` | `ra research "..." -p PERSONA` |
| Statistical analysis | `quant` | `ra quant "..." -p PERSONA` |
| Harness audit | `audit` | `ra audit -p PERSONA` |
| Any workflow by name | `workflow run` | `ra workflow run NAME "..." -p PERSONA` |

## Spaces

Four spaces exist, each representing an academic domain:

| Space | Domain | Knowledge Base |
|-------|--------|----------------|
| QNTR | Quantitative Research Methods | Course materials, method readings, datasets |
| CRO | Corporate Research & Operations | Industry cases, operational frameworks |
| DBA | Doctoral Business Administration | Dissertation materials, methodology guides |
| CW | Case Writing | Published cases, teaching notes, style guides |

Each space has its own:
- **knowledge/** (read-only source material)
- **output/** (final deliverables)
- **doc/** (lessons, session memory, workflow guides)
- **cache/** (reusable stage outputs)
- **artifacts/** (intermediate files per run)

## Level 3 Modules

### 1. Dispatch Contract (Pre-Dispatch)

Built after KB extraction, before agents execute. Defines:
- **done_definition**: 2-3 sentences describing what a successful output looks like
- **completeness_criteria**: What a complete answer must include
- **required_sections**: Sections the output must contain
- **grounding_requirements**: Claims that must be KB-grounded

Uses LLM for complex queries, falls back to workflow-specific heuristics for simple ones.
Trivial queries (< 15 words) get `skip_evaluator=True`.

The contract is injected into both the Analyst's scoring prompt and the Reviewer's validation prompt, so they score against intent rather than generic quality.

### 2. Recitation Checkpoint (Pre-Composition)

Inserted at two points:
- Before the final stage in multi-stage workflows
- Before `_format_output()` in all workflows

Re-states: "Original question was X. From stage 1 I have Y. From stage 2 I have Z. The user needs W."

Max ~200 words. Prevents drift toward the most verbose source.

### 3. Parallel Evaluation (Post-Composition)

Replaces the old sequential Analyst then Reviewer loop. Now runs three evaluators concurrently:

| Evaluator | What it checks | Criteria |
|-----------|---------------|----------|
| Analyst | Reasoning quality | KB grounding, completeness, quality, structure (0-10) |
| Reviewer | Standards compliance | Workflow-specific rubric, strengths/issues/suggestions |
| Evaluator | Intent alignment | Answer alignment, claim-evidence, completeness, actionability (1-5 each) |

All three run in `ThreadPoolExecutor(max_workers=3)` with 120s timeout.
Results merge into `UnifiedEvaluation`. If any evaluator fails, one revision attempt with combined feedback.

Latency savings: ~60-70% reduction vs sequential evaluation.

### 4. Harness Audit

Run on-demand or when the model changes. Checks:
- Are thresholds still right? (7.5 pass, 70% context, max 5 iterations)
- Is the workflow doing work the model now handles natively?
- Are there stale error patterns in lessons_learned.md?
- Are heuristic pre-checks still catching anything?

Produces a markdown report with findings and recommendations.

## How Stage Detection Works

When your query contains `STEP 1 / STEP 2 / STEP 3` markers, the invoker splits it into stages. Each stage is automatically classified:

| Stage Type | Detection Keywords | Processing Mode |
|------------|-------------------|-----------------|
| Multi-doc analysis | "analyze all", "each case", "benchmark", "all papers" | Parallel or iterative (1 doc at a time) |
| Document writing | "write the", "generate the complete", "draft the" | Section-by-section (template-driven) |
| Everything else | (none) | Single focused LLM call |

## Section Templates (Auto-Selected)

The system detects what you're writing and selects the right section structure:

| Document Type | Detection Keywords | Sections |
|--------------|-------------------|----------|
| Case study | "case study", "teaching case" | Opening, Background, Industry, Crisis, Options, Decision, Exhibits |
| Research paper | "research paper", "journal paper" | Abstract, Intro, Lit Review, Methodology, Results, Discussion, Conclusion |
| Literature review | "literature", "lit review", "survey" | Search Strategy, Thematic Analysis, Framework Mapping, Methods Assessment, Gaps, Conceptual Framework |
| Thesis intro | "thesis", "chapter 1", "introduction" | Context, Problem, Questions, Significance, Overview |
| Thesis methodology | "methodology", "chapter 3" | Philosophy, Design, Collection, Analysis, Ethics |
| Thesis results | "results", "chapter 4" | Descriptive Stats, Assumptions, Hypothesis Testing, Summary |
| Thesis discussion | "discussion", "chapter 5" | Findings Summary, Discussion, Theory Implications, Practice Implications, Limitations |

## Evaluation Pipeline (Level 3)

After content is generated, all three evaluators run in parallel:

**Analyst (4 LLM calls, sequential within agent)**:
1. Structure & Clarity: score + reasoning
2. KB Grounding: score + compare with previous (contract-aware)
3. Completeness: score + compare with previous (contract-aware)
4. Quality & Rigor: final score informed by all dimensions

Pass threshold: 7.5/10.

**Reviewer (3 LLM calls, sequential within agent)**:
1. Identify strengths (contract-aware)
2. Identify issues (informed by strengths)
3. Generate suggestions (informed by both)

Pass threshold: 6.0/10.

**Evaluator (1 LLM call)**:
Scores 4 criteria 1-5:
- Answer Alignment: Does it answer the actual question?
- Claim-Evidence Linkage: Is every claim backed by a source?
- Completeness: Would the user need an obvious follow-up?
- Actionability: Can the user DO something with this?

Pass threshold: All scores >= 3.

If any evaluator fails, one revision with combined feedback from all three.

## Shared Workspace & Caching

Each staged execution creates:
- `spaces/{PERSONA}/cache/{workflow_id}/` for cached stage outputs (resume on failure)
- `spaces/{PERSONA}/workspace/{workflow_id}/` for shared workspace intermediate results

Any stage can read from the workspace. If stage 3 fails, stages 1-2 are cached and will not regenerate on re-run.

## Learning System

Every run:
1. Loads lessons from `spaces/{PERSONA}/doc/lessons_learned.md`
2. Injects them into every LLM prompt
3. After completion, extracts a new one-line lesson via LLM
4. Stores it for future runs
5. If score >= 8.0, stores reasoning pattern with strategies for warm-start matching

View lessons: `cat src/research_assistant/spaces/{PERSONA}/doc/lessons_learned.md`

## Workflow Logging (Level 3)

Each execution logs to `logs/workflow_history.jsonl` with expanded data:

```json
{
  "timestamp": "2026-04-09T...",
  "workflow": "explain",
  "persona": "QNTR",
  "query": "...",
  "score": 8.2,
  "reasoning_iterations": 2,
  "validation_iterations": 1,
  "execution_time_ms": 45000,
  "eval": {
    "analyst_score": 8.2,
    "reviewer_score": 7.5,
    "evaluator": {
      "alignment": 4,
      "evidence": 4,
      "completeness": 3,
      "actionability": 4
    },
    "overall_pass": true
  }
}
```

This data feeds the Harness Audit for threshold analysis.

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `LLM_TIMEOUT_SECONDS` | 300 | Base timeout (adaptive estimation may increase) |
| `LLM_MODEL` | claude-sonnet-4.5 | Model for kiro-cli |
| `PERPLEXITY_API_KEY` | (none) | Use Perplexity API instead of kiro-cli |
| `ANTHROPIC_API_KEY` | (none) | Use Anthropic API directly |

## Tips

1. **Use STEP markers** for complex tasks to trigger staged execution
2. **Reference file paths** in your query; the reader extracts them automatically
3. **Re-run on failure**; cached stages will not regenerate
4. **Check lessons**: `cat spaces/PERSONA/doc/lessons_learned.md`
5. **>5 documents** triggers parallel analysis automatically
6. **Run `ra audit`** after model changes or quarterly to check threshold staleness
7. **Check eval logs**: `tail logs/workflow_history.jsonl` shows all three evaluator scores

---

## Change Log

### 2026-04-25: Cross-Space Knowledge, Session Memory, Layered Config, Agent Protocol

**Source**: Analysis of [AWSMantle genai-rewrite branch](https://code.amazon.com/packages/AWSMantle/trees/genai-rewrite) for applicable patterns.

**Changes to workflow capabilities**:

#### 1. Cross-Space Knowledge Access with Isolation

*Problem*: A research paper might need knowledge from CRO (industry cases), QNTR (method readings), and DBA (dissertation frameworks), but each workflow was locked to one space's knowledge base.

*Solution*: Spaces can now declare read-only references to other spaces' knowledge via `cross_space_sources` in persona.yaml:

```yaml
cross_space_sources:
  - space: DBA
    access: read_only
    knowledge_types: [research_papers, methodology]
  - space: CRO
    access: read_only
    knowledge_types: [industry_cases]
```

Key behaviors:
- Cross-space access is read-only for knowledge. Learnings and patterns stay isolated per space.
- Every piece of cross-space content is tagged with its source space so agents know provenance.
- When a cross-space reference is ambiguous, the system flags `[CLARIFICATION NEEDED]` rather than assuming. It does not make assumptions about which space's interpretation to use.
- The Learner tracks which cross-space combinations work well for which query types, building patterns over time.
- Enabled/disabled via `--cross-space` CLI flag or `cross_space_enabled` config.

*Performance*: Zero additional LLM calls. The Reader already reads files; this expands which files it can read.

#### 2. Single-File Cross-Session Memory

*Problem*: Memory was in-process only. Reasoning patterns and strategies were lost between CLI runs. Only one-line lessons persisted.

*Solution*: At workflow end, a `session_memory.md` file (~2K tokens) is written per space:

```
spaces/{SPACE}/doc/session_memory.md
```

Contains:
- Last 5 query summaries with scores
- Top strategies that worked (from Learner patterns)
- Known user preferences observed across runs
- Cross-space patterns (which combinations produced good results)

At workflow start, this file is loaded alongside lessons and injected into the warm-start context.

*Performance*: Zero additional LLM calls in the common case. LLM summarization only triggers when the file exceeds 2K tokens (roughly every 10-15 runs). The file read at startup is negligible.

#### 3. Layered Configuration with Runtime Overrides

*Problem*: Changing evaluation thresholds or disabling features required editing config files.

*Solution*: New CLI flags and config section for runtime control:

```bash
# Fast mode: skip parallel eval, limit iterations
ra explain "topic" -p QNTR --skip-parallel-eval --max-iterations 2

# Disable post-completion LLM calls (lesson extraction, strategy extraction)
ra explain "topic" -p QNTR --skip-learner-llm

# Enable cross-space knowledge
ra research "topic" -p QNTR --cross-space

# Combine for maximum speed
ra explain "topic" -p QNTR --skip-parallel-eval --skip-learner-llm --max-iterations 1
```

Config file equivalent:

```yaml
performance:
  parallel_eval_enabled: true
  max_reasoning_iterations: 5
  learner_llm_calls: true
  cross_space_enabled: false
```

CLI flags override config file values. Environment variables override both.

*Performance*: Strictly positive. Provides explicit controls to trade quality for speed when needed.

#### 4. Formalized Agent Interface Protocol

*Problem*: `BaseAgent.execute(**kwargs)` accepted anything. Agents could be wired wrong without errors until runtime.

*Solution*: Python `Protocol` classes define typed input/output for each agent role:

```python
class ReaderProtocol(Protocol):
    def execute(self, query: str, knowledge_dir: Path) -> AgentResult: ...

class AnalystProtocol(Protocol):
    def execute(self, query: str, reasoning: str,
                knowledge_content: List[str], iteration: int) -> AgentResult: ...

class ReviewerProtocol(Protocol):
    def review_against_standards(self, content: str, workflow_name: str,
                                  user_query: str, persona: Dict,
                                  contract: Any) -> Any: ...

class LearnerProtocol(Protocol):
    def get_patterns(self, query: str) -> Dict[str, Any]: ...
    def store_pattern(self, query: str, reasoning: str,
                      score: float, feedback: Optional[str]) -> Any: ...
```

Startup validation checks that all agents satisfy their protocol before the workflow runs. Catches wiring errors immediately instead of mid-execution.

*Performance*: Zero. Validation runs once at startup in microseconds.

**Files touched**: `agents/base.py`, `config.py`, `spaces/loader.py`, `agents/reader.py`, `agents/learner.py`, `workflows/invoker.py`, `cli.py`, each space's `persona.yaml`.

### 2026-04-28: Binary File Reading, Sub-Agent Contract, Memory Tools

**What changed**:

#### 1. Binary File Handling

The workflow pipeline now reads PDFs, DOCX, and XLSX files in full. Previously the ReaderAgent truncated PDFs at 10K characters; that limit was removed. Token budget management stays at the `extract_relevant()` orchestration layer.

The utility at `scripts/read_binary.py` handles extraction in-memory. No conversion files are written to disk; the binary file remains the single source of truth. Supported commands:

```bash
python3 scripts/read_binary.py paper.pdf            # Full extraction
python3 scripts/read_binary.py paper.pdf --pages 1-10
python3 scripts/read_binary.py paper.pdf --meta     # Page count only
python3 scripts/read_binary.py data.xlsx --sheet "2025 JQL"
```

#### 2. Sub-Agent Contract for Large Documents

For documents over 15 pages or 30K characters of extracted text, the orchestrator delegates full-document processing to a sub-agent. The contract is enforced by both the steering rule (`.kiro/steering/binary-file-reading.md`) and the AnalystAgent's grounding check:

- **Input**: full extracted text + explicit task instruction
- **Output**: structured response with page/section references for every claim, completeness declaration, zero fabrication
- **Conduct**: no partial extraction, no summary-only responses, no vague statements
- **Orchestrator verification**: spot-check 2-3 claims directly against source pages, flag outputs that lack page references, reject and re-delegate thin outputs

When the ReaderAgent encounters a binary file during workflow execution, the AnalystAgent's completeness check now verifies that all pages/sections were processed, and the grounding check verifies page-level references.

#### 3. Persistent Memory Tools (Optional)

**CognitiveInfrastructure**: MCP server installed via `aim mcp install cognitive-infrastructure-mcp`. Provides `kiro-recall` (hybrid keyword + vector search over curated knowledge, local embeddings, no AWS credentials needed), `workspace-search` (BM25 full-workspace index), and `tool-router` (MCP proxy). Configure `VAULT_DIR` in `~/.kiro/settings/mcp.json` to point at the workspace root.

**Kiro Evolve** (IDE-adapted): Captures Kiro IDE conversations via `promptSubmit` and `agentStop` hooks, writes daily transcripts to `~/.kiro/transcripts/`. After 50+ prompts across 2+ days, proposes knowledge graduation via a manual trigger. Approved knowledge lands in `.kiro/steering/evolved/` and auto-loads into future sessions. Say "evolve" in any session for on-demand review.

Both tools apply to Kiro IDE and to kiro-cli workflow execution (which reads the same `~/.kiro/settings/mcp.json` and `.kiro/steering/` directory).

#### 4. Applicability

These changes apply workspace-wide:
- **Kiro IDE sessions**: all chat interactions
- **Workflows**: explain, guide, review, research, quant
- **ReaderAgent**: binary file consumption during workflow execution
- **AnalystAgent**: completeness and grounding verification against binary sources
