---
name: repository-organization
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Audit and improve repository structure: naming consistency, directory patterns,
  file organization, staleness detection. Auto-organization per Constitution XVIII. [EXPLICIT]
  Trigger: "repo organization", "structure audit", "naming consistency", "directory cleanup", "auto-organize"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
---

# Repository Organization

> "Entropy is actively countered — the repo gets more organized over time, not less."

## TL;DR

Audits and improves repository structure for navigability and maintainability. Checks naming consistency (kebab-case slugs), directory patterns (self-documenting layout), file organization (no accumulation without structure), and staleness (empty/outdated directories). Implements Constitution XVIII auto-organization: when files accumulate without structure, organize into named subdirectories with READMEs. [EXPLICIT]

## Deterministic Safety Contract

- Use `assets/repository-organization-contract.json` for report shape.
- Use `assets/transient-placement-policy.json` to classify workspace/archive files.
- Use `assets/move-manifest-policy.json` before moving, archiving, or deleting local files.
- Use `assets/private-boundary-policy.json` to keep private context out of publishable paths.
- Validate reports with `scripts/validate_repository_organization_report.py`.
- Run `scripts/check.sh` before claiming the repo is organized.

Fail closed when a private path is moved or published, a cleanup action lacks a manifest, or `clean_claim` is true while unresolved transient/private findings remain. [EXPLICIT]

## Procedure

### Step 1: Discover
- Scan full directory tree
- Check naming conventions across all directories and files
- Identify directories with >10 files (candidates for sub-organization)
- Check for empty directories
- Read .gitignore for completeness

### Step 2: Analyze
- **Naming audit**: all directories kebab-case? All files follow conventions?
- **Pattern consistency**: do similar components follow same directory layout?
- **Accumulation check**: any directory with >10 unorganized files?
- **Staleness**: empty directories? Directories with no recent commits?
- **Workspace separation**: any transient files outside workspace/?

### Step 3: Execute
- Generate organization report with findings and recommendations
- For accumulated files: propose subdirectory structure with READMEs
- For naming violations: propose renames (with impact assessment)
- For empty directories: propose removal
- For stale directories: flag for review
- Auto-generate READMEs for any directory missing one

### Step 4: Validate
- All directories follow naming conventions
- No directory has >10 unorganized files
- No empty directories remain
- All transient files are in workspace/
- Every directory has a README
- Report is actionable (specific paths, specific recommendations)

## Quality Criteria

- [ ] Full directory tree scanned
- [ ] Naming conventions checked
- [ ] Accumulation flagged (>10 files)
- [ ] Empty directories flagged
- [ ] Stale directories flagged
- [ ] Recommendations are specific and actionable
- [ ] Evidence tags applied

## Related Skills

- `indexability-validator` — README-specific validation
- `code-review` — Code sustainability includes naming (XII)
- `workspace-governance` — Workspace structure separate from repo

## Usage

Example invocations:

- "/repository-organization" — Run the full repository organization workflow
- "repository organization on this project" — Apply to current context


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
