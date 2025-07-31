#!/usr/bin/env python3
"""
TypeScript/JavaScript Example Tester - Main Entry Point
Extracts code blocks from markdown files and tests them with appropriate tools
"""

import sys

from models import TestConfig, TestResults, CodeType
from extractor import CodeExtractor
from type_checker import TypeChecker
from file_generator import FileGenerator
from utils import CommandDiscovery


class ExampleTester:
    """Main orchestrator for the TypeScript/JavaScript example testing process"""

    def __init__(self, config: TestConfig) -> None:
        self.config = config
        self.cmd_discovery = CommandDiscovery()
        self.extractor = CodeExtractor(config)
        self.type_checker = TypeChecker(config, self.cmd_discovery)
        self.file_generator = FileGenerator(config)

    def run(self) -> TestResults:
        """Run the complete test suite and create consolidated file"""
        print(f"🔍 Extracting examples from: {self.config.book_dir}")
        print(f"📁 Using test directory: {self.config.temp_dir}")

        try:
            # Extract examples
            examples = self.extractor.extract_all_examples()
            if not examples:
                return TestResults(
                    total_examples=0,
                    typescript_examples=0,
                    javascript_examples=0,
                    type_check_passed=False,
                    js_check_passed=False,
                    errors=["No code examples found"]
                )

            # Count examples by type
            ts_count = sum(1 for ex in examples if ex.is_typescript)
            js_count = sum(1 for ex in examples if ex.is_javascript)

            print(f"📄 Extracted {len(examples)} examples ({ts_count} TypeScript, {js_count} JavaScript)")

            # Create test files
            self.file_generator.create_test_files(examples)

            # Run checks and create consolidated file
            print("Running syntax and type checks...")
            ts_output, js_output, all_errors, failing_files = self.type_checker.run_checks()

            self.file_generator.create_consolidated_file(examples, ts_output, js_output, failing_files)

            # Determine if checks passed
            ts_passed = len([e for e in all_errors if e.startswith('TS')]) == 0
            js_passed = len([e for e in all_errors if e.startswith('JS')]) == 0

            return TestResults(
                total_examples=len(examples),
                typescript_examples=ts_count,
                javascript_examples=js_count,
                type_check_passed=ts_passed,
                js_check_passed=js_passed,
                errors=all_errors
            )

        finally:
            if self.config.cleanup:
                self.file_generator.cleanup()


def print_results(results: TestResults) -> None:
    """Print test results to console"""
    if results.success:
        print(f"✅ Successfully processed {results.total_examples} examples")
        print(f"   TypeScript: {results.typescript_examples} examples")
        print(f"   JavaScript: {results.javascript_examples} examples")
    else:
        print(f"⚠️  Processed {results.total_examples} examples with issues:")
        print(f"   TypeScript: {results.typescript_examples} examples (passed: {results.type_check_passed})")
        print(f"   JavaScript: {results.javascript_examples} examples (passed: {results.js_check_passed})")

        if results.errors:
            print(f"\n❌ Found {len(results.errors)} error(s):")
            for i, error in enumerate(results.errors, 1):
                # Truncate very long errors for console display
                display_error = error[:100] + "..." if len(error) > 100 else error
                print(f"   {i:2d}. {display_error}")
            print(f"\n📄 See test_results.txt for complete details")


def main() -> None:
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract TypeScript and JavaScript examples from markdown files and test them',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                         # Test all chapters (errors only)
  python main.py --everything            # Test all chapters (include all examples)
  python main.py --chapters 1 2 3       # Test specific chapters (errors only)
  python main.py --no-cleanup           # Keep temporary files

Note: 
  - TypeScript (.ts) examples are checked with the TypeScript compiler
  - JavaScript (.js) examples are checked with Node.js syntax validation
  - Examples maintain the order they appear in the markdown files
        """
    )

    parser.add_argument('--book-dir', default=r'.\docs\Chapters',
                        help='Directory containing markdown files (default: %(default)s)')
    parser.add_argument('--temp-dir',
                        help='Directory for test files (default: ./test)')
    parser.add_argument('--no-cleanup', action='store_true',
                        help='Keep node_modules directory after testing')
    parser.add_argument('--everything', action='store_true',
                        help='Include all examples in output (default: only show examples with errors)')
    parser.add_argument('--chapters', type=int, nargs='+',
                        help='Test only specific chapters (e.g., --chapters 1 2 5)')

    args = parser.parse_args()

    config = TestConfig.from_args(
        book_dir=args.book_dir,
        temp_dir=args.temp_dir,
        specific_chapters=args.chapters,
        cleanup=not args.no_cleanup,
        include_all_examples=args.everything
    )

    tester = ExampleTester(config)

    try:
        results = tester.run()
        print_results(results)
        sys.exit(0 if results.success else 1)

    except KeyboardInterrupt:
        print("\n⏹️  Processing interrupted")
        if config.cleanup:
            tester.file_generator.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
    
