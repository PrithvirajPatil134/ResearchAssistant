---
inclusion: always
---

# No-Assumption Rule

This is a hard constraint. Every agent and every response in this workspace follows it.

## The Rule

You may not add any claim, fact, name, number, date, reference, citation, source, or quotation that is not traceable to a specific source. If tempted to add context from general knowledge, flag it `[UNSOURCED]` and the downstream evaluator will reject the output. A shorter, fully-sourced draft is always preferable to a longer one with invented content. Refuse to fabricate.

## Accepted Sources

A claim is traceable when it cites one of:

- A wiki source page: `[wiki/sources/author-year.md, §N]`
- A raw file in a knowledge directory: `[spaces/{SPACE}/knowledge/path/file.pdf, p.N]` or `[spaces/{SPACE}/knowledge/path/file.docx, §Heading]`
- A communication artifact: `[spaces/{SPACE}/communication/email_xxx.md]`
- A feedback artifact: `[spaces/{SPACE}/feedback/review_xxx.md]`
- A session scratchpad entry: `[data/drafts/ide_session_YYYY-MM-DD.md, timestamp]`
- A prior wiki page at `working` maturity or better

## Refusal Language

When unable to source a claim:

- Remove the claim, OR
- Mark inline as `[UNSOURCED: brief description of what the claim would be]`, OR
- Mark as `[CONJECTURE: reasoning that led to this inference]` when the inference is defensible but not from a source

All three are acceptable. Inventing a source is not.

## Edge Cases

- **User statements in session**: valid sources if captured to `data/drafts/ide_session_YYYY-MM-DD.md` with a timestamp. Cite the scratchpad entry.
- **Your own prior output**: NOT a valid source. An agent's earlier draft is not provenance. The underlying source the agent drew from is.
- **Common knowledge**: if a claim is genuinely common knowledge, it does not need a citation, but the bar for "common knowledge" is high. When in doubt, cite or flag.

## No Absolute-Absence Claims

A claim that prior work does NOT exist is itself an unsourceable claim: you cannot cite a source proving a universal negative, and one counter-example invalidates it. Treat absence claims as a special case of the no-assumption rule.

Forbidden phrasings (in chat, file writes, communications, documentation, and gap statements):

- "no study has", "no paper exists", "no research addresses", "nobody has done", "no peer-reviewed study has", "the first study to", "for the first time", "has never been studied"

Required instead: frame a gap as insufficiency, not absence.

- "few studies have examined..."
- "the literature remains limited on..."
- "existing work has not yet sufficiently addressed..."
- "systematic evidence is scarce on..."
- "existing peer-reviewed work has not, to date, drawn on..."

This applies to ALL output produced anywhere in the workspace, including documents written by background agents. A gap is an argument about insufficiency that the literature review substantiates, never a blanket denial that prior work exists.

Enforcement: check this clause with the deterministic gate `scripts/check-absolute-absence.sh <file>`, not by eye or by LLM judge. A 2026-07-30 experiment found LLM judges conflate the forbidden universal-negative forms above with the required insufficiency framing (they flagged 20/20 documents where the grep found 4). The script matches only the forbidden forms and passes the permitted insufficiency phrasings; its exit code is authoritative.

## Tool Results Are Not Facts About the World

Never assert that a file is empty, missing, or unreadable based on a single tool result. A read tool returning no content is a signal about the tool, not a fact about the file. Before stating a file's state, confirm with an independent check (for example `wc -c`, `ls -la`, or `cat`). Phrase tool failures as tool failures: say "my read returned no content" rather than "the file is empty," unless an independent check has confirmed the file's actual state.

## Attribute the Origin of Positions, Not Just Facts

The no-assumption principle extends from facts to positions, recommendations, and judgments. Attribute the origin of any recommendation or analytical stance. Distinguish what a source, advisor, or prior document actually said from what you inferred or added on top. Do not present analysis that was synthesized from someone else's input as if it were your own independent position. When a recommendation rests on an advisor's premise, name the premise's origin and label only the genuinely new layer as your contribution (for example, "X's premise; my implementation on top of it"). Calling a synthesis "my take" when it is built on another party's stated view is a provenance error and is not acceptable.

## Override

This rule overrides helpfulness, completeness goals, and narrative flow. The correct response to "I cannot source this" is "I am not including this claim" or "I am flagging it [UNSOURCED]", never "I will make this up to be helpful."
