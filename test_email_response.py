#!/usr/bin/env python3
"""Test email response with image reading."""

import sys
sys.path.insert(0, 'src')

from pathlib import Path
from research_assistant.workflows.invoker import WorkflowInvoker

# The actual command that was run
query = 'Generate an appropriate response for Prof. Cardasso\'s email. The screenshot of the email is at /Users/propatil/workplace/ResearchAssistant/src/research_assistant/spaces/DBA/communication/ProfCardasso_email_2026-02-05 at 4.21.20 PM.png'

print("=" * 70)
print("Testing Email Response Guide Workflow")
print("=" * 70)
print(f"Query: {query[:100]}...")
print(f"Persona: DBA")
print(f"Workflow: guide")
print("-" * 70)

result = WorkflowInvoker.invoke(
    workflow_name='guide',
    persona_name='DBA',
    initial_state={'assignment': query},  # guide workflow expects 'assignment'
    show_progress=True
)

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)
print(f"Success: {result.success}")
print(f"Final Score: {result.final_score}/10")
print(f"Reasoning Iterations: {result.reasoning_iterations}")
print(f"Validation Iterations: {result.validation_iterations}")
print(f"Execution Time: {result.execution_time_ms}ms")

if result.output_path:
    print(f"\nOutput saved to: {result.output_path}")
    print("\nFirst 1500 chars of output:")
    print("-" * 70)
    with open(result.output_path) as f:
        content = f.read()
        print(content[:1500])
        print("\n[...truncated...]")

if result.error:
    print(f"\nError: {result.error}")
else:
    print("\n✅ Test completed successfully!")
