"""
Artifact Cache - Persists intermediate stage outputs so later stages
can resume without regenerating everything from scratch.

Each workflow execution gets a cache directory:
  spaces/{PERSONA}/cache/{workflow_id}/
    stage_1_benchmark_analysis.md
    stage_2_context_ingestion.md
    stage_3_write_case_study.md
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ArtifactCache:
    """Cache intermediate workflow artifacts to disk."""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._metadata_path = self.cache_dir / "_metadata.json"
        self._metadata: Dict[str, Any] = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        if self._metadata_path.exists():
            try:
                return json.loads(self._metadata_path.read_text())
            except (json.JSONDecodeError, OSError):
                pass
        return {"created": datetime.now().isoformat(), "stages": {}}
    
    def _save_metadata(self) -> None:
        self._metadata_path.write_text(json.dumps(self._metadata, indent=2))
    
    def has_stage(self, stage_name: str) -> bool:
        """Check if a stage output is cached."""
        stage_file = self.cache_dir / f"{stage_name}.md"
        return stage_file.exists() and stage_file.stat().st_size > 0
    
    def get_stage(self, stage_name: str) -> Optional[str]:
        """Retrieve cached stage output."""
        stage_file = self.cache_dir / f"{stage_name}.md"
        if stage_file.exists():
            content = stage_file.read_text()
            if content.strip():
                logger.info(f"[CACHE] Hit: {stage_name} ({len(content)} chars)")
                return content
        logger.info(f"[CACHE] Miss: {stage_name}")
        return None
    
    def put_stage(self, stage_name: str, content: str, metadata: Optional[Dict] = None) -> None:
        """Store stage output to cache."""
        stage_file = self.cache_dir / f"{stage_name}.md"
        stage_file.write_text(content)
        
        self._metadata["stages"][stage_name] = {
            "cached_at": datetime.now().isoformat(),
            "chars": len(content),
            **(metadata or {}),
        }
        self._save_metadata()
        logger.info(f"[CACHE] Stored: {stage_name} ({len(content)} chars)")
    
    def clear(self) -> None:
        """Clear all cached artifacts."""
        for f in self.cache_dir.glob("*.md"):
            f.unlink()
        self._metadata = {"created": datetime.now().isoformat(), "stages": {}}
        self._save_metadata()
        logger.info("[CACHE] Cleared all artifacts")
    
    def summary(self) -> Dict[str, Any]:
        """Get cache summary."""
        stages = {}
        for f in self.cache_dir.glob("*.md"):
            stages[f.stem] = {"chars": f.stat().st_size}
        return {
            "cache_dir": str(self.cache_dir),
            "stages": stages,
            "total_cached": len(stages),
        }
