# Eval Calibration Log

Records where the pipeline eval verdict diverged from the user's actual verdict.
The post-stitch eval agent should read this file and treat each entry as a
"DO NOT REPEAT" pattern: if a similar document type comes through, check for
these specific failure modes.

---

## GRADUATED PATTERN: Contract-first eval (3 observations, stable)

**Rule**: Check advisor-guidance.md requirements as binary checklist BEFORE scoring quality. Produce a structured compliance table with present/absent per item.
**Observations**: 3 (v3-final3 miss 2026-05-14, cro fix 2026-06-29, barneto clean 2026-07-07)
**Status**: PERMANENT. All future post-stitch evals must produce the contract compliance table as Gate Check 0 before any quality scoring.

---

## 2026-05-14: qntr-termpaper-v3-final3 (pipeline=pass, user=fail)

**What the eval missed**: Missing gap table (Han et al. 2017 style), missing market evidence (McKinsey/Deloitte), missing Discussion section, missing Diamantopoulos/Hildebrandt citations. 2/6 Prashar requirements met. Eval passed but should have failed.

**Pattern**: Trigger: qntr document type with advisor revision requirements. Diagnosis: Eval scored on prose quality, missed contract items. Action: Check advisor-guidance.md requirements as binary checklist BEFORE scoring quality.

---

## 2026-06-29: cro-session7-review (pipeline=pass, user=TBD)

**What the eval caught correctly**: Applied binary contract checklist first (per pattern above). 11/12 items present. Single miss was 3.2% word count overshoot (minor). Post-stitch eval correctly failed the first attempt (1627 words, 2 citations) and passed the second (3574 words, full contract compliance).

**Pattern confirmed**: The eval_calibration fix from 2026-05-14 is working. Post-stitch eval's `eval_calibration_pattern_check` field explicitly confirmed it read and applied the pattern. No divergence expected on this run (pipeline verdict aligned with contract requirements).

---

## 2026-07-07: barneto-july-theory-selection-litreview (pipeline=pass, user=TBD)

**What the eval caught correctly**: Post-stitch eval produced 12-item binary contract compliance table. All 12 present. Explicitly noted reading eval_calibration.md patterns from 2026-05-14 and 2026-06-29. No divergence expected.

**Note**: This is the 3rd clean pass using the contract-first approach. Pattern graduated above.

---

## 2026-07-16: qntr-candidate-dimensions-prashar-jul2026 (outer-heuristic=fail, benchmark+post-stitch=pass)

**What diverged**: The outer heuristic eval FAILED the document on "Too few citations (3)" — a raw distinct author-year count. The benchmark comparator measured citation DENSITY at 12.6/1000w (high end of the A* band) and passed with 0 flags; post-stitch contract-first eval also passed (all items present, 5 page-anchored quotes spot-verified). Delivery proceeded correctly via the benchmark override.

**Pattern**: Trigger: advisor working paper / synthesis memo drawing deeply on a small source core (~7 sources) with page anchors, yielding a low absolute citation count. Diagnosis: the outer citation heuristic is journal-tuned to absolute distinct-citation count and misfires on the deep-source-core advisor form. Same class as the graduated pre-stitch word-range false positive. Action: outer-eval citation check should use density per 1000 words (~8-10/1000w threshold) for advisor/working-paper forms, or defer to the benchmark comparator's density figure, rather than absolute count. **Observations**: 1/3 toward graduation. Watch on next advisor-memo run.

**Also confirmed (4th clean application)**: Post-stitch eval built the binary Gate Check 0 checklist before quality scoring; all 5 advisor-guidance items and 12 hard requirements present. Contract-first pattern holding.

---
