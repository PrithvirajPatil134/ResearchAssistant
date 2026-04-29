"""
Base Agent - Abstract base class and Protocol definitions for all agents.

Protocols define the typed interface each agent role must satisfy.
Startup validation checks agent wiring before the workflow runs.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any, TYPE_CHECKING, runtime_checkable, Protocol
from datetime import datetime
import logging

if TYPE_CHECKING:
    from ..core.memory import Memory
    from ..core.contextguard import ContextGuardAgent

logger = logging.getLogger(__name__)


# =============================================================================
# Agent Protocols (typed interfaces for each role)
# =============================================================================

@runtime_checkable
class ReaderProtocol(Protocol):
    """Interface that ReaderAgent must satisfy."""
    def execute(self, **kwargs) -> "AgentResult": ...
    def set_knowledge_dir(self, path: Path) -> None: ...
    def extract_relevant(self, query: str, knowledge_dir: Path) -> list: ...


@runtime_checkable
class AnalystProtocol(Protocol):
    """Interface that AnalystAgent must satisfy."""
    def execute(self, **kwargs) -> "AgentResult": ...


@runtime_checkable
class ReviewerProtocol(Protocol):
    """Interface that ReviewerAgent must satisfy."""
    def execute(self, **kwargs) -> "AgentResult": ...
    def review_against_standards(
        self, content: str, workflow_name: str,
        user_query: str, persona: Dict, contract: Any,
    ) -> Any: ...


@runtime_checkable
class LearnerProtocol(Protocol):
    """Interface that LearnerAgent must satisfy."""
    def execute(self, **kwargs) -> "AgentResult": ...
    def get_patterns(self, query: str) -> Dict[str, Any]: ...
    def store_pattern(
        self, query: str, reasoning: str,
        score: float, feedback: Optional[str] = None,
    ) -> Any: ...
    def load_lessons(self, persona_dir: Any) -> List[str]: ...
    def get_lessons_for_prompt(self) -> str: ...


def validate_agent_wiring(
    reader: Any,
    analyst: Any,
    reviewer: Any,
    learner: Any,
) -> List[str]:
    """
    Validate that all agents satisfy their expected protocols.
    
    Returns a list of error messages. Empty list means all agents are valid.
    Called once at workflow startup; cost is negligible.
    """
    errors = []
    
    checks = [
        ("reader", reader, ReaderProtocol, ["execute", "set_knowledge_dir", "extract_relevant"]),
        ("analyst", analyst, AnalystProtocol, ["execute"]),
        ("reviewer", reviewer, ReviewerProtocol, ["execute", "review_against_standards"]),
        ("learner", learner, LearnerProtocol, ["execute", "get_patterns", "store_pattern", "load_lessons", "get_lessons_for_prompt"]),
    ]
    
    for name, agent, protocol, required_methods in checks:
        for method_name in required_methods:
            if not hasattr(agent, method_name) or not callable(getattr(agent, method_name)):
                errors.append(f"{name} agent missing required method: {method_name}")
    
    if errors:
        logger.error(f"[AGENT_VALIDATION] {len(errors)} wiring errors found")
        for err in errors:
            logger.error(f"  - {err}")
    else:
        logger.debug("[AGENT_VALIDATION] All agents satisfy their protocols")
    
    return errors


# =============================================================================
# Base classes
# =============================================================================

@dataclass
class AgentResult:
    """Result from agent operation."""
    success: bool
    output: Any
    tokens_used: int = 0
    duration_ms: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Abstract base class for all specialized agents.
    
    All agents share:
    - Access to shared memory
    - Context guard awareness
    - Persona context loading
    - Logging integration
    """
    
    def __init__(
        self,
        agent_id: str,
        memory: "Memory",
        context_guard: "ContextGuardAgent",
    ):
        self.agent_id = agent_id
        self.memory = memory
        self.context_guard = context_guard
        self._persona_context: Optional[Dict[str, Any]] = None
        
        logger.info(f"Agent initialized: {agent_id}")
    
    def set_persona_context(self, persona_context: Dict[str, Any]) -> None:
        """Set persona-specific context for this agent."""
        self._persona_context = persona_context
        agent_config = persona_context.get("agents", {}).get(self.agent_id, {})
        self._apply_persona_config(agent_config)
    
    def _apply_persona_config(self, config: Dict[str, Any]) -> None:
        """Apply persona-specific configuration. Override in subclasses."""
        pass
    
    def get_persona_prompt(self, prompt_type: str) -> Optional[str]:
        """Get persona-specific prompt if available."""
        if not self._persona_context:
            return None
        prompts = self._persona_context.get("prompts", {})
        return prompts.get(prompt_type)
    
    def log_operation(self, operation: str, tokens: int = 0) -> None:
        """Log operation and track tokens."""
        self.context_guard.monitor_tokens(self.agent_id, operation, tokens)
    
    def check_context_budget(self, estimated_tokens: int) -> bool:
        """Check if operation is within context budget."""
        impact = self.context_guard.estimate_operation_impact(estimated_tokens)
        return not impact["will_breach_threshold"]
    
    @abstractmethod
    def execute(self, **kwargs) -> AgentResult:
        """Execute the agent's primary action."""
        pass
