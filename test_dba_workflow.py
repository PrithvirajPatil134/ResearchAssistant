#!/usr/bin/env python3
"""Test DBA workflow with DRO topic."""

import sys
sys.path.insert(0, 'src')

from research_assistant.workflows.invoker import WorkflowInvoker

print("Starting DBA workflow test...")
print("Topic: digital resource orchestration and capital efficiency in SaaS management")
print("-" * 60)

result = WorkflowInvoker.invoke(
    workflow_name='explain',
    persona_name='DBA',
    initial_state={'topic': 'digital resource orchestration and capital efficiency in SaaS management'},
    show_progress=True
)

print("\n" + "=" * 60)
print(f"Success: {result.success}")
print(f"Score: {result.final_score}/10")
print(f"Reasoning Iterations: {result.reasoning_iterations}")
print(f"Validation Iterations: {result.validation_iterations}")
print(f"Execution Time: {result.execution_time_ms}ms")

if result.output_path:
    print(f"\nOutput saved to: {result.output_path}")
    print("\nFirst 2000 chars of output:")
    print("-" * 60)
    with open(result.output_path) as f:
        print(f.read()[:2000])

if result.error:
    print(f"\nError: {result.error}")
