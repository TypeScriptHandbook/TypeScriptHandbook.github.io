"""
Configuration constants for the semantic line breaks tool.
"""

# Configuration constants
LONG_SENTENCE_THRESHOLD = 80  # Characters - sentences longer than this get line breaks

# Conjunctions that trigger line breaks when they start the next sentence
TRANSITION_WORDS = [
    'however', 'therefore', 'furthermore', 'moreover',
    'nevertheless', 'consequently', 'meanwhile', 'otherwise',
    'additionally', 'similarly', 'conversely', 'nonetheless'
]
