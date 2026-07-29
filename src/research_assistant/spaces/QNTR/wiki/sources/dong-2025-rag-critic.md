---
type: source
title: "RAG-Critic: Leveraging Automated Critic-Guided Agentic Workflow for Retrieval Augmented Generation"
maturity: seed
tags: [rag, nlp-methods, agentic-workflow, self-correction, llm-as-judge, critic-model, agentic-adjacent, tangential-to-thesis]
schema_version: "1.0"
created: 2026-07-28
last_updated: 2026-07-28
originating_space: QNTR
applicable_to: [research_paper, literature_review, term_paper]
draws_from: []
authors: ["Dong, Guanting", "Jin, Jiajie", "Li, Xiaoxi", "Zhu, Yutao", "Dou, Zhicheng", "Wen, Ji-Rong"]
year: 2025
journal: "Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025), Volume 1: Long Papers"
volume: "ACL 2025"
pages: "3551-3578"
source_path: "knowledge/literature review/Agentic Governance/Relevant Readings/Tech Paper Deep Dive (Round 1)/RAG Critic_Dong_Jin_2025_A_.pdf"
ingested: 2026-07-28
code_url: "https://github.com/RUC-NLPIR/RAG-Critic"
target_path: src/research_assistant/spaces/QNTR/wiki/sources/dong-2025-rag-critic.md
---

# RAG-Critic: Leveraging Automated Critic-Guided Agentic Workflow for Retrieval Augmented Generation

## Positioning (read first)

This is a technical NLP / retrieval-augmented-generation methods paper. It is agentic-adjacent: it builds an autonomous "critic-guided agentic workflow" with a planning agent and a code executor, so it is a concrete engineering instance of agentic self-correction. It is NOT a governance study and reports no organizational, risk, or business-performance findings. Cite it only for the mechanics of agentic self-correction or as an engineering example; do not cite it as governance evidence.

## Key Arguments

The authors argue that retrieval-augmented generation (RAG) produces a wider variety of fine-grained errors than other tasks, and that automated on-policy assessment plus error-oriented correction remains unresolved [p.1, Abstract]. They contend that relying on a single LLM as judge fails to give precise, reliable judgments for RAG because of the knowledge-intensive, fine-grained nature of RAG errors [p.1]. They also state that predefined error taxonomies suffer from "Insufficient Generalization" and "Lacks Granularity & High Cost," and that the field lacks high-quality error-annotated datasets [p.2].

Their proposed answer, RAG-Critic, has three components [p.2]: (1) construction of a hierarchical RAG error system from real error responses; (2) alignment of a RAG error-critic model via a coarse-to-fine training objective that yields fine-grained error feedback; and (3) a critic-guided agentic RAG workflow that customizes and executes executor-based solution flows from the critic's feedback, enabling error-driven self-correction.

## Methodology

Three-step error-system construction pipeline [pp.3-5]:
- Step 1, Error Response Sampling: a mixed dataset is drawn from the train sets of 9 knowledge-intensive open-source datasets spanning 6 task paradigms (Table 1: NQ, TriviaQA, HotpotQA, 2Wiki, ASQA, ELI5, WoW, FEVER, WikiASP) [p.4]. A dense retriever recalls Top-K passages from a Wikipedia corpus. A pool of 15 open-source models from 9 series (parameter sizes 3B-70B) samples responses; Qwen2.5-72B acts as the supervision critic that filters erroneous samples and provides error rationales [pp.2, 4].
- Step 2, Critical Annotation & Tagging: open-set annotation (no predefined labels) with Qwen2.5-72B produces over 20,000 atomic error labels in JSON; normalization (frequency threshold, 25-token cap, JSON-format filtering) reduces these to 4,000 atomic labels [pp.4-5].
- Step 3, Error Label Summarization: hierarchical clustering (Ward Jr, 1963) yields 20 class centers; GPT-4o summarizes second-tier types; three annotators manually summarize top-tier types with cross-validation. Result: a hierarchical RAG error system of 7 top-tier labels, 19 second-tier labels, and over 4,000 tertiary labels [p.5]. (The abstract and Fig. 2 describe "3 error tiers and over 4,000 unique error types"; Fig. 2 labels the tiers as Level 1 = 7 types, Level 2 = 19 types, Level 3 = 4000+ types [pp.2-3].)

Error-Critic alignment [p.5]: supervised fine-tuning (SFT) balancing correct and error responses, followed by a Coarse-to-Fine Direct Preference Optimization (DPO, Rafailov et al. 2023) objective. The critic outputs JSON containing a binary error judgment and 3-tier error tags.

Critic-guided agentic RAG framework [pp.5-7]: an "Error-Action Mapping" table (offline solutions per error type, summarized by GPT-4o and manually optimized) plus a "Generate-Critic-Planning-Execution" workflow. Five action functions are defined (Retrieval, Rewrite, Decompose, Refine, Generate; Table 2) implementing over 15 fine-grained sub-actions [p.6, Table 2 p.5]. A planning model autonomously selects and sequences actions into an executable program; a Python executor runs it to produce a corrected answer. If the critic judges the response correct, correction is skipped (Algorithm 1) [pp.6-7].

RAG-Error benchmark [pp.6-7]: 1,900 samples (950 error + 950 correct), resampled with 5 advanced LLMs (Qwen2.5 7B/70B, Llama3.1 8B/70B, Mistral v0.3 7B) and dual LLM+human verification, balanced at 50 instances per fine-grained category, covering 9 coarse-grained and 19 fine-grained error categories.

Experimental setup [p.7]: evaluation on 6 datasets across 4 task types (single-hop QA: NQ, TriviaQA; multi-hop QA: HotpotQA, 2WikimultihopQA; long-form QA: ASQA; dialogue: WoW), metrics EM and F1. Baselines: proprietary models (o1-preview, GPT-4o, Claude 3.5-sonnet, Qwen2.5 3B-70B, Llama3.1 8B/70B) and critical-RAG baselines (Self-RAG, FLARE, MetaRAG, Self-Refine).

## Key Findings

- RAG-Critic outperforms all baselines across 7 RAG-related datasets. On the Llama3.1-8B backbone it improves overall F1 by +5.3% over standard RAG (34.0 vs 28.7); improvements hold across backbones (Qwen2.5-7B +3.8%, Llama3.1-70B +2.9%, Qwen2.5-72B +2.8%) [p.8, Table 3].
- Existing critic-based RAG methods struggle on complex QA: Self-Refine (-6.5%) and FLARE (-5.9%) decline versus standard RAG on the Llama3.1-8B backbone; MetaRAG gains only +1.9% [p.8, Table 3].
- Ablation: removing the critic model causes the largest drop (e.g., NQ F1 -5.0), followed by auto-planning; removing data-driven or manual error-system components also degrades performance [p.8, Table 4].
- On the RAG-Error benchmark, RAG-Critic at only 3B parameters reaches 96.2% average error-identification accuracy and 58.3% average classification, surpassing 70B+ models (e.g., Qwen2.5-72B 79.8% / 31.5%; GPT-4o 78.0% / 26.9%) [p.8, Table 5; p.9]. Large LLMs like Claude-3.5 and Llama3.1-70B show a bias toward over-predicting one category (borderline <70% average identification despite >95% on one class) [pp.8-9].
- Error distribution analysis (Qwen2.5-7B, Llama3.1-8B, 9 datasets): generation-phase errors (58.7%) exceed retrieval-phase errors (41.3%); over 40% of errors involve incomplete information or responses. The 7 first-tier error types by occurrence: Inaccurate Response 465 (23.51%), Incomplete Response 422 (21.33%), Incomplete Information 419 (21.18%), Irrelevant Information 339 (17.14%), Off-Topic Response 274 (13.85%), Erroneous Information 58 (2.93%), Overly Verbose Response 1 (0.05%) [p.9, Fig. 6]. The authors conclude that supplying more accurate information for retrieval and reasoning is more urgent than improving the generator's reasoning [p.9].

## Relevance to Research

Weak and indirect for the agentic-AI-governance thesis. The paper is useful only as a concrete engineering example of an autonomous "agentic workflow" that plans and self-corrects (planning agent + action functions + code executor + critic-driven skip logic, Algorithm 1) [pp.6-7]. That maps loosely to the thesis's interest in agentic autonomy and self-correction, but the paper offers no organizational-risk, governance, or business-performance analysis and no management framing. If cited at all, it belongs as a technical footnote illustrating what "agentic self-correction" looks like in a deployed NLP system, not as governance evidence. It does not fill any candidate-dimension gap in the term paper.

## Pending Actions

- [ ] Decide, with the user, whether a tangential NLP-methods paper should remain in the QNTR wiki or be reclassified as background reading only.
- [ ] If a "critic-guided agentic workflow" or "agentic self-correction" concept page is ever warranted, a second source must first appear (see manifest log Deferred items).
