---
name: google-workspace-apis-meta
type: self-improvement
version: 2.1.0
description: "Evaluate and improve the Google Workspace APIs skill."
---

# Google Workspace APIs — Self-Improvement

## Evaluate

1. Do `assets/workspace-service-matrix.json` methods still match official docs?
2. Are scope profiles narrower than the requested operation?
3. Do MCP tool names reflect the active Workspace MCP server surface?
4. Do fixtures reject missing consent, broad scopes, and tool mismatches?
5. Does the validation matrix distinguish offline, sandbox, and live-read-only?

## Improve

1. Update source links in `assets/source-map.md`.
2. Add service methods only with official documentation.
3. Extend fixtures before adding new compiler branches.
4. Keep scripts offline and deterministic.
5. Update evals when a new failure mode is encoded.
