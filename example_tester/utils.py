"""
Utility functions for command discovery and subprocess management
"""

import subprocess
from pathlib import Path

from models import CommandNotFoundError


class CommandDiscovery:
    """Handles discovery and caching of npm/npx commands"""

    def __init__(self) -> None:
        self._npm_cmd: str | None = None
        self._npx_cmd: str | None = None

    def discover_commands(self) -> bool:
        """Discover and cache npm and npx commands"""
        if self._npm_cmd is not None and self._npx_cmd is not None:
            return True

        npm_variants = ['npm', 'npm.cmd', 'npm.exe']
        npx_variants = ['npx', 'npx.cmd', 'npx.exe']

        self._npm_cmd = self._find_working_command(npm_variants)
        self._npx_cmd = self._find_working_command(npx_variants)

        if self._npm_cmd is None:
            print("❌ npm not found. Please ensure Node.js and npm are properly installed.")
            return False

        if self._npx_cmd is None:
            print("❌ npx not found. Please ensure Node.js and npm are properly installed.")
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

    def run_subprocess(self, cmd_type: str, args: list[str], temp_dir: Path, **kwargs) -> subprocess.CompletedProcess[
        str]:
        """Run subprocess with guaranteed non-None command"""
        if not self.discover_commands():
            raise CommandNotFoundError("Could not discover npm/npx commands")

        command = self._npm_cmd if cmd_type == 'npm' else self._npx_cmd
        assert command is not None  # Guaranteed by discover_commands success

        return subprocess.run([command] + args,
                              cwd=temp_dir,
                              capture_output=True,
                              text=True,
                              shell=True,
                              **kwargs)
