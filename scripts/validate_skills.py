#!/usr/bin/env python3
"""Validate root-level skill metadata and the README skill index."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
FRONTMATTER_DELIMITER = "---"
KEBAB_CASE_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LEGACY_NAMES = {"fashion_model_conversion", "seedance_video"}
NON_SKILL_DIRECTORIES = {".git", ".github", ".idea", "scripts", "templates"}
README_SKILL_LINK = re.compile(r"\]\(([^)]+/SKILL\.md)\)")


def read_frontmatter(path: Path) -> dict[str, str]:
    """Read the simple key/value YAML frontmatter used by skills."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIMITER:
        raise ValueError("frontmatter must start with '---'")

    try:
        end = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == FRONTMATTER_DELIMITER
        )
    except StopIteration as exc:
        raise ValueError("frontmatter closing '---' is missing") from exc

    metadata: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"line {line_number}: expected a key/value field")
        key, value = line.split(":", maxsplit=1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        if not key or not value:
            raise ValueError(f"line {line_number}: key and value must be non-empty")
        if key in metadata:
            raise ValueError(f"line {line_number}: duplicate field '{key}'")
        metadata[key] = value

    for required in ("name", "description"):
        if not metadata.get(required, "").strip():
            raise ValueError(f"required field '{required}' is missing or empty")
    return metadata


def validate() -> list[str]:
    errors: list[str] = []
    skills: list[Path] = []
    for directory in sorted(ROOT.iterdir()):
        if not directory.is_dir() or directory.name in NON_SKILL_DIRECTORIES:
            continue
        skill_file = directory / "SKILL.md"
        if skill_file.is_file():
            skills.append(skill_file)
        else:
            errors.append(
                f"root directory '{directory.name}' does not contain a SKILL.md"
            )
    if not skills:
        errors.append("no root-level skill directories containing SKILL.md were found")

    names: dict[str, Path] = {}
    for skill_file in skills:
        directory_name = skill_file.parent.name
        try:
            metadata = read_frontmatter(skill_file)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{skill_file.relative_to(ROOT)}: {exc}")
            continue

        name = metadata["name"]
        if not KEBAB_CASE_NAME.fullmatch(name) and name not in LEGACY_NAMES:
            errors.append(
                f"{skill_file.relative_to(ROOT)}: name '{name}' must use lowercase kebab-case"
            )
        if name != directory_name:
            errors.append(
                f"{skill_file.relative_to(ROOT)}: name '{name}' does not match directory '{directory_name}'"
            )
        if name in names:
            errors.append(
                f"duplicate skill name '{name}' in {names[name].relative_to(ROOT)} and {skill_file.relative_to(ROOT)}"
            )
        else:
            names[name] = skill_file

    if not README.is_file():
        errors.append("README.md is missing")
    else:
        readme = README.read_text(encoding="utf-8")
        linked_paths = set(README_SKILL_LINK.findall(readme))
        linked_skill_paths = {
            path for path in linked_paths if not path.startswith("templates/")
        }
        expected_paths = {f"{skill.parent.name}/SKILL.md" for skill in skills}
        for missing in sorted(expected_paths - linked_skill_paths):
            errors.append(f"README.md is missing a skill index link to {missing}")
        for stale in sorted(linked_skill_paths - expected_paths):
            errors.append(f"README.md contains a stale skill index link to {stale}")
        for linked_path in sorted(linked_paths):
            target = ROOT / linked_path
            if not target.is_file():
                errors.append(f"README.md links to a missing file: {linked_path}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Skill metadata and README index are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
