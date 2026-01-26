"""
ContextGuard Agent - Token monitoring and context management.

Monitors token usage across all agents and triggers context reconstruction
when the 70% threshold is breached.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TokenStatus(Enum):
    """Token usage status levels."""
    GREEN = "green"      # Below 60% - safe
    YELLOW = "yellow"    # 60-70% - warning
    RED = "red"          # Above 70% - threshold breached
    CRITICAL = "critical"  # Above 85% - immediate action required


@dataclass
class TokenStats:
    """Token usage statistics."""
    agent_id: str
    operation: str
    tokens_used: int
    cumulative_tokens: int
    max_tokens: int
    percentage: float
    status: TokenStatus
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "operation": self.operation,
            "tokens_used": self.tokens_used,
            "cumulative_tokens": self.cumulative_tokens,
            "max_tokens": self.max_tokens,
            "percentage": round(self.percentage * 100, 2),
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class Alert:
    """Alert for threshold breach."""
    agent_id: str
    current_percentage: float
    threshold_percentage: float
    message: str
    severity: str
    recommended_action: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class EssentialContext:
    """Compressed essential context after reconstruction."""
    summary: str
    key_facts: List[str]
    active_task: Optional[str]
    important_references: List[str]
    token_count: int
    original_token_count: int
    compression_ratio: float


@dataclass
class ContextSnapshot:
    """Snapshot of context at a point in time."""
    content: str
    token_count: int
    agent_id: str
    operation: str
    timestamp: datetime = field(default_factory=datetime.now)


class ContextGuardAgent:
    """
    Monitors token usage across all agents.
    
    Key responsibilities:
    - Track cumulative token consumption
    - Alert at 70% threshold
    - Trigger context reconstruction
    - Maintain essential context summaries
    
    Configuration:
    - THRESHOLD_PERCENTAGE: 70% - Alert and reconstruct
    - WARNING_PERCENTAGE: 60% - Early warning
    - RECONSTRUCTION_TARGET: 30% - Target after compression
    """
    
    # Threshold configurations
    THRESHOLD_PERCENTAGE = 0.70  # 70% - trigger reconstruction
    WARNING_PERCENTAGE = 0.60    # 60% - early warning
    RECONSTRUCTION_TARGET = 0.30  # 30% - target after reconstruction
    CRITICAL_PERCENTAGE = 0.85   # 85% - critical, immediate action
    
    def __init__(
        self,
        max_tokens: int = 10000,
        threshold: float = 0.70,
        warning: float = 0.60,
        reconstruction_target: float = 0.30,
    ):
        self.max_tokens = max_tokens
        self.threshold_percentage = threshold
        self.warning_percentage = warning
        self.reconstruction_target = reconstruction_target
        
        # State tracking
        self._cumulative_tokens: int = 0
        self._agent_tokens: Dict[str, int] = {}
        self._history: List[TokenStats] = []
        self._alerts: List[Alert] = []
        self._context_snapshots: List[ContextSnapshot] = []
        
        # Callbacks for alerts
        self._alert_callbacks: List[Callable[[Alert], None]] = []
        
        logger.info(
            f"ContextGuard initialized: max={max_tokens}, "
            f"threshold={threshold*100}%, warning={warning*100}%"
        )
    
    @property
    def current_percentage(self) -> float:
        """Current token usage as percentage."""
        return self._cumulative_tokens / self.max_tokens
    
    @property
    def current_status(self) -> TokenStatus:
        """Get current token status."""
        pct = self.current_percentage
        if pct >= self.CRITICAL_PERCENTAGE:
            return TokenStatus.CRITICAL
        elif pct >= self.threshold_percentage:
            return TokenStatus.RED
        elif pct >= self.warning_percentage:
            return TokenStatus.YELLOW
        return TokenStatus.GREEN
    
    @property
    def tokens_remaining(self) -> int:
        """Tokens remaining before max."""
        return self.max_tokens - self._cumulative_tokens
    
    @property
    def tokens_until_threshold(self) -> int:
        """Tokens remaining before threshold breach."""
        threshold_tokens = int(self.max_tokens * self.threshold_percentage)
        return max(0, threshold_tokens - self._cumulative_tokens)
    
    def register_alert_callback(self, callback: Callable[[Alert], None]) -> None:
        """Register a callback for alert notifications."""
        self._alert_callbacks.append(callback)
    
    def monitor_tokens(
        self,
        agent_id: str,
        operation: str,
        tokens_used: int,
    ) -> TokenStats:
        """
        Monitor token usage for an operation.
        
        Args:
            agent_id: Identifier of the agent using tokens
            operation: Description of the operation
            tokens_used: Number of tokens consumed
            
        Returns:
            TokenStats with current status
        """
        # Update cumulative tokens
        self._cumulative_tokens += tokens_used
        
        # Update per-agent tracking
        if agent_id not in self._agent_tokens:
            self._agent_tokens[agent_id] = 0
        self._agent_tokens[agent_id] += tokens_used
        
        # Calculate status
        percentage = self.current_percentage
        status = self.current_status
        
        # Create stats
        stats = TokenStats(
            agent_id=agent_id,
            operation=operation,
            tokens_used=tokens_used,
            cumulative_tokens=self._cumulative_tokens,
            max_tokens=self.max_tokens,
            percentage=percentage,
            status=status,
        )
        
        # Log the monitoring
        self._history.append(stats)
        
        logger.info(
            f"[TOKEN] {agent_id} | {operation} | "
            f"used={tokens_used} | cumulative={self._cumulative_tokens} | "
            f"pct={percentage*100:.1f}% | status={status.value}"
        )
        
        # Check if we need to alert
        if status in (TokenStatus.RED, TokenStatus.CRITICAL):
            alert = self._create_alert(agent_id, percentage, status)
            self._trigger_alert(alert)
        elif status == TokenStatus.YELLOW:
            logger.warning(
                f"[CONTEXTGUARD] Warning: Token usage at {percentage*100:.1f}% "
                f"(approaching {self.threshold_percentage*100}% threshold)"
            )
        
        return stats
    
    def _create_alert(
        self,
        agent_id: str,
        percentage: float,
        status: TokenStatus,
    ) -> Alert:
        """Create an alert for threshold breach."""
        if status == TokenStatus.CRITICAL:
            severity = "CRITICAL"
            message = (
                f"CRITICAL: Token usage at {percentage*100:.1f}%! "
                f"Immediate context reconstruction required."
            )
            recommended_action = "IMMEDIATE_RECONSTRUCTION"
        else:
            severity = "WARNING"
            message = (
                f"Token threshold breached: {percentage*100:.1f}% "
                f"(threshold: {self.threshold_percentage*100}%). "
                f"Context reconstruction recommended."
            )
            recommended_action = "RECONSTRUCT_CONTEXT"
        
        alert = Alert(
            agent_id=agent_id,
            current_percentage=percentage,
            threshold_percentage=self.threshold_percentage,
            message=message,
            severity=severity,
            recommended_action=recommended_action,
        )
        
        self._alerts.append(alert)
        return alert
    
    def _trigger_alert(self, alert: Alert) -> None:
        """Trigger alert to all registered callbacks."""
        logger.warning(f"[CONTEXTGUARD ALERT] {alert.message}")
        
        for callback in self._alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Alert callback failed: {e}")
    
    def check_threshold(self) -> tuple[bool, Optional[Alert]]:
        """
        Check if threshold is breached.
        
        Returns:
            Tuple of (is_breached, alert_if_any)
        """
        if self.current_percentage >= self.threshold_percentage:
            alert = self._create_alert(
                "system",
                self.current_percentage,
                self.current_status,
            )
            return True, alert
        return False, None
    
    def should_reconstruct(self) -> bool:
        """Check if context reconstruction should be triggered."""
        return self.current_percentage >= self.threshold_percentage
    
    def estimate_operation_impact(self, estimated_tokens: int) -> Dict[str, Any]:
        """
        Estimate the impact of a planned operation.
        
        Args:
            estimated_tokens: Estimated tokens for the operation
            
        Returns:
            Impact assessment including whether it would breach threshold
        """
        projected_total = self._cumulative_tokens + estimated_tokens
        projected_percentage = projected_total / self.max_tokens
        
        will_breach_warning = projected_percentage >= self.warning_percentage
        will_breach_threshold = projected_percentage >= self.threshold_percentage
        will_breach_critical = projected_percentage >= self.CRITICAL_PERCENTAGE
        
        return {
            "estimated_tokens": estimated_tokens,
            "current_tokens": self._cumulative_tokens,
            "projected_total": projected_total,
            "projected_percentage": projected_percentage,
            "current_percentage": self.current_percentage,
            "will_breach_warning": will_breach_warning,
            "will_breach_threshold": will_breach_threshold,
            "will_breach_critical": will_breach_critical,
            "recommendation": self._get_recommendation(projected_percentage),
        }
    
    def _get_recommendation(self, projected_percentage: float) -> str:
        """Get recommendation based on projected percentage."""
        if projected_percentage >= self.CRITICAL_PERCENTAGE:
            return "ABORT: Operation would exceed critical threshold. Reconstruct context first."
        elif projected_percentage >= self.threshold_percentage:
            return "CAUTION: Operation would breach threshold. Consider reconstructing context first."
        elif projected_percentage >= self.warning_percentage:
            return "WARNING: Operation would approach threshold. Monitor closely."
        return "PROCEED: Operation within safe limits."
    
    def reconstruct_context(
        self,
        current_context: str,
        summarizer: Optional[Callable[[str], str]] = None,
    ) -> EssentialContext:
        """
        Reconstruct context to reduce token usage.
        
        This is the core context management function that:
        1. Analyzes current context
        2. Extracts essential information
        3. Compresses to target percentage
        
        Args:
            current_context: The current full context
            summarizer: Optional function to summarize text
            
        Returns:
            EssentialContext with compressed information
        """
        original_tokens = self._estimate_tokens(current_context)
        
        logger.info(
            f"[CONTEXTGUARD] Starting context reconstruction. "
            f"Current tokens: {original_tokens}"
        )
        
        # Extract essential components
        key_facts = self._extract_key_facts(current_context)
        important_refs = self._extract_references(current_context)
        active_task = self._extract_active_task(current_context)
        
        # Create summary
        if summarizer:
            summary = summarizer(current_context)
        else:
            summary = self._default_summarize(current_context)
        
        # Calculate new token count
        compressed_content = self._build_compressed_context(
            summary, key_facts, active_task, important_refs
        )
        new_tokens = self._estimate_tokens(compressed_content)
        
        # Calculate compression ratio
        compression_ratio = 1 - (new_tokens / original_tokens) if original_tokens > 0 else 0
        
        # Reset token counter to new level
        self._cumulative_tokens = new_tokens
        
        essential = EssentialContext(
            summary=summary,
            key_facts=key_facts,
            active_task=active_task,
            important_references=important_refs,
            token_count=new_tokens,
            original_token_count=original_tokens,
            compression_ratio=compression_ratio,
        )
        
        logger.info(
            f"[CONTEXTGUARD] Context reconstruction complete. "
            f"Before: {original_tokens} | After: {new_tokens} | "
            f"Compression: {compression_ratio*100:.1f}%"
        )
        
        return essential
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count for text (rough approximation)."""
        # Rough estimate: ~4 characters per token
        return len(text) // 4
    
    def _extract_key_facts(self, context: str) -> List[str]:
        """Extract key facts from context."""
        # This would be enhanced with AI extraction
        # For now, simple extraction based on patterns
        facts = []
        lines = context.split("\n")
        for line in lines:
            line = line.strip()
            # Look for bullet points, numbered items, or key phrases
            if (
                line.startswith("- ") or
                line.startswith("* ") or
                line.startswith("• ") or
                (len(line) > 2 and line[0].isdigit() and line[1] in ".)")
            ):
                facts.append(line.lstrip("-*•0123456789.) "))
        return facts[:10]  # Limit to 10 key facts
    
    def _extract_references(self, context: str) -> List[str]:
        """Extract important references from context."""
        # Look for URLs, citations, file paths
        import re
        refs = []
        
        # URLs
        urls = re.findall(r'https?://[^\s]+', context)
        refs.extend(urls[:5])
        
        # File paths
        paths = re.findall(r'[\w/]+\.\w{2,4}', context)
        refs.extend(paths[:5])
        
        return refs[:10]
    
    def _extract_active_task(self, context: str) -> Optional[str]:
        """Extract the currently active task from context."""
        # Look for task indicators
        lines = context.split("\n")
        for line in lines:
            lower = line.lower()
            if any(kw in lower for kw in ["current task:", "working on:", "active:", "todo:"]):
                return line.split(":", 1)[-1].strip()
        return None
    
    def _default_summarize(self, context: str) -> str:
        """Default summarization (truncation with key preservation)."""
        # Simple truncation - would be replaced with AI summarization
        max_summary_length = 500
        if len(context) <= max_summary_length:
            return context
        
        # Take beginning and end with ellipsis
        half = max_summary_length // 2
        return context[:half] + "\n...[truncated]...\n" + context[-half:]
    
    def _build_compressed_context(
        self,
        summary: str,
        key_facts: List[str],
        active_task: Optional[str],
        references: List[str],
    ) -> str:
        """Build compressed context string."""
        parts = ["## Context Summary", summary, ""]
        
        if active_task:
            parts.extend(["## Active Task", active_task, ""])
        
        if key_facts:
            parts.append("## Key Facts")
            for fact in key_facts:
                parts.append(f"- {fact}")
            parts.append("")
        
        if references:
            parts.append("## References")
            for ref in references:
                parts.append(f"- {ref}")
        
        return "\n".join(parts)
    
    def save_snapshot(self, context: str, agent_id: str, operation: str) -> None:
        """Save a context snapshot for potential recovery."""
        snapshot = ContextSnapshot(
            content=context,
            token_count=self._estimate_tokens(context),
            agent_id=agent_id,
            operation=operation,
        )
        self._context_snapshots.append(snapshot)
        
        # Keep only last 5 snapshots
        if len(self._context_snapshots) > 5:
            self._context_snapshots = self._context_snapshots[-5:]
    
    def get_latest_snapshot(self) -> Optional[ContextSnapshot]:
        """Get the most recent context snapshot."""
        return self._context_snapshots[-1] if self._context_snapshots else None
    
    def reset(self) -> None:
        """Reset token tracking (for new session/workflow)."""
        self._cumulative_tokens = 0
        self._agent_tokens.clear()
        logger.info("[CONTEXTGUARD] Token tracking reset")
    
    def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report."""
        return {
            "cumulative_tokens": self._cumulative_tokens,
            "max_tokens": self.max_tokens,
            "percentage": round(self.current_percentage * 100, 2),
            "status": self.current_status.value,
            "tokens_remaining": self.tokens_remaining,
            "tokens_until_threshold": self.tokens_until_threshold,
            "threshold_percentage": self.threshold_percentage * 100,
            "warning_percentage": self.warning_percentage * 100,
            "agent_breakdown": dict(self._agent_tokens),
            "total_operations": len(self._history),
            "total_alerts": len(self._alerts),
            "recent_alerts": [
                {
                    "message": a.message,
                    "severity": a.severity,
                    "timestamp": a.timestamp.isoformat(),
                }
                for a in self._alerts[-5:]
            ],
        }
    
    def get_agent_usage(self, agent_id: str) -> Dict[str, Any]:
        """Get token usage for specific agent."""
        agent_history = [h for h in self._history if h.agent_id == agent_id]
        return {
            "agent_id": agent_id,
            "total_tokens": self._agent_tokens.get(agent_id, 0),
            "operation_count": len(agent_history),
            "recent_operations": [
                h.to_dict() for h in agent_history[-10:]
            ],
        }
