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
    
    def set_knowledge_dir(self, path: Path) -> None:
        """Set the knowledge directory to read from."""
        self._knowledge_dir = path
    
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
        """Extract content relevant to query from knowledge directory."""
        self.log_operation("extract_relevant", 100)
        
        relevant_content = []
        query_terms = [t.lower() for t in query.split() if len(t) > 3]
        
        # Check if query contains explicit file path
        explicit_file = self._extract_file_path(query)
        if explicit_file and explicit_file.exists():
            logger.info(f"[ReaderAgent] Reading explicit file: {explicit_file}")
            content = self._read_file(explicit_file)
            if content:
                content.relevance_score = 1.0  # Explicit file = max relevance
                relevant_content.append(content)
        
        if not knowledge_dir.exists():
            return relevant_content
        
        # Walk through knowledge directory
        for filepath in knowledge_dir.rglob("*"):
            if filepath.is_file():
                content = self._read_file(filepath)
                if content:
                    # Calculate relevance
                    relevance = self._calculate_relevance(content.content, query_terms)
                    content.relevance_score = relevance
                    
                    # Include if relevant
                    if relevance > 0.1:
                        relevant_content.append(content)
        
        # Sort by relevance
        relevant_content.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return relevant_content[:10]  # Top 10 most relevant
    
    def _extract_file_path(self, query: str) -> Optional[Path]:
        """Extract explicit file path from query (handles spaces and Unicode)."""
        import re
        
        # Pattern: Capture from / to file extension, allowing spaces
        patterns = [
            r'(?:at\s+)?(/[^"\']+?\.(?:eml|png|jpg|jpeg|pdf|docx|txt|md|xlsx))\b',
            r'(?:file|screenshot|image|document|email)(?:\s+is)?\s+(?:at\s+)?([/~][^"\']+?\.(?:eml|png|jpg|jpeg|pdf|docx|txt|md|xlsx))\b',
            r'["\']([/~][^"\']+?\.(?:eml|png|jpg|jpeg|pdf|docx|txt|md|xlsx))["\']',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                filepath_str = match.group(1).strip()
                filepath = Path(filepath_str)
                
                # Direct match (exact path)
                if filepath.exists():
                    logger.info(f"[ReaderAgent] Found explicit file: {filepath}")
                    return filepath
                
                # Try with ~ expansion
                if filepath_str.startswith('~'):
                    filepath = Path(filepath_str).expanduser()
                    if filepath.exists():
                        logger.info(f"[ReaderAgent] Found explicit file (expanded ~): {filepath}")
                        return filepath
                
                # Handle Unicode/encoding issues (e.g., narrow no-break space)
                # Try fuzzy matching in the parent directory
                parent = filepath.parent
                if parent.exists():
                    target_name = filepath.name
                    logger.debug(f"[ReaderAgent] Trying fuzzy match for: {target_name}")
                    
                    for file in parent.iterdir():
                        # Normalize both names for comparison
                        import unicodedata
                        norm_file = unicodedata.normalize('NFKC', file.name)
                        norm_target = unicodedata.normalize('NFKC', target_name)
                        
                        if norm_file == norm_target or file.name == target_name:
                            logger.info(f"[ReaderAgent] Found explicit file (fuzzy match): {file}")
                            return file
        
        logger.debug(f"[ReaderAgent] No explicit file path found in query")
        return None
    
    def _read_file(self, filepath: Path) -> Optional[ExtractedContent]:
        """Read content from a file based on its type."""
        suffix = filepath.suffix.lower()
        
        try:
            if suffix in ['.txt', '.md']:
                return self._read_text(filepath)
            elif suffix == '.eml':
                return self._read_eml(filepath)
            elif suffix == '.docx':
                return self._read_docx(filepath)
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
    
    def _read_text(self, filepath: Path) -> ExtractedContent:
        """Read plain text file."""
        content = filepath.read_text(errors='ignore')[:10000]  # Limit size
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
    
    def _read_docx(self, filepath: Path) -> Optional[ExtractedContent]:
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
            
            content = ' '.join(text_parts)[:10000]
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
    
    def _read_pdf(self, filepath: Path) -> Optional[ExtractedContent]:
        """Read PDF - basic text extraction."""
        # Note: Full PDF extraction requires PyPDF2 or similar
        # This is a placeholder that returns filename as content
        return ExtractedContent(
            source_file=str(filepath.name),
            content_type="reference",
            content=f"[PDF Document: {filepath.name}]",
            metadata={"format": "pdf", "requires_ocr": True}
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
