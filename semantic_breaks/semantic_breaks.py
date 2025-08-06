"""
Main semantic line breaking functionality.
"""

from sentence_reassembly import reassemble_broken_sentences
from sentence_breaking import split_into_sentences, should_break_after_sentence
from comma_breaking import break_sentence_at_commas


def apply_semantic_breaks(text: str) -> str:
    """Apply semantic line breaks to a paragraph of text."""
    if not text.strip():
        return text

    # First, reassemble any previously broken sentences
    reassembled_text = reassemble_broken_sentences(text)

    # Split into sentences using NLTK with protection for abbreviations/markdown
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
        if should_break_after_sentence(sentence, next_sent) and next_sent:
            result_parts.append('\n')
        else:
            # Add space if there's a next sentence and no line break
            if next_sent:
                result_parts.append(' ')

    return ''.join(result_parts)
