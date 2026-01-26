"""
Research Assistant - An AI-powered research workflow automation package.

Multi-agent architecture for:
- Case studies
- Teaching notes
- Research papers
- Literature reviews

Core Agents:
- Controller: Orchestrates thinking, prevents hallucination
- ContextGuard: Monitors tokens, manages context at 70% threshold
- Learner: Learns from feedback and patterns
- Reviewer: Validates against standards and examples
"""

__version__ = "0.1.0"
__author__ = "propatil"

from .config import Config
from .personas import PersonaLoader, Persona
from .workflows import WorkflowInvoker, WorkflowSpec, WorkflowResult

__all__ = [
    "Config",
    "PersonaLoader",
    "Persona",
    "WorkflowInvoker",
    "WorkflowSpec",
    "WorkflowResult",
]
