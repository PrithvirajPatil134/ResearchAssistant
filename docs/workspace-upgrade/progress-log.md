# Progress Log — Kiro → Claude Code Upgrade

Append-only. Newest entry at top. Record what changed, how it was verified, and
what remains. One entry per work session or wave.

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
