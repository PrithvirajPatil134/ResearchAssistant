# Knowledge Ingest Triage — 2026-07-28

Full triage of all knowledge/ files across the four spaces (197 files), produced
by four parallel per-space triage agents that opened each file to verify true
author/year/title (not filename), cross-checked against existing wiki sources,
and traced version lineage. Read-only; no wiki writes during triage.

User scoping directives (2026-07-28):
- The journal-ranking sheets (ABDC JQL), class supplementary spreadsheet
  (Variability), and impact-factor sheet (JCRI) ARE wanted → INGEST.
- Anything relevant to the DBA thesis OR the Prof. Prashar co-authored paper
  belongs in the wiki → the agentic-governance + quant-methods items are all
  in-scope (they serve both efforts), pulling several "low-priority" items up.
- The rest of the triage stands.

## The two research scopes (grounds "relevant")

- **Prashar/QNTR paper**: "Agentic AI Governance and Its Impact on Enterprise Risk
  and Business Performance." Governance-maturity → incidents/losses/compliance.
  Lenses: principal-agent theory, formative measurement, SEM + mediation/moderation.
- **DBA thesis**: "Capital Efficiency in the Digital Era: IT Governance and
  Resource Rationalization on Firm Performance." SaaS rationalization, ROIC,
  agency theory, governance-index method, org-structure coding.

Because the thesis and paper share methods (formative scales, SEM fit, mediation,
governance constructs), the QNTR quant-methods papers are in-scope for BOTH.

## FINAL INGEST LIST (after user directives)

### QNTR — governance domain (Prashar paper + thesis)
| Slug | Source file | Priority |
|---|---|---|
| dafoe-2018-ai-governance-research-agenda | GovAI-Research-Agenda.pdf | HIGH |
| gahnberg-2021-framing-governance-artificial-agency | Framing Governance...Ganhberg | HIGH |
| deng-2025-ai-agents-security-survey | AI Agents Under Threat_Deng | HIGH |
| julian-botti-2019-multi-agent-systems | Multi-Agent Systems_Julian_Botti | MED (now in-scope: agentic) |
| dong-2025-rag-critic | RAG Critic_Dong_Jin | LOW (agentic-adjacent tech) |

### QNTR — quant methods (paper's scale + thesis method)
| Slug | Source file | Priority |
|---|---|---|
| diamantopoulos-2008-advancing-formative | 2008 JBR Diamantopoulos | HIGH |
| hu-bentler-1999-cutoff-criteria-fit-indexes | 1999 Hu & Bentler | HIGH |
| preacher-2007-moderated-mediation | 2007 Preacher | HIGH |
| hildebrandt-temme-2006-formative-csa | 2006 Hildebrandt & Temme | MED |
| mackinnon-2007-mediation-analysis | 2007 MacKinnon | MED |
| marcoulides-yuan-2016-goodness-of-fit | 2016 Marcoulides & Yuan | MED |
| shi-2017-model-size-effect-sem | 2017 Shi | MED |
| shi-2021-sem-fit-small-df | 2021 Shi | MED |
| maula-stam-enhancing-rigor-quant-research | Enhancing rigor in quant research | MED |

### QNTR — reference sheets (user explicitly requested)
| Slug | Source file | Note |
|---|---|---|
| abdc-jql-2022-journal-ranking | S1-2 QNTR 2025 - ABDC JQL 2022 v3.xlsx | Journal-quality gate for lit search |
| abdc-jql-2025-journal-ranking | ABDC_JQL_2025_consultation-draft.xlsx | Newer ABDC draft |
| jcri-impact-factors-2025 | JCRI-mpact-Factors_2025.pdf | Impact-factor reference |
| qntr-variability-supp-material | S1-2 QNTR 2025 Supp Material - Variability.xlsx | Class supplementary |

### QNTR — persona anchor
| Slug | Source file | Note |
|---|---|---|
| prashar-maity-2024-cbib-internal-branding | Model research article.pdf | Prashar's own IMM paper; persona anchor |

### DBA — thesis-spine (open-access foundations)
| Slug | Source file | Priority |
|---|---|---|
| alekseeva-2026-ai-adoption-managerial-expertise | thesis-spine-papers/alekseeva-2026 | HIGH (IV measure) |
| albert-2026-org-structure-database | thesis-spine-papers/albert-2026 | HIGH (method to replicate) |
| larcker-2007-governance-index-ssrn | thesis-spine-papers/larcker-2007 | MED-HIGH (governance index) |

### CRO — theory (methods thread supports both efforts)
| Slug | Source file | Priority |
|---|---|---|
| eisenhardt-1989-building-theories-case-study | Session 4 AMR 1989 | HIGH (distinct from ingested 2007) |
| dimaggio-1995-comments-what-theory-is-not | Session 3 comments | HIGH (companion to Sutton-Staw) |
| kohli-jaworski-1990-market-orientation | Session 7 | MED |

### OFF-SCOPE / deferred (NOT thesis- or paper-relevant)
- lewin-massini-peeters-2009-offshoring (CRO, low)
- sheth-2011-emerging-markets-marketing (QNTR, off-topic)
- zeithaml-2000-service-quality, szymanski-2007-npd-meta (DBA marketing course)
- tooze-2018-crashed (480pp book; chapter-scoped only if CG coursework needs it)
- CW: publication-playbook-v4, Sen class notes, HBS TN guide, Ivey submission +
  citation guidelines (case-writing methodology; dormant space, ingest if/when CW
  work resumes). ~20 CW exemplar cases: deferred (playbook already distills them).

## Traps the deep triage caught (would have failed on filenames)
- `Mikalef-Conboy_Lundstorm_2025.pdf` is actually **Papagiannidis et al.** →
  already ingested as papagiannidis-2025. NOT a new paper.
- Eisenhardt **1989** (uncovered) ≠ Eisenhardt & Graebner **2007** (ingested).
- "AI Agents Under Threat ...2021" is actually a **2025** ACM survey (Deng et al.).
- `Agentic Governance Research Paper_v1_WIP.docx`: superseded draft containing
  fabricated stats ("78% of organizations…") — EXCLUDE; would violate no-assumption.
- Vu 2025 has two full-text .md extractions + the wiki page (one paper, not three).
- CW Publication_Playbook chain: v4 wins over v1/v2/v3.

## Counts
- FINAL INGEST (in-scope): ~28 (QNTR 19 incl. sheets, DBA 3, CRO 3, + persona anchor)
- Already-covered: 36 | Skip-noise: ~65 | Skip-superseded: ~6 | Operational: ~31
- CW methodology set (5) + exemplars (~20): deferred to CW reactivation.

## Prerequisite (DONE 2026-07-28)
`read_binary.py` was fixed (commit 9f693b5): PyPDF2/python-docx/python-pptx/openpyxl
declared + installed in .venv, .pptx support added. Ingest of DOCX/PPTX/XLSX
sources now works; before this the ingestor would have failed on non-PDF files.
