"""
TypeScript and JavaScript code extraction from markdown files
"""

import re
from pathlib import Path

from models import CodeExample, TestConfig, CodeType


class CodeExtractor:
    """Handles extraction of TypeScript and JavaScript code from markdown files"""

    def __init__(self, config: TestConfig) -> None:
        self.config = config

    def extract_code_blocks_content(self, content: str) -> list[tuple[str, CodeType]]:
        """Extract TypeScript and JavaScript code blocks from markdown content, preserving order"""
        # Pattern to match both ts and js code blocks with their positions
        pattern = r'```(ts|js)\n(.*?)\n```'

        matches = []
        for match in re.finditer(pattern, content, re.DOTALL):
            lang = match.group(1)
            code = match.group(2).strip()

            if code:  # Only include non-empty code blocks
                code_type = CodeType.TYPESCRIPT if lang == 'ts' else CodeType.JAVASCRIPT
                matches.append((code, code_type))

        return matches

    def extract_code_blocks(self, markdown_file: Path) -> list[CodeExample]:
        """Extract TypeScript and JavaScript code blocks from a markdown file"""
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            print(f"⚠️  Warning: Could not read {markdown_file}: {e}")
            return []

        code_blocks = self.extract_code_blocks_content(content)
        chapter_name = markdown_file.stem
        examples = []

        for i, (code, code_type) in enumerate(code_blocks, 1):
            examples.append(CodeExample(
                chapter=chapter_name,
                number=i,
                code=code,
                code_type=code_type,
                source_file=str(markdown_file)
            ))

        return examples

    def find_markdown_files(self) -> list[Path]:
        """Find markdown files, optionally filtered by chapter numbers"""
        try:
            all_files = list(self.config.book_dir.glob("*.md"))
        except OSError as e:
            print(f"❌ Error accessing directory {self.config.book_dir}: {e}")
            return []

        if not self.config.specific_chapters:
            return all_files

        filtered_files = []
        for chapter_num in self.config.specific_chapters:
            chapter_files = [
                f for f in all_files
                if f.stem == f"{chapter_num:02d}" or f.stem == str(chapter_num)
            ]
            filtered_files.extend(chapter_files)

        return filtered_files

    def extract_all_examples(self) -> list[CodeExample]:
        """Extract all code examples from markdown files"""
        examples = []
        markdown_files = self.find_markdown_files()

        if not markdown_files:
            print("⚠️  No markdown files found")
            return []

        for md_file in markdown_files:
            file_examples = self.extract_code_blocks(md_file)
            examples.extend(file_examples)

        return examples
