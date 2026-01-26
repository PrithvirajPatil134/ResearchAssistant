"""
LLM Integration Module for Research Assistant.

Uses kiro-cli for LLM execution (same as adw-core-ws reference).
Falls back to direct Anthropic API if kiro-cli not available.
"""

import os
import re
import subprocess
import time
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
    execution_time_ms: int = 0


# Kiro CLI path from environment
KIRO_CLI_PATH = os.getenv("KIRO_CLI_PATH", "kiro-cli")


def strip_ansi_codes(text: str) -> str:
    """Remove ANSI escape codes from text."""
    if not text:
        return text
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?\x07|\x1b\[[\d;]*m")
    return ansi_pattern.sub("", text)


def check_kiro_installed() -> bool:
    """Check if kiro-cli is installed and working."""
    try:
        result = subprocess.run(
            [KIRO_CLI_PATH, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


class LLMClient:
    """
    LLM client using kiro-cli (same approach as adw-core-ws).
    
    Priority:
    1. kiro-cli (if installed) - uses Claude via CLI
    2. Anthropic Python SDK (if ANTHROPIC_API_KEY set)
    3. OpenAI Python SDK (if OPENAI_API_KEY set)
    """
    
    def __init__(
        self,
        model: str = "claude-sonnet-4",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        timeout_seconds: int = 120,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout_seconds = timeout_seconds
        
        self._provider = self._detect_provider()
        self._anthropic_client = None
        self._openai_client = None
        
        logger.info(f"[LLM] Initialized with provider: {self._provider}, model: {self.model}")
    
    def _detect_provider(self) -> str:
        """Detect available LLM provider."""
        # Check for kiro-cli first (preferred)
        if check_kiro_installed():
            logger.info("[LLM] kiro-cli detected, using CLI provider")
            return "kiro"
        
        # Check for Anthropic SDK
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                import anthropic
                self._anthropic_client = anthropic.Anthropic()
                logger.info("[LLM] Using Anthropic API provider")
                return "anthropic"
            except ImportError:
                logger.warning("ANTHROPIC_API_KEY set but anthropic package not installed")
        
        # Check for OpenAI SDK
        if os.getenv("OPENAI_API_KEY"):
            try:
                import openai
                self._openai_client = openai.OpenAI()
                logger.info("[LLM] Using OpenAI API provider")
                return "openai"
            except ImportError:
                logger.warning("OPENAI_API_KEY set but openai package not installed")
        
        # No LLM available
        logger.warning("[LLM] No LLM provider available - install kiro-cli or set API keys")
        return "none"
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[List[Dict[str, str]]] = None,
    ) -> LLMResponse:
        """Generate response from LLM."""
        if self._provider == "kiro":
            return self._generate_kiro(prompt, system_prompt)
        elif self._provider == "anthropic":
            return self._generate_anthropic(prompt, system_prompt, context)
        elif self._provider == "openai":
            return self._generate_openai(prompt, system_prompt, context)
        else:
            return LLMResponse(
                content="Error: No LLM provider available. Install kiro-cli or set ANTHROPIC_API_KEY/OPENAI_API_KEY",
                model="none",
                tokens_used=0,
                success=False,
                error="No LLM provider configured",
            )
    
    def _generate_kiro(
        self,
        prompt: str,
        system_prompt: Optional[str],
    ) -> LLMResponse:
        """Generate using kiro-cli (same as adw-core-ws)."""
        start_time = time.time()
        
        # Build full prompt with system context
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n---\n\n{prompt}"
        
        # Build command
        cmd = [
            KIRO_CLI_PATH,
            "chat",
            "--no-interactive",
            "--trust-all-tools",
            "--model", self.model,
            full_prompt,
        ]
        
        # Set up environment
        env = self._get_safe_env()
        
        logger.debug(f"[LLM] Executing kiro-cli with model {self.model}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                timeout=self.timeout_seconds,
            )
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            if result.returncode == 0:
                output = strip_ansi_codes(result.stdout.strip())
                # Estimate tokens (rough approximation)
                tokens_used = len(output) // 4
                
                logger.info(f"[LLM] kiro-cli success: ~{tokens_used} tokens in {execution_time_ms}ms")
                
                return LLMResponse(
                    content=output,
                    model=self.model,
                    tokens_used=tokens_used,
                    success=True,
                    execution_time_ms=execution_time_ms,
                )
            else:
                error_msg = result.stderr.strip() if result.stderr else f"Exit code {result.returncode}"
                logger.error(f"[LLM] kiro-cli error: {error_msg}")
                
                return LLMResponse(
                    content="",
                    model=self.model,
                    tokens_used=0,
                    success=False,
                    error=error_msg,
                    execution_time_ms=execution_time_ms,
                )
                
        except subprocess.TimeoutExpired:
            execution_time_ms = int((time.time() - start_time) * 1000)
            error_msg = f"Timeout after {self.timeout_seconds}s"
            logger.error(f"[LLM] kiro-cli timeout")
            
            return LLMResponse(
                content="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=error_msg,
                execution_time_ms=execution_time_ms,
            )
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            logger.error(f"[LLM] kiro-cli exception: {e}")
            
            return LLMResponse(
                content="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=str(e),
                execution_time_ms=execution_time_ms,
            )
    
    def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        context: Optional[List[Dict[str, str]]],
    ) -> LLMResponse:
        """Generate using Anthropic Claude API."""
        start_time = time.time()
        
        try:
            messages = []
            
            if context:
                for msg in context:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", ""),
                    })
            
            messages.append({"role": "user", "content": prompt})
            
            response = self._anthropic_client.messages.create(
                model=self.model if "claude" in self.model else "claude-3-haiku-20240307",
                max_tokens=self.max_tokens,
                system=system_prompt or "You are a helpful research assistant.",
                messages=messages,
            )
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            
            logger.info(f"[LLM] Anthropic success: {tokens_used} tokens in {execution_time_ms}ms")
            
            return LLMResponse(
                content=content,
                model=self.model,
                tokens_used=tokens_used,
                success=True,
                execution_time_ms=execution_time_ms,
            )
            
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            logger.error(f"[LLM] Anthropic error: {e}")
            
            return LLMResponse(
                content="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=str(e),
                execution_time_ms=execution_time_ms,
            )
    
    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        context: Optional[List[Dict[str, str]]],
    ) -> LLMResponse:
        """Generate using OpenAI API."""
        start_time = time.time()
        
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            if context:
                for msg in context:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", ""),
                    })
            
            messages.append({"role": "user", "content": prompt})
            
            response = self._openai_client.chat.completions.create(
                model="gpt-4o-mini" if "claude" in self.model else self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            logger.info(f"[LLM] OpenAI success: {tokens_used} tokens in {execution_time_ms}ms")
            
            return LLMResponse(
                content=content,
                model=response.model,
                tokens_used=tokens_used,
                success=True,
                execution_time_ms=execution_time_ms,
            )
            
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            logger.error(f"[LLM] OpenAI error: {e}")
            
            return LLMResponse(
                content="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=str(e),
                execution_time_ms=execution_time_ms,
            )
    
    def _get_safe_env(self) -> Dict[str, str]:
        """Get filtered environment for subprocess."""
        safe_vars = {
            "HOME": os.getenv("HOME"),
            "USER": os.getenv("USER"),
            "PATH": os.getenv("PATH"),
            "SHELL": os.getenv("SHELL"),
            "TERM": os.getenv("TERM"),
            "LANG": os.getenv("LANG"),
            "LC_ALL": os.getenv("LC_ALL"),
            "PYTHONPATH": os.getenv("PYTHONPATH"),
            "PYTHONUNBUFFERED": "1",
            "PWD": os.getcwd(),
            # AWS credentials for Bedrock
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "AWS_SESSION_TOKEN": os.getenv("AWS_SESSION_TOKEN"),
            "AWS_REGION": os.getenv("AWS_REGION"),
            "AWS_DEFAULT_REGION": os.getenv("AWS_DEFAULT_REGION"),
            # Anthropic API key
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        }
        return {k: v for k, v in safe_vars.items() if v is not None}
    
    def generate_with_feedback(
        self,
        prompt: str,
        previous_output: str,
        feedback: str,
        system_prompt: Optional[str] = None,
    ) -> LLMResponse:
        """Generate improved output based on feedback."""
        improved_prompt = f"""{prompt}

---

**Previous Attempt:**
{previous_output[:3000]}

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
