"""
Controller Agent - Master orchestrator for workflows.

Controls the thinking module, prevents hallucination, manages agent coordination.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable, TYPE_CHECKING
from datetime import datetime
from enum import Enum
import logging

if TYPE_CHECKING:
    from .contextguard import ContextGuardAgent
    from .memory import Memory
    from .thinking import ThinkingModule, ReasoningChain

logger = logging.getLogger(__name__)


class WorkflowState(Enum):
    """Workflow execution states."""
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    REVIEWING = "reviewing"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentTask:
    """Task assigned to an agent."""
    task_id: str
    agent_id: str
    description: str
    inputs: Dict[str, Any]
    persona_context: Optional[Dict[str, Any]] = None
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class WorkflowStep:
    """Single step in a workflow."""
    step_id: str
    name: str
    agent_id: str
    action: str
    inputs: Dict[str, Any]
    depends_on: List[str] = field(default_factory=list)
    status: str = "pending"
    result: Optional[Any] = None


@dataclass
class WorkflowExecution:
    """Execution context for a workflow."""
    workflow_id: str
    workflow_name: str
    steps: List[WorkflowStep]
    persona: Optional[str] = None
    state: WorkflowState = WorkflowState.IDLE
    current_step_index: int = 0
    results: Dict[str, Any] = field(default_factory=dict)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class ControllerAgent:
    """
    Master orchestrator that controls the thinking module and workflow execution.
    
    Key responsibilities:
    - Validate reasoning chains (anti-hallucination)
    - Ground responses in sources
    - Orchestrate multi-agent workflows
    - Manage agent coordination
    - Handle context guard alerts
    """
    
    def __init__(
        self,
        memory: "Memory",
        context_guard: "ContextGuardAgent",
        thinking: "ThinkingModule",
    ):
        self.memory = memory
        self.context_guard = context_guard
        self.thinking = thinking
        
        self._agents: Dict[str, Any] = {}
        self._current_execution: Optional[WorkflowExecution] = None
        self._execution_history: List[WorkflowExecution] = []
        
        # Register for context guard alerts
        self.context_guard.register_alert_callback(self._handle_context_alert)
        
        logger.info("Controller initialized")
    
    def register_agent(self, agent_id: str, agent: Any) -> None:
        """Register an agent with the controller."""
        self._agents[agent_id] = agent
        logger.info(f"Agent registered: {agent_id}")
    
    def get_agent(self, agent_id: str) -> Optional[Any]:
        """Get registered agent by ID."""
        return self._agents.get(agent_id)
    
    # === Reasoning Control ===
    
    def validate_reasoning(self, chain: "ReasoningChain") -> Dict[str, Any]:
        """
        Validate a reasoning chain for logical consistency and grounding.
        
        Returns validation result with any issues found.
        """
        issues = []
        
        # Check each step is grounded
        for step in chain.steps:
            if not step.grounded_in:
                issues.append({
                    "step": step.step_number,
                    "issue": "ungrounded",
                    "message": "No evidence sources provided",
                })
            
            # Check confidence
            if step.confidence < 0.5:
                issues.append({
                    "step": step.step_number,
                    "issue": "low_confidence",
                    "message": f"Confidence {step.confidence} below threshold",
                })
        
        # Check conclusion
        if not chain.conclusion:
            issues.append({
                "step": "conclusion",
                "issue": "missing",
                "message": "No conclusion provided",
            })
        
        is_valid = len(issues) == 0
        
        return {
            "is_valid": is_valid,
            "issues": issues,
            "overall_confidence": chain.overall_confidence,
            "recommendation": "proceed" if is_valid else "revise",
        }
    
    def ground_response(
        self,
        response: str,
        sources: List[str],
    ) -> Dict[str, Any]:
        """
        Ground a response in provided sources.
        
        Checks that claims in response are supported by sources.
        """
        # Simple grounding check - in production would use semantic matching
        grounding_score = min(1.0, len(sources) / 3)  # More sources = better grounding
        
        return {
            "response": response,
            "sources": sources,
            "grounding_score": grounding_score,
            "is_grounded": grounding_score >= 0.5,
            "needs_verification": grounding_score < 0.7,
        }
    
    def detect_hallucination(self, claim: str, evidence: List[str]) -> Dict[str, Any]:
        """Check if a claim might be hallucinated."""
        return self.thinking.check_hallucination_risk(claim, evidence)
    
    # === Workflow Orchestration ===
    
    def start_workflow(
        self,
        workflow_name: str,
        steps: List[Dict[str, Any]],
        persona: Optional[str] = None,
    ) -> WorkflowExecution:
        """Start a new workflow execution."""
        import uuid
        
        workflow_steps = [
            WorkflowStep(
                step_id=f"step_{i}",
                name=s.get("name", f"Step {i+1}"),
                agent_id=s["agent"],
                action=s["action"],
                inputs=s.get("inputs", {}),
                depends_on=s.get("depends_on", []),
            )
            for i, s in enumerate(steps)
        ]
        
        execution = WorkflowExecution(
            workflow_id=str(uuid.uuid4())[:8],
            workflow_name=workflow_name,
            steps=workflow_steps,
            persona=persona,
            state=WorkflowState.PLANNING,
            started_at=datetime.now(),
        )
        
        self._current_execution = execution
        
        # Store in memory
        self.memory.set_workflow_context({
            "workflow_id": execution.workflow_id,
            "workflow_name": workflow_name,
            "persona": persona,
        })
        
        logger.info(f"[CONTROLLER] Started workflow: {workflow_name} ({execution.workflow_id})")
        return execution
    
    def execute_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute a single workflow step."""
        agent = self._agents.get(step.agent_id)
        if not agent:
            raise ValueError(f"Agent not found: {step.agent_id}")
        
        step.status = "running"
        
        # Check context before execution
        impact = self.context_guard.estimate_operation_impact(1000)  # Estimate
        if impact["will_breach_threshold"]:
            logger.warning(f"[CONTROLLER] Step would breach context threshold")
            return {"status": "paused", "reason": "context_threshold"}
        
        try:
            # Execute agent action
            action_method = getattr(agent, step.action, None)
            if not action_method:
                raise ValueError(f"Agent {step.agent_id} has no action: {step.action}")
            
            result = action_method(**step.inputs)
            step.status = "completed"
            step.result = result
            
            return {"status": "completed", "result": result}
            
        except Exception as e:
            step.status = "failed"
            logger.error(f"[CONTROLLER] Step failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def run_workflow(self) -> WorkflowExecution:
        """Run the current workflow to completion."""
        if not self._current_execution:
            raise ValueError("No active workflow")
        
        execution = self._current_execution
        execution.state = WorkflowState.EXECUTING
        
        for i, step in enumerate(execution.steps):
            execution.current_step_index = i
            
            # Check dependencies
            for dep_id in step.depends_on:
                dep_step = next((s for s in execution.steps if s.step_id == dep_id), None)
                if dep_step and dep_step.status != "completed":
                    logger.warning(f"Dependency not met: {dep_id}")
                    continue
            
            result = self.execute_step(step)
            execution.results[step.step_id] = result
            
            if result["status"] == "failed":
                execution.state = WorkflowState.FAILED
                break
            elif result["status"] == "paused":
                execution.state = WorkflowState.PAUSED
                break
        else:
            execution.state = WorkflowState.COMPLETED
            execution.completed_at = datetime.now()
        
        self._execution_history.append(execution)
        return execution
    
    # === Context Management ===
    
    def _handle_context_alert(self, alert: Any) -> None:
        """Handle context guard alerts."""
        logger.warning(f"[CONTROLLER] Context alert: {alert.message}")
        
        if alert.recommended_action == "IMMEDIATE_RECONSTRUCTION":
            self._trigger_context_reconstruction()
        elif self._current_execution:
            self._current_execution.state = WorkflowState.PAUSED
    
    def _trigger_context_reconstruction(self) -> None:
        """Trigger context reconstruction."""
        # Get current context from memory
        context = self.memory.compress_for_context()
        context_str = str(context)
        
        # Reconstruct
        essential = self.context_guard.reconstruct_context(context_str)
        
        logger.info(
            f"[CONTROLLER] Context reconstructed: "
            f"{essential.original_token_count} → {essential.token_count}"
        )
    
    def get_status(self) -> Dict[str, Any]:
        """Get controller status."""
        return {
            "agents": list(self._agents.keys()),
            "current_workflow": (
                self._current_execution.workflow_name 
                if self._current_execution else None
            ),
            "workflow_state": (
                self._current_execution.state.value 
                if self._current_execution else "idle"
            ),
            "context_status": self.context_guard.get_status_report(),
            "memory_summary": self.memory.get_summary(),
        }
