---
name: meta-orchestration-updater
description: Auto-updates orchestration state. Syncs context.json, score-history.json, skills_index.json. Triggers dashboard regeneration. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montano
tags: [meta, orchestration, sync, auto-update]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# meta-orchestration-updater {Meta} (v1.0)

> **"Skills that create, review, search, and deploy other skills."**

## Purpose
Keeps all orchestration artifacts in sync. Updates context.json stage, regenerates index, refreshes dashboard. [EXPLICIT]

**When to use:** After any pipeline phase completion or artifact change. Run `/jm:status` to trigger.

## Core Principles
1. **Law of Sync:** context.json, score-history.json, and skills_index.json must reflect current state. [EXPLICIT]
2. **Law of Dashboard:** After state change, regenerate .specify/dashboard.html. [EXPLICIT]
3. **Law of Automation:** This skill runs automatically after gate passes and phase transitions. [EXPLICIT]

## Core Process
### Phase 1: Read current .specify/context.json state.
### Phase 2: Compute stage from artifact existence. Update context.json.
### Phase 3: Regenerate skills_index.json + dashboard.html. Update score-history.json.

## Validation Gate
- [ ] Operation completed successfully
- [ ] skills_index.json updated if needed
- [ ] context.json reflects current state
- [ ] No stack violations (R-002, R-003)

## 4. Self-Correction Triggers
> [!WARNING]
> IF skills_index.json is stale THEN regenerate before searching.
> IF deploying a skill with status != production THEN WARN user.

## Usage

Example invocations:

- "/meta-orchestration-updater" — Run the full meta orchestration updater workflow
- "meta orchestration updater on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
