# Stitching Patterns
# Token cap: 1000 tokens
# Format: Trigger / Diagnosis / Action entries
# Graduation rule: 3 independent observations across different documents
# Purpose: What makes good assembly/stitching for the doc-stitcher agent
#
# Entries below this line follow the schema:
# ---
# ## Pattern: <name>
# **Trigger**: <document length, section count, or condition>
# **Diagnosis**: <what went wrong or could improve>
# **Action**: <what the stitcher should DO differently>
# ---

## Pattern: Short docs stitch cleanly without sliding window (GRADUATED 2026-05-14)

**Trigger**: term_paper or short documents under 5000 words, any mode, 5-7 sections
**Diagnosis**: Stitcher processes all sections in a single pass (~2.5-3 min). Output word count nearly unchanged (±15 words). Minimal expansion from transition smoothing. No sliding window triggered (threshold: 10,000 words).
**Action**: For documents under 5000 words, single-pass stitching is confirmed optimal. The 10,000 word sliding-window threshold is correct. No adjustment needed. Stitch time for short docs: budget 3 minutes.
**Observations**: 4 (qntr-termpaper-v3b 2435w, qntr-termpaper-v3-final3 2479w, qntr-termpaper-v3-validated 3499→3493w, barneto-july 2950→2962w)

## [2026-07-16] Observation: Internal workspace source markers survive to the delivered draft (1/3)

**Trigger**: Advisor-facing or external-facing document where the no-assumption rule requires inline source paths during drafting.
**Diagnosis**: The barneto-litfindings v1 was delivered with `[data/drafts/...]`, `[syntheses/...]`, `[data/summaries/...]` markers embedded throughout. The benchmark report flagged this as delivery-blocking: the Barneto advisor fingerprint explicitly requires internal markers stripped before sharing. The markers are needed during writing and eval (they prove sourcing), but the reader must not see them, and the pipeline has no strip step between post-stitch and delivery for external documents.
**Action**: Add a marker-strip step (a stitcher/abstract-stage instruction or a dedicated post-eval pass) for advisor-facing and external documents. It should run AFTER post-stitch eval verifies sourcing and BEFORE delivery, converting inline workspace source paths into a discreet evidence-status footnote or removing them, while keeping the marked copy in the working dir for provenance.
**Observations**: 1/3 (barneto-litfindings-jul2026). Inconsistent across advisor docs: qntr-candidate-dimensions (2026-07-16, Prashar memo) delivered with ZERO markers (grep-verified), barneto-litfindings delivered WITH them. A dedicated strip step is still warranted, but the failure did not recur here. Watch the next external-facing document.

## [2026-06-29] Observation: Stitcher acts as content generator when sections are thin (1/3)

**Trigger**: Sections total 1267 words against a 3900-word outline target (32% of target). Post-stitch eval fails on word count and citation count.
**Diagnosis**: When section writers dramatically undershoot targets, the stitcher is asked to re-stitch with gate feedback. The stitcher expanded from 1488 words (first attempt) to 3574 words (second attempt), a 2.4x expansion. This means the stitcher generated ~2000 words of new content including full subsections, page-referenced citations, and analytical prose. The document passed eval but this is architecturally wrong: the stitcher's role is transitions and voice, not content generation.
**Action**: (1) If pre-stitch eval shows sections at <50% of outline target, the pipeline should re-dispatch section writers with explicit feedback rather than passing the problem to the stitcher. (2) If the stitcher must expand, limit expansion to 50% above incoming word count; beyond that, flag for section re-write. Current behavior works (final doc passed all gates) but puts too much quality burden on a single re-stitch agent.
**Observations**: 1 (cro-session7-review: 1267→3574 = 2.8x). Needs 2 more to graduate.
