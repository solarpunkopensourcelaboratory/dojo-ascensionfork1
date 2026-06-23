#!/usr/bin/env python3
"""Create a plain-text bundle of the repository contents for AI collaborators."""

from __future__ import annotations

from pathlib import Path
import sys

IGNORE_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}
IGNORE_FILES = {".DS_Store", "Thumbs.db"}


def iter_repo_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        parts = rel.parts
        if any(part in IGNORE_DIRS for part in parts[:-1]):
            continue
        if any(part in IGNORE_DIRS for part in parts):
            continue
        if rel.parts and rel.parts[0] in IGNORE_DIRS:
            continue
        if path.name in IGNORE_FILES:
            continue
        yield path


def generate_repo_text_bundle(root: Path, output_path: Path) -> Path:
    root = root.resolve()
    output_path = output_path.resolve()

    lines = []
    for path in iter_repo_files(root):
        rel = path.relative_to(root)
        lines.append(f"===== {rel} =====")
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = "<binary or non-utf8 content>"
        lines.append(content.rstrip())
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    output_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else root / "repo_bundle.txt"
    generate_repo_text_bundle(root, output_path)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    main()
