from pathlib import Path
import re
import argparse
from dataclasses import dataclass

@dataclass
class NumberedFile:
    path: Path
    base: int
    suffix: str

def shift_files_forward(directory: Path, force: bool) -> None:
    """
    Increment the base number of files with the pattern N_suffix.md by 1.
    Operates from highest to lowest base number to avoid collisions.
    If `force` is False, just prints what it would do.
    """
    files: list[NumberedFile] = []

    pattern = re.compile(r"^(\d+)_(.+)\.md$")

    for file in directory.iterdir():
        if match := pattern.match(file.name):
            base = int(match.group(1))
            suffix = match.group(2)
            files.append(NumberedFile(file, base, suffix))

    for f in sorted(files, key=lambda nf: nf.base, reverse=True):
        new_name = f"{f.base + 1}_{f.suffix}.md"
        new_path = f.path.with_name(new_name)
        if force:
            f.path.rename(new_path)
            print(f"Renamed {f.path.name} → {new_path.name}")
        else:
            print(f"Would rename {f.path.name} → {new_path.name}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Shift base numbers in N_suffix.md files forward by 1.")
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Perform the renaming (without this flag, just show what would happen)"
    )
    parser.add_argument(
        "-d", "--directory",
        type=Path,
        default=Path("."),
        help="Target directory (default: current directory)"
    )

    args = parser.parse_args()
    shift_files_forward(args.directory, args.force)

if __name__ == "__main__":
    main()
