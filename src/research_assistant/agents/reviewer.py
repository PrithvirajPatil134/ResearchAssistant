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
        workflow_name: Optional[str] = None,
        user_query: Optional[str] = None,
    ) -> ReviewResult:
        """Review content against configured standards and workflow-specific criteria."""
        issues = []
        suggestions = []
        strengths = []
        score = 7.0  # Base score
        
        # CRITICAL: Check for workflow-specific issues (auto-fail conditions)
        critical_issues = self._check_critical_issues(content, workflow_name, user_query)
        for issue in critical_issues:
            issues.append(issue)
            score -= 3.0  # Critical issues heavily penalize score
        
        # Check workflow-specific format
        if workflow_name:
            workflow_issues, workflow_strengths = self._validate_workflow_format(
                content, workflow_name, user_query
            )
            issues.extend(workflow_issues)
            strengths.extend(workflow_strengths)
            if workflow_issues:
                score -= len(workflow_issues) * 0.5
        
        # Check length
        word_count = len(content.split())
        if word_count < 100:
            issues.append({"type": "length", "severity": "major", "message": "Content too short"})
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
        
        # Cap score at 0-10 range
        score = max(0.0, min(10.0, score))
        meets_standards = score >= 6.0 and not any(i.get("severity") == "critical" for i in issues)
        
        self.log_operation("review_against_standards", 150)
        
        return ReviewResult(
            overall_score=score,
            meets_standards=meets_standards,
            issues=issues,
            suggestions=suggestions,
            strengths=strengths,
        )
    
    def _check_critical_issues(
        self,
        content: str,
        workflow_name: Optional[str],
        user_query: Optional[str],
    ) -> List[Dict[str, Any]]:
        """Check for critical issues that should auto-fail the review."""
        critical_issues = []
        content_lower = content.lower()
        
        # Critical Issue 1: Empty topic response when user provided input
        empty_topic_phrases = [
            "topic is empty",
            "topic field is empty",
            "topic required",
            "need you to specify",
            "please specify what",
            "awaiting topic selection",
        ]
        if user_query and any(phrase in content_lower for phrase in empty_topic_phrases):
            critical_issues.append({
                "type": "empty_topic_response",
                "severity": "critical",
                "message": "Output claims 'topic is empty' when user provided input",
            })
        
        # Critical Issue 2: Wrong workflow format (explain template for guide, etc.)
        if workflow_name == "guide":
            # Guide should NOT use explain-style headers for concept explanation
            if "explained by:" in content_lower and "prof." in content_lower:
                if "guidance:" not in content_lower and "objective" not in content_lower:
                    critical_issues.append({
                        "type": "wrong_workflow_format",
                        "severity": "critical",
                        "message": "Guide workflow used explain template format",
                    })
        
        # Critical Issue 3: No KB grounding
        generic_phrases = [
            "i don't have access to",
            "i cannot access",
            "no specific information",
        ]
        if any(phrase in content_lower for phrase in generic_phrases):
            critical_issues.append({
                "type": "no_kb_grounding",
                "severity": "critical",
                "message": "Output not grounded in knowledge base materials",
            })
        
        return critical_issues
    
    def _validate_workflow_format(
        self,
        content: str,
        workflow_name: str,
        user_query: Optional[str],
    ) -> tuple:
        """Validate content matches expected workflow format."""
        issues = []
        strengths = []
        content_lower = content.lower()
        query_lower = (user_query or "").lower()
        
        if workflow_name == "explain":
            # Explain should have educational structure
            if "##" in content and ("definition" in content_lower or "concept" in content_lower):
                strengths.append("Proper explain format with sections")
            
        elif workflow_name == "guide":
            # Check if objective generation request
            objective_triggers = ["objective", "generate objective", "create objective", "thesis objective"]
            is_objective_request = any(t in query_lower for t in objective_triggers)
            
            if is_objective_request:
                # Must have objective-specific format
                if "the objective of this research is to" in content_lower:
                    strengths.append("Follows Prof. Cardasso objective format")
                else:
                    issues.append({
                        "type": "missing_objective_format",
                        "severity": "major",
                        "message": "Objective should start with 'The objective of this research is to...'",
                    })
                
                if "business context" in content_lower:
                    strengths.append("Includes business context section")
                else:
                    issues.append({
                        "type": "missing_business_context",
                        "severity": "major",
                        "message": "Objective missing Business Context section",
                    })
            
            # General guide checks
            if "reflection question" in content_lower or "framework" in content_lower:
                strengths.append("Includes guiding elements")
        
        elif workflow_name == "review":
            if "strength" in content_lower and "weakness" in content_lower:
                strengths.append("Proper review format with strengths/weaknesses")
            elif "suggestion" in content_lower or "improve" in content_lower:
                strengths.append("Provides improvement guidance")
        
        elif workflow_name == "research":
            if "gap" in content_lower or "source" in content_lower:
                strengths.append("Identifies research gaps/sources")
        
        return issues, strengths
    
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
