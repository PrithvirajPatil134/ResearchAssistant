"""
Analyst Agent - LLM-powered evaluation of reasoning quality.

Uses a rubric-based LLM grader (inspired by Anthropic's eval framework)
with heuristic pre-checks to catch obviously broken output fast.

Evaluation dimensions:
- KB Grounding (25%): Is content grounded in provided source materials?
- Completeness (25%): Does it address all parts of the query?
- Quality & Rigor (25%): Does it meet academic/professional standards?
- Structure & Clarity (25%): Is it well-organized and clear?
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
import json
import re

from .base import BaseAgent, AgentResult

logger = logging.getLogger(__name__)


@dataclass
class ReasoningScore:
    """Score for a reasoning chain."""
    overall: float  # 0-10 scale
    passed: bool  # True if overall >= threshold
    kb_relevance: float  # 0-10: How well grounded in knowledge base
    coherence: float  # 0-10: Structure and clarity
    addresses_question: float  # 0-10: Completeness
    feedback: str  # Specific improvement feedback
    iteration: int = 0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class AnalysisContext:
    """Context for analysis."""
    query: str
    reasoning: str
    knowledge_content: List[str]
    persona_context: Optional[Dict[str, Any]] = None
    contract: Optional[Any] = None  # DispatchContract for Level 3 scoring


class AnalystAgent(BaseAgent):
    """
    LLM-powered evaluation agent.
    
    Two-phase scoring:
    1. Fast heuristic pre-check (catches empty/broken output instantly)
    2. LLM rubric evaluation (real quality assessment)
    
    Falls back to heuristic-only if LLM is unavailable.
    """
    
    PASS_THRESHOLD = 7.5  # Lowered from 9.0 — LLM scoring is stricter than heuristics
    MAX_ITERATIONS = 5
    
    def __init__(self, memory, context_guard):
        super().__init__("analyst", memory, context_guard)
        self._scoring_history: List[ReasoningScore] = []
        self._current_iteration = 0
    
    def execute(self, **kwargs) -> AgentResult:
        """Main execution - score reasoning quality."""
        query = kwargs.get("query", "")
        reasoning = kwargs.get("reasoning", "")
        knowledge_content = kwargs.get("knowledge_content", [])
        iteration = kwargs.get("iteration", 0)
        contract = kwargs.get("contract", None)
        
        self._current_iteration = iteration
        
        context = AnalysisContext(
            query=query,
            reasoning=reasoning,
            knowledge_content=knowledge_content,
            persona_context=self._persona_context,
            contract=contract,
        )
        
        score = self.score_reasoning(context)
        
        return AgentResult(
            success=True,
            output=score,
            tokens_used=500,
            metadata={
                "passed": score.passed,
                "overall_score": score.overall,
                "iteration": iteration,
            }
        )
    
    def score_reasoning(self, context: AnalysisContext) -> ReasoningScore:
        """Score reasoning with heuristic pre-check + LLM evaluation."""
        self.log_operation("score_reasoning", 150)
        
        # Phase 1: Fast heuristic pre-check
        precheck = self._heuristic_precheck(context)
        if precheck is not None:
            self._scoring_history.append(precheck)
            return precheck
        
        # Phase 2: LLM-based rubric evaluation
        score = self._llm_evaluate(context)
        if score is None:
            # LLM unavailable — fall back to heuristic scoring
            score = self._heuristic_score(context)
        
        self._scoring_history.append(score)
        
        logger.info(
            f"[ANALYST] Score: {score.overall}/10 "
            f"(KB:{score.kb_relevance}, Struct:{score.coherence}, Compl:{score.addresses_question}) "
            f"- {'PASS' if score.passed else 'NEEDS IMPROVEMENT'}"
        )
        
        return score
    
    def _heuristic_precheck(self, context: AnalysisContext) -> Optional[ReasoningScore]:
        """Fast check to catch obviously broken output. Returns None if output looks OK."""
        reasoning = context.reasoning.strip()
        
        # Check 1: Empty or near-empty content
        content_words = len(reasoning.split())
        if content_words < 30:
            return ReasoningScore(
                overall=0.0, passed=False,
                kb_relevance=0.0, coherence=0.0, addresses_question=0.0,
                feedback="CRITICAL: Output is empty or near-empty. LLM generation likely failed.",
                iteration=self._current_iteration,
            )
        
        # Check 2: Output is just the prompt echoed back
        query_start = context.query[:100].strip()
        if reasoning.startswith(query_start) and content_words < 100:
            return ReasoningScore(
                overall=0.0, passed=False,
                kb_relevance=0.0, coherence=0.0, addresses_question=0.0,
                feedback="CRITICAL: Output appears to be the prompt echoed back, not generated content.",
                iteration=self._current_iteration,
            )
        
        # Check 3: Output is mostly tool call artifacts
        artifact_lines = sum(1 for line in reasoning.split('\n') 
                           if any(line.strip().startswith(p) for p in 
                                  ['Reading file:', 'Creating:', '✓ Successfully', '(using tool:']))
        total_lines = max(len(reasoning.split('\n')), 1)
        if artifact_lines / total_lines > 0.3:
            return ReasoningScore(
                overall=1.0, passed=False,
                kb_relevance=0.0, coherence=1.0, addresses_question=0.0,
                feedback="CRITICAL: Output contains mostly tool call artifacts, not actual content.",
                iteration=self._current_iteration,
            )
        
        return None  # Passed pre-check, proceed to LLM evaluation
    
    def _llm_evaluate(self, context: AnalysisContext) -> Optional[ReasoningScore]:
        """
        Evaluate output quality iteratively — one dimension at a time,
        like a human reviewer who reads for structure first, then content, then rigor.
        
        Dimensions evaluated sequentially:
        1. Structure & Clarity → sets expectations for what's there
        2. KB Grounding → checks if content is sourced properly
        3. Completeness → checks if all parts of query are addressed
        4. Quality & Rigor → final holistic quality assessment informed by above
        """
        try:
            from ..core import get_llm_client
            llm = get_llm_client()
            
            output_excerpt = context.reasoning[:5000]
            query_excerpt = context.query[:1000]
            kb_excerpt = '\n'.join(c[:500] for c in context.knowledge_content[:3])
            
            base_context = f"""## QUERY: {query_excerpt}

## OUTPUT (excerpt): {output_excerpt}

## KB SOURCES (excerpt): {kb_excerpt[:1500]}"""

            # Level 3: Inject dispatch contract for intent-aware scoring
            if context.contract and hasattr(context.contract, 'to_analyst_prompt'):
                base_context += f"\n\n{context.contract.to_analyst_prompt()}"
            
            sys_prompt = "You are a strict academic evaluator. Output ONLY valid JSON. Be honest."
            
            dimensions = [
                ("structure_clarity", 
                 "Evaluate STRUCTURE & CLARITY only. Is it well-organized? Clear sections? Logical flow? "
                 "Readable formatting? (0=chaotic, 5=basic, 10=exemplary)"),
                ("kb_grounding",
                 "Evaluate KB GROUNDING only. Is content sourced from the provided materials? "
                 "Does it use real data/facts from KB rather than fabricating? (0=fabricated, 5=partial, 10=fully sourced)"),
                ("completeness",
                 "Evaluate COMPLETENESS only. Does it address ALL parts of the query? "
                 "Any missing sections or unanswered aspects? (0=ignores query, 5=partial, 10=comprehensive)"),
                ("quality_rigor",
                 "Evaluate QUALITY & RIGOR only. Does it meet professional/academic standards? "
                 "Is analysis deep, writing precise, reasoning sound? (0=superficial, 5=adequate, 10=publication-ready)"),
            ]
            
            scores_dict = {}
            running_assessment = ""
            all_feedback = []
            
            for dim_name, dim_prompt in dimensions:
                prompt = f"""{base_context}

{f'## ASSESSMENT SO FAR:{chr(10)}{running_assessment}' if running_assessment else ''}

## EVALUATE THIS DIMENSION:
{dim_prompt}

Respond with ONLY: {{"score": <0-10>, "reasoning": "<1 sentence why>"}}"""
                
                response = llm.generate(prompt, sys_prompt)
                
                if response.success and response.content.strip():
                    raw = response.content.strip()
                    json_match = re.search(r'\{.*?\}', raw, re.DOTALL)
                    if json_match:
                        try:
                            result = json.loads(json_match.group(0))
                            score = float(result.get("score", 5))
                            reasoning = result.get("reasoning", "")
                            scores_dict[dim_name] = score
                            running_assessment += f"\n- {dim_name}: {score}/10 — {reasoning}"
                            all_feedback.append(f"{dim_name}: {reasoning}")
                            logger.info(f"[ANALYST] {dim_name}: {score}/10")
                            continue
                        except (json.JSONDecodeError, ValueError):
                            pass
                
                # Fallback for this dimension
                scores_dict[dim_name] = 5.0
                logger.warning(f"[ANALYST] {dim_name}: LLM eval failed, defaulting to 5.0")
            
            # Calculate overall
            kb = scores_dict.get("kb_grounding", 5)
            completeness = scores_dict.get("completeness", 5)
            quality = scores_dict.get("quality_rigor", 5)
            structure = scores_dict.get("structure_clarity", 5)
            overall = round((kb + completeness + quality + structure) / 4, 1)
            feedback = " | ".join(all_feedback) if all_feedback else "No feedback."
            
            logger.info(f"[ANALYST] Final: KB={kb}, Compl={completeness}, Qual={quality}, Struct={structure} → {overall}")
            
            return ReasoningScore(
                overall=overall,
                passed=overall >= self.PASS_THRESHOLD,
                kb_relevance=kb,
                coherence=structure,
                addresses_question=completeness,
                feedback=feedback,
                iteration=self._current_iteration,
            )
            
        except Exception as e:
            logger.warning(f"[ANALYST] LLM eval error: {e}")
            return None
    
    def _heuristic_score(self, context: AnalysisContext) -> ReasoningScore:
        """Fallback heuristic scoring when LLM is unavailable."""
        reasoning = context.reasoning
        query = context.query
        
        # Simple length-based scoring
        word_count = len(reasoning.split())
        length_score = min(10.0, word_count / 100)  # 1000 words = 10
        
        # Term overlap with query
        query_terms = [t.lower() for t in query.split() if len(t) > 3]
        reasoning_lower = reasoning.lower()
        if query_terms:
            overlap = sum(1 for t in query_terms if t in reasoning_lower) / len(query_terms)
        else:
            overlap = 0.5
        relevance_score = min(10.0, 5.0 + overlap * 5.0)
        
        # KB term overlap
        kb_score = 5.0
        if context.knowledge_content:
            kb_terms = set()
            for c in context.knowledge_content:
                kb_terms.update(w.lower() for w in c.split() if len(w) > 5)
            if kb_terms:
                kb_overlap = sum(1 for t in kb_terms if t in reasoning_lower) / max(len(kb_terms), 1)
                kb_score = min(10.0, 5.0 + kb_overlap * 5.0)
        
        overall = round((length_score + relevance_score + kb_score) / 3, 1)
        
        return ReasoningScore(
            overall=overall,
            passed=overall >= self.PASS_THRESHOLD,
            kb_relevance=kb_score,
            coherence=length_score,
            addresses_question=relevance_score,
            feedback=f"Heuristic scoring (LLM unavailable). Length={word_count} words.",
            iteration=self._current_iteration,
        )
    
    def should_continue(self) -> bool:
        return self._current_iteration < self.MAX_ITERATIONS
    
    def get_latest_score(self) -> Optional[ReasoningScore]:
        return self._scoring_history[-1] if self._scoring_history else None
    
    def get_scoring_history(self) -> List[ReasoningScore]:
        return self._scoring_history.copy()
    
    def reset_iteration(self) -> None:
        self._current_iteration = 0
        self._scoring_history.clear()
    
    def get_improvement_summary(self) -> Dict[str, Any]:
        if not self._scoring_history:
            return {"iterations": 0, "improvement": 0.0}
        first_score = self._scoring_history[0].overall
        last_score = self._scoring_history[-1].overall
        return {
            "iterations": len(self._scoring_history),
            "first_score": first_score,
            "last_score": last_score,
            "improvement": last_score - first_score,
            "passed": self._scoring_history[-1].passed,
        }
