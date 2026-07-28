---
name: longdoc
description: Produce a submission-ready long document (research paper, literature review, thesis proposal/chapter, technical guide) via the multi-phase long-doc pipeline.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
---

# Long document production

Manual-only (`/longdoc`). This launches an expensive multi-phase, multi-agent
pipeline with side effects (writes to `spaces/{SPACE}/output/`, dispatches many
1M-context subagents). Never auto-run it — the user controls timing.

## Source of truth

- `WORKFLOW_GUIDE.md` (Long Document Production Workflow section) — when to use,
  flags, pause/resume, output location.
- `docs/long_document_production_system.md` — full 9-phase design, 4-mode system,
  quality gates, two-learner architecture.
- `scripts/long-doc-orchestrate.sh` — the actual coordinator. It governs.

## How to invoke

The orchestrator takes positional args then options:

```
bash scripts/long-doc-orchestrate.sh <doc-id> <space> <doc-type> <prompt-file> [options]
```

- `<doc-id>`: unique slug for this run (e.g. `agentic-gov-litreview-v1`).
- `<space>`: QNTR | CRO | DBA | CW.
- `<doc-type>`: research_paper | literature_review | thesis_proposal |
  thesis_chapter | technical_guide | term_paper | case_study | teaching_note |
  conference_paper.
- `<prompt-file>`: a minimal brief at `data/drafts/{doc-id}_prompt.md` stating
  document type, target length/word budget, description, key sources.
- Options: `--mode parallel|sequential|both` (default: auto-selected from word
  budget — omit unless overriding), `--pause-after outline|sections|stitch`,
  `--resume-from <phase>`, `--no-benchmark`, `--simulate-reviewers <names>`.

## Before running

1. Confirm the target space's wiki has the sources the document needs (the brain
   assembler reads the wiki; thin wiki → thin document).
2. Create the prompt file first. Do not run without it.
3. Mode is auto-selected from the word budget in the prompt file
   (`<2000`→single-raw, `2000-8000`→single-brain, `>8000`→learning-based). Only
   pass `--mode` to override.
4. Obeys `.kiro/steering/no-assumption-rule.md` and `human-authored-writing.md`
   throughout; the pipeline's own eval gates enforce sourcing and voice.

## After running

Output lands at `spaces/{SPACE}/output/{doc-slug}_v1.md` with devil's-advocate
notes and a benchmark report. Capture the user's verdict with
`scripts/capture-user-verdict.sh` so the writing-team learner calibrates.