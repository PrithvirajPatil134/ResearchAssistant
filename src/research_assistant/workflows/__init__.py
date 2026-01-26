"""
Workflow orchestration for Research Assistant.

Following adw-core-ws pattern:
- WorkflowInvoker: Maps workflow names to action sequences
- WorkflowRunner: Executes actions with state management
- WorkflowSpec: Defines workflow structure
"""

from .invoker import WorkflowInvoker, WorkflowSpec, WorkflowResult

__all__ = ["WorkflowInvoker", "WorkflowSpec", "WorkflowResult"]
