# Terminology Drift Log
# Token cap: 500 tokens
# Format: Term | Expected (from brain/terminology.md) | Actual (in section) | Section | Date
# Purpose: Track when section writers deviate from canonical terminology
# Retention: keep only the 20 most recent entries; older entries are summarized
#            into a single "common drift patterns" block at the top
#
# Common drift patterns:
# - "comprehensive": persistent in lit review sections (3 observations, graduated).
#   Writer defaults to it as a generic quality descriptor. Fix: explicit
#   substitution list in section prompt.
# - "paradigm": FALSE POSITIVE in methodology sections (3 observations, graduated).
#   Refers to research paradigms. Eval should exempt in methodology context.
# - "at its core": appeared once (v3-final3). Watch for recurrence.
#
# Recent entries:
# | Term | Expected | Actual | Section | Date |
# |------|----------|--------|---------|------|
# | paradigm | (exempt in method) | "pragmatist paradigm" | Section 3, qntr-termpaper-v3-validated | 2026-05-14 |
# | paradigm | (exempt in method) | "pragmatist paradigm" | Section 3, qntr-termpaper-v3-final3 | 2026-05-13 |
# | comprehensive | (banned) | "comprehensive" (line 33) | Section 2, qntr-termpaper-v3-final3 | 2026-05-13 |
# | at its core | (banned phrase) | "at its core" (line 21) | Section 2, qntr-termpaper-v3-final3 | 2026-05-13 |
