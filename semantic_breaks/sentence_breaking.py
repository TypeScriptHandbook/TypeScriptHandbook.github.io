"""
Functions for sentence-level semantic line breaking.
"""

import re
from typing import Optional

import nltk
from nltk.tokenize import sent_tokenize

from config import LONG_SENTENCE_THRESHOLD, TRANSITION_WORDS
from text_protection_patterns import ABBREVIATION_PATTERNS, MARKDOWN_PROTECTION_PATTERNS

try:
    from spacy_integration import find_sentence_boundaries_spacy, protect_entities_spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False


def ensure_nltk_data():
    """Ensure required NLTK data is available."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt', quiet=True)

    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        try:
            nltk.download('punkt_tab', quiet=True)
        except (OSError, ValueError, ConnectionError, TimeoutError):
            pass  # punkt_tab might not be available in older NLTK versions or network issues


def should_break_after_sentence(sent: str, next_sent: Optional[str] = None) -> bool:
    """Determine if we should add a line break after this sentence."""
    sent = sent.strip()

    # Always break after sentences that end with periods, exclamation, or question marks
    if sent.endswith(('.', '!', '?')):
        return True

    # Break after sentences with certain conjunctions at the start of next sentence
    if next_sent:
        next_start = next_sent.strip().lower()
        if any(next_start.startswith(word) for word in TRANSITION_WORDS):
            return True

    # Break after long sentences
    if len(sent) > LONG_SENTENCE_THRESHOLD:
        return True

    return False


def protect_text_elements(text: str):
    """Protect abbreviations and markdown from sentence tokenization."""
    protected_text = text
    replacements = []

    # Use spaCy NER protection if available (more accurate)
    if SPACY_AVAILABLE:
        try:
            protected_spans = protect_entities_spacy(text)
            # Convert protected spans to replacement tokens
            offset = 0
            for start, end, entity_text in sorted(protected_spans):
                # Adjust positions based on previous replacements
                adjusted_start = start + offset
                adjusted_end = end + offset
                
                # Create a unique token for this entity
                protected_token = f"ENTITY{len(replacements)}"
                replacements.append((protected_token, entity_text))
                
                # Replace the entity text with the token
                protected_text = (protected_text[:adjusted_start] + 
                                protected_token + 
                                protected_text[adjusted_end:])
                
                # Update offset for next replacement
                offset += len(protected_token) - (end - start)
        except Exception:
            pass  # Fall back to regex-based protection

    # Apply abbreviation protections
    for pattern, replacement in ABBREVIATION_PATTERNS:
        matches = list(re.finditer(pattern, protected_text))
        for match in reversed(matches):  # Process in reverse to maintain indices
            original = match.group()
            replacements.append((replacement, original))
            protected_text = protected_text[:match.start()] + replacement + protected_text[match.end():]

    # Apply markdown protections
    for pattern, replacement_func in MARKDOWN_PROTECTION_PATTERNS:
        def replace_match(match):
            result = replacement_func(match)
            # Track what we replaced
            original_periods = match.group().count('.')
            for _ in range(original_periods):
                replacements.append(('MDPERIOD', '.'))
            return result

        protected_text = re.sub(pattern, replace_match, protected_text)

    return protected_text, replacements


def restore_text_elements(sentences, replacements):
    """Restore original text after sentence tokenization."""
    for i, sentence in enumerate(sentences):
        for replacement, original in replacements:
            sentence = sentence.replace(replacement, original)
        sentences[i] = sentence
    return sentences


def split_into_sentences(text: str):
    """Split text into sentences using spaCy (preferred) or NLTK, protecting abbreviations and markdown."""
    # Try spaCy first if available
    if SPACY_AVAILABLE:
        try:
            return find_sentence_boundaries_spacy(text)
        except Exception:
            pass  # Fall back to NLTK
    
    # NLTK fallback
    ensure_nltk_data()

    protected_text, replacements = protect_text_elements(text)
    sentences = sent_tokenize(protected_text)
    sentences = restore_text_elements(sentences, replacements)

    return sentences
