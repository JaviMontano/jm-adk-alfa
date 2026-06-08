# Google Sheets MCP Scripts

`compile-google-sheets-mcp.py` compiles a structured JSON request into a
deterministic Markdown plan/checklist for Google Sheets MCP work. [CODE]

## Contract

- Offline only: no Google Sheets, OAuth, HTTP, network, or MCP calls. [CODE]
- Reads local JSON/Markdown assets under `skills/google-sheets-mcp/assets/` and the provided input fixture. [CODE]
- Writes only the requested Markdown output when `--output` is provided. [CODE]
- Fails fast when the request omits read-only discovery, a valid scope profile, spreadsheet-file scope binding, ValueRange fields, batchUpdate requests, or human confirmation for mutations. [CODE]

## Examples

```bash
python3 skills/google-sheets-mcp/scripts/compile-google-sheets-mcp.py \
  --input skills/google-sheets-mcp/scripts/fixtures/google-sheets-mcp-input.json

bash skills/google-sheets-mcp/scripts/check.sh
```
