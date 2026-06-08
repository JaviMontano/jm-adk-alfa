---
name: git-hook-integration
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Pre-commit and pre-push hooks, conventional commit enforcement. [EXPLICIT]
  Trigger: "git hook integration"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Git Hook Integration
> "Method over hacks."
## TL;DR
Pre-commit and pre-push hooks, conventional commit enforcement. [EXPLICIT]
## Procedure

### Step 1: Discover
- Identify the repository, existing hook managers, current validation commands,
  and whether hook installation is allowed.
- Read existing hook files or config before proposing changes.
- Default to `plan-only` when the user has not explicitly authorized mutation.

### Step 2: Model
- Use `assets/git-hook-integration-schema.json` as the structured input
  contract.
- Ensure `pre-commit`, `commit-msg`, and `pre-push` stages are represented.
- If Conventional Commits are enabled, require a blocking `commit-msg` hook.

### Step 3: Compile
- Prefer `scripts/compile-git-hook-integration.py` when the task can be
  expressed as structured JSON.
- Use `assets/git-hook-integration-template.md` for Markdown output.
- Treat `assets/install-strategy-model.json` as the source for manager
  selection and install commands.

### Step 4: Validate
- Run `bash skills/git-hook-integration/scripts/check.sh` after changing the
  deterministic contract.
- Verify output contains evidence, hook matrix, commit policy, validation
  commands, install plan, validation, and risks.
## Quality Criteria
- [ ] Evidence tags applied
- [ ] Required hook stages are present
- [ ] Conventional Commit policy is backed by `commit-msg` when enabled
- [ ] Install mode is explicit and non-destructive by default
- [ ] Hook commands are reviewable before installation
- [ ] Actionable output

## Usage

Example invocations:

- "/git-hook-integration" — Run the full git hook integration workflow
- "git hook integration on this project" — Apply to current context
- "compile a plan-only .githooks strategy with conventional commits" — Use
  the deterministic compiler contract

## Bundled Resources

- `assets/` contains schemas, policy models, validation catalog, install
  strategies, and the Markdown report template.
- `scripts/compile-git-hook-integration.py` compiles structured JSON into a
  deterministic Markdown plan.
- `scripts/check.sh` runs fixture checks for valid and invalid hook plans.


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Does not install, overwrite, or enable hooks unless the user explicitly asks
  for that mutation [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
