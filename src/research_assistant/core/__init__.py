"""
Core control agents for Research Assistant.

- Controller: Master orchestrator, reasoning control, anti-hallucination
- ContextGuard: Token monitoring, context reconstruction at 70% threshold
- Thinking: Reasoning module controlled by Controller
- Memory: Shared state and context across agents
- LLM: Unified LLM client (Anthropic/OpenAI/local)

Level 3 modules:
- DispatchContract: Pre-dispatch contract defining "what done looks like"
- Evaluator: Post-composition evaluation (4 criteria)
- Recitation: Re-anchoring checkpoint before composition
- ParallelEval: Concurrent Analyst + Reviewer + Evaluator
- HarnessAudit: Systematic review of workflow assumptions
"""

from .controller import ControllerAgent
from .contextguard import ContextGuardAgent
from .memory import Memory
from .thinking import ThinkingModule
from .llm import LLMClient, LLMResponse, get_llm_client
from .dispatch_contract import DispatchContract, build_dispatch_contract
from .evaluator import EvaluationResult, run_evaluator_pass
from .recitation import build_recitation_block, build_stage_summary
from .parallel_eval import UnifiedEvaluation, run_parallel_evaluation
from .harness_audit import run_audit, AuditReport

__all__ = [
    "ControllerAgent",
    "ContextGuardAgent",
    "Memory",
    "ThinkingModule",
    "LLMClient",
    "LLMResponse",
    "get_llm_client",
    # Level 3
    "DispatchContract",
    "build_dispatch_contract",
    "EvaluationResult",
    "run_evaluator_pass",
    "build_recitation_block",
    "build_stage_summary",
    "UnifiedEvaluation",
    "run_parallel_evaluation",
    "run_audit",
    "AuditReport",
]
