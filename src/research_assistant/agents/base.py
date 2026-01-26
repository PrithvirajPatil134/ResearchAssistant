"""
Base Agent - Abstract base class for all agents.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, TYPE_CHECKING
from datetime import datetime
import logging

if TYPE_CHECKING:
    from ..core.memory import Memory
    from ..core.contextguard import ContextGuardAgent

logger = logging.getLogger(__name__)


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
