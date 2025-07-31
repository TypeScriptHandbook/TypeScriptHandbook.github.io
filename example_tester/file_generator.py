"""
File generation functionality for test files and consolidated output
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

from models import CodeExample, TestConfig


class FileGenerator:
    """Handles creation of test files and consolidated output"""

    def __init__(self, config: TestConfig) -> None:
        self.config = config

    def create_package_json(self) -> None:
        """Create package.json for TypeScript and JavaScript dependencies"""
        package_json = {
            "name": "typescript-javascript-book-examples",
            "version": "1.0.0",
            "type": "module",  # Support ES modules for JavaScript
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
                "allowUnusedLabels": True,
                "allowJs": True,  # Allow JavaScript files to be processed
                "checkJs": False  # Don't type-check JavaScript files with TypeScript
            },
            "include": ["**/*.ts"],  # Only include TypeScript files for type checking
            "exclude": ["**/*.js"]   # Explicitly exclude JavaScript files from TypeScript checking
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
        readme_content = f"""# TypeScript and JavaScript Book Examples Test Directory

Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This directory contains automatically extracted TypeScript and JavaScript examples from the book chapters.

## Structure
- `package.json` - Dependencies for both TypeScript and JavaScript
- `tsconfig.json` - TypeScript compiler configuration (excludes .js files)
- `chapter*/` - Example directories organized by chapter
- Each chapter contains numbered files with appropriate extensions (.ts or .js)

## Testing Approach
- TypeScript files (.ts) are checked with the TypeScript compiler
- JavaScript files (.js) are checked with Node.js syntax validation
- Examples maintain the order they appear in the markdown files

## Usage
This directory is automatically recreated each time the test script runs.
See `test_results.txt` in the parent directory for consolidated results.
"""
        with open(self.config.temp_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)

    def create_config_files(self) -> None:
        """Create all configuration and support files"""
        self.create_package_json()
        self.create_tsconfig()
        self.create_support_files()

    def create_chapter_files(self, chapters: dict[str, list[CodeExample]]) -> None:
        """Create TypeScript and JavaScript files organized by chapter"""
        for chapter_name, chapter_examples in chapters.items():
            chapter_dir = self.config.temp_dir / chapter_name
            chapter_dir.mkdir(exist_ok=True)

            # Count examples by type
            ts_count = sum(1 for ex in chapter_examples if ex.is_typescript)
            js_count = sum(1 for ex in chapter_examples if ex.is_javascript)

            # Create chapter README
            readme_content = f"""# {chapter_name.title()} Examples

This directory contains {len(chapter_examples)} examples extracted from {chapter_name}.md
- TypeScript examples: {ts_count}
- JavaScript examples: {js_count}

## Examples (in order of appearance):
"""
            for i, example in enumerate(chapter_examples, 1):
                extension = example.code_type.value
                readme_content += f"- `example_{i:02d}.{extension}` - Example {example.number} from the source ({extension.upper()})\n"

            with open(chapter_dir / "README.md", 'w', encoding='utf-8') as f:
                f.write(readme_content)

            # Create code files with appropriate extensions
            for i, example in enumerate(chapter_examples, 1):
                extension = example.code_type.value
                file_path = chapter_dir / f"example_{i:02d}.{extension}"

                language_name = "TypeScript" if example.is_typescript else "JavaScript"
                header = f"""// Extracted from: {example.source_file}
// Original example number: {example.number}
// Language: {language_name}
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

    def create_test_files(self, examples: list[CodeExample]) -> None:
        """Create all test files from examples"""
        self.setup_test_directory()
        self.create_config_files()

        if not examples:
            print("⚠️  No code examples found")
            return

        # Count examples by type
        ts_count = sum(1 for ex in examples if ex.is_typescript)
        js_count = sum(1 for ex in examples if ex.is_javascript)
        print(f"📊 Found {ts_count} TypeScript and {js_count} JavaScript examples")

        # Group examples by chapter (maintaining order)
        chapters: dict[str, list[CodeExample]] = {}
        for example in examples:
            if example.chapter not in chapters:
                chapters[example.chapter] = []
            chapters[example.chapter].append(example)

        # Create chapter directories and files
        self.create_chapter_files(chapters)

    def should_include_example(self, example: CodeExample, failing_files: set[str]) -> bool:
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

    def extract_errors_for_file(self, filename: str, type_check_output: str, js_check_output: str) -> list[str]:
        """Extract specific error messages for a given file"""
        errors = []

        # Get just the filename for comparison
        file_basename = Path(filename).name

        # Extract TypeScript errors from individual file checking output
        # Look for sections that start with "Checking filename:" and contain "❌ FAILED"
        sections = type_check_output.split('\n\n')
        for section in sections:
            if f"Checking {file_basename}:" in section and "❌ FAILED" in section:
                # Extract error lines from this section
                lines = section.split('\n')
                for line in lines:
                    if ': error TS' in line:
                        try:
                            if '): error TS' in line:
                                error_part = line.split('): error TS', 1)[1]
                                if ':' in error_part:
                                    error_code, message = error_part.split(':', 1)
                                    errors.append(f"TS{error_code.strip()}: {message.strip()}")
                                else:
                                    errors.append(f"TS{error_part.strip()}")
                            else:
                                # Fallback for different error formats
                                if 'error TS' in line:
                                    error_part = line.split('error TS', 1)[1]
                                    if ':' in error_part:
                                        error_code, message = error_part.split(':', 1)
                                        errors.append(f"TS{error_code.strip()}: {message.strip()}")
                        except (IndexError, ValueError):
                            # If parsing fails, include the line as-is
                            if 'error TS' in line:
                                errors.append(line.strip())

        # Extract JavaScript errors
        js_sections = js_check_output.split('\n\n')
        for section in js_sections:
            if f"Checking {file_basename}:" in section and "❌ FAILED" in section:
                lines = section.split('\n')
                for line in lines:
                    if ('SyntaxError:' in line or 'ReferenceError:' in line or
                        'TypeError:' in line or 'Error:' in line):
                        errors.append(f"JS: {line.strip()}")

        return errors

    def create_consolidated_file(self, examples: list[CodeExample],
                               type_check_output: str, js_check_output: str, failing_files: set[str]) -> None:
        """Create consolidated file with all examples and check results"""
        output_path = Path("test_results.txt")

        # Count examples by type
        ts_count = sum(1 for ex in examples if ex.is_typescript)
        js_count = sum(1 for ex in examples if ex.is_javascript)

        # Write consolidated file
        with open(output_path, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write("TYPESCRIPT/JAVASCRIPT BOOK EXAMPLES - CONSOLIDATED TEST FILE\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total examples: {len(examples)}\n")
            f.write(f"TypeScript examples: {ts_count}\n")
            f.write(f"JavaScript examples: {js_count}\n")

            if self.config.include_all_examples:
                f.write("Mode: All examples included\n")
            else:
                f.write("Mode: Error examples only\n")

            if self.config.specific_chapters:
                chapters_str = ', '.join(map(str, self.config.specific_chapters))
                f.write(f"Chapters tested: {chapters_str}\n")
            f.write("\n")

            # TypeScript check results
            f.write("=" * 80 + "\n")
            f.write("TYPESCRIPT CHECK RESULTS\n")
            f.write("=" * 80 + "\n")
            f.write(type_check_output)
            f.write("\n\n")

            # JavaScript check results
            f.write("=" * 80 + "\n")
            f.write("JAVASCRIPT CHECK RESULTS\n")
            f.write("=" * 80 + "\n")
            f.write(js_check_output)
            f.write("\n\n")

            # Examples by chapter (filtered based on mode)
            chapters: dict[str, list[CodeExample]] = {}
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
                    f.write(f"Language: {'TypeScript' if example.is_typescript else 'JavaScript'}\n")
                    f.write(f"Source: {example.source_file}\n")

                    # Extract and display specific errors for this example
                    example_errors = self.extract_errors_for_file(example.filename, type_check_output, js_check_output)

                    if example_errors:
                        f.write("Status: ❌ HAS ERRORS\n")
                        f.write("Errors:\n")
                        for error in example_errors:
                            f.write(f"  • {error}\n")
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
