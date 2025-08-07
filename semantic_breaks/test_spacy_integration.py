#!/usr/bin/env python3
"""
Test script for spaCy integration in semantic line breaks.
"""

from semantic_breaks import apply_semantic_breaks

def test_basic_functionality():
    """Test basic functionality with and without spaCy."""
    print("Testing basic functionality...")
    
    test_text = """
    This is a simple sentence. However, this sentence has multiple clauses, 
    and it should be broken appropriately. The tool should handle complex sentences
    with subordinating conjunctions, because they create natural breaking points.
    """
    
    result = apply_semantic_breaks(test_text.strip())
    print("Input:", repr(test_text.strip()))
    print("Output:", repr(result))
    print()

def test_comma_breaking():
    """Test comma-based breaking with spaCy analysis."""
    print("Testing comma breaking...")
    
    test_text = """
    The TypeScript compiler performs type checking, code generation, and optimization,
    but it also provides excellent tooling support for editors and IDEs.
    """
    
    result = apply_semantic_breaks(test_text.strip())
    print("Input:", repr(test_text.strip()))
    print("Output:", repr(result))
    print()

def test_entity_protection():
    """Test that named entities are protected from inappropriate breaking."""
    print("Testing entity protection...")
    
    test_text = """
    Microsoft Corporation was founded by Bill Gates and Paul Allen in April 1975.
    The company, headquartered in Redmond, Washington, became one of the largest
    software companies in the world.
    """
    
    result = apply_semantic_breaks(test_text.strip())
    print("Input:", repr(test_text.strip()))
    print("Output:", repr(result))
    print()

def test_complex_sentences():
    """Test complex sentence structures."""
    print("Testing complex sentences...")
    
    test_text = """
    When developers write TypeScript code, they often use interfaces to define
    object shapes, because interfaces provide a way to describe the structure
    of objects without creating actual implementations.
    """
    
    result = apply_semantic_breaks(test_text.strip())
    print("Input:", repr(test_text.strip()))
    print("Output:", repr(result))
    print()

def test_markdown_compatibility():
    """Test that the integration doesn't break markdown handling."""
    print("Testing markdown compatibility...")
    
    test_text = """
    The `interface` keyword in TypeScript defines a contract, but unlike classes,
    interfaces exist only at compile time. For example, `interface User { name: string; }`
    creates a type definition that can be used throughout your code.
    """
    
    result = apply_semantic_breaks(test_text.strip())
    print("Input:", repr(test_text.strip()))
    print("Output:", repr(result))
    print()

if __name__ == "__main__":
    print("Testing spaCy Integration for Semantic Line Breaks")
    print("=" * 60)
    
    # Check if spaCy is available
    try:
        from spacy_integration import SPACY_AVAILABLE
        if SPACY_AVAILABLE:
            print("OK spaCy integration is available")
        else:
            print("WARNING spaCy not available, using NLTK fallback")
    except ImportError:
        print("WARNING spaCy integration module not found, using NLTK fallback")
    
    print()
    
    test_basic_functionality()
    test_comma_breaking()
    test_entity_protection()
    test_complex_sentences()
    test_markdown_compatibility()
    
    print("Testing complete!")