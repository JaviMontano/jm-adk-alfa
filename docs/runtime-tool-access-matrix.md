# Runtime × Tool Access Matrix

How JM-ADK's external tools wire into each supported runtime. The kit ships **one** MCP server — `workspace-mcp` (stdio via `uvx`) — that aggregates 9 Google Workspace services. This document defines, per runtime, *where* the server is declared, *how* it authenticates, and the *verification status*.

> Canonical server definition: [`.mcp.json`](../.mcp.json) · OAuth setup: [`google-workspace-mcp-setup.md`](google-workspace-mcp-setup.md) · MCP scope/install notes: [`mcp-integration.md`](mcp-integration.md)
> Generate paste-ready templates: `python3 scripts/generate-mcp-configs.py --apply` → [`references/mcp/`](../references/mcp/) · Validate: `python3 scripts/validate-mcp-config.py`

## The single server

`workspace-mcp` exposes (extended tier, ~65 tools): **Gmail, Drive, Calendar, Docs, Sheets, Slides, Forms, Tasks, Contacts**. Auth is OAuth2; credentials live at `~/.config/workspace-mcp/credentials.json` (never committed) and are injected via the `GOOGLE_WORKSPACE_CREDENTIALS_PATH` env var. Every runtime config below references that env placeholder — **never a literal secret**.

## Runtime wiring matrix

| Runtime | Config file | Server key | Auth | Status | Template |
|---|---|---|---|---|---|
| **Claude Code** | `.mcp.json` (project) — auto-discovered; or `claude mcp add` | `mcpServers` | OAuth2 (browser, first run) + `${ENV}` | ✅ verified `[DOC]` | uses `.mcp.json` directly |
| **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` (local); remote → **Connectors** menu (`+` in chat); `.mcpb` Desktop Extensions | `mcpServers` | local OAuth2; remote via Connectors UI | ✅ verified `[DOC]` | `claude_desktop_config.json.example` |
| **OpenAI Codex CLI** | `~/.codex/config.toml` or project `.codex/config.toml`; or `codex mcp add` | `[mcp_servers.workspace-mcp]` (TOML) | OAuth2 + `${ENV}`; `default_tools_approval_mode` | ⚠️ config verified `[DOC]`, not locally run | `codex.config.toml.example` |
| **Gemini CLI** | `~/.gemini/settings.json` or project `.gemini/settings.json` | `mcpServers` (gate with `mcp.allowed`) | OAuth2 + auto env expand | ⚠️ config verified `[DOC]`, not locally run | `gemini.settings.json.example` |
| **Antigravity** (2.0 / IDE / CLI) | `~/.gemini/config/mcp_config.json` (shared) or **MCP Store** UI | `mcpServers` (remote: `serverUrl` + `headers`) | OAuth DCR auto, or `authProviderType: google_credentials` | ⚠️ config verified `[DOC]`, not locally run | `antigravity.mcp_config.json.example` |
| **Cursor** | `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global) | `mcpServers` | OAuth2 + `${ENV}` | ⚠️ config verified `[DOC]`, not locally run | `cursor.mcp.json.example` |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` (Cascade → MCP → Manage) | `mcpServers` | OAuth2 + `${ENV}` | ⚠️ config verified `[DOC]`, not locally run | `windsurf.mcp_config.json.example` |
| **VS Code (Copilot)** | `.vscode/mcp.json` (workspace) — Copilot Chat **agent mode** | `servers` (with `type: stdio`) | OAuth2 + `${ENV}`/inputs | ⚠️ config verified `[DOC]`, not locally run | `vscode.mcp.json.example` |

> **Status legend** — ✅ verified: documented and exercised in this kit's primary runtime. ⚠️ config verified `[DOC]`: the config-file location and schema come from the runtime's official docs (see Sources); the kit has not been executed end-to-end in that runtime, so treat first run as a smoke test.

## Per-service availability

All services are delivered by the one `workspace-mcp` server, so availability is **per-runtime, not per-service** — if the server connects, every service below is reachable (subject to OAuth scopes granted at consent).

| Service | Skill | Representative tools |
|---|---|---|
| Gmail | `gmail-mcp` | search, read, send, draft, labels, filters, thread read, batch read |
| Drive | `google-drive-mcp` | search, get content, create file/folder, share, permissions |
| Docs | `google-docs-mcp` | create, edit, find-replace, export markdown/PDF |
| Sheets | `google-sheets-mcp` | read/write values, create, format range |
| Slides | `google-slides-mcp` | create, batch update, page thumbnail |
| Calendar | `google-calendar-mcp` | list calendars, events, Meet, out-of-office |
| Forms / Tasks / Contacts | (future) | create/responses · lists/tasks · search/manage |

## Repo-native tools (Claude-runtime only)

These are **not** MCP — they are kit features delivered through Claude Code lifecycle hooks (`hooks/hooks.json`): workspace tracking, artifact-placement guard, prompt-injection filter, persona calibration, tasklog auto-logging. Other runtimes have no hook engine, so apply the placement and naming contract manually ([`references/ontology/placement-naming-contract.md`](../references/ontology/placement-naming-contract.md)).

| Capability | Claude Code | Claude Desktop | Codex / Gemini / Antigravity / Cursor / Windsurf / Copilot |
|---|---|---|---|
| MCP tool access (`workspace-mcp`) | ✅ | ✅ | ✅ (per matrix above) |
| Lifecycle hooks (5) | ✅ | ⚠️ runtime-dependent | ❌ apply contract manually |
| Workspace auto-tracking | ✅ | ⚠️ | ❌ manual `workspace/{active}/` discipline |

## Quick start per runtime

1. Complete OAuth once: follow [`google-workspace-mcp-setup.md`](google-workspace-mcp-setup.md) → credentials land at `~/.config/workspace-mcp/credentials.json`.
2. Export the path: `export GOOGLE_WORKSPACE_CREDENTIALS_PATH="$HOME/.config/workspace-mcp/credentials.json"`.
3. Generate templates: `python3 scripts/generate-mcp-configs.py --apply`.
4. Copy the matching `references/mcp/*.example` into your runtime's config file (matrix above).
5. Restart the runtime; verify the server connects (e.g. Claude Code: `claude mcp list`).
6. Validate the canonical config any time: `python3 scripts/validate-mcp-config.py`.

## Sources `[DOC]`

- Claude Desktop — https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop
- Claude Code MCP — https://code.claude.com/docs/en/mcp
- OpenAI Codex MCP — https://developers.openai.com/codex/mcp
- Gemini CLI MCP — https://geminicli.com/docs/tools/mcp-server/
- Antigravity MCP — https://antigravity.google/docs/mcp · Workspace MCP codelab — https://codelabs.developers.google.com/google-workspace-mcp-antigravity
