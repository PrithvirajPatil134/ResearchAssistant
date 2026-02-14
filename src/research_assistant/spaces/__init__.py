"""
Space management for Research Assistant.

Spaces define the behavior, knowledge base, and prompts for all agents.
Everything in the workflow revolves around the loaded space.

Note: PersonaLoader is an alias for SpaceLoader for backward compatibility.
"""

from .loader import SpaceLoader, PersonaLoader, Persona

__all__ = ["SpaceLoader", "PersonaLoader", "Persona"]
