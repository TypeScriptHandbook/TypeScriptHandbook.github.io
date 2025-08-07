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

# spaCy-specific settings
SPACY_MODEL = "en_core_web_sm"  # Default spaCy model to use
SPACY_COMPLEXITY_THRESHOLD = 5.0  # Complexity score above which to break sentences
SPACY_MIN_CLAUSE_WORDS = 3  # Minimum words after comma to justify breaking

# Named entity types that should be protected from sentence splitting
PROTECTED_ENTITY_TYPES = [
    "PERSON", "ORG", "GPE", "DATE", "TIME", 
    "MONEY", "PERCENT", "CARDINAL", "ORDINAL"
]

# Dependency labels that indicate clause boundaries
CLAUSE_BOUNDARY_DEPS = [
    "mark",     # subordinating conjunctions
    "cc",       # coordinating conjunctions
    "relcl",    # relative clauses
    "advcl",    # adverbial clauses
    "acl"       # clausal modifiers
]
