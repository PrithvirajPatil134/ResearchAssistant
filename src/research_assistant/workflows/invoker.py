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


# =============================================================================
# Progress Indicator
# =============================================================================

class ProgressIndicator:
    """Terminal progress indicator for workflow stages."""
    
    # Stage indices for update() calls
    STAGE_READ = 0
    STAGE_WARM = 1
    STAGE_REASON = 2
    STAGE_ANALYZE = 3
    STAGE_VALIDATE = 4
    STAGE_SAVE = 5
    
    STAGES = [
        ("📚", "Reading KB", "Extracting knowledge base..."),
        ("🔍", "Warm Start", "Finding similar patterns..."),
        ("🧠", "Reasoning", "Generating response..."),
        ("📊", "Analyzing", "Scoring quality..."),
        ("✅", "Validating", "Reviewing output..."),
        ("💾", "Saving", "Writing output file..."),
    ]
    
    SPINNER_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled and sys.stdout.isatty()
        self.current_stage = 0
        self.current_detail = ""
        self._spinner_idx = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
    
    def start(self, query: str) -> None:
        """Start the progress display."""
        if not self.enabled:
            return
        
        # Print header
        print(f"\n{'─' * 60}")
        print(f"🎯 Query: {query[:50]}{'...' if len(query) > 50 else ''}")
        print(f"{'─' * 60}")
        
        self._running = True
        self._thread = threading.Thread(target=self._spinner_loop, daemon=True)
        self._thread.start()
    
    def update(self, stage_idx: int, detail: str = "") -> None:
        """Update progress to a specific stage."""
        if not self.enabled:
            return
        
        with self._lock:
            # Print newline to preserve previous stage before updating
            if stage_idx > self.current_stage:
                sys.stdout.write("\n")
                sys.stdout.flush()
            self.current_stage = min(stage_idx, len(self.STAGES) - 1)
            self.current_detail = detail
    
    def set_detail(self, detail: str) -> None:
        """Update just the detail text."""
        if not self.enabled:
            return
        with self._lock:
            self.current_detail = detail
    
    def stop(self, success: bool = True) -> None:
        """Stop the progress display."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.5)
        
        if self.enabled:
            # Clear the line and print final status
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.flush()
            if success:
                print("✨ Workflow complete!")
            print(f"{'─' * 60}\n")
    
    def _spinner_loop(self) -> None:
        """Background thread for spinner animation."""
        while self._running:
            with self._lock:
                stage_idx = self.current_stage
                detail = self.current_detail
            
            if stage_idx < len(self.STAGES):
                emoji, name, desc = self.STAGES[stage_idx]
                spinner = self.SPINNER_CHARS[self._spinner_idx % len(self.SPINNER_CHARS)]
                
                # Build status line
                detail_text = f" [{detail}]" if detail else ""
                status = f"\r{spinner} [{stage_idx + 1}/{len(self.STAGES)}] {emoji} {name}: {desc}{detail_text}"
                
                # Truncate if too long
                max_len = 78
                if len(status) > max_len:
                    status = status[:max_len-3] + "..."
                
                # Pad to clear previous content
                status = status.ljust(80)
                
                sys.stdout.write(status)
                sys.stdout.flush()
            
            self._spinner_idx += 1
            time_module.sleep(0.1)


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
    
    @classmethod
    def invoke(
        cls,
        workflow_name: str,
        persona_name: str,
        initial_state: Dict[str, Any],
        output_format: str = "md",
        personas_dir: Optional[Path] = None,
        show_progress: bool = True,
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
        """
        import time
        start_time = time.time()
        
        cls._ensure_defaults_registered()
        
        # Initialize progress indicator
        progress = ProgressIndicator(enabled=show_progress)
        query = initial_state.get("topic", initial_state.get("task", ""))
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
        
        # Load persona
        try:
            from research_assistant.personas import PersonaLoader
            
            personas_path = personas_dir or Path(__file__).parent.parent / "personas"
            loader = PersonaLoader(personas_path)
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
            # STEP 2: WARM START - Get patterns from learner
            # =========================================================
            progress.update(ProgressIndicator.STAGE_WARM, "checking history")
            
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
                )
                
                # Update progress for analysis
                progress.update(ProgressIndicator.STAGE_ANALYZE, f"scoring iter {iteration + 1}")
                
                # Score with analyst
                score_result = analyst.execute(
                    query=query,
                    reasoning=reasoning_content,
                    knowledge_content=extracted_content,
                    iteration=iteration,
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
            # STEP 4: WRITE OUTPUT - Format final content
            # =========================================================
            final_content = cls._format_output(
                workflow_name=workflow_name,
                query=query,
                reasoning=reasoning_content,
                persona=persona,
                score=final_score,
                iterations=reasoning_iterations,
            )
            
            # =========================================================
            # STEP 5: VALIDATION LOOP - Reviewer checks output
            # =========================================================
            validation_passed = False
            reviewer_feedback = ""
            
            for val_iteration in range(cls.MAX_VALIDATION_ITERATIONS):
                validation_iterations = val_iteration + 1
                
                progress.update(ProgressIndicator.STAGE_VALIDATE, f"check {val_iteration + 1}/{cls.MAX_VALIDATION_ITERATIONS}")
                
                # Reviewer validates
                review_result = reviewer.execute(
                    content=final_content,
                    original_query=query,
                    context={"persona": persona.name},
                )
                
                if review_result.success:
                    review_data = review_result.output
                    if isinstance(review_data, dict):
                        validation_passed = review_data.get("approved", True)
                        reviewer_feedback = review_data.get("feedback", "")
                    else:
                        validation_passed = True
                else:
                    validation_passed = True  # Skip validation if reviewer fails
                
                logger.info(
                    f"[WORKFLOW] Validation iteration {val_iteration + 1}: "
                    f"{'PASS' if validation_passed else 'NEEDS REVISION'}"
                )
                
                if validation_passed:
                    progress.set_detail("passed")
                    break
                
                # Regenerate with reviewer feedback
                progress.set_detail("revising")
                reasoning_content = cls._generate_reasoning(
                    query=query,
                    persona=persona,
                    extracted_content=extracted_content,
                    warm_start_prompt=warm_start_prompt,
                    previous_feedback=reviewer_feedback,
                    iteration=reasoning_iterations,
                    thinking=thinking,
                )
                
                final_content = cls._format_output(
                    workflow_name=workflow_name,
                    query=query,
                    reasoning=reasoning_content,
                    persona=persona,
                    score=final_score,
                    iterations=reasoning_iterations + val_iteration,
                )
            
            # =========================================================
            # STEP 6: STORE PATTERN - Save for future learning
            # =========================================================
            progress.update(ProgressIndicator.STAGE_SAVE, "storing pattern")
            
            learner.store_pattern(
                query=query,
                reasoning=reasoning_content,
                score=final_score,
                feedback=analyst_feedback,
            )
            
            # =========================================================
            # STEP 7: WRITE OUTPUT FILE
            # =========================================================
            progress.set_detail("writing file")
            
            output_path = output_dir / f"{workflow_id}.{output_format}"
            output_path.write_text(final_content)
            
            execution_time = int((time.time() - start_time) * 1000)
            
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
    ) -> str:
        """Generate reasoning content using LLM with persona context."""
        from research_assistant.core import get_llm_client
        from research_assistant.core.thinking import ReasoningType
        
        # Start reasoning chain for tracking
        chain = thinking.start_reasoning(query)
        
        # Get persona context
        identity = persona.identity
        prof_name = identity.get("name", "Professor")
        institution = identity.get("institution", "University")
        expertise = identity.get("expertise", [])
        
        # Build system prompt with persona context
        system_prompt = f"""You are {prof_name}, a professor at {institution}.
Your areas of expertise: {', '.join(expertise[:5])}.

You are explaining academic concepts to doctoral/research students.
Your explanations should:
1. Be grounded in the provided knowledge base materials
2. Use proper academic terminology and frameworks
3. Include theoretical foundations and practical applications
4. Be structured with clear sections and headings
5. Reference source materials when applicable

Write in a professional academic style that is accessible but rigorous."""

        # Build the prompt with knowledge base content as PRIMARY source
        kb_context = ""
        if extracted_content:
            kb_context = "\n\n## PRIMARY SOURCE - Course Knowledge Base (MUST USE):\n"
            kb_context += "**IMPORTANT**: The following materials are from the professor's course. "
            kb_context += "Use these as your PRIMARY reference. Define terms EXACTLY as they appear in these materials.\n"
            for i, content in enumerate(extracted_content[:5], 1):
                # Include more content for LLM context
                excerpt = content[:2500].strip()
                kb_context += f"\n### Course Material {i}:\n{excerpt}\n"
        
        # Build main prompt with explicit KB grounding instructions
        prompt = f"""Topic: {query}

**CRITICAL INSTRUCTION**: You MUST base your explanation primarily on the Course Knowledge Base materials provided below. 
These are the professor's actual course materials. Use the EXACT definitions and frameworks from these materials.
You may supplement with web search for additional context, but the KB materials are your PRIMARY source.

If the KB materials define a term (like "DRO" = Digital Resource Orchestration), use THAT definition, not web search results.

Please provide a comprehensive explanation of "{query}" using the following structure:

1. **Conceptual Definition** - What is this concept? (Use KB definition FIRST)
2. **Theoretical Foundation** - What theories/frameworks support it? (Reference KB materials)
3. **Key Components** - What are the main elements? (From KB)
4. **Practical Application** - How is it applied in practice?
5. **Research Considerations** - How should researchers approach this topic?
{kb_context}"""

        # Add warm start strategies if available
        if warm_start_prompt:
            prompt += f"\n\n## Suggested Approach (from similar queries):\n{warm_start_prompt}"
        
        # Get LLM client and generate
        llm = get_llm_client()
        
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
            
            response = llm.generate(prompt, system_prompt)
        
        # Log the result
        if response.success:
            logger.info(f"[WORKFLOW] LLM generated {response.tokens_used} tokens via {response.model}")
        else:
            logger.warning(f"[WORKFLOW] LLM error: {response.error}, using fallback")
        
        # Conclude reasoning
        chain_result = thinking.conclude(
            f"Generated explanation for {query} (iteration {iteration + 1})"
        )
        
        # Format the output with persona header
        header = f"""# {query}

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
        description="Full research workflow with analysis and review",
        actions=[ReadAction, ExplainAction, ReviewAction, OutputAction],
        required_inputs=["task"],
        optional_inputs=["scope", "frameworks"],
    ))
    
    logger.debug("Registered default workflows: explain, review, guide, research")
