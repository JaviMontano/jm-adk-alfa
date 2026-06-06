---
name: knowledge-management
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Organizational knowledge capture, searchability, decay prevention. [EXPLICIT]
  Trigger: "knowledge management"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Knowledge Management
> "Method over hacks."
## TL;DR
Organizational knowledge capture, searchability, decay prevention. [EXPLICIT]

Use this skill to turn scattered project knowledge into a deterministic
knowledge register: source-backed entries, owners, retrieval paths, decay
signals, and next actions. [EXPLICIT]

## Procedure
### Step 1: Discover
- Inventory source artifacts: decisions, docs, tasklogs, changelogs, runbooks,
  conversations, specs, and handoff notes.
- Record each candidate with source path, owner, evidence tag, freshness date,
  retrieval terms, and relationship to active work.
### Step 2: Analyze
- Classify each item with the taxonomy in `assets/knowledge-taxonomy.json`.
- Score searchability and decay risk with `assets/searchability-policy.json` and
  `assets/freshness-policy.json`.
- Flag contradictions, orphan knowledge, duplicate sources, stale entries, and
  uncited claims.
### Step 3: Execute
- Produce a knowledge-management report using the contract in
  `assets/report-contract.json`.
- Include a register, gaps, decay review, retrieval map, action log, validation,
  and risks.
### Step 4: Validate
- Verify quality criteria met.
- For JSON reports, run `bash skills/knowledge-management/scripts/check.sh` and
  use `scripts/validate_knowledge_management_report.py` for offline validation.

## Deterministic Assets

- `assets/manifest.json` lists every local asset and its consumer.
- `assets/evidence-policy.json` defines allowed evidence tags.
- `assets/knowledge-taxonomy.json` defines canonical item and gap types.
- `assets/searchability-policy.json` defines retrieval metadata requirements.
- `assets/freshness-policy.json` defines deterministic decay windows based on a
  report `reference_date`, never the live clock.
- `assets/report-contract.json` defines the report fields enforced by the
  offline validator.

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] Knowledge register includes source, owner, status, freshness, retrieval
      terms, and next action for every item.
- [ ] Decay decisions are computed from explicit report dates, not the current
      date.
- [ ] Searchability findings are reproducible without network access.

## Usage

Example invocations:

- "/knowledge-management" — Run the full knowledge management workflow
- "knowledge management on this project" — Apply to current context
- "Build a knowledge register for these docs and flag stale entries"
- "Audit project decisions for searchability and decay risk"


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
| Missing source path | Mark as gap; do not promote the claim to register |
| Stale item without owner | Block closure until owner or escalation path exists |
| Decay review mentions "today" | Replace with explicit `reference_date` |
