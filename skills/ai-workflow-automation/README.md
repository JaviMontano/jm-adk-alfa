<!--
generated-by: scripts/scaffold-skill.py
generated-for: ai-workflow-automation
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# AI Workflow Automation

Design deterministic LLM-in-the-loop workflow plans with explicit AI steps,
approval gates, human handoffs, fallback paths, and offline validation.

## Triggers

- ai-workflow-automation
- ai workflow automation
- LLM workflow
- human-AI handoff
- approval gate
- automate review
- workflow with AI

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when a process needs AI assistance but must remain controllable,
auditable, and safe for human approval or escalation.

The output is a plan, not an unbounded automation runtime. It must make AI input
contracts, output contracts, approval decisions, owners, retries, and fallbacks
explicit.

## Output Format

Markdown or JSON with:

- Workflow summary and scope
- Actors and source inputs
- Step graph with deterministic checks
- Approval gates and decision criteria
- Human-AI handoff packets
- Bounded retries and fallback paths
- Validation evidence
- Risks and assumptions

JSON workflow plans can be validated offline with:

```bash
bash skills/ai-workflow-automation/scripts/check.sh
```
