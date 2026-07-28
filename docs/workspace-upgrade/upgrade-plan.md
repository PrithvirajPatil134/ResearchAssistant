# Upgrade Plan — Kiro → Claude Code

Master plan. Waves are independently approvable and ordered by impact-to-risk.
See `audit-findings.md` for the evidence behind each task and `progress-log.md`
for what has actually been done. Update the status column as work lands.

Status legend: TODO / IN PROGRESS / DONE / BLOCKED / SKIPPED

## Wave 0 — Foundation (already complete before this plan)

| # | Task | Status |
|---|---|---|
| 0.1 | Slim CLAUDE.md via `discover-claude-context.sh` (141k→40k base context) | DONE |
| 0.2 | `harness-doctor.sh` context invariants + warn-only SessionStart wiring | DONE |
| 0.3 | Four skills: `/consensus-search`, `/longdoc`, `/ingest`, `/doctor` | DONE |
| 0.4 | `ra-wiki-lint.sh` checks 1-5 (dual-tree scan, wikilink `\|`-split, ref resolution) | DONE |
| 0.5 | Fix 4 shared-wiki pages missing `originating_space` | DONE |

## Wave 1 — Finish the directory migration (mechanical, low-risk, high-impact)

Acceptance: no script or agent def reads/writes the bare `spaces/*/wiki` legacy
tree for operational purposes; `ra-wiki-lint.sh` passes with checks 6-7 active;
a live long-doc brain-assembly dispatch reads the 67-page canonical tree.

| # | Task | File:line | Type | Status |
|---|---|---|---|---|
| 1.1 | Brain-assembler wiki read → canonical | `long-doc-orchestrate.sh:290` | in-place | TODO |
| 1.2 | Devil's-advocate eval read → canonical | `long-doc-orchestrate.sh:1019` | in-place | TODO |
| 1.3 | Delivery dir → canonical (prefer/fallback) | `long-doc-orchestrate.sh:1362` | in-place, NEEDS DECISION | TODO |
| 1.4 | Lint checks 6-7 driver loops → canonical | `ra-wiki-lint.sh:224,274` | in-place | TODO |
| 1.5 | Rollback safety-net glob → add canonical | `ingest-rollback.sh:99` | in-place | TODO |
| 1.6 | Storage-audit image globs → canonical | `ra-storage-audit.sh:82,125` | in-place | TODO |
| 1.7 | Weekly-status wiki/orphan/seed globs → canonical | `ra-weekly-status.sh:63,97,116` | in-place | TODO |
| 1.8 | Image-orphan-scan → canonical OR consolidate onto `orphan-image-check.sh` | `image-orphan-scan.sh:32,47` | in-place/consolidate | TODO |
| 1.9 | ra-brain-assembler 5 operational reads → canonical | `ra-brain-assembler.md:51,62,100,117,129` | in-place | TODO |
| 1.10 | ra-wiki-reviewer live-page + schema reads → canonical | `ra-wiki-reviewer.md:18,20` | in-place | TODO |
| 1.11 | ra-wiki-linter scan roots → canonical | `ra-wiki-linter.md:44-46` | in-place | TODO |
| 1.12 | ra-email-drafter write target → canonical | `ra-email-drafter.md:33` | in-place | TODO |
| 1.13 | ra-orchestrator guard wording → canonical | `ra-orchestrator.md:77` | in-place | TODO |
| 1.14 | ra-wiki-ingestor explicit canonical `_index.md` | `ra-wiki-ingestor.md:35,40` | in-place | TODO |
| 1.15 | Citation-format examples (`[spaces/{SPACE}/knowledge/...]`) in 11 agents | ~lines 20-22 each | DEFERRED — see note | RECLASSIFIED |

Decisions resolved:
- 1.3 delivery dir: RESOLVED — prefer-canonical/fallback-legacy pattern applied
  (mirrors `long-doc-orchestrate.sh:1179`). New docs land canonical; old ones stay
  discoverable.
- 1.15: RECLASSIFIED and DEFERRED. On inspection these are NOT operational path
  bugs — they are citation-format (provenance-string) examples that match the
  "Accepted Sources" block in `no-assumption-rule.md` VERBATIM. Changing them in
  agents alone would make 11 agents inconsistent with the governing steering rule,
  and the `[spaces/...]` provenance convention is also used across ~92 existing
  wiki pages. Changing the convention is a separate, larger task (steering rule +
  all agents + existing citations together), not a Wave-1 path fix. Tracked for a
  future dedicated decision; NOT a silent-failure bug (agents read the correct tree
  now; only the human-readable citation prefix differs).

## Wave 2 — Rebuild the enforcement layer as Claude Code hooks (new files)

New wrapper scripts in `.claude/hooks/`, registered in `.claude/settings.json`.
Kiro originals untouched. Acceptance: each hook fires on its CC event and its
corrective feedback is observable.

| # | Task | New file | CC event | Status |
|---|---|---|---|---|
| 2.1 | Wiki-lookup-before-drafting classifier | `.claude/hooks/wiki-lookup.sh` | UserPromptSubmit | DONE |
| 2.2 | Human-authored-writing post-write gate (consolidates check-agent-writing + check-submission-writing) | `.claude/hooks/writing-gate.sh` | PostToolUse (Edit\|Write\|MultiEdit) | DONE |
| 2.3 | py_compile lint on edited agent/workflow/core Python | `.claude/hooks/py-lint.sh` | PostToolUse (Edit\|Write\|MultiEdit) | DONE |
| 2.4 | Register 2.1-2.3 in settings.json (SessionStart + permissions preserved) | `.claude/settings.json` | — | DONE |

## Wave 3 — SKIPPED (evolve transcript-reflection loop)

Out of scope by decision (2026-07-27). Claude Code memory + maintained wiki
cover this role. Deterministic learner tier retained. No work here.

## Wave 4 — Make all 23 agents fully Claude Code-compatible and hardened

Every agent definition must be a valid, complete Claude Code subagent that has
everything Claude Code expects to invoke and run it correctly, in addition to
the sourcing/model hardening. First step: read the Claude Code sub-agents doc
(https://code.claude.com/docs/en/sub-agents) and derive the full expected
frontmatter/spec (required + recommended fields: name, description, tools,
model, and any others), then audit all 23 against that spec before editing.

Acceptance: ALL 23 agents conform to the current Claude Code subagent spec
(valid frontmatter, correct field names, sensible tool grants, explicit model);
ALL 23 pin a 1M model; all carry the full sourcing Hard Rule; gap/review agents
carry the absence-claims guard; ingestor contract mandates canonical `target_path`.

| # | Task | Scope | Status |
|---|---|---|---|
| 4.0 | Derive the current CC subagent spec from docs; audit all 23 for compliance | all `.claude/agents/*.md` | DONE |
| 4.1 | Bring every agent into full CC-spec compliance | all `.claude/agents/*.md` | DONE (frontmatter was valid; only model field missing) |
| 4.2 | Pin `model: claude-opus-4-8[1m]` (verified against availableModels) on ALL 23 | all `.claude/agents/*.md` | DONE |
| 4.3 | Upgrade short-form Hard Rules to strengthened form (14 identical weak ones) | 14 agents | DONE |
| 4.4 | Add "No Absolute-Absence Claims" guard | ra-gap-table-builder, ra-litreview-builder, ra-methodology-advisor | DONE |
| 4.5 | Mandate canonical `target_path` in ingestor contract | ra-wiki-ingestor | DONE |

Note on 4.2: the spec-audit subagent recommended `model: opus` or `claude-opus-4-5`
and claimed `[1m]` is non-standard. Verified against `~/.claude/settings.json`
`availableModels` (with `enforceAvailableModels: true`): `claude-opus-4-8[1m]` IS
a registered id here. Using the subagent's guess would have written an
unregistered id into 23 files. Pinned the verified id instead.

## Wave 5 — Reconcile legacy tree + regression guards (destructive; explicit approval)

Acceptance: legacy `spaces/*/wiki` removed with zero content loss; a doctor
invariant fails if any script/agent references the bare legacy path.

| # | Task | Status |
|---|---|---|
| 5.1 | Migrate `principal-agent-theory.md` (unique) into canonical with valid frontmatter | DONE |
| 5.2 | Migrate the Gioia notes source (unique) into canonical (`gioia-2013-qualitative-rigor.md`) | DONE |
| 5.3 | Reconcile `berente-2021`: keep canonical (5 cross-refs), port 3 unique legacy sections | DONE |
| 5.4 | Delete empty legacy `spaces/*/wiki` (output/ deliverables kept) | DONE |
| 5.5 | Add `harness-doctor.sh` check 4 (no bare `spaces/*/wiki` refs) + `.claude/hooks/README.md` | DONE |

Wave 5 note: check 4 immediately caught a real leftover the 5-cluster audit missed
(`obsidian-graph-linker.py` string markers). On inspection that script was already
canonical-correct (its discovery roots are `src/research_assistant/spaces`), so the
match was benign; the guard regex was tightened to a PCRE negative-lookbehind so
canonical paths never match, and the script's dead `EXCLUDED_TREE` (pointing at the
deleted legacy tree) was removed. The guard earning a catch on its first run is the
point.

## Wave 6 — Close the coverage gaps surfaced by the critical review (TODO)

These were found by self-audit AFTER the main waves; logged honestly rather than
declaring the upgrade complete. None is a silent-failure regression; they are
gaps in enforcement reach and scheduling.

| # | Task | Why | Status |
|---|---|---|---|
| 6.1 | Enforce writing/py-lint on subagent + pipeline writes | Main-session PostToolUse hooks do NOT see writes by dispatched subagents or by `long-doc-orchestrate.sh`. Options: per-agent `hooks:` frontmatter, OR verify `ra-pre/post-stitch-eval` + `ra-prose-editor` already enforce the full banned-list. | TODO |
| 6.2 | Maintenance tier: make it zero-effort, zero-noise | Originally framed as "install cron". Re-examined: these scripts are reports + disk housekeeping, no correctness risk if never run. Cron was the wrong tool (misses runs when the Mac sleeps → false "handled"; hides output in logs). | DONE (correctly) — (a) the ONE item with a whiff of correctness (index drift) is now EVENT-DRIVEN: `ingest-commit.sh` auto-rebuilds the affected space's `_index.md` at commit time, the only moment pages change, silently, no timer. (b) Deleted `crontab.example` + `install-crontab.sh` as noise. (c) Reports (lint, storage, status) stay pull-only: run on demand when a symptom shows. (d) Fixed 7 script headers that pointed at the deleted crontab.example. Nothing to remember, nothing scheduled, no session cost. |
| 6.3 | Live long-doc pipeline run (end-to-end proof) | Wave 1 fixed the pipeline's paths but it was never RUN. | DONE — ra-brain-assembler read 29 canonical QNTR pages, wrote 10 grounded brain files, verified on disk. Proves Waves 1+4+5 together. |
| 6.4 | Ingest the 169-file coverage backlog + resolve 29 orphan pages | Surfaced by the now-honest lint check 6. Content work, separate from the CC migration. | TODO |
| 6.5 | Regenerate stale wiki `_index.md` files | Found during 6.3: QNTR `_index.md` reports 0 sources/concepts while 24+6 exist on disk. The brain-assembler survived by trusting the filesystem, but a stale index is a real reliability hazard for anything that trusts it. Needs an index-regeneration pass/script per space. | TODO |
| 6.6 | Fix the eval-tool Python runtime | build_contract.py / run_eval.py import the research_assistant package (needs pyyaml+click); system python3 (PEP 668) lacks them, so the shell eval gate ran degraded — and claude-dispatch.sh SILENTLY proceeded with an empty contract. | DONE — created `.venv` (gitignored) with `pip install -e .`; `claude-dispatch.sh`+`jig-compare.sh` resolve `RA_PYTHON`=.venv/bin/python3; claude-dispatch now warns loudly on empty contract; fixed a SyntaxWarning in invoker.py:797. |

## Cross-cutting acceptance (definition of done for the whole upgrade)

1. `harness-doctor.sh` all green, including the legacy-path invariant. ✓ (Wave 5)
2. `ra-wiki-lint.sh` all 7 checks active and honest (no false "all clean"). ✓ (Wave 1)
3. A live long-doc dispatch produces a brain package built from the 67-page tree. ⧗ (Wave 6.3)
4. Wave-2 hooks demonstrably fire and give corrective feedback. ✓ (UserPromptSubmit verified live; PostToolUse verified against contract, subagent reach = Wave 6.1)
5. Every new file sits in its correct place: hooks in `.claude/hooks/`, plan in
   `docs/workspace-upgrade/`, skills in `.claude/skills/`. ✓
