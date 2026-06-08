# Google Workspace APIs

Deterministic integrator for multi-service Google Workspace automation.

## Use When

- A workflow spans Gmail, Calendar, Drive, Docs, Sheets, or Slides.
- A direct REST/client-library plan must align with MCP tool execution.
- You need scope selection, mutation gates, retry/idempotency, and validation
  before touching live Google data.

## Deterministic Assets

- `assets/workspace-service-matrix.json` defines supported services and methods.
- `assets/auth-scope-policy.json` defines least-privilege profiles.
- `assets/mcp-tool-contract.json` maps MCP tools to Workspace service actions.
- `assets/google-workspace-apis-schema.json` defines compiler input.
- `scripts/compile-google-workspace-apis.py` renders a stable Markdown plan.

## Checks

```bash
python3 -B scripts/validate-skill-dod.py --skill google-workspace-apis
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-workspace-apis
bash skills/google-workspace-apis/scripts/check.sh
```

## Output

The compiler produces a Markdown plan with summary, evidence, service matrix,
auth/scope plan, MCP mapping, workflow sequence, retry/idempotency, secrets,
validation, and residual risks.
