# Outline Failures (Recent)
# Token cap: 800 tokens
# Rolling window: 7 days — entries older than 7 days are either graduated
# to outline_patterns.md (if 3+ observations) or dropped
# Format: Trigger / Diagnosis / Action entries with dates
# Purpose: Recent outline mistakes that haven't yet graduated to patterns
#
# Entries below this line follow the schema:
# ---
# ## [YYYY-MM-DD] Failure: <name>
# **Trigger**: <task type and conditions>
# **Diagnosis**: <what went wrong>
# **Action**: <what to do differently next time>
# ---

## [2026-07-16] Failure: Outline eval double-counts nested subsection word targets

**Trigger**: literature_review outline where a parent section carries a word target AND its subsections carry individual targets (e.g. §3 "1500 words" then "three foundations ~500 each" then "three moves ≤200w each").
**Diagnosis**: Outline eval reported "9350 words targeted" for barneto-litfindings, a document whose outline.md totals 3000 (250+450+1500+350+450) and whose constraints.md caps it at ~3000 with an explicit OVERRIDE of the generic range. The eval summed parent-section AND nested-subsection targets, roughly tripling the true figure. A grossly inflated figure could false-pass a runaway target or false-flag a length mismatch downstream. Here it passed harmlessly, but the number is wrong.
**Action**: Outline eval must count word targets at ONE level only. Where a section lists both a parent target and per-subsection targets, use the parent target (subsections decompose it, they do not add to it). Cross-check the derived total against the explicit "Total: ..." line the brain assembler writes at the bottom of outline.md.

## [2026-07-16] Failure: Pre-stitch counts mechanically-compiled References as a missing section file (recurring, 2/3)

**Trigger**: Outline flags References "compiled mechanically, not a section-writer task"; no section_N.md is produced for it by design.
**Diagnosis**: Pre-stitch eval reported "Section 6: file missing" for barneto-litfindings. References is intentionally excluded from the section-writer loop (2026-05-14 pipeline design + this outline). Same class as the expired 2026-06-29 "Section 5 (References) file missing" entry, now recurring. The heuristic counts every outline heading and expects a matching section file.
**Action**: Pre-stitch eval must skip any outline section flagged "compiled mechanically" / "not a section-writer task" when checking for section files. Read the outline's per-section notes; do not assume section_N.md exists for every heading.
**Observations**: 2 (2026-06-29 cro-session7; 2026-07-16 barneto-litfindings). Needs 1 more to graduate.

# GRADUATED 2026-07-16 → section_patterns.md: "Single-brain undershoot threshold
#   is per-subsection SIZE, not count" (cro-session7, barneto-july, barneto-litfindings).
# Expired (<3 obs, dropped): advisor-mandated content omitted (1); summary line
#   dispatched as section (2); embedded table budget not in target (1).
