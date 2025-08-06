"""
DEPRECATED: This module is being replaced by the new functional approach.
Use semantic_breaks.py instead.

For backward compatibility, this provides a wrapper around the new functions.
"""

from semantic_breaks import apply_semantic_breaks


class SemanticLineBreaker:
    """
    DEPRECATED: Backward compatibility wrapper.
    Consider using apply_semantic_breaks() function directly.
    """

    def __init__(self):
        import warnings
        warnings.warn(
            "SemanticLineBreaker class is deprecated. Use apply_semantic_breaks() function instead.",
            DeprecationWarning,
            stacklevel=2
        )

    def apply_semantic_breaks(self, text: str) -> str:
        """Apply semantic line breaks to a paragraph of text."""
        return apply_semantic_breaks(text)
