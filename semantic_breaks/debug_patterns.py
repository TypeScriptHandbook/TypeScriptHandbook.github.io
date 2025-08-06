"""
Debug utilities for testing comma patterns.
"""

import re
from comma_patterns import COMMA_NO_BREAK_PATTERNS
from comma_breaking import should_break_at_comma


def test_series_detection():
    """Test if series detection works correctly."""
    test_cases = [
        "Java, Rust, C#, or Haskell",
        "apples, oranges, and bananas",
        "cats and dogs",
        "red, white, blue, and green",
        "Node.js, React, and Vue.js",
        "C++, C#, and F#"
    ]

    # Compile patterns
    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in COMMA_NO_BREAK_PATTERNS]

    for test_case in test_cases:
        print(f"\nTesting: '{test_case}'")

        # Find all comma positions
        comma_positions = [i for i, char in enumerate(test_case) if char == ',']

        for pos in comma_positions:
            print(f"  Comma at position {pos}: '{test_case[pos - 5:pos + 10]}'")

            # Check if any pattern matches around this comma
            matched = False
            for i, pattern in enumerate(compiled_patterns):
                # Check wider context around comma
                start = max(0, pos - 50)
                end = min(len(test_case), pos + 50)
                context = test_case[start:end]

                if pattern.search(context):
                    print(f"    ✓ Matched pattern {i}: {COMMA_NO_BREAK_PATTERNS[i]}")
                    matched = True
                    break

            if not matched:
                print(f"    ✗ No pattern matched - would break here")


def test_actual_breaking():
    """Test the actual should_break_at_comma function."""
    test_sentence = "If you're coming from a background in strongly typed languages like Java, Rust, C#, or Haskell, JavaScript might initially appear bewildering."

    print(f"\nTesting actual breaking function:")
    print(f"Sentence: {test_sentence}")
    print(f"Length: {len(test_sentence)}")

    # Find all comma positions
    comma_positions = [i for i, char in enumerate(test_sentence) if char == ',']

    for pos in comma_positions:
        before = test_sentence[max(0, pos - 10):pos]
        after = test_sentence[pos:pos + 15]
        should_break = should_break_at_comma(test_sentence, pos)

        print(f"\n  Comma at {pos}: '{before},{after}'")
        print(f"    should_break_at_comma() returns: {should_break}")

        if should_break:
            print(f"    ✗ WOULD BREAK HERE")
        else:
            print(f"    ✓ Protected from breaking")


def test_problematic_sentence():
    """Test the specific sentence that's causing issues."""
    sentence = "If you're coming from a background in strongly typed languages like Java, Rust, C#, or Haskell, JavaScript might initially appear bewildering."

    print(f"\n=== PROBLEMATIC SENTENCE TEST ===")
    print(f"Sentence: {sentence}")

    # Test just the series part first
    series_part = "Java, Rust, C#, or Haskell"
    print(f"\nTesting series part: '{series_part}'")

    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in COMMA_NO_BREAK_PATTERNS]

    for i, pattern in enumerate(compiled_patterns):
        if pattern.search(series_part):
            print(f"  ✓ Series matches pattern {i}")

    # Now test the full sentence comma by comma
    print(f"\nFull sentence analysis:")
    comma_positions = [i for i, char in enumerate(sentence) if char == ',']

    for pos in comma_positions:
        before = sentence[max(0, pos - 15):pos]
        after = sentence[pos:pos + 20]

        print(f"\n  Comma {pos}: '...{before},{after}...'")

        # Check each pattern
        for i, pattern in enumerate(compiled_patterns):
            start = max(0, pos - 50)
            end = min(len(sentence), pos + 50)
            context = sentence[start:end]

            if pattern.search(context):
                print(f"    ✓ Matches pattern {i}: {COMMA_NO_BREAK_PATTERNS[i][:50]}...")
                break
        else:
            print(f"    ✗ No patterns match - SHOULD BREAK")

        # Test actual function
        should_break = should_break_at_comma(sentence, pos)
        print(f"    should_break_at_comma() = {should_break}")


if __name__ == "__main__":
    test_series_detection()
    test_actual_breaking()
    test_problematic_sentence()
