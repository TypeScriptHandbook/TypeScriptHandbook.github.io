"""
DEPRECATED: This module is being replaced by the new functional approach.
Use markdown_processing.py instead.

For backward compatibility, this provides a wrapper around the new functions.
"""

from markdown_processing import process_markdown_content


class MarkdownProcessor:
    """
    DEPRECATED: Backward compatibility wrapper.
    Consider using process_markdown_content() function directly.
    """

    def __init__(self):
        import warnings
        warnings.warn(
            "MarkdownProcessor class is deprecated. Use process_markdown_content() function instead.",
            DeprecationWarning,
            stacklevel=2
        )

    def process_markdown(self, content: str) -> str:
        """Process markdown content, applying semantic line breaks to prose paragraphs."""
        return process_markdown_content(content)

    def is_prose_paragraph(self, text: str) -> bool:
        """Check if a block of text is a prose paragraph that should be processed."""
        from markdown_detection import is_prose_paragraph
        return is_prose_paragraph(text)
    
