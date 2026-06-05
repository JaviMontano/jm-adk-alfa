# Example Input

Create an agent constitution for `customer-intake-agent`.

Context:

- [EXPLICIT] Existing agents are `orchestrator`, `support-triage-agent`, and `privacy-gatekeeper`.
- [EXPLICIT] Tool registry contains `Read`, `Grep`, and `Glob`.
- [EXPLICIT] The agent may classify incoming customer requests and draft intake summaries.
- [EXPLICIT] The agent must not contact customers, change tickets, access network systems, approve refunds, or write files.
- [EXPLICIT] Escalate to `privacy-gatekeeper` when PII appears, and to `support-triage-agent` when product severity is unclear.
- [OPEN] Memory write approval is not confirmed.

Expected behavior:

- Produce Markdown suitable for `agents/customer-intake-agent/agent.md`.
- Preserve all 22 constitution sections.
- Mark missing memory write policy as `[OPEN]`.
- Put unavailable tools in `Forbidden Tools`.
