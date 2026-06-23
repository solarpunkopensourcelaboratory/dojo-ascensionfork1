#!/usr/bin/env python3
"""Tiny mission validation helper for contributors."""

import json
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "id",
    "number",
    "title",
    "skill",
    "challenge",
    "answer",
]

FOLDER_SCHEMA_FIELDS = [
    "id",
    "number",
    "title",
    "skill",
    "tag",
    "philosophy",
    "economics",
    "techconcept",
    "lesson",
    "challenge",
    "hint",
    "answer",
    "answertype",
    "honorreward",
    "bonusfirsttry",
]


def describe_fix(errors):
    """Return a short, human-friendly summary of what to fix."""
    if not errors:
        return "No issues found."

    if any("Missing required field" in error for error in errors):
        return "Add the missing required fields and keep the mission schema consistent."
    if any("must be" in error for error in errors):
        return "Check the field types so each value matches the expected format."
    if any("should be named" in error for error in errors):
        return "Rename the file to match the repository's mission naming convention."
    return "Review the listed issues and adjust the mission metadata accordingly."


def validate_path(path):
    """Validate a single mission file or a mission index file."""
    path = Path(path)
    errors = []

    if not path.exists():
        return [f"File not found: {path}"]

    if path.is_dir():
        return [f"Path is a directory, not a file: {path}"]

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Invalid JSON: {exc}"]

    if isinstance(data, dict) and "missions" in data:
        items = data.get("missions", [])
        if not isinstance(items, list):
            return ["'missions' must be a list"]
        records = items
        if path.name != "missions.json":
            errors.append(
                f"Mission index file should be named 'missions.json', found '{path.name}'"
            )
    elif isinstance(data, dict):
        records = [data]
        if path.parent.name == "missions":
            number = data.get("number")
            expected_name = f"mission{int(number):02d}.json" if isinstance(number, int) else ""
            if expected_name and path.name != expected_name:
                errors.append(
                    f"Mission file should be named '{expected_name}', found '{path.name}'"
                )
    else:
        return ["Mission file must contain a JSON object"]

    for index, mission in enumerate(records, 1):
        if not isinstance(mission, dict):
            errors.append(f"Mission #{index} is not an object")
            continue

        required_fields = REQUIRED_FIELDS
        if path.parent.name == "missions" and path.name != "missions.json":
            required_fields = FOLDER_SCHEMA_FIELDS

        for field in required_fields:
            if field not in mission:
                errors.append(
                    f"Mission #{index}: Missing required field '{field}'"
                )

        if "number" in mission and not isinstance(mission["number"], int):
            errors.append(f"Mission #{index}: 'number' must be an integer")

        if "id" in mission and not isinstance(mission["id"], str):
            errors.append(f"Mission #{index}: 'id' must be a string")

        if "title" in mission and not isinstance(mission["title"], str):
            errors.append(f"Mission #{index}: 'title' must be a string")

        if "skill" in mission and not isinstance(mission["skill"], str):
            errors.append(f"Mission #{index}: 'skill' must be a string")

        if "challenge" in mission and not isinstance(mission["challenge"], str):
            errors.append(f"Mission #{index}: 'challenge' must be a string")

        if "answer" in mission:
            if not isinstance(mission["answer"], (str, list)):
                errors.append(f"Mission #{index}: 'answer' must be a string or list")

        if "answertype" in mission and not isinstance(mission["answertype"], str):
            errors.append(f"Mission #{index}: 'answertype' must be a string")

        if "honorreward" in mission and not isinstance(mission["honorreward"], int):
            errors.append(f"Mission #{index}: 'honorreward' must be an integer")

    return errors


def main():
    """CLI entry point for validating mission files."""
    targets = sys.argv[1:]
    if not targets:
        mission_dir = Path("missions")
        targets = [
            str(mission_dir / f"mission{index:02d}.json")
            for index in range(1, 11)
        ] + [str(mission_dir / "missions.json")]

    all_errors = []
    for target in targets:
        errors = validate_path(target)
        if errors:
            print(f"[FAIL] {target}")
            print(f"  What to fix: {describe_fix(errors)}")
            for error in errors:
                print(f"  - {error}")
            all_errors.extend(errors)
        else:
            print(f"[OK] {target}")

    if all_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
