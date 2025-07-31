"""
File generation functionality for test files and consolidated output
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

from models import TypeScriptExample, TestConfig


class FileGenerator:
    """Handles creation of test files and consolidated output"""

    def __init__(self, config: TestConfig) -> None:
        self.config = config

    def create_package_json(self) -> None:
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

    def create_tsconfig(self) -> None:
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

    def create_support_files(self) -> None:
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

    def create_config_files(self) -> None:
        """Create all configuration and support files"""
        self.create_package_json()
        self.create_tsconfig()
        self.create_support_files()

    def create_chapter_files(self, chapters: dict[str, list[TypeScriptExample]]) -> None:
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

    def setup_test_directory(self) -> None:
        """Setup the test directory structure"""
        if self.config.temp_dir.exists():
            shutil.rmtree(self.config.temp_dir)
            print(f"🗑️  Removed existing test directory: {self.config.temp_dir}")

        self.config.temp_dir.mkdir(exist_ok=True)
        print(f"📁 Created test directory: {self.config.temp_dir}")

        if self.config.specific_chapters:
            chapters_str = ', '.join(map(str, self.config.specific_chapters))
            print(f"📋 Testing chapters: {chapters_str}")

    def create_test_files(self, examples: list[TypeScriptExample]) -> None:
        """Create all test files from examples"""
        self.setup_test_directory()
        self.create_config_files()

        if not examples:
            print("⚠️  No TypeScript examples found")
            return

        # Group examples by chapter
        chapters: dict[str, list[TypeScriptExample]] = {}
        for example in examples:
            if example.chapter not in chapters:
                chapters[example.chapter] = []
            chapters[example.chapter].append(example)

        # Create chapter directories and files
        self.create_chapter_files(chapters)

    def should_include_example(self, example: TypeScriptExample, failing_files: set[str]) -> bool:
        """Determine if an example should be included in the output"""
        if self.config.include_all_examples:
            return True

        # Check if this example's filename matches any of the failing files
        # Normalize both paths to use forward slashes for comparison
        example_file = example.filename.replace('\\', '/')

        for failing_file in failing_files:
            # Normalize the failing file path too
            normalized_failing_file = failing_file.replace('\\', '/')

            # Exact match
            if example_file == normalized_failing_file:
                return True

            # Check if failing file is a relative path that matches the end of example file
            if example_file.endswith('/' + normalized_failing_file):
                return True

            # Check if example file is a relative path that matches the end of failing file
            if normalized_failing_file.endswith('/' + example_file):
                return True

        return False

    def create_consolidated_file(self, examples: list[TypeScriptExample],
                               type_check_output: str, failing_files: set[str]) -> None:
        """Create consolidated file with all examples and type check results"""
        output_path = Path("test_all.txt")

        # Write consolidated file
        with open(output_path, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write("TYPESCRIPT BOOK EXAMPLES - CONSOLIDATED TEST FILE\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total examples: {len(examples)}\n")

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

            for example in examples:
                if self.should_include_example(example, failing_files):
                    if example.chapter not in chapters:
                        chapters[example.chapter] = []
                    chapters[example.chapter].append(example)
                    included_count += 1

            if not self.config.include_all_examples and included_count < len(examples):
                f.write(f"Note: Showing {included_count} examples with errors out of {len(examples)} total examples.\n")
                f.write("Use --everything flag to include all examples.\n\n")

            for chapter_name in sorted(chapters.keys()):
                chapter_examples = chapters[chapter_name]
                f.write("=" * 80 + "\n")
                f.write(f"CHAPTER: {chapter_name.upper()}\n")
                f.write(f"Examples: {len(chapter_examples)}")

                if not self.config.include_all_examples:
                    total_in_chapter = sum(1 for ex in examples if ex.chapter == chapter_name)
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

        if not self.config.include_all_examples and len(examples) > 0:
            included_count = sum(1 for ex in examples if self.should_include_example(ex, failing_files))
            if included_count < len(examples):
                print(f"📊 Included {included_count} examples with errors (out of {len(examples)} total)")

    def cleanup(self) -> None:
        """Remove temporary files but keep the test structure"""
        node_modules = self.config.temp_dir / "node_modules"
        if node_modules.exists():
            shutil.rmtree(node_modules)
            print(f"🧹 Cleaned up node_modules")
        else:
            print(f"📁 Test directory preserved: {self.config.temp_dir}")
