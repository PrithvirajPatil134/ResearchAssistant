"""Learnings module — reference materials for agent design and evaluation."""

from pathlib import Path

LEARNINGS_DIR = Path(__file__).parent


def get_learnings() -> dict[str, Path]:
    """Return paths to all learning documents."""
    return {
        f.stem: f
        for f in LEARNINGS_DIR.glob("*.md")
        if f.name != "README.md"
    }
