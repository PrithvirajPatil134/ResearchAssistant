# Progress Log — Kiro → Claude Code Upgrade

Append-only. Newest entry at top. Record what changed, how it was verified, and
what remains. One entry per work session or wave.

---

## 2026-07-27 — Wave 6.5 + 6.2 DONE

**Wave 6.5 (stale wiki indexes) — DONE.** Built `scripts/rebuild-wiki-index.py`
(regenerates per-type sections from page frontmatter via venv PyYAML; preserves
header + prose tail; skips non-standard indexes). Rebuilt QNTR (was Sources(0),
now 24/6/2/2/1), CRO (4/1), DBA (14/5/1/1). CW skipped (non-standard, no pages).
ra-wiki-lint warnings 210 → 180 (the 29 not-in-index warnings resolved), 0 errors.
Commit 0e31a8a.

**Wave 6.2 (schedule maintenance tier) — DONE (artifacts).** `crontab.example`
already existed (my earlier "missing" claim was wrong — it just was never
installed; crontab -l = 0 entries). Added the rebuild-wiki-index and storage-audit
weekly jobs. Built `scripts/install-crontab.sh`: idempotent (marked block, re-run
replaces not duplicates), with --dry-run and --uninstall. Dry-run verified; the
user's crontab was NOT modified. Installing cron is an explicit user step
(`bash scripts/install-crontab.sh`) because it changes the user environment.
Commit 6aeca7e.

**Remaining in Wave 6:** 6.1 (CLOSED — pipeline-output writing enforcement lives
in the pre/post-stitch eval agents, confirmed during 6.6); 6.4 (ingest the ~169
uncaptured knowledge/comm files + resolve orphans — content work, not migration).

---

## 2026-07-27 — Wave 6.6 DONE (eval mechanism confirmed + repaired)

**Eval mechanism confirmed in place, with one real defect fixed.** Confirmation
grounded in the actual files:
- Agent-based gate (CC-primary): ra-content-evaluator (4 criteria, hard-fail on
  ANY unsourced claim → score 0, structured pass/fail/hard_fail verdict);
  ra-pre-stitch-eval + ra-post-stitch-eval enforce human-authored-writing.md
  (banned vocab, em-dash grep = gate failure, citation coverage). This also
  ANSWERS Wave 6.1: the writing standard IS enforced on pipeline output by these
  eval agents, not by the main-session PostToolUse hook.
- Scoring engine run_eval.py: threshold 7.5, heuristic fail-fast (empty/echoed/
  tool-artifact → 0) per eval-principles.md.

**Defect found + fixed (Wave 6.6):** build_contract.py and run_eval.py import the
research_assistant package (needs pyyaml+click). System Homebrew python3 3.14
(PEP 668) lacks them → tools crashed with ModuleNotFoundError: yaml. Worse,
claude-dispatch.sh swallowed the failure (2>/dev/null || true) and proceeded with
an EMPTY contract — the shell eval gate ran silently degraded.
- Fix: project `.venv` (gitignored) with `pip install -e .` (declares click+pyyaml).
- claude-dispatch.sh + jig-compare.sh resolve `RA_PYTHON` = .venv/bin/python3 if
  present, else python3; eval-tool calls use it (inline stdlib python3 -c left as-is).
- claude-dispatch.sh now WARNS LOUDLY (with stderr detail) if the contract build
  yields nothing, instead of silently masking a degraded gate.
- Fixed a real SyntaxWarning in invoker.py:797 (invalid \] \) escapes → cleaned
  the char set, membership preserved). Verified end-to-end: build_contract +
  run_eval both work via venv; run_eval correctly failed a thin placeholder.
- Memory written: eval-mechanism-requires-venv (recreate with venv + pip -e . if
  .venv is ever deleted).

**Remaining:** 6.2 (scheduling), 6.4 (ingest backlog), 6.5 (stale indexes).

---

## 2026-07-27 — Wave 6.3 PASS (live pipeline proof) + wiki tracked

**Wiki tracking (durability gap) — DONE.** The canonical wiki
(src/research_assistant/spaces/*/wiki) + shared wiki (data/wiki) were on disk but
never git-tracked. Added 95 wiki .md pages; gitignored *.base. Commit 7469e5e.
ra-wiki-lint 0 errors at commit time.

**Wave 6.3 live long-doc pipeline run — PASS.** Dispatched the hardened
`ra-brain-assembler` (Wave 4: 1M pin, canonical paths, strengthened sourcing)
against QNTR for a real literature_review. Verified against disk, not trusted:
- Read 29 canonical wiki content files from src/research_assistant/spaces/QNTR/wiki
  (the 34-page tree), NOT the deleted 3-page legacy tree. Wave 1 path fix proven.
- Wrote 10 brain files (voice, argument-map, terminology, methodology-context,
  advisor-guidance, literature-map, constraints, exhibits-plan, outline,
  decisions.log) to .kiro/.long-doc/qntr-agentic-governance-litreview-verify/brain/.
  Confirmed present with real sizes. Grounding spot-checked: cited pages exist.
- Derived a coherent thesis + 5 wiki-backed arguments; raised 1 [WIKI GAP]
  (consultancy governance-ROI report), no [THESIS GAP].

This one run validated the whole chain: Wave 1 (canonical read), Wave 4 (hardened
agent), Wave 5 (legacy gone / canonical intact), and no-assumption discipline
inside the dispatched agent.

**NEW BUG surfaced by the run (logged as Wave 6.5):** QNTR `_index.md` is STALE —
its headers say "Sources (0) / Concepts (0) / Methods (0)" while the filesystem
holds 24 sources + 6 concepts. The agent correctly trusted the filesystem over the
stale index (no-assumption rule) and read the real files — the exact silent-failure
this run was checking. Root cause: `_index.md` files were never regenerated as
pages were added. This is content-maintenance (same family as the 29 not-in-index
warnings), NOT a migration defect. Added as Wave 6.5.

---

## 2026-07-27 — Wave 5 complete (legacy tree reconciled + regression guard) + Wave 6 logged

**Wave 5 — DONE, verified.** The legacy `spaces/*/wiki` tree is reconciled and
removed with zero content loss.

- 5.1: `principal-agent-theory.md` (unique, 22.8KB) migrated to
  `src/research_assistant/spaces/QNTR/wiki/concepts/`; added the 3 missing required
  fields (created, originating_space, applicable_to).
- 5.2: Gioia source notes migrated to
  `src/research_assistant/spaces/QNTR/wiki/sources/gioia-2013-qualitative-rigor.md`
  (clean slug); added type/created/originating_space/applicable_to.
- 5.3: `berente-2021` — kept the canonical page (5 cross-refs point at it) and
  ported the 3 sections unique to the legacy validated copy (Open Questions,
  Tensions with Other Sources, Cross-Space Promotion Notes). Canonical 4.9KB→9.1KB.
- 5.4: deleted `spaces/QNTR/wiki` only. All `spaces/*/output/` deliverables (~19
  files) left untouched — the legacy tree was NOT wholesale-deletable, contrary to
  the first plan draft.
- 5.5: added harness-doctor check 4 (no bare `spaces/*/wiki` refs) and
  `.claude/hooks/README.md`.

**The regression guard paid off immediately.** Check 4's first run FAILED on
`obsidian-graph-linker.py` — a script in NONE of the 5 audit clusters. Verified it
was actually canonical-correct (discovery roots are `src/research_assistant/spaces`;
the flagged lines are string markers that legitimately match inside canonical
paths). Tightened the guard to a PCRE negative-lookbehind so canonical never
matches, and removed the script's dead `EXCLUDED_TREE` (pointed at the deleted
legacy tree). harness-doctor: ALL GREEN (4/4).

**Wave 6 logged (NOT done).** Critical self-review surfaced coverage gaps that the
main waves did not close, recorded honestly rather than declaring victory:
- 6.1 subagent/pipeline write enforcement (main-session PostToolUse hooks don't
  see subagent or script writes).
- 6.2 the maintenance tier is unscheduled (0 cron entries).
- 6.3 the long-doc pipeline was path-fixed but never RUN end-to-end.
- 6.4 the 169-file ingest backlog + 29 orphan pages (content work).

**State:** Waves 0-5 complete. Wave 6 is the honest open list.

---

## 2026-07-27 — Wave 4 complete (23 agents CC-compliant + hardened)

**Wave 4 — DONE, verified.** All 23 `.claude/agents/*.md` are now full Claude
Code subagents and carry the hardened contracts.

- 4.0/4.1: spec-audit (via claude-code-guide subagent) confirmed all 23 already
  had valid name/description/tools frontmatter; the only gap was a missing
  `model:` field. Cross-checked against the 23 raw frontmatter blocks.
- 4.2: pinned `model: claude-opus-4-8[1m]` on all 23 (exactly one line each,
  inserted after `tools:`). VERIFIED the id against `~/.claude/settings.json`
  `availableModels` (enforceAvailableModels:true) — the spec agent had wrongly
  claimed `[1m]` was non-standard and suggested `opus`/`claude-opus-4-5`, which
  would have been an unregistered id. Trusting-but-verifying caught it.
- 4.3: 14 agents shared an identical weak one-line Hard Rule (dropped
  "citation, source, quotation" and the override clause). Strengthened all 14 to
  include those terms, the override clause, and a pointer to
  `no-assumption-rule.md`. The other 9 already had full-form or stronger. Net:
  0 agents left on the weak rule.
- 4.4: added an explicit "No Absolute-Absence Claims" guard to the 3 agents that
  make gap statements (gap-table-builder, litreview-builder, methodology-advisor).
- 4.5: mandated a canonical `target_path:` in ra-wiki-ingestor (space →
  src/research_assistant/spaces/..., shared → data/wiki/shared/...), closing the
  cluster-2 footgun where ingest-commit.sh would write to whatever tree the
  ingestor named.

Verification: 23/23 frontmatter compliant, all carry full/strengthened sourcing
rule, absence guard in exactly 3, target_path mandate present, harness-doctor
ALL GREEN.

**Remaining:** Wave 5 (legacy-tree reconciliation + regression guard, destructive).

---

## 2026-07-27 — Wave 2 complete (enforcement layer rebuilt as CC hooks)

**Wave 2 — DONE, verified against the documented hook contract.** The Kiro
enforcement hooks (inert under CC because CC never reads `.kiro/hooks/`) are
rebuilt as Claude Code hooks in `.claude/hooks/`, registered in
`.claude/settings.json`. Kiro originals preserved.

New files (all `bash -n` clean, executable):
- `.claude/hooks/wiki-lookup.sh` — UserPromptSubmit. Injects the 6-category
  task-grounding protocol (communication/document/infrastructure/research/ingest/
  general) as stdout context on exit 0. Phrased as factual statements per the
  doc's prompt-injection caution. Carries the Kiro classifier; paths canonical.
- `.claude/hooks/writing-gate.sh` — PostToolUse (Edit|Write|MultiEdit). On a
  submission-ready write (workspace/|output/|assignment/ or Submission|Paper|
  Teaching|Case|revised in the name; code/config skipped), emits additionalContext
  to scan against human-authored-writing.md. Consolidates the two Kiro writing
  hooks. Non-blocking (PostToolUse cannot block; tool already ran).
- `.claude/hooks/py-lint.sh` — PostToolUse (Edit|Write|MultiEdit). On agent/
  workflow/core Python writes, runs py_compile; exit 2 + stderr surfaces syntax
  errors to Claude. No-op elsewhere.

settings.json: SessionStart + permissions preserved; UserPromptSubmit and
PostToolUse added.

**Verification (6 cases, all pass):** valid JSON + SessionStart intact;
wiki-lookup injects on exit 0; writing-gate emits additionalContext for a
submission file and no-ops for a .sh; py-lint returns exit 2 with the exact
SyntaxError for broken agent Python and exit 0 for non-agent files.

Caveat: tests confirm the scripts honor the documented stdin/exit contract.
Live routing of real CC events through them activates on next SessionStart
(hooks load at session start, like skills and the slim context).

**Remaining:** Waves 4, 5 TODO.

---

## 2026-07-27 — Wave 1 complete (directory migration finished)

**Wave 1 — DONE, verified.** All operational reads/writes moved off the legacy
`spaces/*` tree to canonical `src/research_assistant/spaces/*`.

Scripts (all pass `bash -n`):
- `long-doc-orchestrate.sh:290` brain-assembler wiki read → canonical.
- `long-doc-orchestrate.sh:1019` devil's-advocate eval read → canonical.
- `long-doc-orchestrate.sh:1362` delivery dir → prefer-canonical/fallback-legacy
  (decision: fallback pattern, mirrors line 1179).
- `ra-wiki-lint.sh:224,274` checks 6-7 driver loops → canonical.
- `ingest-rollback.sh:99` safety-net glob → canonical added (legacy+shared kept).
- `ra-storage-audit.sh:82,125`, `ra-weekly-status.sh:63,97,116`,
  `image-orphan-scan.sh:32,47` → canonical.

Agent defs (operational reads/writes only):
- ra-brain-assembler (5 reads), ra-wiki-reviewer (2), ra-wiki-linter (3 roots),
  ra-email-drafter (write target), ra-orchestrator (guard), ra-wiki-ingestor
  (explicit canonical `_index.md`).

**1.15 RECLASSIFIED, not a bug.** The remaining `[spaces/{SPACE}/knowledge/...]`
strings in 11 agents are citation-format examples matching `no-assumption-rule.md`
verbatim, not operational paths. Changing agents alone would desync them from the
governing steering rule and the ~92 existing wiki pages using that provenance
convention. Deferred to a separate convention-change decision.

**Verification result — the fix WORKS and proves itself:** `ra-wiki-lint.sh` check 6
(coverage gap) went from a false "all clean" to 169 real warnings (un-ingested
knowledge/communication files, e.g. CRO Session PDFs with no wiki source page),
plus 29 not-in-index. 0 errors, RESULT PASS. Spot-checked: flagged files are real
and genuinely lack wiki pages. The check that was silently dead is now honest. The
169 gaps are a CONTENT backlog (future ingest work), not a Wave-1 defect.

**Remaining:** Waves 2, 4, 5 TODO. Note the 169-file ingest backlog and 29 orphan
pages as separate content-work items (not part of the CC-migration waves).

---

## 2026-07-27 — Audit complete, plan established, Wave 0 done

**Wave 0 (foundation) — DONE, verified.**
- CLAUDE.md slimmed: base context 564,782 → 40,203 bytes (9 imports). Verified
  active this session via `harness-doctor.sh` (all green, 3 invariants pass).
- Four skills created and live: `/consensus-search`, `/longdoc`, `/ingest`,
  `/doctor`. Confirmed present in the Skill tool listing after reload.
- `ra-wiki-lint.sh` checks 1-5 fixed (dual-tree scan, `[[path|label]]` split,
  workspace-relative ref resolution). Error count 102 → 4 → 0 after schema fixes.
- 4 shared-wiki pages given `originating_space: shared` (gioia-qualitative-rigor,
  baron-kenny-moderation-mediation, mixed-methods-sequential-design,
  thesis-proposal-requirements). Verified against 8 sibling pages that had it.

**Audit — DONE.** Five read-only cluster agents ran concurrently (the first
successful large fan-out since the context fix; would have died on "Prompt is too
long" before). Findings consolidated in `audit-findings.md`. Two root causes:
(A) incomplete `spaces/` → `src/research_assistant/spaces/` migration;
(B) Kiro→CC runtime switch orphaned all 26 `.kiro/hooks/`.

**Decisions recorded:**
- Wave 3 (revive Kiro evolve transcript loop) — SKIPPED. Claude Code memory +
  maintained wiki cover the role; no parallel loop.
- Plan + logs live in `docs/workspace-upgrade/`. New CC hook scripts will live in
  `.claude/hooks/`.
- OPEN: delivery-dir strategy for `long-doc-orchestrate.sh:1362` (hard-switch vs
  prefer-canonical/fallback). Recommendation on file: fallback pattern.

**Remaining:** Waves 1, 2, 4, 5 all TODO. Next up: Wave 1 (finish the directory
migration) pending owner approval of the diffs and the 1.3 delivery-dir decision.
