"""
Configuration constants for the semantic line breaks tool.
"""

# Configuration constants
LONG_SENTENCE_THRESHOLD = 80  # Characters - sentences longer than this get line breaks
LONG_CLAUSE_THRESHOLD = 60  # Characters - clauses longer than this get comma breaks

# Conjunctions that trigger line breaks when they start the next sentence
TRANSITION_WORDS = [
    'however', 'therefore', 'furthermore', 'moreover',
    'nevertheless', 'consequently', 'meanwhile', 'otherwise',
    'additionally', 'similarly', 'conversely', 'nonetheless'
]

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
    # Series (a, b, c pattern)
    r'\w+,\s*\w+,\s*(?:and|or)\s+\w+',
    # Dates
    r'[A-Za-z]+\s+\d+,\s+\d{4}',
    # Addresses
    r'\d+\s+[A-Za-z\s]+,\s+[A-Za-z\s]+,\s+[A-Z]{2}',
]

# Abbreviations to protect from sentence splitting
ABBREVIATION_PATTERNS = [
    (r'\betc\.', 'ETCPERIOD'),
    (r'\be\.g\.', 'EGPERIOD'),
    (r'\bi\.e\.', 'IEPERIOD'),
    (r'\bvs\.', 'VSPERIOD'),
    (r'\bMr\.', 'MRPERIOD'),
    (r'\bMrs\.', 'MRSPERIOD'),
    (r'\bMs\.', 'MSPERIOD'),
    (r'\bDr\.', 'DRPERIOD'),
    (r'\bProf\.', 'PROFPERIOD'),
    (r'\bInc\.', 'INCPERIOD'),
    (r'\bLtd\.', 'LTDPERIOD'),
    (r'\bCorp\.', 'CORPPERIOD'),
    (r'\bCo\.', 'COPERIOD'),
    (r'\bSt\.', 'STPERIOD'),  # Street or Saint
    (r'\bAve\.', 'AVEPERIOD'),
    (r'\bBlvd\.', 'BLVDPERIOD'),
    (r'\bapprox\.', 'APPROXPERIOD'),
    (r'\bmax\.', 'MAXPERIOD'),
    (r'\bmin\.', 'MINPERIOD'),
    (r'\bNo\.', 'NOPERIOD'),  # Number
    (r'\bvol\.', 'VOLPERIOD'),  # Volume
    (r'\bp\.', 'PPERIOD'),  # Page
    (r'\bpp\.', 'PPPERIOD'),  # Pages
]

# Markdown formatting patterns to protect from sentence splitting
# These use lambda functions to preserve the structure while replacing periods
MARKDOWN_PROTECTION_PATTERNS = [
    # Bold text with periods: **text with period.**
    (r'\*\*([^*]+\.+[^*]*)\*\*', lambda m: f"**{m.group(1).replace('.', 'MDPERIOD')}**"),
    # Italic text with periods: *text with period.*
    (r'\*([^*]+\.+[^*]*)\*', lambda m: f"*{m.group(1).replace('.', 'MDPERIOD')}*"),
    # Code spans with periods: `code.method()`
    (r'`([^`]+\.+[^`]*)`', lambda m: f"`{m.group(1).replace('.', 'MDPERIOD')}`"),
    # Links with periods in text: [text with period.](url)
    (r'\[([^\]]+\.+[^\]]*)\]\([^)]+\)',
     lambda m: f"[{m.group(1).replace('.', 'MDPERIOD')}]({m.group(0).split('](')[1]}"),
    # Image alt text with periods: ![alt text with period.](url)
    (r'!\[([^\]]+\.+[^\]]*)\]\([^)]+\)',
     lambda m: f"![{m.group(1).replace('.', 'MDPERIOD')}]({m.group(0).split('](')[1]}"),
]

# Markdown element detection patterns
MARKDOWN_PATTERNS = {
    'code_block': r'^```.*?^```',
    'inline_code': r'`[^`]+`',
    'header': r'^#{1,6}\s+.*',
    'list': r'^\s*[-*+]\s+.*',
    'numbered_list': r'^\s*\d+\.\s+.*',
    'blockquote': r'^>\s*.*',
    'table': r'^\|.*\|',
    'horizontal_rule': r'^[-*_]{3,}',
    'link_ref': r'^\[.*]:\s*.*',
}

# Regex flags for markdown patterns
MARKDOWN_PATTERN_FLAGS = {
    'code_block': {'flags': 'MULTILINE | DOTALL'},
    'inline_code': {'flags': None},
    'header': {'flags': 'MULTILINE'},
    'list': {'flags': 'MULTILINE'},
    'numbered_list': {'flags': 'MULTILINE'},
    'blockquote': {'flags': 'MULTILINE'},
    'table': {'flags': 'MULTILINE'},
    'horizontal_rule': {'flags': 'MULTILINE'},
    'link_ref': {'flags': 'MULTILINE'},
}
