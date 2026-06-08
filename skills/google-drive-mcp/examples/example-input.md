# Example Input

Compile a safe Google Drive MCP plan for this request:

- Search My Drive for existing `alfa` assets before creating anything.
- Create `/P-007/Alfa/DoD` only if it does not already exist.
- Upload `/workspace/artifacts/p-007-alpha-report.pdf` as a PDF with metadata.
- Export the Google Docs source brief to PDF after verifying download capability.
- Share the uploaded report with `reviewer@example.com` as commenter.
- Use read-only-first, `q`, `fields`, `trashed = false`, efficient `corpora`,
  least-privilege scopes, and human confirmation before sharing.

Structured fixture:

```bash
python3 skills/google-drive-mcp/scripts/compile-google-drive-mcp.py \
  --input skills/google-drive-mcp/scripts/fixtures/google-drive-mcp-input.json
```
