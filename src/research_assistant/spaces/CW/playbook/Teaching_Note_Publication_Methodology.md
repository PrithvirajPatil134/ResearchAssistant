# Teaching Note Publication Methodology

**Purpose.** This file is the self-contained reference for writing a publication-ready teaching note in the CW space. It captures the end-to-end process we followed to produce the *SAI TEX LTD.* teaching note (v8b, approved for journal submission), and it converts every piece of feedback we received across the iteration cycle into a proactive checklist so future drafts clear the same bar without depending on reviewer feedback to surface the gaps.

**Companion file.** This methodology is the sibling of `Case_Study_Publication_Methodology.md` in the same folder. The two files are parallel in structure. Read the case study methodology first. A teaching note cannot be strong if the underlying case is weak, and many of the structural principles carry over.

**How to use this file.** Read the whole document once before starting a new teaching note. Then use Section 8 as a live self-review rubric during drafting, and Section 9 as the pre-submission gate. When Section 8 and Section 9 are both clean, the draft is ready for the professor. Section 10 is the Sai Tex feedback cycle, kept as a worked example so the abstract rules have concrete anchors.

---

## 0. Scope and Principles

A teaching note in this workspace is:
- A **solutions-oriented, instructor-facing document** that maps the case's narrative to teaching frameworks, discussion questions, and expected student responses.
- Written for the person teaching the case, not for students. Students never see the teaching note.
- **Framework-explicit.** Where the case text hides the theory, the teaching note names it (PESTEL, Porter's Five Forces, Red Queen Effect, Theory of Constraints, SEW, break-even analysis, and so on).
- Anchored in the exact exhibits and facts of the case; every analytical claim cites the source exhibit or paragraph.
- The document through which classroom time, board plan, and student-response expectations are made concrete enough for a second instructor to pick up the case and teach it well.

Five principles govern every decision:

1. **Serve the instructor.** Every section answers a question an instructor would ask before class: *What will I cover? In what order? What will students say? What frameworks ground the analysis? What do I write on the board?*
2. **One question, one answer.** Each assignment question gets one dedicated analysis section. The answer grounds theory in the case exhibits.
3. **Academic tone throughout.** No casual asides. No first-person narrator. No "here is the problem" style.
4. **Show the actual question.** Each analysis section opens by restating the assignment question, so the instructor can move between prompt and answer without flipping pages.
5. **Concise over exhaustive.** A tight five-page analysis is more useful than a sprawling fifteen-page one. The "What Happened" section in particular must be short.

---

## 1. The End-to-End Methodology

This is the process we actually followed to reach v8b. The time budgets assume the case study is already stable (v7 or later).

### Phase 1. Pattern Extraction and Structural Standards

**Goal.** Understand what a publication-ready teaching note looks like before trying to produce one.

1. Read `src/research_assistant/spaces/CW/artifacts/HBSP_Teaching_Note_Craft_Analysis.md`. This file is the canonical source for teaching note structure. It documents:
   - The HBSP template's 11-section sequence
   - Quality standards for each section
   - The Vinder Oils benchmark structure (Ivey W41939) as a real-world example
   - Gap analysis of prior Sai Tex TN drafts against HBSP / Ivey standards
   - 14 non-negotiable requirements for a publication-ready TN
2. Read the teaching notes of two or three benchmark published cases that match the new case on domain (MSME, family business, Indian industry, and so on). For Sai Tex, the closest benchmark was the Vinder Oils teaching note (Ivey W41939).
3. Read `src/research_assistant/spaces/CW/knowledge/Prof Kakoli Sen_ClassNotes.docx`, specifically the sections on teaching notes: *"Only Case Study is for students, Teaching Note is for self (whoever teaches the case). Through classroom discussion teacher should guide students..."*
4. If a new patterns file is being built, also scan the teaching notes under `src/research_assistant/spaces/CW/knowledge/Case_Studies_Session*/` to reinforce the sample.

### Phase 2. Confirm the Underlying Case is Stable

**Goal.** A teaching note cannot be written against a moving case.

1. Confirm the case study is at v7 or later and has passed the case Section 9 gate in `Case_Study_Publication_Methodology.md`.
2. List every exhibit in the case and every data point that a teaching note answer will need to cite. If an answer needs data that the case does not contain, either add the data to the case first or revise the question.
3. Confirm the dilemma statement is stable; a teaching note's assignment questions hinge on the dilemma, so changes to the dilemma trigger rework of every analysis section.

### Phase 3. First Draft via the Guide Workflow

**Goal.** Produce a complete rough draft using the package's guided workflow, not freeform generation.

1. Run the guide workflow for the teaching note in the CW space. The actual step sequence we ran on 04 April 2026 is cached at `src/research_assistant/spaces/CW/cache/guide_20260404_172752/`. The steps were:
   - Step 1: Teaching note craft analysis (reads HBSP guide and benchmark TNs)
   - Step 2: Benchmark teaching note analysis (deep read of Vinder Oils TN)
   - Step 3: Read the teaching note template
   - Step 4: Ingest the Sai Tex case study
   - Step 5: Write the teaching note
   - Each step is cached as a separate markdown file that can be reused across iterations.
2. Do not skip any step. The craft analysis and benchmark steps are what prevent the first draft from being a generic teaching note. The case-ingest step ensures every analytical claim can cite a specific exhibit.
3. The first draft produced by the guide workflow is typically around 80% of the way there on structure and around 60% on content. Expect two to three revision rounds before submission.

### Phase 4. Gap Analysis Against HBSP / Ivey Standards

**Goal.** Measure the first draft against the 14 non-negotiable TN requirements.

1. Open the gap table in `HBSP_Teaching_Note_Craft_Analysis.md` (the "GAP ANALYSIS" table). For each row, compare the draft against the requirement.
2. The historically weak items across our drafts have been:
   - **Relevant readings.** Early Sai Tex drafts missed this entirely. A publication-ready TN needs 5 to 8 academic references in proper citation format.
   - **Assignment questions.** First drafts tend to have 7 questions; the benchmark is 4 or 5.
   - **Analysis per question.** First drafts often merge framework application with expected student responses. The benchmark separates them.
   - **Teaching note exhibits (TN-1, TN-2, ...).** First drafts rely on the case exhibits only. A publication-ready TN adds its own framework exhibits (break-even summary, SEW dimensions, TOC constraint table, and so on).
3. Record each gap as an explicit revision task.

### Phase 5. Iterate on Content

**Goal.** Strengthen each section until it meets the benchmark.

For each gap, work in this order:

1. **Restate each assignment question at the top of its analysis section.** An instructor reading section 4 of the analysis should not have to flip back to section "Assignment Questions" to remember what question 4 asked. This was a Sai Tex v8 feedback item that we now bake in from v1.
2. **For each analysis section, follow the sequence:** state the question, introduce the framework with a citation, apply the framework to the case exhibits, describe expected student responses, identify the teachable insight.
3. **Remove casual language.** Phrases like *here is the problem, the cycle feeds itself, the takeaway, works like this, that said* do not belong in a teaching note. Replace with formal academic phrasing (*the analysis demonstrates, it is evident that, the preceding analysis indicates*). See Section 7 for the automated hooks that enforce this.
4. **Tighten What Happened.** This section is consistently too long in first drafts. Aim for two tight paragraphs: the decision status and the protagonist's most recent quoted position. Supporting context goes in the body of the teaching note, not here.
5. **Build TN-specific exhibits.** For Sai Tex v8b:
   - Exhibit TN-1: Break-Even Analysis Summary (two panels: current model, Option A projections)
   - Exhibit TN-2: SEW Dimensions Applied to Sai Tex
   - Exhibit TN-3: Theory of Constraints binding constraint identification

### Phase 6. Stitching and Iteration

**Goal.** Produce a draft that reads as one coherent instructor document.

1. Stitch the revised sections in sequence: author disclaimer, title, synopsis, learning objectives, position in course, relevant readings, assignment questions, teaching plan, analysis (one section per question), supplementary frameworks, what happened, teaching note exhibits, references.
2. Read the full draft end to end in one sitting. An instructor should be able to plan a 90-minute class from this document alone.
3. Run both writing hooks against the markdown. See Section 7.
4. Save drafts with an incrementing version number in `src/research_assistant/spaces/CW/output/Teaching_Note_v<N>_<descriptor>.md`.

### Phase 7. Publication Production

**Goal.** Produce the `.docx` that goes to the professor and, ultimately, the journal.

1. Use the same styled `.docx` template as the case study, so the two documents match visually (same disclaimer format, same heading styles).
2. Build the docx programmatically. See the build script used for v8b as a template.
3. Place the author disclaimer at the top. The disclaimer text differs slightly from the case study's: *"Prithviraj Patil and Kakoli Sen wrote this teaching note as an aid to instructors in the classroom use of the case <Case Name>. This teaching note should not be used in any way that would prejudice the future use of the case."*
4. Verify: all assignment questions appear both in the "Assignment Questions" section and restated at the top of each analysis section; all tables render correctly; framework names are italicized where used in analysis headers.
5. Save as `src/research_assistant/spaces/CW/output/<CASE_NAME>_Teaching_Note_v<N>.docx`.

---

## 2. Canonical Section Architecture

The teaching note uses this section sequence (derived from HBSP guide and Ivey benchmark):

| # | Section | Purpose | Length | Required |
|---|---------|---------|--------|----------|
| 1 | Author Disclaimer | Authors, institution, attribution, copyright | 5 lines | Yes |
| 2 | Title | Case title, then "Teaching Note" subtitle | 2 lines | Yes |
| 3 | Synopsis | Abstract of case plus pedagogical focus | 150 to 250 words | Yes |
| 4 | Learning Objectives | 4 to 5 Bloom's-verb objectives | List | Yes |
| 5 | Position in Course | Course types, level, prerequisites, curriculum position | 1 paragraph plus table | Yes |
| 6 | Relevant Readings | 5 to 8 academic references in citation format | List | Yes |
| 7 | Assignment Questions | 4 or 5 questions for students | Numbered list | Yes |
| 8 | Teaching Plan | Time-allocation table for a 90-minute session plus optional 60-minute condensed version | Tables | Yes |
| 9 | Analysis | One section per assignment question | 6 to 10 pages | Yes |
| 10 | Supplementary Framework (PESTEL, Five Forces, and so on) | Optional framework for industry context discussion | Table | Optional |
| 11 | What Happened | Decision status plus protagonist's latest position | 2 paragraphs | Yes |
| 12 | Teaching Note Exhibits | Framework diagrams and calculation summaries | 2 to 4 exhibits | Yes |
| 13 | References | Full academic references in citation format | List | Yes |

---

## 3. Synopsis Standards

**Length.** 150 to 250 words.

**Required content.**
- The case date, protagonist's full name, title, and company.
- The core dilemma in one sentence.
- The three (or two, or four) options available to the protagonist with dollar or rupee amounts.
- The macro context in one sentence (industry, geography, forces at play).
- The target audience for the case (MBA, executive, doctoral).
- A closing note on what makes the case pedagogically interesting.

**Sai Tex v8b synopsis pattern (for reference).** The synopsis opens with the protagonist's name and dilemma, walks through the three options with dollar figures, names the three converging forces that created the crisis, cites the financial deterioration from profit to loss with exact numbers, and closes by stating the case is for MBA, executive education, and doctoral courses.

**Currency footnote.** Immediately after the synopsis, a one-line note: *"Note: US$1 ≈ INR 92 (March 2026). All dollar figures in this teaching note use this rate."*

---

## 4. Learning Objectives

**Count.** 4 to 5 objectives. The historical default has been 5.

**Format.** Each objective uses a Bloom's taxonomy verb (*Evaluate, Analyse, Compare, Apply, Examine, Identify, Construct*).

**Principles.**
- Each objective maps to one or two assignment questions. If an objective maps to zero questions, remove the objective or add a question.
- Objectives should be specific enough that a student reading them can predict what the analysis will ask. Vague objectives ("Understand the case") are not acceptable.
- Mix analytical and applied objectives. Pure analysis without application is weak; pure application without framework grounding is weaker.

**Sai Tex v8b objectives (for reference).**
1. Evaluate strategic options under resource constraints using the financial and operational data provided in the case exhibits.
2. Analyse how the Red Queen Effect operates in a traditional manufacturing cluster.
3. Compare the job-work model with the sale-purchase model and evaluate when a business model pivot is warranted.
4. Apply the Theory of Constraints to identify Sai Tex's binding constraint.
5. Examine how socio-emotional wealth shapes strategic choices in ways that diverge from purely financial optimisation.

Each objective maps directly to assignment questions 2, 3, 3, 4, and 5 respectively. Objective 1 supports question 1.

---

## 5. Analysis Section: The Heart of the Teaching Note

This is the section the instructor will read most carefully. It is also the section where our early drafts were weakest.

**Structure for each analysis section.**

1. **Heading.** Bold, question number and short title. Example: *Question 3: The Red Queen Effect*.
2. **Restate the question.** A single paragraph starting with *"Question:"* followed by the full text of the assignment question. This was a Sai Tex v8 feedback item; now required from v1.
3. **Introduce the framework.** Name the framework, cite its academic origin, and state what it predicts or explains.
4. **Apply the framework to the case.** Use the case's own exhibits, data, and quotes. Every claim traces to a source.
5. **Describe expected student responses.** What will the strong students say? What will the weak students miss? What debate will break out? If the case has not yet been taught, note this with: *"The class will likely split into three camps..."*
6. **Synthesise the teachable insight.** Close with the insight you want students to leave the class holding.

**Academic tone in analysis sections.** This is where our drafts historically slipped. Feedback on v8 flagged Q3 and Q4 for casual language:
- v8 draft opened Q3 with *"The cycle works like this"* and closed with *"The cycle feeds itself."* Both phrases were replaced with formal academic register in v8b.
- v8 draft opened Q4 with *"Goldratt's Theory of Constraints asks a simple question..."* The v8b rewrite replaced this with *"The Theory of Constraints (Goldratt and Cox, 2004) posits that every system's throughput is limited by a single binding constraint."*

**Guiding rule.** A teaching note is academic writing. If a sentence sounds like something you would say aloud to a colleague over coffee, rewrite it.

---

## 6. Teaching Note Exhibits

**What qualifies as a TN exhibit.** Any table, diagram, or structured summary that the instructor would find useful when preparing for class, that is derived from or applied to the case but is not present in the case itself.

**Historical patterns in our TN exhibits.**

| Exhibit | Contents | When to include |
|---------|----------|-----------------|
| TN-1 | Break-even analysis summary with panels for current and future state | Any case with financial options |
| TN-2 | Framework dimensions mapped to the case (for example, SEW five dimensions, Porter's five forces for this industry) | Any case with a theoretical framework |
| TN-3 | Theory of Constraints binding constraint table (candidates, evidence for, evidence against, verdict) | Any case with operational constraints |
| TN-4 | Board plan facsimile | Per HBSP guide; we have not yet included this but should for future publications |

**Format.**
- Exhibits numbered TN-1, TN-2, and so on (distinct from case exhibit numbering).
- Titled in bold.
- Source attribution under every exhibit, typically: *"Source: <Framework source> applied to case data."* or *"Source: Constructed from case Exhibits 1 to 4 and 7."*

---

## 7. Writing Style Guardrails (Automated)

The same two hooks used for case studies enforce teaching note style:

- `check-submission-writing.kiro.hook` triggers on file save for teaching note markdown files.
- `check-agent-writing.kiro.hook` triggers after any agent write on those files.

**Both hooks check for:**

1. **Banned words.** The full list is maintained in `.kiro/steering/human-authored-writing.md` and the two hook files. Refer to those files when scanning a draft.
2. **Banned phrases and sentence openers.** Furthermore, Moreover, Additionally, Consequently, Subsequently, Nevertheless, In conclusion, To sum up.
3. **Uniform sentence rhythm.** Five or more consecutive sentences within five words of each other in length.
4. **Narrator voice.** *"Students should identify..."* is a red flag. Prefer *"The analysis shows..."* or *"The data indicates..."*.
5. **Announcing structure patterns.** *"This section will discuss..."* must be replaced with the actual content.
6. **Em dashes.** Zero tolerance. The em dash character (U+2014) must not appear anywhere. Replace with periods, commas, colons, semicolons, or parentheses.
7. **Academic tone.** Casual phrases (see Section 5 above) must be rewritten.

**Specific TN risk areas.** Because the teaching note is explaining frameworks to an instructor, there is a natural temptation to slip into a conversational voice ("Let me explain this..." or "The key thing to notice..."). Watch for these in draft 1.

---

## 8. Pre-Draft Self-Review Rubric

Run this before writing a single analysis section. If any answer is no, return to the earlier phase.

### Underlying case
- [ ] The case study has passed Section 9 of `Case_Study_Publication_Methodology.md`
- [ ] All data needed to answer each planned assignment question is in the case exhibits
- [ ] The dilemma statement is stable

### Pedagogical scope
- [ ] 4 or 5 assignment questions planned, each tied to a specific learning objective
- [ ] Target course types identified (MBA, executive, doctoral)
- [ ] Target audience position in curriculum identified (early, mid, late)
- [ ] 5 to 8 academic readings identified and accessible

### Framework mapping
- [ ] Each assignment question maps to one or two named frameworks or theories
- [ ] Each framework has a canonical academic citation
- [ ] Each framework's data requirements are satisfied by the case exhibits

---

## 9. Pre-Submission Gate

Run this before sending the `.docx` to the professor or a publisher. Every item must pass.

### Structure
- [ ] All 13 canonical sections present (or explicit justification for any omission)
- [ ] Author disclaimer at the top in the standard 5-paragraph format (Sai Tex v8 failure: missing in early drafts; added in v8b)
- [ ] Title line plus "Teaching Note" subtitle
- [ ] Synopsis 150 to 250 words with currency footnote
- [ ] 4 or 5 learning objectives using Bloom's verbs
- [ ] Position in course section includes a course-area table
- [ ] 5 to 8 academic readings in consistent citation format
- [ ] 4 or 5 assignment questions

### Analysis sections
- [ ] Each analysis section restates the assignment question at the top. (Sai Tex v8 failure: question text was not included before the answer; added in v8b.)
- [ ] Each analysis section names the relevant framework with an academic citation
- [ ] Each analysis section grounds claims in specific case exhibits
- [ ] Each analysis section describes expected student responses
- [ ] Each analysis section closes with a teachable insight
- [ ] Q3 and Q4 (or equivalents) use formal academic register. (Sai Tex v8 failure: Q3 used *"The cycle works like this"* and *"The cycle feeds itself"*, Q4 used *"asks a simple question"*. All fixed in v8b.)

### Teaching plan
- [ ] 90-minute plan present as a time-allocation table with columns for Segment, Time, Activity, Key Discussion Points
- [ ] 60-minute condensed plan present
- [ ] Each row's activity maps to an analysis section or assignment question

### What Happened
- [ ] Section is concise: 2 paragraphs. (Sai Tex v8 failure: this section was long and bullet-heavy; condensed in v8b.)
- [ ] First paragraph: current decision status
- [ ] Second paragraph: protagonist's most recent quoted position, dated
- [ ] No extended contextual bullet points in this section; that content belongs in the Analysis

### Teaching note exhibits
- [ ] At least 2 TN-specific exhibits (break-even summary, framework dimensions table, TOC table, and so on)
- [ ] Exhibits numbered TN-1, TN-2, distinct from case exhibit numbering
- [ ] Source attribution under every exhibit

### References
- [ ] Full references for every framework cited in the analysis sections
- [ ] Consistent citation format (the benchmark has been author-date with journal full name and page range)

### Publication mechanics
- [ ] File saved as `src/research_assistant/spaces/CW/output/<CASE_NAME>_Teaching_Note_v<N>.docx`
- [ ] Run of both writing hooks against the markdown precursor came back clean

### Writing hooks pass
- [ ] Zero em dashes anywhere
- [ ] Zero banned words or banned sentence openers
- [ ] No uniform sentence rhythm clusters
- [ ] No narrator voice
- [ ] No casual or conversational phrasing

---

## 10. Sai Tex Feedback Cycle: Worked Example

This section records what the professor flagged on the teaching note and why each fix matters. Use it as a diagnostic when a new draft feels "almost right but not quite."

### v6 to v7 (early publication drafts)
- Relevant Readings section was missing.
- Only 7 assignment questions; too many for a 90-minute class.
- No teaching note exhibits (TN-1, TN-2, and so on). The TN referenced only the case exhibits.
- What Happened section ran to a full page with extended context bullets.

**Fix.** Added 6 academic references in consistent citation format. Consolidated 7 assignment questions to 5. Built Exhibit TN-1 (break-even summary), TN-2 (SEW dimensions), TN-3 (TOC constraint table). Condensed What Happened to two paragraphs.

### v7 to v8 (feedback on v8 revised)
Three main items, documented:

1. **In Analysis, provide the actual question for each question.** The v8 draft had headings like *"Question 3: The Red Queen Effect"* followed immediately by the analysis, without restating the question text. The professor noted that an instructor using the TN had to flip back to the Assignment Questions section to remember what Q3 asked. *Fix in v8b: each analysis section now begins with a "Question:" paragraph containing the full question text.*
2. **Q3 and Q4 need academic tone.** Specific highlights:
   - Q3 opened with *"The cycle works like this."*
   - Q3 described the self-reinforcing dynamic with *"The cycle feeds itself."*
   - Q4 opened with *"Goldratt's Theory of Constraints asks a simple question: what is the one constraint..."*
   - *Fix in v8b: each of these phrases was rewritten in formal academic register. Q3 now describes the cycle as "a sequence of linked competitive disadvantages" and notes "Each link in this chain reinforces the next." Q4 now opens with the formal TOC definition.*
3. **What Happened section is too long.** The v8 draft had a multi-paragraph status update plus four contextual bullets. *Fix in v8b: condensed to two paragraphs (decision status plus quoted position). The contextual bullets were removed because their content was already in the main Analysis.*

### v8 to v8b
- Author disclaimer added at the top (matching case study format).
- Assignment question text included before each analysis answer.
- Q3 and Q4 rephrased for academic tone.
- What Happened made concise.

### Pattern across the cycle

Feedback mostly clustered into four categories. Each is now covered by Section 9:

1. **Analysis discipline.** Each analysis section restates the question and uses formal academic register.
2. **Section completeness.** Relevant Readings, teaching note exhibits, and publication mechanics present from v1, not bolted on later.
3. **Conciseness.** What Happened kept to two paragraphs; no mission creep into the Analysis section's territory.
4. **Framework grounding.** Every analytical claim traces to a specific exhibit or quote in the case.

If a v1 of a future teaching note clears Section 9 on these four items, most of the iteration loop from v6 to v8b is preempted.

---

## 11. Quick Reference: Where Things Live

| Artifact | Path |
|----------|------|
| HBSP teaching note craft analysis (structural standards) | `src/research_assistant/spaces/CW/artifacts/HBSP_Teaching_Note_Craft_Analysis.md` |
| Publication playbook (case study patterns, still relevant for some TN conventions) | `src/research_assistant/spaces/CW/knowledge/Publication_Playbook_v4.md` |
| Class notes from Prof. Kakoli Sen | `src/research_assistant/spaces/CW/knowledge/Prof Kakoli Sen_ClassNotes.docx` |
| Published benchmark teaching notes | `src/research_assistant/spaces/CW/knowledge/Case_Studies_Session*/*Teaching*` |
| Case study methodology (companion file) | `src/research_assistant/spaces/CW/playbook/Case_Study_Publication_Methodology.md` |
| Guide workflow example for TN drafting | `src/research_assistant/spaces/CW/cache/guide_20260404_172752/` |
| Writing style hooks | `.kiro/hooks/check-submission-writing.kiro.hook`, `.kiro/hooks/check-agent-writing.kiro.hook` |
| Human-authored writing steering | `.kiro/steering/human-authored-writing.md` |
| Sai Tex TN v8b (approved benchmark) | `src/research_assistant/spaces/CW/output/SAI_TEX_LTD_Teaching_Note_v8b.docx` |
| Working drafts | `src/research_assistant/spaces/CW/output/Teaching_Note_v<N>_<descriptor>.md` |
| Final `.docx` files | `src/research_assistant/spaces/CW/output/<CASE_NAME>_Teaching_Note_v<N>.docx` |

---

## 12. What "Done" Looks Like

A teaching note is publication-ready when:

1. Section 9 is clean, every item checked.
2. A second instructor (not the author) can read the teaching note and plan a 90-minute class from it alone, without needing to ask the author any questions.
3. Each analysis section answers its assignment question using the case's own exhibits, with frameworks named and cited.
4. The What Happened section is two paragraphs.
5. The writing hooks fire zero violations on the markdown source.
6. The `.docx` renders correctly across Word, Pages, and Google Docs.
7. The professor's last round of feedback has been explicitly addressed, item by item, in a response email that accompanies the revised draft.

When all seven are true, the teaching note is ready for journal submission alongside the case.
