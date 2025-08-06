"""
Functions for breaking sentences at commas and other punctuation.
"""

import re
from typing import List

from config import LONG_SENTENCE_THRESHOLD, LONG_CLAUSE_THRESHOLD
from comma_patterns import COMMA_BREAK_PATTERNS, COMMA_NO_BREAK_PATTERNS


# Compile patterns once for efficiency
_comma_break_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in COMMA_BREAK_PATTERNS]
_comma_no_break_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in COMMA_NO_BREAK_PATTERNS]


def should_break_at_comma(text: str, comma_pos: int) -> bool:
    """Determine if we should break at a specific comma position."""
    # Check if this comma is in a context where we shouldn't break
    for pattern in _comma_no_break_patterns:
        # Look for pattern around the comma position (wider context for series)
        start = max(0, comma_pos - 50)
        end = min(len(text), comma_pos + 50)
        context = text[start:end]

        if pattern.search(context):
            return False

    # Check if this comma is in a context where we should break
    for pattern in _comma_break_patterns:
        # Look for pattern starting from the comma
        end = min(len(text), comma_pos + 50)
        context = text[comma_pos:end]

        if pattern.match(context):
            return True

    # Fallback: break at comma if the clause before it is long enough
    # Find the start of the current clause (previous line break or sentence start)
    clause_start = 0
    for i in range(comma_pos - 1, -1, -1):
        if text[i] == '\n':
            clause_start = i + 1
            break

    clause_length = comma_pos - clause_start

    # Also check if there's significant content after the comma
    # Look ahead to see if there's enough text to justify breaking
    remaining_text = text[comma_pos + 1:].strip()
    words_after = len(remaining_text.split())

    # Break if:
    # 1. The clause before comma is long enough, AND
    # 2. There are enough words after the comma to justify the break
    return (clause_length > LONG_CLAUSE_THRESHOLD and
            words_after >= 3)


def find_comma_break_positions(sentence: str) -> List[int]:
    """Find all comma positions where we should break."""
    # Find all comma positions
    comma_positions = [i for i, char in enumerate(sentence) if char == ',']

    if not comma_positions:
        return []

    # Determine which commas to break at
    break_positions = []
    for pos in comma_positions:
        if should_break_at_comma(sentence, pos):
            break_positions.append(pos + 1)  # Break after the comma

    return break_positions


def break_sentence_at_commas(sentence: str) -> str:
    """Break a long sentence at appropriate commas."""
    if len(sentence) <= LONG_SENTENCE_THRESHOLD:
        return sentence

    break_positions = find_comma_break_positions(sentence)

    if not break_positions:
        return sentence

    # Split the sentence at the break positions
    parts = []
    last_pos = 0

    for break_pos in break_positions:
        part = sentence[last_pos:break_pos].strip()
        if part:
            parts.append(part)
        last_pos = break_pos

    # Add the remaining part
    remaining = sentence[last_pos:].strip()
    if remaining:
        parts.append(remaining)

    # Join with line breaks, ensuring proper spacing
    result = []
    for i, part in enumerate(parts):
        result.append(part)
        if i < len(parts) - 1:  # Not the last part
            result.append('\n')

    return ''.join(result)
