#!/usr/bin/env python3
"""
Semantic Line Breaks Tool for Markdown Files

This tool applies semantic line breaks to prose paragraphs in Markdown files
while preserving code blocks, headers, lists, and other structural elements.

Dependencies:
    pip install nltk

Usage:
    python semantic_breaks.py input.md [output.md]
    python semantic_breaks.py -i ./docs/Chapters/*.md
    python semantic_breaks.py *.md
"""

import argparse
from pathlib import Path

from markdown_processor import MarkdownProcessor


def expand_wildcards(file_patterns):
    """Expand wildcard patterns to actual file paths using pathlib."""
    expanded_files = []
    for pattern in file_patterns:
        # Check if pattern contains wildcards
        if '*' in pattern or '?' in pattern:
            pattern_path = Path(pattern)

            # For patterns like './docs/*.md' or 'docs\*.md'
            if pattern_path.parent.exists():
                matches = list(pattern_path.parent.glob(pattern_path.name))
                if matches:
                    expanded_files.extend(str(p) for p in matches)
                    continue

            # For more complex patterns, try using Path.cwd().glob()
            try:
                matches = list(Path.cwd().glob(pattern))
                if matches:
                    expanded_files.extend(str(p) for p in matches)
                    continue
            except (OSError, ValueError):
                pass

            # If no matches found, treat as literal
            expanded_files.append(pattern)
        else:
            # No wildcards, treat as literal filename
            expanded_files.append(pattern)

    return expanded_files


def main():
    parser = argparse.ArgumentParser(
        description="Apply semantic line breaks to Markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python semantic_breaks.py document.md
    python semantic_breaks.py input.md output.md
    python semantic_breaks.py *.md
    python semantic_breaks.py -i docs/Chapters/*.md
    python semantic_breaks.py --in-place **/*.md
        """
    )

    parser.add_argument('input_files', nargs='+', help='Input Markdown file(s) (supports wildcards)')
    parser.add_argument('-o', '--output', help='Output file (for single input file)')
    parser.add_argument('--in-place', '-i', action='store_true',
                        help='Modify files in place')
    parser.add_argument('--suffix', default='_semantic',
                        help='Suffix for output files (default: _semantic)')

    args = parser.parse_args()

    # Expand wildcards in input files
    expanded_files = expand_wildcards(args.input_files)

    # Filter to only existing files and warn about missing ones
    existing_files = []
    for file_path in expanded_files:
        path = Path(file_path)
        if path.exists():
            existing_files.append(file_path)
        else:
            print(f"Warning: File '{file_path}' not found, skipping...")

    if not existing_files:
        print("Error: No valid input files found")
        return 1

    processor = MarkdownProcessor()

    processed_count = 0
    error_count = 0

    for input_file in existing_files:
        input_path = Path(input_file)

        print(f"Processing {input_file}...")

        try:
            # Read input file
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Process content
            processed_content = processor.process_markdown(content)

            # Determine output file
            if args.in_place:
                output_path = input_path
            elif args.output and len(existing_files) == 1:
                output_path = Path(args.output)
            else:
                output_path = input_path.with_stem(f"{input_path.stem}{args.suffix}")

            # Write output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)

            print(f"✓ Wrote {output_path}")
            processed_count += 1

        except Exception as e:
            print(f"Error processing {input_file}: {e}")
            error_count += 1

    # Summary
    print(f"\nProcessed {processed_count} files successfully")
    if error_count > 0:
        print(f"Failed to process {error_count} files")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
