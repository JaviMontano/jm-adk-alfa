#!/usr/bin/env python3
"""Validate homologated runtime instruction files without modifying the repo."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PRIMARY_MIRRORS = {
    "CLAUDE.md": ["Claude Desktop", "Claude Code", "Claude Cowork"],
    "GEMINI.md": ["Gemini CLI", "Antigravity"],
    "AGENTS.md": ["Codex", "Visual Studio"],
}

BRIDGE_FILES = {
    "ANTIGRAVITY.md": ["GEMINI.md", "Antigravity", "diagnose-user-context.py --dry-run", "user-context/.jm-adk-context.json"],
    ".agent/rules/GEMINI.md": ["GEMINI.md", "Antigravity", "diagnose-personal-skills.py --dry-run"],
    ".github/copilot-instructions.md": ["AGENTS.md", "Visual Studio", "diagnose-personal-skills.py --dry-run"],
    ".cursorrules": ["Runtime Context Contract", "user-context/.jm-adk-context.json", "user-context/personal-skills/skills/"],
    ".windsurfrules": ["Runtime Context Contract", "user-context/.jm-adk-context.json", "user-context/personal-skills/skills/"],
}

COMMON_RUNTIME_TOKENS = [
    "Runtime Context Contract",
    "diagnose-first-use.py --dry-run",
    "diagnose-user-context.py --dry-run",
    "diagnose-personal-skills.py --dry-run",
    "user-context/.jm-adk-context.json",
    "jm-adk-user-context",
    "user-context/_INDICE.md",
    "user-context/sources/",
    "user-context/resources/",
    "user-context/personal-skills/skills/",
    "scaffold-skill.py --personal",
    "sync-personal-skills.py --dry-run",
    ".local/skills/",
    "workspace/{active}/artifacts/",
    ".jm-adk.local.json",
    ".env*",
    "private `user-context/` content",
    "Constitution v6.0.0",
]

PRIMARY_SECTIONS = [
    "Runtime Context Contract",
    "Input Tolerance",
    "Triad Pattern",
    "Request Classification",
    "Core Rules",
    "Quality Gates",
]

ACTIVE_DOCS = [
    "CLAUDE.md",
    "GEMINI.md",
    "AGENTS.md",
    "CODEX.md",
    "ANTIGRAVITY.md",
    "PRISTINO.md",
    "ARCHITECTURE.md",
    ".agent/rules/GEMINI.md",
    ".agent/ARCHITECTURE.md",
    ".github/copilot-instructions.md",
    ".cursorrules",
    ".windsurfrules",
    "references/ontology/environment-protocol.md",
    "references/ontology/user-context-contract.md",
]


def read(rel: str, errors: list[str]) -> str:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing runtime file: {rel}")
        return ""
    return path.read_text(encoding="utf-8")


def require_tokens(rel: str, text: str, tokens: list[str], errors: list[str]) -> None:
    for token in tokens:
        if token not in text:
            errors.append(f"{rel}: missing token {token!r}")


def main() -> int:
    errors: list[str] = []

    for rel, family_tokens in PRIMARY_MIRRORS.items():
        text = read(rel, errors)
        require_tokens(rel, text, COMMON_RUNTIME_TOKENS + PRIMARY_SECTIONS + family_tokens, errors)

    for rel, bridge_tokens in BRIDGE_FILES.items():
        text = read(rel, errors)
        require_tokens(rel, text, bridge_tokens + ["diagnose-user-context.py --dry-run"], errors)

    codex = read("CODEX.md", errors)
    require_tokens(
        "CODEX.md",
        codex,
        [
            "AGENTS.md",
            "Codex",
            "Visual Studio",
            "diagnose-user-context.py --dry-run",
            "diagnose-personal-skills.py --dry-run",
            "user-context/.jm-adk-context.json",
            "user-context/personal-skills/skills/",
        ],
        errors,
    )

    for rel in ACTIVE_DOCS:
        text = read(rel, errors)
        if "constitution-v5.2.0" in text:
            errors.append(f"{rel}: stale constitution-v5.2.0 reference")

    env = read("references/ontology/environment-protocol.md", errors)
    require_tokens(
        "references/ontology/environment-protocol.md",
        env,
        ["CLAUDE.md", "GEMINI.md", "AGENTS.md", "Claude Desktop", "Gemini CLI", "Visual Studio", "validation pending"],
        errors,
    )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("runtime instructions: passed")
    print("primary mirrors: CLAUDE.md, GEMINI.md, AGENTS.md")
    print("bridges: antigravity, copilot, cursor, windsurf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
