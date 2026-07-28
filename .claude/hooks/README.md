# Claude Code hooks

Hook scripts run by Claude Code, registered in `../settings.json` under the
`hooks` key. These are the Claude Code translations of the Kiro hooks in
`.kiro/hooks/` (which Claude Code does not read). The Kiro originals are kept for
the Kiro runtime; these are the active path under Claude Code.

See `docs/workspace-upgrade/` for the full Kiro→CC migration record.

## Registered hooks

| Script | Event | Matcher | Purpose |
|---|---|---|---|
| `wiki-lookup.sh` | UserPromptSubmit | (none) | Injects the 6-category task-grounding protocol so drafting/communication/infrastructure/research/ingest work is grounded in the wiki before responding. Translates Kiro `wiki-lookup-before-drafting`. |
| `writing-gate.sh` | PostToolUse | `Edit\|Write\|MultiEdit` | On a submission-ready write, emits `additionalContext` to scan against `.kiro/steering/human-authored-writing.md`. Consolidates Kiro `check-agent-writing` + `check-submission-writing`. |
| `py-lint.sh` | PostToolUse | `Edit\|Write\|MultiEdit` | `py_compile` on agent/workflow/core Python; exit 2 + stderr surfaces syntax errors to Claude. Translates Kiro `lint-agents`. |

Also registered in `settings.json` but living in `scripts/`:
`SessionStart → scripts/discover-claude-context.sh` (generates the lean CLAUDE.md).

## Mechanism notes (from code.claude.com/docs/en/hooks)

- `UserPromptSubmit` ignores matchers and always fires; plain stdout on exit 0 is
  injected as context. `wiki-lookup.sh` writes factual statements (not imperatives)
  to avoid tripping prompt-injection defenses. Output stays under the 10k cap.
- `PostToolUse` fires AFTER the tool runs and cannot block it. Feedback reaches
  Claude via `additionalContext` (non-blocking) or exit 2 + stderr (surfaced as an
  error for next-turn self-correction).
- Hooks read event JSON on stdin; file tools expose the path at
  `tool_input.file_path` (parsed via `jq`, with a grep fallback).

## Known coverage limit (tracked as Wave 6)

`writing-gate.sh` and `py-lint.sh` are main-session `PostToolUse` hooks. Writes
made by dispatched subagents (their own Write tool) or by shell scripts
(`long-doc-orchestrate.sh`) do NOT trigger the main session's PostToolUse hook.
For the long-doc pipeline, the writing standard is enforced separately by the
`ra-pre-stitch-eval` / `ra-post-stitch-eval` / `ra-prose-editor` agents. See
`docs/workspace-upgrade/upgrade-plan.md` Wave 6 for the plan to close this gap
(subagent-scoped hooks or verified eval-agent enforcement).

## Testing a hook manually

Feed representative event JSON on stdin:

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"src/research_assistant/spaces/QNTR/output/Paper_Submission.md"}}' \
  | .claude/hooks/writing-gate.sh
```

Registration changes in `settings.json` take effect at the next SessionStart.
