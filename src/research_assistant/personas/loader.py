"""
Persona Loader - Loads and configures personas for the workflow.

Everything in the workflow revolves around the persona:
- Knowledge base
- Agent configurations
- Prompts and templates
- Guidelines and ethics
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
import yaml
import logging

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeSource:
    """A source in the knowledge base."""
    path: Path
    source_type: str  # research_papers, class_slides, etc.
    content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Persona:
    """
    Loaded persona with all configurations.
    
    This is the central object that all agents reference.
    """
    name: str
    domain: str
    description: str
    
    # Identity
    identity: Dict[str, Any]
    
    # Behaviors for voice, structure, teaching approach
    behaviors: Dict[str, Any]
    
    # Agent-specific configurations
    agent_configs: Dict[str, Dict[str, Any]]
    
    # Prompts for each agent
    prompts: Dict[str, Any]
    system_prompt: str
    templates: Dict[str, str]
    
    # Core functions defined for this persona
    functions: Dict[str, Dict[str, Any]]
    
    # Guidelines and ethics
    guidelines: List[str]
    ethics: List[str]
    
    # Knowledge base
    knowledge_base_config: Dict[str, Any]
    knowledge_sources: List[KnowledgeSource] = field(default_factory=list)
    
    # Paths
    persona_dir: Optional[Path] = None
    
    def get_agent_config(self, agent_id: str) -> Dict[str, Any]:
        """Get configuration for specific agent."""
        return self.agent_configs.get(agent_id, {})
    
    def get_prompt(self, agent_id: str, prompt_type: str) -> Optional[str]:
        """Get prompt for agent and type."""
        agent_prompts = self.prompts.get(agent_id, {})
        return agent_prompts.get(prompt_type)
    
    def get_template(self, template_name: str) -> Optional[str]:
        """Get response template."""
        return self.templates.get(template_name)
    
    def get_knowledge_by_type(self, source_type: str) -> List[KnowledgeSource]:
        """Get knowledge sources by type."""
        return [k for k in self.knowledge_sources if k.source_type == source_type]
    
    def to_context(self) -> Dict[str, Any]:
        """Convert to context dictionary for agents."""
        return {
            "name": self.name,
            "identity": self.identity,
            "behaviors": self.behaviors,
            "guidelines": self.guidelines,
            "system_prompt": self.system_prompt,
            "agents": self.agent_configs,
            "prompts": self.prompts,
        }


class PersonaLoader:
    """
    Loads personas from YAML configuration.
    
    Persona directory structure:
    personas/
    └── PERSONA_NAME/
        ├── persona.yaml      # Main configuration
        ├── prompts.yaml      # Agent prompts
        └── knowledge/        # Knowledge base materials
            ├── research_papers/
            ├── class_slides/
            ├── assignments/
            └── documents/
    """
    
    def __init__(self, personas_dir: Path):
        self.personas_dir = Path(personas_dir)
        self._loaded_personas: Dict[str, Persona] = {}
    
    def list_available(self) -> List[str]:
        """List available persona names."""
        if not self.personas_dir.exists():
            return []
        return [
            d.name for d in self.personas_dir.iterdir()
            if d.is_dir() and (d / "persona.yaml").exists()
        ]
    
    def load(self, persona_name: str) -> Persona:
        """Load a persona by name."""
        if persona_name in self._loaded_personas:
            return self._loaded_personas[persona_name]
        
        persona_dir = self.personas_dir / persona_name
        if not persona_dir.exists():
            raise ValueError(f"Persona not found: {persona_name}")
        
        # Load persona.yaml
        persona_path = persona_dir / "persona.yaml"
        with open(persona_path, "r") as f:
            config = yaml.safe_load(f)
        
        # Load prompts.yaml
        prompts_path = persona_dir / "prompts.yaml"
        prompts_config = {}
        if prompts_path.exists():
            with open(prompts_path, "r") as f:
                prompts_config = yaml.safe_load(f) or {}
        
        # Build persona object
        persona = Persona(
            name=config.get("name", persona_name),
            domain=config.get("domain", "general"),
            description=config.get("description", ""),
            identity=config.get("persona_identity", {}),
            behaviors=config.get("behaviors", {}),
            agent_configs=config.get("agents", {}),
            prompts=self._extract_agent_prompts(prompts_config),
            system_prompt=prompts_config.get("system_prompt", ""),
            templates=prompts_config.get("templates", {}),
            functions=config.get("functions", {}),
            guidelines=config.get("guidelines", []),
            ethics=config.get("ethics", []),
            knowledge_base_config=config.get("knowledge_base", {}),
            persona_dir=persona_dir,
        )
        
        # Load knowledge base
        persona.knowledge_sources = self._load_knowledge_base(persona)
        
        self._loaded_personas[persona_name] = persona
        
        logger.info(f"Loaded persona: {persona_name} ({len(persona.knowledge_sources)} sources)")
        return persona
    
    def _extract_agent_prompts(self, prompts_config: Dict) -> Dict[str, Dict[str, str]]:
        """Extract agent-specific prompts from config."""
        agent_prompts = {}
        skip_keys = {"system_prompt", "templates"}
        
        for key, value in prompts_config.items():
            if key not in skip_keys and isinstance(value, dict):
                agent_prompts[key] = value
        
        return agent_prompts
    
    def _load_knowledge_base(self, persona: Persona) -> List[KnowledgeSource]:
        """Load knowledge base sources."""
        sources = []
        kb_config = persona.knowledge_base_config
        
        if not kb_config:
            return sources
        
        sources_dir = persona.persona_dir / kb_config.get("sources_dir", "knowledge")
        if not sources_dir.exists():
            # Create directory structure
            sources_dir.mkdir(parents=True, exist_ok=True)
            for source_type in kb_config.get("types", []):
                (sources_dir / source_type).mkdir(exist_ok=True)
            return sources
        
        # Scan for files
        for source_type in kb_config.get("types", []):
            type_dir = sources_dir / source_type
            if type_dir.exists():
                for file_path in type_dir.iterdir():
                    if file_path.is_file() and file_path.suffix in [".md", ".txt", ".pdf", ".docx"]:
                        sources.append(KnowledgeSource(
                            path=file_path,
                            source_type=source_type,
                            metadata={"filename": file_path.name},
                        ))
        
        # Sort by priority
        priority = kb_config.get("priority_order", [])
        sources.sort(key=lambda s: (
            priority.index(s.source_type) if s.source_type in priority else 999
        ))
        
        return sources
    
    def configure_agents(
        self,
        persona: Persona,
        agents: Dict[str, Any],
    ) -> None:
        """Configure all agents with persona context."""
        persona_context = persona.to_context()
        
        for agent_id, agent in agents.items():
            if hasattr(agent, "set_persona_context"):
                agent.set_persona_context(persona_context)
                logger.debug(f"Configured agent: {agent_id}")
    
    def get_persona_summary(self, persona: Persona) -> Dict[str, Any]:
        """Get summary of loaded persona."""
        return {
            "name": persona.name,
            "domain": persona.domain,
            "identity": persona.identity.get("name", "Unknown"),
            "knowledge_sources": len(persona.knowledge_sources),
            "sources_by_type": {
                t: len(persona.get_knowledge_by_type(t))
                for t in persona.knowledge_base_config.get("types", [])
            },
            "guidelines_count": len(persona.guidelines),
            "configured_agents": list(persona.agent_configs.keys()),
        }
