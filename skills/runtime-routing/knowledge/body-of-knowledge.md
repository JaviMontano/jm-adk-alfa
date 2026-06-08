# Runtime Routing Body of Knowledge

## Canon

Runtime routing is an evidence problem. A route decision is valid only when the recommended runtime has observed support for the task's required capabilities and when unsupported capabilities are marked as pending or unsupported.

## Required Decision Shape

- **Task requirements:** file access, shell, git, PR operations, MCP, hooks, browser, multimodal, IDE state, or adapter generation.
- **Evidence:** repo file, executed check, current runtime metadata, or explicit user config. Conversation memory is not enough.
- **Capability matrix:** each candidate runtime has status `verified`, `pending`, or `unsupported` with evidence ids.
- **Lowest permission:** prefer a verified local route over a broader or remote runtime when both can complete the task.
- **Validation limits:** say exactly which claims are pending and what evidence would close them.
- **Fallback:** provide a local-first fallback or a `Dato requerido` block when no verified route exists.

## Quality Signals

| Signal | Target |
|---|---|
| Evidence coverage | Every supported capability cites an evidence id |
| Permission fit | Recommended runtime is the lowest-permission verified path |
| Pending honesty | Unobserved runtime support is `validation_pending`, not asserted |
| Fallback | Local-first fallback exists with missing data labels |
| Secret boundary | Route does not expand access to secrets or local state unnecessarily |

## Anti-Patterns

- Claiming a runtime supports hooks, MCP, or IDE state without repo evidence or an executed check.
- Routing to a remote runtime when local scripts can complete the task.
- Treating adapter docs as proof that the current session has active runtime capabilities.
- Omitting fallback when a recommended route depends on auth or user-specific state.
