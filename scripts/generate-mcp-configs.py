#!/usr/bin/env python3
"""Generate per-runtime MCP config templates from the canonical .mcp.json.

Reads the single source of truth (.mcp.json, Claude project scope) and emits
paste-ready, secret-free config snippets for every supported runtime into
references/mcp/. Env-var placeholders are preserved verbatim; literal secrets
abort the run.

Default is dry-run (prints what would be written). Use --apply to write files.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

GENERATOR = "scripts/generate-mcp-configs.py"
SERVER = "workspace-mcp"

# A literal secret would match these; ${ENV} placeholders never do.
SECRET_PATTERNS = [
    re.compile(r"\bya29\.[A-Za-z0-9_\-]+"),          # Google OAuth access token
    re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),        # Google API key
    re.compile(r"\b[A-Za-z0-9_\-]{40,}\b"),           # long opaque blob
    re.compile(r"(?i)(secret|password|private[_-]?key)\s*[:=]\s*[\"']?[^\s\"']{8,}"),
]


def repo_root(start: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip())
    return start.resolve()


def scan_secret(name: str, text: str) -> list[str]:
    findings = []
    for pattern in SECRET_PATTERNS:
        # Ignore matches that are purely an ${ENV} placeholder span.
        for m in pattern.finditer(text):
            span = m.group(0)
            if "${" in span:
                continue
            findings.append(f"{name}: secret-like token {span[:12]}...")
            break
    return findings


def load_server(root: Path) -> dict:
    mcp = json.loads((root / ".mcp.json").read_text(encoding="utf-8"))
    servers = mcp.get("mcpServers", {})
    if SERVER not in servers:
        raise SystemExit(f"ERROR: {SERVER!r} not found in .mcp.json")
    return servers[SERVER]


def toml_array(items: list[str]) -> str:
    return "[" + ", ".join(json.dumps(i) for i in items) + "]"


def render_codex(srv: dict) -> str:
    env_lines = "\n".join(f'{k} = {json.dumps(v)}' for k, v in srv.get("env", {}).items())
    return (
        "# OpenAI Codex CLI — ~/.codex/config.toml (or project .codex/config.toml)\n"
        "# Wire with: codex mcp add workspace-mcp -- uvx workspace-mcp\n\n"
        f"[mcp_servers.{SERVER}]\n"
        f'command = {json.dumps(srv["command"])}\n'
        f"args = {toml_array(srv.get('args', []))}\n"
        f"startup_timeout_sec = 30\n"
        f"default_tools_approval_mode = \"prompt\"\n\n"
        f"[mcp_servers.{SERVER}.env]\n"
        f"{env_lines}\n"
    )


def render_json_block(srv: dict, top_key: str) -> str:
    block = {top_key: {SERVER: {
        "command": srv["command"],
        "args": srv.get("args", []),
        "env": srv.get("env", {}),
    }}}
    return json.dumps(block, indent=2, ensure_ascii=False) + "\n"


def render_vscode(srv: dict) -> str:
    # VS Code uses "servers" and a "type" discriminator.
    block = {"servers": {SERVER: {
        "type": "stdio",
        "command": srv["command"],
        "args": srv.get("args", []),
        "env": srv.get("env", {}),
    }}}
    return json.dumps(block, indent=2, ensure_ascii=False) + "\n"


def build(srv: dict) -> dict[str, str]:
    return {
        "codex.config.toml.example": render_codex(srv),
        "gemini.settings.json.example": render_json_block(srv, "mcpServers"),
        "antigravity.mcp_config.json.example": render_json_block(srv, "mcpServers"),
        "claude_desktop_config.json.example": render_json_block(srv, "mcpServers"),
        "cursor.mcp.json.example": render_json_block(srv, "mcpServers"),
        "windsurf.mcp_config.json.example": render_json_block(srv, "mcpServers"),
        "vscode.mcp.json.example": render_vscode(srv),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate per-runtime MCP config templates")
    parser.add_argument("--root", default=".")
    parser.add_argument("--apply", action="store_true", help="Write files to references/mcp/")
    parser.add_argument("--dry-run", action="store_true", help="Show planned output (default)")
    args = parser.parse_args()

    root = repo_root(Path(args.root))
    srv = load_server(root)
    files = build(srv)

    # Secret gate across all rendered outputs.
    findings: list[str] = []
    for name, text in files.items():
        findings += scan_secret(name, text)
    if findings:
        print("ERROR: secret-like content detected; refusing to emit templates.")
        for f in findings:
            print(f"  {f}")
        return 2

    out_dir = root / "references" / "mcp"
    if not args.apply:
        print(f"DRY-RUN: would write {len(files)} templates to {out_dir}")
        for name in files:
            print(f"  {out_dir.relative_to(root)}/{name}")
        return 0

    out_dir.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (out_dir / name).write_text(text, encoding="utf-8")
        print(f"WROTE: references/mcp/{name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
