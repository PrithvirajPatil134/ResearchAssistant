"""
Dispatch Contract — defines "what done looks like" before agents execute.

Level 3 upgrade: Pre-Dispatch Contract.
Before dispatching to agents, the contract specifies what each agent should
produce, what a complete answer includes, and what gaps to flag.

This prevents agents from doing technically correct but contextually wrong work.
The Analyst and Reviewer score against this contract, not just generic rubrics.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import logging
import json
import re

logger = logging.getLogger(__name__)


@dataclass
class AgentExpectation:
    """What a specific agent should produce for this query."""
    agent_id: str
    expected_output: str  # What this agent should find/produce
    required_elements: List[str]  # Specific items that must be present
    gap_flags: List[str]  # What to explicitly flag if missing


@dataclass
class DispatchContract:
    """
    Contract defining what "done" looks like for a specific query + workflow.
    
    Built before agent execution, consumed by Analyst and Reviewer
    to score against intent rather than generic quality.
    """
    query: str
    workflow_name: str
    done_definition: str  # 2-3 sentence description of successful output
    completeness_criteria: List[str]  # What a complete answer must include
    agent_expectations: List[AgentExpectation]
    required_sections: List[str]  # Sections the output must contain
    grounding_requirements: List[str]  # Claims that must be KB-grounded
    skip_evaluator: bool = False  # True for trivial lookups

    def to_analyst_prompt(self) -> str:
        """Format contract for injection into Analyst scoring prompt."""
        criteria = "\n".join(f"  - {c}" for c in self.completeness_criteria)
        grounding = "\n".join(f"  - {g}" for g in self.grounding_requirements)
        sections = "\n".join(f"  - {s}" for s in self.required_sections)
        return f"""## DISPATCH CONTRACT (score against this):
DONE DEFINITION: {self.done_definition}

COMPLETENESS CRITERIA:
{criteria}

REQUIRED SECTIONS:
{sections}

GROUNDING REQUIREMENTS:
{grounding}"""

    def to_reviewer_prompt(self) -> str:
        """Format contract for injection into Reviewer validation prompt."""
        criteria = "\n".join(f"  - {c}" for c in self.completeness_criteria)
        return f"""## CONTRACT (validate against this):
The output is DONE when: {self.done_definition}

MUST INCLUDE:
{criteria}"""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging/caching."""
        return {
            "query": self.query[:200],
            "workflow_name": self.workflow_name,
            "done_definition": self.done_definition,
            "completeness_criteria": self.completeness_criteria,
            "required_sections": self.required_sections,
            "grounding_requirements": self.grounding_requirements,
            "skip_evaluator": self.skip_evaluator,
        }


def build_dispatch_contract(
    query: str,
    workflow_name: str,
    extracted_content: List[str],
    persona_name: str = "",
    llm=None,
) -> DispatchContract:
    """
    Build a dispatch contract for this query + workflow.
    
    Uses LLM if available, falls back to heuristic construction.
    """
    # Detect trivial queries (short, single concept)
    is_trivial = len(query.split()) < 15 and "\n" not in query

    if llm and not is_trivial:
        contract = _build_contract_with_llm(query, workflow_name, extracted_content, persona_name, llm)
        if contract:
            return contract

    # Heuristic fallback
    return _build_contract_heuristic(query, workflow_name, extracted_content, is_trivial)


def _build_contract_with_llm(
    query: str,
    workflow_name: str,
    extracted_content: List[str],
    persona_name: str,
    llm,
) -> Optional[DispatchContract]:
    """Use LLM to generate a precise dispatch contract."""
    try:
        kb_summary = "\n".join(c[:300] for c in extracted_content[:3])

        prompt = f"""Analyze this research query and define what a COMPLETE answer looks like.

QUERY: {query[:800]}
WORKFLOW: {workflow_name}
KB SOURCES AVAILABLE: {kb_summary[:1000]}

Respond with ONLY valid JSON:
{{
  "done_definition": "2-3 sentences describing what a successful output looks like",
  "completeness_criteria": ["criterion 1", "criterion 2", "criterion 3"],
  "required_sections": ["section 1", "section 2"],
  "grounding_requirements": ["claim/topic that must be KB-grounded"]
}}"""

        response = llm.generate(
            prompt,
            "You are a research quality analyst. Output ONLY valid JSON. Be specific to the query."
        )

        if response.success and response.content.strip():
            m = re.search(r'\{.*\}', response.content, re.DOTALL)
            if m:
                data = json.loads(m.group(0))
                return DispatchContract(
                    query=query,
                    workflow_name=workflow_name,
                    done_definition=data.get("done_definition", ""),
                    completeness_criteria=data.get("completeness_criteria", []),
                    agent_expectations=[],
                    required_sections=data.get("required_sections", []),
                    grounding_requirements=data.get("grounding_requirements", []),
                    skip_evaluator=False,
                )
    except Exception as e:
        logger.warning(f"[CONTRACT] LLM contract generation failed: {e}")
    return None


def _build_contract_heuristic(
    query: str,
    workflow_name: str,
    extracted_content: List[str],
    is_trivial: bool,
) -> DispatchContract:
    """Build contract from heuristics based on workflow type and query structure."""
    query_lower = query.lower()

    # Workflow-specific defaults
    WORKFLOW_CONTRACTS = {
        "explain": {
            "done_definition": "A comprehensive explanation of the concept with KB-grounded definitions, theoretical foundations, and practical applications.",
            "completeness_criteria": [
                "Concept defined using KB terminology",
                "Theoretical foundation with proper attribution",
                "Key components/dimensions identified",
                "Practical application examples",
            ],
            "required_sections": [
                "Conceptual Definition",
                "Theoretical Foundation",
                "Key Components",
                "Practical Application",
            ],
        },
        "guide": {
            "done_definition": "Structured guidance that helps the student think through the task without giving direct answers, with KB references and reflection questions.",
            "completeness_criteria": [
                "Task understanding demonstrated",
                "Framework/approach suggested from KB",
                "Step-by-step guidance provided",
                "Reflection questions included",
                "No direct answers given",
            ],
            "required_sections": [
                "Understanding the Task",
                "Suggested Approach",
                "Step-by-Step Guidance",
                "Reflection Questions",
            ],
        },
        "review": {
            "done_definition": "A thorough review identifying strengths and weaknesses with specific, actionable feedback grounded in course criteria.",
            "completeness_criteria": [
                "Strengths identified with specifics",
                "Areas for improvement with recommendations",
                "Course criteria referenced",
                "Actionable next steps provided",
            ],
            "required_sections": [
                "Executive Summary",
                "Strengths",
                "Areas for Improvement",
                "Next Steps",
            ],
        },
        "research": {
            "done_definition": "A structured research plan with clear framing, literature mapping, methodology design, and actionable roadmap grounded in KB frameworks.",
            "completeness_criteria": [
                "Research objective clearly stated",
                "Theoretical lens identified from KB",
                "Literature gaps mapped",
                "Methodology recommended with justification",
                "Phased roadmap provided",
            ],
            "required_sections": [
                "Research Framing",
                "Literature Mapping",
                "Methodology Design",
                "Synthesis & Roadmap",
            ],
        },
        "quant": {
            "done_definition": "Rigorous statistical analysis guidance with method selection, assumption checks, analysis plan, and APA-format reporting template.",
            "completeness_criteria": [
                "Variables and data structure identified",
                "Statistical method selected with justification",
                "Assumptions listed and check procedures given",
                "Step-by-step analysis plan",
                "Reporting template with placeholders",
            ],
            "required_sections": [
                "Data Understanding",
                "Method Selection",
                "Analysis Plan",
                "Interpretation Guide",
            ],
        },
    }

    defaults = WORKFLOW_CONTRACTS.get(workflow_name, WORKFLOW_CONTRACTS["explain"])

    # Extract grounding requirements from query keywords
    grounding_reqs = []
    for content in extracted_content[:3]:
        # Find key terms from KB that appear in the query
        for word in query_lower.split():
            if len(word) > 5 and word in content.lower():
                grounding_reqs.append(f"'{word}' must be defined using KB source material")
                if len(grounding_reqs) >= 3:
                    break
        if len(grounding_reqs) >= 3:
            break

    if not grounding_reqs:
        grounding_reqs = ["Key claims must reference KB materials"]

    return DispatchContract(
        query=query,
        workflow_name=workflow_name,
        done_definition=defaults["done_definition"],
        completeness_criteria=defaults["completeness_criteria"],
        agent_expectations=[],
        required_sections=defaults["required_sections"],
        grounding_requirements=grounding_reqs,
        skip_evaluator=is_trivial,
    )
