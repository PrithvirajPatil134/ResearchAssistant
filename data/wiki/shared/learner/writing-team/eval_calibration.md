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

## 2026-07-30: LLM-judge cannot reliably score the no-absolute-absence rule — use a grep-gate

**Source**: 20-memo reliability experiment (`data/drafts/_experiments/barneto-memo-variance/`). 20 agents independently wrote the same advisor lit-findings memo from identical source extractions; each was then scored by an independent `ra-content-evaluator`.

**What the eval got wrong**: The evaluators flagged **all 20/20** memos as carrying 1-5 absolute-absence violations each. Direct grep of the strictly-forbidden forms found only **4/20** (memos 04, 10, 13, 20). The judge was miscounting the REQUIRED insufficiency framing ("does not yet exist", "has not yet been applied", "the literature remains limited on") as violations of the rule that mandates exactly that framing. An earlier LLM comparator on the same files erred the other way (said 3/20, missed memo-10). Two LLM passes, two different wrong counts; only the grep survived cross-checking.

**Diagnosis**: The no-absolute-absence clause (`.kiro/steering/no-assumption-rule.md`) is a binary, pattern-matchable distinction (forbidden universal-negative forms vs. permitted insufficiency forms). LLM judges do not hold that line consistently: they conflate the two because both talk about what the literature lacks. This inflated and compressed the `writing_standard` score, which was the only criterion showing spread. Grounding / completeness / coherence scored consistently (clustered ~9) and held up on spot-check; the judge is trustworthy on those.

**Action** (graduate immediately, do not wait for 3 observations — the remedy is deterministic and self-verifying):
1. Gate absolute-absence with `scripts/check-absolute-absence.sh <file>` (exit 1 = forbidden phrasing present, prints file:line:match). Tested against this experiment's ground truth: catches all 4 true violators, passes memos using permitted insufficiency framing. Run it in pre-stitch and post-stitch instead of asking the judge to count absence violations.
2. The judge should NOT be asked to produce an absolute-absence count as a scored criterion; if it reports one, treat the grep result as authoritative and the judge's count as advisory only.
3. General principle: for binary/pattern-matchable rules (em-dash ban, banned-vocabulary list, absolute-absence forms), prefer a deterministic grep-gate; spend the LLM-judge's budget on grounding, completeness, and coherence, which it scores reliably.

**Observations**: 1 (2026-07-30). **Status**: remedy GRADUATED (deterministic + tested); calibration finding logged as 1/3 toward a broader "judge is weak on pattern-rules" pattern. Watch whether banned-vocabulary and em-dash counts show the same judge noise on the next run.

---

## 2026-08-02: meta-narration / scaffolding leaked into a supervisor-facing deliverable — no rule existed

**Source**: user review of the v2 Barneto memo (`spaces/DBA/output/barneto-litfindings-jul2026_v2.md`).

**What leaked, and why the eval passed it**: The memo (a) narrated the supervisor's own instructions back at him ("My supervisor asked me to name the theoretical framework... offered disruption and decision theory as examples (supervision meeting, 17 June 2026)"; "Barneto asked on 17 June for the short list"), (b) referenced an internal unpublished artifact ("the circularity worry carried from the two-page note"), (c) printed internal orchestration tags in Exhibit 1 ("FD1 tag" column with PHENOMENON-EVIDENCE / METHOD-SPINE values), and (d) used process meta-narration ("I read disruption as...", "so I keep this lens at the conceptual level", "This memo establishes"). The pre/post-stitch evals passed it because NO WRITING RULE FORBADE ANY OF THIS. The eval agents only check rules that exist.

**Root cause (two layers)**:
1. Missing rule: human-authored-writing.md had no "no meta-narration / no scaffolding leak" clause.
2. Author-side: the ORCHESTRATOR'S OWN brain-package brief instructed section writers to tag each paper PHENOMENON-EVIDENCE / METHOD-SPINE and render it in Exhibit 1. The internal framing vocabulary from the planning conversation was piped directly into the deliverable. A gate helps, but the deeper fix is: do not author internal jargon (FD-numbers, framing tags) into briefs that section writers copy into prose. Keep framing decisions as *instructions to the writer* ("cite this paper for method only"), never as *labels to print*.

**Action** (graduate immediately, remedy is deterministic + tested):
1. `scripts/check-meta-narration.sh <file>` gates the pattern-matchable subset: framing tags, advisor-instruction phrasings, internal-artifact names. Tested against the v2 memo: caught all four leak classes.
2. human-authored-writing.md rule 6 ("No meta-narration or scaffolding leaks") added; pre-stitch check 5f and post-stitch check 4c invoke the gate AND require a fuzzy-form judgment for the process-narration the grep cannot catch.
3. Brain-assembler / brief-authoring guidance: framing decisions are writer instructions, not printable labels. Never put FD-numbers or PHENOMENON-EVIDENCE/METHOD-SPINE style tags into an exhibit or prose that a reviewer sees.

**Observations**: 1 (2026-08-02). **Status**: gate GRADUATED. Broader lesson (now 2 instances with the 2026-07-30 entry): for reviewer-facing deliverables, binary writing rules (absolute-absence, meta-narration, em-dash, banned-vocab) belong in deterministic grep-gates; the LLM-judge is reserved for fuzzy judgment (process-narration register, voice, argument coherence).

---
