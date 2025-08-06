"""
Comma breaking patterns for semantic line breaks.
"""

# Comma break patterns - break after these comma contexts
COMMA_BREAK_PATTERNS = [
    # Coordinating conjunctions after comma
    r',\s+(and|but|or|nor|for|yet|so)\s+',

    # Subordinating conjunctions after comma
    r',\s+(when|where|while|since|because|although|though|unless|until|if|even\s+if|as\s+if|whereas)\s+',

    # Transitional phrases after comma
    r',\s+(however|therefore|furthermore|moreover|nevertheless|consequently|meanwhile|otherwise|additionally|similarly|conversely|nonetheless|for\s+example|in\s+addition|on\s+the\s+other\s+hand|namely|specifically|particularly|especially|including|such\s+as)\s+',

    # Relative pronouns after comma
    r',\s+(which|who|whom|whose|that)\s+',

    # Participial phrases (common patterns)
    r',\s+\w+ing\s+',
    r',\s+\w+ed\s+',

    # Appositives and explanatory phrases
    r',\s+(i\.?e\.?|e\.?g\.?|viz\.?|etc\.?)\s+',
]

# Don't break after commas in these contexts
COMMA_NO_BREAK_PATTERNS = [
    # Numbers with commas
    r'\d+,\d+',

    # Series/lists - matches items in a series but stops at major clause boundaries
    # Matches: "A, B, C, and D" but tries to avoid extending too far
    r'(?:^|[^.!?]\s+)[A-Za-z0-9#+.-]+(?:,\s*[A-Za-z0-9#+.-]+){1,},\s*(?:and|or)\s+[A-Za-z0-9#+.-]+(?=\s*[,.!?]|$)',

    # Dates
    r'[A-Za-z]+\s+\d+,\s+\d{4}',

    # Addresses
    r'\d+\s+[A-Za-z\s]+,\s+[A-Za-z\s]+,\s+[A-Z]{2}',

    # Name lists with titles (Mr. Smith, Dr. Jones, etc.)
    r'(?:Mr|Mrs|Ms|Dr|Prof)\.?\s+\w+(?:,\s*(?:Mr|Mrs|Ms|Dr|Prof)\.?\s+\w+)*',
]
