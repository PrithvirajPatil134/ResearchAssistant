# Case Study Publication Methodology

**Purpose.** This file is the self-contained reference for writing a publication-ready business case study in the CW space. It captures the end-to-end process we followed to produce *SAI TEX LTD.: A Red Queen's Race in Ichhalkaranji* (v8c, approved by Prof. Kakoli Sen for journal submission), and it converts every piece of feedback we received across v5 through v8c into a proactive checklist so future drafts clear the same bar without depending on reviewer feedback to surface the gaps.

**How to use this file.** Read the whole document once before starting a new case. Then use Section 8 as a live self-review rubric during drafting, and Section 9 as the pre-submission gate. When Section 8 and Section 9 are both clean, the draft is ready for the professor. Section 10 is the Sai Tex feedback cycle, kept as a worked example so the abstract rules have concrete anchors.

---

## 0. Scope and Principles

A case study in this workspace is:
- A **third-person, past-tense narrative** of a real protagonist facing a real dilemma.
- Written for students, not instructors; the teaching note is where frameworks are named.
- **Dilemma-focused, not solution-focused.** The protagonist must be left at a decision point with genuine ambiguity.
- Grounded in consented primary data (interviews, company documents) plus verifiable public sources. If consent is not yet secured, the case is built from secondary sources only.
- Less than five years old in its core events (publishers define relevance by recency).
- Between 4,000 and 5,500 narrative words with 3 to 7 exhibits, targeting 8 to 12 total pages.

Five principles govern every decision:

1. **Protagonist first, framework later.** Every sentence in the case serves the protagonist's situation. Frameworks live in the teaching note.
2. **Show, don't tell.** Numbers without adjectives. Quotes sparingly. Let the data escalate the tension.
3. **No right answer.** At least two paths must be defensible with the evidence in the case.
4. **Consent and verifiability.** Every factual claim traces to an interview note, a company document, or a cited public source.
5. **The bar is the published benchmark.** Compare each section against real Ivey or comparable published cases, not against a generic sense of "good writing."

---

## 1. The End-to-End Methodology

This is the process we actually followed to reach v8c. The time budgets are approximate and assume one protagonist with moderate data access.

### Phase 1. Pattern Extraction (before writing anything)

**Goal.** Understand what "publishable" looks like before trying to produce it.

1. Read `src/research_assistant/spaces/CW/knowledge/Publication_Playbook_v4.md`. This file was built from 14 Ivey, Harvard, and SMU published cases (C2 through C15). It documents opening-hook conventions, section-heading taxonomy, narrative arc, exhibit patterns, voice rules, tension levers, variations, and a weighted publication checklist. Treat it as the structural source of truth.
2. Read `src/research_assistant/spaces/CW/knowledge/Prof Kakoli Sen_ClassNotes.docx`. The instructor's notes establish non-negotiable principles: focus on dilemma not solution, consent before publishing, recency under five years, the case answers the five Ws, publisher-specific guidelines.
3. If a new patterns file is being built, also skim the published cases under `src/research_assistant/spaces/CW/knowledge/Case_Studies_Session*` to confirm the playbook still reflects the current sample.

### Phase 2. Scope the Dilemma

**Goal.** Before collecting data, lock down what the case is actually about.

1. Open `src/research_assistant/spaces/CW/knowledge/Case_Idea_Template__DBA Immersion_20251103.docx` and fill out all ten fields:
   - Proposed title
   - Organization / industry context
   - Key issue / decision dilemma (the central question the protagonist faces)
   - Background summary (max 100 words)
   - What makes it teachable (subject area, framework, theory)
   - Potential data sources (interviews, documents, reports, public sources)
   - Accessibility and permissions
   - Tentative learning objectives (2 to 3 points)
   - Keywords (3 to 5)
   - Notes for faculty comment
2. The dilemma statement in field 3 must be a single sentence in the form *"Should [protagonist] do X, Y, or Z?"* with at least two genuinely defensible options. If you cannot complete that sentence, stop and refine the case idea; the rest of the process will not save a weak dilemma.
3. Save a condensed version of the case idea in `src/research_assistant/spaces/CW/knowledge/Case_Idea_Condensed_<SiteName>.md` so the scope is retrievable by the guide workflow.

### Phase 3. First Draft via the Guide Workflow

**Goal.** Produce a complete rough draft using the package's guided workflow, not freeform generation.

1. Run the guide workflow for the case study in the CW space. The workflow breaks drafting into discrete, cache-able steps. For the Sai Tex teaching note, the step sequence was:
   - Step 1: Teaching note craft analysis (or case craft analysis for a case study)
   - Step 2: Benchmark teaching note / case analysis
   - Step 3: Read the relevant template
   - Step 4: Ingest the underlying case study data
   - Step 5: Write the teaching note / case
   - Each step is cached under `src/research_assistant/spaces/CW/cache/guide_<timestamp>/`
2. For a case study, the step sequence is analogous: craft analysis → benchmark case analysis → template review → source-data ingest → draft.
3. Review the guide workflow example `src/research_assistant/spaces/CW/cache/guide_20260404_172752/` to understand the expected depth of each step before running a new workflow.
4. Do not skip steps. Each earlier step grounds the later ones. A draft written without a proper Phase 1 and Phase 2 will require far more iteration.

### Phase 4. Gap Analysis Against Benchmarks

**Goal.** Compare the first draft against published cases section by section.

1. Pick two or three published benchmark cases that match the new case on industry, company size, and dilemma type. For Sai Tex, the closest benchmarks were C4 (Vinder Oils, family-owned oil manufacturer) and C7 (Jaipur Rugs, social-mission MSME).
2. For each of the seven canonical sections (Opening Vignette, Company Background, Industry Context, Problem Escalation, Options / Way Forward, Decision Point, Exhibits), compare the draft against the benchmarks on:
   - Does the draft open with a specific date plus full protagonist name, title, and company in the first narrative sentence?
   - Is the dilemma foreshadowed in paragraph 1?
   - Are there 5 to 9 section headings, ALL CAPS for Ivey or title case for SMU / Harvard?
   - Is the voice third-person past tense throughout, with present tense only for industry facts?
   - Are frameworks named in the text (they should not be)?
   - Are numbers given without adjectives?
   - Are quotes sparing (1 to 3) and always attributed?
   - Do exhibits sit after the narrative, with source attribution and in-text `(see Exhibit N)` references?
3. Record each gap as an explicit revision task. Do not start editing until the full gap list is captured.

### Phase 5. Targeted Data Collection

**Goal.** Ask the protagonist only the questions that close the gaps found in Phase 4.

1. Convert the gap list into an interview question list. For Sai Tex, gaps in financial detail drove questions about the personal ledger, monthly P&L, energy cost per unit, interest rate, and job-work rate history. Gaps in dilemma texture drove questions about the bank's collateral demand, the wife's position, the manager Shivmani's tenure, and the father's exact words.
2. Cross-reference the interview questions against the existing data already captured (in our case, `AKP Responses for Sai Tex Ltd.md` and the supporting spreadsheet). Only ask what is genuinely missing.
3. Record every new answer in a single dated interview transcript file. This becomes the citation source for endnotes.
4. Collect corroborating documents (ledgers, bank letters, notices) and add them to `src/research_assistant/spaces/CW/knowledge/`.

### Phase 6. Stitching and Iteration

**Goal.** Produce a draft that reads as one continuous narrative, not a patchwork of sections.

1. Stitch the revised sections in sequence: vignette, company background, industry context, problem escalation, options, decision point, exhibits, endnotes.
2. Read the full draft aloud or end to end in one sitting. Flag any transition that feels abrupt, any section that loses the protagonist's voice, any fact that appears twice, and any quote that sits in a paragraph it does not belong in.
3. Run the human-authored writing check. See Section 7 for the automated hooks that enforce this.
4. Save drafts with an incrementing version number in `src/research_assistant/spaces/CW/workspace/Case_Study_v<N>_<descriptor>.md`. Each round of feedback triggers a new version.

### Phase 7. Publication Production

**Goal.** Produce the `.docx` that goes to the professor and, ultimately, the journal.

1. Use a styled `.docx` template matching the target publisher's conventions (ALL CAPS headings, `Heading 1` for title, `Heading 2` for sections, `First Paragraph` for first paragraph of each section, `Body Text` for the rest, `Normal` for exhibit bodies and notes, footnotes for endnotes).
2. Build the docx programmatically so the styling is reproducible across versions. See the build scripts used for v8a, v8b, and v8c as templates.
3. Place the author disclaimer at the top (authors, institution, case-writing attribution, copyright notice, reproduction restrictions, copyright year).
4. Verify: section headings match the markdown, tables render correctly, footnotes reference the right endnote numbers, and superscript numerals in the body align with the footnote IDs.
5. Save the final file as `src/research_assistant/spaces/CW/output/<PUBLISHER>_<CASE_NAME>_Case_Study_v<N>.docx`.

---

## 2. Opening Vignette Standards

**The dominant formula (12 of 14 benchmark cases).**

> [Date or specific moment] + [Full name, title, company] + [Emotional or observational verb] + [Dilemma in one sentence]

**Requirements.**

- The first narrative sentence must contain the protagonist's full name, their title, and the company name. No exceptions.
- The dilemma must be foreshadowed in paragraph 1, even if the full options are not revealed until the final section.
- Use a sensory moment (a phone buzz, a letter on the desk, a silent factory floor) or a time-anchored declaration ("In August 2024, ..."). The two can be combined.
- Emotional verbs observed in the benchmark: *pondered, wondered, stared, could not decide, exclaimed, lay sleepless, sat assessing, was tasked with, stood*.
- Optional: an epigraph before the narrative. Three of 14 benchmark cases use one.

**Sai Tex v8c opening (for reference).**

> "On a humid night in March 2026, Avinash Kisanrao Patil, founder and sole proprietor of Sai Tex Ltd., stood on the factory floor of his unit in the Pride Co-operative Textile Park in Ichhalkaranji, Maharashtra. Five of his ten Rifa Electronic Rapier looms clattered through their cycles at 300 revolutions per minute. The other five stood dark and still, their reed frames gathering lint. A year ago, all ten had run through the night. Now, half the floor was silent."

This opening combines a time-anchor ("On a humid night in March 2026"), full protagonist designation, a sensory moment (clattering machines, silence), and foreshadows the capacity dilemma (half the floor silent).

---

## 3. Section Architecture

Target 5 to 9 sections, each serving a distinct narrative function.

| # | Section | Purpose | Length | Required |
|---|---------|---------|--------|----------|
| 1 | Untitled Opening Vignette | Hook plus protagonist plus dilemma foreshadow | 1 to 2 pp | Yes |
| 2 | Industry or Market Context | Market size, trends, competitive forces | 1 to 2 pp | Yes (13 of 14) |
| 3 | Company Background | Founding story, growth arc, protagonist's role | 1 to 2 pp | Yes |
| 4 | Problem Escalation | Crisis with supporting data, escalation | 1 to 2 pp | Yes |
| 5 | Stakeholder Perspectives or Business Model Shift | Alternative framings, 2 to 4 implicit views | 0.5 to 1 pp | Often |
| 6 | Three Paths Forward (or similar) | 2 to 4 explicit options with trade-offs | 1 to 1.5 pp | Yes |
| 7 | Decision Point | Protagonist at the decision; no answer given | 0.5 to 1 pp | Yes |
| 8 | Exhibits | Data appendix after narrative | 2 to 5 pp | Yes |

**Heading conventions.**
- Ivey cases: ALL CAPS section headings.
- SMU and Harvard: title case.
- Pick the convention of your target publisher and hold it across every heading.

**Ordering principle.** Industry context before company background works better when the cluster or industry is itself the protagonist's constraint (Sai Tex, because the Ichhalkaranji cluster's technology stagnation is half the dilemma). Company background before industry context works when the protagonist's history is the distinguishing element (Vinder Oils, where the family legacy is the tension).

---

## 4. Voice and Tone Rules

| Dimension | Rule |
|-----------|------|
| Point of view | Third-person omniscient throughout |
| Tense | Past tense for protagonist actions, present tense only for industry facts ("The cluster houses over 50,000 powerlooms.") |
| Tone | Journalistic, neutral; never advocates for any option |
| Quotes | Direct quotes used 1 to 3 times total, always attributed; italicized in endnotes when quoted verbatim |
| Numbers | Factual, no adjectives ("increased 61%" not "an impressive 61%") |
| Theory | Embedded in the situation, never named in the case text (the teaching note names the framework) |
| Adverbs | Avoid; let the facts carry weight |
| Protagonist feelings | Signaled by action ("closed the message", "stared at the phone") not by declaration ("he was anxious") |

**Academic tone.** The case is narrative but not conversational. Phrases like "here is the problem," "the cycle feeds itself," "the takeaway," "works like this" do not belong in a published case. When in doubt, rewrite for a third-person omniscient narrator describing events to a reader who has no prior context.

---

## 5. Exhibits

**Volume and type.** Median benchmark: 5 exhibits. Heavy cases carry 7 to 13 when the data drives the analysis. Light cases carry 1 to 2 when the narrative carries it.

**Type frequency (from 14-case benchmark).**
- Financial data tables: 10 of 14
- Market or industry data: 7 of 14
- Comparison tables (competitor or option): 5 of 14
- Process or framework diagrams: 5 of 14
- Organizational charts: 4 of 14
- Timeline or milestone tables: 3 of 14

**Non-negotiable rules.**
- Exhibits come after the narrative, never inline.
- Numbered sequentially (Exhibit 1, Exhibit 2, ...).
- Titled in ALL CAPS or title case per publisher convention.
- Source attribution under every exhibit. Format: *"Source: AKP Sai Tex Ltd. Stats.xlsx, 'Financial Performance Stats' sheet. Compiled from protagonist's personal ledger and interview responses (October 2025 to April 2026)."*
- In-text `(see Exhibit N)` references, minimum 3 across the narrative.
- First financial exhibit referenced within the first three narrative pages.
- No fabricated data; every exhibit traces to a company document, interview note, or public source.
- A footnote under exhibits with computed or derived values, explaining the computation.

**Sai Tex v8c exhibit plan (for reference).**
- Exhibit 1: Financial deterioration 2023 vs 2025 (P&L summary, unit-level cost escalation, revenue compression). Three panels included
- Exhibit 2: 2025 monthly production, cost, and sales data. Thirteen rows
- Exhibit 3: Strategic options comparison (three options across five dimensions)
- Exhibit 4: Technology comparison (Rifa Rapier vs Air-Jet across nine parameters)

---

## 6. Endnotes and Source Attribution

**Every factual claim, quote, and data point in the narrative requires an endnote.** Endnotes sit at the bottom of the document in a "Endnotes" or "Notes" section, with superscript numerals in the body.

**Endnote format.**

1. **Attribution footnote for interviews (first use only).** A single blanket attribution is enough: *"Based on interviews with <Protagonist Name> (<INITIALS>), founder of <Company>, conducted between <Start> and <End>. All statements attributed to <Name> in subsequent footnotes derive from these interviews unless otherwise noted."*
2. **Subsequent interview-derived endnotes.** Drop the "AKP interview" prefix. Use the protagonist's name and put direct quotes in italics: *"Patil: \"Power loom industry began in 1904 in Ichalkaranji in Maharashtra.\""*
3. **Document-derived endnotes.** Cite the document and sheet or page: *"AKP Sai Tex Ltd. Stats.xlsx, 'Financial Performance Stats' sheet: 2023 Total Sale INR 675,000..."*
4. **Public-source endnotes.** Full citation including URL if applicable.
5. **Conceptual endnotes (e.g., defining the Red Queen Effect).** Cite the originating academic source: *"See Barnett, W.P. and Hansen, M.T. (1996), 'The Red Queen in Organizational Evolution,' Strategic Management Journal, 17(S1), pp. 139–157."*
6. **Currency footnote.** On the first dollar figure, a note defining the exchange rate: *"US$1 ≈ INR 92 (March 2026). All subsequent dollar figures use this exchange rate."*

**Avoid.** Repeating the same attribution prefix across 20 endnotes (we learned this the hard way on v8a; the consolidation pattern is in v8c).

---

## 7. Writing Style Guardrails (Automated)

Two hooks in `.kiro/hooks/` enforce the writing style automatically on every save and every agent write:

- `check-submission-writing.kiro.hook` triggers on file save for any `workspace/`, `output/`, `assignment/`, or `literature review/` markdown file with a submission-signal filename (Submission, Paper, Teaching, Case, revised).
- `check-agent-writing.kiro.hook` triggers after any agent write tool call (fsWrite, strReplace, fsAppend) on the same path patterns.

**Both hooks check for:**

1. **Banned words.** The full list is maintained in `.kiro/steering/human-authored-writing.md` and the two hook files. It includes common AI-generated vocabulary (roughly 30 terms). Rather than repeat them here, refer to those files when scanning a draft.
2. **Banned phrases and sentence openers.** Furthermore, Moreover, Additionally, Consequently, Subsequently, Nevertheless, In conclusion, To sum up.
3. **Uniform sentence rhythm.** Five or more consecutive sentences within five words of each other in length.
4. **Narrator voice.** "Students should identify..." instead of "The analysis shows..."
5. **Announcing structure patterns.** "This section will discuss..."
6. **Em dashes.** Zero tolerance. The em dash character (U+2014) must not appear anywhere. Replace with periods, commas, colons, semicolons, or parentheses as the grammar requires.
7. **Academic tone.** Casual phrases like *works like this, here is the problem, the cycle feeds itself, the takeaway, that said, at the end of the day* must be rewritten. Prefer *the analysis demonstrates* over *this shows*, *it is evident that* over *clearly*, *the preceding analysis indicates* over *the takeaway*.

When writing a new case or teaching note, assume both hooks will fire on every edit. Clean prose in the first pass is cheaper than cleaning in the third.

---

## 8. Pre-Draft Self-Review Rubric

Run this before writing a single sentence of the narrative. If any answer is no, return to the earlier phase.

### Scope
- [ ] The case idea template has every field filled, including the one-sentence dilemma
- [ ] At least two options are defensible with the evidence available
- [ ] The protagonist has consented, or the case is being built from secondary sources only
- [ ] Core events are within the last five years
- [ ] The target publisher (Ivey, SMU, Emerald, etc.) has been identified and its guidelines reviewed

### Data readiness
- [ ] Financial data sufficient for at least one quantitative exhibit
- [ ] Industry data sufficient for at least one market-context exhibit
- [ ] At least three corroborating documents beyond interview transcripts
- [ ] Every planned fact, quote, and number has a traceable source

### Pedagogical design
- [ ] Minimum 3 stakeholders with conflicting interests
- [ ] Time pressure or urgency is established by a specific event or deadline
- [ ] Personal stakes for the protagonist are clear (career, family, livelihood)
- [ ] The dilemma genuinely splits informed readers; it is not a "right answer in disguise"

---

## 9. Pre-Submission Gate

Run this before sending the `.docx` to the professor or a publisher. Every item must pass.

### Structure
- [ ] Opens with specific date plus full protagonist name, title, and company in the first narrative sentence
- [ ] Dilemma foreshadowed in paragraph 1
- [ ] 5 to 9 section headings, consistent casing (ALL CAPS for Ivey, title case for SMU / Harvard)
- [ ] Narrative word count between 4,000 and 5,500, total pages between 8 and 12
- [ ] Ends with the protagonist at a decision point; no summary paragraph after the final question or scene (Sai Tex v8a failure: the draft had a summary paragraph after the bank manager's call. Fixed in v8b.)

### Voice
- [ ] Third-person past tense throughout; present tense only for industry facts
- [ ] No framework names in the case text (PESTEL, Porter, Red Queen, SEW, TOC all belong in the teaching note)
- [ ] No advocacy or editorializing
- [ ] 1 to 3 direct quotes, each attributed
- [ ] Numbers without adjectives

### Domain terms
- [ ] Every non-English or industry-specific term defined at first use. Sai Tex v8a failure: "paisa" was used without a gloss; fixed in v8b as *paisa (one hundredth of an Indian rupee)*.
- [ ] Foreign place names briefly contextualized if not globally known (e.g., "Bihar, a state in eastern India")

### Exhibits
- [ ] All exhibits after the narrative, never inline
- [ ] Numbered sequentially, titled in publisher casing
- [ ] Source attribution under every exhibit
- [ ] Minimum 3 in-text `(see Exhibit N)` references
- [ ] At least one financial table, one market or industry exhibit, one comparison or process exhibit

### Endnotes
- [ ] Single attribution footnote for interview data at first use; subsequent notes drop the prefix and italicize direct quotes (Sai Tex v8a failure: 20 notes began with "AKP interview:"; consolidated in v8b, preserved in v8c.)
- [ ] Currency footnote on the first dollar figure with exchange rate and date
- [ ] Every factual claim and number endnoted
- [ ] All endnotes sequentially numbered and matched by body superscripts

### Publication mechanics
- [ ] Author disclaimer at the top: authors, institution, case-writing attribution, reproduction restrictions, copyright year. (Sai Tex v8a failure: disclaimer was missing; added in v8b.)
- [ ] Standard publisher boilerplate: *"The authors do not intend to illustrate either effective or ineffective handling of a managerial situation."*
- [ ] File saved as `src/research_assistant/spaces/CW/output/<CASE_NAME>_Case_Study_v<N>.docx`
- [ ] Run of both writing hooks against the markdown precursor came back clean

### Writing hooks pass
- [ ] Zero em dashes anywhere
- [ ] Zero banned words or banned sentence openers
- [ ] No uniform sentence rhythm clusters
- [ ] No narrator voice
- [ ] No casual or conversational phrasing

---

## 10. Sai Tex Feedback Cycle: Worked Example

This section records what the professor flagged on each version and why each fix matters. Use it as a diagnostic when a new draft feels "almost right but not quite."

### v5 to v6 (early drafts)
- Narrative was too long, over 6,000 words.
- Industry context was thin; Ichhalkaranji cluster data was missing.
- Exhibits were in rupees only; dollar-conversion was inconsistent.

**Fix.** Trimmed 1,500 words of secondary industry commentary. Added Exhibit 2 (monthly production data). Standardized to US dollars with a single rupee-to-dollar footnote on first use.

### v7
- Feedback: "too verbose" and "tone needs to be academic."
- Some paragraphs were running 150 words; several used casual constructions.

**Fix.** Re-wrote long paragraphs as two or three shorter ones. Removed casual asides. Kept the narrative but tightened every sentence.

### v8a (first .docx for professor review)
Professor feedback, documented:

1. **Remove or reposition the closing summary paragraph.** The v8a draft ended with a paragraph that summarized Option A's assumptions and risks after the bank manager's question. That paragraph read like a teaching-note answer rather than a case ending. *Fix in v8b: deleted the paragraph entirely. The case now ends with the bank manager's question on the phone.*
2. **"Paisa" has no explanation.** The term appeared four times before any gloss. *Fix in v8b: added "(one hundredth of an Indian rupee)" at first use.*
3. **AKP interview appears too many times and reads as redundant.** 20 of 24 endnotes began with "AKP interview:". *Fix in v8b: consolidated into a single attribution footnote at endnote 1; subsequent notes drop the prefix and italicize direct quotes.*
4. **Author disclaimer needed at the top.** v8a had no disclaimer block. *Fix in v8b: added the standard five-paragraph disclaimer (authors, institution, case-writing attribution, reproduction restrictions, copyright year).*

### v8b to v8c
Minor polish. Footnote 22 was tightened to read "Patil: 'Wasn't aware MAHA-TUFS subsidy; until was made aware through this case study.'" and footnote 24 was rephrased to "We are inclining towards applying..." reflecting updated interview data. The disclaimer line was moved to list "Indian Institute of Management, Sambalpur" with a comma. No structural changes.

### Pattern across the cycle

Feedback mostly clustered into four categories. Each is now covered by Section 9:

1. **Ending discipline.** The case ends with the protagonist facing the decision, not with a narrator's summary.
2. **Domain-term hygiene.** Every non-standard term glossed at first use.
3. **Endnote economy.** Repeated attribution collapsed into one note; quotes italicized.
4. **Publication mechanics.** Disclaimer, copyright, and currency footnote present from v1, not bolted on later.

If a v1 of a future case clears Section 9 on these four items, most of the iteration loop from v8a to v8c is preempted.

---

## 11. Quick Reference: Where Things Live

| Artifact | Path |
|----------|------|
| Publication playbook (structural patterns from 14 cases) | `src/research_assistant/spaces/CW/knowledge/Publication_Playbook_v4.md` |
| Class notes from Prof. Kakoli Sen | `src/research_assistant/spaces/CW/knowledge/Prof Kakoli Sen_ClassNotes.docx` |
| Case idea template | `src/research_assistant/spaces/CW/knowledge/Case_Idea_Template__DBA Immersion_20251103.docx` |
| Published benchmark cases | `src/research_assistant/spaces/CW/knowledge/Case_Studies_Session*/` |
| Guide workflow example (teaching note) | `src/research_assistant/spaces/CW/cache/guide_20260404_172752/` |
| Writing style hooks | `.kiro/hooks/check-submission-writing.kiro.hook`, `.kiro/hooks/check-agent-writing.kiro.hook` |
| Human-authored writing steering | `.kiro/steering/human-authored-writing.md` |
| Sai Tex v8c (approved benchmark) | `src/research_assistant/spaces/CW/output/SAI_TEX_LTD_Case_Study_v8c.docx` |
| Working drafts | `src/research_assistant/spaces/CW/workspace/Case_Study_v<N>_<descriptor>.md` |
| Final `.docx` files | `src/research_assistant/spaces/CW/output/<CASE_NAME>_Case_Study_v<N>.docx` |

---

## 12. What "Done" Looks Like

A case study is publication-ready when:

1. Section 9 is clean, every item checked.
2. A naive reader can read the full narrative in one sitting and articulate the protagonist's dilemma without help.
3. At least two students, given the exhibits and no teaching note, would argue for different options with the case's own evidence.
4. The writing hooks fire zero violations on the markdown source.
5. The `.docx` renders correctly across Word, Pages, and Google Docs (spot-check each).
6. Every endnote has been clicked; every superscript in the body maps to the right note.
7. The professor's last round of feedback has been explicitly addressed, item by item, in a response email that accompanies the revised draft.

When all seven are true, the case is ready for journal submission.
