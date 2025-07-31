"""
TypeScript and JavaScript checking functionality
"""

import subprocess
from pathlib import Path

from models import CommandNotFoundError, TestConfig
from utils import CommandDiscovery


class TypeChecker:
    """Handles TypeScript compilation and JavaScript syntax checking"""

    def __init__(self, config: TestConfig, command_discovery: CommandDiscovery) -> None:
        self.config = config
        self.cmd_discovery = command_discovery

    def parse_typescript_errors(self, output: str) -> tuple[list[str], set[str]]:
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

    def parse_javascript_errors(self, output: str, js_files: list[Path]) -> tuple[list[str], set[str]]:
        """Parse Node.js syntax check output for JavaScript files"""
        error_lines = []
        failing_files = set()

        # Split output by file checks (each file check starts with the filename)
        sections = output.split('\n\n')

        for section in sections:
            if not section.strip():
                continue

            lines = section.strip().split('\n')
            if not lines:
                continue

            # Look for syntax errors in this section
            for line in lines:
                if ('SyntaxError:' in line or 'ReferenceError:' in line or
                    'TypeError:' in line or 'Error:' in line):

                    # Try to identify which file this error belongs to
                    # Check if any js file path appears in the error output
                    for js_file in js_files:
                        file_str = str(js_file.relative_to(self.config.temp_dir)).replace('\\', '/')
                        if file_str in section or js_file.name in section:
                            failing_files.add(file_str)
                            error_lines.append(f"JS Error in {js_file.name}: {line.strip()}")
                            break
                    else:
                        # Generic error if we can't identify the file
                        error_lines.append(f"JS Error: {line.strip()}")

        return error_lines, failing_files

    def find_javascript_files(self) -> list[Path]:
        """Find JavaScript files in chapter directories only (exclude node_modules)"""
        js_files = []
        try:
            # Only look in chapter directories, not in node_modules or other subdirectories
            for item in self.config.temp_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.') and item.name != 'node_modules':
                    # This should be a chapter directory
                    js_files.extend(item.glob("*.js"))
        except OSError:
            pass
        return js_files

    def check_javascript_syntax(self) -> tuple[str, list[str], set[str]]:
        """Check JavaScript files for syntax errors using Node.js"""
        js_files = self.find_javascript_files()

        if not js_files:
            return "✅ No JavaScript files to check", [], set()

        print(f"Checking {len(js_files)} JavaScript files...")

        all_output = []
        all_errors = []
        all_failing_files = set()

        for js_file in js_files:
            try:
                # Use node --check to validate syntax without executing
                result = self.cmd_discovery.run_subprocess(
                    'node',
                    ['--check', str(js_file.relative_to(self.config.temp_dir))],
                    self.config.temp_dir
                )

                file_output = f"Checking {js_file.name}:"
                if result.returncode == 0:
                    file_output += " ✅ OK"
                else:
                    file_output += f" ❌ FAILED\n{result.stderr}"
                    # Add to failing files
                    relative_path = str(js_file.relative_to(self.config.temp_dir)).replace('\\', '/')
                    all_failing_files.add(relative_path)
                    all_errors.append(f"JS Syntax Error in {js_file.name}: {result.stderr.strip()}")

                all_output.append(file_output)

            except (CommandNotFoundError, subprocess.CalledProcessError) as e:
                error_msg = f"Error checking {js_file.name}: {e}"
                all_output.append(error_msg)
                all_errors.append(error_msg)
                relative_path = str(js_file.relative_to(self.config.temp_dir)).replace('\\', '/')
                all_failing_files.add(relative_path)

        full_output = '\n\n'.join(all_output)

        if not all_errors:
            return f"✅ All {len(js_files)} JavaScript files passed syntax check!\n\n{full_output}", [], set()
        else:
            return f"❌ JavaScript syntax check failed:\n\n{full_output}", all_errors, all_failing_files

    def run_typescript_check(self) -> tuple[str, list[str], set[str]]:
        """Run TypeScript compiler on .ts files individually to avoid scope conflicts"""
        print("Running TypeScript check...")

        # Find all TypeScript files
        ts_files = []
        try:
            for item in self.config.temp_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.') and item.name != 'node_modules':
                    ts_files.extend(item.glob("*.ts"))
        except OSError:
            pass

        if not ts_files:
            return "✅ No TypeScript files to check", [], set()

        print(f"Checking {len(ts_files)} TypeScript files individually...")

        all_output = []
        all_errors = []
        all_failing_files = set()

        for ts_file in ts_files:
            try:
                # Check each TypeScript file individually with --noEmit flag
                result = self.cmd_discovery.run_subprocess(
                    'npx',
                    ['tsc', '--noEmit', '--strict', str(ts_file.relative_to(self.config.temp_dir))],
                    self.config.temp_dir
                )

                file_output = f"Checking {ts_file.name}:"
                if result.returncode == 0:
                    file_output += " ✅ OK"
                else:
                    file_output += f" ❌ FAILED\n{result.stdout}"
                    # Add to failing files
                    relative_path = str(ts_file.relative_to(self.config.temp_dir)).replace('\\', '/')
                    all_failing_files.add(relative_path)

                    # Parse errors for this specific file
                    file_errors, _ = self.parse_typescript_errors(result.stdout)
                    all_errors.extend(file_errors)

                all_output.append(file_output)

            except (CommandNotFoundError, subprocess.CalledProcessError) as e:
                error_msg = f"Error checking {ts_file.name}: {e}"
                all_output.append(error_msg)
                all_errors.append(error_msg)
                relative_path = str(ts_file.relative_to(self.config.temp_dir)).replace('\\', '/')
                all_failing_files.add(relative_path)

        full_output = '\n\n'.join(all_output)

        if not all_errors:
            return f"✅ All {len(ts_files)} TypeScript files passed type checking!\n\n{full_output}", [], set()
        else:
            return f"❌ TypeScript checking failed:\n\n{full_output}", all_errors, all_failing_files

    def run_checks(self) -> tuple[str, str, list[str], set[str]]:
        """Run both TypeScript and JavaScript checks and return combined results"""
        print("Installing dependencies...")
        try:
            self.cmd_discovery.run_subprocess('npm', ['install'], self.config.temp_dir, check=True)
        except (CommandNotFoundError, subprocess.CalledProcessError) as e:
            error = f"ERROR: Could not install dependencies: {e}"
            return error, error, [error], set()

        # Run TypeScript check
        ts_output, ts_errors, ts_failing = self.run_typescript_check()

        # Run JavaScript check
        js_output, js_errors, js_failing = self.check_javascript_syntax()

        # Combine results
        all_errors = ts_errors + js_errors
        all_failing = ts_failing | js_failing

        return ts_output, js_output, all_errors, all_failing
