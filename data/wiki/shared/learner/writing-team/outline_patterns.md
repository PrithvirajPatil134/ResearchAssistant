# Outline Patterns
# Token cap: 1500 tokens
# Format: Trigger / Diagnosis / Action entries
# Graduation rule: 3 independent observations across different documents
# Purpose: What makes good outlines for the brain assembler
#
# Entries below this line follow the schema:
# ---
# ## Pattern: <name>
# **Trigger**: <when does this apply>
# **Diagnosis**: <what went wrong or could improve>
# **Action**: <what the brain assembler should DO differently>
# ---

## Pattern: Pre-stitch eval heuristic range mismatch for short docs (GRADUATED 2026-05-13)

**Trigger**: Documents with total word target under 5000 words (term_paper, technical_guide).
**Diagnosis**: The pre-stitch eval heuristic checks a fixed 1200-1800 word range per section. For term papers (150-700 words/section) and technical guides, every section fails even when it meets brain-specified targets. The issue is in the eval infrastructure, not the outline.
**Action**: Brain assembler must include per-section word targets in constraints.md (already does). Pre-stitch eval must read those targets and use ±30% tolerance per section, not a global fixed range. Until the heuristic is patched, pipeline should proceed to stitch despite pre-stitch failure when section word counts are within ±30% of outline targets.
**Observations**: 3 to graduate; 4 confirmations (replication-fda-v4, qntr-termpaper-v3b, qntr-termpaper-v3-final3, barneto-litfindings-jul2026 [§1 99%, §3 84%, §4 98% vs fixed 400-600 band]). The heuristic remains unpatched as of 2026-07-16; every short-doc run still trips it. Patch priority is rising.

## Pattern: Lit review sections need inflated word targets when source-dense (GRADUATED 2026-05-13)

**Trigger**: Any literature review section with 8+ source assignments in the outline.
**Diagnosis**: Writers consistently overshoot word target by 20-40% when synthesizing 8+ sources because adequate synthesis of that density requires more prose. Shorter sections (3-5 sources) hit targets within ±9%.
**Action**: Brain assembler should add 25% to lit review word target when assigning 8+ sources. Example: 700-word target with 12 sources → set target to 875 words.
**Observations**: 3 (qntr-termpaper-v3b +40%, qntr-termpaper-v3c +40%, qntr-termpaper-v3-final3 +20%)
