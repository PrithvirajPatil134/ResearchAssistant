"""
Configuration management for Research Assistant.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import yaml


@dataclass
class TokenConfig:
    """Token management configuration."""
    max_tokens: int = 10000
    threshold_percentage: float = 0.70  # 70% threshold for ContextGuard
    warning_percentage: float = 0.60    # Early warning at 60%
    reconstruction_target: float = 0.30  # Target 30% after reconstruction


@dataclass
class LoggingConfig:
    """Logging configuration."""
    log_dir: Path = field(default_factory=lambda: Path("data/logs"))
    log_level: str = "INFO"
    log_agents: bool = True
    log_tokens: bool = True
    log_workflows: bool = True
    log_feedback: bool = True
    retention_days: int = 30


@dataclass
class AIConfig:
    """AI/LLM configuration."""
    model: str = "claude-3-sonnet"
    temperature: float = 0.7
    max_response_tokens: int = 4000
    timeout_seconds: int = 60


@dataclass
class Config:
    """
    Main configuration class for Research Assistant.
    
    Loads configuration from:
    1. Default values
    2. config.yaml file (if exists)
    3. Environment variables (override)
    """
    
    # Directory paths
    workspace_dir: Path = field(default_factory=lambda: Path.cwd())
    data_dir: Path = field(default_factory=lambda: Path("data"))
    personas_dir: Path = field(default_factory=lambda: Path("src/research_assistant/personas"))
    
    # Sub-configurations
    tokens: TokenConfig = field(default_factory=TokenConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    ai: AIConfig = field(default_factory=AIConfig)
    
    # Current session
    current_persona: Optional[str] = None
    current_workflow: Optional[str] = None
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """Load configuration from file and environment."""
        config = cls()
        
        # Try to load from config file
        if config_path is None:
            config_path = Path("config.yaml")
        
        if config_path.exists():
            with open(config_path, "r") as f:
                yaml_config = yaml.safe_load(f)
                config._apply_yaml_config(yaml_config)
        
        # Apply environment variable overrides
        config._apply_env_overrides()
        
        # Ensure directories exist
        config._ensure_directories()
        
        return config
    
    def _apply_yaml_config(self, yaml_config: Dict[str, Any]) -> None:
        """Apply configuration from YAML file."""
        if not yaml_config:
            return
            
        if "tokens" in yaml_config:
            for key, value in yaml_config["tokens"].items():
                if hasattr(self.tokens, key):
                    setattr(self.tokens, key, value)
        
        if "logging" in yaml_config:
            for key, value in yaml_config["logging"].items():
                if hasattr(self.logging, key):
                    if key == "log_dir":
                        value = Path(value)
                    setattr(self.logging, key, value)
        
        if "ai" in yaml_config:
            for key, value in yaml_config["ai"].items():
                if hasattr(self.ai, key):
                    setattr(self.ai, key, value)
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides."""
        # Token config
        if os.getenv("RA_MAX_TOKENS"):
            self.tokens.max_tokens = int(os.getenv("RA_MAX_TOKENS"))
        if os.getenv("RA_TOKEN_THRESHOLD"):
            self.tokens.threshold_percentage = float(os.getenv("RA_TOKEN_THRESHOLD"))
        
        # AI config
        if os.getenv("RA_AI_MODEL"):
            self.ai.model = os.getenv("RA_AI_MODEL")
        if os.getenv("RA_AI_TEMPERATURE"):
            self.ai.temperature = float(os.getenv("RA_AI_TEMPERATURE"))
        
        # Logging
        if os.getenv("RA_LOG_LEVEL"):
            self.logging.log_level = os.getenv("RA_LOG_LEVEL")
    
    def _ensure_directories(self) -> None:
        """Ensure required directories exist."""
        directories = [
            self.data_dir,
            self.data_dir / "sources",
            self.data_dir / "summaries",
            self.data_dir / "drafts",
            self.data_dir / "feedback",
            self.data_dir / "published",
            self.logging.log_dir,
            self.logging.log_dir / "agents",
            self.logging.log_dir / "tokens",
            self.logging.log_dir / "workflows",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_persona_path(self, persona_name: str) -> Path:
        """Get the path to a persona directory."""
        return self.personas_dir / persona_name
    
    def set_current_persona(self, persona_name: str) -> None:
        """Set the current active persona."""
        persona_path = self.get_persona_path(persona_name)
        if not persona_path.exists():
            raise ValueError(f"Persona '{persona_name}' not found at {persona_path}")
        self.current_persona = persona_name
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "workspace_dir": str(self.workspace_dir),
            "data_dir": str(self.data_dir),
            "personas_dir": str(self.personas_dir),
            "tokens": {
                "max_tokens": self.tokens.max_tokens,
                "threshold_percentage": self.tokens.threshold_percentage,
                "warning_percentage": self.tokens.warning_percentage,
                "reconstruction_target": self.tokens.reconstruction_target,
            },
            "logging": {
                "log_dir": str(self.logging.log_dir),
                "log_level": self.logging.log_level,
                "log_agents": self.logging.log_agents,
                "log_tokens": self.logging.log_tokens,
                "log_workflows": self.logging.log_workflows,
            },
            "ai": {
                "model": self.ai.model,
                "temperature": self.ai.temperature,
                "max_response_tokens": self.ai.max_response_tokens,
            },
            "current_persona": self.current_persona,
            "current_workflow": self.current_workflow,
        }
