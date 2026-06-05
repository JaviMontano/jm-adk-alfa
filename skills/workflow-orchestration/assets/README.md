# workflow-orchestration assets

These assets define the deterministic contract for compiling a resumable multi-step workflow execution plan from structured JSON.

- `orchestration-schema.json` defines required workflow, stage, checkpoint, and resume fields.
- `checkpoint-policy.json` defines pass/fail checkpoint quality rules.
- `resume-policy.json` defines state, idempotency, retry, and recovery requirements.
- `orchestration-template.md` renders a validated orchestration plan into deterministic Markdown.
