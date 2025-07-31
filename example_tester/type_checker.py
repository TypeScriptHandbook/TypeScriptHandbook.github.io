"""
TypeScript and JavaScript checking functionality
"""

import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from collections.abc import Callable

from models import CommandNotFoundError, TestConfig
from utils import CommandDiscovery


class TypeChecker:
    """
    Handles TypeScript compilation and JavaScript syntax checking.
    This class provides methods to check TypeScript and JavaScript files in parallel,
    parsing output for errors, and reporting results in a unified way.
    """

    def __init__(self, config: TestConfig, command_discovery: CommandDiscovery) -> None:
        self.config = config
        self.cmd_discovery = command_discovery

    def parse_typescript_errors(self, output: str) -> tuple[list[str], set[str]]:
        """Parse TypeScript compiler output to extract error summaries and failing files."""
        error_lines: list[str] = []
        failing_files: set[str] = set()

        for line in output.split('\n'):
            line = line.strip()
            if line and ': error TS' in line:
                try:
                    file_part = line.split('(')[0] if '(' in line else line.split(':')[0]
                    if file_part:
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
                    error_lines.append(line)
        return error_lines, failing_files

    def parse_javascript_errors(self, output: str, js_files: list[Path]) -> tuple[list[str], set[str]]:
        """Parse Node.js syntax check output for JavaScript files."""
        error_lines: list[str] = []
        failing_files: set[str] = set()
        sections = output.split('\n\n')
        for section in sections:
            if not section.strip():
                continue
            lines = section.strip().split('\n')
            if not lines:
                continue
            for line in lines:
                if ('SyntaxError:' in line or 'ReferenceError:' in line or
                    'TypeError:' in line or 'Error:' in line):
                    for js_file in js_files:
                        file_str = str(js_file.relative_to(self.config.temp_dir)).replace('\\', '/')
                        if file_str in section or js_file.name in section:
                            failing_files.add(file_str)
                            error_lines.append(f"JS Error in {js_file.name}: {line.strip()}")
                            break
                    else:
                        error_lines.append(f"JS Error: {line.strip()}")
        return error_lines, failing_files

    def find_javascript_files(self) -> list[Path]:
        """Find JavaScript files in chapter directories only (exclude node_modules)."""
        js_files: list[Path] = []
        try:
            for item in self.config.temp_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.') and item.name != 'node_modules':
                    js_files.extend(item.glob("*.js"))
        except OSError:
            pass
        return js_files

    def check_single_javascript_file(self, js_file: Path) -> tuple[str, list[str], str]:
        """Check a single JavaScript file and return results."""
        try:
            result = self.cmd_discovery.run_subprocess(
                'node',
                ['--check', str(js_file.relative_to(self.config.temp_dir))],
                self.config.temp_dir
            )
            file_output = f"Checking {js_file.name}:"
            relative_path = str(js_file.relative_to(self.config.temp_dir)).replace('\\', '/')
            if result.returncode == 0:
                file_output += " ✅ OK"
                return file_output, [], ""
            else:
                file_output += f" ❌ FAILED\n{result.stderr}"
                error_msg = f"JS Syntax Error in {js_file.name}: {result.stderr.strip()}"
                return file_output, [error_msg], relative_path
        except (CommandNotFoundError, subprocess.CalledProcessError) as e:
            error_msg = f"Error checking {js_file.name}: {e}"
            relative_path = str(js_file.relative_to(self.config.temp_dir)).replace('\\', '/')
            return error_msg, [error_msg], relative_path

    def check_single_typescript_file(self, ts_file: Path) -> tuple[str, list[str], str]:
        """Check a single TypeScript file and return results."""
        try:
            result = self.cmd_discovery.run_subprocess(
                'npx',
                ['tsc', '--noEmit', '--strict', str(ts_file.relative_to(self.config.temp_dir))],
                self.config.temp_dir
            )
            file_output = f"Checking {ts_file.name}:"
            relative_path = str(ts_file.relative_to(self.config.temp_dir)).replace('\\', '/')
            if result.returncode == 0:
                file_output += " ✅ OK"
                return file_output, [], ""
            else:
                file_output += f" ❌ FAILED\n{result.stdout}"
                file_errors, _ = self.parse_typescript_errors(result.stdout)
                return file_output, file_errors, relative_path
        except (CommandNotFoundError, subprocess.CalledProcessError) as e:
            error_msg = f"Error checking {ts_file.name}: {e}"
            relative_path = str(ts_file.relative_to(self.config.temp_dir)).replace('\\', '/')
            return error_msg, [error_msg], relative_path

    def _parallel_file_check(
        self,
        files: list[Path],
        single_file_checker: Callable[[Path], tuple[str, list[str], str]],
        file_type: str,
    ) -> tuple[str, list[str], set[str]]:
        """
        Checks files in parallel using the provided single_file_checker.
        Returns formatted output, error strings, and set of failing files.
        """
        if not files:
            return f"✅ No {file_type} files to check", [], set()

        print(f"Checking {len(files)} {file_type} files in parallel...")
        all_output: list[str] = []
        all_errors: list[str] = []
        all_failing_files: set[str] = set()
        max_workers = min(len(files), os.cpu_count() or 4)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(single_file_checker, file): file
                for file in files
            }
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    file_output, file_errors, failing_path = future.result()
                    all_output.append(file_output)
                    all_errors.extend(file_errors)
                    if failing_path:
                        all_failing_files.add(failing_path)
                except Exception as e:
                    error_msg = f"Error processing {file.name}: {e}"
                    all_output.append(error_msg)
                    all_errors.append(error_msg)
        all_output.sort(key=lambda x: x.split(':')[0] if ':' in x else x)
        full_output = '\n\n'.join(all_output)
        if not all_errors:
            return (
                f"✅ All {len(files)} {file_type} files passed "
                f"{'syntax check' if file_type == 'JavaScript' else 'type checking'}!\n\n{full_output}",
                [],
                set(),
            )
        else:
            return (
                f"❌ {file_type} "
                f"{'syntax check' if file_type == 'JavaScript' else 'checking'} failed:\n\n{full_output}",
                all_errors,
                all_failing_files,
            )

    def check_javascript_syntax(self) -> tuple[str, list[str], set[str]]:
        """Check JavaScript files for syntax errors using Node.js with parallel processing."""
        js_files = self.find_javascript_files()
        return self._parallel_file_check(
            js_files,
            self.check_single_javascript_file,
            "JavaScript"
        )

    def run_typescript_check(self) -> tuple[str, list[str], set[str]]:
        """Run TypeScript compiler on .ts files individually using parallel processing."""
        print("Running TypeScript check...")
        ts_files: list[Path] = []
        try:
            for item in self.config.temp_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.') and item.name != 'node_modules':
                    ts_files.extend(item.glob("*.ts"))
        except OSError:
            pass
        return self._parallel_file_check(
            ts_files,
            self.check_single_typescript_file,
            "TypeScript"
        )

    def run_checks(self) -> tuple[str, str, list[str], set[str]]:
        """Run both TypeScript and JavaScript checks and return combined results."""
        print("Installing dependencies...")
        try:
            self.cmd_discovery.run_subprocess('npm', ['install'], self.config.temp_dir, check=True)
        except (CommandNotFoundError, subprocess.CalledProcessError) as e:
            error = f"ERROR: Could not install dependencies: {e}"
            return error, error, [error], set()
        ts_output, ts_errors, ts_failing = self.run_typescript_check()
        js_output, js_errors, js_failing = self.check_javascript_syntax()
        all_errors = ts_errors + js_errors
        all_failing = ts_failing | js_failing
        return ts_output, js_output, all_errors, all_failing
