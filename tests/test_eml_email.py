#!/usr/bin/env python3
"""Test email response workflow with EML file."""

import sys
sys.path.insert(0, 'src')

from research_assistant.workflows.invoker import WorkflowInvoker

eml_path = '/Users/propatil/workplace/ResearchAssistant/src/research_assistant/spaces/DBA/communication/Objective Review.eml'

query = f"Generate an appropriate response for Prof. Cardasso's email at {eml_path}"

print("=" * 70)
print("Testing Email Response with EML File")
print("=" * 70)
print(f"EML: {eml_path}")
print(f"Query: {query}")
print("-" * 70)

result = WorkflowInvoker.invoke(
    workflow_name='guide',
    persona_name='DBA',
    initial_state={'assignment': query},
    show_progress=True
)

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)
print(f"Success: {result.success}")
print(f"Final Score: {result.final_score}/10")
print(f"Iterations: R={result.reasoning_iterations}, V={result.validation_iterations}")

if result.output_path:
    print(f"\nOutput: {result.output_path}")
    print("\nFirst 2000 chars:")
    print("-" * 70)
    with open(result.output_path) as f:
        print(f.read()[:2000])

if result.error:
    print(f"\nError: {result.error}")
