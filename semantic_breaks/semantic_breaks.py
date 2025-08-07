"""
Main semantic line breaking functionality.
"""

from sentence_reassembly import reassemble_broken_sentences
from sentence_breaking import split_into_sentences, should_break_after_sentence
from comma_breaking import break_sentence_at_commas

try:
    from spacy_integration import (
        find_sentence_boundaries_spacy,
        should_break_after_sentence_spacy
    )
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False


def apply_semantic_breaks(text: str) -> str:
    """Apply semantic line breaks to a paragraph of text."""
    if not text.strip():
        return text

    # First, reassemble any previously broken sentences
    reassembled_text = reassemble_broken_sentences(text)

    # Split into sentences using spaCy (preferred) or NLTK fallback
    if SPACY_AVAILABLE:
        try:
            sentences = find_sentence_boundaries_spacy(reassembled_text)
        except Exception:
            # Fallback to NLTK if spaCy fails
            sentences = split_into_sentences(reassembled_text)
    else:
        sentences = split_into_sentences(reassembled_text)

    if len(sentences) <= 1:
        # Even if it's a single sentence, we might want to break it at commas
        single_sentence = sentences[0] if sentences else reassembled_text
        processed_sentence = break_sentence_at_commas(single_sentence)
        return processed_sentence

    result_parts = []

    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue

        # Apply comma breaking to this sentence
        processed_sentence = break_sentence_at_commas(sentence)
        result_parts.append(processed_sentence)

        # Check if we should add a line break after this sentence
        next_sent = sentences[i + 1] if i + 1 < len(sentences) else None
        
        # Use spaCy-enhanced breaking logic if available
        if SPACY_AVAILABLE:
            try:
                should_break = should_break_after_sentence_spacy(sentence, next_sent)
            except Exception:
                should_break = should_break_after_sentence(sentence, next_sent)
        else:
            should_break = should_break_after_sentence(sentence, next_sent)
        
        if should_break and next_sent:
            result_parts.append('\n')
        else:
            # Add space if there's a next sentence and no line break
            if next_sent:
                result_parts.append(' ')

    return ''.join(result_parts)
