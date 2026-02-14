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

Spaces (previously Personas):
- DBA: Prof. Cardasso's DBA research methods
- CW: Prof. Kakoli Sen's case writing
- QNTR: Prof. Atul Prashar's quantitative research
"""

__version__ = "0.1.0"
__author__ = "propatil"

from .config import Config
from .spaces import SpaceLoader, PersonaLoader, Persona  # PersonaLoader is alias for SpaceLoader
from .workflows import WorkflowInvoker, WorkflowSpec, WorkflowResult

__all__ = [
    "Config",
    "SpaceLoader",
    "PersonaLoader",  # Backward compatibility alias
    "Persona",
    "WorkflowInvoker",
    "WorkflowSpec",
    "WorkflowResult",
]
