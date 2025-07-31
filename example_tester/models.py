"""
Data models for the TypeScript Example Tester
"""

from dataclasses import dataclass
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
            # Use current working directory (where the command is run from) instead of script location
            temp_path = Path.cwd() / "test"
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
