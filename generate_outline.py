"""
Generates a Markdown outline from all `.md` files in a specified directory,
using the chapter number and title as the top-level bullet, and nested bullets
for all subheadings.
"""

from pathlib import Path
from argparse import ArgumentParser
from typing import Iterator, Optional

def extract_headers(md_text: str) -> list[str]:
    return [line.strip() for line in md_text.splitlines() if line.lstrip().startswith("#")]

def extract_title(headers: list[str]) -> Optional[str]:
    for header in headers:
        if header.startswith("# "):
            return header.lstrip("#").strip()
    return None

def generate_outline(directory: Path) -> str:
    outline_lines: list[str] = []

    for md_file in sorted(directory.glob("*.md")):
        raw_stem = md_file.stem  # "00", "01", etc.
        chapter_num = raw_stem.lstrip("0") or "0"
        if chapter_num == "0":
            continue

        headers = extract_headers(md_file.read_text(encoding="utf-8"))
        title = extract_title(headers) or "(untitled)"
        outline_lines.append(f"\n### Chapter {chapter_num}: {title}\n")

        for header in headers:
            if header.startswith("# "):
                continue  # already used as title
            level = header.count("#")
            heading_text = header.lstrip("#").strip()
            level = level - 2
            indent = "  " * level
            outline_lines.append(f"{indent}- {heading_text}")

    return "\n".join(outline_lines)

def update_preface(preface_path: Path, outline: str) -> None:
    content = preface_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    try:
        index = next(i for i, line in enumerate(lines) if line.strip() == "## Outline")
    except StopIteration:
        raise ValueError("Could not find '## Outline' in preface file")

    new_content = "\n".join(lines[:index + 1]) + "\n" + outline + "\n"
    preface_path.write_text(new_content, encoding="utf-8")

def main() -> None:
    parser = ArgumentParser(description="Generate a Markdown outline from headers in .md files")
    parser.add_argument("-d", "--directory", type=Path, required=True, help="Path to directory containing .md files")
    parser.add_argument("-p", "--preface", action="store_true", help="Update 00.md after '## Outline' with the generated outline")
    args = parser.parse_args()

    if not args.directory.is_dir():
        raise ValueError(f"{args.directory} is not a directory")

    outline = generate_outline(args.directory)
    print(outline)

    if args.preface:
        preface_path = args.directory / "00.md"
        if not preface_path.exists():
            raise FileNotFoundError("00.md not found in the specified directory")
        update_preface(preface_path, outline)

if __name__ == "__main__":
    main()
