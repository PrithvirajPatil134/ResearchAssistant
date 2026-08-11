---
name: stress-test
description: Run the devil's advocate on a specific answer, draft, or claim on demand. Dispatches ra-post-stitch-eval to find the strongest argument against it, any unsourced claim, the weakest link in the reasoning, and the strongest omitted counterargument. Use when the user says "stress-test this", "play devil's advocate", "poke holes in this", "challenge that", or wants a claim/answer/draft adversarially checked before relying on it.
allowed-tools: Read, Bash, Glob, Grep, Agent
---

# Stress-test (devil's advocate on demand)

Runs the same adversarial pass that gates pipeline deliverables, but on whatever
the user points at right now: my last answer, a draft file, or a specific claim.
This is the explicit, on-demand twin of the `devils-advocate-self-dispatch`
steering rule.

## What to stress-test

Determine the target from the user's message:

- **"stress-test this" / "poke holes in this"** with no other reference → my most
  recent substantive answer in this conversation.
- **A file path or open editor file** → that file.
- **A quoted claim or a claim in their message** → that specific claim.

If the target is ambiguous, ask which one before dispatching. Do not guess.

## How to run it

1. Assemble the target text (my prior answer, the file contents, or the claim)
   and the original question or purpose it serves.
2. Dispatch `ra-post-stitch-eval` via the Agent tool (`run_in_background: false`)
   with this input:
   - The target text.
   - The question/purpose it is meant to serve.
   - Standards to hold it to: `.kiro/steering/no-assumption-rule.md` and
     `.kiro/steering/human-authored-writing.md`.
   - Ask for: the single strongest argument against the target's central point;
     every claim that does not trace to a source (per the no-assumption rule);
     the weakest link in the reasoning with a concrete fix; and the strongest
     counterargument the target omits. Quote 10-30 words for any tone risk.
3. If a file was the target and a research space is active, also let the agent
   read the relevant wiki sources so it can check sourcing against them.

## How to report back

Surface the findings directly, most serious first. Lead with anything that would
change the conclusion (an unsourced claim, a broken inference), then the
weaker-signal notes. If the agent found no material weakness, say so plainly.
Never dump the raw eval JSON at the user; translate it into prose.

If the target was my own prior answer and the pass found a real problem, correct
the answer, do not just report the flaw.

## Honesty

This runs one adversarial agent pass (~20-60s). It is a critique layer, not a
rewrite loop: it finds weaknesses, it does not silently rewrite the target. It is
the same `ra-post-stitch-eval` agent used by the long-doc pipeline and the
short-workflow gate in `claude-dispatch.sh`.
