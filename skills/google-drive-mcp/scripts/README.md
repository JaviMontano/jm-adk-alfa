# Google Drive MCP Scripts

`compile-google-drive-mcp.py` compiles a structured JSON request into a
deterministic Markdown plan/checklist for Google Drive MCP work.

## Contract

- Offline only: no Google Drive, OAuth, HTTP, or MCP calls.
- Reads only local JSON/Markdown assets under `skills/google-drive-mcp/assets/`
  and the provided input fixture.
- Writes only the requested Markdown output when `--output` is provided.
- Fails fast when the request omits read-only discovery, `trashed = false`,
  `fields`, efficient `corpora`, valid scope profiles, upload type rules, or
  human confirmation for mutating operations.

## Examples

```bash
python3 skills/google-drive-mcp/scripts/compile-google-drive-mcp.py \
  --input skills/google-drive-mcp/scripts/fixtures/google-drive-mcp-input.json

bash skills/google-drive-mcp/scripts/check.sh
```
