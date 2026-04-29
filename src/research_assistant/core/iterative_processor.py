"""
Iterative Document Processor — the core mental model for all workflows.

Principle: Process like a human researcher.
- Read one thing at a time, build understanding incrementally
- When tasks are independent, run them in parallel
- Stage all intermediate results to a shared workspace
- Downstream tasks reference the staged data

This applies to ALL workflows:
- Case studies: analyze benchmarks → ingest context → write sections
- Research: map literature → identify gaps → design methodology → roadmap
- Quant: understand data → select methods → plan analysis → interpret
- Thesis: review structure → draft sections → cross-reference → revise
"""

import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from pathlib import Path
import json

logger = logging.getLogger(__name__)


@dataclass
class DocumentSummary:
    """Summary of a single processed document."""
    source: str
    key_points: str
    char_count: int


@dataclass 
class StagedResult:
    """A result staged to the shared workspace for downstream tasks."""
    task_name: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    duration_ms: int = 0


class SharedWorkspace:
    """
    Central staging area for intermediate results.
    Any agent in the pipeline can write to and read from this workspace.
    Persists to disk so results survive failures.
    """
    
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self._results: Dict[str, StagedResult] = {}
        self._load_existing()
    
    def _load_existing(self):
        """Load any previously staged results from disk."""
        for f in self.workspace_dir.glob("*.md"):
            name = f.stem
            content = f.read_text()
            if content.strip():
                self._results[name] = StagedResult(task_name=name, content=content)
                logger.info(f"[WORKSPACE] Loaded existing: {name} ({len(content)} chars)")
    
    def stage(self, result: StagedResult) -> None:
        """Stage a result to the shared workspace."""
        self._results[result.task_name] = result
        # Persist to disk
        filepath = self.workspace_dir / f"{result.task_name}.md"
        filepath.write_text(result.content)
        
        # Write metadata
        meta_path = self.workspace_dir / f"{result.task_name}.meta.json"
        meta_path.write_text(json.dumps(result.metadata, default=str, indent=2))
        
        logger.info(f"[WORKSPACE] Staged: {result.task_name} ({len(result.content)} chars)")
    
    def get(self, task_name: str) -> Optional[str]:
        """Get a staged result by name."""
        if task_name in self._results:
            return self._results[task_name].content
        # Try loading from disk
        filepath = self.workspace_dir / f"{task_name}.md"
        if filepath.exists():
            content = filepath.read_text()
            if content.strip():
                self._results[task_name] = StagedResult(task_name=task_name, content=content)
                return content
        return None
    
    def has(self, task_name: str) -> bool:
        return task_name in self._results or (self.workspace_dir / f"{task_name}.md").exists()
    
    def get_all(self) -> Dict[str, str]:
        """Get all staged results."""
        return {name: r.content for name, r in self._results.items()}
    
    def get_context_for_downstream(self, max_chars: int = 10000) -> str:
        """Build a context string from all staged results for downstream tasks."""
        parts = []
        chars_used = 0
        for name, result in self._results.items():
            excerpt = result.content[:max_chars - chars_used] if chars_used < max_chars else ""
            if excerpt:
                parts.append(f"### {name}\n{excerpt}")
                chars_used += len(excerpt)
        return "\n\n---\n\n".join(parts)


class IterativeProcessor:
    """
    Generic iterative processor that applies the human mental model
    to any workflow: process one at a time, build understanding, synthesize.
    
    Supports:
    - Sequential processing (one doc at a time with running context)
    - Parallel processing (independent tasks run concurrently)
    - Section-by-section writing (each section builds on previous)
    - All results staged to SharedWorkspace for downstream access
    """
    
    def __init__(self, llm_generate: Callable, system_prompt: str = "",
                 workspace: Optional[SharedWorkspace] = None, max_parallel: int = 3):
        self._generate = llm_generate
        self._system_prompt = system_prompt
        self._workspace = workspace
        self._max_parallel = max_parallel
    
    # =========================================================================
    # PATTERN 1: Iterative Document Analysis (read one → extract → compare → synthesize)
    # Used by: benchmark analysis, literature review, thesis chapter review
    # =========================================================================
    
    def analyze_documents(
        self,
        documents: List[Dict[str, str]],
        task_description: str,
        extraction_prompt: str,
        synthesis_prompt: str,
        progress_callback: Optional[Callable] = None,
        parallel: bool = False,
    ) -> str:
        """
        Analyze documents iteratively or in parallel, then synthesize.
        
        Sequential: doc1 → extract → doc2 → extract+compare → ... → synthesize
        Parallel: [doc1, doc2, doc3] → extract all → synthesize
        """
        if not documents:
            return "[No documents to process]"
        
        # Filter out empty/stub documents
        valid_docs = [d for d in documents 
                      if d.get("content", "").strip() 
                      and not d["content"].startswith("[PDF Document:")]
        
        if not valid_docs:
            return "[No documents with extractable content]"
        
        if parallel and len(valid_docs) > 1:
            extractions = self._analyze_parallel(valid_docs, task_description, 
                                                  extraction_prompt, progress_callback)
        else:
            extractions = self._analyze_sequential(valid_docs, task_description,
                                                    extraction_prompt, progress_callback)
        
        if not extractions:
            return "[No documents could be processed]"
        
        # Stage individual extractions to workspace
        if self._workspace:
            for e in extractions:
                self._workspace.stage(StagedResult(
                    task_name=f"analysis_{e.source.replace('.', '_').replace(' ', '_')}",
                    content=e.key_points,
                    metadata={"source": e.source, "chars_analyzed": e.char_count},
                ))
        
        # Synthesize
        if progress_callback:
            progress_callback(len(valid_docs), len(valid_docs), "synthesizing")
        
        synthesis = self._synthesize(extractions, task_description, synthesis_prompt)
        
        # Stage synthesis
        if self._workspace:
            self._workspace.stage(StagedResult(
                task_name="synthesis",
                content=synthesis,
                metadata={"docs_analyzed": len(extractions)},
            ))
        
        return synthesis
    
    def _analyze_sequential(self, docs, task, extraction_prompt, progress_cb) -> List[DocumentSummary]:
        """Process documents one at a time with running context."""
        extractions = []
        running_context = ""
        
        for i, doc in enumerate(docs):
            source = doc.get("source", f"Document {i+1}")
            content = doc.get("content", "")
            
            if progress_cb:
                progress_cb(i, len(docs), source)
            
            prompt = f"""{task}

## DOCUMENT ({i+1}/{len(docs)}): {source}
{content[:8000]}

## EXTRACT:
{extraction_prompt}
"""
            if running_context:
                prompt += f"""
## PATTERNS SO FAR (from {len(extractions)} docs):
{running_context[:3000]}

Compare with patterns above. Note similarities AND differences.
"""
            prompt += "\nOutput CONCISE analysis (max 500 words). Extract insights, not summaries."
            
            response = self._generate(
                prompt,
                self._system_prompt + "\nAnalyze iteratively. Be concise. Extract patterns."
            )
            
            if response.success and response.content.strip():
                extraction = response.content.strip()
                extractions.append(DocumentSummary(source=source, key_points=extraction, char_count=len(content)))
                running_context = self._compress_context(extractions)
                logger.info(f"[ITERATIVE] {source} ({i+1}/{len(docs)}): {len(extraction)} chars")
            else:
                logger.warning(f"[ITERATIVE] Failed: {source}")
        
        return extractions
    
    def _analyze_parallel(self, docs, task, extraction_prompt, progress_cb) -> List[DocumentSummary]:
        """Process independent documents in parallel."""
        extractions = []
        
        def _process_one(i, doc):
            source = doc.get("source", f"Document {i+1}")
            content = doc.get("content", "")
            
            prompt = f"""{task}

## DOCUMENT ({i+1}/{len(docs)}): {source}
{content[:8000]}

## EXTRACT:
{extraction_prompt}

Output CONCISE analysis (max 500 words). Extract insights, not summaries."""
            
            response = self._generate(
                prompt,
                self._system_prompt + "\nAnalyze this document. Be concise."
            )
            
            if response.success and response.content.strip():
                return DocumentSummary(source=source, key_points=response.content.strip(), char_count=len(content))
            return None
        
        logger.info(f"[ITERATIVE] Parallel analysis of {len(docs)} docs (max {self._max_parallel} concurrent)")
        
        with ThreadPoolExecutor(max_workers=self._max_parallel) as executor:
            futures = {executor.submit(_process_one, i, doc): i for i, doc in enumerate(docs)}
            
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    result = future.result()
                    if result:
                        extractions.append(result)
                        if progress_cb:
                            progress_cb(len(extractions), len(docs), result.source)
                        logger.info(f"[ITERATIVE] Parallel done: {result.source}")
                except Exception as e:
                    logger.warning(f"[ITERATIVE] Parallel failed doc {idx}: {e}")
        
        # Sort by original order
        extractions.sort(key=lambda e: next((i for i, d in enumerate(docs) if d.get("source") == e.source), 999))
        return extractions
    
    def _synthesize(self, extractions: List[DocumentSummary], task: str, synthesis_prompt: str) -> str:
        """Synthesize all extractions into a final output."""
        # Compress extractions to fit in prompt — keep key points only
        all_text = "\n\n".join(
            f"**{e.source}**: {e.key_points[:600]}" for e in extractions
        )
        
        # Cap total extraction text to leave room for synthesis output
        if len(all_text) > 12000:
            all_text = all_text[:12000] + "\n\n[... additional extractions truncated for space]"
        
        prompt = f"""{task}

## KEY PATTERNS FROM {len(extractions)} DOCUMENTS:
{all_text}

## SYNTHESIS TASK:
{synthesis_prompt}

IMPORTANT: Keep your synthesis FOCUSED and STRUCTURED. Use bullet points and tables.
Target 1500-2500 words maximum. Prioritize actionable patterns over exhaustive detail.
Do NOT repeat the extraction content — synthesize into a framework."""
        
        response = self._generate(prompt, self._system_prompt)
        if response.success and response.content.strip():
            return response.content.strip()
        return self._compress_context(extractions)
    
    def _compress_context(self, extractions: List[DocumentSummary]) -> str:
        if len(extractions) <= 3:
            return "\n\n".join(f"**{e.source}**: {e.key_points[:400]}" for e in extractions)
        parts = [f"- **{e.source}**: {e.key_points.split(chr(10))[0][:150]}" for e in extractions[:-3]]
        parts += [f"**{e.source}**: {e.key_points[:400]}" for e in extractions[-3:]]
        return "\n\n".join(parts)
    
    # =========================================================================
    # PATTERN 2: Section-by-Section Writing (write one → build on previous)
    # Used by: case study writing, thesis chapters, research papers
    # =========================================================================
    
    def write_sections(
        self,
        sections: List[Dict[str, str]],
        context: str,
        task_description: str,
        progress_callback: Optional[Callable] = None,
    ) -> str:
        """
        Write a document section by section, each building on previous.
        Sections defined generically — works for any document type.
        """
        if not sections:
            return "[No sections defined]"
        
        written = []
        
        for i, section in enumerate(sections):
            name = section.get("name", f"Section {i+1}")
            instructions = section.get("instructions", "")
            
            if progress_callback:
                progress_callback(i, len(sections), name)
            
            # Build context from previous sections
            prev_text = ""
            if written:
                if len(written) > 2:
                    older = "\n".join(f"[{s['name']}: {s['content'][:200]}...]" for s in written[:-2])
                    prev_text = f"## EARLIER SECTIONS (summaries):\n{older}\n\n"
                recent = "\n\n---\n\n".join(f"## {s['name']}\n{s['content']}" for s in written[-2:])
                prev_text += f"## PREVIOUS SECTIONS:\n{recent}"
            
            # Also pull from workspace if available
            workspace_context = ""
            if self._workspace:
                workspace_context = f"\n\n## STAGED DATA FROM PREVIOUS STAGES:\n{self._workspace.get_context_for_downstream(4000)}"
            
            prompt = f"""{task_description}

## SOURCE MATERIAL:
{context[:6000]}
{workspace_context}

{prev_text}

## WRITE THIS SECTION:
### {name}
{instructions}

RULES:
- Write ONLY this section
- Maintain continuity with previous sections
- Ground all claims in source material
- Use [PLACEHOLDER: ...] for missing information
- Target the word count specified in instructions
"""
            
            response = self._generate(prompt, self._system_prompt)
            
            if response.success and response.content.strip():
                content = response.content.strip()
                written.append({"name": name, "content": content})
                
                # Stage each section
                if self._workspace:
                    self._workspace.stage(StagedResult(
                        task_name=f"section_{i+1}_{name.lower().replace(' ', '_')}",
                        content=content,
                        metadata={"section_index": i, "word_count": len(content.split())},
                    ))
                
                logger.info(f"[ITERATIVE] Wrote '{name}': {len(content)} chars")
            else:
                error = response.error if not response.success else "empty"
                logger.warning(f"[ITERATIVE] Failed '{name}': {error}")
                written.append({"name": name, "content": f"[GENERATION FAILED: {error}]"})
        
        return "\n\n---\n\n".join(f"## {s['name']}\n\n{s['content']}" for s in written)
    
    # =========================================================================
    # PATTERN 3: Parallel Independent Tasks (run concurrently → stage results)
    # Used by: analyzing multiple variables, reviewing multiple chapters
    # =========================================================================
    
    def run_parallel_tasks(
        self,
        tasks: List[Dict[str, str]],
        shared_context: str = "",
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, str]:
        """
        Run independent tasks in parallel, stage all results.
        
        Args:
            tasks: List of {"name": "task_name", "prompt": "what to do"}
            shared_context: Context available to all tasks
        Returns:
            Dict of task_name → result
        """
        results = {}
        
        def _run_task(task):
            name = task["name"]
            prompt = task["prompt"]
            if shared_context:
                prompt = f"## SHARED CONTEXT:\n{shared_context[:4000]}\n\n{prompt}"
            
            response = self._generate(prompt, self._system_prompt)
            if response.success and response.content.strip():
                return name, response.content.strip()
            return name, f"[FAILED: {response.error if not response.success else 'empty'}]"
        
        logger.info(f"[ITERATIVE] Running {len(tasks)} parallel tasks (max {self._max_parallel} concurrent)")
        
        with ThreadPoolExecutor(max_workers=self._max_parallel) as executor:
            futures = {executor.submit(_run_task, t): t["name"] for t in tasks}
            
            for future in as_completed(futures):
                task_name = futures[future]
                try:
                    name, content = future.result()
                    results[name] = content
                    
                    if self._workspace:
                        self._workspace.stage(StagedResult(
                            task_name=name,
                            content=content,
                        ))
                    
                    if progress_callback:
                        progress_callback(len(results), len(tasks), name)
                    
                    logger.info(f"[ITERATIVE] Parallel task done: {name}")
                except Exception as e:
                    logger.warning(f"[ITERATIVE] Parallel task failed: {task_name}: {e}")
                    results[task_name] = f"[FAILED: {e}]"
        
        return results
