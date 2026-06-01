# Follow Up Email Scripts

Deterministic local rendering for individualized follow-up drafts.

## Entry Points

- `render-follow-up-email.py`: renders one recipient-specific follow-up email from structured meeting JSON.
- `check.sh`: validates fixtures, rendering, privacy boundaries, and failure cases.

## Contract

- Default output is stdout; files are written only with `--output`.
- The script renders one recipient at a time to prevent cross-recipient action item leakage.
- Missing recipients and malformed JSON fail nonzero.
- Sending is never performed by scripts; MCP sending remains draft-first and user-approved.
