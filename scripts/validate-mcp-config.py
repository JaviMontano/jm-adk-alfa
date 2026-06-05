#!/usr/bin/env python3
"""Validate MCP / tool-access wiring without modifying the repo.

Checks the canonical .mcp.json, the per-runtime access matrix, and the
generated templates stay coherent and secret-free. Read-only.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = "workspace-mcp"
EXPECTED_SERVICES = ["gmail", "drive", "calendar", "docs", "sheets", "slides"]
MATRIX = "docs/runtime-tool-access-matrix.md"
MATRIX_RUNTIMES = [
    "Claude Code", "Claude Desktop", "OpenAI Codex", "Gemini CLI",
    "Antigravity", "Cursor", "Windsurf", "VS Code",
]
TEMPLATES = [
    "references/mcp/codex.config.toml.example",
    "references/mcp/gemini.settings.json.example",
    "references/mcp/antigravity.mcp_config.json.example",
    "references/mcp/claude_desktop_config.json.example",
    "references/mcp/cursor.mcp.json.example",
    "references/mcp/windsurf.mcp_config.json.example",
    "references/mcp/vscode.mcp.json.example",
]
SECRET_PATTERNS = [
    re.compile(r"\bya29\.[A-Za-z0-9_\-]+"),
    re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    re.compile(r"(?i)(secret|password|private[_-]?key)\s*[:=]\s*[\"']?[^\s\"']{8,}"),
]


def has_literal_secret(text: str) -> bool:
    for pattern in SECRET_PATTERNS:
        for m in pattern.finditer(text):
            if "${" not in m.group(0):
                return True
    return False


def main() -> int:
    errors: list[str] = []

    # 1. Canonical .mcp.json
    mcp_path = ROOT / ".mcp.json"
    if not mcp_path.exists():
        print("ERROR: .mcp.json missing")
        return 1
    raw = mcp_path.read_text(encoding="utf-8")
    try:
        mcp = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"ERROR: .mcp.json invalid JSON: {exc}")
        return 1

    servers = mcp.get("mcpServers", {})
    if SERVER not in servers:
        errors.append(f".mcp.json: server {SERVER!r} not defined")
    else:
        srv = servers[SERVER]
        blob = json.dumps(srv)
        if has_literal_secret(blob):
            errors.append(".mcp.json: literal secret detected (use ${ENV} placeholder)")
        if "${" not in json.dumps(srv.get("env", {})):
            errors.append(".mcp.json: env should reference ${ENV} placeholders, not literals")
        args_blob = " ".join(srv.get("args", []))
        for svc in EXPECTED_SERVICES:
            if svc not in args_blob:
                errors.append(f".mcp.json: expected service {svc!r} not in args")

    # 2. Access matrix present + names every runtime
    matrix_path = ROOT / MATRIX
    if not matrix_path.exists():
        errors.append(f"missing {MATRIX}")
    else:
        mtext = matrix_path.read_text(encoding="utf-8")
        for rt in MATRIX_RUNTIMES:
            if rt not in mtext:
                errors.append(f"{MATRIX}: runtime {rt!r} not documented")

    # 3. Templates exist + secret-free
    for rel in TEMPLATES:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing template {rel} (run scripts/generate-mcp-configs.py --apply)")
            continue
        if has_literal_secret(p.read_text(encoding="utf-8")):
            errors.append(f"{rel}: literal secret detected")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("mcp config: passed")
    print(f"server: {SERVER} ({len(EXPECTED_SERVICES)}+ services, env-var auth)")
    print(f"runtimes documented: {len(MATRIX_RUNTIMES)} | templates: {len(TEMPLATES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
