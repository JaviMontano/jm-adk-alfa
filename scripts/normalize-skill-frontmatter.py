#!/usr/bin/env python3
"""Normalize legacy SKILL.md frontmatter without rewriting bodies."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


DEFAULT_ALLOWED_TOOLS = ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
CANONICAL_TOOLS = {
    "Bash",
    "Edit",
    "Glob",
    "Grep",
    "MultiEdit",
    "NotebookEdit",
    "Read",
    "Task",
    "TodoWrite",
    "WebFetch",
    "WebSearch",
    "Write",
}
TOOL_ALIASES = {"Agent": "Task"}
MCP_TOOL_RE = re.compile(r"^mcp__[A-Za-z0-9_-]+__[A-Za-z0-9_-]+$")


def repo_root() -> Path:
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, text=True, stdout=subprocess.PIPE)
    return Path(result.stdout.strip())


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def has_field(fm: str, field: str) -> bool:
    return re.search(rf"^{re.escape(field)}:", fm, flags=re.MULTILINE) is not None


def is_frontmatter_key(line: str) -> bool:
    return bool(line and not line.startswith((" ", "\t", "-")) and re.match(r"^[A-Za-z0-9_-]+:", line))


def normalize_tool(raw: str) -> str | None:
    tool = raw.strip().strip("\"'")
    tool = re.sub(r"\s*\[EXPLICIT\]\s*$", "", tool).strip()
    if not tool or tool == "EXPLICIT":
        return None
    tool = TOOL_ALIASES.get(tool, tool)
    if tool in CANONICAL_TOOLS or MCP_TOOL_RE.match(tool):
        return tool
    return tool


def parse_allowed_tools(lines: list[str]) -> tuple[list[str], int | None, int | None]:
    tools: list[str] = []
    start: int | None = None
    end: int | None = None
    for index, line in enumerate(lines):
        if re.match(r"^allowed[-_]tools:", line):
            start = index
            _, _, value = line.partition(":")
            value = value.strip()
            if value:
                if value.startswith("[") and value.endswith("]"):
                    values = value[1:-1].split(",")
                else:
                    values = value.split(",")
                tools.extend(part.strip() for part in values if part.strip())
            end = index + 1
            while end < len(lines) and not is_frontmatter_key(lines[end]):
                item = lines[end].strip()
                if item.startswith("- "):
                    tools.append(item[2:].strip())
                end += 1
            break
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in tools:
        tool = normalize_tool(raw)
        if tool and tool not in seen:
            normalized.append(tool)
            seen.add(tool)
    if not normalized:
        normalized = DEFAULT_ALLOWED_TOOLS.copy()
    return normalized, start, end


def apply_allowed_tools(lines: list[str]) -> list[str]:
    tools, start, end = parse_allowed_tools(lines)
    block = ["allowed-tools:"] + [f"  - {tool}" for tool in tools]
    if start is not None and end is not None:
        return lines[:start] + block + lines[end:]
    return lines + block


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

    lines = apply_allowed_tools(lines)

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
