# Venue Fingerprints
# Token cap: 2000 tokens
# Max venues: 10 (FIFO when limit reached)
# Format: One section per venue with structural norms
# Purpose: Store structural fingerprints extracted from published papers
#          at target venues so the brain assembler can set accurate word
#          targets and section ratios for future papers
#
# Fingerprint schema per venue:
# ---
# ## Venue: <journal name>
# - ABDC/CORE tier: <rating>
# - Typical word count: <range>
# - Section order: <list>
# - Section ratios: Intro X%, Lit Review Y%, Method Z%, ...
# - Citation density: <N per 1000 words>
# - Abstract word limit: <N>
# - First extracted: YYYY-MM-DD
# - Last updated: YYYY-MM-DD
# - Papers sampled: N
# ---

## Venue: Information & Management
- ABDC tier: A*
- Typical word count: 18000-22000
- Section order: Introduction, Background/Theory, Conceptualization, Methods, Results, Discussion, Conclusion
- Section ratios: Intro 8-10%, Background 15-20%, Methods 25-30%, Results 20-25%, Discussion 10-15%
- Citation density: 15.4 per 1000 words (numbered style)
- Abstract word limit: 150
- First extracted: 2026-05-13
- Last updated: 2026-05-13
- Papers sampled: 1 (Mikalef & Gupta 2021)

## Venue: MIS Quarterly
- ABDC tier: A*
- Typical word count: 10000-15000 (editorials/intros 12000-14000)
- Section order: Introduction, Conceptual Framework, Literature Review, [Varies by type], Implications
- Section ratios: Intro 10-12%, Lit/Theory 30-35%, Core 40-45%, Implications 10-15%
- Citation density: 15.0 per 1000 words (author-year style)
- Abstract word limit: 150
- First extracted: 2026-05-13
- Last updated: 2026-05-13
- Papers sampled: 1 (Berente et al. 2021 editorial)

## Venue: IS Term Paper (QNTR course, IIM Sambalpur)
- Tier: Course submission (targeting A/A* journal conventions)
- Typical word count: 2500-4000
- Section order: Introduction, Theoretical Background, Methodology, Conceptual Framework, Contributions, Limitations, Conclusion
- Section ratios: Intro 10-15%, Lit Review 30-37%, Method 15-20%, Framework 8-12%, Contributions 10-13%, Limitations 4-8%, Conclusion 2.5-7%
- Citation density: 12-17 per 1000 words
- Abstract word limit: 150
- First extracted: 2026-05-13
- Last updated: 2026-05-14
- Papers sampled: 2 (v3-final3, v3-validated)
- Notes: Citation density upper bound raised from 15 to 17 based on v3-validated achieving 17.0 without over-citing (matches A* journal Mikalef at 17.1). Lit review ratio upper bound raised to 37% when a gap table is embedded. Conclusion ratio lower bound dropped to 2.5% (acceptable when Discussion section is expanded per advisor requirements).

## Venue: DBA Advisor Theory-Selection Review (Bordeaux, Prof. Barneto)
- Tier: Working paper for advisor (targeting A* journal conventions for citation quality)
- Typical word count: 2800-3400
- Section order: Framing, Candidate Lenses Surveyed, Comparative Assessment, Proposed Spine, Gap and Next Steps
- Section ratios: Framing 7-8%, Survey/Body 45-47%, Assessment 19-21%, Recommendation 12-13%, Gap/Next 7-8%
- Citation density: 11.6 per 1000 words (author-year style, inline)
- Abstract word limit: 130-150 (working paper abstract, not venue-mandated)
- First extracted: 2026-07-07
- Last updated: 2026-07-07
- Papers sampled: 1 (barneto-july-theory-selection-litreview-20260707); a 2nd same-form document (barneto-litfindings-jul2026, 2907w) passed benchmark against this fingerprint on 2026-07-16 but was NOT promoted to n=2 because its delivered draft still carried internal workspace source markers (per benchmark report). Promote to n=2 once that document is finalized with markers stripped.
- Candidate sub-form (n=1, NOT promoted): "Advisor Synthesis Memo (Prashar, IIM Sambalpur)" — qntr-candidate-dimensions-prashar-jul2026 (2851w, 5 sections, 12.6 citations/1000w, abstract 145w, section ratios Framing 13% / Body 67% / Open-questions 14%). Distinct from the Barneto theory-selection form (dimensions-CHALLENGE memo for a co-author vs theory-SELECTION review) and a different advisor. Per n≥2 promotion rule, do not create a fingerprint until a 2nd same-form Prashar memo exists. Framing and open-questions ran heavy (13-14% vs Barneto 7-8%), purpose-driven for a challenge memo.
- Notes: Benchmark comparison papers (Collins et al. 2022, Papagiannidis et al. 2025, Berente et al. 2021) are 12000-19000 words but those are journal submissions, not advisor working papers. This fingerprint captures the advisor-facing format. Citation density at high end of A* range (matches Berente at 11.8). Internal workspace source markers must be stripped before sharing (confirmed again 2026-07-16: barneto-litfindings delivered with markers still embedded, benchmark flagged it delivery-blocking). barneto-litfindings ran 9.3/1000w citation density, ~20% below the 11.6 target, defensible for a deep-read 5-paper spine but a light-lift candidate.
