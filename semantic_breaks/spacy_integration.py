"""
Enhanced grammatical analysis using spaCy for semantic line breaks.
"""

from typing import List, Optional, Tuple
import spacy
from spacy.lang.en import English
from spacy.tokens import Doc, Token, Span
from config import (
    SPACY_MODEL, SPACY_COMPLEXITY_THRESHOLD, SPACY_MIN_CLAUSE_WORDS,
    PROTECTED_ENTITY_TYPES, CLAUSE_BOUNDARY_DEPS, LONG_CLAUSE_THRESHOLD
)

_nlp = None


def get_nlp_model():
    """Get the spaCy model, loading it if necessary."""
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load(SPACY_MODEL)
        except OSError:
            print(f"spaCy model '{SPACY_MODEL}' not found. Using basic tokenizer...")
            print(f"Install with: python -m spacy download {SPACY_MODEL}")
            # Fallback to basic English tokenizer without statistical models
            _nlp = English()
            _nlp.add_pipe("sentencizer")
    return _nlp


def analyze_text_spacy(text: str) -> Doc:
    """Analyze text using spaCy and return the processed document."""
    nlp = get_nlp_model()
    return nlp(text)


def find_sentence_boundaries_spacy(text: str) -> List[str]:
    """Split text into sentences using spaCy's dependency-based detection."""
    doc = analyze_text_spacy(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]


def find_clause_boundaries_spacy(doc: Doc) -> List[int]:
    """Find clause boundaries using spaCy's dependency parsing."""
    boundaries = []
    
    for token in doc:
        # Subordinating conjunctions (when, because, although, etc.)
        if token.dep_ == "mark":
            boundaries.append(token.i)
        
        # Coordinating conjunctions with verbal heads
        elif (token.dep_ == "cc" and 
              token.head.pos_ == "VERB" and 
              token.i > 0):
            boundaries.append(token.i)
        
        # Relative clauses
        elif token.dep_ == "relcl":
            boundaries.append(token.i)
        
        # Adverbial clauses
        elif token.dep_ == "advcl":
            boundaries.append(token.i)
            
        # Participial phrases (present participle at clause start)
        elif (token.tag_ == "VBG" and 
              token.dep_ in ["acl", "advcl"] and
              token.i > 0):
            boundaries.append(token.i)
    
    return sorted(set(boundaries))


def should_break_at_comma_spacy(doc: Doc, comma_idx: int) -> bool:
    """Determine if we should break at a comma using syntactic analysis."""
    if comma_idx >= len(doc) or doc[comma_idx].text != ",":
        return False
    
    # Don't break if comma is part of a number
    if (comma_idx > 0 and comma_idx < len(doc) - 1 and
        doc[comma_idx - 1].like_num and doc[comma_idx + 1].like_num):
        return False
    
    # Don't break in named entities
    for ent in doc.ents:
        if ent.start <= comma_idx < ent.end:
            if ent.label_ in PROTECTED_ENTITY_TYPES:
                return False
    
    # Look at the token after the comma
    if comma_idx + 1 < len(doc):
        next_token = doc[comma_idx + 1]
        
        # Break after comma + coordinating conjunction + subject/clause
        if (next_token.pos_ == "CCONJ" and 
            comma_idx + 2 < len(doc)):
            # Check if there's a subject or new clause after conjunction
            following = doc[comma_idx + 2]
            if following.dep_ in ["nsubj", "nsubjpass", "csubj"] or following.pos_ == "PRON":
                return True
        
        # Break after comma + subordinating conjunction
        if next_token.dep_ == "mark":
            return True
        
        # Break after comma + adverbial phrases
        if next_token.dep_ == "advmod" and next_token.text.lower() in [
            "however", "therefore", "furthermore", "moreover", "nevertheless",
            "consequently", "meanwhile", "otherwise", "additionally"
        ]:
            return True
        
        # Break after comma + participial phrases
        if next_token.tag_ == "VBG" and next_token.dep_ in ["acl", "advcl"]:
            return True
    
    # Check clause length before comma
    clause_start = 0
    for i in range(comma_idx - 1, -1, -1):
        if doc[i].text == "\n":
            clause_start = i + 1
            break
    
    clause_tokens = doc[clause_start:comma_idx]
    clause_length = sum(len(token.text) + 1 for token in clause_tokens)  # +1 for spaces
    
    # Break if clause is long and there's substantial content after comma
    if clause_length > LONG_CLAUSE_THRESHOLD:
        remaining_tokens = doc[comma_idx + 1:]
        if len([t for t in remaining_tokens if not t.is_space and not t.is_punct]) >= SPACY_MIN_CLAUSE_WORDS:
            return True
    
    return False


def find_comma_break_positions_spacy(text: str) -> List[int]:
    """Find comma positions where we should break using spaCy analysis."""
    doc = analyze_text_spacy(text)
    break_positions = []
    
    for i, token in enumerate(doc):
        if token.text == "," and should_break_at_comma_spacy(doc, i):
            # Convert to character position in original text
            char_pos = token.idx + 1  # Position after the comma
            break_positions.append(char_pos)
    
    return break_positions


def protect_entities_spacy(text: str) -> List[Tuple[int, int, str]]:
    """Find spans that should be protected from sentence splitting using NER."""
    doc = analyze_text_spacy(text)
    protected_spans = []
    
    # Protect named entities
    for ent in doc.ents:
        if ent.label_ in PROTECTED_ENTITY_TYPES:
            protected_spans.append((ent.start_char, ent.end_char, ent.text))
    
    # Protect compound nouns and technical terms
    for chunk in doc.noun_chunks:
        # Protect multi-word technical terms (heuristic)
        if (len(chunk) > 1 and 
            any(token.is_alpha and token.is_title for token in chunk)):
            protected_spans.append((chunk.start_char, chunk.end_char, chunk.text))
    
    return protected_spans


def get_sentence_complexity_score(sentence: str) -> float:
    """Calculate a complexity score for a sentence based on syntactic features."""
    doc = analyze_text_spacy(sentence)
    
    if not doc:
        return 0.0
    
    score = 0.0
    
    # Count subordinate clauses
    subordinate_clauses = sum(1 for token in doc if token.dep_ in ["advcl", "ccomp", "xcomp", "acl", "relcl"])
    score += subordinate_clauses * 2
    
    # Count coordinating conjunctions
    coord_conj = sum(1 for token in doc if token.dep_ == "cc")
    score += coord_conj * 1.5
    
    # Count prepositional phrases
    prep_phrases = sum(1 for token in doc if token.dep_ == "prep")
    score += prep_phrases * 0.5
    
    # Normalize by sentence length
    if len(doc) > 0:
        score = score / len(doc) * 10  # Scale to reasonable range
    
    return min(score, 10.0)  # Cap at 10


def should_break_after_sentence_spacy(sentence: str, next_sentence: Optional[str] = None) -> bool:
    """Enhanced sentence breaking decision using spaCy analysis."""
    sentence = sentence.strip()
    
    # Always break after sentences that end with strong punctuation
    if sentence.endswith(('.', '!', '?')):
        return True
    
    # Analyze sentence complexity
    complexity = get_sentence_complexity_score(sentence)
    if complexity > SPACY_COMPLEXITY_THRESHOLD:
        return True
    
    # Check next sentence for transition words
    if next_sentence:
        next_doc = analyze_text_spacy(next_sentence.strip())
        if next_doc and len(next_doc) > 0:
            first_token = next_doc[0]
            if (first_token.text.lower() in [
                "however", "therefore", "furthermore", "moreover", "nevertheless",
                "consequently", "meanwhile", "otherwise", "additionally", "similarly",
                "conversely", "nonetheless"
            ]):
                return True
    
    # Break after long sentences (fallback)
    if len(sentence) > 80:  # Configurable threshold
        return True
    
    return False