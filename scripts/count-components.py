#!/usr/bin/env python3
"""Count JM-ADK components and optionally verify documented counts."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


DOCS_TO_CHECK = [
    "README.md",
    "AGENTS.md",
    "ARCHITECTURE.md",
    "PRISTINO.md",
    "PRISTINO-INDEX.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".claude-plugin/plugin.json",
    ".jm-adk.json",
]


def repo_root() -> Path:
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, text=True, stdout=subprocess.PIPE)
    return Path(result.stdout.strip())


def counts(root: Path) -> dict[str, int]:
    return {
        "skills": len(list(root.glob("skills/*/SKILL.md"))),
        "agents": len(list(root.glob("agents/*.md"))),
        "commands": len(list(root.glob("commands/*.md"))),
        "prompts": len([p for p in root.glob("prompts/*/*.md") if ".catalog" not in p.parts]),
    }


def print_counts(values: dict[str, int]) -> None:
    for key in ["skills", "agents", "commands", "prompts"]:
        print(f"{key}={values[key]}")
    print(f"components={sum(values.values())}")


def check_docs(root: Path, values: dict[str, int]) -> list[str]:
    errors: list[str] = []
    expected = {
        "skills": values["skills"],
        "agents": values["agents"],
        "commands": values["commands"],
        "prompts": values["prompts"],
    }
    patterns = {
        "skills": [r"(\d+)\s+skills?", r"(\d+)_skills"],
        "agents": [r"(\d+)\s+agents?", r"(\d+)\s+agentes"],
        "commands": [r"(\d+)\s+commands?", r"(\d+)\s+comandos"],
        "prompts": [r"(\d+)\s+prompts?"],
    }
    for rel in DOCS_TO_CHECK:
        path = root / rel
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for key, regexes in patterns.items():
            for regex in regexes:
                for line in lines:
                    lower = line.lower()
                    if "max " in lower or "maximum" in lower:
                        continue
                    for match in re.finditer(regex, line, flags=re.IGNORECASE):
                        found = int(match.group(1))
                        if found != expected[key]:
                            errors.append(f"{rel}: {key} count {found} != {expected[key]}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Count JM-ADK components")
    parser.add_argument("--check-docs", action="store_true", help="Fail when documented counts drift")
    args = parser.parse_args()
    root = repo_root()
    values = counts(root)
    print_counts(values)
    if not args.check_docs:
        return 0
    errors = check_docs(root, values)
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
