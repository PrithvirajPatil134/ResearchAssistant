# ResearchAssistant Architecture

## Current Architecture (2026-05-14)

Two-layer system: a stable Python CLI layer (kiro-cli workflows) and an IDE-native multi-agent layer (Claude Code agents). The Python CLI is the hard-fallback path. The IDE-native layer is the primary execution path for all new work.

### System Diagram

```
User (IDE or CLI)
       │
       ├─────────────── CLI path ──────────────────────────────┐
       │                                                        │
       │    ra explain / guide / review / research / quant      │
       │         │                                              │
       │    WorkflowInvoker (Python)                            │
       │         │                                              │
       │    kiro-cli (pure text generation)                     │
       │         │                                              │
       │    ParallelEval (Analyst + Reviewer + Evaluator)       │
       │         │                                              │
       │    Output (.md) to spaces/{SPACE}/output/              │
       │                                                        │
       ├─────────────── IDE path ──────────────────────────────┐
       │                                                        │
       │    User prompt in IDE                                  │
       │         │                                              │
       │    async-task-gate hook (three-tier routing)           │
       │         │                                              │
       │         ├── sync: handle inline                        │
       │         │                                              │
       │         ├── tier (a) non-doc async: spawn-gpu-agent.sh │
       │         │                                              │
       │         ├── tier (b) tech docs: claude-dispatch.sh     │
       │         │    ├── build_contract.py (LLM contract)      │
       │         │    ├── spawn-gpu-agent.sh (background)       │
       │         │    │    └── claude -p --model opus           │
       │         │    │         └── ra-orchestrator             │
       │         │    │              ├── ra-wiki-ingestor (N)   │
       │         │    │              ├── ra-synthesizer         │
       │         │    │              └── ra-wiki-reviewer       │
       │         │    ├── heuristic pre-check                   │
       │         │    ├── run_eval.py (LLM + heuristic eval)    │
       │         │    ├── retry (max 2) or escalate             │
       │         │    ├── ab_log.py (A/B comparison)            │
       │         │    └── hard fallback → kiro-cli              │
       │         │                                              │
       │         └── tier (c) research: long-doc-orchestrate.sh │
       │              └── auto mode selection from word budget  │
       │                                                        │
       │    gpu-agent-completion hook (reports results)         │
       │                                                        │
       └── ra-learner (post-run pattern capture)               │
                                                                │
       Wiki Knowledge Base ←────────────────────────────────────┘
       spaces/{SPACE}/wiki/ + data/wiki/shared/
```

### Backend Hierarchy

1. **Claude Code (`claude -p --model opus`)**: default for all IDE-dispatched work
2. **kiro-cli**: hard-fallback only. Triggered by: exit code != 0, empty output (<100 chars), auth/quota errors, timeout

No soft-fallback. The switch happens per-task via `SPAWN_BACKEND=kiro-cli` prefix on the dispatch command.

### Agent Roster (23 agents at `.claude/agents/`)

**Librarians (manage the wiki knowledge base, 7 agents):**

| Agent | Role |
|-------|------|
| ra-orchestrator | Plans work, dispatches sub-agents, never writes wiki directly |
| ra-wiki-ingestor | Reads ONE source, proposes wiki page changes |
| ra-synthesizer | Merges N ingestor proposals into coherent change-sets |
| ra-wiki-reviewer | Validates pages against schema, cross-refs, sourcing rules |
| ra-wiki-linter | Periodic health check (orphans, staleness, coverage gaps) |
| ra-content-evaluator | Scores deliverable quality on 4 criteria (1-5 each) |
| ra-learner | Captures run traces, distills patterns with hard token caps |

**Researchers (produce deliverables, 5 agents):**

| Agent | Role |
|-------|------|
| ra-paper-writer | Draft or revise research paper sections |
| ra-litreview-builder | Build systematic/narrative/meta-analytic literature reviews |
| ra-methodology-advisor | Recommend paradigm, design, method |
| ra-gap-table-builder | Produce gap table (Han et al. 2017 Table 1 style) |
| ra-email-drafter | Draft emails to advisors, committee members, editors |

**Editors and Checkers (2 agents):**

| Agent | Role |
|-------|------|
| ra-prose-editor | Apply human-authored-writing.md standard |
| ra-fact-checker | Verify claims against wiki source pages and raw files |

### Dispatch Hierarchy

Only ra-orchestrator dispatches sub-agents. Researchers do not call librarians. Librarians do not call researchers. This keeps the dispatch graph predictable and makes learner capture complete.

Entry points: `claude-dispatch.sh` spawns ra-orchestrator. After orchestrator exits, `claude-dispatch.sh` spawns ra-learner. These are infrastructure-level spawns.

### Wiki Knowledge Base

Structured markdown pages organized by type across three spaces (QNTR, CRO, DBA) plus a shared layer.

```
spaces/{SPACE}/wiki/
├── _index.md          # Content catalog
├── _log.md            # Chronological operation log
├── _schema.md         # Per-space conventions
├── sources/           # One page per ingested paper/document
├── concepts/          # One page per key concept
├── entities/          # One page per recurring person/org/framework
├── syntheses/         # Cross-source analysis
├── methods/           # Methodology reference
└── comparisons/       # Head-to-head source comparisons

data/wiki/
├── _shared_schema.md  # Cross-space schema, frontmatter conventions
└── shared/
    ├── concepts/      # Concepts spanning multiple spaces
    ├── methods/       # Cross-space methodology pages
    ├── deliverables/  # Cross-space synthesis
    └── learner/       # Orchestrator patterns and failure logs
```

Current inventory (2026-05-08): 44 wiki pages total.
- 19 source pages (QNTR: 15, CRO: 3, DBA: 1)
- 8 concept pages (shared: 3, QNTR: 5)
- 5 entity pages (QNTR: 2, DBA: 2, CRO: 1)
- 2 synthesis pages, 1 deliverable page, 2 method pages

**Page maturity states**: seed, working, validated, deprecated.

**Cross-space design**: every wiki page carries `applicable_to` and `originating_space` frontmatter. Shared pages use `draws_from` to declare multi-space provenance.

### Ingest Pipeline (Atomic)

```
ingest-init.sh     → creates .kiro/.ingest-pending/{id}/
ra-wiki-ingestor   → writes proposals to .kiro/.ingest-pending/{id}/proposals/
ra-synthesizer     → merges to .kiro/.ingest-pending/{id}/merged/
ra-wiki-reviewer   → validates
ingest-commit.sh   → batch-renames temp files to real wiki paths (atomic)
ingest-rollback.sh → reverts on failure
ingest-cleanup.sh  → removes old pending manifests (7-day default)
```

### Evaluation Pipeline (claude-dispatch.sh)

1. Build dispatch contract via LLM (`scripts/build_contract.py` calls Sonnet for task-specific rubrics; falls back to heuristic for trivial queries or on LLM failure)
2. Spawn agent via `scripts/spawn-gpu-agent.sh`
3. Locate deliverable file (searches `docs/` and `spaces/*/output/` for `.md` files produced by the agent, not the raw CLI log)
4. Heuristic pre-check: empty output → score 0, echoed prompt → score 0, tool-call noise → score 0
5. LLM-powered evaluation (`scripts/run_eval.py` calls Sonnet via `scripts/llm_eval_caller.py` to score on 4 dimensions: structure, grounding, completeness, quality; heuristic fallback if LLM unavailable). Contract compliance is the primary eval axis; generic quality is secondary.
6. Pass → commit. Fail → one retry with revision feedback. Fail again → escalate to user.
7. A/B comparison log (`scripts/ab_log.py`, report via `scripts/ab_report.py`)
8. Hard fallback to kiro-cli if Claude process hard-failed

**User feedback loop**: after delivery, `scripts/capture-user-verdict.sh` records pass/fail/partial verdicts with freeform feedback. `scripts/capture-user-edits.sh` diffs original vs. user-edited documents to capture sections added, citations added, and tables added. Both feed patterns into `data/wiki/shared/learner/writing-team/eval_calibration.md` and `edit_patterns.md`, which the post-stitch eval reads on subsequent runs to avoid repeating the same misses.

### Learner System

Three learning channels:
1. **Orchestrator-level**: `data/wiki/shared/learner/orchestrator_patterns.md` (max 2000 tokens) + `orchestrator_failures_recent.md` (max 1000 tokens)
2. **Agent-level**: `{agent-name}_patterns.md` (max 500 tokens each)
3. **Per-invocation overlay**: orchestrator includes "DO NOT REPEAT" block in every sub-agent dispatch

Pattern entry schema: Trigger, Diagnosis, Action. Graduation rule: 3 independent observations required.

Token caps enforced by `scripts/learner-size-check.sh` after every ra-learner run.

### Observability

| Script | Schedule | Output |
|--------|----------|--------|
| `ra-weekly-status.sh` | Sunday 09:00 (cron) | `data/logs/status/weekly_YYYY-MM-DD.md` |
| `learner-summarize-month.sh` | 1st of month 03:00 (cron) | `data/logs/learner/summaries/YYYY-MM.md` |
| `ra-storage-audit.sh` | On-demand | Terminal output (size breakdown) |
| `ra-wiki-lint.sh` | On-demand | Terminal output (orphans, staleness, gaps) |
| `learner-archive.sh` | Via cron or manual | Archives Tier 2 logs |
| `trace-report.py` | On-demand | Terminal output (step timing, determinism check) |

**Step-Level Tracing (2026-06-02)**: Every agent dispatch and long-doc phase transition is logged to `data/logs/traces/YYYY-MM-DD.jsonl` (spawn-gpu-agent) and `data/logs/traces/longdoc-YYYY-MM-DD.jsonl` (long-doc phases). Each entry records: timestamp, agent_id/doc_id, backend/mode, category/phase, duration_ms, exit_code/status, output_bytes. Use `python3 scripts/trace-report.py` for summaries, `--determinism` flag for execution shape comparison across repeated runs.

Cron schedule defined in `crontab.example`. User installs manually.

### Storage Policy

Three-tier retention for learner logs (defined in `data/.storage-policy.md`):
- Tier 1 (0-7 days): full raw logs, uncompressed
- Tier 2 (7-90 days): compressed tarball
- Tier 3 (90+ days): tarball deleted, monthly summary only (max 10KB)

Steady-state: ~1.2GB/year, dominated by images at ~1GB.

### Auto-Capture (Narrow Scope)

Triggered via `scripts/autocapture-handler.sh` for:
- Images shared in IDE chat (compressed to JPEG-85 if >200KB)
- Communication files read during conversation
- Explicit "add to wiki" requests

Does NOT capture every file read or every message.

### Infrastructure Scripts

| Script | Purpose |
|--------|---------|
| `spawn-gpu-agent.sh` | Background agent launcher (Claude default, kiro-cli fallback). SENTINEL_V2: watchdog timeout + trap + atomic terminal sentinel + `.running` marker |
| `claude-dispatch.sh` | Full dispatch pipeline (contract, spawn, eval, retry, fallback). SENTINEL_V2: defers final sentinel to itself + trap guarantees a terminal sentinel on abort |
| `sentinel-lib.sh` | Shared completion-signaling primitives: atomic write, `.running` marker, pure-bash watchdog (no GNU `timeout`; macOS bash 3.2) |
| `sentinel-reconcile.sh` | Delivery-guarantee reconciler: atomically claims completed sentinels, detects stalls (dead PID or past deadline) and synthesizes terminal sentinels, retention-cleans `processed/`. Dry-run by default; `--commit` to act |
| `discover-claude-context.sh` | SessionStart hook: generates CLAUDE.md with @import directives |
| `ingest-init.sh` | Create ingest manifest directory |
| `ingest-commit.sh` | Atomic batch-rename of validated wiki pages |
| `ingest-rollback.sh` | Revert failed ingest |
| `ingest-cleanup.sh` | Remove stale pending manifests |
| `ra-manifest-cleanup.sh` | Manifest housekeeping |
| `build_contract.py` | LLM-powered dispatch contract generation (Sonnet; heuristic fallback) |
| `run_eval.py` | LLM + heuristic evaluation bridge for Claude output |
| `llm_eval_caller.py` | Lightweight Sonnet caller for eval LLM calls via `claude -p` subprocess |
| `ab_log.py` / `ab_report.py` | A/B comparison logging and reporting |
| `capture-user-verdict.sh` | Records user rejection verdicts into learner calibration |
| `capture-user-edits.sh` | Diffs user edits against original and feeds patterns to learner |
| `autocapture-handler.sh` | Auto-capture images and communications |
| `orphan-image-check.sh` | Detect unreferenced images |
| `ra-wiki-lint.sh` | Wiki health check |
| `ra-weekly-status.sh` | Weekly status report |
| `ra-storage-audit.sh` | Storage size breakdown |
| `learner-size-check.sh` | Enforce learner token caps |
| `learner-summarize-month.sh` | Monthly learner summary |
| `learner-archive.sh` | Archive old learner logs |
| `test-cron-suite.sh` | Test cron job suite |
| `long-doc-orchestrate.sh` | Long document pipeline coordinator (9 phases) |
| `trace-report.py` | Step-level trace analysis, timing breakdown, determinism verification |
| `convert-citations.py` | Author-year to numbered citation conversion |
| `extract-venue-fingerprint.py` | PDF structural fingerprint extraction |

### Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `wiki-lookup-before-drafting.kiro.hook` | promptSubmit | Classify task (COMMUNICATION/DOCUMENT/INFRASTRUCTURE/RESEARCH/GENERAL), enforce wiki/entity lookup. INFRASTRUCTURE category triggers on: how our system works, comparing external tools to our pipeline, any claim about scripts/hooks/agents/dispatch/eval gates |
| `async-task-gate.kiro.hook` | promptSubmit | Three-tier routing: (a) non-doc async → spawn-gpu-agent.sh, (b) tech docs → claude-dispatch.sh, (c) research deliverables → long-doc-orchestrate.sh with auto mode selection |
| `gpu-agent-completion.kiro.hook` | fileCreated (.done sentinel) | Fast-path report of agent results. Best-effort/opportunistic (fileCreated may not fire for detached-subprocess writes); idempotency guard skips `awaiting_eval` and already-claimed sentinels to avoid double-reporting with the reconciler |
| `check-agent-status.kiro.hook` | promptSubmit | Delivery guarantee: runs `sentinel-reconcile.sh --commit` every message to claim completions, surface stalls, and clean the sentinel dir (replaced the prior `ls | tail -5`) |
| `kiro-evolve-save-prompt.kiro.hook` | promptSubmit | Capture to transcript |
| `kiro-evolve-save-response.kiro.hook` | agentStop | Capture response |
| `kiro-evolve-check-all.kiro.hook` | userTriggered | Run evolve checks |

### Hook Parity: Kiro IDE vs Claude Code (2026-07-20)

The hooks in `.kiro/hooks/` are read by the **Kiro IDE only**. Claude Code reads hooks solely from `.claude/settings.json`, where the only registered hook today is the `SessionStart` context loader (`scripts/discover-claude-context.sh`). Nothing in the current setup is changed by this note; it documents the seams so a future port is deliberate, not accidental.

The governing distinction: **Kiro watches the filesystem; Claude Code watches the turn.** Kiro's `PostFileSave` / `PostFileCreate` triggers fire on any disk change by any actor. Claude Code has no filesystem watcher — its nearest event, `PostToolUse`, fires only after Claude's own Write/Edit tool call. So any enforcement that depended on "a file appeared on disk by some other actor" (hand edits, detached background agents) has no Claude-side trigger.

Parity if the Kiro hooks were ported into `.claude/settings.json`:

| Hook | Kiro trigger | Claude Code status |
|------|-------------|--------------------|
| async-task-gate | UserPromptSubmit | Clean — maps to `UserPromptSubmit` |
| check-agent-status | UserPromptSubmit | Clean (this is the completion delivery guarantee) |
| no-assumption-chat-check | UserPromptSubmit | Clean |
| wiki-lookup-before-drafting | UserPromptSubmit | Clean |
| eval-principles-check | PostToolUse | Clean — maps to `PostToolUse` + matcher |
| check-agent-writing | PostToolUse | Clean |
| check-submission-writing | PostFileSave | Partial — fires only when Claude itself wrote the file, not on external/hand edits |
| lint-agents | PostFileSave | Partial — same limitation |
| new-agent-check | PostFileCreate | Partial — same limitation |
| gpu-agent-completion | PostFileCreate | No equivalent — sentinel is written by a detached process, invisible to `PostToolUse`. Mitigated: `check-agent-status` runs `sentinel-reconcile.sh --commit` on every message and is the real delivery guarantee (the `PostFileCreate` path was always the opportunistic fast path per SENTINEL_V2 below) |
| jig-parallel-dispatch | PostFileCreate | No equivalent, and irrelevant — Jig is parked (cannot compile on macOS ARM) |
| kiro-evolve-check-all | Manual | Covered — "evolve" is a steering-driven command already loaded via CLAUDE.md |
| kiro-evolve-save-prompt | UserPromptSubmit | `enabled: false` — fires nowhere today |
| kiro-evolve-save-response | Stop | `enabled: false` — fires nowhere today |

Summary: of the 14 hooks, 8 port cleanly, 3 degrade to "fires only when Claude is the writer," 1 has no equivalent but is already redundant with the reconciler, and 2 are disabled everywhere.

**Port design (agreed, not yet implemented):**

- **Never hand-copy hook prompts.** Two copies of the same instruction drift silently as the evolve/learner systems rewrite the `.kiro/hooks/*.json` prompts. Instead, extend `discover-claude-context.sh` (already the `SessionStart` hook) to *generate* the Claude-side instruction files from `.kiro/hooks/*.json` at session start. `.kiro/` stays the single source of truth; the Claude copies regenerate every session; drift is impossible.
- **Keep `sentinel-reconcile.sh` as its own dedicated command hook** — it mutates state and must not share a failure domain with instruction-injection hooks.
- **Merge only the model-facing instruction prompts** (async-task-gate, wiki-lookup, no-assumption) into one combined `UserPromptSubmit` instruction, and keep classification model-driven (not bash/regex) so it is as reliable as Kiro's `type: agent` hooks. This pays the full per-turn token cost by design; that is the accepted trade for reliable classification.
- **Precedence ladder** the combined instruction must encode, because `wiki-lookup` (context-gathering) and `async-task-gate` (routing) otherwise issue conflicting "read now and answer" vs "stop and dispatch" orders on the same turn:

  ```
  classify (model-driven, wiki-lookup's 6 categories) ->
    INFRASTRUCTURE / GENERAL -> inline; main agent reads the wiki itself
    RESEARCH / DOCUMENT      -> lean dispatch; the long-doc pipeline
                                (ra-brain-assembler Phase 1) reads the wiki,
                                and the outline eval gate catches thin grounding,
                                so a main-agent pre-read is duplication, not safety
    COMMUNICATION            -> resolve + verify the entity page path in the main
                                thread, pass the path in the dispatch prompt, and
                                let ra-email-drafter do the deep read. If the
                                entity page is ABSENT, surface that (do not spawn
                                a blind, ungroundable draft). This path has NO
                                downstream eval gate, so the check belongs here.
    (no-assumption-chat-check constrains the final text in every branch)
  ```

  The RESEARCH-vs-COMMUNICATION split is justified by gate coverage, not by "value": the research path has a downstream eval gate and an agent whose sole job is reading the wiki; the communication path has neither, so grounding must be front-loaded.

### Reliable Completion Signaling (SENTINEL_V2, 2026-07-13)

Background-agent completion originally relied solely on a `.done` sentinel plus a `fileCreated` hook. That path had no guaranteed producer write (a killed, crashed, or hung agent left no sentinel), no timeout, and no reconciliation for missed `fileCreated` events, so a dispatch could strand a batch silently. Stale sentinels also accumulated because cleanup only ran when the hook fired.

SENTINEL_V2 (default on; set `SENTINEL_V2=0` to fall back to the legacy best-effort path) addresses this in three layers:

- **Producer guarantees** (`spawn-gpu-agent.sh`, `claude-dispatch.sh` via `sentinel-lib.sh`): a `trap` writes a terminal sentinel even on kill/crash/abort; a pure-bash watchdog (`SENTINEL_TIMEOUT`, default 1200s; macOS has no GNU `timeout`) kills hung agents and records `status: timeout` / exit 124; sentinels are written atomically (temp-in-same-dir then `mv`); a `.running` marker records the live PID and deadline. `claude-dispatch.sh` defers the final sentinel to itself (`SENTINEL_DEFER`), so the inner spawn writes a provisional `awaiting_eval` marker and the eval-enriched final sentinel is written once, atomically. A collision guard refuses to clobber a live sentinel/marker unless `SENTINEL_FORCE=1`.
- **Delivery guarantee** (`sentinel-reconcile.sh`, run by `check-agent-status.kiro.hook` on every message): polling reconciliation is the source of truth; the `fileCreated` hook is demoted to an opportunistic fast path. The reconciler atomically claims completed sentinels (moving them to `.kiro/.gpu-agent-done/processed/` so concurrent runs never double-process), detects stalls via PID-liveness plus deadline (a live PID within its deadline is authoritative and never flagged), synthesizes a terminal `status: stalled` sentinel so fan-in batches can progress under their `failure_mode`, and retention-cleans `processed/`.
- **Sentinel schema**: additive. `exit_code` is preserved for `long-doc-orchestrate.sh`'s `wait_for_sentinel` poller (which is unchanged and already reliable). New fields: `status` (`done|timeout|failed|killed|awaiting_eval|stalled|dispatch_aborted`), plus `.running` markers carrying `pid` and `deadline_epoch`.

Residual risks (accepted): a hard `kill -9` writes no sentinel, so detection falls to the reconciler's next PID-liveness check rather than being instant; with the IDE closed and no cron reconciler, batches wait for the user to return.

### Configuration

Claude Code settings at `.claude/settings.json` register the `discover-claude-context.sh` SessionStart hook. Agent specs live at `.claude/agents/*.md`.

### Long Document Production System (2026-05-09)

A dedicated pipeline for producing submission-ready academic documents (25-30 pages). Uses the same `spawn-gpu-agent.sh` infrastructure, the same wiki as knowledge source, and the same no-assumption rule. Adds 9 specialized agents and a shell-based pipeline coordinator.

Full design: `docs/long_document_production_system.md`.

#### Pipeline

```
User Request → long-doc-orchestrate.sh
    │
    ├── Phase 1: BRAIN ASSEMBLY (ra-brain-assembler)
    │   Reads wiki sources/concepts/entities/methods
    │   Version-aware: reads deliverable_synthesis Pending Revision Areas
    │   as hard requirements; encodes them in constraints.md
    │   Produces: .kiro/.long-doc/{doc-id}/brain/
    │     voice.md, argument-map.md, terminology.md,
    │     methodology-context.md, advisor-guidance.md,
    │     literature-map.md, constraints.md, exhibits-plan.md, outline.md
    │
    ├── Phase 2: OUTLINE EVAL (heuristic gate)
    │   Checks structure, source assignments, word targets, argument flow
    │   FAIL → brain assembler revises (max 2 retries)
    │
    ├── Phase 3: SECTION WRITING (ra-section-writer × N)
    │   Parallel or sequential per mode selection
    │   Each writer gets: full brain package + section-specific wiki pages
    │   Each writer reads constraints.md Hard Requirements for its section
    │   References/Bibliography section excluded (compiled mechanically)
    │   Produces: .kiro/.long-doc/{doc-id}/sections/section_N.md
    │
    ├── Phase 4: EXHIBIT PRODUCTION (ra-exhibit-producer)
    │   Tables, figures, diagrams from exhibits-plan.md
    │
    ├── Phase 5: PRE-STITCH EVAL (ra-pre-stitch-eval)
    │   Checks terminology drift, argument gaps, contradictions
    │   FAIL → specific sections rewritten
    │
    ├── Phase 5.5: STITCHING (ra-doc-stitcher)
    │   Sliding window for documents >10,000 words
    │   Fixes transitions, voice normalization, cross-references
    │   Places exhibits at [INSERT Table/Figure N] markers
    │
    ├── Phase 6: POST-STITCH EVAL (ra-post-stitch-eval)
    │   Contract compliance is primary axis (structured checklist output)
    │   Reads eval_calibration.md for past user rejection patterns
    │   Gate check + devil's advocate (always, even on pass)
    │   Enhancement suggestions with priorities
    │
    ├── Phase 7: BENCHMARK COMPARISON (ra-benchmark-comparator)
    │   Compares against 3 random published papers from knowledge/
    │   Structural fingerprints: section ratios, citation density, tone
    │
    ├── Phase 8: ABSTRACT + CITATIONS
    │   ra-abstract-writer (structured abstract)
    │   convert-citations.py (mechanical, no LLM)
    │
    └── Phase 9: WRITING TEAM LEARNER (ra-writing-learner)
        Captures patterns, mode results, terminology drift
        Captures user verdict divergences and edit patterns
        Enforces token caps, graduates after 3 observations
```

#### Four-Mode System

| Mode | How It Works | Best For |
|------|-------------|----------|
| single-raw | One agent, full prompt, no brain package | Short docs (<2000 words) |
| single-brain | One agent, brain package + all sources | Medium docs (2000-8000 words) |
| parallel | Brain + N section writers simultaneously + stitch | Long docs with independent sections |
| sequential | Brain + sections in order (each sees previous tail) + stitch | Long docs where argument flow is critical |

Mode selection is automatic based on the word budget extracted from the prompt file:
- `<2000 words`: single-raw (no brain package needed)
- `2000-8000 words`: single-brain (one agent with brain)
- `>8000 words or unknown`: learning-based selection using `mode_comparison.jsonl` history; defaults to running both parallel and sequential for the first 10 runs of a document type, then graduates a winner

Progressive elimination graduates a winner as early as run 2 on strong signal (>1.5 point gap). After graduation, 5% exploration rate re-tests alternatives.

Pre-flight context budget check skips any mode where brain_tokens + source_tokens + output_tokens > 80% of context window.

#### Two-Learner Architecture

| Learner | Scope | Pattern Files |
|---------|-------|---------------|
| Inner (ra-writing-learner) | Everything inside the long-doc pipeline | `data/wiki/shared/learner/writing-team/` (10 files, ~9000 tokens total) |
| Outer (ra-learner) | Everything outside | `data/wiki/shared/learner/` (orchestrator_patterns, failures_recent) |

Inner captures: outline quality, section patterns, stitching patterns, mode comparison, terminology drift, evaluator agreement, user verdict divergences (`eval_calibration.md`), and user edit patterns (`edit_patterns.md`). Outer captures: pipeline pass/fail rate, doc-type weakness patterns.

#### Agent Specs (9 agents at `.claude/agents/`)

| Agent | Purpose |
|-------|---------|
| ra-brain-assembler | Reads wiki, produces document-specific brain package |
| ra-section-writer | Writes one section from brain + assigned sources |
| ra-doc-stitcher | Sliding window assembly with transition fixes |
| ra-pre-stitch-eval | Section quality gate before assembly |
| ra-post-stitch-eval | Devil's advocate + enhancement suggestions |
| ra-benchmark-comparator | Compares against published papers |
| ra-writing-learner | Inner learner for writing pipeline |
| ra-abstract-writer | Generates structured abstract |
| ra-exhibit-producer | Produces tables, figures, diagrams |

#### Scripts

| Script | Purpose |
|--------|---------|
| `long-doc-orchestrate.sh` | Full pipeline coordinator (1554 lines) |
| `convert-citations.py` | Author-year to numbered citation conversion |
| `extract-venue-fingerprint.py` | PDF structural fingerprint extraction |

---

### Key Design Decisions (Locked)

These were negotiated during the 2026-05-07 build session (documented in `docs/handoff_2026-05-07_multiagent_system.md`) and should not be re-litigated:

1. Claude Code is mandatory for all IDE-dispatched work. kiro-cli is hard-fallback only.
2. Only ra-orchestrator dispatches sub-agents. No peer-to-peer agent calls.
3. Retry cap: 2 revisions per sub-agent, then escalate to user (Option A).
4. No-Assumption Rule: every claim must cite a source. Fabrication is rejection.
5. Cross-space design from day one (applicable_to, originating_space frontmatter).
6. Entity pages only for entities with relational/operational presence, not citation authors.
7. Proposal-based changes for validated pages only. Seed and working pages edited in place.
8. Markdown and YAML only. No SQLite in the wiki core.

---

## Architecture History

### Pre-2026-05-07: Python CLI System (Level 3)

The original system, still operational as the hard-fallback path and for direct CLI use.

## Core Concept

Multi-agent research workflow system where **spaces** (academic domain simulations) orchestrate **agents** to process research tasks, with outputs saved as `.md` files.

Each space (QNTR, CRO, DBA, CW) represents a distinct academic domain with its own knowledge base, persona configuration, prompts, and learned patterns. Agents operate within a space's context but can reference knowledge from other spaces when configured.

Implements **Level 3 context engineering**: designing the information architecture, feedback loops, evaluation criteria, and context lifecycle across the entire agent session.

## Spaces (formerly "Personas")

Spaces are the organizational unit. Everything revolves around the space:

> **Path invariant**: the canonical spaces root is `src/research_assistant/spaces/`
> (see `spaces_dir` in config). A repo-root symlink `spaces -> src/research_assistant/spaces`
> makes the shorthand path `spaces/{SPACE}/...` used throughout this doc, README, and
> WORKFLOW_GUIDE resolve to the same tree. Never create a real `spaces/` directory at the
> repo root: deliverables written there bypass the canonical tree and are git-ignored.
> The `scripts/check-stray-spaces.sh` guard (wired via `.kiro/hooks/check-stray-spaces.json`)
> fails loudly if the symlink is ever replaced by a real directory.

```
src/research_assistant/spaces/
├── QNTR/          # Quantitative Research Methods
│   ├── persona.yaml
│   ├── prompts.yaml
│   ├── knowledge/       # Read-only source material
│   ├── output/          # Final deliverables only
│   ├── artifacts/       # Intermediate files per run
│   ├── cache/           # Cached stage outputs (reusable)
│   ├── doc/             # Lessons, workflow guides, session memory
│   ├── assignment/      # Student submissions for review
│   ├── communication/   # Email drafts, correspondence
│   └── workspace/       # Shared workspace for multi-stage runs
├── CRO/            # Corporate Research & Operations
├── DBA/            # Doctoral Business Administration
├── CW/             # Case Writing
└── loader.py       # SpaceLoader (loads persona.yaml + knowledge)
```

Each space has:
- **persona.yaml**: Identity, behaviors, agent configs, guidelines, ethics, knowledge base config
- **prompts.yaml**: Agent-specific prompts per workflow type
- **knowledge/**: Read-only source material (PDFs, slides, papers). Never written to by agents.
- **output/**: Final deliverables only. One file per workflow run.
- **doc/**: Persistent learning data (lessons_learned.md, workflow guides, session memory)
- **cache/**: Cached stage outputs. Reused across runs if stages match.

## Technical Design

### Entry Points
```
CLI (ra command) → WorkflowInvoker → Contract → Staged Reasoning → ParallelEval → Output
```

### Source Structure
```
src/research_assistant/
├── __init__.py
├── cli.py                    # Click-based CLI (entry point)
├── config.py                 # Configuration management
│
├── workflows/
│   └── invoker.py           # WorkflowInvoker (orchestrator + execution)
│
├── core/                     # Core modules
│   ├── __init__.py           # Exports: Memory, ContextGuard, LLM, etc.
│   ├── contextguard.py      # Token monitoring at 70% threshold
│   ├── memory.py            # Shared state across agents (in-process)
│   ├── thinking.py          # Reasoning chains, hallucination detection
│   ├── controller.py        # Orchestrates thinking process
│   ├── llm.py               # Unified LLM client (Perplexity/Anthropic/OpenAI/kiro-cli)
│   ├── parallel_agents.py   # Parallel document analysis (batched)
│   ├── artifact_cache.py    # Stage-level caching for multi-step workflows
│   ├── workflow_sections.py # Section templates for document types
│   ├── dispatch_contract.py # Pre-dispatch contract (Level 3)
│   ├── evaluator.py         # Post-composition evaluation (Level 3)
│   ├── recitation.py        # Attention re-anchoring (Level 3)
│   ├── parallel_eval.py     # Concurrent evaluation (Level 3)
│   ├── iterative_processor.py # Section-by-section document generation
│   └── harness_audit.py     # Assumption auditing (Level 3)
│
├── agents/                   # Specialized agents
│   ├── base.py              # BaseAgent with persona context
│   ├── reader.py            # Reads and extracts from knowledge base
│   ├── analyst.py           # Scores reasoning quality (0-10)
│   ├── reviewer.py          # Validates against standards
│   └── learner.py           # Learns from feedback, warm-start patterns
│
├── spaces/                   # Space definitions (see above)
│   ├── loader.py            # SpaceLoader
│   ├── QNTR/
│   ├── CRO/
│   ├── DBA/
│   └── CW/
│
└── learnings/               # Cross-space design principles and eval docs
```

## Workflow Execution Flow

The actual execution path through `WorkflowInvoker.invoke()`:

```
1. CLI Command
   ra explain "Brand Equity" --persona QNTR

2. Load Space
   SpaceLoader reads persona.yaml, prompts.yaml, scans knowledge/

3. Initialize Components
   Memory, ContextGuard (100K tokens, 70% threshold),
   ReaderAgent, LearnerAgent, AnalystAgent, ReviewerAgent, ThinkingModule

4. STEP 1: Read KB (ReaderAgent)
   Scan knowledge/ directory, extract content from matching files
   Result: extracted_content[] (list of file contents)

5. STEP 1.5: Build Dispatch Contract (Level 3)
   LLM-generated for complex queries (>15 words), heuristic for simple ones
   Defines: done_definition, completeness_criteria, required_sections, grounding_requirements
   Stored in Memory for Analyst and Reviewer to score against

6. STEP 2: Warm Start (LearnerAgent)
   Load lessons from doc/lessons_learned.md
   Match query against stored reasoning patterns (Jaccard similarity)
   Inject strategies + lessons into system prompt

7. STEP 3: Stage Detection
   If query has STEP 1/STEP 2 markers → split into stages
   Each stage classified: multi-doc analysis, document writing, or single call
   Cached stages reused from previous runs

8. STEP 3a: Reasoning Loop (per stage, max 5 iterations)
   For each stage:
     - Check cache (ArtifactCache) → skip if cached
     - If multi-doc (>3 files): ParallelAgentOrchestrator (3 concurrent, batched)
     - Else: llm.generate_as_agent() (kiro-cli with file access)
     - Auto-continue if output truncates (up to 3 continuations)
     - AnalystAgent scores against dispatch contract
     - If score >= 7.5: proceed to next stage
     - If failed: retry with analyst feedback (max 2 retries per stage)

9. STEP 4: Recitation Checkpoint (Level 3)
   Before final stage: re-state original question + stage summaries
   Prevents drift toward most verbose source (~200 words)

10. STEP 5: Parallel Evaluation (Level 3)
    Three evaluators run concurrently in ThreadPoolExecutor(max_workers=3):
    - Analyst: KB grounding, completeness, quality, structure (0-10, pass >= 7.5)
    - Reviewer: Workflow-specific rubric, strengths/issues (0-10, pass >= 6.0)
    - Evaluator: Alignment, evidence, completeness, actionability (1-5 each, pass >= 3)
    Merge into UnifiedEvaluation
    If any fails: one revision with combined feedback

11. STEP 6: Store Pattern (LearnerAgent)
    Extract lesson via LLM (one-line, max 150 chars)
    Store to doc/lessons_learned.md
    If score >= 8.0: store reasoning pattern with strategies

12. STEP 7: Write Output
    Format with metadata footer
    Write to spaces/{SPACE}/output/{workflow}_{timestamp}.md
    Log to logs/workflow_history.jsonl
```

## LLM Call Map

Every LLM call in a single workflow run, in execution order:

| # | Module | Call | When | Skippable? |
|---|--------|------|------|------------|
| 1 | dispatch_contract.py | Build contract | Complex queries only | Yes (heuristic fallback) |
| 2-N | invoker.py | generate_as_agent() | Per stage (main reasoning) | No (core work) |
| N+1 | analyst.py | Score reasoning | Per iteration in reasoning loop | No (quality gate) |
| N+2 | analyst.py | Score (parallel eval) | Post-composition | Skippable via config |
| N+3 | reviewer.py | Validate standards | Post-composition (parallel) | Skippable via config |
| N+4 | evaluator.py | 4-criteria check | Post-composition (parallel) | Skippable via config |
| N+5 | learner.py | Extract lesson | Post-completion | Skippable via config |
| N+6 | learner.py | Extract strategies | Post-completion (score >= 8) | Skippable via config |
| N+7 | learner.py | Summarize reasoning | Post-completion (score >= 8) | Skippable via config |

Calls N+2 through N+4 run concurrently (parallel eval). Calls N+5 through N+7 are post-completion learning and do not affect output quality.

## Key Components

### WorkflowInvoker
Static class that orchestrates the full workflow. Contains:
- Workflow registration and lookup
- Stage detection and splitting
- The main reasoning loop
- Parallel evaluation orchestration
- Output formatting and logging

### Core Modules
- **ContextGuard**: Monitors token usage, triggers reconstruction at 70%
- **Memory**: In-process shared state (facts, decisions, persona context, contract)
- **ThinkingModule**: Reasoning chains with hallucination detection
- **Controller**: Orchestrates thinking process, validates reasoning chains
- **LLMClient**: Unified client supporting Perplexity, Anthropic, OpenAI, kiro-cli
- **ArtifactCache**: Stage-level caching for multi-step workflows
- **ParallelAgentOrchestrator**: Batched concurrent document analysis

### Specialized Agents
- **ReaderAgent**: Scans knowledge/ directory, extracts content from matching files
- **AnalystAgent**: Scores reasoning quality against dispatch contract (0-10)
- **ReviewerAgent**: Validates against workflow-specific standards
- **LearnerAgent**: Warm-start patterns, lesson extraction, strategy storage

### Level 3 Modules
- **DispatchContract**: Pre-dispatch "what done looks like" definition
- **Evaluator**: Post-composition 4-criteria check (alignment, evidence, completeness, actionability)
- **Recitation**: Re-anchoring checkpoint before final composition stage
- **ParallelEval**: Concurrent Analyst + Reviewer + Evaluator orchestration
- **HarnessAudit**: Periodic threshold and assumption validation

## Workflow Definitions

| Workflow | Purpose | Required Input | Output |
|----------|---------|----------------|--------|
| explain | Explain concept using space's teaching style | topic | explain_{ts}.md |
| guide | Assignment guidance (no direct answers) | assignment | guide_{ts}.md |
| review | Review submission against standards | submission_path | review_{ts}.md |
| research | Full research workflow with lit mapping | task | research_{ts}.md |
| quant | Statistical analysis guidance | task | quant_{ts}.md |

## Configuration

```yaml
# config.yaml
workspace_dir: .
data_dir: data
spaces_dir: src/research_assistant/spaces   # canonical spaces root

tokens:
  max_tokens: 10000
  threshold_percentage: 0.70
  warning_percentage: 0.60
  reconstruction_target: 0.30

ai:
  model: claude-3-sonnet
  temperature: 0.7
  max_response_tokens: 4000
  timeout_seconds: 60

logging:
  log_dir: data/logs
  log_level: INFO
```

Environment variable overrides: `RA_MAX_TOKENS`, `RA_TOKEN_THRESHOLD`, `RA_AI_MODEL`, `RA_AI_TEMPERATURE`, `RA_LOG_LEVEL`.

## Output Convention

All workflow outputs go to:
```
spaces/{SPACE}/output/{workflow}_{timestamp}.md
```

Intermediate artifacts go to:
```
spaces/{SPACE}/artifacts/{workflow}_{timestamp}/
```

Cached stages go to:
```
spaces/{SPACE}/cache/{workflow_id}/
```

## Usage Examples

```bash
# Explain a concept
ra explain "Brand Equity Model" --persona QNTR

# Review a submission
ra review submission.pdf --persona QNTR

# Get assignment guidance
ra guide "Case study approach" --persona QNTR

# Run full research workflow
ra research "Internal branding practices" --persona QNTR

# Statistical analysis guidance
ra quant "Regression analysis for survey data" --persona QNTR

# Run harness audit
ra audit --persona QNTR
```

---

## Change Log

### 2026-06-02: Step-Level Tracing + Hook Classification Fix

**What changed**:

1. **Step-level JSONL tracing.** `spawn-gpu-agent.sh` now appends a trace entry to `data/logs/traces/YYYY-MM-DD.jsonl` after every agent dispatch, recording: timestamp, agent_id, backend, category, duration_ms, exit_code, output_bytes. `long-doc-orchestrate.sh` adds a `trace_step()` function that logs each phase transition to `data/logs/traces/longdoc-YYYY-MM-DD.jsonl` with doc_id, space, mode, phase, step, duration_ms, status.

2. **Trace report utility.** New `scripts/trace-report.py` reads JSONL trace files and produces: step counts, duration breakdowns, slowest steps, category summaries, and a determinism check (verifies same execution shape across repeated runs of the same prompt).

3. **Hook classification fix.** `wiki-lookup-before-drafting.kiro.hook` INFRASTRUCTURE category expanded to trigger on: "how our system works", "comparing an external tool/approach against our pipeline", and "any claim about what our scripts, hooks, agents, dispatch pipeline, eval gates, steering enforcement, or orchestration do or do not do." Addresses a gap where comparison tasks were misclassified as GENERAL, allowing claims about internal infrastructure without reading the actual files.

4. **Jig exploration artifacts (parked).** Explored Jig (code.amazon.com/packages/Jig) as a deterministic workflow runtime alternative. Built comparison infrastructure (scripts/jig-install.sh, jig-compare.sh, jig-compare-report.py, 3 Luau workflows, disabled parallel-dispatch hook). Jig cannot compile on macOS ARM due to Zig @cImport alignment constraints with pthread headers. Artifacts parked at `data/drafts/_staging/jig-workflows/` and `scripts/jig-*.sh` pending upstream macOS support. Decision: tracing additions to existing scripts provide 80% of Jig's traceability benefit without new infrastructure or platform dependencies.

**New files**: `scripts/trace-report.py`, `data/logs/traces/` directory, `scripts/jig-install.sh`, `scripts/jig-compare.sh`, `scripts/jig-compare-report.py`, `data/drafts/_staging/jig-workflows/*.luau`, `.kiro/hooks/jig-parallel-dispatch.kiro.hook` (disabled).

**Modified files**: `scripts/spawn-gpu-agent.sh` (trace logging), `scripts/long-doc-orchestrate.sh` (trace_step function, wait_for_sentinel tracing), `.kiro/hooks/wiki-lookup-before-drafting.kiro.hook` (INFRASTRUCTURE category expansion).

### 2026-05-14: Eval Pipeline Enhancements — LLM Eval, Contract Compliance, User Feedback Loop

**What changed**:

1. **LLM-powered evaluation.** `run_eval.py` now calls Sonnet via `llm_eval_caller.py` to score agent output on 4 dimensions (structure, grounding, completeness, quality). Heuristic scoring remains as fallback. Contract compliance is the primary eval axis; generic quality is secondary.

2. **LLM-powered contract generation.** `build_contract.py` calls Sonnet to generate task-specific dispatch contracts with tailored rubrics, required sections, and grounding requirements. Falls back to heuristic templates for trivial queries or on LLM failure.

3. **Three-tier routing in async-task-gate.** The hook now routes tasks to three pipelines: (a) non-document async tasks → `spawn-gpu-agent.sh` directly, (b) short technical docs → `claude-dispatch.sh` with contract + eval, (c) research deliverables → `long-doc-orchestrate.sh` with auto mode selection.

4. **Auto mode selection.** `long-doc-orchestrate.sh` reads the word budget from the prompt file and selects the mode automatically: `<2000` words → single-raw, `2000-8000` → single-brain, `>8000` → learning-based selection from `mode_comparison.jsonl`.

5. **Brain assembler version-awareness.** `ra-brain-assembler` now reads deliverable synthesis pages for Pending Revision Areas and encodes them as hard requirements in `constraints.md`. Section writers read these constraints for their assigned section.

6. **Post-stitch eval contract-first.** `ra-post-stitch-eval` now uses contract compliance as its primary axis, outputting a structured checklist table. Reads `eval_calibration.md` for past user rejection patterns to avoid repeating the same misses.

7. **References section excluded from section writer loop.** References/Bibliography sections are compiled mechanically, not written by section agents.

8. **User feedback loop.** Two new scripts close the feedback loop: `capture-user-verdict.sh` records pass/fail/partial verdicts with freeform feedback, and `capture-user-edits.sh` diffs original vs. edited documents to capture structural changes. Both feed into `eval_calibration.md` and `edit_patterns.md` in the writing-team learner.

9. **Deliverable-aware dispatch evaluation.** `claude-dispatch.sh` now searches for `.md` deliverable files in `docs/` and `spaces/*/output/` rather than evaluating the raw CLI output log.

**New files**: `scripts/llm_eval_caller.py`, `scripts/capture-user-verdict.sh`, `scripts/capture-user-edits.sh`.

**Modified files**: `scripts/build_contract.py`, `scripts/run_eval.py`, `scripts/claude-dispatch.sh`, `scripts/long-doc-orchestrate.sh`, `.claude/agents/ra-brain-assembler.md`, `.claude/agents/ra-post-stitch-eval.md`, `.kiro/hooks/async-task-gate.kiro.hook`.

**Design principle established**: Contract compliance is PRIMARY eval axis, quality is SECONDARY. Requirements flow deterministically from wiki state through the brain package into constraints and outline, bounding LLM non-determinism with structural constraints. User verdicts and edits feed back into the learner for continuous calibration.

### 2026-05-08: IDE-Native Multi-Agent System + Wiki Knowledge Base

**Source**: `docs/handoff_2026-05-07_multiagent_system.md` (authoritative design document for all decisions).

**What was built**: A complete IDE-native multi-agent layer on top of the existing Python CLI system. 14 specialized Claude Code agents, a wiki knowledge base with 44 pages across 3 spaces, atomic ingest infrastructure, background dispatch with evaluation, and a learner system with token-capped pattern capture. Full details in the "Current Architecture (2026-05-08)" section above.

### 2026-04-25: Cross-Space Knowledge, Session Memory, Layered Config, Agent Protocol

**Source**: Analysis of [AWSMantle genai-rewrite branch](https://code.amazon.com/packages/AWSMantle/trees/genai-rewrite) for applicable patterns.

**What changed and why**:

1. **Cross-Space Knowledge Access with Isolation**
   - *What*: Spaces can now declare read-only references to other spaces' knowledge bases via `cross_space_sources` in persona.yaml. A `CrossSpaceReader` loads knowledge from multiple spaces, tagging each piece with its source space. Learnings and patterns remain isolated per space.
   - *Why*: Research papers span multiple domains (CRO, QNTR/Literature Review, DBA). The system needed to pull knowledge across spaces without breaking isolation of learned patterns. Inspired by Mantle's cellular isolation principle ("once a request enters a cell, it stays in that cell") applied to knowledge boundaries.
   - *Performance*: Zero additional LLM calls. Reader already reads files; this expands which files it can read.
   - *Clarification behavior*: When cross-space references are ambiguous, the system flags `[CLARIFICATION NEEDED]` rather than assuming.

2. **Single-File Cross-Session Memory**
   - *What*: At workflow end, a `session_memory.md` file (~2K tokens) is written per space containing recent query summaries, top strategies, known preferences, and cross-space patterns. Loaded at next workflow start alongside lessons.
   - *Why*: Memory was in-process only; patterns and strategies were lost between CLI runs. Mantle's "single-file memory MVP" pattern (write markdown, load into system prompt) provides cross-session continuity with zero infrastructure.
   - *Performance*: Zero additional LLM calls in the common case. LLM summarization only triggers when the file exceeds 2K tokens (roughly every 10-15 runs).

3. **Layered Configuration with Runtime Overrides**
   - *What*: Config now supports CLI flags and environment variables for runtime parameters: `--skip-parallel-eval`, `--max-iterations`, `--cross-space`, `--skip-learner-llm`. A `performance` section in config controls these defaults.
   - *Why*: Changing evaluation thresholds or disabling features required editing files. This gives speed knobs for quick iterations (e.g., `ra explain "topic" -p QNTR --skip-parallel-eval --max-iterations 2`).
   - *Performance*: Strictly positive. Provides explicit controls to trade quality for speed.

4. **Formalized Agent Interface Protocol**
   - *What*: Python `Protocol` classes define typed input/output for each agent role. Startup validation checks agent wiring before the workflow runs.
   - *Why*: `BaseAgent.execute(**kwargs)` was too loose; agents could be wired wrong without errors until runtime. Inspired by Mantle's `Service` trait pattern where every service declares its interface.
   - *Performance*: Zero. Validation runs once at startup in microseconds.

**Files touched**: `agents/base.py`, `config.py`, `spaces/loader.py`, `agents/reader.py`, `agents/learner.py`, `workflows/invoker.py`, `cli.py`, each space's `persona.yaml`.

### 2026-04-28: Binary File Reading, Sub-Agent Contract, CognitiveInfrastructure, Kiro Evolve

**Source**: Gap analysis on binary file handling, plus adoption of tools from the Amazon Builder GenAI Power Users community wiki.

**What changed and why**:

1. **Binary File Reading Utility**
   - *What*: A `scripts/read_binary.py` utility extracts text from PDF, DOCX, and XLSX files via Python (PyPDF2, python-docx, openpyxl). Supports full extraction, page ranges, specific sheets, and metadata-only mode.
   - *Why*: The workflows (explain, review, research, guide, quant) and the IDE need to consume binary source material directly. The ReaderAgent already had basic PDF/DOCX/XLSX support with a 10K-char truncation; that was removed so full documents can be read when needed. Token budget management stays at the `extract_relevant()` orchestration layer, not the extraction layer.
   - *Applies to*: Both Kiro IDE sessions and all five workflows.

2. **Binary File Reading Steering Rule**
   - *What*: New steering file `.kiro/steering/binary-file-reading.md` covering: supported formats, extraction commands, no-conversion-files rule, sub-agent delegation protocol for large documents, and orchestrator verification requirements.
   - *Why*: Previously I would claim inability to read binary files and ask for text alternatives. The steering rule removes that fallback and mandates the Python extraction path.

3. **Sub-Agent Contract for Large Documents**
   - *What*: For documents over 15 pages or 30,000 characters, full-document processing is delegated to a sub-agent via `invokeSubAgent`. The contract specifies:
     - Input: full extracted text plus explicit task instruction
     - Output: structured response with page/section references for every claim, a completeness declaration, and zero fabrication
     - Conduct: no partial extraction, no summary-only responses, no vague statements
     - Orchestrator verification: spot-check 2-3 claims against the source, flag missing page references, reject and re-delegate thin outputs
   - *Why*: Loading a 25-page paper into the main context exhausts it before analysis can happen. Sub-agent delegation preserves the main context while ensuring full coverage of the source. The fabrication controls (page references, completeness declaration) make the sub-agent's output verifiable.
   - *Applies to*: Both IDE and workflows. The AnalystAgent's completeness and grounding checks align with this contract when source material is a binary file.

4. **CognitiveInfrastructure MCP Server**
   - *What*: Installed via `aim mcp install cognitive-infrastructure-mcp`. Provides three tools: `kiro-recall` (hybrid keyword + vector search over curated knowledge with local transformers.js embeddings), `workspace-search` (BM25 index over the full project workspace), and `tool-router` (MCP proxy that keeps context window clean).
   - *Configuration*: `VAULT_DIR` environment variable in `~/.kiro/settings/mcp.json` points to the ResearchAssistant workspace root. The SQLite recall database lives at `.kiro/recall.db` (git-ignored). Required `npm rebuild better-sqlite3` on macOS ARM64 since the shipped binary was built for AL2023_x86_64.
   - *Why*: As the literature collection grows beyond 50+ PDFs across multiple spaces, finding the right source by filename becomes infeasible. Vector search over curated knowledge lets me query "find all papers discussing principal-agent theory" without loading full documents. Workspace search covers everything outside curated knowledge (specs, outputs, communications, learnings). No AWS credentials required, everything runs locally.
   - *Applies to*: Both IDE and kiro-cli (workflows) via shared MCP config at `~/.kiro/settings/mcp.json`.

5. **Kiro Evolve (IDE-Adapted)**
   - *What*: Persistent memory system that captures Kiro IDE conversations to daily transcript files, proposes knowledge graduation based on recurring patterns, consolidates graduated knowledge periodically, and cleans up old transcripts. Adapted from the CLI-based Kiro Evolve by @alanroth to use Kiro IDE hooks (`promptSubmit`, `agentStop`, `userTriggered`) instead of kiro-cli agent configs.
   - *Components*:
     - Shell scripts in `scripts/kiro_evolve_*.sh` handle transcript capture and the review/dream/cleanup check logic
     - Three hooks in `.kiro/hooks/` trigger the scripts on session events
     - Steering rule `.kiro/steering/kiro-evolve-trigger.md` enables the on-demand "evolve" command
     - Graduated knowledge lives at `.kiro/steering/evolved/` and is auto-loaded by the workspace steering system
     - Transcripts live at `~/.kiro/transcripts/` (user-level, not git-tracked)
   - *Gates*: Review triggers after 50+ prompts and 2+ days since last review. Dream triggers after 14+ days and 5+ evolved files. Cleanup triggers every 90 days on reviewed old transcripts.
   - *Why*: Cross-session memory. Decisions and preferences (e.g., "Holgersson is marginal, drop it from the literature review") would otherwise be lost between sessions. Every approval is explicit, which keeps the steering system under user control.
   - *Applies to*: Kiro IDE sessions. Graduated steering files also apply when kiro-cli reads the same `.kiro/steering/` directory during workflow execution.

**Files added**:
- `scripts/read_binary.py`
- `scripts/kiro_evolve_save_transcript.sh`
- `scripts/kiro_evolve_check_review.sh`
- `scripts/kiro_evolve_check_dream.sh`
- `scripts/kiro_evolve_check_cleanup.sh`
- `.kiro/steering/binary-file-reading.md`
- `.kiro/steering/kiro-evolve-trigger.md`
- `.kiro/hooks/kiro-evolve-save-prompt.kiro.hook`
- `.kiro/hooks/kiro-evolve-save-response.kiro.hook`
- `.kiro/hooks/kiro-evolve-check-all.kiro.hook`
- `.gitignore`

**Files updated**:
- `src/research_assistant/agents/reader.py` (PDF truncation removed, extracts full documents by default)
- `.kiro/steering/reference-provided-context.md` (point 3: binary formats now handled via extraction script)
- `~/.kiro/settings/mcp.json` (CognitiveInfrastructure server registered with VAULT_DIR env)

**MCP server troubleshooting note**: CognitiveInfrastructure ships as a Brazil-built Linux package. On macOS, the `better-sqlite3` native module needs a local rebuild: `npm rebuild better-sqlite3` in the MCP server's package directory. The server also expects `VAULT_DIR` to point to an existing directory; setting it to the workspace root solves this.
