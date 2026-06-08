# Google APIs Integration - Knowledge Graph

## Core Concepts

- `google-apis-integration`: offline planner for multi-service Google API designs.
- `service-catalog`: local operation registry mapped to official Google API surfaces.
- `auth-scope-policy`: least-privilege OAuth and restricted API-key policy.
- `consent-gate`: human approval required before mutating operations.
- `retry-idempotency`: bounded retry behavior paired with duplicate-effect control.
- `secrets-policy`: no OAuth secrets, refresh tokens, or service-account keys in client or repo artifacts.
- `test-matrix`: required validation layers before implementation.

## Dependencies

- Upstream: official Google API references, user requirements, local fixture JSON.
- Downstream: backend implementation, frontend Maps loader, CI validation, security review.

## Skill Relationships

- Adjacent to `google-sheets-mcp`, `google-docs-mcp`, `google-calendar-mcp`,
  `google-drive-mcp`, `google-workspace-apis`, `google-maps-integration`, and
  `youtube-api-integration` style tasks.
