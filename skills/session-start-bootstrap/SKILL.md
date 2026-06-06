---
name: session-start-bootstrap
author: JM Labs (Javier Montaño)
version: 1.1.0
description: >
  Starts an agent session by verifying environment, loading only required
  context, initializing guardrails, and producing a deterministic start packet.
  [EXPLICIT] Trigger: "session start bootstrap"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Session Start Bootstrap

> "Method over hacks."

## TL;DR

Use this skill at the beginning of a session to establish safe operating state:
active repo, branch, brand, instructions, context sources, blockers, validation
baseline, and first action. [EXPLICIT]

## Deterministic Resources

- `assets/bootstrap-contract.json` defines required packet fields.
- `assets/environment-policy.json` defines repo, branch, PR, and dirty-tree
  checks.
- `assets/context-loading-policy.json` defines minimal context loading order.
- `assets/guardrails-policy.json` defines stop conditions and hard-rule loading.
- `assets/source-priority.json` defines source precedence.
- `scripts/check.sh` validates JSON bootstrap packet fixtures offline.

## Inputs

Collect:

- Active user objective and active brand.
- Current repo/workspace, branch, git status, PR state, and merge baseline.
- Applicable `AGENTS.md`, runtime instructions, tasklog/changelog or handoff
  packet, and user constraints.
- Known blockers, stashes, pending validations, and next action.

Mark unknown state `[OPEN]`; never infer a clean tree, current branch, PR state,
or user authorization without evidence.

## Procedure

### Step 1: Verify Environment

- Confirm repo identity and current branch.
- Run or record `git status --short --branch`.
- Check open PRs or local blockers when the workflow requires exclusivity.
- Stop before writes if the repo is dirty outside the active scope.

### Step 2: Load Minimal Context

- Read root instructions first, then only task-relevant sources.
- Prefer recent handoff packets, review docs, tasklog/changelog entries, and
  files named by the user.
- Do not bulk-load private or unrelated context.

### Step 3: Initialize Guardrails

- Record hard rules, forbidden changes, validation requirements, and pause
  criteria.
- Resolve source precedence: explicit user config, repo instructions, active
  handoff, then inferred defaults.

### Step 4: Emit Start Packet

- Produce environment, context sources, guardrails, blockers, validation
  baseline, and first action.
- Block execution if the start packet has unresolved critical gaps.

## Output Contract

The Markdown packet must include:

1. Environment
2. Context Sources Loaded
3. Active Guardrails
4. Current State
5. Blockers And Gaps
6. Validation Baseline
7. First Action
8. Guardian Decision

## Quality Criteria

- [ ] Repo, branch, and dirty-tree state are evidence-backed.
- [ ] Context sources loaded are listed by path or command.
- [ ] Hard rules and pause criteria are explicit.
- [ ] First action is concrete and scoped.
- [ ] Guardian blocks when environment or context authority is missing.

## Usage

- `/session-start-bootstrap`
- `Start this session from the prior handoff.`
- `Bootstrap the repo and tell me the first safe action.`

## Assumptions & Limits

- Does not edit project files unless the start packet is valid and the next
  skill authorizes edits.
- Does not bulk-load unrelated context.
- Does not treat stale handoffs as current without git/PR verification.

## Edge Cases

| Scenario | Handling |
|---|---|
| Dirty tree | Pause and list changed paths before writes. |
| Unknown repo | Request repo identity or inspect safe local markers. |
| Conflicting instructions | Preserve both, apply explicit user config first, and mark conflict. |
| Missing handoff | Start from repo instructions and mark missing handoff `[OPEN]`. |
| Open PR exists | Pause if workflow requires one PR at a time. |
