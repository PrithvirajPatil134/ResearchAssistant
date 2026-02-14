#!/usr/bin/env python3
"""Test file path extraction with spaces and Unicode in filename."""

import sys
sys.path.insert(0, 'src')

from pathlib import Path
from research_assistant.core import Memory, ContextGuardAgent
from research_assistant.agents import ReaderAgent

query = """Generate an appropriate response for Prof. Cardasso's email. The screenshot of the email is at /Users/propatil/workplace/ResearchAssistant/src/research_assistant/spaces/DBA/communication/ProfCardasso_email_2026-02-05 at 4.21.20 PM.png"""

print('=' * 70)
print('Testing ReaderAgent File Path Extraction with Unicode Spaces')
print('=' * 70)
print(f'Query: {query[:80]}...\n')

# Initialize ReaderAgent
memory = Memory()
context_guard = ContextGuardAgent(max_tokens=100000)
reader = ReaderAgent(memory, context_guard)

# Test _extract_file_path method
extracted_file = reader._extract_file_path(query)

print('Results:')
if extracted_file:
    print(f'✅ File extracted: {extracted_file}')
    print(f'   Filename: {extracted_file.name}')
    print(f'   Exists: {extracted_file.exists()}')
    print(f'   Size: {extracted_file.stat().st_size if extracted_file.exists() else 0} bytes')
else:
    print('❌ No file extracted')

print()
expected = '/Users/propatil/workplace/ResearchAssistant/src/research_assistant/spaces/DBA/communication/ProfCardasso_email_2026-02-05 at 4.21.20 PM.png'
print(f'Expected path: {expected}')
print(f'Note: Actual filename has Unicode \\u202f (narrow no-break space) before PM')
