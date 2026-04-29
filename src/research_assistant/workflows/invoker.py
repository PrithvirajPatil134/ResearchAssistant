"""
Workflow Invoker for Research Assistant.

Implements the complete agent workflow with loops:
1. read_files() → extracted_content
2. Learner.get_patterns() [warm start]
3. REASONING LOOP (max 5): Thinking → Analyst (score >= 9 to pass)
4. write_output()
5. VALIDATION LOOP (max 2): Reviewer checks input vs output
6. Learner.store_pattern()
7. Output file to personas/PERSONA/output/
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type
import logging
import sys
import threading
import time as time_module

logger = logging.getLogger(__name__)


def _extract_content(agent_output: str) -> str:
    """
    Extract actual content from kiro-cli agent output.
    
    Agent output contains tool noise, Python code, shell commands, etc.
    This finds the real markdown content — typically starts with a substantial
    markdown header like "# Publication Playbook" or "# SAI TEX LTD."
    """
    if not agent_output or len(agent_output) < 100:
        return agent_output
    
    lines = agent_output.split('\n')
    
    # Find the first line that looks like a real content header
    # Real headers: "# Publication Playbook", "# SAI TEX LTD.", "## 1. Opening Hook"
    # Not headers: "# Get first 1500 chars", "> Let me first read"
    noise_keywords = [
        'get ', 'import ', 'read ', 'extract ', 'let me', 'i will', 'i\'ll',
        'now let', 'running', 'execute', 'print(', 'cd /', 'using tool',
    ]
    
    best_start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Must start with # and be substantial
        if not stripped.startswith('#') or len(stripped) < 15:
            continue
        
        # Skip if it looks like code/tool noise
        header_lower = stripped.lower()
        if any(kw in header_lower for kw in noise_keywords):
            continue
        
        # Check next 3 lines aren't code
        next_chunk = '\n'.join(lines[i+1:i+4]).lower()
        if any(kw in next_chunk for kw in ['import ', 'def ', 'for ', 'try:', '= [', 'print(']):
            continue
        
        best_start = i
        break
    
    if best_start is not None:
        content = '\n'.join(lines[best_start:])
        logger.debug(f"[EXTRACT] Content at line {best_start}: {len(content)} chars")
        return content
    
    # Fallback: strip obvious noise lines
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Skip tool/code noise
        if any(stripped.startswith(p) for p in [
            '> ', 'import ', 'from ', 'def ', 'for ', 'try:', 'except',
            'print(', 'reader =', 'text =', 'I will run',
            'Reading file:', 'Reading directory:', '✓ Successfully',
            '- Completed in', '↱ Operation', 'Batch fs_',
            '⋮', '- Summary:', '(using tool:', 'Purpose:',
        ]):
            continue
        if stripped.startswith('```'):
            continue
        cleaned.append(line)
    
    return '\n'.join(cleaned).strip()


# =============================================================================
# Progress Indicator
# =============================================================================

class ProgressIndicator:
    """Simple terminal progress indicator - prints each stage once."""
    
    # Stage indices for update() calls
    STAGE_READ = 0
    STAGE_WARM = 1
    STAGE_REASON = 2
    STAGE_ANALYZE = 3
    STAGE_VALIDATE = 4
    STAGE_SAVE = 5
    
    STAGES = [
        ("📚", "ReaderAgent"),
        ("🔍", "LearnerAgent"),
        ("🧠", "ThinkingModule"),
        ("📊", "AnalystAgent"),
        ("✅", "ReviewerAgent"),
        ("💾", "OutputWriter"),
    ]
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled and sys.stdout.isatty()
        self.current_stage = -1
        self._printed_stages: set = set()
    
    def start(self, query: str) -> None:
        """Start the progress display."""
        if not self.enabled:
            return
        
        # Print header
        print(f"\n{'─' * 50}")
        print(f"🎯 {query[:45]}{'...' if len(query) > 45 else ''}")
        print(f"{'─' * 50}")
    
    def update(self, stage_idx: int, detail: str = "") -> None:
        """Print stage transition. Shows first occurrence with agent name, subsequent with detail only."""
        if not self.enabled:
            return
        
        if stage_idx < len(self.STAGES):
            emoji, agent = self.STAGES[stage_idx]
            detail_text = f" → {detail}" if detail else ""
            
            if stage_idx not in self._printed_stages:
                # First time seeing this stage — print full line
                self._printed_stages.add(stage_idx)
                self.current_stage = stage_idx
                print(f"  {emoji} {agent}{detail_text}")
            elif detail:
                # Repeated stage (e.g. reasoning iter 2/5) — print detail only
                print(f"     ↳ {detail}")
    
    def set_detail(self, detail: str) -> None:
        """Update detail for the current stage."""
        if self.enabled and detail:
            print(f"     ↳ {detail}")
    
    def log(self, message: str) -> None:
        """Print an important log message."""
        if self.enabled:
            print(f"     ↳ {message}")
    
    def show_timeout_estimate(self, timeout_seconds: int) -> None:
        """Show the estimated timeout so the user knows what to expect."""
        if not self.enabled:
            return
        minutes = timeout_seconds // 60
        secs = timeout_seconds % 60
        if minutes > 0:
            print(f"  ⏱️  Estimated max wait: {minutes}m {secs}s per LLM call")
        else:
            print(f"  ⏱️  Estimated max wait: {secs}s per LLM call")
    
    def stop(self, success: bool = True) -> None:
        """Stop the progress display."""
        if self.enabled:
            print(f"{'─' * 50}")
            if success:
                print("✅ Done")
            else:
                print("❌ Failed")
            print()


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class WorkflowResult:
    """Result of workflow execution."""
    success: bool
    workflow_name: str
    persona_name: str
    output_path: Optional[Path] = None
    error: Optional[str] = None
    artifacts: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: int = 0
    reasoning_iterations: int = 0
    validation_iterations: int = 0
    final_score: float = 0.0


@dataclass
class WorkflowSpec:
    """Specification for a workflow."""
    name: str
    description: str
    actions: List[Type["BaseAction"]]
    required_inputs: List[str]
    optional_inputs: List[str] = field(default_factory=list)


@dataclass
class ActionInput:
    """Input passed to each action."""
    workflow_id: str
    persona: Any  # Persona object
    state: Dict[str, Any]
    memory: Any  # Memory object
    output_dir: Path


@dataclass
class ActionResult:
    """Result from an action."""
    success: bool
    action_name: str
    artifacts: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    content: Optional[str] = None  # Generated content


class BaseAction:
    """Base class for workflow actions."""
    
    name: str = "base"
    
    def execute(self, input: ActionInput) -> ActionResult:
        raise NotImplementedError


# =============================================================================
# Main Workflow Invoker
# =============================================================================

class WorkflowInvoker:
    """
    Unified interface for invoking research workflows.
    
    Implements the full workflow with:
    - File reading with ReaderAgent
    - Pattern-based warm start from LearnerAgent
    - Reasoning loop with AnalystAgent scoring (max 5 iterations)
    - Validation loop with ReviewerAgent (max 2 iterations)
    - Pattern storage for future learning
    """
    
    WORKFLOWS: Dict[str, WorkflowSpec] = {}
    _defaults_registered: bool = False
    
    # Loop configuration
    MAX_REASONING_ITERATIONS = 5
    MIN_SCORE_THRESHOLD = 9.0
    MAX_VALIDATION_ITERATIONS = 2
    
    @classmethod
    def register(cls, spec: WorkflowSpec) -> None:
        """Register a workflow specification."""
        cls.WORKFLOWS[spec.name] = spec
        logger.debug(f"Registered workflow: {spec.name}")
    
    @classmethod
    def list_workflows(cls) -> List[str]:
        """List available workflow names."""
        cls._ensure_defaults_registered()
        return list(cls.WORKFLOWS.keys())
    
    @classmethod
    def get_spec(cls, name: str) -> Optional[WorkflowSpec]:
        """Get workflow specification by name."""
        cls._ensure_defaults_registered()
        return cls.WORKFLOWS.get(name)
    
    @staticmethod
    def _detect_file_pairs(file_paths: List[str]) -> bool:
        """Detect if file paths contain paired files (e.g., teaching note + case study).
        
        Heuristic: if files come in pairs where one references the other
        (e.g., 'Vinder Oils Ltd. Teaching Notes_C4.pdf' paired with 'C4.pdf'),
        return True so batch_size=2 keeps pairs together.
        """
        import re
        basenames = [p.split('/')[-1] for p in file_paths]
        # Count files that look like case references (C2.pdf, C4.pdf, etc.)
        case_pattern = re.compile(r'^C\d+\.pdf$', re.IGNORECASE)
        case_files = [b for b in basenames if case_pattern.match(b)]
        # If roughly half the files are case references, we likely have pairs
        return len(case_files) >= 2 and len(case_files) >= len(basenames) * 0.3
    
    @classmethod
    def _detect_stages(cls, query: str) -> List[Dict[str, str]]:
        """
        Detect if a query contains multiple logical stages (STEP 1, STEP 2, etc.)
        and split them into separate focused prompts.
        
        Returns a list of stage dicts: [{"name": "...", "prompt": "..."}]
        If the query is simple (no stages), returns a single-element list.
        """
        import re
        
        # Look for explicit step markers
        step_pattern = re.compile(
            r'(?:^|\n)\s*(?:STEP\s+(\d+)|Step\s+(\d+)|(\d+)\s*[\.\)]\s*(?:—|-))\s*(?:—|-|:)?\s*(.*?)(?=\n\s*(?:STEP\s+\d|Step\s+\d|\d+\s*[\.\)]\s*(?:—|-))|\Z)',
            re.DOTALL | re.IGNORECASE
        )
        
        matches = list(step_pattern.finditer(query))
        
        if len(matches) < 2:
            # Not a multi-step query — return as single stage
            return [{"name": "main", "prompt": query}]
        
        stages = []
        for match in matches:
            step_num = match.group(1) or match.group(2) or match.group(3)
            step_title = match.group(4).strip().split('\n')[0]  # First line as title
            step_content = match.group(0).strip()
            
            stages.append({
                "name": f"step_{step_num}_{step_title[:30].replace(' ', '_').lower()}",
                "prompt": step_content,
            })
        
        # Add any preamble before the first step as context
        first_step_start = matches[0].start()
        preamble = query[:first_step_start].strip()
        if preamble:
            for stage in stages:
                stage["preamble"] = preamble
        
        logger.info(f"[WORKFLOW] Detected {len(stages)} stages in query")
        for s in stages:
            logger.info(f"  → {s['name']}")
        
        return stages
    
    @classmethod
    def invoke(
        cls,
        workflow_name: str,
        persona_name: str,
        initial_state: Dict[str, Any],
        output_format: str = "md",
        personas_dir: Optional[Path] = None,
        show_progress: bool = True,
        perf_overrides: Optional[Dict[str, Any]] = None,
    ) -> WorkflowResult:
        """
        Invoke a workflow with full agent orchestration.
        
        Workflow:
        1. read_files() → extracted_content
        2. Learner.get_patterns() [warm start]
        3. REASONING LOOP (max 5): Thinking → Analyst (score >= 9?)
        4. write_output()
        5. VALIDATION LOOP (max 2): Reviewer validates output
        6. Learner.store_pattern()
        7. Output file
        
        perf_overrides: Dict of performance config overrides from CLI flags.
            Keys: parallel_eval_enabled, max_reasoning_iterations,
                  learner_llm_calls, cross_space_enabled, session_memory_enabled
        """
        import time
        start_time = time.time()
        
        cls._ensure_defaults_registered()
        
        # Load performance config (defaults + yaml + env + CLI overrides)
        from research_assistant.config import Config
        config = Config.load()
        perf = config.performance
        if perf_overrides:
            for key, value in perf_overrides.items():
                if hasattr(perf, key):
                    setattr(perf, key, value)
        
        cls._ensure_defaults_registered()
        
        # Initialize progress indicator
        progress = ProgressIndicator(enabled=show_progress)
        query = initial_state.get("topic", initial_state.get("task", initial_state.get("assignment", "")))
        progress.start(query)
        
        # Get workflow spec
        spec = cls.WORKFLOWS.get(workflow_name)
        if not spec:
            progress.stop(success=False)
            return WorkflowResult(
                success=False,
                workflow_name=workflow_name,
                persona_name=persona_name,
                error=f"Unknown workflow: {workflow_name}. Available: {list(cls.WORKFLOWS.keys())}",
            )
        
        # Validate required inputs
        missing = [k for k in spec.required_inputs if k not in initial_state]
        if missing:
            progress.stop(success=False)
            return WorkflowResult(
                success=False,
                workflow_name=workflow_name,
                persona_name=persona_name,
                error=f"Missing required inputs: {missing}",
            )
        
        # Load space (persona)
        try:
            from research_assistant.spaces import SpaceLoader
            
            spaces_path = personas_dir or Path(__file__).parent.parent / "spaces"
            loader = SpaceLoader(spaces_path)
            persona = loader.load(persona_name)
        except Exception as e:
            progress.stop(success=False)
            return WorkflowResult(
                success=False,
                workflow_name=workflow_name,
                persona_name=persona_name,
                error=f"Failed to load persona: {e}",
            )
        
        # Initialize core components
        try:
            from research_assistant.core import Memory, ContextGuardAgent, ThinkingModule
            from research_assistant.agents import (
                ReaderAgent, LearnerAgent, AnalystAgent, ReviewerAgent
            )
            
            memory = Memory()
            memory.set_persona(persona.name, persona.to_context())
            
            # Initialize context guard with token limits
            context_guard = ContextGuardAgent(
                max_tokens=100000,  # 100K token budget
                threshold=0.70,
                warning=0.60,
            )
            
            # Initialize agents
            reader = ReaderAgent(memory, context_guard)
            learner = LearnerAgent(memory, context_guard)
            analyst = AnalystAgent(memory, context_guard)
            reviewer = ReviewerAgent(memory, context_guard)
            thinking = ThinkingModule()
            
            # Validate agent wiring (Enhancement 4: Agent Protocol)
            from research_assistant.agents.base import validate_agent_wiring
            wiring_errors = validate_agent_wiring(reader, analyst, reviewer, learner)
            if wiring_errors:
                progress.stop(success=False)
                return WorkflowResult(
                    success=False,
                    workflow_name=workflow_name,
                    persona_name=persona_name,
                    error=f"Agent wiring errors: {'; '.join(wiring_errors)}",
                )
            
            # Load cross-space knowledge if enabled (Enhancement 1)
            if perf.cross_space_enabled:
                cross_sources = loader.load_cross_space_knowledge(
                    primary_space=persona,
                    cross_space_enabled=True,
                )
                if cross_sources:
                    reader.set_cross_space_sources(cross_sources)
                    logger.info(f"[WORKFLOW] Cross-space: {len(cross_sources)} sources loaded")
            
        except Exception as e:
            progress.stop(success=False)
            return WorkflowResult(
                success=False,
                workflow_name=workflow_name,
                persona_name=persona_name,
                error=f"Failed to initialize components: {e}",
            )
        
        # Create output directory
        workflow_id = f"{workflow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_dir = persona.persona_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        artifacts_dir = persona.persona_dir / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        
        # Track metrics
        reasoning_iterations = 0
        validation_iterations = 0
        final_score = 0.0
        
        try:
            # =========================================================
            # STEP 1: READ FILES - Extract content from knowledge base
            # =========================================================
            progress.update(ProgressIndicator.STAGE_READ, "scanning KB")
            
            knowledge_dir = persona.persona_dir / "knowledge"
            
            reader.set_knowledge_dir(knowledge_dir)
            read_result = reader.execute(query=query, knowledge_dir=knowledge_dir)
            
            extracted_content = []
            if read_result.success and read_result.output:
                extracted_content = [
                    c.content for c in read_result.output 
                    if hasattr(c, 'content')
                ]
            
            progress.set_detail(f"{len(extracted_content)} files")
            logger.info(f"[WORKFLOW] Extracted {len(extracted_content)} content pieces")
            
            # =========================================================
            # STEP 1.5: BUILD DISPATCH CONTRACT (Level 3)
            # =========================================================
            from research_assistant.core.dispatch_contract import build_dispatch_contract
            try:
                from research_assistant.core import get_llm_client as _get_llm
                _contract_llm = _get_llm()
            except Exception:
                _contract_llm = None
            
            dispatch_contract = build_dispatch_contract(
                query=query,
                workflow_name=workflow_name,
                extracted_content=extracted_content,
                persona_name=persona.name,
                llm=_contract_llm,
            )
            logger.info(f"[WORKFLOW] Contract built: skip_evaluator={dispatch_contract.skip_evaluator}")
            
            # Store contract in memory for all agents to reference
            from research_assistant.core.memory import MemoryType
            memory.store(
                key="dispatch_contract",
                value=dispatch_contract.to_dict(),
                memory_type=MemoryType.CONTEXT,
                source_agent="workflow",
                importance=9,
            )
            
            # =========================================================
            # STEP 2: WARM START - Get patterns from learner
            # =========================================================
            progress.update(ProgressIndicator.STAGE_WARM, "checking history")
            
            # Load lessons from previous runs
            lessons = learner.load_lessons(persona.persona_dir)
            lessons_prompt = learner.get_lessons_for_prompt()
            
            # Load session memory if enabled (Enhancement 2)
            session_memory_prompt = ""
            if perf.session_memory_enabled:
                session_memory_prompt = learner.load_session_memory(persona.persona_dir)
            
            patterns = learner.get_patterns(query)
            warm_start_prompt = patterns.get("warm_start_prompt")
            suggested_strategies = patterns.get("suggested_strategies", [])
            
            if patterns.get("found"):
                progress.set_detail(f"{len(suggested_strategies)} patterns")
                logger.info(f"[WORKFLOW] Warm start: {len(suggested_strategies)} strategies")
            else:
                progress.set_detail("cold start")
                logger.info("[WORKFLOW] No similar patterns found, cold start")
            
            # =========================================================
            # STEP 3: REASONING LOOP - Generate and score until pass
            # =========================================================
            reasoning_content = ""
            analyst_feedback = ""
            previous_output = ""
            
            # Show estimated timeout to user before entering the reasoning loop
            from research_assistant.core.llm import LLMClient as _LLMClient
            est_timeout = _LLMClient.estimate_timeout(
                prompt=query,
                kb_file_count=len(extracted_content),
                workflow_name=workflow_name,
            )
            progress.show_timeout_estimate(est_timeout)
            
            # Detect multi-step queries and break into stages
            stages = cls._detect_stages(query)
            is_staged = len(stages) > 1
            
            if is_staged:
                progress.log(f"Multi-step query detected: {len(stages)} stages")
                
                from research_assistant.core.artifact_cache import ArtifactCache
                from research_assistant.core import get_llm_client
                
                # Try to reuse cache from most recent run with same workflow+stages
                cache_base = persona.persona_dir / "cache"
                cache_dir = cache_base / workflow_id
                
                # Check if a previous run has cached stages we can reuse
                if cache_base.exists():
                    stage_names = {s["name"] for s in stages}
                    for prev_dir in sorted(cache_base.iterdir(), reverse=True):
                        if prev_dir.is_dir() and prev_dir.name.startswith(workflow_name + "_"):
                            # Check if it has any of our stages cached
                            cached_stages = {f.stem for f in prev_dir.glob("*.md") if not f.name.startswith("_")}
                            reusable = stage_names & cached_stages
                            if reusable and prev_dir != cache_dir:
                                logger.info(f"[WORKFLOW] Reusing {len(reusable)} cached stages from {prev_dir.name}")
                                cache_dir = prev_dir  # Reuse the previous cache
                                break
                
                cache = ArtifactCache(cache_dir)
                llm = get_llm_client()
                
                # Create timestamped artifacts folder for this run
                import datetime as _dt
                pst = _dt.timezone(_dt.timedelta(hours=-7))
                run_ts = datetime.now(pst).strftime('%Y%m%d_%H%M%S_PST')
                artifacts_run_dir = persona.persona_dir / "artifacts" / f"{workflow_name}_{run_ts}"
                artifacts_run_dir.mkdir(parents=True, exist_ok=True)
                
                # Build persona system prompt — kiro-cli runs as full agent
                identity = persona.identity
                prof_name = identity.get("name", "Professor")
                institution = identity.get("institution", "University")
                expertise = identity.get("expertise", [])
                sys_prompt = cls._build_system_prompt(
                    workflow_name, prof_name, institution, expertise, persona
                )
                sys_prompt += f"""
You are an expert researcher and writer. You have full access to read files and use tools.
Complete the task thoroughly. Output your response as well-structured markdown.
Do NOT ask follow-up questions — complete the FULL task in one response.

CRITICAL FILE RULES:
- NEVER create or modify files in the knowledge/ directory — it is READ-ONLY source material.
- NEVER write intermediate files (drafts, analyses, extractions, batch outputs) to the output/ directory.
- For ANY intermediate files you create, save them to: {artifacts_run_dir}
- The output/ directory is ONLY for the final user-requested deliverable.
- Output your content as your response text — do NOT write it to a file unless explicitly asked."""
                
                if lessons_prompt:
                    sys_prompt += f"\n\n{lessons_prompt}"
                
                if session_memory_prompt:
                    sys_prompt += f"\n\n{session_memory_prompt}"
                
                stage_outputs = []
                seen_agent_files = set()  # Track files already claimed by previous stages
                
                for stage_idx, stage in enumerate(stages):
                    stage_name = stage["name"]
                    stage_query = stage["prompt"]
                    preamble = stage.get("preamble", "")
                    
                    # Check cache first
                    cached = cache.get_stage(stage_name)
                    if cached:
                        progress.update(
                            ProgressIndicator.STAGE_REASON,
                            f"stage {stage_idx + 1}/{len(stages)}: {stage_name} (cached)"
                        )
                        stage_outputs.append(cached)
                        continue
                    
                    progress.update(
                        ProgressIndicator.STAGE_REASON,
                        f"stage {stage_idx + 1}/{len(stages)}: {stage_name}"
                    )
                    
                    # Mark stage start time for file detection
                    stage_start_time = time.time()
                    
                    # Build stage prompt with previous stage context (compressed + cleaned)
                    prompt = ""
                    if preamble:
                        prompt += preamble + "\n\n"
                    prompt += stage_query
                    
                    if stage_outputs:
                        from research_assistant.core.parallel_agents import ParallelAgentOrchestrator
                        # For the final stage (writing), include ALL previous stages
                        # with generous budget — it needs the full playbook + guide + template + case
                        is_final_stage = (stage_idx == len(stages) - 1)
                        
                        if is_final_stage:
                            # Level 3: Inject recitation checkpoint before final stage
                            from research_assistant.core.recitation import build_recitation_block, build_stage_summary
                            _stage_sums = [
                                build_stage_summary(
                                    stages[si]["name"] if si < len(stages) else f"stage_{si}",
                                    _extract_content(so)
                                )
                                for si, so in enumerate(stage_outputs)
                            ]
                            _recitation = build_recitation_block(
                                original_query=query,
                                contract=dispatch_contract,
                                stage_summaries=_stage_sums,
                            )
                            prompt = _recitation + "\n\n" + prompt
                            
                            # Final stage gets ALL previous stages with higher char budget
                            cleaned_outputs = [_extract_content(so) for so in stage_outputs]
                            # Give each stage proportional space, total ~20K chars
                            per_stage_budget = max(4000, 20000 // len(cleaned_outputs))
                            compressed_parts = []
                            for si, so in enumerate(cleaned_outputs):
                                stage_label = stages[si]["name"] if si < len(stages) else f"stage_{si}"
                                compressed = ParallelAgentOrchestrator.compress_for_downstream(
                                    so, max_chars=per_stage_budget
                                )
                                compressed_parts.append(f"### {stage_label}:\n{compressed}")
                            prompt += f"\n\n## OUTPUT FROM ALL PREVIOUS STAGES:\n" + "\n\n---\n\n".join(compressed_parts)
                        else:
                            # Intermediate stages get last 2 stages compressed
                            cleaned_outputs = [_extract_content(so) for so in stage_outputs[-2:]]
                            compressed_prev = ParallelAgentOrchestrator.compress_for_downstream(
                                "\n\n---\n\n".join(cleaned_outputs), max_chars=6000
                            )
                            prompt += f"\n\n## OUTPUT FROM PREVIOUS STAGES:\n{compressed_prev}"
                    
                    # Detect if this stage involves analyzing multiple documents
                    stage_lower = stage_query.lower()
                    is_multi_doc = any(kw in stage_lower for kw in [
                        "analyze all", "read and analyze", "for each case", "each case",
                        "benchmark", "all published", "c2 through", "every case",
                        "all papers", "all articles", "each paper", "each article",
                        "all chapters", "each chapter", "all sources",
                    ])
                    
                    # Extract file paths referenced in this stage's query
                    from research_assistant.agents.reader import ReaderAgent as _R
                    _tmp_reader = _R.__new__(_R)
                    stage_file_paths = _tmp_reader._extract_all_file_paths(stage_query)
                    
                    if is_multi_doc and len(stage_file_paths) > 3:
                        # PARALLEL AGENT PATH — split files into batches, run concurrently
                        from research_assistant.core.parallel_agents import ParallelAgentOrchestrator
                        from research_assistant.core.workflow_sections import get_extraction_prompt, get_synthesis_prompt
                        
                        file_path_strs = [str(p) for p in stage_file_paths]
                        
                        # Detect paired files (teaching note + case study pairs)
                        # and use batch_size=2 to keep pairs together
                        has_pairs = cls._detect_file_pairs(file_path_strs)
                        batch_sz = 2 if has_pairs else 3
                        
                        orchestrator = ParallelAgentOrchestrator(
                            llm=llm, system_prompt=sys_prompt,
                            max_parallel=3, batch_size=batch_sz, stagger_delay=15.0,
                        )
                        
                        def _par_cb(done, total, status):
                            progress.set_detail(f"parallel: {status}")
                        
                        progress.log(f"Parallel analysis: {len(file_path_strs)} files → {(len(file_path_strs) + 4) // 5} agents")
                        
                        stage_output = orchestrator.analyze_documents_parallel(
                            file_paths=file_path_strs,
                            extraction_task=get_extraction_prompt(workflow_name, query),
                            synthesis_task=get_synthesis_prompt(workflow_name, query),
                            progress_callback=_par_cb,
                        )
                        reasoning_iterations += (len(file_path_strs) + 4) // 5 + 1  # batches + synthesis
                    
                    else:
                        # SINGLE AGENT PATH — one kiro-cli agent handles the stage
                        from research_assistant.core.llm import LLMClient as _LC
                        est = _LC.estimate_timeout(prompt, len(extracted_content), workflow_name)
                        
                        # Boost timeout for final writing stage — it produces 15-20 pages
                        is_writing_stage = (stage_idx == len(stages) - 1) and any(
                            kw in stage_query.lower() for kw in ['write', 'generate', 'produce', 'create', 'deliver']
                        )
                        if is_writing_stage:
                            est = max(est, 1200)  # At least 20 minutes for comprehensive writing
                        
                        llm.timeout_seconds = max(llm.timeout_seconds, est)
                        
                        logger.info(f"[WORKFLOW] Stage {stage_idx+1}: {stage_name} (single agent, timeout={llm.timeout_seconds}s)")
                        
                        response = llm.generate_as_agent(prompt, sys_prompt)
                        
                        if response.success and response.content.strip():
                            stage_output = response.content.strip()
                            
                            # Detect truncation — auto-continue (up to 3 continuations)
                            max_continuations = 3
                            for cont_attempt in range(max_continuations):
                                is_truncated = (
                                    len(stage_output) > 1000
                                    and stage_output[-1] not in '.!?"\')\]\n—–|}\n*'
                                    and not stage_output.rstrip().endswith('---')
                                    and not stage_output.rstrip().endswith('*')
                                )
                                if not is_truncated:
                                    break  # Output ends properly
                                
                                logger.warning(f"[WORKFLOW] Output truncated (attempt {cont_attempt+1}), requesting continuation")
                                progress.set_detail(f"continuing truncated output ({cont_attempt+1}/{max_continuations})...")
                                
                                # Give the continuation agent more context — include the
                                # original task description so it knows what it's completing
                                task_summary = stage_query[:300] if len(stage_query) > 300 else stage_query
                                cont_prompt = (
                                    f"You were working on this task:\n{task_summary}\n\n"
                                    f"Your previous response was truncated. The last 800 characters were:\n\n"
                                    f"...{stage_output[-800:]}\n\n"
                                    f"Continue from EXACTLY where you left off. Do NOT repeat any content. "
                                    f"Do NOT start over. Just complete the remaining sections."
                                )
                                
                                # Use shorter timeout for continuations — if it stalls, bail
                                saved_timeout = llm.timeout_seconds
                                llm.timeout_seconds = min(saved_timeout, 600)  # Max 10 min for continuation
                                
                                # Use shorter stall threshold for continuations (3 min vs 10 min)
                                cont = llm.generate_as_agent(cont_prompt, sys_prompt, stall_override=180)
                                llm.timeout_seconds = saved_timeout  # Restore
                                
                                if cont.success and cont.content.strip():
                                    cont_content = cont.content.strip()
                                    # Only append if the continuation is substantial (not just a stall fragment)
                                    if len(cont_content) > 200:
                                        stage_output += "\n\n" + cont_content
                                        reasoning_iterations += 1
                                    else:
                                        logger.warning(f"[WORKFLOW] Continuation too short ({len(cont_content)} chars), skipping")
                                        break
                                else:
                                    logger.warning(f"[WORKFLOW] Continuation failed, accepting truncated output")
                                    break  # Can't continue further
                        elif not response.success:
                            raise RuntimeError(f"Stage {stage_name} failed: {response.error}")
                        else:
                            raise RuntimeError(f"Stage {stage_name} returned empty content")
                        
                        reasoning_iterations += 1
                    
                    # Check if the agent wrote output to a file instead of stdout
                    # (kiro-cli agents often create files directly)
                    # Only consider files created AFTER this stage started, and not already claimed
                    # Only check the run-specific artifacts dir and output/ — NOT the parent artifacts/
                    new_files = []
                    check_dirs = [artifacts_run_dir, persona.persona_dir / "output"]
                    import os
                    for check_dir in check_dirs:
                        if check_dir.exists():
                            for f in check_dir.glob("*.md"):
                                if f.name == ".DS_Store" or str(f) in seen_agent_files:
                                    continue
                                # Only files created/modified AFTER this stage started
                                if f.stat().st_mtime >= stage_start_time:
                                    # Skip our own workflow output files (guide_*, explain_*, etc.)
                                    if not any(f.name.startswith(p + "_2") for p in ["guide", "explain", "review", "research", "quant"]):
                                        new_files.append(f)
                    
                    if new_files:
                        # Agent wrote to file — use the largest new file as the stage output
                        new_files.sort(key=lambda f: f.stat().st_size, reverse=True)
                        best_file = new_files[0]
                        file_content = best_file.read_text()
                        if len(file_content) > len(_extract_content(stage_output)):
                            logger.info(f"[WORKFLOW] Agent wrote to file: {best_file.name} ({len(file_content)} chars) — using as stage output")
                            progress.set_detail(f"using agent file: {best_file.name}")
                            stage_output = file_content
                        # Mark this file as claimed so later stages don't reuse it
                        seen_agent_files.add(str(best_file))
                        # Move the file to artifacts if it was written to output/
                        if best_file.parent.name == "output":
                            dest = artifacts_run_dir / best_file.name
                            try:
                                import shutil
                                shutil.move(str(best_file), str(dest))
                                logger.info(f"[WORKFLOW] Moved agent file from output/ to artifacts/: {best_file.name}")
                                # Update seen_agent_files with new path
                                seen_agent_files.discard(str(best_file))
                                seen_agent_files.add(str(dest))
                            except Exception as e:
                                logger.warning(f"[WORKFLOW] Failed to move {best_file.name}: {e}")
                    
                    cache.put_stage(stage_name, stage_output)
                    stage_outputs.append(stage_output)
                    progress.set_detail(f"stage {stage_idx + 1} complete ({len(stage_output)} chars)")
                
                # Combine all stage outputs — extract clean content from each
                reasoning_content = "\n\n---\n\n".join(
                    _extract_content(so) for so in stage_outputs
                )
                
                # Score + retry loop (max 2 retries, re-run last stage with feedback)
                max_retries = 2
                for retry in range(max_retries + 1):
                    progress.update(
                        ProgressIndicator.STAGE_ANALYZE,
                        f"scoring {'output' if retry == 0 else f'revision {retry}'}"
                    )
                    score_result = analyst.execute(
                        query=query, reasoning=reasoning_content,
                        knowledge_content=extracted_content, iteration=retry,
                        contract=dispatch_contract,
                    )
                    score = score_result.output
                    final_score = score.overall
                    analyst_feedback = score.feedback
                    progress.set_detail(f"score: {final_score:.1f}/10")
                    
                    if score.passed:
                        break
                    if retry >= max_retries:
                        break
                    
                    # Re-run last stage as agent with feedback
                    last = stages[-1]
                    progress.update(ProgressIndicator.STAGE_REASON, f"revising with feedback (attempt {retry+1})")
                    
                    retry_prompt = ""
                    if last.get("preamble"):
                        retry_prompt += last["preamble"] + "\n\n"
                    retry_prompt += last["prompt"]
                    if len(stage_outputs) > 1:
                        retry_prompt += "\n\n## PREVIOUS STAGES:\n" + "\n\n---\n\n".join(so[:8000] for so in stage_outputs[:-1])
                    retry_prompt += f"\n\n## ANALYST FEEDBACK:\n{analyst_feedback}"
                    retry_prompt += f"\n\n## YOUR PREVIOUS ATTEMPT (improve on this):\n{stage_outputs[-1][:5000]}"
                    
                    r = llm.generate_as_agent(retry_prompt, sys_prompt)
                    if r.success and r.content.strip():
                        stage_outputs[-1] = r.content.strip()
                        reasoning_content = "\n\n---\n\n".join(stage_outputs)
                        cache.put_stage(last["name"], stage_outputs[-1])
                        reasoning_iterations += 1
            
            else:
                # Standard single-stage reasoning loop
                for iteration in range(cls.MAX_REASONING_ITERATIONS):
                    reasoning_iterations = iteration + 1
                    
                    # Update progress for reasoning
                    progress.update(ProgressIndicator.STAGE_REASON, f"iter {iteration + 1}/{cls.MAX_REASONING_ITERATIONS}")
                    
                    # Generate reasoning with LLM
                    reasoning_content = cls._generate_reasoning(
                        query=query,
                        persona=persona,
                        extracted_content=extracted_content,
                        warm_start_prompt=warm_start_prompt,
                        previous_feedback=analyst_feedback,
                        iteration=iteration,
                        thinking=thinking,
                        previous_output=previous_output,
                        workflow_name=workflow_name,
                        lessons_prompt=lessons_prompt,
                    )
                    
                    # Update progress for analysis
                    progress.update(ProgressIndicator.STAGE_ANALYZE, f"scoring iter {iteration + 1}")
                    
                    # Score with analyst (with contract for Level 3)
                    score_result = analyst.execute(
                        query=query,
                        reasoning=reasoning_content,
                        knowledge_content=extracted_content,
                        iteration=iteration,
                        contract=dispatch_contract,
                    )
                    
                    score = score_result.output
                    final_score = score.overall
                    
                    progress.set_detail(f"score: {final_score:.1f}/10")
                    logger.info(
                        f"[WORKFLOW] Reasoning iteration {iteration + 1}: "
                        f"Score {final_score}/10 ({'PASS' if score.passed else 'RETRY'})"
                    )
                    
                    if score.passed:
                        break
                    
                    # Save current output and get feedback for next iteration
                    previous_output = reasoning_content
                    analyst_feedback = score.feedback
            
            # =========================================================
            # STEP 4: RECITATION CHECKPOINT + FORMAT OUTPUT (Level 3)
            # =========================================================
            from research_assistant.core.recitation import build_recitation_block, build_stage_summary
            
            # Build recitation block to re-anchor on original intent
            stage_summaries = None
            if is_staged and stage_outputs:
                stage_summaries = [
                    build_stage_summary(stages[i]["name"] if i < len(stages) else f"stage_{i}", so)
                    for i, so in enumerate(stage_outputs)
                ]
            
            recitation = build_recitation_block(
                original_query=query,
                contract=dispatch_contract,
                stage_summaries=stage_summaries,
            )
            logger.info(f"[WORKFLOW] Recitation checkpoint: {len(recitation)} chars")
            
            final_content = cls._format_output(
                workflow_name=workflow_name,
                query=query,
                reasoning=reasoning_content,
                persona=persona,
                score=final_score,
                iterations=reasoning_iterations,
            )
            
            # =========================================================
            # STEP 5: PARALLEL EVALUATION (Level 3)
            # Analyst + Reviewer + Evaluator run concurrently
            # =========================================================
            from research_assistant.core.parallel_eval import run_parallel_evaluation
            
            progress.update(ProgressIndicator.STAGE_VALIDATE, "parallel eval (analyst+reviewer+evaluator)")
            
            try:
                eval_llm = _contract_llm
            except NameError:
                try:
                    from research_assistant.core import get_llm_client as _get_llm2
                    eval_llm = _get_llm2()
                except Exception:
                    eval_llm = None
            
            unified_eval = run_parallel_evaluation(
                content=final_content,
                query=query,
                extracted_content=extracted_content,
                contract=dispatch_contract,
                analyst=analyst,
                reviewer=reviewer,
                workflow_name=workflow_name,
                persona_name=persona.name,
                iteration=reasoning_iterations,
                llm=eval_llm,
            )
            
            # Update scores from unified evaluation
            final_score = unified_eval.analyst_score
            validation_passed = unified_eval.overall_pass
            validation_iterations = 1
            
            progress.set_detail(
                f"analyst={unified_eval.analyst_score:.1f} "
                f"reviewer={unified_eval.reviewer_score:.1f} "
                f"eval=({unified_eval.evaluator_alignment},{unified_eval.evaluator_evidence},"
                f"{unified_eval.evaluator_completeness},{unified_eval.evaluator_actionability})"
            )
            
            # If parallel eval fails and not staged, attempt one revision
            if not unified_eval.overall_pass and not is_staged:
                progress.set_detail("revising based on parallel eval feedback")
                logger.info(f"[WORKFLOW] Parallel eval failed, revising with feedback")
                
                # Use combined feedback from all evaluators
                combined_feedback = unified_eval.revision_prompt
                
                reasoning_content = cls._generate_reasoning(
                    query=query,
                    persona=persona,
                    extracted_content=extracted_content,
                    warm_start_prompt=warm_start_prompt,
                    previous_feedback=combined_feedback,
                    iteration=reasoning_iterations,
                    thinking=thinking,
                    workflow_name=workflow_name,
                    lessons_prompt=lessons_prompt,
                )
                
                final_content = cls._format_output(
                    workflow_name=workflow_name,
                    query=query,
                    reasoning=reasoning_content,
                    persona=persona,
                    score=final_score,
                    iterations=reasoning_iterations + 1,
                )
                validation_iterations = 2
            
            # =========================================================
            # STEP 6: STORE PATTERN - Save for future learning
            # =========================================================
            progress.update(ProgressIndicator.STAGE_SAVE, "storing pattern")
            
            pattern = learner.store_pattern(
                query=query,
                reasoning=reasoning_content,
                score=final_score,
                feedback=analyst_feedback,
            )
            
            # Update workflow doc with learned pattern (if score was good)
            if pattern and final_score >= 8.0:
                strategies = pattern.strategies if pattern.strategies else ["KB grounding"]
                learner.update_workflow_doc(
                    persona_dir=persona.persona_dir,
                    workflow_name=workflow_name,
                    query=query,
                    approach=strategies[0] if strategies else "structured explanation",
                    score=final_score,
                    success_factor="Passed analyst scoring",
                )
            
            # Store compacted lesson from this run (always, regardless of score)
            lesson = learner.extract_lesson_with_llm(
                query=query,
                reasoning=reasoning_content,
                score=final_score,
                feedback=analyst_feedback or "No feedback",
            )
            if lesson:
                learner.store_lesson(persona.persona_dir, lesson, query, final_score)
            
            # Save session memory for cross-session persistence (Enhancement 2)
            if perf.session_memory_enabled:
                # Collect cross-space origins from extracted content
                cross_origins = [
                    c.metadata.get("cross_space_origin")
                    for c in (extracted_content if isinstance(extracted_content, list) and extracted_content and hasattr(extracted_content[0], 'metadata') else [])
                    if hasattr(c, 'metadata') and c.metadata.get("cross_space_origin")
                ]
                # Collect strategies from learner patterns
                pattern_strategies = pattern.strategies if (pattern and hasattr(pattern, 'strategies')) else []
                
                try:
                    _session_llm = None
                    if perf.learner_llm_calls:
                        try:
                            from research_assistant.core import get_llm_client as _get_session_llm
                            _session_llm = _get_session_llm()
                        except Exception:
                            pass
                    
                    learner.save_session_memory(
                        persona_dir=persona.persona_dir,
                        query=query,
                        score=final_score,
                        strategies=pattern_strategies,
                        cross_space_origins=cross_origins,
                        llm=_session_llm,
                    )
                except Exception as e:
                    logger.warning(f"[WORKFLOW] Session memory save failed (non-fatal): {e}")
            
            # =========================================================
            # STEP 7: WRITE OUTPUT FILE
            # =========================================================
            progress.set_detail("writing file")
            
            output_path = output_dir / f"{workflow_id}.{output_format}"
            output_path.write_text(final_content)
            
            execution_time = int((time.time() - start_time) * 1000)
            
            # =========================================================
            # STEP 8: LOG WORKFLOW EXECUTION
            # =========================================================
            cls._log_workflow_execution(
                workflow_name=workflow_name,
                persona_name=persona_name,
                query=query,
                output_path=output_path,
                score=final_score,
                reasoning_iterations=reasoning_iterations,
                validation_iterations=validation_iterations,
                execution_time_ms=execution_time,
                eval_data={
                    "analyst_score": unified_eval.analyst_score,
                    "reviewer_score": unified_eval.reviewer_score,
                    "evaluator": {
                        "alignment": unified_eval.evaluator_alignment,
                        "evidence": unified_eval.evaluator_evidence,
                        "completeness": unified_eval.evaluator_completeness,
                        "actionability": unified_eval.evaluator_actionability,
                    },
                    "overall_pass": unified_eval.overall_pass,
                },
            )
            
            progress.stop(success=True)
            
            return WorkflowResult(
                success=True,
                workflow_name=workflow_name,
                persona_name=persona_name,
                output_path=output_path,
                artifacts={
                    "query": query,
                    "extracted_files": len(extracted_content),
                    "patterns_used": patterns.get("found", False),
                },
                execution_time_ms=execution_time,
                reasoning_iterations=reasoning_iterations,
                validation_iterations=validation_iterations,
                final_score=final_score,
            )
            
        except Exception as e:
            logger.exception(f"[WORKFLOW] Error: {e}")
            progress.stop(success=False)
            return WorkflowResult(
                success=False,
                workflow_name=workflow_name,
                persona_name=persona_name,
                error=str(e),
                reasoning_iterations=reasoning_iterations,
                validation_iterations=validation_iterations,
            )
    
    
    @classmethod
    def _generate_reasoning(
        cls,
        query: str,
        persona: Any,
        extracted_content: List[str],
        warm_start_prompt: Optional[str],
        previous_feedback: str,
        iteration: int,
        thinking: Any,
        previous_output: str = "",
        workflow_name: str = "explain",
        lessons_prompt: str = "",
    ) -> str:
        """Generate reasoning content using LLM with persona context."""
        from research_assistant.core import get_llm_client
        from research_assistant.core.thinking import ReasoningType
        
        # Start reasoning chain for tracking
        chain = thinking.start_reasoning(query)
        
        # Load workflow guide for grounding (proactive reading)
        workflow_guide = cls._load_workflow_guide(persona, workflow_name)
        
        # Get persona context
        identity = persona.identity
        prof_name = identity.get("name", "Professor")
        institution = identity.get("institution", "University")
        expertise = identity.get("expertise", [])
        
        # Build workflow-specific system prompt (pass persona to load YAML config)
        system_prompt = cls._build_system_prompt(workflow_name, prof_name, institution, expertise, persona)
        
        # Detect if query references files — if so, let the agent read them
        has_file_refs = '/Users/' in query or '/home/' in query or '/spaces/' in query or any(
            ext in query.lower() for ext in ['.pdf', '.docx', '.xlsx', '.eml']
        )
        
        if has_file_refs:
            system_prompt += f"""
You are an expert researcher and writer. You have full access to read files and use tools.
Complete the task thoroughly. Output your response as well-structured markdown.
Do NOT ask follow-up questions — complete the FULL task in one response.

CRITICAL FILE RULES:
- NEVER create or modify files in the knowledge/ directory — it is READ-ONLY source material.
- NEVER write intermediate files (drafts, analyses, extractions) to the output/ directory.
- For ANY intermediate files, save them to: {persona.persona_dir}/artifacts/
- The output/ directory is ONLY for the final user-requested deliverable.
- Output your content as your response text — do NOT write it to a file unless explicitly asked."""
        else:
            system_prompt += """
All source materials you need are provided below in this prompt. Do your full reasoning and analysis.
Output your response as well-structured markdown.
Do NOT ask follow-up questions. Complete the FULL task in one response."""

        # Build the prompt with knowledge base content as PRIMARY source
        kb_context = cls._build_kb_context(extracted_content)
        
        # Build workflow-specific main prompt
        prompt = cls._build_workflow_prompt(workflow_name, query, kb_context, workflow_guide, persona.name)

        # Add workflow guide for grounding (from doc/)
        if workflow_guide:
            prompt += f"\n\n## WORKFLOW GROUNDING GUIDE:\n{workflow_guide}"
        
        # Add warm start strategies if available
        if warm_start_prompt:
            prompt += f"\n\n## Suggested Approach (from similar queries):\n{warm_start_prompt}"
        
        # Add lessons from previous runs
        if lessons_prompt:
            prompt += f"\n\n{lessons_prompt}"
        
        # Add session memory from previous runs (Enhancement 2)
        if session_memory_prompt:
            prompt += f"\n\n{session_memory_prompt}"
        
        # Get LLM client and apply adaptive timeout
        llm = get_llm_client()
        
        # Estimate timeout based on prompt complexity
        from research_assistant.core.llm import LLMClient
        estimated_timeout = LLMClient.estimate_timeout(
            prompt=prompt + (system_prompt or ""),
            kb_file_count=len(extracted_content),
            workflow_name=workflow_name,
        )
        # Use the higher of estimated vs configured timeout
        llm.timeout_seconds = max(llm.timeout_seconds, estimated_timeout)
        logger.info(f"[WORKFLOW] Using timeout: {llm.timeout_seconds}s (estimated: {estimated_timeout}s)")
        
        if iteration > 0 and previous_feedback and previous_output:
            # Use feedback-based improvement
            thinking.add_thought(
                thought=f"Iteration {iteration + 1}: Improving based on feedback",
                reasoning_type=ReasoningType.ANALYTICAL,
                grounded_in=["analyst_feedback"],
                confidence=0.85,
            )
            
            response = llm.generate_with_feedback(
                prompt=prompt,
                previous_output=previous_output,
                feedback=previous_feedback,
                system_prompt=system_prompt,
            )
        else:
            # First iteration - fresh generation
            thinking.add_thought(
                thought=f"Generating initial explanation for {query}",
                reasoning_type=ReasoningType.SYNTHESIS,
                grounded_in=[f"persona:{persona.name}", "knowledge_base"],
                confidence=0.9,
            )
            
            if has_file_refs:
                response = llm.generate_as_agent(prompt, system_prompt)
            else:
                response = llm.generate(prompt, system_prompt)
        
        # Log the result and fail fast on empty content
        if response.success and response.content.strip():
            logger.info(f"[WORKFLOW] LLM generated {response.tokens_used} tokens via {response.model}")
        elif not response.success:
            error_msg = f"LLM generation failed: {response.error}"
            logger.error(f"[WORKFLOW] {error_msg}")
            raise RuntimeError(error_msg)
        else:
            # success=True but empty content (shouldn't happen, but guard against it)
            error_msg = "LLM returned empty content"
            logger.error(f"[WORKFLOW] {error_msg}")
            raise RuntimeError(error_msg)
        
        # Conclude reasoning
        chain_result = thinking.conclude(
            f"Generated explanation for {query} (iteration {iteration + 1})"
        )
        
        # Format the output with persona header
        # Truncate query for heading if it's too long (e.g. multi-step prompts)
        display_title = query if len(query) <= 200 else query[:200].rsplit(' ', 1)[0] + "..."
        
        header = f"""# {display_title}

**Explained by: {prof_name}**
*{institution} | Expertise: {', '.join(expertise[:3])}*

---

"""
        
        footer = f"""

---

*This explanation follows {prof_name}'s teaching approach at {institution}, 
emphasizing both theoretical rigor and practical application.*

**Next Steps**: Review course materials for deeper exploration and develop your own analytical framework.
"""
        
        return header + response.content + footer
    
    @classmethod
    def _build_system_prompt(
        cls,
        workflow_name: str,
        prof_name: str,
        institution: str,
        expertise: List[str],
        persona: Any = None,
    ) -> str:
        """Build workflow-specific system prompt from YAML configuration."""
        expertise_str = ', '.join(expertise[:5])
        
        # Try to load system prompt from persona's prompts.yaml
        if persona:
            prompts_config = cls._load_prompts_yaml(persona)
            if prompts_config:
                # Use system_prompt from YAML if available
                yaml_system = prompts_config.get("system_prompt", "")
                if yaml_system:
                    return yaml_system
                
                # Try to get workflow-specific prompts
                workflows = prompts_config.get("workflows", {})
                workflow_config = workflows.get(workflow_name, {})
                
                if workflow_config:
                    # Build structured prompt from YAML sections
                    scope = workflow_config.get("scope", "")
                    decision_flow = workflow_config.get("decision_flow", "")
                    validation_rules = workflow_config.get("validation_rules", "")
                    
                    structured_prompt = f"""You are {prof_name}, a professor at {institution}.
Your areas of expertise: {expertise_str}.

{scope}

{decision_flow}

{validation_rules}
"""
                    return structured_prompt
        
        # Fallback to hardcoded if YAML not available
        base_prompt = f"""You are {prof_name}, a professor at {institution}.
Your areas of expertise: {expertise_str}.
"""
        
        if workflow_name == "explain":
            return base_prompt + """
You are explaining academic concepts to doctoral/research students.
Your explanations should:
1. Be grounded in the provided knowledge base materials
2. Use proper academic terminology and frameworks
3. Include theoretical foundations and practical applications
4. Be structured with clear sections and headings
5. Reference source materials when applicable

Write in a professional academic style that is accessible but rigorous."""
        
        elif workflow_name == "guide":
            return base_prompt + """
You are GUIDING students through academic tasks - helping them develop their own work.
Your guidance should:
1. NOT provide direct answers or do the work for them
2. Help them understand what's being asked
3. Suggest frameworks and approaches from course materials
4. Ask reflection questions that prompt critical thinking
5. Reference specific KB materials they should consult

Write as a mentor guiding discovery, not a tutor giving answers."""
        
        elif workflow_name == "review":
            return base_prompt + """
You are reviewing student submissions against academic standards.
Your reviews should:
1. Identify both strengths and areas for improvement
2. Reference specific criteria from course materials
3. Provide constructive, actionable feedback
4. Maintain an encouraging but rigorous tone
5. Suggest next steps for improvement

Be thorough but supportive - the goal is student development."""
        
        elif workflow_name == "research":
            return base_prompt + """
You are helping plan research strategy and methodology.
Your research guidance should:
1. Map to theoretical frameworks from the knowledge base
2. Identify literature and gaps
3. Suggest appropriate methodologies
4. Consider validity and ethical implications
5. Provide structured research roadmaps

Ground all suggestions in academic rigor and KB materials."""
        
        else:
            return base_prompt + """
Write in a professional academic style that is accessible but rigorous.
Always ground responses in the provided knowledge base materials."""
    
    @classmethod
    def _load_prompts_yaml(cls, persona: Any) -> Optional[Dict]:
        """Load prompts.yaml configuration for a persona."""
        try:
            import yaml
            prompts_path = persona.persona_dir / "prompts.yaml"
            if prompts_path.exists():
                with open(prompts_path, 'r') as f:
                    return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"[WORKFLOW] Failed to load prompts.yaml: {e}")
        return None
    
    @classmethod
    def _build_kb_context(cls, extracted_content: List[str]) -> str:
        """Build knowledge base context section.
        
        The reader already manages a token budget, so we include all content
        it provides rather than aggressively truncating.
        """
        if not extracted_content:
            return ""
        
        kb_context = "\n\n## PRIMARY SOURCE - Course Knowledge Base (MUST USE):\n"
        kb_context += "**IMPORTANT**: The following materials are from the professor's course. "
        kb_context += "Use these as your PRIMARY reference. Define terms EXACTLY as they appear in these materials.\n"
        
        # Include all content from reader (already budget-managed)
        for i, content in enumerate(extracted_content, 1):
            # Use full content — reader already applied token budget
            kb_context += f"\n### Course Material {i}:\n{content}\n"
        
        return kb_context
    
    @classmethod
    def _build_workflow_prompt(
        cls,
        workflow_name: str,
        query: str,
        kb_context: str,
        workflow_guide: str,
        persona_name: str = "PERSONA",
    ) -> str:
        """Build workflow-specific main prompt."""
        
        if workflow_name == "explain":
            # Detect if query is actually procedural (guide question in wrong workflow)
            query_lower = query.lower()
            procedural_keywords = ["how do i", "how to", "help me", "how would we", "how should i", "what should i do", "guide me", "steps to", "process for"]
            
            if any(keyword in query_lower for keyword in procedural_keywords):
                return f"""Topic: {query}

**⚠️ WORKFLOW MISMATCH DETECTED ⚠️**

Your query asks "**how to proceed**" or "**how to do**" something - this is a **PROCEDURAL/GUIDANCE** question, not a conceptual explanation.

**Current workflow**: EXPLAIN (designed for "What is X?" or "Define Y")
**Recommended workflow**: **GUIDE** (designed for "How do I..." or "Help me with...")

**What you should do**:
Re-run with the GUIDE workflow:
```
ra guide "{query}" --persona {persona_name}
```

**Why this matters**:
- EXPLAIN workflow explains concepts (e.g., "Explain research methodology")
- GUIDE workflow provides step-by-step procedural guidance (e.g., "How do I analyze this case study?")

Your query asks for procedural guidance, which requires:
- Step-by-step approach
- Framework application guidance
- Task breakdown
- Reflection questions

The GUIDE workflow is specifically designed for this type of request.

**Quick Reference**:
| Use EXPLAIN when | Use GUIDE when |
|------------------|----------------|
| "Explain mediation" | "How do I analyze mediation?" |
| "What is SEM?" | "Help me run SEM analysis" |
| "Define validity" | "How do I establish validity?" |

Please re-run with: `ra guide "..." --persona {persona_name}`

{kb_context}"""
            
            else:
                return f"""Topic: {query}

**CRITICAL INSTRUCTION**: You MUST base your explanation primarily on the Course Knowledge Base materials provided below. 
These are the professor's actual course materials. Use the EXACT definitions and frameworks from these materials.

Please provide a comprehensive explanation of "{query}" using the following structure:

1. **Conceptual Definition** - What is this concept? (Use KB definition FIRST)
2. **Theoretical Foundation** - What theories/frameworks support it? (Reference KB materials)
3. **Key Components** - What are the main elements? (From KB)
4. **Practical Application** - How is it applied in practice?
5. **Research Considerations** - How should researchers approach this topic?
{kb_context}"""
        
        elif workflow_name == "guide":
            # Detect request type from query
            query_lower = query.lower()
            
            if any(t in query_lower for t in ["email", "response", "reply", "communication", "prof"]):
                return f"""Assignment: {query}

**CRITICAL INSTRUCTION**: ALWAYS provide comprehensive structured guidance based on available context.

**MANDATORY OUTPUT STRUCTURE**:

## 1. Email Context Summary
Extract and summarize what the professor said/asked from KB materials.
If email content is in KB: use it directly.
If not fully available: work with what you have and note gaps.

## 2. Key Points to Address
List specific items from the professor's message that need response.

## 3. Suggested Response Structure
- Opening: Professional greeting template
- Body: How to address each point (provide specific guidance)
- Closing: Next steps template

## 4. Tone Guidelines
Professional communication principles.

## 5. Draft Template
Complete email structure with [PLACEHOLDERS] for customization.
Include actual suggested content based on KB.

## 6. Questions for Clarification (Optional)
ONLY if additional context would significantly improve the guidance.
Format as: "To provide more specific guidance, it would help to know: ..."

**CRITICAL RULES**:
- Provide guidance with available context FIRST
- Do NOT refuse to proceed due to missing information
- Do NOT start by asking what's needed - start by providing what you can
- Clarification questions come LAST, after providing comprehensive guidance

{kb_context}"""
            
            elif any(t in query_lower for t in ["objective", "aim", "goal"]):
                return f"""Assignment: {query}

**CRITICAL INSTRUCTION**: This is a GUIDE workflow requesting help with research OBJECTIVE formulation.
You MUST follow the workflow guide format for objectives.

The student needs guidance on writing a research objective. 
Use the professor's criteria from the workflow guide.

**OUTPUT MUST INCLUDE:**
1. Research Objective statement starting with "The objective of this research is to..."
2. Business Context section explaining why this matters
3. Research Scope (general to specific)
4. Suggested Title aligned with objective words
5. Rationale table showing how it meets professor's criteria

Do NOT give a generic explanation. Follow the objective format exactly.
{kb_context}"""
            
            elif any(t in query_lower for t in ["questionnaire", "scale", "items", "measurement"]):
                return f"""Assignment: {query}

**CRITICAL INSTRUCTION**: This is a GUIDE workflow for questionnaire/measurement guidance.
Help the student understand measurement design without doing the work for them.

Provide:
1. Understanding of the measurement task
2. Framework suggestions from KB materials
3. Reference to example instruments in KB
4. Questions for reflection
5. Next steps

Ground in course materials about scale development and measurement.
{kb_context}"""
            
            else:
                return f"""Assignment: {query}

**CRITICAL INSTRUCTION**: ALWAYS provide comprehensive structured guidance based on available context.

**MANDATORY OUTPUT STRUCTURE**:

## 1. Understanding the Task
Analyze what's being asked based on the query and KB context.

## 2. Suggested Approach/Framework
Provide specific methodology or framework from KB materials.

## 3. Relevant KB Materials
Reference specific documents, sections, templates from KB.

## 4. Step-by-Step Guidance
Concrete steps the student should take.

## 5. Reflection Questions
Questions to guide their thinking.

## 6. Draft/Template (if applicable)
Provide structure with [PLACEHOLDERS] for them to fill.

## 7. Questions for Additional Context (Optional)
ONLY if more information would significantly enhance guidance.
Format as: "To provide more specific guidance, it would help to know: ..."

**CRITICAL RULES**:
- Provide guidance with available context FIRST
- Do NOT start by asking what's needed
- Do NOT refuse to proceed
- Clarification questions come LAST

{kb_context}"""
        
        elif workflow_name == "review":
            return f"""Submission for Review: {query}

**CRITICAL INSTRUCTION**: Provide a thorough review against academic standards.

Structure your review as:
1. Executive Summary (2-3 sentences)
2. Strengths (what works well)
3. Areas for Improvement (with specific recommendations)
4. Detailed feedback by section
5. Next steps

Be constructive and reference course criteria.
{kb_context}"""
        
        elif workflow_name == "research":
            return f"""Research Task: {query}

**CRITICAL INSTRUCTION**: Conduct a structured research analysis grounded in KB materials.
This is a MULTI-PHASE research workflow. Complete ALL phases in your response.

## PHASE 1: RESEARCH FRAMING
- Clarify the research objective (what exactly are we investigating?)
- Identify the theoretical lens (which frameworks from KB apply?)
- Define scope and boundaries

## PHASE 2: LITERATURE MAPPING
- Identify key sources from the KB that are relevant
- Map the theoretical landscape (what theories/models apply?)
- Identify gaps in the available literature
- Suggest additional sources to seek (with specific search terms)

## PHASE 3: METHODOLOGY DESIGN
- Recommend research design (qualitative/quantitative/mixed)
- Suggest data collection methods with justification
- Identify variables (dependent, independent, mediating, moderating)
- Address validity and reliability considerations
- Note ethical implications

## PHASE 4: SYNTHESIS & ROADMAP
- Synthesize findings into a coherent research plan
- Provide a phased timeline with milestones
- Identify risks and mitigation strategies
- List concrete next steps

**RULES**:
- Ground EVERY recommendation in KB materials or established academic frameworks
- Use [PLACEHOLDER: ...] for information you don't have
- Be specific — name theories, cite sources, suggest exact methods
- Do NOT be generic or hand-wavy

{kb_context}"""
        
        elif workflow_name == "quant":
            return f"""Quantitative Analysis Task: {query}

**CRITICAL INSTRUCTION**: Provide rigorous statistical analysis guidance grounded in KB materials.

## PHASE 1: DATA UNDERSTANDING
- What variables are involved? (types: nominal, ordinal, interval, ratio)
- What is the sample size and structure?
- What are the research hypotheses?

## PHASE 2: METHOD SELECTION
- Recommend appropriate statistical test(s) with justification
- Explain WHY this method is appropriate for this data/question
- List assumptions that must be checked (normality, homoscedasticity, etc.)
- Reference KB materials on method selection criteria

## PHASE 3: ANALYSIS PLAN
- Step-by-step analysis procedure
- Software/tool recommendations (SPSS, R, Python) with specific commands if applicable
- How to check assumptions before running the main analysis
- What to do if assumptions are violated

## PHASE 4: INTERPRETATION GUIDE
- How to read the output (which numbers matter)
- What constitutes statistical significance vs practical significance
- Effect size interpretation (Cohen's d, eta-squared, etc.)
- How to report results in APA format

## PHASE 5: REPORTING TEMPLATE
- Results section template with [PLACEHOLDERS] for actual values
- Table format for presenting results
- How to discuss findings in context of hypotheses

**RULES**:
- Reference specific KB materials (Hair et al., Field, etc.) for method justification
- Include actual threshold values (e.g., KMO > 0.6, Cronbach's α > 0.7)
- Be precise about which test variant to use (e.g., Welch's t-test vs Student's t-test)
- Use [PLACEHOLDER: ...] for data-specific values

{kb_context}"""
        
        else:
            return f"""Task: {query}

Please address this request using the knowledge base materials as your primary source.
{kb_context}"""
    
    @classmethod
    def _format_output(
        cls,
        workflow_name: str,
        query: str,
        reasoning: str,
        persona: Any,
        score: float,
        iterations: int,
    ) -> str:
        """Format the final output content."""
        # Add metadata footer
        metadata = [
            "",
            "---",
            "",
            f"*Generated by Research Assistant | Workflow: {workflow_name}*",
            f"*Persona: {persona.name} | Quality Score: {score}/10 | Iterations: {iterations}*",
        ]
        
        return reasoning + "\n".join(metadata)
    
    @classmethod
    def _load_workflow_guide(cls, persona: Any, workflow_name: str) -> str:
        """
        Load workflow guide document for grounding.
        
        Proactively reads persona/doc/{workflow_name}_workflow.md to provide
        grounding rules and learned patterns to the thinker.
        """
        doc_dir = persona.persona_dir / "doc"
        guide_path = doc_dir / f"{workflow_name}_workflow.md"
        
        if guide_path.exists():
            try:
                content = guide_path.read_text()
                logger.info(f"[WORKFLOW] Loaded workflow guide: {guide_path.name}")
                return content
            except Exception as e:
                logger.warning(f"[WORKFLOW] Failed to read workflow guide: {e}")
                return ""
        else:
            logger.debug(f"[WORKFLOW] No workflow guide found at {guide_path}")
            return ""
    
    @classmethod
    def _log_workflow_execution(
        cls,
        workflow_name: str,
        persona_name: str,
        query: str,
        output_path: Path,
        score: float,
        reasoning_iterations: int,
        validation_iterations: int,
        execution_time_ms: int,
        eval_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log workflow execution to logs/workflow_history.jsonl"""
        try:
            import json
            from datetime import datetime
            
            # Get project root (where logs/ should be)
            project_root = Path(__file__).parent.parent.parent
            log_file = project_root / "logs" / "workflow_history.jsonl"
            
            # Ensure logs directory exists
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Create log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "workflow": workflow_name,
                "persona": persona_name,
                "query": query,
                "output_path": str(output_path),
                "score": score,
                "reasoning_iterations": reasoning_iterations,
                "validation_iterations": validation_iterations,
                "execution_time_ms": execution_time_ms,
            }
            
            # Level 3: Include parallel evaluation data
            if eval_data:
                log_entry["eval"] = eval_data
            
            # Append to log file (JSONL format - one JSON object per line)
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            
            logger.info(f"[WORKFLOW] Logged execution to {log_file}")
            
        except Exception as e:
            logger.warning(f"[WORKFLOW] Failed to log execution: {e}")
    
    @classmethod
    def _ensure_defaults_registered(cls) -> None:
        """Register default workflows if not already done."""
        if not cls._defaults_registered:
            _register_default_workflows()
            cls._defaults_registered = True


# =============================================================================
# Action Implementations (for backward compatibility)
# =============================================================================

class ReadAction(BaseAction):
    """Read and extract relevant content from knowledge base."""
    name = "read"
    
    def execute(self, input: ActionInput) -> ActionResult:
        """Scan knowledge base for relevant content."""
        import os
        
        topic = input.state.get("topic", input.state.get("task", ""))
        persona = input.persona
        knowledge_dir = persona.persona_dir / "knowledge"
        
        relevant_files = []
        relevant_content = []
        search_terms = topic.lower().split()
        
        if knowledge_dir.exists():
            for root, dirs, files in os.walk(knowledge_dir):
                for file in files:
                    file_lower = file.lower()
                    if any(term in file_lower for term in search_terms):
                        filepath = Path(root) / file
                        relevant_files.append(str(filepath.relative_to(knowledge_dir)))
                        
                        if file.endswith('.txt') or file.endswith('.md'):
                            try:
                                content = filepath.read_text()[:2000]
                                relevant_content.append(f"From {file}:\n{content}")
                            except:
                                pass
        
        input.memory.add_fact(f"Found {len(relevant_files)} relevant files for: {topic}", "reader", 8)
        
        return ActionResult(
            success=True,
            action_name=self.name,
            artifacts={
                "knowledge_extracted": True,
                "relevant_files": relevant_files,
                "relevant_content": relevant_content,
                "search_topic": topic,
            },
        )


class ExplainAction(BaseAction):
    """Generate explanation using persona voice and knowledge base."""
    name = "explain"
    
    def execute(self, input: ActionInput) -> ActionResult:
        """Generate content - delegates to main workflow loop."""
        # This is now handled by the main invoke() method
        return ActionResult(
            success=True,
            action_name=self.name,
            artifacts={"delegated_to_workflow": True},
        )


class ReviewAction(BaseAction):
    """Review submission against standards."""
    name = "review"
    
    def execute(self, input: ActionInput) -> ActionResult:
        submission = input.state.get("submission_path", "submission")
        persona = input.persona
        
        content = f"""# Review: {submission}

## Strengths
[Positive aspects of the submission]

## Areas for Development
[What needs improvement]

## Recommendations
[Specific suggestions]

## Estimated Grade: [Grade]

*Reviewed by {persona.name} persona*
"""
        
        return ActionResult(
            success=True,
            action_name=self.name,
            content=content,
            artifacts={"submission_reviewed": submission},
        )


class GuideAction(BaseAction):
    """Provide assignment guidance without answers."""
    name = "guide"
    
    def execute(self, input: ActionInput) -> ActionResult:
        assignment = input.state.get("assignment", input.state.get("task", "assignment"))
        persona = input.persona
        
        content = f"""# Guidance: {assignment}

## Understanding the Task
[Clarification of what's being asked]

## Suggested Approach
[Hints on how to approach this]

## Frameworks to Consider
[Relevant frameworks from {persona.name}'s course]

## Questions to Ask Yourself
- [Reflection question 1]
- [Reflection question 2]
- [Reflection question 3]

*I encourage you to develop your own analysis. - {persona.identity.get('name', 'Professor')}*
"""
        
        return ActionResult(
            success=True,
            action_name=self.name,
            content=content,
            artifacts={"assignment_guided": assignment},
        )


class OutputAction(BaseAction):
    """Final output action - formats and saves."""
    name = "output"
    
    def execute(self, input: ActionInput) -> ActionResult:
        return ActionResult(
            success=True,
            action_name=self.name,
            artifacts={"output_ready": True},
        )


# =============================================================================
# Default Workflow Registration
# =============================================================================

def _register_default_workflows() -> None:
    """Register standard research workflows."""
    
    WorkflowInvoker.register(WorkflowSpec(
        name="explain",
        description="Explain concept using persona's teaching style with reasoning loop",
        actions=[ReadAction, ExplainAction, OutputAction],
        required_inputs=["topic"],
        optional_inputs=["depth", "examples"],
    ))
    
    WorkflowInvoker.register(WorkflowSpec(
        name="review",
        description="Review submission against persona standards",
        actions=[ReadAction, ReviewAction, OutputAction],
        required_inputs=["submission_path"],
        optional_inputs=["rubric_path"],
    ))
    
    WorkflowInvoker.register(WorkflowSpec(
        name="guide",
        description="Provide assignment guidance without direct answers",
        actions=[ReadAction, GuideAction, OutputAction],
        required_inputs=["assignment"],
        optional_inputs=[],
    ))
    
    WorkflowInvoker.register(WorkflowSpec(
        name="research",
        description="Full research workflow with literature mapping, methodology design, and roadmap",
        actions=[ReadAction, ExplainAction, ReviewAction, OutputAction],
        required_inputs=["task"],
        optional_inputs=["scope", "frameworks"],
    ))
    
    WorkflowInvoker.register(WorkflowSpec(
        name="quant",
        description="Quantitative analysis guidance with method selection, analysis plan, and reporting",
        actions=[ReadAction, ExplainAction, ReviewAction, OutputAction],
        required_inputs=["task"],
        optional_inputs=["dataset", "variables", "hypotheses"],
    ))
    
    logger.debug("Registered default workflows: explain, review, guide, research, quant")
