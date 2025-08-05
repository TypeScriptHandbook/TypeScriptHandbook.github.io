"""
Semantic line breaking logic using NLTK for sentence segmentation.
"""

from typing import Optional
import re

import nltk
from nltk.tokenize import sent_tokenize

from config import LONG_SENTENCE_THRESHOLD, TRANSITION_WORDS


class SemanticLineBreaker:
    def __init__(self):
        """Initialize the semantic line breaker with NLTK."""
        # Download required NLTK data if not already present
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
            except:
                pass  # punkt_tab might not be available in older NLTK versions

    def should_break_after_sentence(self, sent: str, next_sent: Optional[str] = None) -> bool:
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

    def apply_semantic_breaks(self, text: str) -> str:
        """Apply semantic line breaks to a paragraph of text."""
        if not text.strip():
            return text

        # Use NLTK to split into sentences, but be more careful about abbreviations
        # and markdown formatting
        protected_text = text
        replacements = []

        # Protect common abbreviations
        abbrev_patterns = [
            (r'\betc\.', 'ETCPERIOD'),
            (r'\be\.g\.', 'EGPERIOD'),
            (r'\bi\.e\.', 'IEPERIOD'),
            (r'\bvs\.', 'VSPERIOD'),
            (r'\bMr\.', 'MRPERIOD'),
            (r'\bMrs\.', 'MRSPERIOD'),
            (r'\bDr\.', 'DRPERIOD'),
        ]

        # Protect periods inside markdown formatting
        markdown_patterns = [
            # Bold text with periods: **text with period.**
            (r'\*\*([^*]+\.+[^*]*)\*\*', lambda m: f"**{m.group(1).replace('.', 'MDPERIOD')}**"),
            # Italic text with periods: *text with period.*
            (r'\*([^*]+\.+[^*]*)\*', lambda m: f"*{m.group(1).replace('.', 'MDPERIOD')}*"),
            # Code spans with periods: `code.method()`
            (r'`([^`]+\.+[^`]*)`', lambda m: f"`{m.group(1).replace('.', 'MDPERIOD')}`"),
            # Links with periods in text: [text with period.](url)
            (r'\[([^\]]+\.+[^\]]*)\]\([^)]+\)', lambda m: f"[{m.group(1).replace('.', 'MDPERIOD')}]({m.group(0).split('](')[1]}"),
        ]

        # Apply abbreviation protections
        for pattern, replacement in abbrev_patterns:
            matches = list(re.finditer(pattern, protected_text))
            for match in reversed(matches):  # Process in reverse to maintain indices
                original = match.group()
                replacements.append((replacement, original))
                protected_text = protected_text[:match.start()] + replacement + protected_text[match.end():]

        # Apply markdown protections
        for pattern, replacement_func in markdown_patterns:
            def replace_match(match):
                result = replacement_func(match)
                # Track what we replaced
                original_periods = match.group().count('.')
                for _ in range(original_periods):
                    replacements.append(('MDPERIOD', '.'))
                return result

            protected_text = re.sub(pattern, replace_match, protected_text)

        # Now use NLTK sentence tokenization
        sentences = sent_tokenize(protected_text)

        # Restore the original text
        for i, sentence in enumerate(sentences):
            for replacement, original in replacements:
                sentence = sentence.replace(replacement, original)
            sentences[i] = sentence

        if len(sentences) <= 1:
            return text

        result_parts = []

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue

            result_parts.append(sentence)

            # Check if we should add a line break
            next_sent = sentences[i + 1] if i + 1 < len(sentences) else None
            if self.should_break_after_sentence(sentence, next_sent) and next_sent:
                result_parts.append('\n')
            else:
                # Add space if there's a next sentence and no line break
                if next_sent:
                    result_parts.append(' ')

        return ''.join(result_parts)
