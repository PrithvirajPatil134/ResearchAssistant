"""
Specialized agents for Research Assistant.

- BaseAgent: Abstract base class for all agents
- LearnerAgent: Learns from feedback and patterns
- ReviewerAgent: Reviews against standards and examples
- ReaderAgent: Extracts content from knowledge base files
- AnalystAgent: Scores reasoning quality
"""

from .base import BaseAgent, AgentResult
from .learner import LearnerAgent, Learning, ReasoningPattern, Suggestion
from .reviewer import ReviewerAgent
from .reader import ReaderAgent, ExtractedContent
from .analyst import AnalystAgent, ReasoningScore, AnalysisContext

__all__ = [
    # Base
    "BaseAgent",
    "AgentResult",
    # Learner
    "LearnerAgent",
    "Learning",
    "ReasoningPattern",
    "Suggestion",
    # Reviewer
    "ReviewerAgent",
    # Reader
    "ReaderAgent",
    "ExtractedContent",
    # Analyst
    "AnalystAgent",
    "ReasoningScore",
    "AnalysisContext",
]
