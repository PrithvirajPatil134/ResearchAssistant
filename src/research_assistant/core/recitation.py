"""
Recitation Checkpoint — re-anchors attention on original intent before composition.

Level 3 upgrade: Prevents drift toward the most verbose source.
Before composing multi-source responses, re-states:
"Original question was X. I have Y from source A, Z from source B. The user needs W."

Same principle as Manus's todo.md pattern — push the objective into recent attention.
Inserted at two points:
  A) Before final stage in multi-stage workflows
  B) Before _format_output() in all workflows
"""

from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


def build_recitation_block(
    original_query: str,
    contract: Any,  # DispatchContract, optional
    source_summaries: Optional[List[Dict[str, str]]] = None,
    stage_summaries: Optional[List[Dict[str, str]]] = None,
) -> str:
    """
    Build a recitation block that re-anchors attention on the original intent.
    
    Max ~200 words. Prepended to the next LLM call's prompt to prevent
    drift toward whatever source was most verbose.
    
    Args:
        original_query: The user's original question
        contract: DispatchContract with done_definition
        source_summaries: [{"name": "source A", "contribution": "provided X"}]
        stage_summaries: [{"name": "stage 1", "contribution": "produced Y"}]
    
    Returns:
        Recitation block string for prompt injection.
    """
    # Truncate query for recitation (keep it focused)
    query_short = original_query[:300]
    if len(original_query) > 300:
        query_short = query_short.rsplit(' ', 1)[0] + "..."

    parts = [f"## RECITATION CHECKPOINT (re-anchor before composing)"]
    parts.append(f"ORIGINAL QUESTION: {query_short}")

    # What the user needs (from contract)
    if contract and hasattr(contract, 'done_definition') and contract.done_definition:
        parts.append(f"USER NEEDS: {contract.done_definition}")

    # What we have from sources
    if source_summaries:
        source_lines = []
        for s in source_summaries[:5]:  # Cap at 5 sources
            name = s.get("name", "source")[:50]
            contrib = s.get("contribution", "content")[:80]
            source_lines.append(f"  - {name}: {contrib}")
        parts.append("AVAILABLE FROM SOURCES:\n" + "\n".join(source_lines))

    # What we have from stages
    if stage_summaries:
        stage_lines = []
        for s in stage_summaries[:5]:
            name = s.get("name", "stage")[:30]
            contrib = s.get("contribution", "output")[:80]
            stage_lines.append(f"  - {name}: {contrib}")
        parts.append("AVAILABLE FROM STAGES:\n" + "\n".join(stage_lines))

    # Completeness criteria from contract
    if contract and hasattr(contract, 'completeness_criteria') and contract.completeness_criteria:
        criteria = contract.completeness_criteria[:4]
        parts.append("MUST ADDRESS:\n" + "\n".join(f"  - {c}" for c in criteria))

    parts.append("INSTRUCTION: Compose the response addressing the ORIGINAL QUESTION above. Do not drift toward the most verbose source.")

    block = "\n".join(parts)

    # Enforce ~200 word limit
    words = block.split()
    if len(words) > 220:
        block = " ".join(words[:220]) + "\n[recitation truncated]"

    logger.info(f"[RECITATION] Built checkpoint: {len(block)} chars, {len(block.split())} words")
    return block


def build_stage_summary(stage_name: str, stage_output: str) -> Dict[str, str]:
    """
    Summarize a stage's output for the recitation checkpoint.
    Extracts the first meaningful header and a brief description.
    """
    lines = stage_output.split('\n')
    
    # Find first header
    header = stage_name
    for line in lines[:20]:
        stripped = line.strip()
        if stripped.startswith('#') and len(stripped) > 5:
            header = stripped.lstrip('#').strip()[:60]
            break

    # Count substantive content
    word_count = len(stage_output.split())
    
    return {
        "name": stage_name,
        "contribution": f"{header} ({word_count} words)",
    }
