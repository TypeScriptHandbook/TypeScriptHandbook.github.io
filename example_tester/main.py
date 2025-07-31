#!/usr/bin/env python3
"""
TypeScript Example Tester - Main Entry Point
Extracts code blocks from markdown files and tests them with TypeScript compiler
"""

import sys

from models import TestConfig, TestResults
from extractor import CodeExtractor
from type_checker import TypeChecker
from file_generator import FileGenerator
from utils import CommandDiscovery


class ExampleTester:
    """Main orchestrator for the TypeScript example testing process"""

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
                    type_check_passed=False,
                    errors=["No TypeScript examples found"]
                )

            print(f"📄 Extracted {len(examples)} examples")

            # Create test files
            self.file_generator.create_test_files(examples)

            # Run type checking and create consolidated file
            print("Running type check...")
            type_check_output, error_summary, failing_files = self.type_checker.run_type_check()

            self.file_generator.create_consolidated_file(examples, type_check_output, failing_files)

            return TestResults(
                total_examples=len(examples),
                type_check_passed=len(error_summary) == 0,
                errors=error_summary
            )

        finally:
            if self.config.cleanup:
                self.file_generator.cleanup()


def print_results(results: TestResults) -> None:
    """Print test results to console"""
    if results.success:
        print(f"✅ Successfully processed {results.total_examples} examples")
    else:
        print(f"⚠️  Processed {results.total_examples} examples with issues:")
        print(f"   Type check passed: {results.type_check_passed}")

        if results.errors:
            print(f"\n❌ Found {len(results.errors)} error(s):")
            for i, error in enumerate(results.errors, 1):
                # Truncate very long errors for console display
                display_error = error[:100] + "..." if len(error) > 100 else error
                print(f"   {i:2d}. {display_error}")
            print(f"\n📄 See test_all.txt for complete details")


def main() -> None:
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract TypeScript examples from markdown files and test them',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                         # Test all chapters (errors only)
  python main.py --everything            # Test all chapters (include all examples)
  python main.py --chapters 1 2 3       # Test specific chapters (errors only)
  python main.py --no-cleanup           # Keep temporary files
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
