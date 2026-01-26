"""
Analyst Agent - Scores reasoning quality against knowledge base.

Evaluates reasoning chains for:
- KB relevance (40%)
- Coherence (30%)  
- Addresses question (30%)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from .base import BaseAgent, AgentResult

logger = logging.getLogger(__name__)


@dataclass
class ReasoningScore:
    """Score for a reasoning chain."""
    overall: float  # 0-10 scale
    passed: bool  # True if overall >= 9.0
    kb_relevance: float  # 0-10: How well grounded in knowledge base
    coherence: float  # 0-10: Logical flow and consistency
    addresses_question: float  # 0-10: How well it answers the query
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


class AnalystAgent(BaseAgent):
    """
    Scores reasoning quality against standards.
    
    Scoring weights:
    - KB Relevance: 40% - Is reasoning grounded in knowledge base?
    - Coherence: 30% - Is the logic consistent and well-structured?
    - Addresses Question: 30% - Does it actually answer what was asked?
    
    Threshold: >= 9.0 to pass
    Max iterations: 5
    """
    
    PASS_THRESHOLD = 9.0
    MAX_ITERATIONS = 5
    
    # Scoring weights
    WEIGHT_KB_RELEVANCE = 0.40
    WEIGHT_COHERENCE = 0.30
    WEIGHT_ADDRESSES_QUESTION = 0.30
    
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
        
        self._current_iteration = iteration
        
        context = AnalysisContext(
            query=query,
            reasoning=reasoning,
            knowledge_content=knowledge_content,
            persona_context=self._persona_context,
        )
        
        score = self.score_reasoning(context)
        
        return AgentResult(
            success=True,
            output=score,
            tokens_used=200,
            metadata={
                "passed": score.passed,
                "overall_score": score.overall,
                "iteration": iteration,
            }
        )
    
    def score_reasoning(self, context: AnalysisContext) -> ReasoningScore:
        """
        Score reasoning chain against quality criteria.
        
        Returns ReasoningScore with overall score and component scores.
        """
        self.log_operation("score_reasoning", 150)
        
        # Calculate component scores
        kb_score = self._score_kb_relevance(context.reasoning, context.knowledge_content)
        coherence_score = self._score_coherence(context.reasoning)
        addresses_score = self._score_addresses_question(context.query, context.reasoning)
        
        # Calculate weighted overall score
        overall = (
            kb_score * self.WEIGHT_KB_RELEVANCE +
            coherence_score * self.WEIGHT_COHERENCE +
            addresses_score * self.WEIGHT_ADDRESSES_QUESTION
        )
        
        # Round to 1 decimal place
        overall = round(overall, 1)
        
        # Generate feedback
        feedback = self._generate_feedback(kb_score, coherence_score, addresses_score, context)
        
        score = ReasoningScore(
            overall=overall,
            passed=overall >= self.PASS_THRESHOLD,
            kb_relevance=kb_score,
            coherence=coherence_score,
            addresses_question=addresses_score,
            feedback=feedback,
            iteration=self._current_iteration,
        )
        
        self._scoring_history.append(score)
        
        logger.info(
            f"[ANALYST] Score: {overall}/10 (KB:{kb_score}, Coh:{coherence_score}, Addr:{addresses_score}) "
            f"- {'PASS' if score.passed else 'NEEDS IMPROVEMENT'}"
        )
        
        return score
    
    def _score_kb_relevance(self, reasoning: str, knowledge_content: List[str]) -> float:
        """
        Score how well reasoning is grounded in knowledge base.
        
        Checks:
        - References to source materials
        - Use of specific concepts from KB
        - Proper citation/attribution
        """
        if not reasoning:
            return 0.0
        
        reasoning_lower = reasoning.lower()
        score = 5.0  # Base score
        
        # Check for knowledge base references
        if knowledge_content:
            kb_terms = set()
            for content in knowledge_content:
                # Extract significant terms from KB content
                words = content.lower().split()
                kb_terms.update(w for w in words if len(w) > 4)
            
            # Count how many KB terms appear in reasoning
            matches = sum(1 for term in kb_terms if term in reasoning_lower)
            term_ratio = min(1.0, matches / max(len(kb_terms), 1))
            score += term_ratio * 3.0  # Up to +3 for term matches
        
        # Check for citation indicators
        citation_indicators = [
            "according to", "based on", "from the", "course material",
            "professor", "research shows", "literature", "study",
            "framework", "model", "theory", "source"
        ]
        citation_count = sum(1 for ind in citation_indicators if ind in reasoning_lower)
        score += min(2.0, citation_count * 0.5)  # Up to +2 for citations
        
        return min(10.0, max(0.0, score))
    
    def _score_coherence(self, reasoning: str) -> float:
        """
        Score logical coherence and structure.
        
        Checks:
        - Logical flow
        - Structured organization
        - Clear progression
        """
        if not reasoning:
            return 0.0
        
        score = 5.0  # Base score
        
        # Check for structural elements
        structure_indicators = [
            ("##", 1.0),  # Headers
            ("1.", 0.5), ("2.", 0.5), ("3.", 0.5),  # Numbered lists
            ("-", 0.3), ("•", 0.3),  # Bullet points
            ("first", 0.5), ("second", 0.5), ("third", 0.5),
            ("therefore", 0.5), ("thus", 0.5), ("hence", 0.5),
            ("because", 0.3), ("since", 0.3),
            ("in conclusion", 0.5), ("to summarize", 0.5),
        ]
        
        reasoning_lower = reasoning.lower()
        for indicator, value in structure_indicators:
            if indicator.lower() in reasoning_lower:
                score += value
        
        # Check for length (too short = incomplete, reasonable length = good)
        word_count = len(reasoning.split())
        if word_count < 50:
            score -= 2.0  # Too short
        elif word_count >= 100:
            score += 1.0  # Good length
        if word_count >= 200:
            score += 0.5  # Comprehensive
        
        # Check for paragraph structure
        paragraphs = [p for p in reasoning.split('\n\n') if p.strip()]
        if len(paragraphs) >= 3:
            score += 1.0  # Good paragraph structure
        
        return min(10.0, max(0.0, score))
    
    def _score_addresses_question(self, query: str, reasoning: str) -> float:
        """
        Score how well reasoning addresses the original question.
        
        Checks:
        - Query terms in response
        - Direct addressing of question
        - Completeness of answer
        """
        if not reasoning or not query:
            return 0.0
        
        score = 5.0  # Base score
        
        query_lower = query.lower()
        reasoning_lower = reasoning.lower()
        
        # Extract key terms from query
        query_terms = [t for t in query_lower.split() if len(t) > 3]
        
        # Check if query terms appear in reasoning
        term_matches = sum(1 for term in query_terms if term in reasoning_lower)
        if query_terms:
            match_ratio = term_matches / len(query_terms)
            score += match_ratio * 3.0  # Up to +3 for term coverage
        
        # Check for direct addressing
        direct_indicators = [
            f"about {query_lower[:20]}" if len(query_lower) > 20 else query_lower,
            "this means", "this refers to", "defined as",
            "the answer", "in response", "to address",
        ]
        
        for indicator in direct_indicators:
            if indicator in reasoning_lower:
                score += 0.5
        
        # Bonus for comprehensive coverage
        if len(reasoning) > 500 and term_matches >= len(query_terms) * 0.7:
            score += 1.0
        
        return min(10.0, max(0.0, score))
    
    def _generate_feedback(
        self,
        kb_score: float,
        coherence_score: float,
        addresses_score: float,
        context: AnalysisContext,
    ) -> str:
        """Generate specific improvement feedback."""
        feedback_parts = []
        
        # KB relevance feedback
        if kb_score < 7.0:
            feedback_parts.append(
                "GROUNDING: Strengthen connection to knowledge base materials. "
                "Include specific references to course concepts, frameworks, or readings."
            )
        elif kb_score < 9.0:
            feedback_parts.append(
                "GROUNDING: Good foundation. Add more specific citations or examples from source materials."
            )
        
        # Coherence feedback
        if coherence_score < 7.0:
            feedback_parts.append(
                "STRUCTURE: Improve logical flow. Use headers, numbered steps, or clear transitions. "
                "Ensure each point builds on the previous."
            )
        elif coherence_score < 9.0:
            feedback_parts.append(
                "STRUCTURE: Good organization. Consider adding a summary or clearer conclusion."
            )
        
        # Addresses question feedback
        if addresses_score < 7.0:
            feedback_parts.append(
                f"RELEVANCE: Response doesn't fully address the question '{context.query[:50]}...'. "
                "Directly answer what was asked before expanding."
            )
        elif addresses_score < 9.0:
            feedback_parts.append(
                "RELEVANCE: Good coverage. Ensure all aspects of the question are addressed."
            )
        
        if not feedback_parts:
            return "Excellent reasoning quality. No improvements needed."
        
        return " | ".join(feedback_parts)
    
    def should_continue(self) -> bool:
        """Check if more iterations are allowed."""
        return self._current_iteration < self.MAX_ITERATIONS
    
    def get_latest_score(self) -> Optional[ReasoningScore]:
        """Get the most recent score."""
        return self._scoring_history[-1] if self._scoring_history else None
    
    def get_scoring_history(self) -> List[ReasoningScore]:
        """Get all scores from this session."""
        return self._scoring_history.copy()
    
    def reset_iteration(self) -> None:
        """Reset iteration counter for new reasoning chain."""
        self._current_iteration = 0
        self._scoring_history.clear()
    
    def get_improvement_summary(self) -> Dict[str, Any]:
        """Get summary of score progression."""
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
