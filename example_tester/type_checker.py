"""
TypeScript type checking functionality
"""

import subprocess

from models import CommandNotFoundError, TestConfig
from utils import CommandDiscovery


class TypeChecker:
    """Handles TypeScript compilation and error parsing"""

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

    def run_type_check(self) -> tuple[str, list[str], set[str]]:
        """Run TypeScript compiler and return (full_output, error_summary, failing_files)"""
        print("Installing TypeScript dependencies...")
        try:
            self.cmd_discovery.run_subprocess('npm', ['install'], self.config.temp_dir, check=True)
        except (CommandNotFoundError, subprocess.CalledProcessError) as e:
            error = f"ERROR: Could not install TypeScript dependencies: {e}"
            return error, [error], set()

        print("Running type check...")
        try:
            result = self.cmd_discovery.run_subprocess('npx', ['tsc'], self.config.temp_dir)
            if result.returncode == 0:
                return "✅ All examples type check successfully!", [], set()
            else:
                full_output = f"❌ Type checking failed:\n{result.stdout}"
                if result.stderr:
                    full_output += f"\n{result.stderr}"

                error_summary, failing_files = self.parse_typescript_errors(result.stdout)
                if not error_summary:
                    error_summary = ["Type checking failed - see test_all.txt for details"]

                return full_output, error_summary, failing_files

        except CommandNotFoundError as e:
            error = f"ERROR: {e}"
            return error, [error], set()
