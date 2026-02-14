#!/usr/bin/env python3
"""Test image reading with vision directly."""

import sys
sys.path.insert(0, 'src')

from pathlib import Path
from research_assistant.core import Memory, ContextGuardAgent
from research_assistant.agents import ReaderAgent

image_path = Path('/Users/propatil/workplace/ResearchAssistant/src/research_assistant/spaces/DBA/communication/ProfCardasso_email_2026-02-05 at 4.21.20\u202fPM.png')

print('=' * 70)
print('Testing Direct Image Reading with Vision')
print('=' * 70)
print(f'Image path: {image_path}')
print(f'File exists: {image_path.exists()}')
print(f'File size: {image_path.stat().st_size if image_path.exists() else 0} bytes')
print()

if not image_path.exists():
    print('❌ File not found! Cannot proceed.')
    sys.exit(1)

# Initialize ReaderAgent
memory = Memory()
context_guard = ContextGuardAgent(max_tokens=100000)
reader = ReaderAgent(memory, context_guard)

print('Calling _read_image() method...')
print('This will take 20-30 seconds for vision extraction...\n')

# Call _read_image directly
result = reader._read_image(image_path)

print('-' * 70)
if result:
    print(f'✅ SUCCESS!')
    print(f'Content type: {result.content_type}')
    print(f'Content length: {len(result.content)} chars')
    print(f'\nFirst 500 chars of extracted text:')
    print('-' * 70)
    print(result.content[:500])
    print('-' * 70)
else:
    print('❌ FAILED - No content extracted')
