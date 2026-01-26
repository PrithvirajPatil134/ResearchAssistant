# Agent Architecture

## Overview

This system uses **5 LLM Agents** and **4 Modules** to process research queries within a **Space** guided by a **Mentor**.

## Terminology

- **Space**: A knowledge domain with its own knowledge base (KB)
- **Mentor**: The guide/expert context for the space (not a voice, but a reference)
- **Agent**: Uses LLM for decision-making and content generation
- **Module**: Performs deterministic operations without LLM

---

## Workflow

```
User Query
    │
    ▼
┌────────────────────────────────────────────────────────────────┐
│                    CONTROLLER (Module)                          │
│    Orchestrates workflow, prevents hallucination, tracks state │
└───────────────────────────────┬────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────┐
│                      READER (Module)                            │
│              Extract content from Space KB                      │
│           Parse: DOCX, PDF, Excel, TXT, MD                     │
└───────────────────────────────┬────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────┐
│                    LEARNER AGENT (LLM)                          │
│        Retrieve patterns/strategies from past queries          │
│              Provide warm-start to Thinker                     │
└───────────────────────────────┬────────────────────────────────┘
                                │
    ┌───────────────────────────┴───────────────────────────────┐
    │                    REASONING LOOP                          │
    │                                                            │
    │   ┌────────────────────────────────────────────────────┐  │
    │   │               THINKER AGENT (LLM)                   │  │
    │   │  • Understand user expectation                      │  │
    │   │  • Connect KB content to query                      │  │
    │   │  • Surf web if KB insufficient                      │  │
    │   │  • Create structured reasoning plan                 │  │
    │   └─────────────────────────┬──────────────────────────┘  │
    │                             │                              │
    │                             ▼                              │
    │   ┌────────────────────────────────────────────────────┐  │
    │   │             IMPLEMENTER AGENT (LLM)                 │  │
    │   │  • Execute Thinker's plan                          │  │
    │   │  • Generate actual content                          │  │
    │   │  • Synthesize KB + web sources                      │  │
    │   │  • Maintain mentor alignment                        │  │
    │   └─────────────────────────┬──────────────────────────┘  │
    │                             │                              │
    │                             ▼                              │
    │   ┌────────────────────────────────────────────────────┐  │
    │   │               ANALYST AGENT (LLM)                   │  │
    │   │  • Verify reasoning against context                 │  │
    │   │  • Validate claims (can surf web)                   │  │
    │   │  • Score: KB grounding + coherence + query fit      │  │
    │   │  • Pass threshold: >= 9.0                           │  │
    │   └─────────────────────────┬──────────────────────────┘  │
    │                             │                              │
    │              ┌──────────────┴──────────────┐               │
    │              │                             │               │
    │              ▼                             ▼               │
    │         Score < 9.0                   Score >= 9.0        │
    │              │                             │               │
    │              ▼                             │               │
    │     Loop to THINKER                        │               │
    │     with feedback                          │               │
    │              │                             │               │
    └──────────────┴─────────────────────────────┘               │
                                                 │
                                                 ▼
┌────────────────────────────────────────────────────────────────┐
│                       WRITER (Module)                           │
│                 Format and write output                         │
└───────────────────────────────┬────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────┐
│                    REVIEWER AGENT (LLM)                         │
│  • Validate output answers original query                       │
│  • Check completeness and quality                               │
│  • Final approval gate                                          │
└───────────────────────────────┬────────────────────────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │                                   │
              ▼                                   ▼
          REJECTED                            APPROVED
              │                                   │
              ▼                                   ▼
    Loop to THINKER               ┌────────────────────────────┐
    with feedback                 │ PUBLISH to /output          │
                                  └────────────┬───────────────┘
                                               │
                                               ▼
┌────────────────────────────────────────────────────────────────┐
│                    LEARNER AGENT (LLM)                          │
│  • Extract insights from workflow                               │
│  • Store successful strategies                                  │
│  • Learn from failures                                          │
│  • Improve future Thinker performance                           │
└────────────────────────────────────────────────────────────────┘

---

## Components

### Agents (5) - Use LLM

| Agent | Responsibility | Web Access |
|-------|---------------|------------|
| **Thinker** | Create reasoning plan from KB + query | ✅ Yes |
| **Implementer** | Execute plan, generate content | ❌ No |
| **Analyst** | Verify reasoning, score quality | ✅ Yes |
| **Reviewer** | Validate output vs input | ❌ No |
| **Learner** | Extract patterns, improve future runs | ❌ No |

### Modules (4) - No LLM

| Module | Responsibility |
|--------|---------------|
| **Controller** | Orchestrate workflow, prevent hallucination |
| **Reader** | Parse KB files (DOCX, PDF, Excel, TXT) |
| **Writer** | Format and write final output |
| **ContextGuard** | Track token usage, manage context |

---

## Loop Configuration

```
MAX_REASONING_ITERATIONS = 5  # Thinker → Analyst loop
MAX_VALIDATION_ITERATIONS = 2  # Reviewer rejection loop
PASS_THRESHOLD = 9.0           # Analyst score to pass
```

---

## Prompt Files

Each agent has a dedicated prompt file defining:
- Role and responsibilities
- Input/Output format
- Guidelines and anti-hallucination rules

```
prompts/
├── thinker.md
├── implementer.md
├── analyst.md
├── learner.md
└── reviewer.md
