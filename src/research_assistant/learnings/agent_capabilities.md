# Agent Capability Design

Sources:
- [The Agent Capability Menu: What to Give Your Agent (and When)](https://w.amazon.com/bin/view/JahoodBlog/2025/12-12-agents-tools-skills-powers)
- [Prompts vs Skills vs MCP Tools vs Agents: When to Use What](https://w.amazon.com/bin/view/Ssamptur/blog/Prompts_Skills_MCP_Tools_AI_Agents)

## The Capability Spectrum

| Type | What it provides | Loading pattern | Use when |
|------|-----------------|-----------------|----------|
| Context files | Guidelines, reference | Eager (session start) | Agent always needs this info |
| Tools | Actions (APIs, file ops) | Eager (session start) | Need external system access |
| Prompts | Structured workflows | On user invoke | Clear workflow, user-triggered |
| Skills | Scripts + guidance | Progressive (on-demand) | Repeatable reasoning tasks |
| Powers | Tools + context | Progressive (on-demand) | Domain expertise needed sometimes |

## Four Properties of Effective Context

1. **Correctness**: Information must accurately represent reality.
2. **Relevance**: Must relate directly to the current task. Tangential content dilutes signal.
3. **Structure**: Must be formatted so the model can parse it. Clear headers, consistent naming, XML tags.
4. **Timing**: Must arrive when needed. Don't load everything upfront; don't load too late.

## Key Principles for Our Workflow

### 1. Progressive Disclosure Over Eager Loading
> "Skills use a two-part structure — frontmatter and detailed instructions. The agent only sees compact frontmatter, not the full prompt."

**Applied**: Our KB reader shouldn't dump all knowledge files into context. Load summaries first, then deep-dive into relevant files only.

### 2. Context Window is a Finite Budget
> "Keep usage around 10% and avoid exceeding 40%."

**Applied**: Our ContextGuard (100K token budget) should actively manage what's loaded. A massive case study prompt + all KB files + all benchmark cases can easily blow the budget.

### 3. Start Simple, Add Complexity When Needed
> "Start with a context file and a prompt. See how the agent behaves. Add skills or powers when you hit context pressure."

**Applied**: For simple explain queries, don't run the full 5-iteration reasoning loop. Estimate complexity first, then choose the right depth.

### 4. Ingredients vs Recipes
> "Think of agent composition like cooking. You have ingredients (individual capabilities) that you combine into recipes (purpose-built agent configurations)."

**Applied**: Our workflow agents (Reader, Analyst, Reviewer, Learner) are ingredients. The workflow spec (explain, guide, review) is the recipe. Keep them composable.

### 5. Don't Over-Engineer
> "The goal isn't to use the most sophisticated tool available but to solve the problem effectively with the least complexity necessary."

**Applied**: Not every query needs 5 reasoning iterations + 2 validation passes. Simple questions should get simple, fast answers.

### 6. Skills + Tools = Better Together
> "Skills handle the reasoning and formatting locally, while CLI and MCP tools handle data retrieval and external system interactions."

**Applied**: Our persona system (reasoning/formatting) + KB reader (data retrieval) follows this pattern. Keep them complementary, not overlapping.

## Common Mistakes to Avoid

1. **Overloading context at session start** — Don't load all KB files for every query.
2. **Using the wrong capability type** — Don't build complex agent orchestration for a simple prompt task.
3. **Poor descriptions for progressive capabilities** — Agent needs clear signals for when to activate what.
4. **Not iterating based on agent behavior** — Watch how the agent behaves, refine accordingly.
5. **Bundling too much into one capability** — Keep capabilities focused and composable.
