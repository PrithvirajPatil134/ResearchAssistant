# Orchestrator Failures (Recent, 7-Day Window)

<!-- Cap: 1000 tokens. Entries older than 7 days are pruned on each learner run. -->
<!-- Format: ### Pattern Name / **Trigger** / **Diagnosis** / **Action** / **Observed**: YYYY-MM-DD -->

### Template-Over-Source in "How to Proceed" Responses

**Trigger**: User asks "how to proceed" after a communication file (email thread, advisor feedback) is read. The file contains resolved decisions and answered questions.

**Diagnosis**: Agent generated next-steps from a generic research-project template rather than grounding each recommendation against the specific content already in the thread. Result: recommended actions that were already resolved (clarify scope when scope was clarified; gather PDFs when PDFs were already provided).

**Action**: Before generating any action list, extract RESOLVED decisions, ANSWERED questions, and PROVIDED resources as quoted text. Only then identify genuinely OPEN items. Cross-check every proposed action against the extracted lists before including it.

**Observed**: 2026-05-09
