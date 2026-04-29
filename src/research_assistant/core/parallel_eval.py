"""
Parallel Evaluation Orchestrator — runs Analyst, Reviewer, and Evaluator concurrently.

Level 3 upgrade: Instead of sequential Analyst → Reviewer → Evaluator,
run all three in parallel since they're independent evaluations of the
same content. Merges their verdicts into a unified evaluation result.

Latency savings: ~60-70% reduction in evaluation time (3 sequential LLM
calls become 1 parallel round).
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class UnifiedEvaluation:
    """Merged result from parallel Analyst + Reviewer + Evaluator."""
    # Analyst results
    analyst_score: float = 0.0
    analyst_passed: bool = False
    analyst_feedback: str = ""

    # Reviewer results
    reviewer_score: float = 0.0
    reviewer_passed: bool = False
    reviewer_issues: List[Dict[str, Any]] = field(default_factory=list)
    reviewer_suggestions: List[str] = field(default_factory=list)
    reviewer_strengths: List[str] = field(default_factory=list)

    # Evaluator results
    evaluator_alignment: int = 0
    evaluator_evidence: int = 0
    evaluator_completeness: int = 0
    evaluator_actionability: int = 0
    evaluator_passed: bool = False
    evaluator_feedback: str = ""

    # Unified verdict
    overall_pass: bool = False
    revision_prompt: str = ""

    def compute_verdict(self) -> None:
        """Compute unified pass/fail from all three evaluations."""
        self.overall_pass = (
            self.analyst_passed
            and self.reviewer_passed
            and self.evaluator_passed
        )

        if not self.overall_pass:
            parts = []
            if not self.analyst_passed:
                parts.append(f"ANALYST ({self.analyst_score:.1f}/10): {self.analyst_feedback}")
            if not self.reviewer_passed:
                issues_text = "; ".join(
                    i.get("message", "") for i in self.reviewer_issues[:3]
                )
                parts.append(f"REVIEWER ({self.reviewer_score:.1f}/10): {issues_text}")
            if not self.evaluator_passed:
                parts.append(f"EVALUATOR: {self.evaluator_feedback}")
            self.revision_prompt = "## PARALLEL EVALUATION FEEDBACK:\n" + "\n".join(parts)


def run_parallel_evaluation(
    content: str,
    query: str,
    extracted_content: List[str],
    contract: Any,
    analyst: Any,
    reviewer: Any,
    workflow_name: str = "explain",
    persona_name: str = "",
    iteration: int = 0,
    llm: Any = None,
) -> UnifiedEvaluation:
    """
    Run Analyst, Reviewer, and Evaluator in parallel.

    All three evaluate the same content independently, then their
    verdicts are merged into a UnifiedEvaluation.

    Falls back to sequential execution if threading fails.
    """
    result = UnifiedEvaluation()

    def _run_analyst():
        """Run analyst scoring."""
        try:
            score_result = analyst.execute(
                query=query,
                reasoning=content,
                knowledge_content=extracted_content,
                iteration=iteration,
            )
            return ("analyst", score_result)
        except Exception as e:
            logger.warning(f"[PARALLEL_EVAL] Analyst failed: {e}")
            return ("analyst", None)

    def _run_reviewer():
        """Run reviewer validation."""
        try:
            review_result = reviewer.review_against_standards(
                content=content,
                workflow_name=workflow_name,
                user_query=query,
                persona={"name": persona_name},
                contract=contract,
            )
            return ("reviewer", review_result)
        except Exception as e:
            logger.warning(f"[PARALLEL_EVAL] Reviewer failed: {e}")
            return ("reviewer", None)

    def _run_evaluator():
        """Run evaluator pass."""
        try:
            from .evaluator import run_evaluator_pass
            eval_result = run_evaluator_pass(
                content=content,
                query=query,
                contract=contract,
                llm=llm,
            )
            return ("evaluator", eval_result)
        except Exception as e:
            logger.warning(f"[PARALLEL_EVAL] Evaluator failed: {e}")
            return ("evaluator", None)

    # Run all three in parallel
    tasks = [_run_analyst, _run_reviewer, _run_evaluator]

    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(fn): fn.__name__ for fn in tasks}

            for future in as_completed(futures, timeout=120):
                try:
                    agent_name, agent_result = future.result(timeout=60)
                    _merge_result(result, agent_name, agent_result)
                except Exception as e:
                    fn_name = futures[future]
                    logger.warning(f"[PARALLEL_EVAL] {fn_name} timed out or failed: {e}")

    except Exception as e:
        logger.warning(f"[PARALLEL_EVAL] Parallel execution failed, falling back to sequential: {e}")
        # Sequential fallback
        for fn in tasks:
            try:
                agent_name, agent_result = fn()
                _merge_result(result, agent_name, agent_result)
            except Exception as ex:
                logger.warning(f"[PARALLEL_EVAL] Sequential {fn.__name__} failed: {ex}")

    result.compute_verdict()

    logger.info(
        f"[PARALLEL_EVAL] Analyst={result.analyst_score:.1f} "
        f"Reviewer={result.reviewer_score:.1f} "
        f"Evaluator=({result.evaluator_alignment},{result.evaluator_evidence},"
        f"{result.evaluator_completeness},{result.evaluator_actionability}) "
        f"→ {'PASS' if result.overall_pass else 'REVISE'}"
    )

    return result


def _merge_result(unified: UnifiedEvaluation, agent_name: str, agent_result: Any) -> None:
    """Merge an individual agent result into the unified evaluation."""
    if agent_result is None:
        return

    if agent_name == "analyst":
        score = agent_result.output
        if score:
            unified.analyst_score = score.overall
            unified.analyst_passed = score.passed
            unified.analyst_feedback = score.feedback

    elif agent_name == "reviewer":
        unified.reviewer_score = agent_result.overall_score
        unified.reviewer_passed = agent_result.meets_standards
        unified.reviewer_issues = agent_result.issues
        unified.reviewer_suggestions = agent_result.suggestions
        unified.reviewer_strengths = agent_result.strengths

    elif agent_name == "evaluator":
        unified.evaluator_alignment = agent_result.answer_alignment
        unified.evaluator_evidence = agent_result.claim_evidence
        unified.evaluator_completeness = agent_result.completeness
        unified.evaluator_actionability = agent_result.actionability
        unified.evaluator_passed = agent_result.overall_pass
        unified.evaluator_feedback = agent_result.feedback
