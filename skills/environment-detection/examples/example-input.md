# Example Input — Environment Detection

Detect the active environment for a JM Labs session before bootstrap.

Available local signals:

- `AGENTS.md` is loaded for the workspace.
- The runtime exposes read, write, shell, and git commands.
- No subagent, hooks, or MCP orchestration tools are available in this session.
- The user supplied model context budget is `128000` tokens.
- Network access is available, but it must not be used as detection evidence.

Return a Markdown summary and JSON report. The loading plan must be safe for the detected tier and must not persist full transcript content.
