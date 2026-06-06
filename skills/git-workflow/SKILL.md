---
name: git-workflow
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Git workflow fundamentals: branching strategy, commit conventions, PR workflow, conflict resolution, release tagging. Foundation for parallel-workflow. [EXPLICIT]
  Trigger: "git workflow", "branching", "commit convention", "PR process", "merge conflict", "release"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Git Workflow

> "Method over hacks. Evidence over assumption."

## TL;DR

Establishes Git workflow fundamentals: branching strategy (trunk-based or feature branches), conventional commit messages, PR templates and review process, conflict resolution patterns, and release tagging with semantic versioning. Foundation that parallel-workflow builds on. [EXPLICIT]

## Deterministic Resources

Use these bundled assets for planning or validating workflow output:

- `assets/workflow-plan-contract.json` defines the required workflow-plan fields.
- `assets/command-policy.json` defines allowed command prefixes and forbidden destructive commands.
- `assets/branch-policy.json` defines branch naming, branch types, and protected bases.
- `assets/release-policy.json` defines release tag strategies and SemVer tag format.

If converting the final plan to JSON for validation, it must pass `scripts/validate_git_workflow_plan.py`.

## Procedure

### Step 1: Discover
- Verify repo state first: branch, local changes, remote alignment, open PRs, and protected base branch.
- Read existing workflow docs, branch naming conventions, PR templates, release notes, and CI configuration when present.
- If repo state is dirty or base is not aligned, stop and report the blocking condition before proposing mutating commands.

### Step 2: Analyze
- Choose branch strategy: `feature`, `hotfix`, `release`, or `trunk`.
- Select commit convention and PR merge method from existing project conventions.
- Map required local validation and CI checks.
- Identify conflict, rollback, and branch-cleanup policy.

### Step 3: Execute
- Produce an ordered command plan with preconditions, expected outcomes, and rollback notes.
- Avoid `git reset --hard`, `git clean -fd`, `git checkout --`, and unsafe force pushes unless the user explicitly authorizes a separate destructive workflow.
- Use `git pull --ff-only` for base updates unless a project-specific policy says otherwise.

### Step 4: Validate
- Validate the plan against required local checks, PR checks, merge criteria, and release-tag criteria.
- Evidence tags must distinguish observed repo state from assumptions.
- Report stop conditions before presenting the next action.

## Quality Criteria

- [ ] Repo state includes branch, cleanliness, remote alignment, and open PR count. `[CODE]`
- [ ] Branch name matches policy and does not target a protected base directly. `[CONFIG]`
- [ ] Command plan excludes forbidden destructive commands unless explicitly blocked for user confirmation. `[CONFIG]`
- [ ] PR policy names required checks, merge method, and branch cleanup. `[CONFIG]`
- [ ] Release policy includes SemVer tag evidence when release tagging is requested. `[CONFIG]`
- [ ] Stop conditions block progress on dirty tree, unaligned base, failed validation, or open conflicting PR. `[CONFIG]`

## Related Skills

- `parallel-workflow` — Advanced parallel Git patterns
- `github-actions-ci` — CI/CD integration
- `deployment-checklist` — Pre-deploy Git checks

## Usage

Example invocations:

- "/git-workflow" — Run the full git workflow workflow
- "git workflow on this project" — Apply to current context


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
