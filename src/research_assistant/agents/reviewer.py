"""
Reviewer Agent - Reviews content against standards and examples.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from .base import BaseAgent, AgentResult

logger = logging.getLogger(__name__)


@dataclass
class ReviewResult:
    """Result of content review."""
    overall_score: float  # 0-10
    meets_standards: bool
    issues: List[Dict[str, Any]]
    suggestions: List[str]
    strengths: List[str]


@dataclass
class GuidelineCheck:
    """Result of guideline compliance check."""
    guideline: str
    compliant: bool
    notes: str


class ReviewerAgent(BaseAgent):
    """
    Reviews outputs against standards and guidelines.
    
    Key responsibilities:
    - Validate against industry standards
    - Compare with provided examples
    - Check adherence to persona guidelines
    - Provide structured feedback
    """
    
    def __init__(self, memory, context_guard):
        super().__init__("reviewer", memory, context_guard)
        self._standards: List[str] = []
        self._examples: List[Dict[str, Any]] = []
        self._guidelines: List[str] = []
    
    def _apply_persona_config(self, config: Dict[str, Any]) -> None:
        """Apply persona-specific review standards."""
        self._standards = config.get("standards", [])
    
    def execute(self, **kwargs) -> AgentResult:
        """Main execution - review content."""
        content = kwargs.get("content")
        if not content:
            return AgentResult(success=False, output=None)
        
        result = self.review_against_standards(content)
        return AgentResult(success=True, output=result, tokens_used=200)
    
    def set_standards(self, standards: List[str]) -> None:
        """Set review standards."""
        self._standards = standards
    
    def set_examples(self, examples: List[Dict[str, Any]]) -> None:
        """Set reference examples."""
        self._examples = examples
    
    def set_guidelines(self, guidelines: List[str]) -> None:
        """Set guidelines to check."""
        self._guidelines = guidelines
    
    def review_against_standards(
        self,
        content: str,
        persona: Optional[Dict[str, Any]] = None,
    ) -> ReviewResult:
        """Review content against configured standards."""
        issues = []
        suggestions = []
        strengths = []
        score = 7.0  # Base score
        
        # Check length
        word_count = len(content.split())
        if word_count < 100:
            issues.append({"type": "length", "message": "Content too short"})
            score -= 1
        elif word_count > 500:
            strengths.append("Comprehensive content")
        
        # Check structure
        if "##" in content or content.count("\n\n") > 2:
            strengths.append("Good structure with sections")
        else:
            suggestions.append("Consider adding section headers")
        
        # Check standards compliance
        for standard in self._standards:
            # Simple keyword check - would use AI in production
            if standard.lower() not in content.lower():
                suggestions.append(f"Address: {standard}")
        
        meets_standards = score >= 6.0 and len(issues) == 0
        
        self.log_operation("review_against_standards", 150)
        
        return ReviewResult(
            overall_score=score,
            meets_standards=meets_standards,
            issues=issues,
            suggestions=suggestions,
            strengths=strengths,
        )
    
    def compare_with_examples(
        self,
        content: str,
        examples: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Compare content with reference examples."""
        examples = examples or self._examples
        
        comparisons = []
        for ex in examples[:3]:  # Limit to 3 examples
            comparisons.append({
                "example": ex.get("name", "Example"),
                "similarity": 0.7,  # Placeholder
                "notes": "Structure comparison",
            })
        
        self.log_operation("compare_with_examples", 100)
        
        return {
            "comparisons": comparisons,
            "overall_alignment": 0.75,
        }
    
    def check_guidelines(
        self,
        content: str,
        guidelines: Optional[List[str]] = None,
    ) -> List[GuidelineCheck]:
        """Check content against guidelines."""
        guidelines = guidelines or self._guidelines
        checks = []
        
        for guideline in guidelines:
            # Simple check - would use AI in production
            compliant = len(content) > 50
            checks.append(GuidelineCheck(
                guideline=guideline,
                compliant=compliant,
                notes="Checked" if compliant else "Review needed",
            ))
        
        self.log_operation("check_guidelines", 80)
        return checks
    
    def generate_feedback(self, review: ReviewResult) -> str:
        """Generate human-readable feedback from review."""
        lines = [f"## Review Score: {review.overall_score}/10", ""]
        
        if review.strengths:
            lines.append("### Strengths")
            for s in review.strengths:
                lines.append(f"- {s}")
            lines.append("")
        
        if review.issues:
            lines.append("### Issues")
            for i in review.issues:
                lines.append(f"- {i['message']}")
            lines.append("")
        
        if review.suggestions:
            lines.append("### Suggestions")
            for s in review.suggestions:
                lines.append(f"- {s}")
        
        self.log_operation("generate_feedback", 30)
        return "\n".join(lines)
