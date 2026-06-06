---
name: session-end-cleanup
author: JM Labs (Javier Montaño)
version: 1.1.0
description: >
  Closes an agent session with a deterministic evidence-tagged handoff: session
  summary, decisions, open tasks, insights, risks, validation evidence, and
  tasklog/changelog update plan. [EXPLICIT]
  Trigger: "session end cleanup"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Session End Cleanup

> "Method over hacks."

## TL;DR

Use this skill at the end of an agent session to leave a reproducible closeout
packet: what changed, what was validated, what remains open, which durable logs
need updates, and what the next session should do first. [EXPLICIT]

## Deterministic Resources

- `assets/activation-policy.json` defines activation and false-positive rules.
- `assets/output-contract.json` defines the required closeout sections.
- `assets/evidence-policy.json` defines allowed evidence tags and proof rules.
- `assets/closure-checklist.json` defines the guardian checklist.
- `assets/update-policy.json` defines tasklog and changelog update boundaries.
- `scripts/check.sh` runs offline fixture validation for the JSON closeout
  contract.

## Inputs

Collect only session-local evidence before writing:

- User objective, active brand, active repo or workspace, and explicit
  constraints.
- Files changed, commands run, validations passed or failed, PR/CI/merge state,
  and unresolved blockers.
- Decisions made, assumptions accepted, risks found, and follow-up tasks.
- Existing tasklog/changelog paths only when the user or repo policy authorizes
  durable updates.

If evidence is missing, mark it as `[ASSUMPTION]` or `[OPEN]`; never invent a
successful command, PR state, merge state, or task closure.

## Procedure

### Step 1: Inventory Evidence

- Read relevant git status, diffs, command logs, PR/CI state, and task artifacts.
- List sources inspected and source gaps explicitly.
- Stop before durable writes if the working tree has unrelated changes.

### Step 2: Normalize The Session

- Produce stable sections in this order: summary, changes, decisions, tasks,
  insights, risks, validation, durable updates, and next handoff.
- Use evidence tags on every factual claim.
- Separate completed work from proposed follow-up work.

### Step 3: Update Durable Logs When Authorized

- Update only the active tasklog/changelog rows or entries supported by local
  evidence.
- If log paths or authority are unclear, emit a proposed update block instead of
  writing.
- Preserve existing chronology and never rewrite unrelated history.

### Step 4: Validate The Closeout

- Check that every required section exists.
- Check that all commands and validation outcomes are evidence-backed.
- Run `bash skills/session-end-cleanup/scripts/check.sh` when the skill itself is
  being maintained.
- Block completion when validation, PR, CI, merge, or ledger evidence is absent.

## Output Contract

Use Markdown for human handoff and JSON only when an automation asks for a
machine-checkable closeout. The Markdown closeout must include:

1. Session Summary
2. Changes Completed
3. Decisions And Assumptions
4. Open Tasks
5. Insights Captured
6. Risks And Blockers
7. Validation Evidence
8. Durable Updates
9. Next Handoff
10. Guardian Decision

## Quality Criteria

- [ ] Every factual claim has `[CODE]`, `[CONFIG]`, `[DOC]`, `[INFERENCE]`, or
  `[ASSUMPTION]`.
- [ ] Validation outcomes name the exact command or local source.
- [ ] Completed tasks are backed by evidence and failed/skipped checks are not
  hidden.
- [ ] Durable updates touch only authorized tasklog/changelog entries.
- [ ] Next handoff is actionable without reading the whole conversation.

## Usage

Example invocations:

- `/session-end-cleanup` after a coding session.
- `Run session end cleanup for this PR and prepare the handoff.`
- `Close this session but do not update durable logs; give me proposed entries.`

## Assumptions & Limits

- Assumes access to current session evidence and relevant project files.
- Does not fetch remote status unless explicitly needed for PR/CI/merge evidence.
- Does not mark tasks complete, claim CI green, or claim merge success without
  local or remote proof.
- Does not replace domain expert judgment for legal, financial, medical,
  security, or contractual decisions.

## Edge Cases

| Scenario | Handling |
|---|---|
| No files changed | Produce a no-change closeout with decisions, risks, and next handoff. |
| Validation failed | Block completion and place the failed command in Risks And Blockers. |
| Missing durable log authority | Emit proposed tasklog/changelog entries only. |
| Conflicting session goals | Preserve both claims, mark conflict, and request owner decision. |
| Unrelated local changes | Stop before writes and identify the unexpected paths. |
