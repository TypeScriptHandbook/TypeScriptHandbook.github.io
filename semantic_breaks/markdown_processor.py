"""
Markdown processing logic for identifying and handling different markdown elements.
"""

import re
from .line_breaker import SemanticLineBreaker


class MarkdownProcessor:
    def __init__(self):
        self.line_breaker = SemanticLineBreaker()

        # Patterns for detecting markdown elements that should not be processed
        self.code_block_pattern = re.compile(r'^```.*?^```', re.MULTILINE | re.DOTALL)
        self.inline_code_pattern = re.compile(r'`[^`]+`')
        self.header_pattern = re.compile(r'^#{1,6}\s+.*$', re.MULTILINE)
        self.list_pattern = re.compile(r'^\s*[-*+]\s+.*$', re.MULTILINE)
        self.numbered_list_pattern = re.compile(r'^\s*\d+\.\s+.*$', re.MULTILINE)
        self.blockquote_pattern = re.compile(r'^>\s*.*$', re.MULTILINE)
        self.table_pattern = re.compile(r'^\|.*\|$', re.MULTILINE)
        self.horizontal_rule_pattern = re.compile(r'^[-*_]{3,}$', re.MULTILINE)
        self.link_ref_pattern = re.compile(r'^\[.*]:\s*.*$', re.MULTILINE)

    def is_prose_paragraph(self, text: str) -> bool:
        """Check if a block of text is a prose paragraph that should be processed."""
        text = text.strip()

        if not text:
            return False

        # Skip if it matches any non-prose patterns
        patterns_to_skip = [
            self.header_pattern,
            self.list_pattern,
            self.numbered_list_pattern,
            self.blockquote_pattern,
            self.table_pattern,
            self.horizontal_rule_pattern,
            self.link_ref_pattern
        ]

        for pattern in patterns_to_skip:
            if pattern.match(text):
                return False

        # Skip if it's primarily code
        if text.startswith('```') or text.count('`') > len(text) // 10:
            return False

        # It's likely a prose paragraph
        return True

    def process_markdown(self, content: str) -> str:
        """Process markdown content, applying semantic line breaks to prose paragraphs."""
        # First, protect code blocks by replacing them with placeholders
        code_blocks = []

        def replace_code_block(match):
            code_blocks.append(match.group(0))
            return f"__CODE_BLOCK_{len(code_blocks) - 1}__"

        content = self.code_block_pattern.sub(replace_code_block, content)

        # Split content into paragraphs (separated by blank lines)
        paragraphs = re.split(r'\n\s*\n', content)
        processed_paragraphs = []

        for paragraph in paragraphs:
            if self.is_prose_paragraph(paragraph):
                # Apply semantic line breaks to prose paragraphs
                processed = self.line_breaker.apply_semantic_breaks(paragraph)
                processed_paragraphs.append(processed)
            else:
                # Keep non-prose paragraphs unchanged
                processed_paragraphs.append(paragraph)

        # Rejoin paragraphs with double newlines
        result = '\n\n'.join(processed_paragraphs)

        # Restore code blocks
        for i, code_block in enumerate(code_blocks):
            result = result.replace(f"__CODE_BLOCK_{i}__", code_block)

        return result
