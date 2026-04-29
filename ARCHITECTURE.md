# ResearchAssistant Architecture

## Core Concept

Multi-agent research workflow system where **spaces** (academic domain simulations) orchestrate **agents** to process research tasks, with outputs saved as `.md` files.

Each space (QNTR, CRO, DBA, CW) represents a distinct academic domain with its own knowledge base, persona configuration, prompts, and learned patterns. Agents operate within a space's context but can reference knowledge from other spaces when configured.

Implements **Level 3 context engineering**: designing the information architecture, feedback loops, evaluation criteria, and context lifecycle across the entire agent session.

## Spaces (formerly "Personas")

Spaces are the organizational unit. Everything revolves around the space:

```
src/research_assistant/spaces/
├── QNTR/          # Quantitative Research Methods
│   ├── persona.yaml
│   ├── prompts.yaml
│   ├── knowledge/       # Read-only source material
│   ├── output/          # Final deliverables only
│   ├── artifacts/       # Intermediate files per run
│   ├── cache/           # Cached stage outputs (reusable)
│   ├── doc/             # Lessons, workflow guides, session memory
│   ├── assignment/      # Student submissions for review
│   ├── communication/   # Email drafts, correspondence
│   └── workspace/       # Shared workspace for multi-stage runs
├── CRO/            # Corporate Research & Operations
├── DBA/            # Doctoral Business Administration
├── CW/             # Case Writing
└── loader.py       # SpaceLoader (loads persona.yaml + knowledge)
```

Each space has:
- **persona.yaml**: Identity, behaviors, agent configs, guidelines, ethics, knowledge base config
- **prompts.yaml**: Agent-specific prompts per workflow type
- **knowledge/**: Read-only source material (PDFs, slides, papers). Never written to by agents.
- **output/**: Final deliverables only. One file per workflow run.
- **doc/**: Persistent learning data (lessons_learned.md, workflow guides, session memory)
- **cache/**: Cached stage outputs. Reused across runs if stages match.

## Technical Design

### Entry Points
```
CLI (ra command) → WorkflowInvoker → Contract → Staged Reasoning → ParallelEval → Output
```

### Source Structure
```
src/research_assistant/
├── __init__.py
├── cli.py                    # Click-based CLI (entry point)
├── config.py                 # Configuration management
│
├── workflows/
│   └── invoker.py           # WorkflowInvoker (orchestrator + execution)
│
├── core/                     # Core modules
│   ├── __init__.py           # Exports: Memory, ContextGuard, LLM, etc.
│   ├── contextguard.py      # Token monitoring at 70% threshold
│   ├── memory.py            # Shared state across agents (in-process)
│   ├── thinking.py          # Reasoning chains, hallucination detection
│   ├── controller.py        # Orchestrates thinking process
│   ├── llm.py               # Unified LLM client (Perplexity/Anthropic/OpenAI/kiro-cli)
│   ├── parallel_agents.py   # Parallel document analysis (batched)
│   ├── artifact_cache.py    # Stage-level caching for multi-step workflows
│   ├── workflow_sections.py # Section templates for document types
│   ├── dispatch_contract.py # Pre-dispatch contract (Level 3)
│   ├── evaluator.py         # Post-composition evaluation (Level 3)
│   ├── recitation.py        # Attention re-anchoring (Level 3)
│   ├── parallel_eval.py     # Concurrent evaluation (Level 3)
│   ├── iterative_processor.py # Section-by-section document generation
│   └── harness_audit.py     # Assumption auditing (Level 3)
│
├── agents/                   # Specialized agents
│   ├── base.py              # BaseAgent with persona context
│   ├── reader.py            # Reads and extracts from knowledge base
│   ├── analyst.py           # Scores reasoning quality (0-10)
│   ├── reviewer.py          # Validates against standards
│   └── learner.py           # Learns from feedback, warm-start patterns
│
├── spaces/                   # Space definitions (see above)
│   ├── loader.py            # SpaceLoader
│   ├── QNTR/
│   ├── CRO/
│   ├── DBA/
│   └── CW/
│
└── learnings/               # Cross-space design principles and eval docs
```

## Workflow Execution Flow

The actual execution path through `WorkflowInvoker.invoke()`:

```
1. CLI Command
   ra explain "Brand Equity" --persona QNTR

2. Load Space
   SpaceLoader reads persona.yaml, prompts.yaml, scans knowledge/

3. Initialize Components
   Memory, ContextGuard (100K tokens, 70% threshold),
   ReaderAgent, LearnerAgent, AnalystAgent, ReviewerAgent, ThinkingModule

4. STEP 1: Read KB (ReaderAgent)
   Scan knowledge/ directory, extract content from matching files
   Result: extracted_content[] (list of file contents)

5. STEP 1.5: Build Dispatch Contract (Level 3)
   LLM-generated for complex queries (>15 words), heuristic for simple ones
   Defines: done_definition, completeness_criteria, required_sections, grounding_requirements
   Stored in Memory for Analyst and Reviewer to score against

6. STEP 2: Warm Start (LearnerAgent)
   Load lessons from doc/lessons_learned.md
   Match query against stored reasoning patterns (Jaccard similarity)
   Inject strategies + lessons into system prompt

7. STEP 3: Stage Detection
   If query has STEP 1/STEP 2 markers → split into stages
   Each stage classified: multi-doc analysis, document writing, or single call
   Cached stages reused from previous runs

8. STEP 3a: Reasoning Loop (per stage, max 5 iterations)
   For each stage:
     - Check cache (ArtifactCache) → skip if cached
     - If multi-doc (>3 files): ParallelAgentOrchestrator (3 concurrent, batched)
     - Else: llm.generate_as_agent() (kiro-cli with file access)
     - Auto-continue if output truncates (up to 3 continuations)
     - AnalystAgent scores against dispatch contract
     - If score >= 7.5: proceed to next stage
     - If failed: retry with analyst feedback (max 2 retries per stage)

9. STEP 4: Recitation Checkpoint (Level 3)
   Before final stage: re-state original question + stage summaries
   Prevents drift toward most verbose source (~200 words)

10. STEP 5: Parallel Evaluation (Level 3)
    Three evaluators run concurrently in ThreadPoolExecutor(max_workers=3):
    - Analyst: KB grounding, completeness, quality, structure (0-10, pass >= 7.5)
    - Reviewer: Workflow-specific rubric, strengths/issues (0-10, pass >= 6.0)
    - Evaluator: Alignment, evidence, completeness, actionability (1-5 each, pass >= 3)
    Merge into UnifiedEvaluation
    If any fails: one revision with combined feedback

11. STEP 6: Store Pattern (LearnerAgent)
    Extract lesson via LLM (one-line, max 150 chars)
    Store to doc/lessons_learned.md
    If score >= 8.0: store reasoning pattern with strategies

12. STEP 7: Write Output
    Format with metadata footer
    Write to spaces/{SPACE}/output/{workflow}_{timestamp}.md
    Log to logs/workflow_history.jsonl
```

## LLM Call Map

Every LLM call in a single workflow run, in execution order:

| # | Module | Call | When | Skippable? |
|---|--------|------|------|------------|
| 1 | dispatch_contract.py | Build contract | Complex queries only | Yes (heuristic fallback) |
| 2-N | invoker.py | generate_as_agent() | Per stage (main reasoning) | No (core work) |
| N+1 | analyst.py | Score reasoning | Per iteration in reasoning loop | No (quality gate) |
| N+2 | analyst.py | Score (parallel eval) | Post-composition | Skippable via config |
| N+3 | reviewer.py | Validate standards | Post-composition (parallel) | Skippable via config |
| N+4 | evaluator.py | 4-criteria check | Post-composition (parallel) | Skippable via config |
| N+5 | learner.py | Extract lesson | Post-completion | Skippable via config |
| N+6 | learner.py | Extract strategies | Post-completion (score >= 8) | Skippable via config |
| N+7 | learner.py | Summarize reasoning | Post-completion (score >= 8) | Skippable via config |

Calls N+2 through N+4 run concurrently (parallel eval). Calls N+5 through N+7 are post-completion learning and do not affect output quality.

## Key Components

### WorkflowInvoker
Static class that orchestrates the full workflow. Contains:
- Workflow registration and lookup
- Stage detection and splitting
- The main reasoning loop
- Parallel evaluation orchestration
- Output formatting and logging

### Core Modules
- **ContextGuard**: Monitors token usage, triggers reconstruction at 70%
- **Memory**: In-process shared state (facts, decisions, persona context, contract)
- **ThinkingModule**: Reasoning chains with hallucination detection
- **Controller**: Orchestrates thinking process, validates reasoning chains
- **LLMClient**: Unified client supporting Perplexity, Anthropic, OpenAI, kiro-cli
- **ArtifactCache**: Stage-level caching for multi-step workflows
- **ParallelAgentOrchestrator**: Batched concurrent document analysis

### Specialized Agents
- **ReaderAgent**: Scans knowledge/ directory, extracts content from matching files
- **AnalystAgent**: Scores reasoning quality against dispatch contract (0-10)
- **ReviewerAgent**: Validates against workflow-specific standards
- **LearnerAgent**: Warm-start patterns, lesson extraction, strategy storage

### Level 3 Modules
- **DispatchContract**: Pre-dispatch "what done looks like" definition
- **Evaluator**: Post-composition 4-criteria check (alignment, evidence, completeness, actionability)
- **Recitation**: Re-anchoring checkpoint before final composition stage
- **ParallelEval**: Concurrent Analyst + Reviewer + Evaluator orchestration
- **HarnessAudit**: Periodic threshold and assumption validation

## Workflow Definitions

| Workflow | Purpose | Required Input | Output |
|----------|---------|----------------|--------|
| explain | Explain concept using space's teaching style | topic | explain_{ts}.md |
| guide | Assignment guidance (no direct answers) | assignment | guide_{ts}.md |
| review | Review submission against standards | submission_path | review_{ts}.md |
| research | Full research workflow with lit mapping | task | research_{ts}.md |
| quant | Statistical analysis guidance | task | quant_{ts}.md |

## Configuration

```yaml
# config.yaml
workspace_dir: .
data_dir: data
spaces_dir: src/research_assistant/spaces

tokens:
  max_tokens: 10000
  threshold_percentage: 0.70
  warning_percentage: 0.60
  reconstruction_target: 0.30

ai:
  model: claude-3-sonnet
  temperature: 0.7
  max_response_tokens: 4000
  timeout_seconds: 60

logging:
  log_dir: data/logs
  log_level: INFO
```

Environment variable overrides: `RA_MAX_TOKENS`, `RA_TOKEN_THRESHOLD`, `RA_AI_MODEL`, `RA_AI_TEMPERATURE`, `RA_LOG_LEVEL`.

## Output Convention

All workflow outputs go to:
```
spaces/{SPACE}/output/{workflow}_{timestamp}.md
```

Intermediate artifacts go to:
```
spaces/{SPACE}/artifacts/{workflow}_{timestamp}/
```

Cached stages go to:
```
spaces/{SPACE}/cache/{workflow_id}/
```

## Usage Examples

```bash
# Explain a concept
ra explain "Brand Equity Model" --persona QNTR

# Review a submission
ra review submission.pdf --persona QNTR

# Get assignment guidance
ra guide "Case study approach" --persona QNTR

# Run full research workflow
ra research "Internal branding practices" --persona QNTR

# Statistical analysis guidance
ra quant "Regression analysis for survey data" --persona QNTR

# Run harness audit
ra audit --persona QNTR
```

---

## Change Log

### 2026-04-25: Cross-Space Knowledge, Session Memory, Layered Config, Agent Protocol

**Source**: Analysis of [AWSMantle genai-rewrite branch](https://code.amazon.com/packages/AWSMantle/trees/genai-rewrite) for applicable patterns.

**What changed and why**:

1. **Cross-Space Knowledge Access with Isolation**
   - *What*: Spaces can now declare read-only references to other spaces' knowledge bases via `cross_space_sources` in persona.yaml. A `CrossSpaceReader` loads knowledge from multiple spaces, tagging each piece with its source space. Learnings and patterns remain isolated per space.
   - *Why*: Research papers span multiple domains (CRO, QNTR/Literature Review, DBA). The system needed to pull knowledge across spaces without breaking isolation of learned patterns. Inspired by Mantle's cellular isolation principle ("once a request enters a cell, it stays in that cell") applied to knowledge boundaries.
   - *Performance*: Zero additional LLM calls. Reader already reads files; this expands which files it can read.
   - *Clarification behavior*: When cross-space references are ambiguous, the system flags `[CLARIFICATION NEEDED]` rather than assuming.

2. **Single-File Cross-Session Memory**
   - *What*: At workflow end, a `session_memory.md` file (~2K tokens) is written per space containing recent query summaries, top strategies, known preferences, and cross-space patterns. Loaded at next workflow start alongside lessons.
   - *Why*: Memory was in-process only; patterns and strategies were lost between CLI runs. Mantle's "single-file memory MVP" pattern (write markdown, load into system prompt) provides cross-session continuity with zero infrastructure.
   - *Performance*: Zero additional LLM calls in the common case. LLM summarization only triggers when the file exceeds 2K tokens (roughly every 10-15 runs).

3. **Layered Configuration with Runtime Overrides**
   - *What*: Config now supports CLI flags and environment variables for runtime parameters: `--skip-parallel-eval`, `--max-iterations`, `--cross-space`, `--skip-learner-llm`. A `performance` section in config controls these defaults.
   - *Why*: Changing evaluation thresholds or disabling features required editing files. This gives speed knobs for quick iterations (e.g., `ra explain "topic" -p QNTR --skip-parallel-eval --max-iterations 2`).
   - *Performance*: Strictly positive. Provides explicit controls to trade quality for speed.

4. **Formalized Agent Interface Protocol**
   - *What*: Python `Protocol` classes define typed input/output for each agent role. Startup validation checks agent wiring before the workflow runs.
   - *Why*: `BaseAgent.execute(**kwargs)` was too loose; agents could be wired wrong without errors until runtime. Inspired by Mantle's `Service` trait pattern where every service declares its interface.
   - *Performance*: Zero. Validation runs once at startup in microseconds.

**Files touched**: `agents/base.py`, `config.py`, `spaces/loader.py`, `agents/reader.py`, `agents/learner.py`, `workflows/invoker.py`, `cli.py`, each space's `persona.yaml`.

### 2026-04-28: Binary File Reading, Sub-Agent Contract, CognitiveInfrastructure, Kiro Evolve

**Source**: Gap analysis on binary file handling, plus adoption of tools from the Amazon Builder GenAI Power Users community wiki.

**What changed and why**:

1. **Binary File Reading Utility**
   - *What*: A `scripts/read_binary.py` utility extracts text from PDF, DOCX, and XLSX files via Python (PyPDF2, python-docx, openpyxl). Supports full extraction, page ranges, specific sheets, and metadata-only mode.
   - *Why*: The workflows (explain, review, research, guide, quant) and the IDE need to consume binary source material directly. The ReaderAgent already had basic PDF/DOCX/XLSX support with a 10K-char truncation; that was removed so full documents can be read when needed. Token budget management stays at the `extract_relevant()` orchestration layer, not the extraction layer.
   - *Applies to*: Both Kiro IDE sessions and all five workflows.

2. **Binary File Reading Steering Rule**
   - *What*: New steering file `.kiro/steering/binary-file-reading.md` covering: supported formats, extraction commands, no-conversion-files rule, sub-agent delegation protocol for large documents, and orchestrator verification requirements.
   - *Why*: Previously I would claim inability to read binary files and ask for text alternatives. The steering rule removes that fallback and mandates the Python extraction path.

3. **Sub-Agent Contract for Large Documents**
   - *What*: For documents over 15 pages or 30,000 characters, full-document processing is delegated to a sub-agent via `invokeSubAgent`. The contract specifies:
     - Input: full extracted text plus explicit task instruction
     - Output: structured response with page/section references for every claim, a completeness declaration, and zero fabrication
     - Conduct: no partial extraction, no summary-only responses, no vague statements
     - Orchestrator verification: spot-check 2-3 claims against the source, flag missing page references, reject and re-delegate thin outputs
   - *Why*: Loading a 25-page paper into the main context exhausts it before analysis can happen. Sub-agent delegation preserves the main context while ensuring full coverage of the source. The fabrication controls (page references, completeness declaration) make the sub-agent's output verifiable.
   - *Applies to*: Both IDE and workflows. The AnalystAgent's completeness and grounding checks align with this contract when source material is a binary file.

4. **Reference-Provided Context Rule Updated**
   - *What*: `.kiro/steering/reference-provided-context.md` point 3 updated to reference the binary extraction script instead of the prior "ask the user for a text alternative" fallback.
   - *Why*: Keeps the two steering rules (reference handling and binary file reading) consistent.

5. **CognitiveInfrastructure MCP Server**
   - *What*: Installed via `aim mcp install cognitive-infrastructure-mcp`. Provides three tools: `kiro-recall` (hybrid keyword + vector search over curated knowledge with local transformers.js embeddings), `workspace-search` (BM25 index over the full project workspace), and `tool-router` (MCP proxy that keeps context window clean).
   - *Configuration*: `VAULT_DIR` environment variable in `~/.kiro/settings/mcp.json` points to the ResearchAssistant workspace root. The SQLite recall database lives at `.kiro/recall.db` (git-ignored). Required `npm rebuild better-sqlite3` on macOS ARM64 since the shipped binary was built for AL2023_x86_64.
   - *Why*: As the literature collection grows beyond 50+ PDFs across multiple spaces, finding the right source by filename becomes infeasible. Vector search over curated knowledge lets me query "find all papers discussing principal-agent theory" without loading full documents. Workspace search covers everything outside curated knowledge (specs, outputs, communications, learnings). No AWS credentials required, everything runs locally.
   - *Applies to*: Both IDE and kiro-cli (workflows) via shared MCP config at `~/.kiro/settings/mcp.json`.

6. **Kiro Evolve (IDE-Adapted)**
   - *What*: Persistent memory system that captures Kiro IDE conversations to daily transcript files, proposes knowledge graduation based on recurring patterns, consolidates graduated knowledge periodically, and cleans up old transcripts. Adapted from the CLI-based Kiro Evolve by @alanroth to use Kiro IDE hooks (`promptSubmit`, `agentStop`, `userTriggered`) instead of kiro-cli agent configs.
   - *Components*:
     - Shell scripts in `scripts/kiro_evolve_*.sh` handle transcript capture and the review/dream/cleanup check logic
     - Three hooks in `.kiro/hooks/` trigger the scripts on session events
     - Steering rule `.kiro/steering/kiro-evolve-trigger.md` enables the on-demand "evolve" command
     - Graduated knowledge lives at `.kiro/steering/evolved/` and is auto-loaded by the workspace steering system
     - Transcripts live at `~/.kiro/transcripts/` (user-level, not git-tracked)
   - *Gates*: Review triggers after 50+ prompts and 2+ days since last review. Dream triggers after 14+ days and 5+ evolved files. Cleanup triggers every 90 days on reviewed old transcripts.
   - *Why*: Cross-session memory. Decisions and preferences (e.g., "Holgersson is marginal, drop it from the literature review") would otherwise be lost between sessions. Every approval is explicit, which keeps the steering system under user control.
   - *Applies to*: Kiro IDE sessions. Graduated steering files also apply when kiro-cli reads the same `.kiro/steering/` directory during workflow execution.

**Files added**:
- `scripts/read_binary.py`
- `scripts/kiro_evolve_save_transcript.sh`
- `scripts/kiro_evolve_check_review.sh`
- `scripts/kiro_evolve_check_dream.sh`
- `scripts/kiro_evolve_check_cleanup.sh`
- `.kiro/steering/binary-file-reading.md`
- `.kiro/steering/kiro-evolve-trigger.md`
- `.kiro/hooks/kiro-evolve-save-prompt.kiro.hook`
- `.kiro/hooks/kiro-evolve-save-response.kiro.hook`
- `.kiro/hooks/kiro-evolve-check-all.kiro.hook`
- `.gitignore`

**Files updated**:
- `src/research_assistant/agents/reader.py` (PDF truncation removed, extracts full documents by default)
- `.kiro/steering/reference-provided-context.md` (point 3: binary formats now handled via extraction script)
- `~/.kiro/settings/mcp.json` (CognitiveInfrastructure server registered with VAULT_DIR env)

**MCP server troubleshooting note**: CognitiveInfrastructure ships as a Brazil-built Linux package. On macOS, the `better-sqlite3` native module needs a local rebuild: `npm rebuild better-sqlite3` in the MCP server's package directory. The server also expects `VAULT_DIR` to point to an existing directory; setting it to the workspace root solves this.
