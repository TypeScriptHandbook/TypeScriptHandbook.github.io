# spaCy Integration for Semantic Line Breaks

This enhanced version of the semantic line breaking tool integrates spaCy for improved grammatical analysis and more intelligent line breaking decisions.

## Installation

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Install spaCy and language model:
   ```bash
   python install_spacy.py
   ```

   Or manually:
   ```bash
   pip install spacy>=3.4.0
   python -m spacy download en_core_web_sm
   ```

## Features Enhanced by spaCy

### 1. Dependency-Based Sentence Analysis
- Uses syntactic parsing instead of regex patterns for clause detection
- Identifies subordinate clauses, relative clauses, and coordinate structures
- More accurate than pattern matching

### 2. Named Entity Protection
- Automatically protects named entities (people, organizations, dates, etc.) from inappropriate breaks
- Replaces manual abbreviation lists with intelligent entity recognition

### 3. Part-of-Speech Aware Breaking
- Makes breaking decisions based on grammatical roles
- Identifies coordinating conjunctions with subjects
- Recognizes participial phrases and adverbial clauses

### 4. Complexity-Based Breaking
- Calculates sentence complexity scores based on syntactic features
- Breaks sentences with high subordination or coordination
- Configurable complexity thresholds

## Configuration

spaCy-specific settings in `config.py`:

```python
# spaCy model to use
SPACY_MODEL = "en_core_web_sm"

# Complexity threshold for sentence breaking
SPACY_COMPLEXITY_THRESHOLD = 5.0

# Minimum words after comma to justify breaking
SPACY_MIN_CLAUSE_WORDS = 3

# Entity types to protect
PROTECTED_ENTITY_TYPES = [
    "PERSON", "ORG", "GPE", "DATE", "TIME", 
    "MONEY", "PERCENT", "CARDINAL", "ORDINAL"
]
```

## Testing

Run the test suite to verify functionality:

```bash
python test_spacy_integration.py
```

## Fallback Behavior

The tool automatically falls back to NLTK-based processing if:
- spaCy is not installed
- The language model is not available
- spaCy processing fails for any reason

This ensures the tool remains functional even without spaCy.

## Performance Considerations

spaCy processing is more sophisticated but slightly slower than regex patterns. For large documents, the improved accuracy typically outweighs the performance cost.

The tool caches the spaCy model after first load for better performance in batch processing scenarios.

## Architecture

The integration follows a clean separation of concerns:

- `spacy_integration.py` - Core spaCy functionality
- `semantic_breaks.py` - Main logic with spaCy/NLTK fallback
- `sentence_breaking.py` - Sentence boundary detection
- `comma_breaking.py` - Comma-based clause breaking
- `config.py` - Configuration constants

Each module can function independently with appropriate fallbacks, making the codebase resilient and maintainable.