"""
Functions for detecting and classifying markdown elements.
"""

import re
from markdown_patterns import MARKDOWN_PATTERNS

# Compile patterns once for efficiency
_compiled_patterns = {}


def _get_compiled_pattern(pattern_name: str):
    """Get a compiled regex pattern, compiling it if necessary."""
    if pattern_name not in _compiled_patterns:
        pattern = MARKDOWN_PATTERNS[pattern_name]

        # Handle special cases for flags
        if pattern_name == 'code_block':
            _compiled_patterns[pattern_name] = re.compile(pattern, re.MULTILINE | re.DOTALL)
        elif pattern_name in ['header', 'list', 'numbered_list', 'blockquote',
                              'table', 'horizontal_rule', 'link_ref']:
            _compiled_patterns[pattern_name] = re.compile(pattern, re.MULTILINE)
        else:
            _compiled_patterns[pattern_name] = re.compile(pattern)

    return _compiled_patterns[pattern_name]


def is_code_block(text: str) -> bool:
    """Check if text contains or is a code block."""
    return text.startswith('```') or _get_compiled_pattern('code_block').search(text) is not None


def is_header(text: str) -> bool:
    """Check if text is a markdown header."""
    return _get_compiled_pattern('header').match(text.strip()) is not None


def is_list_item(text: str) -> bool:
    """Check if text is a list item (bulleted or numbered)."""
    text = text.strip()
    return (_get_compiled_pattern('list').match(text) is not None or
            _get_compiled_pattern('numbered_list').match(text) is not None)


def is_blockquote(text: str) -> bool:
    """Check if text is a blockquote."""
    return _get_compiled_pattern('blockquote').match(text.strip()) is not None


def is_table_row(text: str) -> bool:
    """Check if text is a table row."""
    return _get_compiled_pattern('table').match(text.strip()) is not None


def is_horizontal_rule(text: str) -> bool:
    """Check if text is a horizontal rule."""
    return _get_compiled_pattern('horizontal_rule').match(text.strip()) is not None


def is_link_reference(text: str) -> bool:
    """Check if text is a link reference definition."""
    return _get_compiled_pattern('link_ref').match(text.strip()) is not None


def has_excessive_inline_code(text: str) -> bool:
    """Check if text has too much inline code to be considered prose."""
    inline_code_pattern = _get_compiled_pattern('inline_code')
    code_matches = inline_code_pattern.findall(text)
    return len(''.join(code_matches)) > len(text) // 10


def is_prose_paragraph(text: str) -> bool:
    """
    Check if a block of text is a prose paragraph that should be processed.

    Returns False for:
    - Empty text
    - Headers
    - List items
    - Blockquotes
    - Tables
    - Horizontal rules
    - Link references
    - Code blocks
    - Text with excessive inline code
    """
    text = text.strip()

    if not text:
        return False

    # Check each type of non-prose content
    if (
        is_header(text) or
        is_list_item(text) or
        is_blockquote(text) or
        is_table_row(text) or
        is_horizontal_rule(text) or
        is_link_reference(text) or
        is_code_block(text) or
        has_excessive_inline_code(text)
    ):
        return False

    # If none of the above, it's likely a prose paragraph
    return True
