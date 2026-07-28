# Section Writing Patterns
# Token cap: 1500 tokens
# Format: Trigger / Diagnosis / Action entries
# Graduation rule: 3 independent observations across different documents
# Purpose: What makes good section writing for section writer agents
#
# Entries below this line follow the schema:
# ---
# ## Pattern: <name>
# **Trigger**: <section type, document type, or condition>
# **Diagnosis**: <what went wrong or could improve>
# **Action**: <what the section writer should DO differently>
# ---

## Pattern: Single-brain word target adherence (GRADUATED 2026-05-13)

**Trigger**: term_paper, single-brain mode, multiple sections with targets 150-700 words
**Diagnosis**: Section writers in single-brain mode hit targets well: ±11% (v3b), ±6% excl. lit review (v3c), +1% overall (v3-final3). Lit review overshoots by 20-40% when 8+ sources assigned. Shorter sections (150-250 target) consistently tight (±9%).
**Action**: Non-lit-review sections: no intervention needed, writers are well-calibrated. Lit review sections: accept +20% overshoot as natural, or inflate target in brain (see outline_patterns.md).
**Observations**: 3 (qntr-termpaper-v3b, v3c, v3-final3)

## Pattern: "Paradigm" exemption in methodology sections (GRADUATED 2026-05-13)

**Trigger**: Section 3 (Research Methodology) discussing research philosophy or paradigms
**Diagnosis**: "Paradigm" is banned in human-authored-writing.md but has legitimate academic meaning in methodology sections (pragmatist paradigm, interpretive paradigm, etc.). Flagged as false positive in all 3 term paper runs.
**Action**: Pre-stitch and post-stitch eval should exempt "paradigm" when: (1) the section is titled "Methodology" or "Research Design", AND (2) the word modifies a research philosophy term. Section writers should continue using "paradigm" in this context. In non-methodology sections, "paradigm" remains banned.
**Observations**: 3 (qntr-termpaper-v3b, v3c, v3-final3)

## Pattern: "Comprehensive" is persistent AI-signal drift (GRADUATED 2026-05-13)

**Trigger**: Literature review or theoretical sections in term_paper/research_paper
**Diagnosis**: Writer uses "comprehensive" as a generic quality descriptor ("comprehensive governance framework", "comprehensive review") despite it being banned in human-authored-writing.md. Occurs in lit review sections across all 3 term paper runs.
**Action**: Section writer prompt must include explicit banned-word reminder with substitutions: "comprehensive" → "most complete", "most detailed", "broadest", or a specific descriptor of what makes it complete. This is a real drift pattern, not a false positive.
**Observations**: 3 (qntr-termpaper-v3c, v3-final3 post-stitch, v3-final3 pre-stitch)

## Pattern: Single-brain undershoot threshold is per-subsection SIZE, not count (GRADUATED 2026-07-16)

**Trigger**: literature_review or any document where a single section dispatch in single-brain mode contains multiple planned subsections.
**Diagnosis**: Section writers collapse a multi-subsection dispatch to summary depth (~28-30% of target) when individual subsections target 300-600 words each, but hit 84-104% when every subsection is capped small (≤350w) and explicitly enumerated with its own target. The failure driver is per-subsection target SIZE, not subsection count: cro-session7 held 3-5 subsections at 300-600w each and collapsed (28-30%); barneto-july held a 6-subsection §2 at 100-350w each and hit 104%; barneto-litfindings held §3 as 3 foundations x 3 moves at ≤200w each and hit 84% (1263/1500), a mild undershoot, not a collapse.
**Action**: For any subsection targeting >350w in single-brain, either (1) add "Produce ALL subsections at FULL specified length" to the section prompt, or (2) route that section to sequential mode. Subsections ≤350w with explicit per-subsection targets are safe in single-brain; expect 84-104% adherence. The brain assembler already applies this ("every subsection target kept under 350 words per section_patterns.md" appeared in the barneto-litfindings outline), so hold the ≤350w discipline in the outline stage.
**Observations**: 3 (cro-session7-review collapsed at 300-600w/subsection; barneto-july 104% at 100-350w; barneto-litfindings 84% at ≤200w moves). Confirmed again 2026-07-16: qntr-candidate-dimensions §2 held four subsections at ~260w each and hit 91% (958/1050), inside the 84-104% safe band.

# Expired observations (dropped without graduation, <3 observations):
# - [2026-05-14] Framework sections with propositions underbid word targets (1 obs, qntr-termpaper-v3-validated; no recurrence in 2 subsequent runs, expired 2026-07-16)
