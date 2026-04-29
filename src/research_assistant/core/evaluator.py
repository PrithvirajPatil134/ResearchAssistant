"""
Evaluator Pass — grades composed output against original intent.

Level 3 upgrade: Post-composition evaluation using 4 criteria:
1. Answer Alignment: Does it answer the actual question?
2. Claim-Evidence Linkage: Is every claim backed by a source?
3. Completeness: Would the user need an obvious follow-up?
4. Actionability: Can the user DO something with this?

Separate from Analyst (scores reasoning quality during loop) and
Reviewer (checks standards compliance). The Evaluator asks:
"Would the user actually be satisfied with this?"

If any score < 3, output goes back for revision with specific feedback.
Skipped for trivial lookups (contract.skip_evaluator=True).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import logging
import json
import re

logger = logging.getLogger(__name__)


@dataclass
class EvaluationResult:
    """Result of the evaluator pass."""
    answer_alignment: int  # 1-5
    claim_evidence: int    # 1-5
    completeness: int      # 1-5
    actionability: int     # 1-5
    overall_pass: bool
    feedback: str  # Specific feedback on failing criteria
    revision_needed: List[str]  # Which criteria need revision

    @property
    def min_score(self) -> int:
        return min(self.answer_alignment, self.claim_evidence,
                   self.completeness, self.actionability)

    def to_revision_prompt(self) -> str:
        """Generate a revision prompt from failing criteria."""
        parts = []
        if self.answer_alignment < 3:
            parts.append(f"ANSWER ALIGNMENT ({self.answer_alignment}/5): The output doesn't answer the actual question. Re-read the original query and ensure every section directly addresses what was asked.")
        if self.claim_evidence < 3:
            parts.append(f"CLAIM-EVIDENCE ({self.claim_evidence}/5): Claims lack KB source backing. Every substantive claim must reference a specific KB material.")
        if self.completeness < 3:
            parts.append(f"COMPLETENESS ({self.completeness}/5): The user would need an obvious follow-up. Fill the gaps identified below.")
        if self.actionability < 3:
            parts.append(f"ACTIONABILITY ({self.actionability}/5): The user can't do anything concrete with this output. Add specific steps, templates, or frameworks.")
        if parts:
            return "## EVALUATOR FEEDBACK (fix these before presenting):\n" + "\n".join(parts)
        return ""



def run_evaluator_pass(
    content: str,
    query: str,
    contract: Any,  # DispatchContract
    llm=None,
) -> EvaluationResult:
    """
    Grade composed output against original intent using 4 criteria.
    
    Returns EvaluationResult with scores and revision feedback.
    Skipped if contract.skip_evaluator is True.
    """
    if contract and contract.skip_evaluator:
        return EvaluationResult(
            answer_alignment=5, claim_evidence=5,
            completeness=5, actionability=5,
            overall_pass=True, feedback="", revision_needed=[],
        )

    if llm:
        result = _llm_evaluate(content, query, contract, llm)
        if result:
            return result

    # Heuristic fallback
    return _heuristic_evaluate(content, query, contract)


def _llm_evaluate(
    content: str,
    query: str,
    contract: Any,
    llm,
) -> Optional[EvaluationResult]:
    """LLM-based evaluation against the 4 criteria."""
    try:
        contract_text = ""
        if contract:
            contract_text = f"\nDONE DEFINITION: {contract.done_definition}\nCRITERIA: {', '.join(contract.completeness_criteria[:5])}"

        prompt = f"""Evaluate this output against the original question.

ORIGINAL QUESTION: {query[:800]}
{contract_text}

OUTPUT (excerpt): {content[:5000]}

Score each criterion 1-5 (1=failing, 3=acceptable, 5=excellent):

1. ANSWER ALIGNMENT: Does the output answer the ACTUAL question asked (not a related one)?
2. CLAIM-EVIDENCE LINKAGE: Is every substantive claim backed by a source or KB reference?
3. COMPLETENESS: Would the user need an obvious follow-up to use this?
4. ACTIONABILITY: Can the user DO something concrete with this output?

Respond with ONLY valid JSON:
{{"answer_alignment": <1-5>, "claim_evidence": <1-5>, "completeness": <1-5>, "actionability": <1-5>, "feedback": "one sentence on the weakest criterion"}}"""

        response = llm.generate(
            prompt,
            "You are an output quality evaluator. Score honestly. Output ONLY valid JSON."
        )

        if response.success and response.content.strip():
            m = re.search(r'\{.*\}', response.content, re.DOTALL)
            if m:
                data = json.loads(m.group(0))
                scores = {
                    "answer_alignment": max(1, min(5, int(data.get("answer_alignment", 3)))),
                    "claim_evidence": max(1, min(5, int(data.get("claim_evidence", 3)))),
                    "completeness": max(1, min(5, int(data.get("completeness", 3)))),
                    "actionability": max(1, min(5, int(data.get("actionability", 3)))),
                }
                feedback = data.get("feedback", "")
                revision_needed = [k for k, v in scores.items() if v < 3]

                result = EvaluationResult(
                    answer_alignment=scores["answer_alignment"],
                    claim_evidence=scores["claim_evidence"],
                    completeness=scores["completeness"],
                    actionability=scores["actionability"],
                    overall_pass=len(revision_needed) == 0,
                    feedback=feedback,
                    revision_needed=revision_needed,
                )
                logger.info(
                    f"[EVALUATOR] Scores: align={result.answer_alignment}, "
                    f"evidence={result.claim_evidence}, complete={result.completeness}, "
                    f"action={result.actionability} → {'PASS' if result.overall_pass else 'REVISE'}"
                )
                return result

    except Exception as e:
        logger.warning(f"[EVALUATOR] LLM evaluation failed: {e}")
    return None


def _heuristic_evaluate(
    content: str,
    query: str,
    contract: Any,
) -> EvaluationResult:
    """Heuristic fallback evaluation."""
    words = len(content.split())
    query_words = set(query.lower().split())

    # Answer alignment: check if key query terms appear in output
    content_lower = content.lower()
    query_term_hits = sum(1 for w in query_words if len(w) > 4 and w in content_lower)
    alignment = min(5, max(2, query_term_hits))

    # Claim-evidence: check for reference markers
    ref_markers = content_lower.count("according to") + content_lower.count("source:") + content_lower.count("kb:") + content_lower.count("(") 
    evidence = min(5, max(2, ref_markers // 3))

    # Completeness: check word count relative to query complexity
    query_complexity = len(query.split())
    expected_min = query_complexity * 20
    completeness = 4 if words >= expected_min else (3 if words >= expected_min // 2 else 2)

    # Actionability: check for action-oriented content
    action_markers = sum(1 for marker in ["step", "next", "should", "recommend", "template", "framework", "approach"]
                        if marker in content_lower)
    actionability = min(5, max(2, action_markers))

    revision_needed = []
    for name, score in [("answer_alignment", alignment), ("claim_evidence", evidence),
                        ("completeness", completeness), ("actionability", actionability)]:
        if score < 3:
            revision_needed.append(name)

    return EvaluationResult(
        answer_alignment=alignment,
        claim_evidence=evidence,
        completeness=completeness,
        actionability=actionability,
        overall_pass=len(revision_needed) == 0,
        feedback="Heuristic evaluation — LLM unavailable",
        revision_needed=revision_needed,
    )
