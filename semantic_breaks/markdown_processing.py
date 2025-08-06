"""
Functions for processing markdown content with semantic line breaks.
"""

import re
from semantic_breaks import apply_semantic_breaks
from markdown_detection import is_prose_paragraph


def protect_code_blocks(content: str):
    """
    Protect code blocks by replacing them with placeholders.
    Returns (protected_content, code_blocks_list).
    """
    code_blocks = []

    def replace_code_block(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks) - 1}__"

    # Use the same pattern as in config, but compile it here
    code_block_pattern = re.compile(r'^```.*?^```', re.MULTILINE | re.DOTALL)
    protected_content = code_block_pattern.sub(replace_code_block, content)

    return protected_content, code_blocks


def restore_code_blocks(content: str, code_blocks: list) -> str:
    """Restore code blocks from placeholders."""
    result = content
    for i, code_block in enumerate(code_blocks):
        result = result.replace(f"__CODE_BLOCK_{i}__", code_block)
    return result


def split_into_paragraphs(content: str) -> list:
    """Split content into paragraphs separated by blank lines."""
    return re.split(r'\n\s*\n', content)


def process_paragraph(paragraph: str) -> str:
    """Process a single paragraph, applying semantic breaks if it's prose."""
    if is_prose_paragraph(paragraph):
        return apply_semantic_breaks(paragraph)
    else:
        return paragraph


def process_markdown_content(content: str) -> str:
    """
    Process markdown content, applying semantic line breaks to prose paragraphs.

    This is the main entry point for markdown processing.
    """
    # Protect code blocks from processing
    protected_content, code_blocks = protect_code_blocks(content)

    # Split into paragraphs and process each one
    paragraphs = split_into_paragraphs(protected_content)
    processed_paragraphs = [process_paragraph(p) for p in paragraphs]

    # Rejoin paragraphs
    result = '\n\n'.join(processed_paragraphs)

    # Restore code blocks
    result = restore_code_blocks(result, code_blocks)

    return result
