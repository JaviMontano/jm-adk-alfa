# GitHub Actions CI/CD Assets

These assets define the deterministic contract for GitHub Actions CI/CD plans.

## Files

- `ci-workflow-contract.json`: required output sections and JSON fields.
- `triggers-policy.json`: safe trigger definitions and deploy restrictions.
- `permissions-policy.json`: least-privilege permission rules.
- `action-pinning-policy.json`: immutable action reference requirements.
- `cache-policy.json`: dependency cache key and invalidation rules.
- `matrix-policy.json`: bounded matrix strategy requirements.
- `secrets-policy.json`: secret name, scope, and inline value rules.
- `deployment-policy.json`: protected environment and branch gate rules.
- `evidence-policy.json`: validation evidence required before readiness.

Use these assets as the source of truth before editing prompts or examples.
