"""
Reader Agent - Extracts and parses content from knowledge base.

Handles DOCX, Excel, PDF, and text files.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import zipfile
import xml.etree.ElementTree as ET

from .base import BaseAgent, AgentResult

logger = logging.getLogger(__name__)


@dataclass
class ExtractedContent:
    """Content extracted from a file."""
    source_file: str
    content_type: str  # text, table, structured
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    relevance_score: float = 0.0


class ReaderAgent(BaseAgent):
    """
    Reads and extracts content from knowledge base files.
    
    Supports:
    - DOCX (Word documents)
    - XLSX (Excel spreadsheets)
    - PDF (text extraction)
    - TXT, MD (plain text)
    
    Key responsibilities:
    - Parse various file formats
    - Extract relevant content based on query
    - Score content relevance
    - Store extracted content in Memory
    """
    
    def __init__(self, memory, context_guard):
        super().__init__("reader", memory, context_guard)
        self._knowledge_dir: Optional[Path] = None
        self._extracted_cache: Dict[str, ExtractedContent] = {}
        self._cross_space_dirs: List[Dict[str, Any]] = []  # [{path: Path, origin: str}]
    
    def set_knowledge_dir(self, path: Path) -> None:
        """Set the knowledge directory to read from."""
        self._knowledge_dir = path
    
    def set_cross_space_sources(self, sources: list) -> None:
        """
        Register cross-space knowledge sources for reading.
        
        Each source is a KnowledgeSource with metadata['cross_space_origin'] set.
        The reader groups them by origin space and makes their parent directories
        available for scanning, tagged with provenance.
        """
        seen_dirs = {}
        for source in sources:
            origin = source.metadata.get("cross_space_origin", "unknown")
            parent = source.path.parent
            key = str(parent)
            if key not in seen_dirs:
                seen_dirs[key] = {"path": parent, "origin": origin}
        
        self._cross_space_dirs = list(seen_dirs.values())
        if self._cross_space_dirs:
            logger.info(
                f"[ReaderAgent] Registered {len(self._cross_space_dirs)} cross-space "
                f"knowledge directories from {len(set(d['origin'] for d in self._cross_space_dirs))} spaces"
            )
    
    def execute(self, **kwargs) -> AgentResult:
        """Main execution - extract content relevant to query."""
        query = kwargs.get("query", "")
        knowledge_dir = kwargs.get("knowledge_dir") or self._knowledge_dir
        
        if not knowledge_dir:
            return AgentResult(success=False, output=None, metadata={"error": "No knowledge directory"})
        
        extracted = self.extract_relevant(query, Path(knowledge_dir))
        
        # Store in memory
        for content in extracted:
            self.memory.add_fact(
                f"From {content.source_file}: {content.content[:200]}...",
                source=self.agent_id,
                importance=int(content.relevance_score * 10)
            )
        
        return AgentResult(
            success=True,
            output=extracted,
            tokens_used=sum(len(c.content.split()) for c in extracted),
            metadata={"files_read": len(extracted)}
        )
    
    def extract_relevant(self, query: str, knowledge_dir: Path) -> List[ExtractedContent]:
        """Extract content relevant to query from knowledge directory.
        
        Strategy:
        1. Extract ALL explicitly referenced files/dirs from query → load with full content
        2. Scan KB directory for additional relevant files → load with standard limits
        3. Respect a total token budget to avoid blowing up the prompt
        """
        self.log_operation("extract_relevant", 100)
        
        relevant_content = []
        seen_files = set()
        query_terms = [t.lower() for t in query.split() if len(t) > 3]
        
        # Token budget: ~80K chars ≈ 20K tokens for KB context
        TOKEN_BUDGET_CHARS = 80000
        chars_used = 0
        
        # --- Phase 1: Load explicitly referenced files with generous limits ---
        explicit_paths = self._extract_all_file_paths(query)
        for filepath in explicit_paths:
            if chars_used >= TOKEN_BUDGET_CHARS:
                logger.warning(f"[ReaderAgent] Token budget exhausted, skipping remaining explicit files")
                break
            
            content = self._read_file(filepath, max_chars=30000)  # 30K per explicit file
            if content:
                content.relevance_score = 1.0  # Explicit = max relevance
                remaining = TOKEN_BUDGET_CHARS - chars_used
                if len(content.content) > remaining:
                    content.content = content.content[:remaining]
                chars_used += len(content.content)
                relevant_content.append(content)
                seen_files.add(str(filepath))
                logger.info(f"[ReaderAgent] Loaded explicit: {filepath.name} ({len(content.content)} chars)")
        
        # --- Phase 2: Scan KB directory for additional relevant files ---
        if knowledge_dir.exists() and chars_used < TOKEN_BUDGET_CHARS:
            scored_content = []
            
            for filepath in knowledge_dir.rglob("*"):
                if filepath.is_file() and str(filepath) not in seen_files:
                    content = self._read_file(filepath)  # Standard 10K limit
                    if content:
                        relevance = self._calculate_relevance(content.content, query_terms)
                        content.relevance_score = relevance
                        if relevance > 0.1:
                            scored_content.append(content)
            
            # Sort by relevance, fill remaining budget
            scored_content.sort(key=lambda x: x.relevance_score, reverse=True)
            
            for content in scored_content:
                if chars_used >= TOKEN_BUDGET_CHARS:
                    break
                remaining = TOKEN_BUDGET_CHARS - chars_used
                if len(content.content) > remaining:
                    content.content = content.content[:remaining]
                chars_used += len(content.content)
                relevant_content.append(content)
        
        # --- Phase 3: Scan cross-space knowledge directories (if configured) ---
        if self._cross_space_dirs and chars_used < TOKEN_BUDGET_CHARS:
            cross_scored = []
            
            for dir_info in self._cross_space_dirs:
                cross_dir = dir_info["path"]
                origin = dir_info["origin"]
                
                if not cross_dir.exists():
                    continue
                
                for filepath in cross_dir.rglob("*"):
                    if filepath.is_file() and str(filepath) not in seen_files:
                        content = self._read_file(filepath)
                        if content:
                            relevance = self._calculate_relevance(content.content, query_terms)
                            content.relevance_score = relevance
                            if relevance > 0.15:  # Slightly higher threshold for cross-space
                                # Tag with provenance
                                content.metadata["cross_space_origin"] = origin
                                content.source_file = f"[{origin}] {content.source_file}"
                                cross_scored.append(content)
            
            cross_scored.sort(key=lambda x: x.relevance_score, reverse=True)
            
            for content in cross_scored:
                if chars_used >= TOKEN_BUDGET_CHARS:
                    break
                remaining = TOKEN_BUDGET_CHARS - chars_used
                if len(content.content) > remaining:
                    content.content = content.content[:remaining]
                chars_used += len(content.content)
                relevant_content.append(content)
                seen_files.add(str(content.metadata.get("original_path", content.source_file)))
            
            if cross_scored:
                logger.info(
                    f"[ReaderAgent] Cross-space: {len([c for c in relevant_content if c.metadata.get('cross_space_origin')])} "
                    f"files added from other spaces"
                )
        
        logger.info(
            f"[ReaderAgent] Total: {len(relevant_content)} files, "
            f"{chars_used} chars (~{chars_used // 4} tokens)"
        )
        
        return relevant_content
    
    def _extract_file_path(self, query: str) -> Optional[Path]:
        """Extract explicit file path from query. Returns first match. See _extract_all_file_paths for multiple."""
        paths = self._extract_all_file_paths(query)
        return paths[0] if paths else None

    def _extract_all_file_paths(self, query: str) -> List[Path]:
        """Extract ALL explicit file paths and directory paths from query."""
        import re
        
        found_paths = []
        
        # File patterns — allow apostrophes and other common filename chars
        file_patterns = [
            r'(?:at\s+)?(/[^\n"<>]+?\.(?:eml|png|jpg|jpeg|pdf|docx|txt|md|xlsx))\b',
            r'["\']([/~][^"\']+?\.(?:eml|png|jpg|jpeg|pdf|docx|txt|md|xlsx))["\']',
            r'\((/[^)]+?\.(?:eml|png|jpg|jpeg|pdf|docx|txt|md|xlsx))\)',
        ]
        
        # Directory patterns (e.g., "at /path/to/dir/ (C2 through C15)")
        dir_patterns = [
            r'(?:at\s+)?(/[^\n"<>]+?/)\s*\(',
            r'(?:at\s+)?(/[^\n"<>]+?/)(?:\s|$)',
        ]
        
        seen = set()
        
        for pattern in file_patterns:
            for match in re.finditer(pattern, query, re.IGNORECASE):
                filepath_str = match.group(1).strip()
                filepath = self._resolve_path(filepath_str)
                if filepath and filepath.is_file() and str(filepath) not in seen:
                    seen.add(str(filepath))
                    found_paths.append(filepath)
        
        # Also resolve directories — load all readable files within them
        for pattern in dir_patterns:
            for match in re.finditer(pattern, query, re.IGNORECASE):
                dirpath_str = match.group(1).strip()
                dirpath = Path(dirpath_str)
                if dirpath.is_dir():
                    for child in sorted(dirpath.rglob("*")):
                        if child.is_file() and child.suffix.lower() in ['.md', '.txt', '.docx', '.pdf', '.xlsx', '.eml'] and str(child) not in seen:
                            seen.add(str(child))
                            found_paths.append(child)
        
        logger.info(f"[ReaderAgent] Extracted {len(found_paths)} explicit paths from query")
        return found_paths

    def _resolve_path(self, filepath_str: str) -> Optional[Path]:
        """Resolve a file path string, handling ~ expansion and Unicode normalization."""
        import unicodedata
        
        filepath = Path(filepath_str)
        
        if filepath.exists():
            return filepath
        
        if filepath_str.startswith('~'):
            filepath = Path(filepath_str).expanduser()
            if filepath.exists():
                return filepath
        
        # Fuzzy match in parent directory (handles Unicode issues)
        parent = filepath.parent
        if parent.exists():
            target_name = filepath.name
            for file in parent.iterdir():
                norm_file = unicodedata.normalize('NFKC', file.name)
                norm_target = unicodedata.normalize('NFKC', target_name)
                if norm_file == norm_target:
                    return file
        
        return None
    
    def _read_file(self, filepath: Path, max_chars: int = 10000) -> Optional[ExtractedContent]:
        """Read content from a file based on its type."""
        suffix = filepath.suffix.lower()
        
        try:
            if suffix in ['.txt', '.md']:
                return self._read_text(filepath, max_chars)
            elif suffix == '.eml':
                return self._read_eml(filepath)
            elif suffix == '.docx':
                return self._read_docx(filepath, max_chars)
            elif suffix == '.xlsx':
                return self._read_xlsx(filepath)
            elif suffix == '.pdf':
                return self._read_pdf(filepath)
            elif suffix in ['.png', '.jpg', '.jpeg']:
                return self._read_image(filepath)
            else:
                return None
        except Exception as e:
            logger.warning(f"Failed to read {filepath}: {e}")
            return None
    
    def _read_text(self, filepath: Path, max_chars: int = 50000) -> ExtractedContent:
        """Read plain text file. No artificial truncation — budget managed by extract_relevant."""
        content = filepath.read_text(errors='ignore')[:max_chars]
        return ExtractedContent(
            source_file=str(filepath.name),
            content_type="text",
            content=content,
        )
    
    def _read_eml(self, filepath: Path) -> Optional[ExtractedContent]:
        """Read EML email file."""
        try:
            import email
            from email import policy
            
            with open(filepath, 'rb') as f:
                msg = email.message_from_binary_file(f, policy=policy.default)
            
            # Extract email components
            parts = []
            parts.append(f"From: {msg.get('From', 'Unknown')}")
            parts.append(f"To: {msg.get('To', 'Unknown')}")
            parts.append(f"Date: {msg.get('Date', 'Unknown')}")
            parts.append(f"Subject: {msg.get('Subject', 'No Subject')}")
            parts.append("\n" + "-" * 50 + "\n")
            
            # Get email body
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True)
                        if body:
                            parts.append(body.decode('utf-8', errors='ignore'))
                            break
            else:
                body = msg.get_payload(decode=True)
                if body:
                    parts.append(body.decode('utf-8', errors='ignore'))
            
            content = '\n'.join(parts)[:10000]
            
            return ExtractedContent(
                source_file=str(filepath.name),
                content_type="email",
                content=content,
                metadata={
                    "format": "eml",
                    "from": msg.get('From'),
                    "subject": msg.get('Subject'),
                    "date": msg.get('Date'),
                }
            )
        except Exception as e:
            logger.warning(f"EML read error: {e}")
            return None
    
    def _read_docx(self, filepath: Path, max_chars: int = 50000) -> Optional[ExtractedContent]:
        """Read DOCX file by extracting XML."""
        try:
            text_parts = []
            with zipfile.ZipFile(filepath) as z:
                if 'word/document.xml' in z.namelist():
                    xml_content = z.read('word/document.xml')
                    tree = ET.fromstring(xml_content)
                    
                    # Extract text from w:t elements
                    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                    for elem in tree.iter():
                        if elem.text and elem.tag.endswith('}t'):
                            text_parts.append(elem.text)
            
            content = ' '.join(text_parts)[:max_chars]
            return ExtractedContent(
                source_file=str(filepath.name),
                content_type="text",
                content=content,
                metadata={"format": "docx"}
            )
        except Exception as e:
            logger.warning(f"DOCX read error: {e}")
            return None
    
    def _read_xlsx(self, filepath: Path) -> Optional[ExtractedContent]:
        """Read Excel file - extracts all content for LLM comprehension."""
        try:
            with zipfile.ZipFile(filepath) as z:
                # Read shared strings (cell text values) - these contain ALL text data
                shared_strings = []
                if 'xl/sharedStrings.xml' in z.namelist():
                    ss_xml = z.read('xl/sharedStrings.xml')
                    ss_tree = ET.fromstring(ss_xml)
                    ns_ss = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
                    for t_elem in ss_tree.iter(f'{{{ns_ss}}}t'):
                        if t_elem.text:
                            shared_strings.append(t_elem.text)
                
                # Read sheet1 data with row structure
                rows_data = []
                if 'xl/worksheets/sheet1.xml' in z.namelist():
                    sheet_xml = z.read('xl/worksheets/sheet1.xml')
                    sheet_tree = ET.fromstring(sheet_xml)
                    ns_sheet = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
                    
                    for row in sheet_tree.iter(f'{{{ns_sheet}}}row'):
                        row_values = []
                        for cell in row.iter(f'{{{ns_sheet}}}c'):
                            cell_value = ""
                            cell_type = cell.get('t', '')
                            v_elem = cell.find(f'{{{ns_sheet}}}v')
                            if v_elem is not None and v_elem.text:
                                if cell_type == 's':  # Shared string reference
                                    idx = int(v_elem.text)
                                    if idx < len(shared_strings):
                                        cell_value = shared_strings[idx]
                                else:
                                    cell_value = v_elem.text
                            row_values.append(cell_value)
                        if any(row_values):
                            rows_data.append(row_values)
                
                # Check if we have meaningful row data (more than sparse form data)
                meaningful_rows = len(rows_data) > 3 and len(rows_data[0]) > 3 if rows_data else False
                
                # Format as structured content for LLM
                if meaningful_rows:
                    # Traditional tabular data
                    headers = rows_data[0]
                    lines = [f"## Excel Data: {filepath.name}"]
                    lines.append(f"**Columns**: {' | '.join(h for h in headers if h)}")
                    lines.append("")
                    
                    for row in rows_data[1:60]:
                        row_parts = []
                        for i, val in enumerate(row):
                            if val and i < len(headers) and headers[i]:
                                row_parts.append(f"**{headers[i]}**: {val}")
                        if row_parts:
                            lines.append("- " + " | ".join(row_parts))
                    
                    content = '\n'.join(lines)
                else:
                    # Form-based or sparse data - use ALL shared strings
                    # This captures questionnaires, surveys, and structured forms
                    lines = [f"## Excel Content: {filepath.name}"]
                    lines.append(f"**Total items**: {len(shared_strings)}")
                    lines.append("")
                    
                    # Group content by detecting section headers
                    current_section = "Content"
                    for i, s in enumerate(shared_strings):
                        # Detect section headers (often short, capitalized)
                        if len(s) < 50 and s.strip() and not any(c.isdigit() for c in s[:3]):
                            if s in ['Demographics', 'Antecedents', 'Mediators', 'Moderators', 
                                    'Outcomes', 'Control Variables', 'Survey', 'Questions']:
                                current_section = s
                                lines.append(f"\n### {current_section}")
                                continue
                        
                        # Format each entry
                        if s.strip():
                            lines.append(f"- {s}")
                    
                    content = '\n'.join(lines)
            
            return ExtractedContent(
                source_file=str(filepath.name),
                content_type="table",
                content=content,
                metadata={"format": "xlsx", "shared_strings": len(shared_strings), "rows": len(rows_data)}
            )
        except Exception as e:
            logger.warning(f"XLSX read error: {e}")
            return None
    
    def _read_pdf(self, filepath: Path, max_chars: int = 0) -> Optional[ExtractedContent]:
        """Read PDF with actual text extraction using PyPDF2.
        
        Extracts ALL pages by default (max_chars=0 means no limit).
        Token budget management is handled by extract_relevant(), not here.
        Per binary-file-reading steering rule: never truncate source documents
        at the extraction layer.
        """
        try:
            import PyPDF2
            
            text_parts = []
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            
            content = '\n\n'.join(text_parts)
            if max_chars > 0:
                content = content[:max_chars]
            
            if not content.strip():
                # Fallback: PDF might be image-based (scanned)
                logger.warning(f"[ReaderAgent] PDF has no extractable text (may be scanned): {filepath.name}")
                return ExtractedContent(
                    source_file=str(filepath.name),
                    content_type="reference",
                    content=f"[PDF Document: {filepath.name} — {num_pages} pages, scanned/image-based, text extraction not possible]",
                    metadata={"format": "pdf", "pages": num_pages, "requires_ocr": True}
                )
            
            logger.info(f"[ReaderAgent] PDF extracted: {filepath.name} ({num_pages} pages, {len(content)} chars)")
            
            return ExtractedContent(
                source_file=str(filepath.name),
                content_type="text",
                content=content,
                metadata={"format": "pdf", "pages": num_pages}
            )
            
        except Exception as e:
            logger.warning(f"[ReaderAgent] PDF read error for {filepath.name}: {e}")
            return ExtractedContent(
                source_file=str(filepath.name),
                content_type="reference",
                content=f"[PDF Document: {filepath.name} — read error: {e}]",
                metadata={"format": "pdf", "error": str(e)}
            )
    
    def _read_image(self, filepath: Path) -> Optional[ExtractedContent]:
        """Read image file using vision model (Anthropic API) for text extraction."""
        try:
            import anthropic
            import base64
            import os
            
            logger.info(f"[ReaderAgent] Reading image with vision: {filepath.name}")
            
            # Check for API key
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                logger.error("[ReaderAgent] ANTHROPIC_API_KEY not set")
                return ExtractedContent(
                    source_file=str(filepath.name),
                    content_type="reference",
                    content=f"[Image: {filepath.name} - no API key]",
                    metadata={"format": "image", "error": "ANTHROPIC_API_KEY not set"}
                )
            
            # Read and encode image
            with open(filepath, 'rb') as f:
                image_data = base64.standard_b64encode(f.read()).decode('utf-8')
            
            # Determine media type
            suffix = filepath.suffix.lower()
            media_type_map = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
            }
            media_type = media_type_map.get(suffix, 'image/png')
            
            # Create Anthropic client
            client = anthropic.Anthropic(api_key=api_key)
            
            # Build vision prompt
            vision_prompt = """Extract ALL text content from this image.

If it's an email or message:
- Extract sender, recipient, date, subject
- Extract full message body
- Preserve formatting and structure

If it's a document or form:
- Extract all text maintaining logical order
- Preserve section headers and labels
- Include any important metadata

Output the extracted text in a clear, readable format."""
            
            # Call Claude with vision
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": vision_prompt
                            }
                        ],
                    }
                ],
            )
            
            extracted_text = message.content[0].text
            logger.info(f"[ReaderAgent] Successfully extracted {len(extracted_text)} chars from image")
            
            return ExtractedContent(
                source_file=str(filepath.name),
                content_type="image_text",
                content=extracted_text,
                metadata={"format": "image", "original_path": str(filepath)}
            )
                
        except Exception as e:
            logger.error(f"[ReaderAgent] Image read error: {e}")
            return ExtractedContent(
                source_file=str(filepath.name),
                content_type="reference",
                content=f"[Image: {filepath.name} - error: {e}]",
                metadata={"format": "image", "error": str(e)}
            )
    
    def _calculate_relevance(self, content: str, query_terms: List[str]) -> float:
        """Calculate relevance score based on term matching."""
        if not content or not query_terms:
            return 0.0
        
        content_lower = content.lower()
        matches = sum(1 for term in query_terms if term in content_lower)
        
        # Bonus for exact phrase matches
        query_phrase = ' '.join(query_terms)
        phrase_bonus = 0.3 if query_phrase in content_lower else 0.0
        
        return min(1.0, (matches / len(query_terms)) + phrase_bonus)
    
    def get_file_summary(self, filepath: Path) -> Dict[str, Any]:
        """Get summary info about a file without full extraction."""
        return {
            "name": filepath.name,
            "type": filepath.suffix,
            "size_kb": filepath.stat().st_size // 1024 if filepath.exists() else 0,
        }
