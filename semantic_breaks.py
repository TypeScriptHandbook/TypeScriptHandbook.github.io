#!/usr/bin/env python3
"""
Semantic Line Breaks Tool for Markdown Files

This tool applies semantic line breaks to prose paragraphs in Markdown files
while preserving code blocks, headers, lists, and other structural elements.

Dependencies:
    pip install nltk

Usage:
    python semantic_breaks.py input.md [output.md]
"""

import argparse
from pathlib import Path

from semantic_breaks import MarkdownProcessor


def main():
    parser = argparse.ArgumentParser(
        description="Apply semantic line breaks to Markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python semantic_breaks.py document.md
    python semantic_breaks.py input.md output.md
    python semantic_breaks.py *.md
        """
    )

    parser.add_argument('input_files', nargs='+', help='Input Markdown file(s)')
    parser.add_argument('-o', '--output', help='Output file (for single input file)')
    parser.add_argument('--in-place', '-i', action='store_true',
                        help='Modify files in place')
    parser.add_argument('--suffix', default='_semantic',
                        help='Suffix for output files (default: _semantic)')

    args = parser.parse_args()

    processor = MarkdownProcessor()

    for input_file in args.input_files:
        input_path = Path(input_file)

        if not input_path.exists():
            print(f"Error: File '{input_file}' not found")
            continue

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
            elif args.output and len(args.input_files) == 1:
                output_path = Path(args.output)
            else:
                output_path = input_path.with_stem(f"{input_path.stem}{args.suffix}")

            # Write output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)

            print(f"✓ Wrote {output_path}")

        except Exception as e:
            print(f"Error processing {input_file}: {e}")


if __name__ == "__main__":
    main()
