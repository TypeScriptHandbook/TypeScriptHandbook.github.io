"""
Markdown element detection patterns.
"""

# Markdown element detection patterns
MARKDOWN_PATTERNS = {
    'code_block': r'^```.*?^```',
    'inline_code': r'`[^`]+`',
    'header': r'^#{1,6}\s+.*$',
    'list': r'^\s*[-*+]\s+.*$',
    'numbered_list': r'^\s*\d+\.\s+.*$',
    'blockquote': r'^>\s*.*$',
    'table': r'^\|.*\|$',
    'horizontal_rule': r'^[-*_]{3,}$',
    'link_ref': r'^\[.*]:\s*.*$',
}
