"""
Memory - Shared state and context across agents.

Provides a centralized memory store that all agents can access
for maintaining context, facts, and workflow state.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Types of memory entries."""
    FACT = "fact"              # Key facts to remember
    CONTEXT = "context"        # Contextual information
    DECISION = "decision"      # Decisions made
    FEEDBACK = "feedback"      # Mentor/reviewer feedback
    LEARNING = "learning"      # Learned patterns
    REFERENCE = "reference"    # Source references
    TASK = "task"              # Task-related info
    PERSONA = "persona"        # Current persona context


@dataclass
class MemoryEntry:
    """Single memory entry."""
    key: str
    value: Any
    memory_type: MemoryType
    source_agent: str
    importance: int = 5  # 1-10 scale
    timestamp: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value,
            "type": self.memory_type.value,
            "source": self.source_agent,
            "importance": self.importance,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class Memory:
    """
    Shared memory store for all agents.
    
    Features:
    - Store and retrieve facts, context, decisions
    - Priority-based memory (importance scoring)
    - Automatic expiration
    - Memory compression for context management
    - Persona-aware context
    """
    
    def __init__(self):
        self._store: Dict[str, MemoryEntry] = {}
        self._by_type: Dict[MemoryType, List[str]] = {t: [] for t in MemoryType}
        self._by_agent: Dict[str, List[str]] = {}
        self._current_persona: Optional[str] = None
        self._workflow_context: Dict[str, Any] = {}
        
        logger.info("Memory initialized")
    
    def store(
        self,
        key: str,
        value: Any,
        memory_type: MemoryType,
        source_agent: str,
        importance: int = 5,
        expires_in_minutes: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryEntry:
        """Store a memory entry."""
        expires_at = None
        if expires_in_minutes:
            from datetime import timedelta
            expires_at = datetime.now() + timedelta(minutes=expires_in_minutes)
        
        entry = MemoryEntry(
            key=key,
            value=value,
            memory_type=memory_type,
            source_agent=source_agent,
            importance=importance,
            expires_at=expires_at,
            metadata=metadata or {},
        )
        
        self._store[key] = entry
        self._by_type[memory_type].append(key)
        
        if source_agent not in self._by_agent:
            self._by_agent[source_agent] = []
        self._by_agent[source_agent].append(key)
        
        logger.debug(f"Memory stored: {key} ({memory_type.value}) from {source_agent}")
        return entry
    
    def get(self, key: str) -> Optional[Any]:
        """Get a memory value by key."""
        entry = self._store.get(key)
        if entry and not entry.is_expired():
            return entry.value
        return None
    
    def get_entry(self, key: str) -> Optional[MemoryEntry]:
        """Get full memory entry by key."""
        entry = self._store.get(key)
        if entry and not entry.is_expired():
            return entry
        return None
    
    def get_by_type(self, memory_type: MemoryType) -> List[MemoryEntry]:
        """Get all entries of a specific type."""
        keys = self._by_type.get(memory_type, [])
        return [
            self._store[k] for k in keys 
            if k in self._store and not self._store[k].is_expired()
        ]
    
    def get_by_agent(self, agent_id: str) -> List[MemoryEntry]:
        """Get all entries from a specific agent."""
        keys = self._by_agent.get(agent_id, [])
        return [
            self._store[k] for k in keys 
            if k in self._store and not self._store[k].is_expired()
        ]
    
    def get_important(self, min_importance: int = 7) -> List[MemoryEntry]:
        """Get entries above importance threshold."""
        return [
            e for e in self._store.values()
            if e.importance >= min_importance and not e.is_expired()
        ]
    
    def delete(self, key: str) -> bool:
        """Delete a memory entry."""
        if key in self._store:
            entry = self._store.pop(key)
            if key in self._by_type[entry.memory_type]:
                self._by_type[entry.memory_type].remove(key)
            if entry.source_agent in self._by_agent:
                if key in self._by_agent[entry.source_agent]:
                    self._by_agent[entry.source_agent].remove(key)
            return True
        return False
    
    def cleanup_expired(self) -> int:
        """Remove all expired entries."""
        expired = [k for k, v in self._store.items() if v.is_expired()]
        for key in expired:
            self.delete(key)
        return len(expired)
    
    # Persona context
    def set_persona(self, persona_name: str, persona_context: Dict[str, Any]) -> None:
        """Set current persona context."""
        self._current_persona = persona_name
        self.store(
            key=f"persona:{persona_name}",
            value=persona_context,
            memory_type=MemoryType.PERSONA,
            source_agent="system",
            importance=10,
        )
    
    def get_persona_context(self) -> Optional[Dict[str, Any]]:
        """Get current persona context."""
        if self._current_persona:
            return self.get(f"persona:{self._current_persona}")
        return None
    
    # Workflow context
    def set_workflow_context(self, context: Dict[str, Any]) -> None:
        """Set workflow-level context."""
        self._workflow_context.update(context)
    
    def get_workflow_context(self) -> Dict[str, Any]:
        """Get workflow context."""
        return self._workflow_context.copy()
    
    # Facts management
    def add_fact(self, fact: str, source: str, importance: int = 5) -> None:
        """Add a fact to memory."""
        key = f"fact:{hash(fact)}"
        self.store(key, fact, MemoryType.FACT, source, importance)
    
    def get_facts(self) -> List[str]:
        """Get all facts."""
        return [e.value for e in self.get_by_type(MemoryType.FACT)]
    
    # Feedback management
    def add_feedback(
        self,
        feedback: str,
        source: str,
        target_section: Optional[str] = None,
    ) -> None:
        """Add feedback to memory."""
        key = f"feedback:{datetime.now().timestamp()}"
        self.store(
            key, feedback, MemoryType.FEEDBACK, source, 
            importance=8,
            metadata={"target_section": target_section},
        )
    
    def get_feedback(self) -> List[MemoryEntry]:
        """Get all feedback entries."""
        return self.get_by_type(MemoryType.FEEDBACK)
    
    # Context compression
    def compress_for_context(self, max_entries: int = 20) -> Dict[str, Any]:
        """
        Compress memory for efficient context inclusion.
        Prioritizes by importance and recency.
        """
        all_entries = [e for e in self._store.values() if not e.is_expired()]
        
        # Sort by importance (desc) then recency (desc)
        sorted_entries = sorted(
            all_entries,
            key=lambda e: (e.importance, e.timestamp.timestamp()),
            reverse=True,
        )[:max_entries]
        
        compressed = {
            "persona": self._current_persona,
            "workflow": self._workflow_context,
            "key_memories": [
                {
                    "type": e.memory_type.value,
                    "value": str(e.value)[:200],  # Truncate long values
                    "importance": e.importance,
                }
                for e in sorted_entries
            ],
        }
        
        return compressed
    
    def get_summary(self) -> Dict[str, Any]:
        """Get memory summary statistics."""
        return {
            "total_entries": len(self._store),
            "by_type": {t.value: len(keys) for t, keys in self._by_type.items()},
            "by_agent": {a: len(keys) for a, keys in self._by_agent.items()},
            "current_persona": self._current_persona,
            "workflow_context_keys": list(self._workflow_context.keys()),
        }
    
    def clear(self) -> None:
        """Clear all memory."""
        self._store.clear()
        self._by_type = {t: [] for t in MemoryType}
        self._by_agent.clear()
        self._workflow_context.clear()
        logger.info("Memory cleared")
    
    def export(self) -> str:
        """Export memory to JSON string."""
        data = {
            "entries": [e.to_dict() for e in self._store.values()],
            "current_persona": self._current_persona,
            "workflow_context": self._workflow_context,
        }
        return json.dumps(data, indent=2, default=str)
