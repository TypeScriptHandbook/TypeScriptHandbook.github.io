"""
Semantic Line Breaks Tool for Markdown Files

This package applies semantic line breaks to prose paragraphs in Markdown files
while preserving code blocks, headers, lists, and other structural elements.
"""

from .line_breaker import SemanticLineBreaker
from .markdown_processor import MarkdownProcessor
from .config import LONG_SENTENCE_THRESHOLD

__version__ = "1.0.0"
__all__ = ["SemanticLineBreaker", "MarkdownProcessor", "LONG_SENTENCE_THRESHOLD"]
