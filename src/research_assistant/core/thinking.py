"""
Thinking Module - Reasoning engine controlled by Controller.

Provides structured reasoning capabilities with hallucination prevention.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ReasoningType(Enum):
    """Types of reasoning."""
    DEDUCTIVE = "deductive"    # From general to specific
    INDUCTIVE = "inductive"    # From specific to general
    ANALYTICAL = "analytical"  # Breaking down complex problems
    SYNTHESIS = "synthesis"    # Combining information
    EVALUATIVE = "evaluative"  # Assessing quality/validity


@dataclass
class ThoughtStep:
    """Single step in reasoning chain."""
    step_number: int
    thought: str
    reasoning_type: ReasoningType
    grounded_in: List[str]  # Sources/evidence
    confidence: float  # 0-1
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ReasoningChain:
    """Complete reasoning chain."""
    question: str
    steps: List[ThoughtStep]
    conclusion: Optional[str] = None
    overall_confidence: float = 0.0
    is_valid: bool = False
    validation_notes: List[str] = field(default_factory=list)


class ThinkingModule:
    """
    Structured reasoning module.
    
    Features:
    - Step-by-step reasoning chains
    - Evidence grounding
    - Confidence scoring
    - Hallucination detection via grounding checks
    """
    
    def __init__(self):
        self._active_chain: Optional[ReasoningChain] = None
        self._history: List[ReasoningChain] = []
        
    def start_reasoning(self, question: str) -> ReasoningChain:
        """Start a new reasoning chain."""
        self._active_chain = ReasoningChain(question=question, steps=[])
        logger.info(f"[THINKING] Started reasoning: {question[:50]}...")
        return self._active_chain
    
    def add_thought(
        self,
        thought: str,
        reasoning_type: ReasoningType,
        grounded_in: List[str],
        confidence: float = 0.8,
    ) -> ThoughtStep:
        """Add a thought step to active chain."""
        if not self._active_chain:
            raise ValueError("No active reasoning chain")
        
        step = ThoughtStep(
            step_number=len(self._active_chain.steps) + 1,
            thought=thought,
            reasoning_type=reasoning_type,
            grounded_in=grounded_in,
            confidence=min(1.0, max(0.0, confidence)),
        )
        self._active_chain.steps.append(step)
        
        logger.debug(f"[THINKING] Step {step.step_number}: {thought[:50]}...")
        return step
    
    def conclude(self, conclusion: str) -> ReasoningChain:
        """Conclude the reasoning chain."""
        if not self._active_chain:
            raise ValueError("No active reasoning chain")
        
        self._active_chain.conclusion = conclusion
        self._active_chain.overall_confidence = self._calculate_confidence()
        
        self._history.append(self._active_chain)
        result = self._active_chain
        self._active_chain = None
        
        logger.info(f"[THINKING] Concluded with confidence {result.overall_confidence:.2f}")
        return result
    
    def _calculate_confidence(self) -> float:
        """Calculate overall confidence from steps."""
        if not self._active_chain or not self._active_chain.steps:
            return 0.0
        
        confidences = [s.confidence for s in self._active_chain.steps]
        # Multiplicative confidence decay
        result = 1.0
        for c in confidences:
            result *= c
        return result
    
    def validate_chain(self, chain: ReasoningChain) -> ReasoningChain:
        """Validate reasoning chain for logical consistency."""
        notes = []
        is_valid = True
        
        # Check grounding
        for step in chain.steps:
            if not step.grounded_in:
                notes.append(f"Step {step.step_number}: No evidence grounding")
                is_valid = False
            if step.confidence < 0.5:
                notes.append(f"Step {step.step_number}: Low confidence ({step.confidence})")
        
        # Check conclusion exists
        if not chain.conclusion:
            notes.append("Missing conclusion")
            is_valid = False
        
        chain.is_valid = is_valid
        chain.validation_notes = notes
        return chain
    
    def check_hallucination_risk(self, claim: str, evidence: List[str]) -> Dict[str, Any]:
        """Check if a claim might be hallucinated."""
        risk_level = "low"
        reasons = []
        
        if not evidence:
            risk_level = "high"
            reasons.append("No supporting evidence provided")
        elif len(evidence) < 2:
            risk_level = "medium"
            reasons.append("Limited evidence (single source)")
        
        # Check for speculative language
        speculative_words = ["might", "could", "possibly", "perhaps", "maybe"]
        if any(w in claim.lower() for w in speculative_words):
            reasons.append("Contains speculative language")
            if risk_level == "low":
                risk_level = "medium"
        
        return {
            "claim": claim,
            "risk_level": risk_level,
            "reasons": reasons,
            "evidence_count": len(evidence),
            "recommendation": "Verify with sources" if risk_level != "low" else "Acceptable",
        }
