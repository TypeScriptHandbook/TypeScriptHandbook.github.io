#!/usr/bin/env python3
"""
TypeScript Example Tester
Extracts code blocks from markdown files and tests them with TypeScript compiler
"""

import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class TypeScriptExample:
    """Represents a single TypeScript code example extracted from markdown"""
    chapter: str
    number: int
    code: str
    source_file: str
    filename: str = ""

    def __post_init__(self) -> None:
        """Set default filename if not provided"""
        if not self.filename:
            self.filename = f"{self.chapter}_example_{self.number:02d}.ts"


@dataclass
class TestConfig:
    """Configuration for the test runner"""
    book_dir: Path
    temp_dir: Path
    specific_chapters: list[int] | None = None
    cleanup: bool = True
    include_all_examples: bool = False

    @classmethod
    def from_args(cls, book_dir: str | Path = r".\docs\Chapters",
                  temp_dir: str | Path | None = None,
                  specific_chapters: list[int] | None = None,
                  cleanup: bool = True,
                  include_all_examples: bool = False) -> "TestConfig":
        """Create TestConfig with path resolution"""
        book_path = Path(book_dir)

        if temp_dir is None:
            script_dir = Path(__file__).parent if __file__ else Path.cwd()
            temp_path = script_dir / "test"
        else:
            temp_path = Path(temp_dir)

        return cls(
            book_dir=book_path,
            temp_dir=temp_path,
            specific_chapters=specific_chapters,
            cleanup=cleanup,
            include_all_examples=include_all_examples
        )


@dataclass
class TestResults:
    """Results from running the test suite"""
    total_examples: int
    type_check_passed: bool
    errors: list[str]

    @property
    def success(self) -> bool:
        """Check if the test run was successful"""
        return self.type_check_passed and len(self.errors) == 0


class CommandNotFoundError(Exception):
    """Raised when npm or npx commands cannot be found"""
    pass


class ExampleTester:
    """Main class for extracting and testing TypeScript examples"""

    def __init__(self, config: TestConfig) -> None:
        self.config = config
        self.examples: list[TypeScriptExample] = []
        self._npm_cmd: str | None = None
        self._npx_cmd: str | None = None

    def _discover_commands(self) -> bool:
        """Discover and cache npm and npx commands"""
        if self._npm_cmd is not None and self._npx_cmd is not None:
            return True

        # Try different command variants for Windows compatibility
        npm_variants = ['npm', 'npm.cmd', 'npm.exe']
        npx_variants = ['npx', 'npx.cmd', 'npx.exe']

        self._npm_cmd = self._find_working_command(npm_variants)
        self._npx_cmd = self._find_working_command(npx_variants)

        if not self._npm_cmd:
            print("❌ npm not found. Please ensure Node.js and npm are properly installed.")
            return False
        return False

    def _run_type_check(self) -> tuple[str, list[str], set[str]]:
        """Run TypeScript compiler and return (full_output, error_summary, failing_files)"""
        print("Installing TypeScript dependencies...")
        try:
            self._run_subprocess('npm', ['install'], check=True)
        except (CommandNotFoundError, subprocess.CalledProcessError) as e:
            error = f"ERROR: Could not install TypeScript dependencies: {e}"
            return error, [error], set()

        print("Running type check...")
        try:
            result = self._run_subprocess('npx', ['tsc'])
            if result.returncode == 0:
                return "✅ All examples type check successfully!", [], set()
            else:
                full_output = f"❌ Type checking failed:\n{result.stdout}"
                if result.stderr:
                    full_output += f"\n{result.stderr}"

                error_summary, failing_files = self._parse_typescript_errors(result.stdout)
                if not error_summary:
                    error_summary = ["Type checking failed - see test_all.txt for details"]

                return full_output, error_summary, failing_files

        except CommandNotFoundError as e:
            error = f"ERROR: {e}"
            return error, [error], set()

    def _find_working_command(self, variants: list[str]) -> str | None:
        """Find the first working command from a list of variants"""
        for cmd in variants:
            try:
                result = subprocess.run([cmd, '--version'],
                                        capture_output=True,
                                        text=True,
                                        timeout=5,
                                        shell=True)
                if result.returncode == 0:
                    return cmd
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        return None

    def _run_subprocess(self, cmd_type: str, args: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
        """Run subprocess with guaranteed non-None command"""
        if not self._discover_commands():
            raise CommandNotFoundError("Could not discover npm/npx commands")

        command = self._npm_cmd if cmd_type == 'npm' else self._npx_cmd
        assert command is not None  # Guaranteed by _discover_commands success

        return subprocess.run([command] + args,
                              cwd=self.config.temp_dir,
                              capture_output=True,
                              text=True,
                              shell=True,
                              **kwargs)

    def _extract_typescript_blocks(self, content: str) -> list[str]:
        """Extract TypeScript code blocks from markdown content"""
        pattern = r'```ts\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        return [code.strip() for code in matches if code.strip()]

    def extract_code_blocks(self, markdown_file: Path) -> list[TypeScriptExample]:
        """Extract TypeScript code blocks from a markdown file"""
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            print(f"⚠️  Warning: Could not read {markdown_file}: {e}")
            return []

        code_blocks = self._extract_typescript_blocks(content)
        chapter_name = markdown_file.stem
        examples = []

        for i, code in enumerate(code_blocks, 1):
            examples.append(TypeScriptExample(
                chapter=chapter_name,
                number=i,
                code=code,
                source_file=str(markdown_file)
            ))

        return examples

    def find_markdown_files(self) -> list[Path]:
        """Find markdown files, optionally filtered by chapter numbers"""
        try:
            all_files = list(self.config.book_dir.glob("*.md"))
        except OSError as e:
            print(f"❌ Error accessing directory {self.config.book_dir}: {e}")
            return []

        if not self.config.specific_chapters:
            return all_files

        filtered_files = []
        for chapter_num in self.config.specific_chapters:
            chapter_files = [
                f for f in all_files
                if f.stem == f"{chapter_num:02d}" or f.stem == str(chapter_num)
            ]
            filtered_files.extend(chapter_files)

        return filtered_files

    def _create_package_json(self) -> None:
        """Create package.json for TypeScript dependencies"""
        package_json = {
            "name": "typescript-book-examples",
            "version": "1.0.0",
            "devDependencies": {
                "typescript": "^5.0.0",
                "@types/node": "^20.0.0",
                "ts-node": "^10.0.0"
            }
        }

        package_path = self.config.temp_dir / "package.json"
        with open(package_path, 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2)

    def _create_tsconfig(self) -> None:
        """Create TypeScript configuration file"""
        tsconfig = {
            "compilerOptions": {
                "target": "ES2020",
                "module": "ESNext",
                "moduleResolution": "node",
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True,
                "noEmit": True,
                "allowUnreachableCode": True,
                "allowUnusedLabels": True
            },
            "include": ["**/*.ts"]
        }

        tsconfig_path = self.config.temp_dir / "tsconfig.json"
        with open(tsconfig_path, 'w', encoding='utf-8') as f:
            json.dump(tsconfig, f, indent=2)

    def _create_support_files(self) -> None:
        """Create .gitignore and README files"""
        # .gitignore
        gitignore_content = """# Dependencies
node_modules/
package-lock.json

# Generated files
*.log
*.tmp
"""
        with open(self.config.temp_dir / ".gitignore", 'w', encoding='utf-8') as f:
            f.write(gitignore_content)

        # README.md
        readme_content = f"""# TypeScript Book Examples Test Directory

Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This directory contains automatically extracted TypeScript examples from the book chapters.

## Structure
- `package.json` - TypeScript dependencies
- `tsconfig.json` - TypeScript compiler configuration
- `chapter*/` - Example directories organized by chapter
- Each chapter contains numbered TypeScript files

## Usage
This directory is automatically recreated each time the test script runs.
See `test_all.txt` in the parent directory for consolidated results.
"""
        with open(self.config.temp_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)

    def _create_config_files(self) -> None:
        """Create all configuration and support files"""
        self._create_package_json()
        self._create_tsconfig()
        self._create_support_files()

    def _create_chapter_files(self, chapters: dict[str, list[TypeScriptExample]]) -> None:
        """Create TypeScript files organized by chapter"""
        for chapter_name, chapter_examples in chapters.items():
            chapter_dir = self.config.temp_dir / chapter_name
            chapter_dir.mkdir(exist_ok=True)

            # Create chapter README
            readme_content = f"""# {chapter_name.title()} Examples

This directory contains {len(chapter_examples)} examples extracted from {chapter_name}.md

## Examples:
"""
            for i, example in enumerate(chapter_examples, 1):
                readme_content += f"- `example_{i:02d}.ts` - Example {example.number} from the source\n"

            with open(chapter_dir / "README.md", 'w', encoding='utf-8') as f:
                f.write(readme_content)

            # Create TypeScript files
            for i, example in enumerate(chapter_examples, 1):
                file_path = chapter_dir / f"example_{i:02d}.ts"

                header = f"""// Extracted from: {example.source_file}
// Original example number: {example.number}
// Auto-generated - do not edit directly

"""
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(header + example.code)

                # Update filename for later reference
                example.filename = str(file_path.relative_to(self.config.temp_dir))

    def create_test_files(self) -> None:
        """Create TypeScript files from extracted examples"""
        # Setup test directory
        if self.config.temp_dir.exists():
            shutil.rmtree(self.config.temp_dir)
            print(f"🗑️  Removed existing test directory: {self.config.temp_dir}")

        self.config.temp_dir.mkdir(exist_ok=True)
        print(f"📁 Created test directory: {self.config.temp_dir}")

        if self.config.specific_chapters:
            chapters_str = ', '.join(map(str, self.config.specific_chapters))
            print(f"📋 Testing chapters: {chapters_str}")

        # Create configuration files
        self._create_config_files()

        # Extract examples from markdown files
        markdown_files = self.find_markdown_files()
        if not markdown_files:
            print("⚠️  No markdown files found")
            return

        for md_file in markdown_files:
            examples = self.extract_code_blocks(md_file)
            self.examples.extend(examples)

        if not self.examples:
            print("⚠️  No TypeScript examples found")
            return

        # Group examples by chapter
        chapters: dict[str, list[TypeScriptExample]] = {}
        for example in self.examples:
            if example.chapter not in chapters:
                chapters[example.chapter] = []
            chapters[example.chapter].append(example)

        # Create chapter directories and files
        self._create_chapter_files(chapters)

    def _parse_typescript_errors(self, output: str) -> tuple[list[str], set[str]]:
        """Parse TypeScript compiler output to extract error summaries and failing files"""
        error_lines = []
        failing_files = set()

        for line in output.split('\n'):
            line = line.strip()
            if line and ': error TS' in line:
                # Format: "file(line,col): error TSxxxx: message"
                try:
                    # Extract the filename from the beginning of the error
                    file_part = line.split('(')[0] if '(' in line else line.split(':')[0]
                    if file_part:
                        # Normalize the path - TypeScript might output with forward slashes
                        # and we need to match against the stored filename format
                        normalized_file = file_part.replace('\\', '/').strip()
                        failing_files.add(normalized_file)

                    parts = line.split(': error TS', 1)
                    if len(parts) >= 2:
                        error_part = parts[1]
                        if ':' in error_part:
                            error_code, message = error_part.split(':', 1)
                            error_lines.append(f"TS{error_code.strip()}: {message.strip()}")
                        else:
                            error_lines.append(f"TS{error_part.strip()}")
                except (IndexError, ValueError):
                    # If parsing fails, use the original line
                    error_lines.append(line)

        return error_lines, failing_files

    def _should_include_example(self, example: TypeScriptExample, failing_files: set[str]) -> bool:
        """Determine if an example should be included in the output"""
        if self.config.include_all_examples:
            return True

        # Check if this example's filename matches any of the failing files
        # We need to handle different path formats
        example_file = example.filename.replace('\\', '/')

        for failing_file in failing_files:
            # Direct match
            if example_file == failing_file:
                return True
            # Check if the failing file ends with the example filename (relative path match)
            if failing_file.endswith('/' + example_file.split('/')[-1]):
                return True
            # Check if the example file ends with the failing file (in case paths are reversed)
            if example_file.endswith('/' + failing_file.split('/')[-1]):
                return True

        return False

    def create_consolidated_file(self) -> list[str]:
        """Create consolidated file with all examples and type check results"""
        output_path = Path("test_all.txt")

        print("Running type check...")
        type_check_output, error_summary, failing_files = self._run_type_check()

        # Write consolidated file
        with open(output_path, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write("TYPESCRIPT BOOK EXAMPLES - CONSOLIDATED TEST FILE\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total examples: {len(self.examples)}\n")

            if self.config.include_all_examples:
                f.write("Mode: All examples included\n")
            else:
                f.write("Mode: Error examples only\n")

            if self.config.specific_chapters:
                chapters_str = ', '.join(map(str, self.config.specific_chapters))
                f.write(f"Chapters tested: {chapters_str}\n")
            f.write("\n")

            # Type check results
            f.write("=" * 80 + "\n")
            f.write("TYPE CHECK RESULTS\n")
            f.write("=" * 80 + "\n")
            f.write(type_check_output)
            f.write("\n\n")

            # Examples by chapter (filtered based on mode)
            chapters: dict[str, list[TypeScriptExample]] = {}
            included_count = 0

            for example in self.examples:
                if self._should_include_example(example, failing_files):
                    if example.chapter not in chapters:
                        chapters[example.chapter] = []
                    chapters[example.chapter].append(example)
                    included_count += 1

            if not self.config.include_all_examples and included_count < len(self.examples):
                f.write(
                    f"Note: Showing {included_count} examples with errors out of {len(self.examples)} total examples.\n")
                f.write("Use --everything flag to include all examples.\n\n")

            for chapter_name in sorted(chapters.keys()):
                chapter_examples = chapters[chapter_name]
                f.write("=" * 80 + "\n")
                f.write(f"CHAPTER: {chapter_name.upper()}\n")
                f.write(f"Examples: {len(chapter_examples)}")

                if not self.config.include_all_examples:
                    total_in_chapter = sum(1 for ex in self.examples if ex.chapter == chapter_name)
                    if len(chapter_examples) < total_in_chapter:
                        f.write(f" (showing errors only, {total_in_chapter} total)")

                f.write("\n")
                f.write("=" * 80 + "\n\n")

                for i, example in enumerate(chapter_examples, 1):
                    f.write("-" * 40 + "\n")
                    f.write(f"Example {i:02d} (Original #{example.number})\n")
                    f.write(f"File: {example.filename}\n")
                    f.write(f"Source: {example.source_file}\n")

                    # Mark examples with errors
                    if example.filename in failing_files:
                        f.write("Status: ❌ HAS ERRORS\n")
                    elif self.config.include_all_examples:
                        f.write("Status: ✅ No errors\n")

                    f.write("-" * 40 + "\n")
                    f.write(example.code)
                    f.write("\n\n")

        print(f"📝 Created consolidated file: {output_path}")

        if not self.config.include_all_examples and len(self.examples) > 0:
            included_count = sum(1 for ex in self.examples if self._should_include_example(ex, failing_files))
            if included_count < len(self.examples):
                print(f"📊 Included {included_count} examples with errors (out of {len(self.examples)} total)")

        return error_summary

    def cleanup(self) -> None:
        """Remove temporary files but keep the test structure"""
        node_modules = self.config.temp_dir / "node_modules"
        if node_modules.exists():
            shutil.rmtree(node_modules)
            print(f"🧹 Cleaned up node_modules")
        else:
            print(f"📁 Test directory preserved: {self.config.temp_dir}")

    def run(self) -> TestResults:
        """Run the complete test suite and create consolidated file"""
        print(f"🔍 Extracting examples from: {self.config.book_dir}")
        print(f"📁 Using test directory: {self.config.temp_dir}")

        try:
            # Extract and create test files
            self.create_test_files()
            if not self.examples:
                return TestResults(
                    total_examples=0,
                    type_check_passed=False,
                    errors=["No TypeScript examples found"]
                )

            print(f"📄 Extracted {len(self.examples)} examples")

            # Create consolidated file and get error summary
            error_summary = self.create_consolidated_file()

            return TestResults(
                total_examples=len(self.examples),
                type_check_passed=len(error_summary) == 0,
                errors=error_summary
            )

        finally:
            if self.config.cleanup:
                self.cleanup()


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
  python test_examples.py                    # Test all chapters (errors only)
  python test_examples.py --everything       # Test all chapters (include all examples)
  python test_examples.py --chapters 1 2 3  # Test specific chapters (errors only)
  python test_examples.py --no-cleanup      # Keep temporary files
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
            tester.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
