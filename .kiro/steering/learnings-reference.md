---
inclusion: fileMatch
fileMatchPattern: "**/learnings/**,**/agents/learner.py"
---

# Learnings Reference

When working on the learnings module or the LearnerAgent, reference these source documents:

## Source Articles
- Anthropic Evals: #[[file:src/research_assistant/learnings/agent_evals.md]]
- Agent Capabilities: #[[file:src/research_assistant/learnings/agent_capabilities.md]]
- Design Principles: #[[file:src/research_assistant/learnings/design_principles.md]]

## Key Concepts
- Progressive disclosure: load only what's needed, when needed
- Context window is finite: keep KB context under 40% of budget
- Lessons compound: each run should make the next one better
- Warm start: use patterns from similar past queries to bootstrap generation
