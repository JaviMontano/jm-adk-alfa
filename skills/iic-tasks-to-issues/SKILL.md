---
name: iic-tasks-to-issues
description: Converts tasks.md entries to GitHub Issues via gh CLI. Links to spec IDs. Tracks in context.json. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [metacognition, integrity, github, issues]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# iic-tasks-to-issues {Metacognition} (v1.0)

> **"Every task deserves a home in the issue tracker."**

## Purpose
Converts tasks.md task entries into GitHub Issues using the `gh` CLI. Each issue links back to spec IDs (FR-XXX, US-X). Tracks issue numbers in context.json. [EXPLICIT]

**When to use:**
- After tasks.md is finalized
- When team collaboration requires issue tracking

---

## Core Principles
1. **Law of Mapping:** One task [T###] = one GitHub Issue. [EXPLICIT]
2. **Law of Linkage:** Issue body includes FR-XXX/US-X references from tasks.md. [EXPLICIT]
3. **Law of Labels:** Parallelizable [P] tasks get "parallelizable" label. [EXPLICIT]

## Core Process
### Phase 1: Parse Tasks
1. Read tasks.md for all `- [ ] [T###]` entries. [EXPLICIT]
2. Extract description, US-X link, [P] flag. [EXPLICIT]

### Phase 2: Create Issues
1. `gh issue create --title "[T###] {description}" --body "Linked: US-X, FR-XXX"`. [EXPLICIT]
2. Add labels: priority, parallelizable, category. [EXPLICIT]
3. Record issue number in context.json. [EXPLICIT]

## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| tasks.md | File | Yes | Task list |

| Output | Type | Description |
|--------|------|-------------|
| GitHub Issues | Remote | Created issues |
| context.json update | JSON | Issue number mapping |

## Validation Gate
- [ ] All tasks converted to issues
- [ ] Issues link to spec IDs
- [ ] Issue numbers tracked in context.json

## Usage

Example invocations:

- "/iic-tasks-to-issues" — Run the full iic tasks to issues workflow
- "iic tasks to issues on this project" — Apply to current context


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
