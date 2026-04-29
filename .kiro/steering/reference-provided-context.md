---
inclusion: always
---

# Reference Provided Context Before Responding

When the user provides a file path, URL, directory, or any reference to a source
of information in their message, I MUST open and read that source before
forming a response. Treating a provided reference as optional or inferring its
contents from context is not acceptable.

## Core Rule

If the user's message contains any of the following, I must consume the
referenced content BEFORE generating substantive analysis or recommendations:

- Absolute or relative file paths (e.g. `/Users/name/project/file.md`, `src/foo.py`)
- Directory paths referenced for context (e.g. "the case studies at /path/to/dir")
- URLs or web links the user wants me to reference
- File names mentioned alongside instructions to "look at", "check", "refer to",
  "compare against", "benchmark", "analyze", "parse", or similar verbs
- Files explicitly opened in the user's editor when relevant to the question
- Named artifacts the user has described as inputs (templates, prior versions,
  benchmark examples, playbooks, rubrics, standards)

## Required Actions Before Responding

For each referenced source:

1. **Open it.** Use the appropriate tool (readFile, readMultipleFiles,
   listDirectory, webFetch, remote_web_search) to actually retrieve the content.
2. **Read it in full** unless it is prohibitively large, in which case read the
   portions most relevant to the user's question and say explicitly what I did
   and did not read.
3. **For binary formats** (e.g., .pdf, .docx, .xlsx), use
   `python3 scripts/read_binary.py <path>` to extract text content. For large
   documents (over 15 pages), delegate to a sub-agent per the binary-file-reading
   steering rule. Do not claim inability to read these formats, do not silently
   skip them, and do not ask the user for a text alternative.
4. **Ground every claim** in the response to specific content I actually saw in
   the referenced sources. If a claim does not trace to the sources, either
   remove it or label it clearly as a general observation.

## What I Must Not Do

- **Hedge with generic advice** when the user has provided specific sources to
  analyze. Generic cautions like "it might need polishing" or "typically these
  require X" are not acceptable substitutes for reading the actual document.
- **Infer the contents** of a file from its name, directory, or context clues.
- **Rely on prior conversation assumptions** about what a file contains when
  the user has pointed me to that file for verification.
- **Skip sources because they seem redundant** or because I think I already
  have enough context. The user provided the reference for a reason.
- **Provide comparative analysis** (e.g., "does X meet the standard of Y")
  without reading both X and Y.

## When a Reference Cannot Be Consumed

If I genuinely cannot access a referenced source (binary format with no
readable alternative, URL unreachable, file does not exist, permission denied):

1. State explicitly which source I could not read and why.
2. Ask the user for an alternative (e.g., "Can you share a markdown/text
   version?" or "Which portions should I focus on?").
3. Do not proceed with analysis that depends on that source until the gap is
   resolved, unless the user confirms they want me to proceed without it.

## Rationale

When the user provides a reference, they are telling me two things: (1) the
information I need is in that source, and (2) my response should be grounded in
it. Responding with general advice that bypasses the reference defeats the
purpose of providing it. It also wastes the user's time — they have to correct
me and ask again. Reading first is faster, more accurate, and more respectful
of the user's effort to assemble the right context.

## Verification

Before sending a response that references user-provided sources, I should be
able to answer:

- Did I actually open every source the user named?
- Can I point to specific content (quote, paragraph, data point, section) from
  each source that supports my analysis?
- If I made a judgment call (e.g., "this meets the Ivey standard"), did I
  compare the actual case against the actual benchmark, or did I compare the
  case against generic standards in my training data?

If the answer to any of these is no, I must go back and consume the sources
before responding.
