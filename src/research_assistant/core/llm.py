"""
LLM Integration Module for Research Assistant.

Provider priority:
1. Perplexity API (PERPLEXITY_API_KEY) - Supports multiple models including Grok
2. Anthropic API (ANTHROPIC_API_KEY)
3. OpenAI API (OPENAI_API_KEY)
4. kiro-cli (if installed)
"""

import os
import re
import subprocess
import sys
import time
import logging
import json
import threading
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass
import urllib.request
import urllib.error

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


def strip_file_paths(text: str) -> str:
    """Remove absolute file paths from text to prevent kiro-cli from trying to read them.
    
    Replaces paths like /Users/propatil/workplace/.../file.md with just the filename.
    The reader already extracted the content — the LLM doesn't need the paths.
    """
    if not text:
        return text
    
    # Match absolute paths: /Users/... or /home/... up to a file extension or trailing /
    # Allow spaces, apostrophes, and other chars in filenames
    def _replace_path(match):
        full_path = match.group(1)
        # Extract just the filename (last component)
        parts = full_path.rstrip('/').split('/')
        filename = parts[-1] if parts else full_path
        return f'[file: {filename}]'
    
    # Match paths ending with a file extension
    result = re.sub(
        r'(/(?:Users|home|tmp|var)/[^\n]+?\.(?:md|pdf|docx|txt|xlsx|eml|png|jpg))',
        _replace_path,
        text,
    )
    
    # Match directory paths ending with /
    result = re.sub(
        r'(/(?:Users|home|tmp|var)/[^\n]+?/)\s*\(',
        lambda m: f'[directory] (',
        result,
    )
    
    # Catch any remaining absolute paths
    result = re.sub(
        r'(/(?:Users|home|tmp|var)/[^\n\s]{20,})',
        lambda m: '[path removed]',
        result,
    )
    
    return result


def _clean_kiro_output(text: str) -> str:
    """Clean kiro-cli agent artifacts from output.
    
    Removes:
    - Tool call output lines (Reading file:, Creating:, etc.)
    - Status lines (✓ Successfully read, Completed in, etc.)
    - Agent conversation lines (> I'll..., > Ready for..., Should I proceed?)
    - Diff-style lines (+  1: ...)
    """
    if not text:
        return text
    
    lines = text.split('\n')
    cleaned = []
    skip_block = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip tool call output
        if any(stripped.startswith(p) for p in [
            'Reading file:', 'Reading directory:', 'Creating:',
            'I\'ll create the following file:', 'Purpose:',
            '✓ Successfully', '- Completed in',
            '(using tool:', 'Batch fs_read', 'Batch fs_write',
            '↱ Operation', '⋮', '- Summary:',
        ]):
            skip_block = True
            continue
        
        # Skip diff-style lines from file writes
        if re.match(r'^\+\s+\d+:', stripped):
            continue
        
        # Skip kiro-cli preamble
        if stripped.startswith('> ') and any(kw in stripped.lower() for kw in [
            'i\'ll', 'i understand', 'let me', 'should i proceed',
            'ready for step', 'i\'ve created', 'i now have',
        ]):
            continue
        
        # End of skip block on empty line
        if skip_block and not stripped:
            skip_block = False
            continue
        
        if not skip_block:
            cleaned.append(line)
    
    # Remove leading/trailing blank lines
    result = '\n'.join(cleaned).strip()
    
    # Remove kiro-cli response prefix "> " from the start of the output
    if result.startswith('> '):
        result = result[2:]
    
    # Detect truncation — if output ends mid-sentence, log a warning
    if result and not result[-1] in '.!?"\')]\n—–' and len(result) > 1000:
        logger.warning(f"[LLM] Output may be truncated (ends with: '...{result[-50:]}')")
    
    return result


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
    LLM client with multiple provider support.
    
    Priority:
    1. Perplexity API (if PERPLEXITY_API_KEY set) - Supports Grok, Llama, etc.
    2. Anthropic Python SDK (if ANTHROPIC_API_KEY set)
    3. OpenAI Python SDK (if OPENAI_API_KEY set)
    4. kiro-cli (if installed)
    """
    
    # Default models for each provider
    DEFAULT_MODELS = {
        "perplexity": "sonar-pro",  # Best Perplexity model with web search
        "anthropic": "claude-3-haiku-20240307",
        "openai": "gpt-4o-mini",
        "kiro": "claude-opus-4.7",  # Opus 4.7 (primary); falls back to claude-opus-4.6
    }
    
    # Fallback chain: if primary model is unavailable, try these in order
    FALLBACK_MODELS = {
        "kiro": ["claude-opus-4.7", "claude-opus-4.6"],
    }
    
    # Available models by provider
    # Set LLM_MODEL env var to select a specific model
    AVAILABLE_MODELS = {
        "perplexity": [
            # Perplexity Sonar models (with web search)
            "sonar-pro",           # Most capable, 200k context
            "sonar",               # Lightweight, 128k context
            "sonar-reasoning-pro", # Extended thinking
            "sonar-reasoning",     # Reasoning
        ],
        "kiro": [
            # Run `kiro-cli chat --help` to see available models
            "Auto",                # Auto-select best model
            "claude-sonnet-4.5",   # Claude Sonnet 4.5
            "claude-sonnet-4",     # Claude Sonnet 4 (default)
            "claude-haiku-4.5",    # Claude Haiku 4.5 (fast)
            "claude-opus-4.5",     # Claude Opus 4.5 (most capable)
            "claude-opus-4.6",     # Claude Opus 4.6 (fallback)
            "claude-opus-4.7",     # Claude Opus 4.7 (default)
            "claude-sonnet-4.5",   # Claude Sonnet 4.5 with large context
            "qwen3-coder-480b",    # Qwen 3 Coder 480B
        ],
    }
    
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 16000,
        timeout_seconds: Optional[int] = None,
    ):
        self.temperature = temperature
        self.max_tokens = max_tokens
        # Allow env override: LLM_TIMEOUT_SECONDS, default 600s (10 min base for research)
        self.timeout_seconds = timeout_seconds or int(os.getenv("LLM_TIMEOUT_SECONDS", "600"))
        
        self._provider = self._detect_provider()
        
        # Model selection priority: constructor arg > LLM_MODEL env > default
        self.model = (
            model
            or os.getenv("LLM_MODEL")
            or self.DEFAULT_MODELS.get(self._provider, "gpt-4o-mini")
        )
        
        self._anthropic_client = None
        self._openai_client = None
        
        logger.info(f"[LLM] Initialized with provider: {self._provider}, model: {self.model}")
        logger.debug(f"[LLM] Available models: {self.AVAILABLE_MODELS.get(self._provider, [])}")
    
    def _detect_provider(self) -> str:
        """Detect available LLM provider."""
        # Check for Perplexity API (priority for Grok access)
        if os.getenv("PERPLEXITY_API_KEY"):
            logger.info("[LLM] Using Perplexity API provider (Grok 4.0)")
            return "perplexity"
        
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
        
        # Check for kiro-cli
        if check_kiro_installed():
            logger.info("[LLM] kiro-cli detected, using CLI provider")
            return "kiro"
        
        # No LLM available
        logger.warning("[LLM] No LLM provider available - set PERPLEXITY_API_KEY or other API keys")
        return "none"

    @staticmethod
    def estimate_timeout(prompt: str, kb_file_count: int = 0, workflow_name: str = "explain") -> int:
        """
        Estimate an appropriate timeout based on prompt complexity.
        
        Research workloads are expected to take time — the agent needs to
        thoroughly read files, reason, and produce comprehensive output.
        
        Heuristics:
        - Base: 180s for simple prompts
        - +60s per 1000 chars of prompt beyond 2000
        - +45s per KB file referenced (reading files takes time)
        - Workflow multiplier: guide=1.5x, research=2.0x, quant=1.5x
        - Cap at 1800s (30 min) — research tasks can legitimately take this long
        """
        prompt_len = len(prompt)
        
        # Base timeout — generous for research
        base = 180
        
        # Scale with prompt length
        if prompt_len > 2000:
            extra_chars = prompt_len - 2000
            base += int((extra_chars / 1000) * 60)
        
        # Scale with KB files — each file the agent reads takes time
        base += kb_file_count * 45
        
        # Workflow multiplier
        multipliers = {
            "guide": 1.5,
            "review": 1.2,
            "research": 2.0,
            "quant": 1.5,
            "explain": 1.0,
        }
        base = int(base * multipliers.get(workflow_name, 1.0))
        
        # Clamp to [180, 1800] — 30 min ceiling for thorough research
        timeout = max(180, min(base, 1800))
        
        logger.info(
            f"[LLM] Estimated timeout: {timeout}s "
            f"(prompt={prompt_len} chars, kb_files={kb_file_count}, workflow={workflow_name})"
        )
        return timeout
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[List[Dict[str, str]]] = None,
    ) -> LLMResponse:
        """Generate response from LLM. Retries with fallback models if primary is unavailable."""
        # Log prompt size for debugging
        total_chars = len(prompt) + len(system_prompt or "")
        est_tokens = total_chars // 4
        if est_tokens > 50000:
            logger.warning(
                f"[LLM] Very large prompt: ~{est_tokens} tokens ({total_chars} chars). "
                f"Consider reducing KB content to avoid timeouts."
            )
            print(
                f"   ⚠️  Large prompt detected: ~{est_tokens} tokens. This may take a while.",
                file=sys.stderr,
                flush=True,
            )
        
        result = self._dispatch_generate(prompt, system_prompt, context)
        
        # If model not found or produced zero output (stall), try fallback chain
        if not result.success and result.error and (
            "does not exist" in result.error
            or "0 chars" in result.error
        ):
            result = self._retry_with_fallback(prompt, system_prompt, context, agent_mode=False)
        
        return result
    
    def _dispatch_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[List[Dict[str, str]]] = None,
    ) -> LLMResponse:
        """Dispatch to the appropriate provider."""
        if self._provider == "perplexity":
            return self._generate_perplexity(prompt, system_prompt, context)
        elif self._provider == "anthropic":
            return self._generate_anthropic(prompt, system_prompt, context)
        elif self._provider == "openai":
            return self._generate_openai(prompt, system_prompt, context)
        elif self._provider == "kiro":
            return self._generate_kiro(prompt, system_prompt)
        else:
            return LLMResponse(
                content="Error: No LLM provider available. Set PERPLEXITY_API_KEY for Grok 4.0 access.",
                model="none",
                tokens_used=0,
                success=False,
                error="No LLM provider configured",
            )
    
    def generate_as_agent(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        stall_override: Optional[int] = None,
    ) -> LLMResponse:
        """
        Generate using kiro-cli as a full agent (can read files, use tools).
        Used for content generation stages where the agent needs file access.
        Falls back to regular generate() for non-kiro providers.
        
        stall_override: If set, overrides the default stall threshold (seconds).
        Useful for continuation agents that should bail faster (e.g., 180s).
        """
        if self._provider == "kiro":
            result = self._generate_kiro(prompt, system_prompt, agent_mode=True, stall_override=stall_override)
            
            # If model not found or produced zero output (stall), try fallback chain in agent mode
            if not result.success and result.error and (
                "does not exist" in result.error
                or "0 chars" in result.error
            ):
                result = self._retry_with_fallback(prompt, system_prompt, context=None, agent_mode=True, stall_override=stall_override)
            
            return result
        else:
            # Non-kiro providers don't have agent mode
            return self.generate(prompt, system_prompt)
    
    def _retry_with_fallback(
        self,
        prompt: str,
        system_prompt: Optional[str],
        context: Optional[List[Dict[str, str]]] = None,
        agent_mode: bool = False,
        stall_override: Optional[int] = None,
    ) -> LLMResponse:
        """Retry generation with fallback models when the primary model is unavailable."""
        fallback_chain = self.FALLBACK_MODELS.get(self._provider, [])
        
        for fallback_model in fallback_chain:
            if fallback_model == self.model:
                continue  # Skip the model that already failed
            
            logger.warning(f"[LLM] Model '{self.model}' unavailable. Trying fallback: {fallback_model}")
            print(
                f"   ⚠️  Model '{self.model}' not available. Falling back to '{fallback_model}'.",
                file=sys.stderr, flush=True,
            )
            
            original_model = self.model
            self.model = fallback_model
            
            if agent_mode and self._provider == "kiro":
                result = self._generate_kiro(prompt, system_prompt, agent_mode=True, stall_override=stall_override)
            elif self._provider == "kiro":
                result = self._generate_kiro(prompt, system_prompt, agent_mode=False)
            else:
                result = self._dispatch_generate(prompt, system_prompt, context)
            
            if result.success or (result.error and "does not exist" not in result.error and "0 chars" not in result.error):
                # Either succeeded or failed for a different reason; keep this model for future calls
                logger.info(f"[LLM] Fallback to '{fallback_model}' {'succeeded' if result.success else 'failed (non-model error)'}")
                return result
            
            # This fallback also doesn't exist, restore and try next
            self.model = original_model
        
        # All fallbacks exhausted
        logger.error(f"[LLM] All fallback models exhausted for provider '{self._provider}'")
        return LLMResponse(
            content="",
            model=self.model,
            tokens_used=0,
            success=False,
            error=f"All models unavailable. Tried: {', '.join(fallback_chain)}",
        )
    
    def _generate_perplexity(
        self,
        prompt: str,
        system_prompt: Optional[str],
        context: Optional[List[Dict[str, str]]],
    ) -> LLMResponse:
        """Generate using Perplexity API with Grok 4.0 model."""
        start_time = time.time()
        api_key = os.getenv("PERPLEXITY_API_KEY")
        
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
            
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            }
            
            request = urllib.request.Request(
                "https://api.perplexity.ai/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            )
            
            logger.debug(f"[LLM] Calling Perplexity API with model {self.model}")
            
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                result = json.loads(response.read().decode("utf-8"))
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            content = result["choices"][0]["message"]["content"]
            tokens_used = result.get("usage", {}).get("total_tokens", len(content) // 4)
            
            logger.info(f"[LLM] Perplexity/Grok success: {tokens_used} tokens in {execution_time_ms}ms")
            
            return LLMResponse(
                content=content,
                model=result.get("model", self.model),
                tokens_used=tokens_used,
                success=True,
                execution_time_ms=execution_time_ms,
            )
            
        except urllib.error.HTTPError as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            error_body = e.read().decode("utf-8") if e.fp else str(e)
            logger.error(f"[LLM] Perplexity HTTP error {e.code}: {error_body}")
            
            return LLMResponse(
                content="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=f"HTTP {e.code}: {error_body}",
                execution_time_ms=execution_time_ms,
            )
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            logger.error(f"[LLM] Perplexity error: {e}")
            
            return LLMResponse(
                content="",
                model=self.model,
                tokens_used=0,
                success=False,
                error=str(e),
                execution_time_ms=execution_time_ms,
            )
    
    # Stall detection thresholds
    STALL_TIMEOUT_TEXTGEN = 120   # 2 min for scoring/learning (small prompts)
    STALL_TIMEOUT_AGENT = 600     # 10 min for agent mode (Opus needs time to read + reason over large inputs)
    
    def _generate_kiro(
        self,
        prompt: str,
        system_prompt: Optional[str],
        agent_mode: bool = False,
        stall_override: Optional[int] = None,
    ) -> LLMResponse:
        """
        Generate using kiro-cli with real-time progress monitoring.
        
        Two modes:
        - agent_mode=False: Text generation (scoring/learning). Strips paths, cleans artifacts.
        - agent_mode=True: Full agent (content generation). Keeps paths, raw output.
        
        stall_override: If set, overrides the default stall threshold (useful for
        continuation agents that should bail faster).
        
        Progress monitoring:
        - Reads stdout in real-time via Popen
        - Prints heartbeat every 15s showing output size growth
        - Detects stalls: if no new output for threshold (120s text-gen, 300s agent), kills process
        - This prevents deadlocks while allowing legitimately long operations
        """
        start_time = time.time()
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n---\n\n{prompt}"
        
        prompt_len = len(full_prompt)
        logger.info(f"[LLM] Prompt size: {prompt_len} chars (~{prompt_len // 4} tokens), agent_mode={agent_mode}")
        
        if not agent_mode:
            full_prompt = strip_file_paths(full_prompt)
        
        cmd = [
            KIRO_CLI_PATH,
            "chat",
            "--legacy-ui",
            "--no-interactive",
            "--trust-all-tools",
            "--model", self.model,
        ]
        
        env = self._get_safe_env()
        logger.debug(f"[LLM] Executing kiro-cli (agent_mode={agent_mode})")
        
        # Use Popen for real-time output monitoring
        # start_new_session=True gives each process its own session —
        # critical for parallel execution so processes don't compete for terminal
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            start_new_session=True,
        )
        
        # Send prompt via stdin and close
        try:
            process.stdin.write(full_prompt)
            process.stdin.close()
        except BrokenPipeError:
            pass
        
        # Monitor output in a separate thread
        output_chunks = []
        last_output_time = time.time()
        stop_monitor = threading.Event()
        
        def _read_stdout():
            """Read stdout chunks as they arrive."""
            nonlocal last_output_time
            try:
                while not stop_monitor.is_set():
                    chunk = process.stdout.read(4096)
                    if not chunk:
                        break
                    output_chunks.append(chunk)
                    last_output_time = time.time()
            except (ValueError, OSError):
                pass  # Process closed
        
        def _monitor():
            """Print progress and detect stalls."""
            interval = 30  # Every 30s, not 15 — less noise
            prev_size = 0
            while not stop_monitor.wait(interval):
                elapsed = int(time.time() - start_time)
                current_size = sum(len(c) for c in output_chunks)
                since_last = int(time.time() - last_output_time)
                
                size_delta = current_size - prev_size
                prev_size = current_size
                
                # Concise one-line status
                if size_delta > 0:
                    status = f"+{size_delta} chars ({current_size} total)"
                elif current_size > 0:
                    status = f"idle {since_last}s ({current_size} total)"
                else:
                    status = f"starting... ({since_last}s)"
                
                remaining = self.timeout_seconds - elapsed
                print(
                    f"   ⏳ {elapsed}s | {status} | ~{max(0,remaining)}s left",
                    file=sys.stderr, flush=True,
                )
                
                # Stall detection — use longer threshold for agent mode (needs reasoning time)
                # stall_override allows callers to set a shorter threshold (e.g., for continuations)
                stall_threshold = stall_override or (self.STALL_TIMEOUT_AGENT if agent_mode else self.STALL_TIMEOUT_TEXTGEN)
                
                if since_last > stall_threshold:
                    if current_size > 0:
                        logger.warning(f"[LLM] Stall: no output for {since_last}s after {current_size} chars")
                        print(
                            f"   ⚠️  Stall ({since_last}s idle, threshold={stall_threshold}s). Returning partial output.",
                            file=sys.stderr, flush=True,
                        )
                    else:
                        logger.warning(f"[LLM] No output after {since_last}s (threshold={stall_threshold}s)")
                        print(
                            f"   ⚠️  No output after {since_last}s. Terminating.",
                            file=sys.stderr, flush=True,
                        )
                    process.kill()
                    return
                
                if elapsed >= self.timeout_seconds:
                    logger.warning(f"[LLM] Hard timeout at {elapsed}s with {current_size} chars")
                    process.kill()
                    return
        
        reader_thread = threading.Thread(target=_read_stdout, daemon=True)
        monitor_thread = threading.Thread(target=_monitor, daemon=True)
        reader_thread.start()
        monitor_thread.start()
        
        try:
            process.wait(timeout=self.timeout_seconds)
        except subprocess.TimeoutExpired:
            process.kill()
        
        stop_monitor.set()
        reader_thread.join(timeout=5)
        
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Collect output
        raw_output = ''.join(output_chunks)
        stderr_output = ""
        try:
            stderr_output = process.stderr.read() or ""
        except (ValueError, OSError):
            pass
        
        if process.returncode == 0 or (process.returncode is None and raw_output.strip()):
            output = strip_ansi_codes(raw_output.strip())
            
            if not agent_mode:
                output = _clean_kiro_output(output)
            
            if output.strip():
                tokens_used = len(output) // 4
                logger.info(f"[LLM] kiro-cli success: ~{tokens_used} tokens in {execution_time_ms}ms")
                
                return LLMResponse(
                    content=output,
                    model=self.model,
                    tokens_used=tokens_used,
                    success=True,
                    execution_time_ms=execution_time_ms,
                )
        
        # Determine error with diagnostic context
        if process.returncode is None or process.returncode == -9:
            since_last = int(time.time() - last_output_time)
            total_output = len(raw_output)
            
            if since_last > (self.STALL_TIMEOUT_AGENT if agent_mode else self.STALL_TIMEOUT_TEXTGEN):
                error_msg = f"Stalled after {total_output} chars ({since_last}s idle)"
                # Concise diagnostic — just the facts
                logger.warning(
                    f"[LLM] DIAGNOSTIC: stall | model={self.model} | "
                    f"output={total_output} chars | idle={since_last}s | "
                    f"elapsed={execution_time_ms}ms | agent_mode={agent_mode} | "
                    f"last_output_tail='{raw_output[-100:].strip()[:80]}'"
                )
            else:
                error_msg = f"Timeout after {self.timeout_seconds}s ({total_output} chars produced)"
                logger.warning(
                    f"[LLM] DIAGNOSTIC: timeout | model={self.model} | "
                    f"output={total_output} chars | timeout={self.timeout_seconds}s | "
                    f"agent_mode={agent_mode}"
                )
            
            # Return partial output if substantial
            partial = strip_ansi_codes(raw_output.strip())
            if not agent_mode:
                partial = _clean_kiro_output(partial)
            if len(partial) > 500:
                logger.info(f"[LLM] Returning partial output ({len(partial)} chars)")
                return LLMResponse(
                    content=partial,
                    model=self.model,
                    tokens_used=len(partial) // 4,
                    success=True,
                    execution_time_ms=execution_time_ms,
                )
        else:
            # Check both stderr and stdout for error messages (kiro-cli may write errors to either)
            stderr_clean = strip_ansi_codes(stderr_output.strip()) if stderr_output.strip() else ""
            stdout_clean = strip_ansi_codes(raw_output.strip()) if raw_output.strip() else ""
            
            if stderr_clean:
                error_msg = stderr_clean[:500]
            elif stdout_clean:
                error_msg = stdout_clean[:500]
            else:
                error_msg = f"Exit code {process.returncode}"
            
            logger.warning(
                f"[LLM] DIAGNOSTIC: error | rc={process.returncode} | "
                f"model={self.model} | error={error_msg[:100]}"
            )
        
        logger.error(f"[LLM] kiro-cli failed: {error_msg}")
        return LLMResponse(
            content="",
            model=self.model,
            tokens_used=0,
            success=False,
            error=error_msg,
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
                model=self.model if "gpt" in self.model else "gpt-4o-mini",
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
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "AWS_SESSION_TOKEN": os.getenv("AWS_SESSION_TOKEN"),
            "AWS_REGION": os.getenv("AWS_REGION"),
            "AWS_DEFAULT_REGION": os.getenv("AWS_DEFAULT_REGION"),
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY"),
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
