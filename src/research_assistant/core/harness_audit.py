"""
Harness Audit — systematic review of workflow assumptions.

Level 3 upgrade: Every component encodes an assumption about what the model
can't do. Those assumptions go stale. This module audits them on-demand
or when the model changes.

Checks:
- Are complexity thresholds still right? (7.5 pass, 70% context, max 5 iters)
- Is the workflow doing work the model now handles natively?
- Are there new capabilities not being exploited?
- Are any error patterns resolved and stale?

Run via: ra audit --persona PERSONA
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class AuditFinding:
    """Single audit finding."""
    category: str  # threshold, redundancy, capability, stale_pattern
    component: str  # Which component the finding applies to
    finding: str
    recommendation: str
    severity: str  # info, warning, action_needed


@dataclass
class AuditReport:
    """Complete audit report."""
    timestamp: str
    model: str
    findings: List[AuditFinding]
    workflow_stats: Dict[str, Any]
    recommendations: List[str]

    def to_markdown(self) -> str:
        lines = [
            f"# Harness Audit Report",
            f"*Generated: {self.timestamp} | Model: {self.model}*\n",
            f"## Workflow Statistics",
        ]
        for k, v in self.workflow_stats.items():
            lines.append(f"- {k}: {v}")

        lines.append(f"\n## Findings ({len(self.findings)})\n")
        for i, f in enumerate(self.findings, 1):
            icon = {"info": "ℹ️", "warning": "⚠️", "action_needed": "🔴"}.get(f.severity, "•")
            lines.append(f"{icon} **{f.category}** ({f.component})")
            lines.append(f"  {f.finding}")
            lines.append(f"  → {f.recommendation}\n")

        if self.recommendations:
            lines.append("## Top Recommendations\n")
            for r in self.recommendations:
                lines.append(f"1. {r}")

        return "\n".join(lines)


def run_audit(
    persona_dir: Path,
    model_name: str = "unknown",
    log_file: Optional[Path] = None,
) -> AuditReport:
    """
    Run a harness audit against workflow history and current configuration.
    """
    findings: List[AuditFinding] = []
    stats: Dict[str, Any] = {}

    # Load workflow history
    history = _load_history(log_file or persona_dir.parent.parent / "logs" / "workflow_history.jsonl")
    stats["total_runs"] = len(history)

    if history:
        # Analyze score distribution
        scores = [h.get("score", 0) for h in history]
        stats["avg_score"] = round(sum(scores) / len(scores), 1)
        stats["min_score"] = min(scores)
        stats["max_score"] = max(scores)
        stats["pass_rate"] = f"{sum(1 for s in scores if s >= 7.5) / len(scores) * 100:.0f}%"

        # Analyze iteration counts
        iters = [h.get("reasoning_iterations", 0) for h in history]
        stats["avg_reasoning_iters"] = round(sum(iters) / len(iters), 1)
        stats["max_reasoning_iters"] = max(iters)

        # Check threshold findings
        findings.extend(_audit_thresholds(history, scores, iters))

        # Check for stale patterns
        findings.extend(_audit_stale_patterns(history))

    # Check lessons file for resolved patterns
    lessons_path = persona_dir / "doc" / "lessons_learned.md"
    if lessons_path.exists():
        findings.extend(_audit_lessons(lessons_path))

    # Check for redundancy in heuristic pre-checks
    findings.extend(_audit_redundancy(history))

    # Generate top recommendations
    recommendations = _generate_recommendations(findings)

    return AuditReport(
        timestamp=datetime.now().isoformat(),
        model=model_name,
        findings=findings,
        workflow_stats=stats,
        recommendations=recommendations,
    )


def _load_history(log_file: Path) -> List[Dict]:
    """Load workflow history from JSONL file."""
    if not log_file.exists():
        return []
    entries = []
    for line in log_file.read_text().strip().split('\n'):
        if line.strip():
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def _audit_thresholds(history: List[Dict], scores: List[float], iters: List[int]) -> List[AuditFinding]:
    """Check if current thresholds are still appropriate."""
    findings = []

    # If most runs pass on first iteration, threshold may be too low
    first_iter_passes = sum(1 for h in history if h.get("reasoning_iterations", 0) <= 1 and h.get("score", 0) >= 7.5)
    if len(history) > 5 and first_iter_passes / len(history) > 0.8:
        findings.append(AuditFinding(
            category="threshold",
            component="AnalystAgent.PASS_THRESHOLD",
            finding=f"{first_iter_passes}/{len(history)} runs pass on first iteration. Threshold 7.5 may be too lenient.",
            recommendation="Consider raising PASS_THRESHOLD to 8.0 to push for higher quality.",
            severity="warning",
        ))

    # If runs consistently hit max iterations without passing
    max_iter_hits = sum(1 for i in iters if i >= 5)
    if len(history) > 5 and max_iter_hits / len(history) > 0.3:
        findings.append(AuditFinding(
            category="threshold",
            component="WorkflowInvoker.MAX_REASONING_ITERATIONS",
            finding=f"{max_iter_hits}/{len(history)} runs hit max iterations (5). Wasting compute on unimprovable output.",
            recommendation="Either lower the pass threshold or add early-exit when score plateaus across iterations.",
            severity="action_needed",
        ))

    # Check if average score is very high (model improved)
    avg = sum(scores) / len(scores) if scores else 0
    if avg > 8.5 and len(history) > 10:
        findings.append(AuditFinding(
            category="threshold",
            component="Overall",
            finding=f"Average score is {avg:.1f}/10 across {len(history)} runs. Model may have improved.",
            recommendation="Run a capability probe to check if heuristic pre-checks are still needed.",
            severity="info",
        ))

    return findings


def _audit_stale_patterns(history: List[Dict]) -> List[AuditFinding]:
    """Check for error patterns that no longer occur."""
    findings = []

    # Check if recent runs (last 10) have different characteristics than older runs
    if len(history) < 20:
        return findings

    recent = history[-10:]
    older = history[:-10]

    recent_avg = sum(h.get("score", 0) for h in recent) / len(recent)
    older_avg = sum(h.get("score", 0) for h in older) / len(older)

    if recent_avg - older_avg > 1.0:
        findings.append(AuditFinding(
            category="stale_pattern",
            component="Scoring",
            finding=f"Recent avg score ({recent_avg:.1f}) is significantly higher than older ({older_avg:.1f}). Model or prompts improved.",
            recommendation="Review if older workarounds (extra iterations, verbose prompts) are still needed.",
            severity="info",
        ))

    return findings


def _audit_lessons(lessons_path: Path) -> List[AuditFinding]:
    """Check lessons file for patterns that may be resolved."""
    findings = []
    content = lessons_path.read_text()
    lessons = [l.strip() for l in content.split('\n') if l.strip().startswith('-')]

    if len(lessons) > 30:
        findings.append(AuditFinding(
            category="stale_pattern",
            component="LearnerAgent",
            finding=f"{len(lessons)} lessons accumulated. Older lessons may be stale or contradictory.",
            recommendation="Prune lessons older than 30 days or with low relevance scores.",
            severity="warning",
        ))

    return findings


def _audit_redundancy(history: List[Dict]) -> List[AuditFinding]:
    """Check if heuristic pre-checks are catching anything."""
    findings = []

    # If no runs have score 0 (heuristic catches), the pre-checks may be redundant
    zero_scores = sum(1 for h in history if h.get("score", 0) == 0)
    if len(history) > 10 and zero_scores == 0:
        findings.append(AuditFinding(
            category="redundancy",
            component="AnalystAgent._heuristic_precheck",
            finding="No runs triggered heuristic pre-check (score=0) in recent history.",
            recommendation="The model may now reliably produce non-empty output. Consider simplifying pre-checks.",
            severity="info",
        ))

    return findings


def _generate_recommendations(findings: List[AuditFinding]) -> List[str]:
    """Generate top-level recommendations from findings."""
    recs = []
    action_needed = [f for f in findings if f.severity == "action_needed"]
    warnings = [f for f in findings if f.severity == "warning"]

    for f in action_needed[:3]:
        recs.append(f.recommendation)
    for f in warnings[:2]:
        recs.append(f.recommendation)

    if not recs:
        recs.append("No urgent issues found. Schedule next audit in 30 days or on model change.")

    return recs
