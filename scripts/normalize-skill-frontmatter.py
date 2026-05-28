#!/usr/bin/env python3
"""Normalize legacy SKILL.md frontmatter without rewriting bodies."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


def repo_root() -> Path:
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, text=True, stdout=subprocess.PIPE)
    return Path(result.stdout.strip())


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def has_field(fm: str, field: str) -> bool:
    return re.search(rf"^{re.escape(field)}:", fm, flags=re.MULTILINE) is not None


def normalize_file(path: Path, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    normalized = re.sub(r"^---\s+\[EXPLICIT\]\s*$", "---", text, flags=re.MULTILINE)
    match = re.match(r"^---\s*\n(.*?)\n---", normalized, re.DOTALL)
    slug = path.parent.name

    if match:
        fm = match.group(1)
        body = normalized[match.end() :]
        lines = fm.splitlines()
    else:
        lines = []
        body = "\n" + normalized.lstrip("\n")

    existing_fm = "\n".join(lines)
    additions: list[str] = []
    if not has_field(existing_fm, "name"):
        additions.append(f"name: {slug}")
    if not has_field(existing_fm, "version"):
        additions.append("version: 1.0.0")
    if not has_field(existing_fm, "description"):
        additions.append(f'description: "Skill for {title_from_slug(slug)}."')

    if additions:
        insert_at = 1 if lines and lines[0].startswith("name:") else 0
        lines[insert_at:insert_at] = additions

    new_text = "---\n" + "\n".join(lines).rstrip() + "\n---" + body
    if new_text == text:
        return False
    print(f"normalize: {path}")
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize SKILL.md frontmatter")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = repo_root()
    count = 0
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        if normalize_file(path, args.dry_run):
            count += 1
    mode = "dry-run" if args.dry_run else "applied"
    print(f"{mode}: normalized={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
