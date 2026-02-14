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
        """Print stage transition once."""
        if not self.enabled:
            return
        
        # Only print each stage once
        if stage_idx in self._printed_stages:
            return
        
        self._printed_stages.add(stage_idx)
        self.current_stage = stage_idx
        
        if stage_idx < len(self.STAGES):
            emoji, agent = self.STAGES[stage_idx]
            detail_text = f" → {detail}" if detail else ""
            print(f"  {emoji} {agent}{detail_text}")
    
    def set_detail(self, detail: str) -> None:
        """Update detail - only prints for significant events."""
        pass  # No-op for simple progress
    
    def log(self, message: str) -> None:
        """Print an important log message."""
        if self.enabled:
            print(f"     ↳ {message}")
    
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
                    workflow_name=workflow_name,
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
                
                # Reviewer validates with workflow context
                review_result = reviewer.review_against_standards(
                    content=final_content,
                    workflow_name=workflow_name,
                    user_query=query,
                    persona={"name": persona.name},
                )
                
                # Extract results from ReviewResult
                validation_passed = review_result.meets_standards
                reviewer_feedback = "; ".join(
                    i.get("message", "") for i in review_result.issues
                ) or "; ".join(review_result.suggestions)
                
                # Check for critical issues
                has_critical = any(
                    i.get("severity") == "critical" for i in review_result.issues
                )
                if has_critical:
                    validation_passed = False
                    progress.log(f"Critical issue: {review_result.issues[0].get('message', 'unknown')}")
                
                logger.info(
                    f"[WORKFLOW] Validation iteration {val_iteration + 1}: "
                    f"Score {review_result.overall_score}/10 "
                    f"({'PASS' if validation_passed else 'NEEDS REVISION'})"
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
                    workflow_name=workflow_name,
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
        """Build knowledge base context section."""
        if not extracted_content:
            return ""
        
        kb_context = "\n\n## PRIMARY SOURCE - Course Knowledge Base (MUST USE):\n"
        kb_context += "**IMPORTANT**: The following materials are from the professor's course. "
        kb_context += "Use these as your PRIMARY reference. Define terms EXACTLY as they appear in these materials.\n"
        
        for i, content in enumerate(extracted_content[:5], 1):
            excerpt = content[:2500].strip()
            kb_context += f"\n### Course Material {i}:\n{excerpt}\n"
        
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

**CRITICAL INSTRUCTION**: Help plan research strategy grounded in KB materials.

Provide:
1. Research objective clarification
2. Theoretical framework mapping
3. Literature/source strategy
4. Methodology recommendations
5. Timeline/next steps

Ground all suggestions in academic frameworks from the knowledge base.
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
        description="Full research workflow with analysis and review",
        actions=[ReadAction, ExplainAction, ReviewAction, OutputAction],
        required_inputs=["task"],
        optional_inputs=["scope", "frameworks"],
    ))
    
    logger.debug("Registered default workflows: explain, review, guide, research")
