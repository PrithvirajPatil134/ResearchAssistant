"""
Learner Agent - Learns from feedback and patterns.

Provides pattern-based warm start for reasoning:
- get_patterns(query) → returns similar past queries + what worked
- store_pattern(query, reasoning, score) → saves for future
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging

from .base import BaseAgent, AgentResult
from ..core.memory import MemoryType

logger = logging.getLogger(__name__)


@dataclass
class Learning:
    """A learned pattern or insight."""
    pattern_type: str  # "feedback", "style", "structure", "correction"
    description: str
    source: str  # Where this learning came from
    examples: List[str]
    confidence: float = 0.8
    times_applied: int = 0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ReasoningPattern:
    """A stored pattern of successful reasoning."""
    query: str  # Original query
    reasoning_summary: str  # Key points from successful reasoning
    score: float  # Score achieved (0-10)
    key_terms: List[str]  # Important terms for matching
    strategies: List[str]  # What worked well
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Suggestion:
    """Improvement suggestion based on learnings."""
    section: Optional[str]
    suggestion: str
    based_on: str  # Learning that generated this
    priority: int = 5  # 1-10


class LearnerAgent(BaseAgent):
    """
    Learns from interactions and feedback.
    
    Key responsibilities:
    - Capture patterns from successful outputs
    - Learn mentor preferences
    - Improve prompts based on feedback
    - Maintain knowledge base of learnings
    - Provide warm start patterns for new queries
    """
    
    def __init__(self, memory, context_guard):
        super().__init__("learner", memory, context_guard)
        self._learnings: List[Learning] = []
        self._mentor_preferences: Dict[str, Any] = {}
        self._reasoning_patterns: List[ReasoningPattern] = []
    
    def execute(self, **kwargs) -> AgentResult:
        """Main execution - learn from provided feedback."""
        feedback = kwargs.get("feedback")
        original = kwargs.get("original")
        context = kwargs.get("context", {})
        
        if feedback:
            learning = self.learn_from_feedback(feedback, original, context)
            return AgentResult(
                success=True,
                output=learning,
                tokens_used=100,
            )
        return AgentResult(success=False, output=None)
    
    def learn_from_feedback(
        self,
        feedback: str,
        original: Optional[str],
        context: Dict[str, Any],
    ) -> Learning:
        """Learn from feedback on content."""
        # Analyze feedback type
        pattern_type = self._classify_feedback(feedback)
        
        learning = Learning(
            pattern_type=pattern_type,
            description=f"From feedback: {feedback[:100]}",
            source=context.get("source", "mentor"),
            examples=[feedback],
        )
        
        self._learnings.append(learning)
        
        # Store in memory
        self.memory.store(
            key=f"learning:{len(self._learnings)}",
            value=learning.description,
            memory_type=MemoryType.LEARNING,
            source_agent=self.agent_id,
            importance=7,
        )
        
        self.log_operation("learn_from_feedback", 50)
        logger.info(f"[LEARNER] Learned pattern: {pattern_type}")
        
        return learning
    
    def _classify_feedback(self, feedback: str) -> str:
        """Classify feedback type."""
        lower = feedback.lower()
        if any(w in lower for w in ["structure", "organize", "flow", "order"]):
            return "structure"
        elif any(w in lower for w in ["style", "tone", "voice", "write"]):
            return "style"
        elif any(w in lower for w in ["wrong", "incorrect", "error", "fix"]):
            return "correction"
        return "feedback"
    
    def apply_learnings(
        self,
        task: Dict[str, Any],
        persona: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Apply learnings to enhance a task."""
        relevant = self._find_relevant_learnings(task, persona)
        
        enhanced_task = task.copy()
        enhanced_task["learnings_applied"] = [l.description for l in relevant]
        
        for learning in relevant:
            learning.times_applied += 1
        
        self.log_operation("apply_learnings", 30)
        return enhanced_task
    
    def _find_relevant_learnings(
        self,
        task: Dict[str, Any],
        persona: Optional[str],
    ) -> List[Learning]:
        """Find learnings relevant to current task."""
        # Simple relevance - return recent high-confidence learnings
        return sorted(
            self._learnings,
            key=lambda l: (l.confidence, l.times_applied),
            reverse=True,
        )[:5]
    
    def suggest_improvements(self, draft: str) -> List[Suggestion]:
        """Suggest improvements based on learnings."""
        suggestions = []
        
        for learning in self._learnings:
            if learning.pattern_type == "structure":
                suggestions.append(Suggestion(
                    section=None,
                    suggestion=f"Consider: {learning.description}",
                    based_on=learning.pattern_type,
                    priority=6,
                ))
        
        self.log_operation("suggest_improvements", 40)
        return suggestions
    
    def store_mentor_preference(self, key: str, preference: Any) -> None:
        """Store a mentor preference."""
        self._mentor_preferences[key] = preference
        self.memory.store(
            key=f"mentor_pref:{key}",
            value=preference,
            memory_type=MemoryType.FEEDBACK,
            source_agent=self.agent_id,
            importance=8,
        )
    
    def get_learnings_summary(self) -> Dict[str, Any]:
        """Get summary of all learnings."""
        by_type = {}
        for l in self._learnings:
            by_type.setdefault(l.pattern_type, []).append(l)
        
        return {
            "total": len(self._learnings),
            "by_type": {k: len(v) for k, v in by_type.items()},
            "mentor_preferences": len(self._mentor_preferences),
            "reasoning_patterns": len(self._reasoning_patterns),
        }
    
    # =========================================================================
    # Pattern-based Warm Start Methods
    # =========================================================================
    
    def get_patterns(self, query: str) -> Dict[str, Any]:
        """
        Get relevant patterns for a new query (warm start).
        
        Returns similar past queries and what strategies worked.
        """
        self.log_operation("get_patterns", 50)
        
        if not self._reasoning_patterns:
            return {
                "found": False,
                "similar_queries": [],
                "suggested_strategies": [],
                "warm_start_prompt": None,
            }
        
        # Extract key terms from query
        query_terms = self._extract_key_terms(query)
        
        # Find similar patterns
        similar = self._find_similar_patterns(query_terms, top_k=3)
        
        if not similar:
            return {
                "found": False,
                "similar_queries": [],
                "suggested_strategies": [],
                "warm_start_prompt": None,
            }
        
        # Aggregate strategies that worked
        all_strategies = []
        for pattern, similarity in similar:
            all_strategies.extend(pattern.strategies)
        
        # Deduplicate strategies
        unique_strategies = list(dict.fromkeys(all_strategies))[:5]
        
        # Build warm start prompt
        warm_start = self._build_warm_start_prompt(query, similar, unique_strategies)
        
        logger.info(f"[LEARNER] Found {len(similar)} similar patterns for query")
        
        return {
            "found": True,
            "similar_queries": [
                {
                    "query": p.query,
                    "score": p.score,
                    "similarity": sim,
                }
                for p, sim in similar
            ],
            "suggested_strategies": unique_strategies,
            "warm_start_prompt": warm_start,
        }
    
    def store_pattern(
        self,
        query: str,
        reasoning: str,
        score: float,
        feedback: Optional[str] = None,
    ) -> ReasoningPattern:
        """
        Store a successful reasoning pattern for future reference.
        
        Only stores patterns with score >= 8.0 (good quality).
        """
        self.log_operation("store_pattern", 30)
        
        # Only store good patterns
        if score < 8.0:
            logger.debug(f"[LEARNER] Score {score} too low to store pattern")
            return None
        
        # Extract key terms
        key_terms = self._extract_key_terms(query)
        
        # Extract strategies from reasoning
        strategies = self._extract_strategies(reasoning, feedback)
        
        # Create summary
        summary = self._summarize_reasoning(reasoning)
        
        pattern = ReasoningPattern(
            query=query,
            reasoning_summary=summary,
            score=score,
            key_terms=key_terms,
            strategies=strategies,
        )
        
        self._reasoning_patterns.append(pattern)
        
        # Also store in memory for persistence
        self.memory.store(
            key=f"pattern:{len(self._reasoning_patterns)}",
            value={
                "query": query,
                "summary": summary,
                "score": score,
                "strategies": strategies,
            },
            memory_type=MemoryType.LEARNING,
            source_agent=self.agent_id,
            importance=8,
        )
        
        logger.info(f"[LEARNER] Stored pattern with score {score}")
        
        return pattern
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract important terms from text for matching."""
        # Simple extraction - words > 4 chars, excluding common words
        stopwords = {
            "this", "that", "what", "when", "where", "which", "their",
            "there", "these", "those", "about", "would", "could", "should",
            "have", "been", "were", "will", "with", "from", "they", "them",
        }
        
        words = text.lower().split()
        terms = [
            w.strip('.,!?;:"\'()[]{}')
            for w in words
            if len(w) > 4 and w.lower() not in stopwords
        ]
        
        # Return unique terms
        return list(dict.fromkeys(terms))[:20]
    
    def _find_similar_patterns(
        self,
        query_terms: List[str],
        top_k: int = 3,
    ) -> List[Tuple["ReasoningPattern", float]]:
        """Find patterns similar to current query."""
        if not query_terms or not self._reasoning_patterns:
            return []
        
        scored_patterns = []
        query_set = set(query_terms)
        
        for pattern in self._reasoning_patterns:
            pattern_set = set(pattern.key_terms)
            
            # Calculate Jaccard similarity
            intersection = len(query_set & pattern_set)
            union = len(query_set | pattern_set)
            
            if union > 0:
                similarity = intersection / union
                if similarity > 0.1:  # Minimum threshold
                    scored_patterns.append((pattern, similarity))
        
        # Sort by similarity (descending) and score (descending)
        scored_patterns.sort(key=lambda x: (x[1], x[0].score), reverse=True)
        
        return scored_patterns[:top_k]
    
    def _extract_strategies(
        self,
        reasoning: str,
        feedback: Optional[str] = None,
    ) -> List[str]:
        """Extract effective strategies from reasoning."""
        strategies = []
        reasoning_lower = reasoning.lower()
        
        # Check for structural patterns that indicate good strategies
        if "##" in reasoning or "###" in reasoning:
            strategies.append("Use clear section headers")
        
        if "1." in reasoning or "2." in reasoning:
            strategies.append("Use numbered steps or lists")
        
        if "framework" in reasoning_lower:
            strategies.append("Reference theoretical frameworks")
        
        if "example" in reasoning_lower or "for instance" in reasoning_lower:
            strategies.append("Include concrete examples")
        
        if "according to" in reasoning_lower or "research shows" in reasoning_lower:
            strategies.append("Cite sources and evidence")
        
        if "therefore" in reasoning_lower or "thus" in reasoning_lower:
            strategies.append("Use clear logical transitions")
        
        if "in conclusion" in reasoning_lower or "to summarize" in reasoning_lower:
            strategies.append("Include clear conclusion")
        
        # Extract strategies from feedback if available
        if feedback:
            if "grounding" in feedback.lower():
                strategies.append("Strengthen knowledge base grounding")
            if "structure" in feedback.lower():
                strategies.append("Improve organizational structure")
        
        return list(dict.fromkeys(strategies))[:5]  # Unique, max 5
    
    def _summarize_reasoning(self, reasoning: str) -> str:
        """Create a brief summary of reasoning for storage."""
        # Extract first substantial paragraph or section
        paragraphs = [p.strip() for p in reasoning.split('\n\n') if p.strip()]
        
        if not paragraphs:
            return reasoning[:200]
        
        # Find first content paragraph (skip title-like lines)
        for para in paragraphs[:3]:
            if len(para) > 100 and not para.startswith('#'):
                return para[:300] + "..." if len(para) > 300 else para
        
        return paragraphs[0][:200]
    
    def _build_warm_start_prompt(
        self,
        query: str,
        similar_patterns: List[Tuple["ReasoningPattern", float]],
        strategies: List[str],
    ) -> str:
        """Build a warm start prompt based on similar patterns."""
        prompt_parts = [
            f"For the query: '{query}'",
            "",
            "Based on similar past reasoning patterns that scored well:",
        ]
        
        # Add similar query info
        for pattern, similarity in similar_patterns[:2]:
            prompt_parts.append(
                f"- Similar query (score {pattern.score}): {pattern.query[:80]}..."
            )
        
        # Add strategies
        if strategies:
            prompt_parts.append("")
            prompt_parts.append("Recommended strategies:")
            for strategy in strategies:
                prompt_parts.append(f"  • {strategy}")
        
        return "\n".join(prompt_parts)
    
    def get_patterns_summary(self) -> Dict[str, Any]:
        """Get summary of stored patterns."""
        if not self._reasoning_patterns:
            return {
                "total_patterns": 0,
                "average_score": 0.0,
                "common_strategies": [],
            }
        
        scores = [p.score for p in self._reasoning_patterns]
        all_strategies = []
        for p in self._reasoning_patterns:
            all_strategies.extend(p.strategies)
        
        # Count strategy frequency
        strategy_counts = {}
        for s in all_strategies:
            strategy_counts[s] = strategy_counts.get(s, 0) + 1
        
        common = sorted(strategy_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_patterns": len(self._reasoning_patterns),
            "average_score": sum(scores) / len(scores),
            "common_strategies": [s for s, _ in common],
        }
