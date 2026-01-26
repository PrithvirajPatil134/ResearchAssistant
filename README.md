# Research Assistant

AI-powered research workflow automation with persona-based agents.

## Overview

Research Assistant follows the **adw-core-ws** technical design pattern while implementing a multi-agent research workflow system. Personas (professor simulations) orchestrate agents to process academic tasks, with all outputs saved as `.md` files.

## Architecture

```
CLI (ra) → WorkflowInvoker → Actions → Core Agents → Output (.md)
```

### Key Components

- **Personas**: Define behavior, knowledge base, and prompts (e.g., QNTR = Prof. Atul Prashar)
- **Workflows**: Predefined action sequences (explain, review, guide, research)
- **Actions**: Individual workflow steps that use agents
- **Core Agents**: ContextGuard, Memory, Thinking, Controller
- **Outputs**: Generated `.md` files in `personas/{PERSONA}/output/`

## Installation

```bash
cd ResearchAssistant
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

# List available workflows
ra workflow list

# List available personas
ra persona list

# Show persona details
ra persona info QNTR
```

### Python API

```python
from research_assistant import WorkflowInvoker

# Run explain workflow
result = WorkflowInvoker.invoke(
    workflow_name="explain",
    persona_name="QNTR",
    initial_state={"topic": "Brand Equity"},
)

if result.success:
    print(f"Output: {result.output_path}")
else:
    print(f"Error: {result.error}")
```

## Available Workflows

| Workflow | Description | Required Inputs |
|----------|-------------|-----------------|
| `explain` | Explain concept using persona's teaching style | topic |
| `review` | Review submission against persona standards | submission_path |
| `guide` | Provide assignment guidance (no direct answers) | assignment |
| `research` | Full research workflow with analysis | task |

## Output Convention

All workflow outputs are saved to:
```
personas/{PERSONA_NAME}/output/{workflow}_{timestamp}.md
```

Example:
```
personas/QNTR/output/explain_20260125_181500.md
personas/QNTR/output/review_20260125_182000.md
```

## Personas

### QNTR (Prof. Atul Prashar)

- **Domain**: Marketing Academia
- **Institution**: IIM Sambalpur
- **Expertise**: Brand Management, Internal Branding, Digital Transformation
- **Research Interests**: Corporate Brand Management, Brand Communities

### Adding a New Persona

1. Create directory: `personas/{NAME}/`
2. Add `persona.yaml` (identity, behaviors, guidelines)
3. Add `prompts.yaml` (agent-specific prompts)
4. Add `knowledge/` directory with course materials
5. Outputs will auto-generate to `output/`

## Project Structure

```
src/research_assistant/
├── cli.py                  # CLI entry point
├── config.py               # Configuration
├── workflows/
│   ├── invoker.py          # WorkflowInvoker (adw-style)
│   └── __init__.py
├── core/                   # Core agents
│   ├── contextguard.py     # Token monitoring (70% threshold)
│   ├── memory.py           # Shared state
│   ├── thinking.py         # Reasoning chains
│   └── controller.py       # Orchestration
├── agents/                 # Specialized agents
│   ├── base.py
│   ├── learner.py
│   └── reviewer.py
└── personas/
    └── QNTR/
        ├── persona.yaml
        ├── prompts.yaml
        ├── knowledge/      # Input: course materials
        └── output/         # Output: generated .md files
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy src/

# Linting
ruff check src/
```

## License

MIT
