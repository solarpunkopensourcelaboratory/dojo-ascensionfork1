#!/usr/bin/env python3
"""Convenience wrapper to regenerate the plain-text repo bundle."""

from pathlib import Path
import sys

from repo_text_export import generate_repo_text_bundle


def main() -> int:
    root = Path(__file__).resolve().parent
    output_path = root / "repo_bundle.txt"
    generate_repo_text_bundle(root, output_path)
    print(f"Refreshed {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
