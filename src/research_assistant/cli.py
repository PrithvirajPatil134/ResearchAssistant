"""
Research Assistant CLI - Command-line interface for research workflows.

Usage:
    ra explain "Brand Equity" --persona QNTR
    ra review submission.pdf --persona QNTR
    ra guide "Assignment approach" --persona QNTR
    ra workflow list
    ra persona list
"""

from pathlib import Path
from typing import Optional

import click


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.version_option(version="0.1.0", prog_name="ra")
@click.pass_context
def cli(ctx: click.Context, verbose: bool):
    """Research Assistant - AI-powered academic workflow automation."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose


@cli.command()
@click.argument("topic")
@click.option("--persona", "-p", required=True, help="Persona name (e.g., QNTR)")
@click.pass_context
def explain(ctx: click.Context, topic: str, persona: str):
    """Explain a concept using persona's teaching style.
    
    Output: personas/{PERSONA}/output/explain_{timestamp}.md
    """
    import logging
    
    verbose = ctx.obj.get("verbose", False)
    if verbose:
        logging.basicConfig(
            level=logging.INFO,
            format='%(name)s - %(levelname)s - %(message)s'
        )
    
    from research_assistant.workflows import WorkflowInvoker
    
    result = WorkflowInvoker.invoke(
        workflow_name="explain",
        persona_name=persona,
        initial_state={"topic": topic},
    )
    
    if result.success:
        click.echo(click.style(f"✅ Output: {result.output_path}", fg="green"))
        click.echo(f"   Score: {result.final_score}/10 | Reasoning iterations: {result.reasoning_iterations} | Validation: {result.validation_iterations}")
        click.echo(f"   Time: {result.execution_time_ms}ms | KB files: {result.artifacts.get('extracted_files', 0)}")
    else:
        click.echo(click.style(f"❌ Error: {result.error}", fg="red"), err=True)
        ctx.exit(1)


@cli.command()
@click.argument("submission_path", type=click.Path(exists=True, path_type=Path))
@click.option("--persona", "-p", required=True, help="Persona name")
@click.option("--rubric", type=click.Path(exists=True), help="Rubric file")
@click.pass_context
def review(ctx: click.Context, submission_path: Path, persona: str, rubric: Optional[str]):
    """Review a submission against persona's standards.
    
    Output: personas/{PERSONA}/output/review_{timestamp}.md
    """
    from research_assistant.workflows import WorkflowInvoker
    
    state = {"submission_path": str(submission_path)}
    if rubric:
        state["rubric_path"] = rubric
    
    result = WorkflowInvoker.invoke(
        workflow_name="review",
        persona_name=persona,
        initial_state=state,
    )
    
    if result.success:
        click.echo(click.style(f"✅ Review saved: {result.output_path}", fg="green"))
    else:
        click.echo(click.style(f"❌ Error: {result.error}", fg="red"), err=True)
        ctx.exit(1)


@cli.command()
@click.argument("assignment")
@click.option("--persona", "-p", required=True, help="Persona name")
@click.pass_context
def guide(ctx: click.Context, assignment: str, persona: str):
    """Get assignment guidance (no direct answers).
    
    Output: personas/{PERSONA}/output/guide_{timestamp}.md
    """
    from research_assistant.workflows import WorkflowInvoker
    
    result = WorkflowInvoker.invoke(
        workflow_name="guide",
        persona_name=persona,
        initial_state={"assignment": assignment},
    )
    
    if result.success:
        click.echo(click.style(f"✅ Guidance saved: {result.output_path}", fg="green"))
    else:
        click.echo(click.style(f"❌ Error: {result.error}", fg="red"), err=True)
        ctx.exit(1)


@cli.group()
def workflow():
    """Workflow management commands."""
    pass


@workflow.command("list")
def workflow_list():
    """List available workflows."""
    from research_assistant.workflows import WorkflowInvoker
    
    click.echo("\nAvailable workflows:")
    for name in WorkflowInvoker.list_workflows():
        spec = WorkflowInvoker.get_spec(name)
        if spec:
            actions = " → ".join(a.name for a in spec.actions)
            click.echo(f"  • {name}: {spec.description}")
            click.echo(f"    Actions: {actions}")
            click.echo(f"    Required: {spec.required_inputs}")
    click.echo()


@workflow.command("run")
@click.argument("name")
@click.argument("task")
@click.option("--persona", "-p", required=True, help="Persona name")
@click.pass_context
def workflow_run(ctx: click.Context, name: str, task: str, persona: str):
    """Run a named workflow."""
    from research_assistant.workflows import WorkflowInvoker
    
    result = WorkflowInvoker.invoke(
        workflow_name=name,
        persona_name=persona,
        initial_state={"task": task, "topic": task, "assignment": task},
    )
    
    if result.success:
        click.echo(click.style(f"✅ Output: {result.output_path}", fg="green"))
        click.echo(f"   Time: {result.execution_time_ms}ms")
    else:
        click.echo(click.style(f"❌ Error: {result.error}", fg="red"), err=True)
        ctx.exit(1)


@cli.group()
def persona():
    """Persona management commands."""
    pass


@persona.command("list")
def persona_list():
    """List available personas."""
    from research_assistant.personas import PersonaLoader
    
    personas_dir = Path(__file__).parent / "personas"
    loader = PersonaLoader(personas_dir)
    
    personas = loader.list_available()
    if personas:
        click.echo("\nAvailable personas:")
        for p in personas:
            click.echo(f"  • {p}")
        click.echo()
    else:
        click.echo("No personas found")


@persona.command("info")
@click.argument("name")
def persona_info(name: str):
    """Show persona details."""
    from research_assistant.personas import PersonaLoader
    
    personas_dir = Path(__file__).parent / "personas"
    loader = PersonaLoader(personas_dir)
    
    try:
        p = loader.load(name)
        summary = loader.get_persona_summary(p)
        
        click.echo(f"\n{name} Persona:")
        click.echo(f"  Name: {summary['identity']}")
        click.echo(f"  Domain: {summary['domain']}")
        click.echo(f"  Knowledge Sources: {summary['knowledge_sources']}")
        click.echo(f"  Guidelines: {summary['guidelines_count']}")
        click.echo(f"  Configured Agents: {', '.join(summary['configured_agents'])}")
        click.echo()
    except ValueError as e:
        click.echo(click.style(f"Error: {e}", fg="red"), err=True)


def main():
    """CLI entry point."""
    cli()


if __name__ == "__main__":
    main()
