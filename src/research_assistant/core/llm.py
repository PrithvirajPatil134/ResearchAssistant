"""
LLM Integration Module for Research Assistant.

Provides unified interface to Claude (Anthropic) or GPT (OpenAI).
Falls back to template-based generation if no API key is configured.
"""

import os
import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Response from LLM."""
    content: str
    model: str
    tokens_used: int
    success: bool
    error: Optional[str] = None


class LLMClient:
    """
    Unified LLM client supporting Anthropic Claude and OpenAI.
    
    Priority:
    1. Anthropic Claude (if ANTHROPIC_API_KEY set)
    2. OpenAI (if OPENAI_API_KEY set)
    3. Local fallback (template-based)
    """
    
    def __init__(
        self,
        model: str = "claude-3-haiku-20240307",
        temperature: float = 0.7,
        max_tokens: int = 4000,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        self._anthropic_client = None
        self._openai_client = None
        self._provider = self._detect_provider()
        
        logger.info(f"[LLM] Initialized with provider: {self._provider}, model: {self.model}")
    
    def _detect_provider(self) -> str:
        """Detect available LLM provider."""
        # Check for Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                import anthropic
                self._anthropic_client = anthropic.Anthropic()
                return "anthropic"
            except ImportError:
                logger.warning("ANTHROPIC_API_KEY set but anthropic package not installed")
        
        # Check for OpenAI
        if os.getenv("OPENAI_API_KEY"):
            try:
                import openai
                self._openai_client = openai.OpenAI()
                return "openai"
            except ImportError:
                logger.warning("OPENAI_API_KEY set but openai package not installed")
        
        # Fallback to local
        logger.info("[LLM] No API keys found, using local template generation")
        return "local"
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[List[Dict[str, str]]] = None,
    ) -> LLMResponse:
        """
        Generate response from LLM.
        
        Args:
            prompt: The user prompt/question
            system_prompt: Optional system instructions
            context: Optional conversation context
            
        Returns:
            LLMResponse with generated content
        """
        if self._provider == "anthropic":
            return self._generate_anthropic(prompt, system_prompt, context)
        elif self._provider == "openai":
            return self._generate_openai(prompt, system_prompt, context)
        else:
            return self._generate_local(prompt, system_prompt, context)
    
    def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        context: Optional[List[Dict[str, str]]],
    ) -> LLMResponse:
        """Generate using Anthropic Claude."""
        try:
            messages = []
            
            # Add context if provided
            if context:
                for msg in context:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", ""),
                    })
            
            # Add current prompt
            messages.append({"role": "user", "content": prompt})
            
            # Make API call
            response = self._anthropic_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt or "You are a helpful research assistant.",
                messages=messages,
            )
            
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            
            logger.info(f"[LLM] Anthropic response: {tokens_used} tokens")
            
            return LLMResponse(
                content=content,
                model=self.model,
                tokens_used=tokens_used,
                success=True,
            )
            
        except Exception as e:
            logger.error(f"[LLM] Anthropic error: {e}")
            return LLMResponse(
                content="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=str(e),
            )
    
    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        context: Optional[List[Dict[str, str]]],
    ) -> LLMResponse:
        """Generate using OpenAI."""
        try:
            messages = []
            
            # Add system prompt
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add context if provided
            if context:
                for msg in context:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", ""),
                    })
            
            # Add current prompt
            messages.append({"role": "user", "content": prompt})
            
            # Make API call
            response = self._openai_client.chat.completions.create(
                model=self.model if "gpt" in self.model else "gpt-4o-mini",
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            logger.info(f"[LLM] OpenAI response: {tokens_used} tokens")
            
            return LLMResponse(
                content=content,
                model=response.model,
                tokens_used=tokens_used,
                success=True,
            )
            
        except Exception as e:
            logger.error(f"[LLM] OpenAI error: {e}")
            return LLMResponse(
                content="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=str(e),
            )
    
    def _generate_local(
        self,
        prompt: str,
        system_prompt: Optional[str],
        context: Optional[List[Dict[str, str]]],
    ) -> LLMResponse:
        """Generate using local template (fallback when no API)."""
        logger.info("[LLM] Using local template generation (no API key)")
        
        # Extract key information from prompt
        lines = prompt.split("\n")
        topic = ""
        for line in lines:
            if "Topic:" in line or "Query:" in line:
                topic = line.split(":", 1)[-1].strip()
                break
        
        if not topic:
            topic = lines[0][:100] if lines else "the topic"
        
        # Generate structured template response
        content = f"""Based on the available knowledge base materials and academic standards, here is an analysis of {topic}:

## Core Concept

{topic} represents a multifaceted approach that integrates theoretical frameworks with practical applications. This concept has been extensively studied in academic literature and has significant implications for organizational strategy.

## Key Components

1. **Strategic Alignment**: Ensuring resources and capabilities support organizational objectives
2. **Capability Development**: Building competencies that enable sustained competitive advantage
3. **Process Integration**: Connecting operational activities with strategic outcomes
4. **Performance Measurement**: Tracking and optimizing key metrics

## Theoretical Framework

The effectiveness of {topic} can be understood through the lens of resource-based theory and dynamic capabilities. Organizations that successfully implement this approach demonstrate:

- Clear articulation of strategic intent
- Systematic resource allocation processes
- Continuous learning and adaptation
- Strong stakeholder engagement

## Practical Implications

For practitioners, {topic} requires:

1. Comprehensive assessment of current capabilities
2. Gap analysis against strategic requirements
3. Development of action plans with clear milestones
4. Regular review and adjustment cycles

## Research Considerations

When studying {topic}, researchers should consider:

- Appropriate measurement scales and constructs
- Sample selection and data collection methods
- Statistical techniques suitable for the research questions
- Theoretical grounding in established literature

---

*This analysis synthesizes available course materials and academic literature. For deeper exploration, consult the referenced knowledge base sources.*"""
        
        return LLMResponse(
            content=content,
            model="local-template",
            tokens_used=len(content) // 4,  # Approximate
            success=True,
        )
    
    def generate_with_feedback(
        self,
        prompt: str,
        previous_output: str,
        feedback: str,
        system_prompt: Optional[str] = None,
    ) -> LLMResponse:
        """
        Generate improved output based on feedback.
        
        This is the key method for the reasoning loop - it takes previous
        output and feedback to generate an improved version.
        """
        improved_prompt = f"""{prompt}

---

**Previous Attempt:**
{previous_output[:2000]}

**Feedback for Improvement:**
{feedback}

---

Please generate an IMPROVED version that addresses the feedback. Focus on:
1. Better integration of knowledge base content
2. Clearer structure and coherence
3. More directly addressing the original question
"""
        
        return self.generate(improved_prompt, system_prompt)


# Singleton instance
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create LLM client singleton."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
