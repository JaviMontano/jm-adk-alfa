# Hooks Audit: jm-adk-alfa

## Summary

- [CODE] Hooks path: hooks/hooks.json.
- [CODE] Hooks shape: event-keyed-object.
- [CODE] Total hook entries: 4.
- [CODE] Safe entries: 4.
- [CODE] Findings: critical=0, warning=0, info=0.
- [CODE] Overall status: PASS.

## Evidence

- [CODE] mutation_policy: no hooks executed and no config mutated.
- [CODE] read_mode: offline-read-only.
- [CODE] source: provided hooks.json fixture.

## Critical Findings

- [CODE] No critical findings.

## Findings

- [CODE] No findings.

## ToolUseContext Compatibility

- [CODE] ToolUseContext is available only on PreToolUse, PermissionRequest, and PostToolUse.
- [CODE] command and http hooks are compatible with all 22 recognized events.
- [CODE] prompt and agent hooks are compatible only with ToolUseContext events.
- [CODE] No prompt or agent hooks are registered on non-ToolUseContext events.

## Command Safety

- [CODE] Command hooks inspected without execution: 2.
- [CODE] No command safety findings.

## Placement Guard

- [CODE] Expected event: PreToolUse.
- [CODE] Detected placement guard reference on PreToolUse as command.
- [CODE] Policy reference: references/guardrails/placement-policy.json.

## Remediation Checklist

- [CODE] No remediation required.

## Validation

- [CODE] hooks.json structure checked: event-keyed-object.
- [CODE] Event names checked against all 22 recognized events.
- [CODE] Hook type compatibility checked against command, http, prompt, and agent.
- [CODE] ToolUseContext availability checked for prompt and agent hooks.
- [CODE] Command safety inspected by string analysis only.
- [CODE] Placement guard expectations checked without mutating config.

## Risks And Limits

- [INFERENCE] Offline checks cannot prove runtime behavior of hook commands.
- [INFERENCE] Command safety checks are pattern-based and may miss project-specific hazards.
- [ASSUMPTION] The supplied hooks_json is the authoritative hooks configuration for the audited plugin root.
- [CODE] This compiler does not execute hook commands and only writes a report when --output is supplied.
