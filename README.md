# Research Assistant

AI-powered research workflow automation with persona-based agents.

## Overview

Research Assistant follows the **adw-core-ws** technical design pattern while implementing a multi-agent research workflow system. Personas (professor simulations) orchestrate agents to process academic tasks, with all outputs saved as `.md` files.

The system implements **Level 3 context engineering** — designing the information architecture, feedback loops, evaluation criteria, and context lifecycle across the entire agent session, not just optimizing individual agent calls.

## Architecture

```
CLI (ra) → WorkflowInvoker → Contract → Actions → Core Agents → Parallel Eval → Output (.md)
```

### Key Components

- **Personas**: Define behavior, knowledge base, and prompts (e.g., QNTR = Prof. Atul Prashar)
- **Workflows**: Predefined action sequences (explain, review, guide, research, quant)
- **Core Agents**: ContextGuard, Memory, Thinking, Controller
- **Level 3 Modules**: DispatchContract, Evaluator, Recitation, ParallelEval, HarnessAudit
- **Outputs**: Generated `.md` files in `spaces/{PERSONA}/output/`

### Level 3 Context Engineering

Five structural upgrades from Level 2 (agent orchestration) to Level 3 (harness/context engineering):

| Module | Purpose | Failure Mode Prevented |
|--------|---------|----------------------|
| DispatchContract | Defines "what done looks like" before agents run | Technically correct but contextually wrong output |
| Evaluator | Grades output on 4 criteria (alignment, evidence, completeness, actionability) | Self-praise — agents rating their own work highly |
| Recitation | Re-anchors attention on original intent before composition | Drift toward most verbose source in multi-stage workflows |
| ParallelEval | Runs Analyst + Reviewer + Evaluator concurrently | Sequential evaluation latency (~60-70% reduction) |
| HarnessAudit | Audits thresholds and assumptions on model change | Stale thresholds after model improvements |

## Installation

```bash
pip install -e .
```

## Usage

### CLI Commands

```bash
# Explain a concept using persona's teaching style
ra explain "Brand Equity Model" --persona QNTR

# Review a submission against persona's standards
ra review assignment.pdf --persona QNTR

# Get assignment guidance (no direct answers)
ra guide "How to approach the case study" --persona QNTR

# Run a named workflow
ra workflow run research "Internal branding" --persona QNTR

# Run harness audit (Level 3)
ra audit --persona QNTR

# List available workflows
ra workflow list

# List available personas
ra persona list
```

### Python API

```python
from research_assistant import WorkflowInvoker

result = WorkflowInvoker.invoke(
    workflow_name="explain",
    persona_name="QNTR",
    initial_state={"topic": "Brand Equity"},
)

if result.success:
    print(f"Output: {result.output_path}")
    print(f"Score: {result.final_score}")
```

## Workflow Execution Flow

```
1. Read KB files (ReaderAgent)
2. Build Dispatch Contract (Level 3) — defines "done"
3. Warm Start (LearnerAgent) — load patterns from previous runs
4. Reasoning Loop (max 5 iterations):
   - Generate content (ThinkingModule + LLM)
   - Score against contract (AnalystAgent)
   - If score >= 7.5: proceed
5. Recitation Checkpoint (Level 3) — re-anchor on original intent
6. Format Output
7. Parallel Evaluation (Level 3):
   - Analyst scores reasoning quality
   - Reviewer checks standards compliance
   - Evaluator grades intent alignment (4 criteria)
   - All three run concurrently
8. If any evaluator fails: revise with combined feedback
9. Store pattern (LearnerAgent)
10. Write output file
```

## Available Workflows

| Workflow | Description | Required Inputs |
|----------|-------------|-----------------|
| `explain` | Explain concept using persona's teaching style | topic |
| `review` | Review submission against persona standards | submission_path |
| `guide` | Provide assignment guidance (no direct answers) | assignment |
| `research` | Full research workflow with analysis | task |
| `quant` | Statistical analysis guidance | task |

## Project Structure

```
src/research_assistant/
├── cli.py                  # CLI entry point
├── config.py               # Configuration
├── workflows/
│   ├── invoker.py          # WorkflowInvoker (orchestration)
│   └── __init__.py
├── core/                   # Core + Level 3 modules
│   ├── contextguard.py     # Token monitoring (70% threshold)
│   ├── memory.py           # Shared state
│   ├── thinking.py         # Reasoning chains
│   ├── controller.py       # Orchestration
│   ├── parallel_agents.py  # Parallel document analysis
│   ├── dispatch_contract.py # Pre-dispatch contract (L3)
│   ├── evaluator.py        # Post-composition evaluation (L3)
│   ├── recitation.py       # Attention re-anchoring (L3)
│   ├── parallel_eval.py    # Concurrent evaluation (L3)
│   └── harness_audit.py    # Assumption auditing (L3)
├── agents/                 # Specialized agents
│   ├── base.py
│   ├── reader.py
│   ├── analyst.py          # Contract-aware scoring
│   ├── reviewer.py         # Contract-aware review
│   └── learner.py
└── spaces/
    └── QNTR/
        ├── persona.yaml
        ├── prompts.yaml
        ├── knowledge/      # Input: course materials
        └── output/         # Output: generated .md files
```

## Binary File Support

PDFs, DOCX, and XLSX files are read directly via `scripts/read_binary.py`. Full-document extraction is the default; page ranges and sheet-specific extraction are available via flags:

```bash
# Full extraction
python3 scripts/read_binary.py paper.pdf

# Page range for a large PDF
python3 scripts/read_binary.py paper.pdf --pages 1-10

# Metadata only (page count, sheet names)
python3 scripts/read_binary.py data.xlsx --meta
```

For documents over 15 pages, the IDE and workflows delegate full-document processing to a sub-agent with a strict contract: page references for every claim, completeness declaration, zero fabrication. See `.kiro/steering/binary-file-reading.md`.

## Persistent Memory (Optional)

Two community tools are integrated:

**CognitiveInfrastructure** (via AIM): MCP server providing hybrid keyword and vector search (`kiro-recall`) over curated knowledge and BM25 search (`workspace-search`) over the full workspace. Install with `aim mcp install cognitive-infrastructure-mcp`. On macOS, rebuild the native module: `npm rebuild better-sqlite3` in the MCP server's package directory. Configure via `VAULT_DIR` in `~/.kiro/settings/mcp.json`.

**Kiro Evolve** (IDE-adapted): Captures Kiro IDE conversations to daily transcripts, proposes knowledge graduation after 50+ prompts, consolidates graduated knowledge every 14 days. Transcripts live at `~/.kiro/transcripts/`; graduated knowledge lives at `.kiro/steering/evolved/` and auto-loads into future sessions. Say "evolve" in any session for on-demand review.

## Development

```bash
pip install -e ".[dev]"
pytest
mypy src/
ruff check src/
```

## License

MIT
