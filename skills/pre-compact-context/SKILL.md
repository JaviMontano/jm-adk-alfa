---
name: pre-compact-context
author: JM Labs (Javier Montaño)
version: 1.1.0
description: >
  Preserves critical working context before conversation compaction by producing
  a deterministic retention map, compression summary, risk list, and
  rehydration prompt. [EXPLICIT]
  Trigger: "pre compact context"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Pre Compact Context

> "Method over hacks."

## TL;DR

Use this skill before a context window is compacted, summarized, or handed to a
new thread. It decides what must be preserved verbatim, what may be compressed,
what can be dropped, and what the next session needs to read first. [EXPLICIT]

## Deterministic Resources

- `assets/retention-policy.json` defines priority classes and drop rules.
- `assets/output-contract.json` defines the required packet sections.
- `assets/evidence-policy.json` defines source and evidence tag requirements.
- `assets/rehydration-checklist.json` defines the resume checklist.
- `assets/compaction-risk-policy.json` defines known loss modes and blockers.
- `scripts/check.sh` validates deterministic JSON packet fixtures offline.

## Inputs

Collect local and user-provided context before writing:

- Active objective, brand, repo/workspace, branch, PR/CI state, and hard rules.
- Current progress, pending tasks, blockers, assumptions, and decisions.
- Files, docs, commands, validation evidence, and source paths needed to resume.
- User preferences, naming conventions, scope boundaries, and forbidden changes.

If evidence is missing, mark it `[OPEN]` or `[ASSUMPTION]`; never invent command
results, task status, PR state, or durable context.

## Procedure

### Step 1: Inventory Sources

- Read the active instructions, task state, git status, changed files, and any
  tasklog/changelog or review artifacts needed to resume.
- Identify context that must survive compaction without relying on hidden chat
  memory.

### Step 2: Classify Retention

- Mark P0 for hard rules, active objective, blockers, merge/PR state, and next
  action.
- Mark P1 for implementation details, file paths, validation commands, and
  decisions.
- Mark P2 for helpful background that can be summarized.
- Mark DROP for repeated chatter, stale alternatives, and details disproven by
  later evidence.

### Step 3: Build The Rehydration Packet

- Produce fixed sections: trigger, preserve verbatim, compressed summary,
  discard list, open questions, risks, validation evidence, and rehydration
  prompt.
- Keep source paths and commands exact.
- Include first action for the next session.

### Step 4: Validate Before Compaction

- Ensure every P0 item has a source, evidence tag, and reason.
- Ensure DROP items do not contain active blockers or hard rules.
- Run `bash skills/pre-compact-context/scripts/check.sh` when maintaining this
  skill.
- Block compaction when critical evidence is missing or contradictory.

## Output Contract

The Markdown packet must include:

1. Compaction Trigger
2. Preserve Verbatim
3. Compressed Summary
4. Discard List
5. Open Questions
6. Risks And Blockers
7. Validation Evidence
8. Rehydration Prompt
9. Guardian Decision

## Quality Criteria

- [ ] Every P0 item has source, evidence tag, and reason.
- [ ] All factual claims use `[CODE]`, `[CONFIG]`, `[DOC]`, `[INFERENCE]`,
  `[ASSUMPTION]`, or `[OPEN]`.
- [ ] The packet distinguishes preserve, compress, and discard decisions.
- [ ] The rehydration prompt names exact files, commands, branch/PR state, and
  next action.
- [ ] Guardian blocks if compaction would lose active blockers, hard rules, or
  validation state.

## Usage

Example invocations:

- `/pre-compact-context`
- `Before compaction, preserve the current PR state and next action.`
- `Prepare a rehydration packet for the next session.`

## Assumptions & Limits

- Assumes the current session has enough local evidence to classify context.
- Does not update durable memory unless explicitly authorized.
- Does not replace `session-end-cleanup`; it prepares for compaction before the
  session is necessarily complete.
- Does not claim that omitted context is irrelevant unless it is classified DROP
  with a reason.

## Edge Cases

| Scenario | Handling |
|---|---|
| Context almost full | Emit a minimal P0/P1 packet and block low-value detail. |
| Conflicting task state | Preserve both claims and mark the conflict `[OPEN]`. |
| Unknown PR/CI status | Mark status unknown and include verification command. |
| Missing source path | Keep the item but mark source `[OPEN]`. |
| User asks to compact secrets | Preserve redacted reference only; do not echo secrets. |
