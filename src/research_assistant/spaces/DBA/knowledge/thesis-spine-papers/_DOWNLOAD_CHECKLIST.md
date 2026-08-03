# Thesis Spine Papers — Download Checklist

**STATUS 2026-07-29: COMPLETE.** All spine papers are downloaded and on disk in this
folder. PDFs are full-text (page counts verified with `read_binary.py --meta`).
Next step is full-text methodology extraction, not retrieval — see
`data/summaries/thesis-fulltext-extractions.md` Section 4.

Read any paper with `python3 scripts/read_binary.py <path>`. Do NOT re-attempt web
retrieval; these are already here.

## On disk (all obtained)

- [x] **Alekseeva, Azar, Giné & Samila (2026)** — AI adoption intensity (IV) — Gold OA, 2026-07-15
  - `alekseeva-2026-ai-adoption-managerial-expertise.pdf`
- [x] **Albert, Eklund & Tang (2026)** — org structure database from SEC filings (DV method) — Gold OA, 2026-07-15
  - `albert-2026-org-structure-database.pdf`
- [x] **Larcker, Richardson & Tuna (2007)** — governance index PCA — 2026-07-29
  - `larcker-2007-governance-index-published.pdf` (published Accounting Review version, 47 pp)
  - `larcker-2007-governance-index-ssrn.pdf` (SSRN working-paper version, retained)
- [x] **Romanelli & Tushman (1994)**, Academy of Management Journal — canonical PE coding scheme — 2026-07-29
  - `romanelli-tushman-1994-pe-empirical-test.pdf` (27 pp)
- [x] **Lee, Sridhar, Henderson & Palmatier (2015)**, Marketing Science — segment-reporting structure coding — 2026-07-29
  - `lee-2015-customer-centric-structure.pdf` (20 pp)
- [x] **Lant, Milliken & Batra (1992)**, SMJ — strategy+domain reorientation rule — 2026-07-29
  - `lant-1992-managerial-learning-reorientation.pdf` (25 pp)
- [x] **Zahra & Covin (1993)**, SMJ — technology posture scale — 2026-07-29
  - `zahra-covin-1993-technology-posture.pdf` (29 pp)
- [x] **Mithas & Rust (2016)**, MIS Quarterly — IT spending ratio construction — 2026-07-29
  - `mithas-rust-2016-it-strategy-investments.pdf` (25 pp)

## Already extracted into thesis-fulltext-extractions.md (methodology captured)

- [x] McElheran et al. (2024) — extracted from NBER working paper 31788
- [x] Girod & Whittington (2015) — extracted from U. Reading CentAUR repository (has the 0.30 restructuring threshold). Published Organization Science version now also on disk: `girod-whittington-2015-change-escalation.pdf`

## Not yet retrieved (were on the original 9-paper priority list; optional depth)

The ~15 further A*/A papers catalogued at abstract level in
`data/summaries/lit-search-thesis-foundations-v2.md` (Gersick 1991, Meyer 1982,
Greenwood & Hinings 1996, Sanders & Carpenter 1998, Gerstner et al. 2013, etc.)
are not downloaded. They are secondary to the eight spine papers above.

## After this

Tell the IDE agent "extract the spine papers" and it will fan out one
`ra-wiki-ingestor` per PDF, extract coding schemes/thresholds/scale items with page
citations, then update `data/summaries/thesis-fulltext-extractions.md`.
