# Google Workspace APIs Scripts

## compile-google-workspace-apis.py

Offline compiler for multi-service Google Workspace plans. It reads only local
JSON assets and fixtures, validates service methods, OAuth scopes, MCP tool
mapping, consent gates, secrets policy, retry/idempotency, and validation
layers, then renders a deterministic Markdown plan.

## check.sh

Runs the positive fixture and negative fixtures. It must pass without network,
Google OAuth, MCP servers, or live API access.
