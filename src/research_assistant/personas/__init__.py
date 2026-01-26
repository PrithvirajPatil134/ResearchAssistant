"""
Persona management for Research Assistant.

Personas define the behavior, knowledge base, and prompts for all agents.
Everything in the workflow revolves around the loaded persona.
"""

from .loader import PersonaLoader, Persona

__all__ = ["PersonaLoader", "Persona"]
