"""
Functions for reassembling previously line-broken sentences.
"""

import re


def line_ends_sentence(line: str) -> bool:
    """Check if a line ends a complete sentence."""
    line = line.strip()
    if not line:
        return False

    # Remove any trailing whitespace and check last character
    last_char = line[-1]

    # Definitely continues if ends with comma, colon, semicolon
    if last_char in ',;:':
        return False

    # Ends with sentence-ending punctuation
    if last_char in '.!?':
        # But check if it's likely an abbreviation
        words = line.split()
        if words:
            last_word = words[-1].lower()
            # Common abbreviations that might appear at line end
            common_abbrevs = {
                'etc.', 'e.g.', 'i.e.', 'vs.', 'mr.', 'mrs.', 'ms.', 'dr.', 'prof.',
                'inc.', 'ltd.', 'corp.', 'co.', 'st.', 'ave.', 'blvd.',
                'approx.', 'max.', 'min.', 'no.', 'vol.', 'p.', 'pp.'
            }
            if last_word in common_abbrevs:
                return False
        return True

    # Check if ends with continuation words
    words = line.split()
    if not words:
        return True  # Empty line, treat as sentence end

    last_word = words[-1].lower().rstrip('.,!?;:')  # Remove punctuation for comparison

    # Words that typically indicate continuation
    continuation_words = {
        # Coordinating conjunctions
        'and', 'or', 'but', 'yet', 'so', 'for', 'nor',
        # Subordinating conjunctions
        'because', 'since', 'when', 'where', 'while', 'although', 'though',
        'unless', 'until', 'if', 'whereas', 'whenever', 'wherever',
        # Relative pronouns
        'that', 'which', 'who', 'whom', 'whose',
        # Other continuation indicators
        'with', 'without', 'through', 'during', 'before', 'after'
    }

    if last_word in continuation_words:
        return False

    # Default: assume it's a sentence ending
    return True


def reassemble_broken_sentences(text: str) -> str:
    """
    Reassemble sentences that were previously broken across multiple lines
    back into single lines before applying new semantic breaks.
    """
    if not text.strip():
        return text

    # Split by paragraphs first (double newlines)
    paragraphs = re.split(r'\n\s*\n', text)
    reassembled_paragraphs = []

    for paragraph in paragraphs:
        if not paragraph.strip():
            reassembled_paragraphs.append('')
            continue

        lines = paragraph.split('\n')
        reassembled_lines = []
        current_sentence = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Add line to current sentence
            current_sentence.append(line)

            # Check if this line ends a sentence
            if line_ends_sentence(line):
                reassembled_lines.append(' '.join(current_sentence))
                current_sentence = []

        # Handle any remaining sentence
        if current_sentence:
            reassembled_lines.append(' '.join(current_sentence))

        # Join sentences in this paragraph with newlines
        reassembled_paragraphs.append('\n'.join(reassembled_lines))

    return '\n\n'.join(reassembled_paragraphs)
