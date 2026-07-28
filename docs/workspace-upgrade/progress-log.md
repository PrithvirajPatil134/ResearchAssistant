# Progress Log — Kiro → Claude Code Upgrade

Append-only. Newest entry at top. Record what changed, how it was verified, and
what remains. One entry per work session or wave.

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
