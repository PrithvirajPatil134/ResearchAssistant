"""
Parallel Agent Orchestrator — runs multiple kiro-cli agents concurrently.

Splits large tasks (e.g., analyzing 14 PDFs) into batches,
runs each batch as a separate kiro-cli agent in parallel,
then synthesizes results with a final agent.

Also handles context compression between stages so downstream
agents get focused summaries, not raw 20K char dumps.
"""

import logging
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Callable, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class ParallelAgentOrchestrator:
    """
    Orchestrates multiple kiro-cli agent processes for parallel work.
    
    Usage:
        orchestrator = ParallelAgentOrchestrator(llm, system_prompt)
        
        # Parallel document analysis
        playbook = orchestrator.analyze_documents_parallel(
            file_paths=[...],
            extraction_task="Extract narrative patterns...",
            synthesis_task="Synthesize into a playbook...",
        )
        
        # Compressed context for next stage
        compressed = orchestrator.compress_for_downstream(playbook, max_chars=3000)
    """
    
    def __init__(self, llm, system_prompt: str, max_parallel: int = 3, batch_size: int = 2,
                 stagger_delay: float = 15.0):
        self._llm = llm
        self._system_prompt = system_prompt
        self._max_parallel = max_parallel
        self._batch_size = batch_size
        self._stagger_delay = stagger_delay  # Seconds between launching parallel agents
    
    def analyze_documents_parallel(
        self,
        file_paths: List[str],
        extraction_task: str,
        synthesis_task: str,
        progress_callback: Optional[Callable] = None,
    ) -> str:
        """
        Analyze multiple documents in parallel batches, then synthesize.
        
        Each batch runs as a separate kiro-cli process with start_new_session=True
        so processes don't compete for terminal resources.
        """
        if not file_paths:
            return "[No documents to analyze]"
        
        if len(file_paths) <= self._batch_size:
            batches = [file_paths]
        else:
            batches = self._split_into_batches(file_paths)
        
        logger.info(f"[AGENTS] {len(file_paths)} files → {len(batches)} batch(es), parallel={min(len(batches), self._max_parallel)}")
        
        if progress_callback:
            progress_callback(0, len(batches), f"{len(batches)} batch(es), {min(len(batches), self._max_parallel)} parallel")
        
        # Run batches with staggered parallel execution
        # Stagger launches to avoid kiro-cli initialization conflicts
        batch_outputs = {}
        
        with ThreadPoolExecutor(max_workers=self._max_parallel) as executor:
            futures = {}
            for batch_idx, batch in enumerate(batches):
                # Stagger: wait before launching each batch after the first
                if batch_idx > 0 and self._max_parallel > 1:
                    import time as _time
                    logger.info(f"[AGENTS] Staggering batch {batch_idx+1} launch by {self._stagger_delay}s")
                    _time.sleep(self._stagger_delay)
                
                future = executor.submit(
                    self._run_batch_agent,
                    batch_idx, batch, extraction_task, len(batches),
                )
                futures[future] = batch_idx
            
            for future in as_completed(futures):
                batch_idx = futures[future]
                try:
                    result = future.result()
                    batch_outputs[batch_idx] = result
                    if progress_callback:
                        progress_callback(
                            len(batch_outputs), len(batches),
                            f"batch {batch_idx+1} done ({len(result)} chars)"
                        )
                    logger.info(f"[AGENTS] Batch {batch_idx+1}/{len(batches)}: {len(result)} chars")
                except Exception as e:
                    logger.error(f"[AGENTS] Batch {batch_idx+1} failed: {e}")
                    batch_outputs[batch_idx] = f"[Batch {batch_idx+1} failed: {e}]"
        
        ordered = [batch_outputs[i] for i in range(len(batches)) if i in batch_outputs]
        
        if not ordered or all(b.startswith("[Batch") for b in ordered):
            return "[All batches failed]"
        
        if len(batches) == 1:
            return ordered[0]
        
        if progress_callback:
            progress_callback(len(batches), len(batches), "synthesizing across batches")
        
        synthesis = self._run_synthesis_agent(ordered, synthesis_task)
        logger.info(f"[AGENTS] Synthesis: {len(synthesis)} chars from {len(ordered)} batches")
        return synthesis
    
    def _split_into_batches(self, file_paths: List[str]) -> List[List[str]]:
        """Split file paths into batches."""
        n_batches = math.ceil(len(file_paths) / self._batch_size)
        batches = []
        for i in range(n_batches):
            start = i * self._batch_size
            end = start + self._batch_size
            batches.append(file_paths[start:end])
        return batches
    
    def _run_batch_agent(
        self, batch_idx: int, file_paths: List[str],
        extraction_task: str, total_batches: int,
    ) -> str:
        """Run a single kiro-cli agent to analyze a batch of files."""
        file_list = "\n".join(f"- {p}" for p in file_paths)
        
        prompt = f"""You are analyzing batch {batch_idx + 1} of {total_batches}.

## FILES TO ANALYZE:
{file_list}

## TASK:
Read each file above and {extraction_task}

## OUTPUT FORMAT:
For each file, provide a thorough structured analysis (500-800 words per file).
Then provide a batch summary of common patterns across these {len(file_paths)} files.
Be thorough — every file must be fully analyzed. Do not skip or abbreviate any file."""
        
        response = self._llm.generate_as_agent(prompt, self._system_prompt)
        
        if response.success and response.content.strip():
            return response.content.strip()
        else:
            error = response.error if not response.success else "empty response"
            raise RuntimeError(f"Batch agent failed: {error}")
    
    def _run_synthesis_agent(self, batch_outputs: List[str], synthesis_task: str) -> str:
        """Run a kiro-cli agent to synthesize all batch outputs."""
        # Compress each batch output to fit in synthesis prompt
        # Use generous budget — teaching note analyses need detail preserved
        compressed_batches = []
        per_batch_budget = max(4000, 24000 // max(len(batch_outputs), 1))
        for i, output in enumerate(batch_outputs):
            compressed = output[:per_batch_budget]
            compressed_batches.append(f"### Batch {i+1} Analysis:\n{compressed}")
        
        all_analyses = "\n\n---\n\n".join(compressed_batches)
        
        prompt = f"""## ANALYSES FROM {len(batch_outputs)} PARALLEL AGENTS:

{all_analyses}

## SYNTHESIS TASK:
{synthesis_task}

Produce a comprehensive synthesis that:
1. Identifies common patterns across ALL batches
2. Notes variations and outliers
3. Creates an actionable framework/playbook
4. Uses bullet points and tables for clarity
5. Targets 1500-2500 words"""
        
        response = self._llm.generate_as_agent(prompt, self._system_prompt)
        
        if response.success and response.content.strip():
            return response.content.strip()
        else:
            # Fallback: concatenate batch outputs
            logger.warning("[PARALLEL] Synthesis agent failed, returning concatenated batches")
            return "\n\n---\n\n".join(batch_outputs)
    
    @staticmethod
    def compress_for_downstream(content: str, max_chars: int = 3000) -> str:
        """
        Compress stage output for passing to the next stage.
        Keeps structure (headers, key points) but removes verbose detail.
        """
        if len(content) <= max_chars:
            return content
        
        # Strategy: keep headers and first sentence of each section
        lines = content.split('\n')
        compressed = []
        chars = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Always keep headers
            if stripped.startswith('#') or stripped.startswith('|'):
                compressed.append(line)
                chars += len(line)
            # Keep bullet points (first 100 chars)
            elif stripped.startswith('-') or stripped.startswith('*') or stripped.startswith('•'):
                truncated = line[:100] + ('...' if len(line) > 100 else '')
                compressed.append(truncated)
                chars += len(truncated)
            # Keep first line of paragraphs
            elif stripped and not compressed[-1].strip() if compressed else True:
                truncated = line[:150] + ('...' if len(line) > 150 else '')
                compressed.append(truncated)
                chars += len(truncated)
            else:
                compressed.append('')
            
            if chars >= max_chars:
                compressed.append('\n[... compressed for downstream stage]')
                break
        
        return '\n'.join(compressed)
