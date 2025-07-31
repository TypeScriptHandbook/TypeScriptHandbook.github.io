"""
Utility functions for command discovery and subprocess management
"""

import subprocess
from pathlib import Path

from models import CommandNotFoundError


class CommandDiscovery:
    """Handles discovery and caching of npm/npx/node commands"""

    def __init__(self) -> None:
        self._npm_cmd: str | None = None
        self._npx_cmd: str | None = None
        self._node_cmd: str | None = None

    def discover_commands(self) -> bool:
        """Discover and cache npm, npx, and node commands"""
        if (self._npm_cmd is not None and
            self._npx_cmd is not None and
            self._node_cmd is not None):
            return True

        npm_variants = ['npm', 'npm.cmd', 'npm.exe']
        npx_variants = ['npx', 'npx.cmd', 'npx.exe']
        node_variants = ['node', 'node.cmd', 'node.exe']

        self._npm_cmd = self._find_working_command(npm_variants)
        self._npx_cmd = self._find_working_command(npx_variants)
        self._node_cmd = self._find_working_command(node_variants)

        missing_commands = []
        if self._npm_cmd is None:
            missing_commands.append('npm')
        if self._npx_cmd is None:
            missing_commands.append('npx')
        if self._node_cmd is None:
            missing_commands.append('node')

        if missing_commands:
            print(f"❌ Missing commands: {', '.join(missing_commands)}")
            print("Please ensure Node.js and npm are properly installed.")
            return False

        print(f"🔧 Using npm: {self._npm_cmd}, npx: {self._npx_cmd}, node: {self._node_cmd}")
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

    def run_subprocess(self, cmd_type: str, args: list[str], temp_dir: Path, **kwargs) -> subprocess.CompletedProcess[str]:
        """Run subprocess with guaranteed non-None command"""
        if not self.discover_commands():
            raise CommandNotFoundError("Could not discover npm/npx/node commands")

        if cmd_type == 'npm':
            command = self._npm_cmd
        elif cmd_type == 'npx':
            command = self._npx_cmd
        elif cmd_type == 'node':
            command = self._node_cmd
        else:
            raise ValueError(f"Unknown command type: {cmd_type}")

        assert command is not None  # Guaranteed by discover_commands success

        return subprocess.run([command] + args,
                              cwd=temp_dir,
                              capture_output=True,
                              text=True,
                              shell=True,
                              **kwargs)
