# Validate Hooks DOCX Template

## Document Structure

- Title: Hooks Audit - {repo_name}
- Author: JM Labs
- Date: {date}

## Sections

1. Summary metrics: hooks path, shape, totals, safe count, severity counts, status.
2. Evidence: source, read mode, and mutation policy.
3. Critical findings: compatibility, structure, command safety, and placement guard blockers.
4. Findings table: severity, event, hook type, rule, finding, remediation.
5. Event coverage: recognized, ToolUseContext, non-ToolUseContext, and unknown events.
6. ToolUseContext compatibility: command/http all events; prompt/agent only PreToolUse, PermissionRequest, PostToolUse.
7. Command safety: string-only inspection, script references, no hook execution.
8. Placement guard: expected PreToolUse command registration and policy reference.
9. Remediation checklist.
10. Validation and residual limits.
