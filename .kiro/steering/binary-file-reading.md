---
inclusion: always
---

# Binary File Reading and Processing

## Core Rule

Never claim inability to read PDF, DOCX, XLSX, or image files. These formats
are readable using available Python libraries. When a binary file is referenced
or encountered, extract its content and work with it.

## Extraction Method

Use `python3 scripts/read_binary.py <path> [options]` for all binary file extraction.

Supported formats and commands:
- **PDF**: `python3 scripts/read_binary.py file.pdf` (full) or `--pages 1-5` (range) or `--meta` (page count only)
- **DOCX**: `python3 scripts/read_binary.py file.docx` (full) or `--meta` (paragraph count and headings)
- **XLSX**: `python3 scripts/read_binary.py file.xlsx` (full) or `--sheet SheetName` (specific sheet) or `--meta` (sheet names and dimensions)
- **Images**: Use Pillow for metadata. For text extraction from images, note that tesseract OCR is not installed. If OCR is needed, ask the user to install it (`brew install tesseract`).

## No Conversion Files

All extraction happens in-memory via stdout. Do not write `.md`, `.txt`, or any
other converted version of a binary file to disk. The original binary file is
the single source of truth. If the content is needed again later, re-run the
extraction.

The only exception: the user explicitly asks for a markdown transcription or
annotated version of a document for a stated purpose.

## Large Document Handling: Sub-Agent Delegation

For documents over 15 pages or 30,000 characters of extracted text, delegate
full-document processing to a sub-agent via `invokeSubAgent`. This prevents
context window exhaustion in the main session.

### Sub-Agent Input Contract

The sub-agent receives:
1. The full extracted text of the document (all pages, no truncation)
2. A specific, explicit task instruction (not vague; e.g., "extract all key
   arguments with supporting evidence and page references" rather than
   "summarise this paper")

### Sub-Agent Output Contract

The sub-agent must return:
1. The requested structured output, addressing every part of the task instruction
2. Page or section references for every claim (e.g., "p.7, Section 3.2")
3. A completeness declaration: which sections of the document were processed
   and which (if any) were skipped, with reasons
4. Zero fabrication: if information is not present in the document, the sub-agent
   states "not found in document" rather than inferring from general knowledge
   or training data

### Sub-Agent Conduct Rules

- The sub-agent must process the entire document. Partial extraction,
  summary-only responses, or vague statements like "the paper discusses X"
  without specifics constitute a failed contract.
- The sub-agent must not assume, infer, or fabricate any content that is not
  explicitly present in the extracted text.
- Every factual claim in the output must trace to a specific location in the
  source document.

### Orchestrator Verification

When the sub-agent returns output, the orchestrator (main agent) must:
1. Verify the completeness declaration against the known document structure
   (page count, section headings from `--meta`)
2. Spot-check at least 2-3 claims by extracting those specific pages directly
   using `--pages` and comparing against the sub-agent's output
3. Flag any output that lacks page or section references as incomplete
4. Reject and re-delegate if the output is thin, vague, or missing sections
   the document clearly contains

## Applicability

This rule applies to:
- **Kiro IDE sessions**: all chat interactions in this workspace
- **ResearchAssistant workflows**: all five workflows (explain, guide, review,
  research, quant) running through the WorkflowInvoker pipeline
- **ReaderAgent**: when scanning knowledge directories and encountering binary files
- **AnalystAgent**: when evaluating output grounded in binary source documents,
  the completeness check must verify that all pages/sections of the source
  were processed, and the grounding check must verify page-level references

The sub-agent contract, conduct rules, and orchestrator verification apply
equally in both Kiro IDE and ResearchAssistant workflow contexts.
