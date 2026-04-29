---
inclusion: always
---

# Kiro Evolve: On-Demand "evolve" Command

When the user says "evolve" in any session, run a manual transcript review.

## Instructions

1. Read today's transcript at `~/.kiro/transcripts/YYYY-MM-DD.md` (today's date) and ALL existing files in `.kiro/steering/evolved/` AND `.kiro/steering/` to understand what is already captured.

2. Apply a filter gate before proposing anything: "Would this change how the assistant interacts with the user in a future session?"
   - Evolve IS for: preferences, research domain context, stakeholder dynamics (professors, advisors, committee members), calibration patterns, reusable frameworks (e.g., paper review rubrics, search strategies), tone/voice refinements.
   - Evolve is NOT for: debugging sessions, tool configuration, one-off scripts, prompt engineering fixes, task execution artifacts.

3. For each candidate, check whether it belongs as an update to an existing knowledge or steering file rather than a new file. Prefer updating existing files over creating new ones. Only update existing files if the new insight would change the first draft of a future output.

4. Convert all relative time references to absolute dates. "This week" becomes "week of 2026-04-28". "Recently" becomes "as of April 2026".

5. Propose changes with FULL file content, one at a time. Ask "Approve, edit, or reject?" and WAIT for user response. Maximum 5 proposals per review.

6. Write approved files to `.kiro/steering/evolved/` (create the directory if it does not exist). These files will be auto-loaded into future sessions via the workspace steering system.

7. Do NOT mark transcripts as reviewed and do NOT update `~/.kiro/transcripts/.last-review`. Manual reviews preserve transcripts for the periodic automatic review.
