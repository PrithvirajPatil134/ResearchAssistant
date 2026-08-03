# Literature Findings: Punctuated Equilibrium and Generative AI Restructuring

*Interim findings memo for Prof. Pascal Barneto, July 2026.*

## Abstract

Technology firms restructured between 2022 and 2026 at a scale the sector had not previously recorded, and they cited generative AI while doing so. Whether that restructuring follows the sequence punctuated equilibrium predicts remains open, and the literature has not yet applied the theory's coding rules to the generative AI transition. This memo surveys the groundwork for that test. Three linked findings hold. Firm AI adoption intensity is measurable and non-circular through a continuous AI Share built from job postings (Alekseeva et al., 2026). Reorientation separates from convergence using Girod and Whittington's (2015) interview-validated 0.30 structural change ratio. Organizational structure is recoverable from 10-K and DEF 14A filings at 98.1% accuracy (Albert, Eklund, & Tang, 2026). Together they form one archival test: aggressive adopters should cross the reorientation threshold while incremental adopters stay in convergence, with disruption theory supplying the trigger.

## 1. Research Question and Sub-Questions

Between November 2022 and mid-2026, major technology firms restructured at a scale the sector had not recorded before, and they did so while citing generative AI in their restructuring communications [data/drafts/dba-topic-proposal-org-restructuring-genai.md, §1]. That coincidence frames what this study asks. The question is about organizational form, not adoption rates: what happens to the deep structure of a firm when the generative AI jolt lands, and whether the change follows the sequence punctuated equilibrium predicts.

The primary research question is:

> How do organizational restructuring patterns differ between technology firms pursuing aggressive generative AI integration and those adopting an incremental approach, and to what extent do these patterns align with the predictions of punctuated equilibrium theory? [syntheses/dba-thesis-proposal-2026.md, "Current Research Direction"]

Three sub-questions sit inside it:

- Which structural elements (management layers, role categories, divisional boundaries, reporting relationships) changed across the sampled firms between 2022 and 2027? [data/drafts/dba-topic-proposal-org-restructuring-genai.md, §2, RQ1a]
- Do the sampled firms converge toward a common organizational form, or diverge into distinct structural archetypes? [data/drafts/dba-topic-proposal-org-restructuring-genai.md, §2, RQ1b]
- Do aggressive adopters cross into reorientation, showing concurrent multi-domain structural change, while incremental adopters stay in convergence, as punctuated equilibrium would expect? [syntheses/dba-thesis-proposal-2026.md, "Testable expectation"; data/drafts/dba-topic-proposal-org-restructuring-genai.md, §2, RQ1c]

This wording keeps the study to one specific question with sub-questions nested inside it, the shape Barneto asked for on 2026-06-17, and situates it in the observed 2022-2026 technology restructuring wave rather than treating AI uptake as the outcome of interest [entities/prof-barneto.md, "First Supervision Meeting (2026-06-17)"].

## 2. Theoretical Framework

The study anchors on punctuated equilibrium and reads disruption theory as the complementary lens. The split of labour is deliberate. Punctuated equilibrium models what changes inside a firm and carries archival coding precedent; disruption theory names why the generative AI jolt forces the response in the first place. The anchoring choice originates in the user's own proposal, and the instruction to name a framework explicitly came from Barneto on 2026-06-17 [data/drafts/dba-topic-proposal-org-restructuring-genai.md, §3.1; entities/prof-barneto.md, "First Supervision Meeting (2026-06-17)"].

### 2.1 Punctuated equilibrium as the anchor

Tushman and Romanelli (1985) hold that organizations move through long convergent periods of incremental change that preserves the deep structure, broken by brief reorientation episodes in which strategy, structure, power, and control systems shift together [data/drafts/dba-topic-proposal-org-restructuring-genai.md, §3.1]. Romanelli and Tushman (1994) took that model to archival data and set the canonical coding rule: substantial change in two or more domains within a compressed window counts as reorientation [abstract-level; full text pending] [data/summaries/lit-search-thesis-foundations-v2.md, §2]. Gersick (1991) fixes the object of that change as deep structure, so a revolution means the deep structure is dismantled, not merely resurfaced [abstract-level; full text pending] [data/summaries/lit-search-thesis-foundations-v2.md, §2].

What the theory contributes is a testable structural mechanism and, more usefully, a way to measure it from disclosure. Girod and Whittington (2015), read in full, coded organizational titles to four hierarchical levels, computed a continuous structural change ratio, and validated a 0.30 threshold above which a firm-year reads as discontinuous restructuring [data/summaries/lit-search-thesis-foundations-v2.md, §2]. That turns the theory into a coding rule the study can apply, not a metaphor it can only gesture at.

### 2.2 Disruption theory as the complementary lens, and what the study tests

Punctuated equilibrium is thin on why this particular jolt lands now, and that is the gap disruption theory fills. Barneto named the theory of disruption as an example of the kind of framework the thesis should identify [entities/prof-barneto.md, "First Supervision Meeting (2026-06-17)"]. In this design it supplies the trigger mechanism: the reason the generative AI shift destabilizes the prior equilibrium and forces a response, aligning with the environmental-jolt concept (Meyer, 1982) that lets an external shock be theorized as the punctuation trigger [abstract-level; full text pending] [data/summaries/lit-search-thesis-foundations-v2.md, §2, §4]. [UNSOURCED: Christensen 1997 disruption book is not in the wiki; only the concept Barneto named is used here.]

The study therefore deduces a directional expectation rather than a loose association, which is what Sutton and Staw (1995) demand of theory: an account of why, not merely a description of what [data/wiki/shared/concepts/what-theory-is-not.md]. It tests whether firms crossing higher AI adoption intensity show reorientation-pattern change, several domains moving within a compressed window or a structural change ratio above threshold, while incremental adopters stay in convergence [data/summaries/lit-search-thesis-foundations-v2.md, §4; syntheses/dba-thesis-proposal-2026.md, "Testable expectation"].

## 3. Literature Survey: Three Foundations

The measurement chain this thesis needs has three links: a way to grade firms by how hard they are adopting AI (the independent variable), a rule for deciding when the resulting organizational change is a reorientation rather than routine adjustment (the dependent-variable coding), and evidence that both can be read off public corporate disclosure rather than collected by hand. I survey each link the way Barneto asked: what the literature settles, what it leaves open, and how punctuated equilibrium can be tested against the gap. Where a paper was read only at abstract level, I say so; confidence should not run past the evidence.

### 3.1 Foundation 1: Classifying firms by AI adoption intensity (the IV)

**What we know.** Adoption intensity can be measured continuously from public data, and the top strategy journals accept it. Alekseeva, Azar, Giné and Samila (2026) build a firm-year "AI Share," the proportion of a firm's job postings that are AI-related, from Lightcast vacancy data matched to Compustat by name and a Bing-API URL-overlap algorithm. Their sample runs to 823 firms and 9,876 firm-years over 2010 to 2022, with firm and industry-year fixed effects and a shift-share instrument whose first-stage F-statistic is 89.8 [data/drafts/_staging/extract-alekseeva-results.md §1, §2, §4, §7]. McElheran et al. (2024) give the survey-based alternative: a binary "Use AI" indicator plus a four-level intensity scale (testing, under 5%, 5 to 25%, over 25% of production), drawn from the 2018 Annual Business Survey covering roughly 447,000 firms [data/summaries/thesis-fulltext-extractions.md §1]. Both keep the IV as a labor or spending input, which is what makes it non-circular with a structural DV. Two older A* anchors sit alongside them: Zahra and Covin's (1993) technology-posture classification (leader versus follower) and Mithas and Rust's (2016) IT-spending-to-revenue ratio [abstract-level; full text pending] [data/summaries/thesis-fulltext-extractions.md §1].

**What we do not know.** No validated intensity scale specific to generative or agentic AI yet exists. Alekseeva et al. measure predictive, pre-generative AI, and the authors themselves flag that generative and agentic systems "redistribute cognitive complexity across organizational roles in qualitatively different ways" [data/drafts/_staging/extract-alekseeva-results.md §8]. So the measure is precedent for the method, not a ready instrument for the thesis window.

**How the theory can be tested.** AI Share, or a disclosed-AI-intensity measure built the same way from job postings and 10-K language, becomes the environmental-jolt proxy in punctuated equilibrium terms. Firms crossing into the high end of the adoption-intensity distribution are the candidate reorientation cases; incremental adopters are the expected convergence cases. The comparison the thesis makes (aggressive versus incremental adopters) maps directly onto that split [data/summaries/lit-search-thesis-foundations-v2.md §4]. The continuity of the measure matters here. Because AI Share runs on a scale rather than a yes-or-no flag (mean 0.5%, rising from below 0.1% to roughly 1% across the sample), it can locate where each firm sits along an adoption gradient rather than forcing a binary that would flatten the very variation the theory predicts should matter [data/drafts/_staging/extract-alekseeva-results.md §1, §3].

### 3.2 Foundation 2: Operationalizing punctuated equilibrium in archival data (the DV coding)

**What we know.** Reorientation can be told apart from convergence with a quantitative cutoff. Girod and Whittington (2015) compute a structural change ratio in three steps: for each firm-year they take the proportion of top-management titles in each horizontal category and vertical level, difference those proportions against the prior year in absolute value, and sum the differences; the ratio ranges from 0 to 0.97, and a firm-year above 0.30 is coded as restructuring [data/summaries/thesis-fulltext-extractions.md §2]. That 0.30 cutoff is not arbitrary. They validated it by interviewing fourteen executives at twelve firms, who confirmed changes above 0.30 as genuine restructurings while treating lower values as ambivalent [data/summaries/thesis-fulltext-extractions.md §2]. The coding runs on annual-report and SEC 10-K data. The canonical scheme upstream of it is Romanelli and Tushman's (1994) multi-domain simultaneity: substantial change in two or more domains within a compressed window counts as reorientation [abstract-level; full text pending] [data/summaries/lit-search-thesis-foundations-v2.md §2]. Table 2 sets the main coding approaches side by side.

**Table 2. Punctuated equilibrium coding approaches compared.**

| Approach | Scale | Best for | Canonical paper | Evidence status |
|---|---|---|---|---|
| Multi-domain simultaneity | binary per domain | large-N archival | Romanelli & Tushman (1994) | [abstract-level; full text pending] |
| Proportion-based structural | continuous | large-N archival databases | Girod & Whittington (2015) | [FULL] |
| Strategy-plus coupling | binary | large-N archival | Lant et al. (1992) | [abstract-level; full text pending] |
| Archetype transition | categorical | small-N longitudinal | Greenwood & Hinings (1996) | [abstract-level; full text pending] |
| Deep structure disruption | binary | small-N longitudinal | Silva & Hirschheim (2007) | [abstract-level; full text pending] |

*Source: [data/summaries/lit-search-thesis-foundations-v2.md §2].*

**What we do not know.** The multi-domain coding I would lean on most is not fully in hand. Romanelli and Tushman's strategy and power coding rules are behind a paywall, so the domain definitions I would replicate are read only at abstract level [data/summaries/thesis-fulltext-extractions.md §2]. And the threshold problem is real: outside Girod and Whittington's 0.30, most punctuated-equilibrium work treats "substantial change" qualitatively, and the literature remains limited on applying any of these cutoffs to a generative-AI transition [data/summaries/lit-search-thesis-foundations-v2.md §6].

**How the theory can be tested.** A firm-year is coded reorientation when the structural change ratio exceeds the 0.30 threshold, or when two or more organizational domains shift inside a compressed window. Convergence years are everything below that. This turns punctuated equilibrium from a metaphor into a rule that can be applied to disclosure data year by year.

### 3.3 Foundation 3: Measuring organizational structure from corporate disclosure (data-source validity)

**What we know.** Structure is recoverable from public filings at high accuracy. Albert, Eklund and Tang (2026) code top-management-team composition from 10-K, 20-F and DEF 14A filings into six role groups (CEO, CXO, primary value chain, support, business unit, board affiliation) and twelve hierarchical levels, using a fine-tuned GPT-4o model that reached 98.1% accuracy on a held-out sample. Their database spans 521 firms and 161,028 executive-firm-years from 1993 to 2020, is free and publicly available, and yields a TMT Hierarchy count (0 to 6) plus proportional role measures [data/drafts/_staging/extract-albert-results.md §1, §2, §4, §5, §6]. They show the method catching real reorganizations: Hewlett Packard's swing between functional and divisional structure across 1999 to 2008, tracked through the shifting proportion of business-unit versus functional roles [data/drafts/_staging/extract-albert-results.md §8.2]. Larcker, Richardson and Tuna (2007) offer the governance-index template, reducing 39 proxy-statement governance variables through oblique principal component analysis to 14 dimensions that hold 61.7% of the variance across 2,106 firms [SSRN working-paper version; verify against published Accounting Review article] [data/drafts/_staging/extract-larcker-results.md §1, §2, §3]. Beyond filings, earnings-call transcripts (DesJardine & Bansal 2019) and WARN Act layoff notices have been validated as organizational-data sources [abstract-level; full text pending] [data/summaries/lit-search-thesis-foundations-v2.md §3].

**What we do not know.** Albert et al. cover 1993 to 2020 and, by their own account, do not code punctuated versus incremental change; a researcher applying the theory must set the punctuation threshold on their TMT-composition data [data/drafts/_staging/extract-albert-results.md §8.4]. More broadly, existing peer-reviewed work has not yet applied these archival structure methods specifically to AI-driven restructuring [data/summaries/lit-search-thesis-foundations-v2.md §6].

**How the theory can be tested.** The Albert et al. taxonomy supplies the raw structural signal (role proportions and hierarchical levels per firm-year) directly from 10-K and DEF 14A filings; the Girod and Whittington cutoff from Foundation 2 turns that signal into a convergence-or-reorientation code. Public headcount and earnings-call disclosures add corroborating evidence. Read together, the three foundations form one archival test: an adoption-intensity input, a punctuated-equilibrium coding rule, and a disclosure-based structural measure, each with A*/A precedent, and each connected to the next.

## 4. Spine Papers

Barneto asked for a short list of spine papers: the anchors that hold the design together, each with a one-line statement of what it fixes. Five papers do that work. Together they cover the theory coding, the independent variable, the dependent-variable measure, and the archival data source, and four of the five are read in full.

**Table 1. Spine papers and what each fixes.**

| Paper | Role in design | What it fixes | Evidence |
|---|---|---|---|
| Romanelli & Tushman (1994), AMJ, A* | Punctuated equilibrium canonical coding | The reorientation-versus-convergence rule: substantial change in two or more domains within a compressed window counts as reorientation | [abstract-level; full text pending] |
| Girod & Whittington (2015), Org. Science, A* | Continuous PE coding | The quantitative punctuation cutoff: a structural change ratio above 0.30, interview-validated, applied to annual-report and 10-K data | [FULL] |
| Albert, Eklund & Tang (2026), SMJ, A* | Organizational-structure database | How the structural DV is read from 10-K, 20-F and DEF 14A filings: six role groups by twelve hierarchical levels, at 98.1% accuracy | [FULL] |
| Alekseeva, Azar, Giné & Samila (2026), SMJ, A* | AI adoption measure | The firm-level adoption-intensity IV: a continuous AI Share built from job postings matched to Compustat | [FULL] |
| McElheran et al. (2024), JEMS, A | AI adoption measurement | The survey-based alternative intensity scale and the industry benchmarks against which a disclosure measure can be checked | [FULL] |

*Sources: [data/summaries/lit-search-thesis-foundations-v2.md §2]; [data/summaries/thesis-fulltext-extractions.md §1, §2]; [data/drafts/_staging/extract-albert-results.md §1, §6]; [data/drafts/_staging/extract-alekseeva-results.md §1].*

Two of these carry the design more than the rest. Girod and Whittington supply the one thing punctuated-equilibrium research usually lacks, a defensible numeric threshold, and Albert, Eklund and Tang supply the free, filing-derived structure database that makes a fully archival study feasible at scale. Alekseeva et al. anchor the input side, and McElheran et al. give an independent benchmark for it. Romanelli and Tushman remain the conceptual reference for what a reorientation is, though the coding specifics stay abstract-level until the full text is in hand.

## 5. How the Theory Will Be Tested

The three foundations join into a single archival test. The chain runs from input to mechanism to form: AI adoption intensity supplies the independent variable, punctuated equilibrium supplies the coding rule, and top management team composition read from filings supplies the dependent variable. This measurement-chain synthesis is set out in lit-search-thesis-foundations-v2.md §4; I adopt it here as the design's backbone.

The independent variable stands in for the environmental jolt. Following Alekseeva et al. (2026), the study reads a continuous AI Share for each firm-year from job postings matched to Compustat, a measure that captures how intensively a firm is hiring toward AI while saying nothing about its organizational form. [extract-alekseeva-results.md §1] Where posting data is thin, McElheran et al.'s (2024) four-level intensity scale offers a survey-anchored alternative. [thesis-fulltext-extractions.md §1]

The dependent variable is coded by the punctuated equilibrium rule. A firm-year counts as reorientation when its structural change ratio clears the 0.30 threshold Girod and Whittington (2015) validated on annual-report data, or when substantial change appears in two or more organizational domains within a compressed window, the multi-domain simultaneity criterion (Romanelli & Tushman, 1994 [abstract-level; full text pending]). [thesis-fulltext-extractions.md §2] Structure itself is recovered from 10-K and DEF 14A filings using the role-group and hierarchical-level coding Albert, Eklund and Tang (2026) demonstrate at 98.1% accuracy. [extract-albert-results.md §1-6]

The testable expectation then follows directly, and it is the expectation the proposal and the Cardoso correspondence set out: aggressive adopters, those with high AI Share, should cross the reorientation threshold, while incremental adopters should remain in convergence. [syntheses/dba-thesis-proposal-2026.md; data/drafts/dba-topic-proposal-org-restructuring-genai.md §4] Disruption theory carries the trigger side of the claim, explaining why the generative-AI jolt forces a response at all.

One discipline keeps the test honest. Non-circularity holds because the independent variable measures spending and hiring while the dependent variable measures organizational form; neither embeds the other. That is why Venkatraman transformation levels are excluded as a classifier: their higher stages already imply structural change. [lit-search-thesis-foundations-v2.md §4]

The open gaps are real, and they belong to the thesis rather than to the literature. No validated agentic-AI intensity scale yet exists, so Alekseeva's pre-generative AI Share is a proxy the study must defend. [extract-alekseeva-results.md §8] The Romanelli and Tushman strategy-and-power coding scheme is still unread [abstract-level; full text pending], and the punctuation threshold on TMT-composition data is researcher-set, not inherited. [extract-albert-results.md §8.4] These are the design choices the December document will have to earn.

## References

[Compiled mechanically from the works cited above. Not produced at the stitching stage.]
