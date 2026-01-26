"""
Core control agents for Research Assistant.

- Controller: Master orchestrator, reasoning control, anti-hallucination
- ContextGuard: Token monitoring, context reconstruction at 70% threshold
- Thinking: Reasoning module controlled by Controller
- Memory: Shared state and context across agents
- LLM: Unified LLM client (Anthropic/OpenAI/local)
"""

from .controller import ControllerAgent
from .contextguard import ContextGuardAgent
from .memory import Memory
from .thinking import ThinkingModule
from .llm import LLMClient, LLMResponse, get_llm_client

__all__ = [
    "ControllerAgent",
    "ContextGuardAgent",
    "Memory",
    "ThinkingModule",
    "LLMClient",
    "LLMResponse",
    "get_llm_client",
]
