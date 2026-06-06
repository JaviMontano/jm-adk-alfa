---
name: workspace-governance
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Scaffold and govern the workspace/ directory — gitignored user interaction layer
  with dated session folders, task bridges, and estandares. Constitution XVIII + Workspace. [EXPLICIT]
  Trigger: "workspace", "scaffold workspace", "session folder", "workspace governance", "estandares"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
---

# Workspace Governance

> "The repo stays clean; the workspace stays flexible."

## TL;DR

Scaffolds and maintains the `workspace/` directory — the user's local interaction layer that is gitignored. Creates dated session folders, task bridges (connecting `tasklog.md` to working files), and manages the `estandares/` reference area. Ensures workspace structure is canonical and never pollutes the version-controlled repository. [EXPLICIT]

Use deterministic assets in `assets/` for gitignore policy, session naming, task bridges, estandares, stale review, and report shape. When producing a JSON workspace governance report, validate it offline with `bash skills/workspace-governance/scripts/check.sh`. [EXPLICIT]

## Procedure

### Step 1: Discover
- Check if `workspace/` exists at project root
- Check if `workspace/` is in `.gitignore`
- Inventory existing workspace content (sessions, tasks, estandares)
- Read `tasklog.md` for open items that need working directories

### Step 2: Analyze
- Determine what needs scaffolding (full workspace or new session)
- Map open tasklog items to `workspace/tasks/TL-XXX-<slug>/` directories
- Identify sessions >30 days old for cleanup review
- Check estandares/ for completeness

### Step 3: Execute
- Scaffold workspace if missing:
  ```
  workspace/
    README.md
    tasks/
      README.md
    estandares/
      README.md
  ```
- Create dated session folder for current work:
  ```
  workspace/YYYY-MM-DD-<slug>/
    README.md
    inputs/
    outputs/
    annexes/
  ```
- Create task bridge directories for open tasklog items:
  ```
  workspace/tasks/TL-XXX-<slug>/
    README.md
  ```
- Add `workspace/` to `.gitignore` if not present
- Write README.md for every new subfolder

### Step 4: Validate
- `workspace/` is in `.gitignore`
- Every subfolder has a README.md
- Dated folders use `YYYY-MM-DD-<slug>` format
- Task bridges match open tasklog items
- Sessions >30 days flagged for cleanup

## Quality Criteria

- [ ] workspace/ exists and is gitignored
- [ ] README.md in every workspace subfolder
- [ ] Dated session folders use correct format
- [ ] Task bridges connect to tasklog.md items
- [ ] Stale sessions (>30 days) flagged
- [ ] estandares/ directory present
- [ ] No workspace action targets paths outside `workspace/` except `.gitignore`
- [ ] JSON report passes `scripts/check.sh` when produced

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Committing workspace files | Pollutes repo with transient data | Keep workspace/ in .gitignore |
| Session folders without README | Lose context of what the session was for | Always add README with purpose |
| No task bridges | Disconnect between tracking and files | Create TL-XXX-slug/ per open task |
| Never cleaning up | Disk bloat, stale confusion | Review >30 day sessions |

## Related Skills

- `session-protocol` — Creates session folders as part of init
- `tasklog-management` — Tasklog items drive task bridge creation
- `indexability-validator` — Workspace READMEs follow same rules
- `repository-organization` — Workspace complements repo organization

## Usage

Example invocations:

- "/workspace-governance" — Run the full workspace governance workflow
- "workspace governance on this project" — Apply to current context


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
