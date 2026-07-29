# DV Financial-Loss Evidence Search — Agentic AI Governance Term Paper

**Date:** 2026-07-28
**Purpose:** Find real, citable sources that quantify enterprise financial losses / incident costs from AI or automated-system failures, to fill the ONE evidence gap on the dependent-variable side of the Prashar co-authored paper "Agentic AI Governance and Its Impact on Enterprise Risk and Business Performance."
**Gap identified (blind wiki test):** DV evidence (reportable incidents, financial losses, compliance failures) currently leans on a single secondary survey (Deng et al. 2025) and lacks FIRM-LEVEL FINANCIAL-LOSS data. Prashar flagged missing "McKinsey/Deloitte"-type market evidence (see synthesis, Pending Revision Areas, "Market evidence" row).
**Tooling note:** Only `WebFetch` was available this session (no `WebSearch`). Candidates were reached by fetching known authoritative landing pages/DOIs directly. Several publisher domains (IBM, McKinsey, Deloitte, Gartner) block automated fetch (HTTP 403 / 404 / timeout), so those are marked `[UNVERIFIED]` below with the reason. Everything not so marked was fetched and read in this session.

---

## Queries / fetches run

| # | Target | URL | Outcome |
|---|--------|-----|---------|
| 1 | IBM Cost of a Data Breach 2025 (landing) | ibm.com/reports/data-breach | 403 Forbidden — could not read |
| 2 | AI Incident Database | incidentdatabase.ai | FETCHED & VERIFIED |
| 3 | Stanford HAI AI Index 2025 | hai.stanford.edu/ai-index/2025-ai-index-report | FETCHED & VERIFIED |
| 4 | GDPR Enforcement Tracker | enforcementtracker.com | FETCHED & VERIFIED |
| 5 | AIID (Wikipedia cross-check) | en.wikipedia.org/wiki/AI_Incident_Database | FETCHED & VERIFIED (founding/history) |
| 6 | McGregor 2021 AAAI (AIID academic anchor) | ojs.aaai.org/index.php/AAAI/article/view/17817 (DOI 10.1609/aaai.v35i17.17817) | FETCHED & VERIFIED |
| 7 | OECD AI Incidents Monitor (AIM) | oecd.ai/en/incidents | FETCHED & VERIFIED |
| 8 | IBM Cost of a Data Breach (multiple secondary/press/PDF routes) | newsroom.ibm.com, securityintelligence.com, bleepingcomputer, helpnetsecurity, techtarget, csoonline, ibm.com/downloads | ALL 403/404/cert error — could not read |
| 9 | McKinsey State of AI (2024 PDF + 2023 page) | mckinsey.com/.../the-state-of-ai | Timeout — could not read |
| 10 | Deloitte State of GenAI in the Enterprise | deloitte.com/.../state-of-generative-ai-in-enterprise.html | 404 after redirect — could not read |
| 11 | Gartner agentic-AI cancellation prediction | gartner.com newsroom | 403 Forbidden — could not read |

---

## Verified candidate sources (ranked)

Ranked by how directly each fills the FIRM-LEVEL FINANCIAL-LOSS gap. Note up front: the sources that were openly fetchable give **incident COUNTS** and **regulatory FINES**, not firm-level operating losses from agentic AI. That is the honest state of the openly-accessible evidence (see "What remains hard to source").

| Rank | Title | Publisher | Year | Metric offered (verified quote) | Access | URL |
|------|-------|-----------|------|--------------------------------|--------|-----|
| 1 | GDPR Enforcement Tracker | CMS Law (cms.law) | Live / updated hourly (accessed 2026-07-28) | **3,202 tracked enforcement actions; €6.31B total fines** to date; filterable by country, sector, article, date, fine amount | Open, web; downloadable per-case; "DPA Access" for authorities | https://www.enforcementtracker.com/ |
| 2 | OECD AI Incidents and Hazards Monitor (AIM) | OECD | Beta, live (accessed 2026-07-28) | **~16,618 incidents & hazards** catalogued from media; filter by harm type, industry, AI principle; "Download results" available | Open, web; downloadable | https://oecd.ai/en/incidents |
| 3 | AI Incident Database (AIID) | Responsible AI Collaborative (founding sponsors Wu Foundation, Partnership on AI) | Launched Nov 2020; independent non-profit since 2022 (accessed 2026-07-28) | Real-world AI harm index; highest incident ID visible **1607**; full DB downloadable. **Does NOT attach dollar figures** to incidents | Open, web; "Download Complete Database" | https://incidentdatabase.ai/ |
| 4 | "Preventing Repeated Real World AI Failures by Cataloging Incidents: The AI Incident Database" | McGregor, S. — *Proceedings of the AAAI Conference on Artificial Intelligence*, Vol. 35, No. 17 (IAAI-21) | 2021 | Peer-reviewed academic anchor for AIID; reports "more than 1,000 incident reports archived to date" (as of 2021); faceted + full-text search design | Open access (AAAI OJS, PDF) | https://ojs.aaai.org/index.php/AAAI/article/view/17817 (DOI 10.1609/aaai.v35i17.17817) |
| 5 | The 2025 AI Index Report (Ch. 3 Responsible AI; Ch. 4 Economy) | Stanford Institute for Human-Centered AI (HAI) | 2025 (7th ed.) | States "AI-related incidents are rising sharply"; tracks responsible-AI adoption; economy chapter reports US private AI investment $109.1B (2024), gen-AI $33.9B globally, 78% org adoption. **Incident-count/harm framing, not firm-loss dollars** | Open, free PDF + public data | https://hai.stanford.edu/ai-index/2025-ai-index-report |

### `[UNVERIFIED — blocked this session, but known to exist and worth downloading manually]`

These are the sources Prashar's "McKinsey/Deloitte" note points at and the closest thing to firm-level dollar figures. I could not fetch them (publisher anti-bot blocks). They are listed so the author can retrieve them manually (they are free, registration may be required). Do NOT cite figures from these until the actual document is downloaded and read — no numbers are asserted here.

| Title | Publisher | Expected metric | Access | Where to get it |
|-------|-----------|-----------------|--------|-----------------|
| Cost of a Data Breach Report 2025 `[UNVERIFIED]` | IBM (with Ponemon Institute) | Global average breach cost (single most-cited firm-level dollar figure in the field); breakdowns by cause; historically an AI/automation cost-impact section and, in recent editions, shadow-AI figures | Free with registration | ibm.com/reports/data-breach |
| The State of AI (annual global survey) `[UNVERIFIED]` | McKinsey & Company (QuantumBlack) | % of orgs experiencing negative consequences from gen AI (inaccuracy, cybersecurity, regulatory-compliance, IP, reputational) and % taking mitigation steps | Free | mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai |
| State of Generative AI in the Enterprise `[UNVERIFIED]` | Deloitte | Barriers/risks to scaling gen AI: governance, regulatory/compliance concerns, value/ROI realization | Free | deloitte.com insights, emerging-technologies |
| Agentic-AI project cancellation prediction `[UNVERIFIED]` | Gartner (press release) | Widely-cited prediction that a large share of agentic-AI projects will be scrapped by 2027 due to cost/unclear value/inadequate risk controls | Press release, free | gartner.com newsroom (June 2025) |

---

## Assessment — which 2-3 best fill the firm-level financial-loss gap

The gap has two distinct sub-needs, and no single open source fills both. Splitting them is the honest framing:

1. **For a defensible, single firm-level dollar figure → IBM Cost of a Data Breach 2025 `[UNVERIFIED, must download]`.** This is the field's most-cited firm-level loss number and is exactly the "McKinsey/Deloitte-type" market evidence Prashar asked for. It is the strongest fit *in principle*, but it was not fetchable this session, so it must be downloaded and read before any figure is quoted. Caveat: it measures data-breach cost broadly, not agentic-AI-specific loss; recent editions add AI/shadow-AI cuts that narrow the gap.

2. **For a citable, quantified, and openly verifiable count of AI-caused harms → OECD AI Incidents Monitor (AIM) (~16,618 incidents) paired with the peer-reviewed AIID (McGregor 2021 AAAI).** AIM gives a large, filterable, downloadable incident count from an inter-governmental body; McGregor 2021 gives the peer-reviewed methodological anchor that makes the AIID citable in an academic paper rather than as a bare website. Together these substantiate the "reportable incidents" limb of the DV with sources that survive a reviewer's scrutiny.

3. **For the "compliance failures" limb of the DV → GDPR Enforcement Tracker (€6.31B across 3,202 actions).** This is the cleanest quantified proxy for the regulatory/compliance-failure dimension: real fines, real amounts, filterable by sector, openly downloadable. It is not AI-specific, but AI/automated-processing cases can be filtered within it, and it directly operationalises "compliance failures" as a measurable, monetised outcome.

Recommended top 3: **IBM Cost of a Data Breach 2025** (financial-loss limb — download required), **OECD AIM + McGregor 2021 AAAI** (incident-count limb — verified, open), **GDPR Enforcement Tracker** (compliance-failure limb — verified, open).

---

## Honest note — what remains hard to source

- **True firm-level financial losses from *agentic* AI specifically are largely proprietary and not systematically published.** Companies rarely disclose the dollar impact of an AI or agent failure; where they do (litigation, breach disclosures), it is case-by-case, not a dataset. The openly-verifiable sources above give incident *counts* (AIID, OECD AIM) and regulatory *fines* (GDPR tracker) — useful proxies, but none is a firm-level P&L-loss figure attributable to agentic AI.
- **The single best firm-level dollar figure (IBM's average breach cost) is (a) about data breaches broadly, not agentic AI, and (b) gated behind publisher anti-bot/registration**, so it could not be verified in-session. It should be downloaded manually before any number is cited.
- **McKinsey/Deloitte/Gartner surveys report the *share of firms* that experienced negative consequences, not the *money lost*.** They answer "how common" not "how costly." They still satisfy Prashar's "market evidence" ask, but they do not close the financial-loss gap on their own.
- **Deng et al. (2025), already in the wiki, remains the only source tying specific agentic-AI failure modes to loss claims** ("millions of dollars in losses for service providers"), and that figure is itself secondary (reported from a cited primary source, not measured). No open source found this session upgrades that to a measured firm-level agentic-AI loss.
- **Recommendation for provenance integrity:** frame the DV evidence as a triangulation across (i) incident counts (AIID/OECD AIM), (ii) breach-cost benchmarks (IBM, once downloaded), (iii) regulatory fines (GDPR tracker), and (iv) practitioner-survey consequence rates (McKinsey/Deloitte, once downloaded). State plainly that agentic-AI-specific firm-loss data is scarce — this is itself a defensible gap argument (framed as insufficiency, per the no-assumption rule), not a weakness to hide.

---

## Provenance

Every candidate NOT marked `[UNVERIFIED]` was fetched and read via WebFetch on 2026-07-28. Figures are quoted from those fetches. No wiki source pages were created (per instruction: we ingest only from files on disk, and none of these are downloaded). This is a candidate + search log only.
