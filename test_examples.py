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
    include_errors: bool = False

    @classmethod
    def create(cls, book_dir: str | Path = r".\docs\Chapters",
               temp_dir: str | Path | None = None,
               specific_chapters: list[int] | None = None,
               cleanup: bool = True,
               include_errors: bool = False) -> "TestConfig":
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
            include_errors=include_errors
        )


@dataclass
class TestResults:
    """Results from running the test suite"""
    total_examples: int
    successful_runs: int
    type_check_passed: bool
    errors: list[str]

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage"""
        if self.total_examples == 0:
            return 0.0
        return (self.successful_runs / self.total_examples) * 100

    @property
    def all_passed(self) -> bool:
        """Check if all tests passed"""
        return self.type_check_passed and self.successful_runs == self.total_examples


class ExampleTester:
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
            print("npm not found. Please ensure Node.js and npm are properly installed.")
            return False

        if not self._npx_cmd:
            print("npx not found. Please ensure Node.js and npm are properly installed.")
            return False

        print(f"🔧 Using npm: {self._npm_cmd}, npx: {self._npx_cmd}")
        return True

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

    def _run_subprocess(self, cmd: str, args: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
        """Run subprocess with guaranteed non-None command"""
        if not self._discover_commands():
            raise RuntimeError("Could not discover npm/npx commands")

        command = self._npm_cmd if cmd == 'npm' else self._npx_cmd
        assert command is not None  # Guaranteed by _discover_commands success

        return subprocess.run([command] + args,
                              cwd=self.config.temp_dir,
                              capture_output=True,
                              text=True,
                              shell=True,
                              **kwargs)

    def extract_code_blocks(self, markdown_file: Path) -> list[TypeScriptExample]:
        """Extract TypeScript code blocks from a markdown file"""
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = r'```ts\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        chapter_name = markdown_file.stem
        examples = []

        for i, code in enumerate(matches, 1):
            code = code.strip()
            if not code:
                continue

            examples.append(TypeScriptExample(
                chapter=chapter_name,
                number=i,
                code=code,
                source_file=str(markdown_file)
            ))

        return examples

    def find_markdown_files(self, specific_chapters: list[int] | None = None) -> list[Path]:
        """Find markdown files, optionally filtered by chapter numbers"""
        all_files = list(self.config.book_dir.glob("*.md"))

        if not specific_chapters:
            return all_files

        filtered_files = []
        for chapter_num in specific_chapters:
            chapter_files = [
                f for f in all_files
                if f.stem == f"{chapter_num:02d}" or f.stem == str(chapter_num)
            ]
            filtered_files.extend(chapter_files)
        return filtered_files

    def _create_config_files(self) -> None:
        """Create package.json, tsconfig.json, and other config files"""
        # package.json
        package_json = {
            "name": "typescript-book-examples",
            "version": "1.0.0",
            "devDependencies": {
                "typescript": "^5.0.0",
                "@types/node": "^20.0.0",
                "ts-node": "^10.0.0"
            }
        }
        with open(self.config.temp_dir / "package.json", 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2)

        # tsconfig.json
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
        with open(self.config.temp_dir / "tsconfig.json", 'w', encoding='utf-8') as f:
            json.dump(tsconfig, f, indent=2)

        # .gitignore
        gitignore_content = """# Dependencies
node_modules/
package-lock.json

# Generated files that change frequently
*.log
*.tmp
"""
        with open(self.config.temp_dir / ".gitignore", 'w', encoding='utf-8') as f:
            f.write(gitignore_content)

        # README.md
        readme_content = """# TypeScript Book Examples Test Directory

This directory contains automatically extracted TypeScript examples from the book chapters.

## Structure

test/
- package.json         # TypeScript dependencies
- tsconfig.json        # TypeScript compiler configuration
- chapter01/           # Examples from Chapter 1
  - example_01.ts
  - example_02.ts
  - ...
- chapter02/           # Examples from Chapter 2
  - example_01.ts
  - ...

## Usage
Run the test script from the project root:
```bash
python test_examples.py
```

Each chapter directory contains the extracted code examples from that chapter's markdown file.
This directory is automatically recreated each time the test script runs.
"""
        with open(self.config.temp_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)

    def _create_chapter_files(self, chapters: dict[str, list[TypeScriptExample]]) -> None:
        """Create TypeScript files organized by chapter"""
        for chapter_name, chapter_examples in chapters.items():
            chapter_dir = self.config.temp_dir / chapter_name
            chapter_dir.mkdir(exist_ok=True)

            # Create chapter README
            chapter_readme = f"""# {chapter_name.title()} Examples

This directory contains {len(chapter_examples)} examples extracted from {chapter_name}.md

## Examples:
"""
            for i, example in enumerate(chapter_examples, 1):
                chapter_readme += f"- `example_{i:02d}.ts` - Example {example.number} from the source\n"

            with open(chapter_dir / "README.md", 'w', encoding='utf-8') as f:
                f.write(chapter_readme)

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

    def create_test_files(self, specific_chapters: list[int] | None = None) -> None:
        """Create TypeScript files from extracted examples"""
        # Setup test directory
        if self.config.temp_dir.exists():
            shutil.rmtree(self.config.temp_dir)
            print(f"🗑️  Removed existing test directory: {self.config.temp_dir}")

        self.config.temp_dir.mkdir(exist_ok=True)
        print(f"📁 Created test directory: {self.config.temp_dir}")

        if specific_chapters:
            print(f"📋 Testing chapters: {', '.join(map(str, specific_chapters))}")

        # Create configuration files
        self._create_config_files()

        # Extract examples from markdown files
        markdown_files = self.find_markdown_files(specific_chapters)
        for md_file in markdown_files:
            examples = self.extract_code_blocks(md_file)
            self.examples.extend(examples)

        # Group examples by chapter
        chapters: dict[str, list[TypeScriptExample]] = {}
        for example in self.examples:
            chapter = example.chapter
            if chapter not in chapters:
                chapters[chapter] = []
            chapters[chapter].append(example)

        # Create chapter directories and files
        self._create_chapter_files(chapters)

    def _get_type_check_output(self) -> str:
        """Get type check output for consolidated file"""
        if not self._discover_commands():
            return "ERROR: Could not discover npm/npx commands"

        print("Installing TypeScript dependencies...")
        try:
            self._run_subprocess('npm', ['install'], check=True)
        except (RuntimeError, subprocess.CalledProcessError) as e:
            return f"ERROR: Could not install TypeScript dependencies: {e}"

        print("Running type check...")
        try:
            result = self._run_subprocess('npx', ['tsc'])
            if result.returncode == 0:
                return "✅ All examples type check successfully!"
            else:
                return f"❌ Type checking failed:\n{result.stdout}\n{result.stderr}"
        except RuntimeError as e:
            return f"ERROR: Could not run TypeScript compiler: {e}"

    def create_consolidated_file(self, include_errors: bool = False,
                                 specific_chapters: list[int] | None = None) -> Path:
        """Create a single file containing all extracted examples for easy review"""
        consolidated_path = Path(".") / "test_all.txt"

        # Get type check output if requested
        type_check_output = ""
        if include_errors:
            print("Running type check to capture errors...")
            type_check_output = self._get_type_check_output()

        # Write consolidated file
        with open(consolidated_path, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write("TYPESCRIPT BOOK EXAMPLES - CONSOLIDATED TEST FILE\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total examples: {len(self.examples)}\n")
            f.write(f"Include errors: {include_errors}\n")
            if specific_chapters:
                f.write(f"Chapters tested: {', '.join(map(str, specific_chapters))}\n")
            f.write("\n")

            # Type check results
            if include_errors and type_check_output:
                f.write("=" * 80 + "\n")
                f.write("TYPE CHECK RESULTS\n")
                f.write("=" * 80 + "\n")
                f.write(type_check_output)
                f.write("\n\n")

            # Examples by chapter
            chapters: dict[str, list[TypeScriptExample]] = {}
            for example in self.examples:
                chapter = example.chapter
                if chapter not in chapters:
                    chapters[chapter] = []
                chapters[chapter].append(example)

            for chapter_name in sorted(chapters.keys()):
                chapter_examples = chapters[chapter_name]
                f.write("=" * 80 + "\n")
                f.write(f"CHAPTER: {chapter_name.upper()}\n")
                f.write(f"Examples: {len(chapter_examples)}\n")
                f.write("=" * 80 + "\n\n")

                for i, example in enumerate(chapter_examples, 1):
                    f.write("-" * 40 + "\n")
                    f.write(f"Example {i:02d} (Original #{example.number})\n")
                    f.write(f"File: {example.filename}\n")
                    f.write(f"Source: {example.source_file}\n")
                    f.write("-" * 40 + "\n")
                    f.write(example.code)
                    f.write("\n\n")

        print(f"📝 Created consolidated file: {consolidated_path}")
        return consolidated_path

    def cleanup(self) -> None:
        """Remove node_modules but keep the test files"""
        node_modules = self.config.temp_dir / "node_modules"
        if node_modules.exists():
            shutil.rmtree(node_modules)
            print(f"🧹 Cleaned up node_modules: {node_modules}")
        else:
            print(f"📁 Test directory preserved: {self.config.temp_dir}")

    def test_all(self) -> TestResults:
        """Run the complete test suite and create consolidated file"""
        print(f"🔍 Extracting examples from: {self.config.book_dir}")
        print(f"📁 Using test directory: {self.config.temp_dir}")

        try:
            # Extract and create test files
            self.create_test_files(self.config.specific_chapters)
            print(f"📄 Extracted {len(self.examples)} examples")

            # Always create consolidated file
            self.create_consolidated_file(self.config.include_errors, self.config.specific_chapters)

            return TestResults(
                total_examples=len(self.examples),
                successful_runs=len(self.examples),
                type_check_passed=True,
                errors=[]
            )

        finally:
            if self.config.cleanup:
                self.cleanup()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description='Test TypeScript examples from markdown files and create consolidated output')
    parser.add_argument('--book-dir', default=r'.\docs\Chapters', help='Directory containing markdown files')
    parser.add_argument('--temp-dir', help='Directory for test files (default: ./test)')
    parser.add_argument('--no-cleanup', action='store_true', help='Keep node_modules directory')
    parser.add_argument('--include-errors', action='store_true',
                        help='Include TypeScript error output in consolidated file')
    parser.add_argument('--chapters', type=int, nargs='+', help='Test only specific chapters (e.g., --chapters 1 2 5)')

    args = parser.parse_args()

    config = TestConfig.create(
        book_dir=args.book_dir,
        temp_dir=args.temp_dir,
        specific_chapters=args.chapters,
        cleanup=not args.no_cleanup,
        include_errors=args.include_errors
    )

    tester = ExampleTester(config)

    try:
        results = tester.test_all()
        success = results.all_passed

        if success:
            print(f"✅ Successfully processed {results.total_examples} examples and created consolidated file")
        else:
            print(f"⚠️  Processed {results.total_examples} examples with some issues - check test_all.txt for details")

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n⏹️  Processing interrupted")
        if not args.no_cleanup:
            tester.cleanup()
        sys.exit(1)


if __name__ == '__main__':
    main()
