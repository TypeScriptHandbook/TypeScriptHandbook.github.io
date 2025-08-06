"""
Patterns for protecting abbreviations and markdown from sentence splitting.
"""

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
