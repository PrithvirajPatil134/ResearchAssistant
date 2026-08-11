---
inclusion: always
---

# Devil's Advocate Self-Dispatch (chat responses)

Every substantive answer I give in this IDE should be stress-tested before the
user relies on it. Pipeline deliverables already pass a devil's-advocate gate
(`ra-post-stitch-eval` in the long-doc pipeline; the Step 5b gate in
`claude-dispatch.sh` for the five short workflows). This rule closes the last
gap: the analytical answers I produce directly in chat, which pass through no
gate on their own.

## The Rule

Before delivering a substantive answer, dispatch a devil's-advocate pass on my
own draft and fold what it finds into the response (or surface it plainly).
"Substantive" means the answer contains any of:

- Analysis, an interpretation, or an argument the user will act on
- A recommendation or a judgment call (what to do, which option, whether X holds)
- Factual claims, numbers, dates, names, or citations
- A research, methodology, or infrastructure conclusion ("our pipeline does X",
  "the literature shows Y", "this construct has validated measures")

## What does NOT trigger it

Skip the pass for turns where a critique adds nothing: quick lookups, file
reads, confirmations ("done", "yes", "the file is at X"), status updates,
mechanical edits, and clarifying questions back to the user. The pass costs a
full subagent call (roughly 20-60s); do not spend it on a trivial turn. When in
doubt on a borderline answer, run it.

## Mechanism

1. Draft the answer.
2. Dispatch `ra-post-stitch-eval` via the Agent tool (`run_in_background: false`)
   with: my draft, the user's original question, and the standards it should hold
   the draft to (`no-assumption-rule.md`, `human-authored-writing.md`). Ask it for
   the strongest argument against my conclusion, any unsourced claim, the weakest
   link in my reasoning, and the strongest counterargument I omitted.
3. Fold the result in. If it found a real problem, fix the answer before sending.
   If the challenge is worth the user seeing, surface it under a short
   **"Devil's advocate:"** line rather than burying it. If the pass found nothing
   substantive, a one-line note ("stress-tested, no material weakness found") is
   enough. Never present the raw eval JSON.

## Honesty about this rule

This is a behavioral rule, not a hard gate. It relies on adherence the same way
the no-assumption rule does. For a specific answer the user wants challenged on
demand, the `/stress-test` skill runs the same pass explicitly. If the user
wants it truly unskippable on every turn, that requires a Stop hook, which
appends critique after the answer has already streamed (its latency and
loop trade-offs were the reason this behavioral path was chosen instead).

## Relationship to other gates

- Short workflows (explain/guide/review/research/quant): gated in
  `claude-dispatch.sh` Step 5b (deterministic gate scripts + `ra-post-stitch-eval`).
- Long documents (>5pp): gated by `ra-post-stitch-eval` in `long-doc-orchestrate.sh`.
- Chat responses: this rule, plus `/stress-test` on demand.

See [[reviewer-facing-writing-enforcement]] and [[scope-claims-to-what-was-verified]].
