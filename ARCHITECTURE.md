# ResearchAssistant Architecture

## Core Concept
Multi-agent research workflow system where **personas** (professor simulations) orchestrate **agents** to process academic tasks, with outputs saved as `.md` files.

## Technical Design (Following adw-core-ws Pattern)

### Entry Points
```
CLI (ra command) → WorkflowInvoker → WorkflowRunner → Actions → Agents
```

### Directory Structure
```
src/research_assistant/
├── __init__.py
├── cli.py                    # Click-based CLI (entry point)
├── config.py                 # Configuration management
│
├── workflows/                # Workflow orchestration (adw-style)
│   ├── __init__.py
│   ├── invoker.py           # WorkflowInvoker (maps names to actions)
│   ├── runner.py            # WorkflowRunner (executes action sequences)
│   └── specs.py             # WorkflowSpec definitions
│
├── actions/                  # Individual workflow steps (adw-style)
│   ├── __init__.py
│   ├── base.py              # BaseAction (input/output contract)
│   ├── explain.py           # ExplainAction
│   ├── review.py            # ReviewAction
│   ├── guide.py             # GuideAction
│   ├── analyze.py           # AnalyzeAction
│   └── output.py            # OutputHandler (writes .md files)
│
├── core/                     # Core agents (ResearchAssistant original)
│   ├── __init__.py
│   ├── contextguard.py      # Token monitoring at 70% threshold
│   ├── memory.py            # Shared state across agents
│   ├── thinking.py          # Reasoning chains, hallucination detection
│   └── controller.py        # Orchestrates thinking process
│
├── agents/                   # Specialized agents
│   ├── __init__.py
│   ├── base.py              # BaseAgent with persona context
│   ├── reader.py            # Reads and extracts from knowledge base
│   ├── analyst.py           # Analyzes cases and research
│   ├── writer.py            # Generates content
│   ├── reviewer.py          # Reviews against standards
│   └── learner.py           # Learns from feedback
│
└── personas/                 # Persona definitions
    ├── __init__.py
    ├── loader.py            # PersonaLoader
    └── QNTR/                # Prof. Atul Prashar persona
        ├── persona.yaml     # Identity, behaviors, guidelines
        ├── prompts.yaml     # Agent-specific prompts
        ├── knowledge/       # Input: course materials
        │   ├── research_papers/
        │   ├── class_slides/
        │   └── assignments/
        └── output/          # Output: generated .md files
            └── {workflow_id}_{timestamp}.md
```

## Workflow Execution Flow

```
1. CLI Command
   ra explain "Brand Equity" --persona QNTR

2. WorkflowInvoker
   - Load persona (QNTR)
   - Map workflow name to WorkflowSpec
   - Validate required inputs
   - Create WorkflowRunner

3. WorkflowRunner
   - Initialize Memory with persona context
   - Execute actions in sequence
   - Track state between actions
   - Handle errors/rollback

4. Actions (use core agents)
   ExplainAction:
     - Reader: Extract relevant content from knowledge base
     - Controller: Orchestrate thinking with persona context
     - Writer: Generate explanation in persona voice
     - OutputHandler: Save to persona/output/{id}.md

5. Output
   personas/QNTR/output/explain_20260125_180000.md
```

## Key Components

### WorkflowInvoker (adw pattern)
- Maps workflow names to action sequences
- Validates inputs
- Handles sync/async execution
- Returns WorkflowResult with output_path

### Actions (adw pattern + research agents)
Each action:
- Receives ActionInput (persona, state, memory)
- Uses core agents (Controller, ContextGuard, Memory)
- Uses specialized agents (Reader, Writer, Reviewer)
- Returns ActionResult with artifacts

### Core Agents (ResearchAssistant original)
- **ContextGuard**: Monitors token usage, triggers reconstruction at 70%
- **Memory**: Shared state (facts, decisions, persona context)
- **Thinking**: Reasoning chains with hallucination detection
- **Controller**: Orchestrates thinking process

### Specialized Agents (persona-aware)
- **Reader**: Extracts from knowledge base using persona prompts
- **Writer**: Generates content in persona voice
- **Reviewer**: Validates against persona standards
- **Learner**: Captures feedback for persona improvement

### Output Convention
All workflow outputs go to:
```
personas/{PERSONA_NAME}/output/{workflow}_{timestamp}.md
```

## Workflow Definitions

### explain
Purpose: Explain concept using persona's teaching style
Actions: Reader → Controller → Writer → Output
Output: `explain_{timestamp}.md`

### review
Purpose: Review submission against persona standards
Actions: Reader → Reviewer → Writer → Output
Output: `review_{timestamp}.md`

### guide
Purpose: Provide assignment guidance (no direct answers)
Actions: Reader → Controller → Writer → Output
Output: `guide_{timestamp}.md`

### analyze
Purpose: Analyze case/research using persona frameworks
Actions: Reader → Analyst → Writer → Output
Output: `analysis_{timestamp}.md`

### research
Purpose: Full research workflow
Actions: Reader → Analyst → Writer → Reviewer → Output
Output: `research_{timestamp}.md`

## Configuration

```yaml
# ra_config.yaml
application:
  name: "Research Assistant"
  
paths:
  personas_dir: "personas"
  
defaults:
  persona: "QNTR"
  model: "claude-sonnet-4"
  
contextguard:
  threshold: 0.70
  reconstruction_enabled: true
```

## Usage Examples

```bash
# Explain a concept
ra explain "Brand Equity Model" --persona QNTR

# Review a submission
ra review submission.pdf --persona QNTR --rubric rubric.md

# Get assignment guidance
ra guide "Case study approach" --persona QNTR

# Run full research workflow
ra workflow research "Internal branding practices" --persona QNTR

# List personas
ra persona list

# Show persona info
ra persona info QNTR
