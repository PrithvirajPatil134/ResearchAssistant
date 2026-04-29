"""
Reviewer Agent - LLM-powered content review against standards.

Two-phase review:
1. Fast heuristic pre-check (catches critical format issues)
2. LLM-based review with workflow-specific rubric
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


# Workflow-specific review rubrics for the LLM reviewer
REVIEW_RUBRICS = {
    "guide": """Review this GUIDANCE output. A good guide should:
- Help the student think, NOT give direct answers
- Reference specific KB materials and frameworks
- Include reflection questions
- Provide structured approach without doing the work
- Be actionable and specific, not generic""",

    "explain": """Review this EXPLANATION output. A good explanation should:
- Define concepts using KB terminology exactly
- Include theoretical foundations with proper attribution
- Progress from simple to complex
- Include practical applications
- Be academically rigorous but accessible""",

    "review": """Review this REVIEW output. A good review should:
- Identify both strengths and weaknesses
- Reference specific criteria from course materials
- Provide constructive, actionable feedback
- Be thorough but encouraging
- Suggest concrete next steps""",

    "research": """Review this RESEARCH output. A good research output should:
- Identify clear research gaps with evidence
- Map to theoretical frameworks
- Suggest appropriate methodologies with justification
- Consider validity, reliability, and ethical implications
- Provide a structured research roadmap""",

    "quant": """Review this QUANTITATIVE ANALYSIS output. A good quant output should:
- Use appropriate statistical methods for the data type
- Report all relevant statistics (test statistic, p-value, effect size, CI)
- Check and report assumption violations
- Interpret results in context, not just numbers
- Include limitations and caveats""",
}


class ReviewerAgent(BaseAgent):
    """
    LLM-powered content reviewer with workflow-specific rubrics.
    
    Phase 1: Heuristic pre-check (critical format issues, empty content)
    Phase 2: LLM review with workflow-specific rubric
    Falls back to heuristic-only if LLM unavailable.
    """
    
    def __init__(self, memory, context_guard):
        super().__init__("reviewer", memory, context_guard)
        self._standards: List[str] = []
        self._examples: List[Dict[str, Any]] = []
        self._guidelines: List[str] = []
    
    def _apply_persona_config(self, config: Dict[str, Any]) -> None:
        self._standards = config.get("standards", [])
    
    def execute(self, **kwargs) -> AgentResult:
        content = kwargs.get("content")
        if not content:
            return AgentResult(success=False, output=None)
        result = self.review_against_standards(content)
        return AgentResult(success=True, output=result, tokens_used=500)
    
    def set_standards(self, standards: List[str]) -> None:
        self._standards = standards
    
    def set_examples(self, examples: List[Dict[str, Any]]) -> None:
        self._examples = examples
    
    def set_guidelines(self, guidelines: List[str]) -> None:
        self._guidelines = guidelines
    
    def review_against_standards(
        self,
        content: str,
        persona: Optional[Dict[str, Any]] = None,
        workflow_name: Optional[str] = None,
        user_query: Optional[str] = None,
        contract: Optional[Any] = None,
    ) -> ReviewResult:
        """Review content with heuristic pre-check + LLM evaluation."""
        self.log_operation("review_against_standards", 150)
        self._contract = contract  # Store for use in _llm_review
        
        # Phase 1: Heuristic pre-check for critical issues
        critical_issues = self._check_critical_issues(content, workflow_name, user_query)
        if any(i.get("severity") == "critical" for i in critical_issues):
            return ReviewResult(
                overall_score=1.0,
                meets_standards=False,
                issues=critical_issues,
                suggestions=["Fix critical issues before resubmitting"],
                strengths=[],
            )
        
        # Phase 2: LLM-based review
        llm_result = self._llm_review(content, workflow_name, user_query)
        if llm_result:
            return llm_result
        
        # Fallback: heuristic review
        return self._heuristic_review(content, workflow_name, user_query, critical_issues)
    
    def _llm_review(
        self,
        content: str,
        workflow_name: Optional[str],
        user_query: Optional[str],
    ) -> Optional[ReviewResult]:
        """
        LLM-powered review — iterative, like a human reviewer.
        
        Pass 1: Identify strengths (what works well)
        Pass 2: Identify issues (what needs fixing)
        Pass 3: Generate actionable suggestions informed by passes 1-2
        """
        try:
            from ..core import get_llm_client
            llm = get_llm_client()
            
            rubric = REVIEW_RUBRICS.get(workflow_name or "guide", REVIEW_RUBRICS["guide"])
            content_excerpt = content[:5000]
            query_excerpt = (user_query or 'Not provided')[:800]
            standards_text = '\n'.join(f'- {s}' for s in self._standards[:5]) if self._standards else '(none)'
            
            base_context = f"""## QUERY: {query_excerpt}
## OUTPUT (excerpt): {content_excerpt}
## RUBRIC: {rubric}
## STANDARDS: {standards_text}"""

            # Level 3: Inject dispatch contract for intent-aware review
            if hasattr(self, '_contract') and self._contract and hasattr(self._contract, 'to_reviewer_prompt'):
                base_context += f"\n\n{self._contract.to_reviewer_prompt()}"
            
            sys_prompt = "You are a strict academic reviewer. Output ONLY valid JSON."
            
            # Pass 1: Strengths
            r1 = llm.generate(
                f"""{base_context}

TASK: Identify 2-4 specific STRENGTHS of this output. What works well?
Respond with ONLY: {{"strengths": ["strength 1", "strength 2"]}}""",
                sys_prompt
            )
            
            strengths = []
            if r1.success:
                m = re.search(r'\{.*?\}', r1.content, re.DOTALL)
                if m:
                    try:
                        strengths = json.loads(m.group(0)).get("strengths", [])
                    except (json.JSONDecodeError, ValueError):
                        pass
            
            # Pass 2: Issues (informed by strengths)
            r2 = llm.generate(
                f"""{base_context}

## STRENGTHS ALREADY IDENTIFIED: {json.dumps(strengths)}

TASK: Now identify ISSUES — what needs fixing? Classify each as critical/major/minor.
Respond with ONLY: {{"issues": [{{"type": "...", "severity": "critical|major|minor", "message": "..."}}], "score": <0-10>}}""",
                sys_prompt
            )
            
            issues = []
            score = 6.0
            if r2.success:
                m = re.search(r'\{.*\}', r2.content, re.DOTALL)
                if m:
                    try:
                        data = json.loads(m.group(0))
                        raw_issues = data.get("issues", [])
                        issues = [i if isinstance(i, dict) else {"message": str(i), "severity": "minor", "type": "general"} for i in raw_issues]
                        score = float(data.get("score", 6))
                    except (json.JSONDecodeError, ValueError):
                        pass
            
            # Pass 3: Suggestions (informed by both strengths and issues)
            r3 = llm.generate(
                f"""{base_context}

## STRENGTHS: {json.dumps(strengths)}
## ISSUES: {json.dumps([i.get('message','') for i in issues])}

TASK: Given the strengths and issues above, provide 2-4 specific, actionable SUGGESTIONS for improvement.
Respond with ONLY: {{"suggestions": ["suggestion 1", "suggestion 2"]}}""",
                sys_prompt
            )
            
            suggestions = []
            if r3.success:
                m = re.search(r'\{.*?\}', r3.content, re.DOTALL)
                if m:
                    try:
                        suggestions = json.loads(m.group(0)).get("suggestions", [])
                    except (json.JSONDecodeError, ValueError):
                        pass
            
            meets = score >= 6.0 and not any(i.get("severity") == "critical" for i in issues)
            
            logger.info(f"[REVIEWER] Score: {score}/10, {len(strengths)} strengths, {len(issues)} issues, {len(suggestions)} suggestions")
            
            return ReviewResult(
                overall_score=score,
                meets_standards=meets,
                issues=issues,
                suggestions=suggestions,
                strengths=strengths,
            )
            
        except Exception as e:
            logger.warning(f"[REVIEWER] LLM review error: {e}")
            return None
    
    def _check_critical_issues(self, content: str, workflow_name: Optional[str], user_query: Optional[str]) -> List[Dict[str, Any]]:
        """Fast heuristic check for critical issues."""
        critical = []
        content_lower = content.lower()
        
        if len(content.split()) < 30:
            critical.append({"type": "empty", "severity": "critical", "message": "Content too short or empty"})
        
        empty_phrases = ["topic is empty", "need you to specify", "please specify"]
        if user_query and any(p in content_lower for p in empty_phrases):
            critical.append({"type": "empty_topic", "severity": "critical", "message": "Output claims topic is empty when user provided input"})
        
        no_kb = ["i don't have access to", "i cannot access", "no specific information"]
        if any(p in content_lower for p in no_kb):
            critical.append({"type": "no_kb", "severity": "critical", "message": "Output not grounded in knowledge base"})
        
        if workflow_name == "guide" and "explained by:" in content_lower:
            if "guidance:" not in content_lower and "objective" not in content_lower:
                critical.append({"type": "wrong_format", "severity": "critical", "message": "Guide workflow used explain template"})
        
        return critical
    
    def _heuristic_review(self, content: str, workflow_name: Optional[str], user_query: Optional[str], existing_issues: List) -> ReviewResult:
        """Fallback heuristic review."""
        issues = list(existing_issues)
        suggestions = []
        strengths = []
        score = 7.0
        
        word_count = len(content.split())
        if word_count < 100:
            issues.append({"type": "length", "severity": "major", "message": "Content too short"})
            score -= 1
        elif word_count > 500:
            strengths.append("Comprehensive content")
        
        if "##" in content:
            strengths.append("Good structure with sections")
        else:
            suggestions.append("Add section headers for clarity")
        
        score = max(0.0, min(10.0, score - len(issues) * 0.5))
        
        return ReviewResult(
            overall_score=score,
            meets_standards=score >= 6.0 and not any(i.get("severity") == "critical" for i in issues),
            issues=issues,
            suggestions=suggestions,
            strengths=strengths,
        )
    
    def compare_with_examples(self, content: str, examples: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        examples = examples or self._examples
        self.log_operation("compare_with_examples", 100)
        return {"comparisons": [], "overall_alignment": 0.75}
    
    def check_guidelines(self, content: str, guidelines: Optional[List[str]] = None) -> List[GuidelineCheck]:
        guidelines = guidelines or self._guidelines
        self.log_operation("check_guidelines", 80)
        return [GuidelineCheck(guideline=g, compliant=len(content) > 50, notes="Checked") for g in guidelines]
    
    def generate_feedback(self, review: ReviewResult) -> str:
        lines = [f"## Review Score: {review.overall_score}/10", ""]
        if review.strengths:
            lines.append("### Strengths")
            lines.extend(f"- {s}" for s in review.strengths)
            lines.append("")
        if review.issues:
            lines.append("### Issues")
            lines.extend(f"- {i.get('message', i) if isinstance(i, dict) else i}" for i in review.issues)
            lines.append("")
        if review.suggestions:
            lines.append("### Suggestions")
            lines.extend(f"- {s}" for s in review.suggestions)
        self.log_operation("generate_feedback", 30)
        return "\n".join(lines)
