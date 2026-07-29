---
type: reference
title: "Washington & Lee Law Journal Rankings"
maturity: seed
tags: [journal-ranking, law, washington-and-lee, quality-gate, literature-search]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [literature_review, research_paper, term_paper]
draws_from: []
source_url: "https://managementtools4.wlu.edu/LawJournals/"
target_path: src/research_assistant/spaces/QNTR/wiki/references/wl-law-journal-rankings.md
---

**What it is**

The Washington & Lee (W&L) Law Journal Rankings database, hosted by the W&L Law Library. There is no local file for this list; it lives online only. The current active database is at `managementtools4.wlu.edu/LawJournals/`. It states the "2025 Rankings provide citation data and calculated ranks for the top 400 U.S.-published law journals and the top 100 law journals published outside the United States," with a five-year survey span (2021-2025) [managementtools4.wlu.edu/LawJournals/, fetched 2026-07-28].

**What it is for**

The journal-quality gate for Law sources in QNTR literature search. `.kiro/steering/literature-review-standards.md` names "Washington & Lee Law Journal Rankings (Top 50)" as the Law standard [literature-review-standards.md, §"Ranking systems to use"]. Use the database to confirm a law journal ranks within the Top 50 before including a paper.

**How to use**

Open `https://managementtools4.wlu.edu/LawJournals/`. Under "Choose Journal Criteria," filter by Subject, Country, Journal Name, Language, Journal Type, Editor, and Format, and pick a Year (2025 or prior years). Under "Show:" choose a preset list size (Top 10 / 25 / 50 / 100 / 200 / 400 / All). Rank by "Combined Score" and take the "Top 50" view to apply the standard [managementtools4.wlu.edu/LawJournals/, fetched 2026-07-28].

**Ranking metrics** (as observed on the database)

Column measures: Combined Score, Impact Factor, Journal Cites, Currency Factor, and Case Cites [managementtools4.wlu.edu/LawJournals/, fetched 2026-07-28]. The default view ranks by Combined Score (e.g. Columbia Law Review 100.00, Harvard Law Review 94.68, Stanford Law Review 85.64 at the top of the 2025 list).

**Caveat**: The database uses ASP.NET postback controls, so column sorts and journal-detail links require interacting with the live site rather than a static fetch. The Top 50 threshold above is stated per the steering file. Older W&L URLs (e.g. `lawlib.wlu.edu`, `managementranking.lawlib.wlu.edu`) did not resolve when fetched on 2026-07-28; use the `managementtools4.wlu.edu/LawJournals/` host.

**Portal**: `https://managementtools4.wlu.edu/LawJournals/` (no local file — online lookup only)
