"""
Basic configuration constants for the semantic line breaks tool.
"""

# Line breaking thresholds
LONG_SENTENCE_THRESHOLD = 80  # Characters - sentences longer than this get line breaks
LONG_CLAUSE_THRESHOLD = 60   # Characters - clauses longer than this get comma breaks

# Conjunctions that trigger line breaks when they start the next sentence
TRANSITION_WORDS = [
    'however', 'therefore', 'furthermore', 'moreover',
    'nevertheless', 'consequently', 'meanwhile', 'otherwise',
    'additionally', 'similarly', 'conversely', 'nonetheless'
]
