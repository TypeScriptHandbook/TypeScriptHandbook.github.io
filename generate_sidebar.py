#!/usr/bin/env python3
"""
Generate _sidebar.md for Docsify from Markdown chapters.
Reads all .md files in ./Chapters directory and creates a sidebar
based on filename numbers and first # heading in each file.
"""

import os
import re
from pathlib import Path

def extract_title_from_markdown(filepath):
    """Extract the first # heading from a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    # Remove the # and any extra whitespace
                    return line[2:].strip()
        # If no # heading found, return filename without extension
        return filepath.stem
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")
        return filepath.stem

def extract_chapter_number(filename):
    """Extract chapter number from filename. Returns tuple (number, filename)."""
    # Look for number at the start of filename
    match = re.match(r'^(\d+)', filename)
    if match:
        return (int(match.group(1)), filename)
    else:
        # If no number found, put it at the end with a high number
        return (999, filename)

def generate_sidebar():
    """Generate _sidebar.md from chapters in ./Chapters directory."""

    chapters_dir = Path('./Chapters')
    docs_dir = Path('./docs')

    if not chapters_dir.exists():
        print(f"Error: {chapters_dir} directory not found!")
        return

    if not docs_dir.exists():
        print(f"Error: {docs_dir} directory not found!")
        return

    # Get all .md files in Chapters directory
    md_files = list(chapters_dir.glob('*.md'))

    if not md_files:
        print(f"No .md files found in {chapters_dir}")
        return

    print(f"Found {len(md_files)} markdown files in {chapters_dir}")

    # Sort files by chapter number extracted from filename
    sorted_files = sorted(md_files, key=lambda f: extract_chapter_number(f.name))

    # Generate sidebar content
    sidebar_lines = []

    for filepath in sorted_files:
        title = extract_title_from_markdown(filepath)
        # Use absolute GitHub path to the raw file
        relative_path = f"https://raw.githubusercontent.com/TypeScriptHandbook/TypeScriptHandbook.github.io/main/Chapters/{filepath.name}"

        # Format: * [Title](path)
        sidebar_line = f"* [{title}]({relative_path})"
        sidebar_lines.append(sidebar_line)

        print(f"  {filepath.name} -> {title}")

    # Write _sidebar.md
    sidebar_path = docs_dir / '_sidebar.md'

    try:
        with open(sidebar_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sidebar_lines) + '\n')

        print(f"\n✅ Generated {sidebar_path}")
        print(f"   Contains {len(sidebar_lines)} chapters")

    except Exception as e:
        print(f"❌ Error writing {sidebar_path}: {e}")

if __name__ == "__main__":
    generate_sidebar()