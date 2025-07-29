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
from datetime import datetime
from pathlib import Path


class ExampleTester:
    def __init__(self, book_dir=r".\docs\Chapters", temp_dir=None):
        self.book_dir = Path(book_dir)
        # Default to 'test' directory in project root
        if temp_dir is None:
            # Find project root (directory containing this script)
            script_dir = Path(__file__).parent if __file__ else Path.cwd()
            self.temp_dir = script_dir / "test"
        else:
            self.temp_dir = Path(temp_dir)
        self.examples = []

    def extract_code_blocks(self, markdown_file):
        """Extract TypeScript code blocks from a markdown file"""
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all TypeScript code blocks
        pattern = r'```ts\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)

        chapter_name = markdown_file.stem
        examples = []

        for i, code in enumerate(matches, 1):
            # Clean up the code
            code = code.strip()
            if not code:
                continue

            example = {
                'chapter': chapter_name,
                'number': i,
                'filename': f"{chapter_name}_example_{i:02d}.ts",
                'code': code,
                'source_file': str(markdown_file)
            }
            examples.append(example)

        return examples

    def find_markdown_files(self):
        """Find all markdown files in the book directory"""
        return list(self.book_dir.glob("*.md"))

    def create_test_files(self):
        """Create TypeScript files from extracted examples"""
        # Remove and recreate test directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print(f"🗑️  Removed existing test directory: {self.temp_dir}")

        self.temp_dir.mkdir(exist_ok=True)
        print(f"📁 Created test directory: {self.temp_dir}")

        # Create package.json for TypeScript support at root of test directory
        package_json = {
            "name": "typescript-book-examples",
            "version": "1.0.0",
            "devDependencies": {
                "typescript": "^5.0.0",
                "@types/node": "^20.0.0",
                "ts-node": "^10.0.0"
            }
        }

        with open(self.temp_dir / "package.json", 'w', encoding='utf-8') as f:
            json.dump(package_json, f, indent=2)

        # Create tsconfig.json that includes all subdirectories
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

        with open(self.temp_dir / "tsconfig.json", 'w', encoding='utf-8') as f:
            json.dump(tsconfig, f, indent=2)

        # Create .gitignore to ignore node_modules but keep the test files
        gitignore_content = """# Dependencies
node_modules/
package-lock.json

# Generated files that change frequently
*.log
*.tmp
"""

        with open(self.temp_dir / ".gitignore", 'w', encoding='utf-8') as f:
            f.write(gitignore_content)

        # Create README explaining the test directory (avoiding Unicode box characters)
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
- ...

## Usage
Run the test script from the project root:
```bash
python test_examples.py
```

Each chapter directory contains the extracted code examples from that chapter's markdown file.
This directory is automatically recreated each time the test script runs.
"""

        with open(self.temp_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)

        # Extract examples from all markdown files
        markdown_files = self.find_markdown_files()

        for md_file in markdown_files:
            examples = self.extract_code_blocks(md_file)
            self.examples.extend(examples)

        # Group examples by chapter and create chapter directories
        chapters = {}
        for example in self.examples:
            chapter = example['chapter']
            if chapter not in chapters:
                chapters[chapter] = []
            chapters[chapter].append(example)

        # Create chapter directories and write TypeScript files
        for chapter_name, chapter_examples in chapters.items():
            chapter_dir = self.temp_dir / chapter_name
            chapter_dir.mkdir(exist_ok=True)

            # Create a README for each chapter
            chapter_readme = f"""# {chapter_name.title()} Examples

This directory contains {len(chapter_examples)} examples extracted from {chapter_name}.md

## Examples:
"""
            for i, example in enumerate(chapter_examples, 1):
                chapter_readme += f"- `example_{i:02d}.ts` - Example {example['number']} from the source\n"

            with open(chapter_dir / "README.md", 'w', encoding='utf-8') as f:
                f.write(chapter_readme)

            # Write TypeScript files with simplified names
            for i, example in enumerate(chapter_examples, 1):
                file_path = chapter_dir / f"example_{i:02d}.ts"

                # Add some helpful context as comments
                header = f"""// Extracted from: {example['source_file']}
// Original example number: {example['number']}
// Auto-generated - do not edit directly

"""

                # Wrap isolated expressions in a function to avoid top-level issues
                code = self.wrap_code_if_needed(example['code'])

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(header + code)

                # Update the example's filename for later reference
                example['filename'] = str(file_path.relative_to(self.temp_dir))

    def wrap_code_if_needed(self, code):
        """Add any necessary wrapping to make code valid TypeScript"""
        lines = code.strip().split('\n')

        # Don't wrap anything - let TypeScript handle conflicts with module resolution
        # Each file is isolated so there shouldn't be conflicts within a single file
        return code

    def indent_code(self, code, spaces):
        """Indent code by a number of spaces"""
        indent = ' ' * spaces
        return '\n'.join(indent + line if line.strip() else line for line in code.split('\n'))

    def install_dependencies(self):
        """Install TypeScript and dependencies"""
        print("Installing TypeScript dependencies...")

        # Try different npm commands for Windows compatibility
        npm_commands = ['npm', 'npm.cmd', 'npm.exe']

        for npm_cmd in npm_commands:
            try:
                subprocess.run([npm_cmd, 'install'],
                               cwd=self.temp_dir,
                               check=True,
                               capture_output=True,
                               text=True,
                               shell=True)  # Use shell=True for Windows
                return True
            except subprocess.CalledProcessError as e:
                print(f"Failed to install dependencies with {npm_cmd}: {e}")
                print(f"stdout: {e.stdout}")
                print(f"stderr: {e.stderr}")
                continue
            except FileNotFoundError:
                continue  # Try next command

        print("npm not found with any variant. Please ensure Node.js and npm are properly installed.")
        return False

    def type_check_examples(self):
        """Run TypeScript compiler to check examples"""
        print("Type checking examples...")

        # Try different npx commands for Windows compatibility
        npx_commands = ['npx', 'npx.cmd', 'npx.exe']

        for npx_cmd in npx_commands:
            try:
                result = subprocess.run([npx_cmd, 'tsc'],
                                        cwd=self.temp_dir,
                                        capture_output=True,
                                        text=True,
                                        shell=True)  # Use shell=True for Windows

                if result.returncode == 0:
                    print("✅ All examples type check successfully!")
                    return True
                else:
                    print("❌ Type checking failed:")
                    print(result.stdout)
                    print(result.stderr)
                    return False

            except FileNotFoundError:
                continue  # Try next command

        print("TypeScript compiler not found. Please ensure Node.js and npm are properly installed.")
        return False

    def run_examples(self):
        """Run the examples with Node.js"""
        print("Running examples...")
        success_count = 0

        # Try different npx commands for Windows compatibility
        npx_commands = ['npx', 'npx.cmd', 'npx.exe']

        for example in self.examples:
            file_path = self.temp_dir / example['filename']
            print(f"\n📝 Running {example['chapter']} example {example['number']} ({example['filename']})...")

            success = False
            for npx_cmd in npx_commands:
                try:
                    # Use ts-node to run TypeScript directly
                    result = subprocess.run([npx_cmd, 'ts-node', str(file_path)],
                                            cwd=self.temp_dir,
                                            capture_output=True,
                                            text=True,
                                            timeout=10,
                                            shell=True)  # Use shell=True for Windows

                    if result.returncode == 0:
                        print("✅ Success")
                        if result.stdout.strip():
                            print(f"Output: {result.stdout.strip()}")
                        success_count += 1
                        success = True
                        break
                    else:
                        if npx_cmd == npx_commands[-1]:  # Last attempt
                            print("❌ Runtime error:")
                            print(result.stderr)

                except subprocess.TimeoutExpired:
                    print("⏰ Timeout (example may have infinite loop)")
                    success = True  # Don't try other commands for timeout
                    break
                except FileNotFoundError:
                    continue  # Try next command
                except Exception as e:
                    if npx_cmd == npx_commands[-1]:  # Last attempt
                        print(f"❌ Error: {e}")

            if not success and not any(cmd for cmd in npx_commands):
                print("❌ Could not run example - npx not found")

        print(f"\n📊 Results: {success_count}/{len(self.examples)} examples ran successfully")
        return success_count == len(self.examples)

    def create_consolidated_file(self):
        """Create a single file containing all extracted examples for easy review"""
        consolidated_path = Path(".") / "test_all.txt"

        with open(consolidated_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("TYPESCRIPT BOOK EXAMPLES - CONSOLIDATED TEST FILE\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total examples: {len(self.examples)}\n\n")

            # Group by chapter for better organization
            chapters = {}
            for example in self.examples:
                chapter = example['chapter']
                if chapter not in chapters:
                    chapters[chapter] = []
                chapters[chapter].append(example)

            for chapter_name in sorted(chapters.keys()):
                chapter_examples = chapters[chapter_name]

                f.write("=" * 80 + "\n")
                f.write(f"CHAPTER: {chapter_name.upper()}\n")
                f.write("=" * 80 + "\n\n")

                for i, example in enumerate(chapter_examples, 1):
                    f.write("-" * 40 + "\n")
                    f.write(f"Example {i:02d} (Original #{example['number']})\n")
                    f.write(f"File: {example['filename']}\n")
                    f.write("-" * 40 + "\n")
                    f.write(example['code'])
                    f.write("\n\n")

        print(f"📝 Created consolidated file: {consolidated_path}")
        return consolidated_path

    def cleanup(self):
        """Remove node_modules but keep the test files"""
        node_modules = self.temp_dir / "node_modules"
        if node_modules.exists():
            shutil.rmtree(node_modules)
            print(f"🧹 Cleaned up node_modules: {node_modules}")
        else:
            print(f"📁 Test directory preserved: {self.temp_dir}")

    def test_all(self, cleanup=True, create_consolidated=False):
        """Run the complete test suite"""
        print(f"🔍 Extracting examples from: {self.book_dir}")
        print(f"📁 Using test directory: {self.temp_dir}")

        try:
            # Step 1: Extract and create test files
            self.create_test_files()
            print(f"📄 Extracted {len(self.examples)} examples")

            # Step 1.5: Create consolidated file if requested
            if create_consolidated:
                self.create_consolidated_file()
                return True  # Just create the file and exit

            # Step 2: Install dependencies
            if not self.install_dependencies():
                return False

            # Step 3: Type check
            type_check_ok = self.type_check_examples()

            # Step 4: Run examples
            run_ok = self.run_examples()

            return type_check_ok and run_ok

        finally:
            if cleanup:
                self.cleanup()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Test TypeScript examples from markdown files')
    parser.add_argument('--book-dir', default=r'.\docs\Chapters', help='Directory containing markdown files')
    parser.add_argument('--temp-dir', help='Directory for test files (default: ./test)')
    parser.add_argument('--no-cleanup', action='store_true', help='Keep node_modules directory')
    parser.add_argument('--type-check-only', action='store_true', help='Only run type checking')
    parser.add_argument('--consolidated', action='store_true', help='Create consolidated test_all.txt file and exit')

    args = parser.parse_args()

    tester = ExampleTester(args.book_dir, args.temp_dir)

    try:
        if args.consolidated:
            tester.create_test_files()
            tester.create_consolidated_file()
            success = True
        elif args.type_check_only:
            tester.create_test_files()
            tester.install_dependencies()
            success = tester.type_check_examples()
        else:
            success = tester.test_all(cleanup=not args.no_cleanup)

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted")
        if not args.no_cleanup:
            tester.cleanup()
        sys.exit(1)


if __name__ == '__main__':
    main()
