---
name: safe-scripting-and-bash
version: 1.0.0
description: "Design and review safe, portable, dry-run-first scripts for local agentic development workflows."
owner: "JM Labs"
triggers:
  - safe-scripting
  - bash
  - shell-script
  - dry-run
  - script-safety
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Safe Scripting And Bash

## When To Use

- Creating or reviewing local scripts for Alfa.
- A script can write, move, generate, sync, or inspect many files.
- Bash portability, dry-run behavior, repo-root detection, or rollback matters.

## When Not To Use

- A simple one-line command is enough and has no durable value.
- The requested command is destructive and lacks explicit approval.
- Secrets or credentials would be read, printed, or stored.

## Inputs

- Script purpose.
- Inputs and outputs.
- Files or directories affected.
- Required permissions.
- Dry-run, apply, force, and fallback behavior.

## Outputs

- Safe script or review.
- Usage examples.
- Risk notes and rollback/fallback.
- Validation command.

## Workflow

1. Discover: read existing scripts and repo conventions.
2. Analyze: identify write surface, destructive risk, secrets risk, and portability needs.
3. Execute: implement with repo-root detection and dry-run-first behavior when writes are possible.
4. Validate: run syntax checks and non-destructive smoke tests.

## Safety Limits

- No `rm -rf`, hard reset, force push, or broad overwrite without explicit approval.
- No absolute repo paths inside scripts; use `git rev-parse --show-toplevel` or equivalent.
- No overwrites without `--force`.

## Success Criteria

- Script is stdlib/portable unless justified.
- Dry-run is default for broad writes.
- Failure modes are clear.
- Validation is documented.

## Fallback

If safe automation is unclear, produce a checklist and manual commands instead of a script.

## Examples

- Add a dry-run setup script for local profile creation.
- Review a sync script for local-state and nested-repo hazards.
