# Voice Calibration
# Token cap: 500 tokens
# Format: Adjustments to voice parameters based on user feedback
# Purpose: Track voice refinements from post-delivery user corrections
# Graduation rule: after 3 consistent corrections in the same direction,
#                  the adjustment becomes a permanent voice rule
#
# Permanent voice rules: (none yet)
#
# Recent adjustments:
# ---
# ## [YYYY-MM-DD] Adjustment: <description>
# **Source**: user correction on doc_id <id>
# **Before**: <what the voice was doing>
# **After**: <what the user wanted instead>
# **Observations**: N/3 toward graduation
# ---

## Permanent Rule: No em dashes, no formulaic openers, academic third-person (GRADUATED 2026-05-14)

**Source**: 3 consecutive IS term paper runs (v3b, v3-final3, v3-validated)
**Rule**: IS term papers use academic third-person prose with zero em dashes, zero banned openers (Furthermore, Moreover, Additionally, Consequently, Subsequently, Nevertheless), varied sentence rhythm, no contractions. Current voice.md instructions are well-calibrated for this genre. No intervention needed.
**Observations**: 3/3 (v3b, v3-final3, v3-validated all passed voice checks cleanly)
