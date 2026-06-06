---
name: guardrails-management
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Detect, confirm, store, and enforce user-declared guidelines, constraints, and
  guardrails as JSON files. Pristino's internal RAG for working rules. [EXPLICIT]
  Trigger: "guardrail", "guideline", "constraint", "from now on", "always use", "never use"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Guardrails Management

> "Rules you declare become rules the system enforces."

## TL;DR

Manages user-declared working rules stored as JSON in `references/guardrails/`. When the user expresses a preference ("always use TypeScript", "never use jQuery"), Pristino detects the intent, confirms with the user, and stores it. These rules are loaded at every session start and the Guardian checks compliance. [EXPLICIT]

## Procedure

### Step 1: Discover
- Detect user intent to set a working rule (keywords: "always", "never", "from now on", "prefer", "avoid")
- Read existing guardrails: `references/guardrails/guidelines.json`, `constraints.json`, `guardrails.json`
- Check for duplicates or conflicts with existing rules
- Capture source text, proposed scope, evidence tag, and proposed verifiable
  check before any write.

### Step 2: Analyze
- Classify the rule type:
  - **Constraint** (hard, "never"): stored in `constraints.json`
  - **Guideline** (default, "always"): stored in `guidelines.json`
  - **Guardrail** (soft, "prefer"): stored in `guardrails.json`
- Generate next ID: `GL-NNN` (guidelines), `CT-NNN` (constraints), `GR-NNN` (guardrails)
- Apply `assets/classification-policy.json`, `assets/storage-map.json`, and
  `assets/conflict-policy.json`.

### Step 3: Execute
- **Confirm with user**: "I want to confirm: should I save this as a working [guideline/constraint/guardrail]? (yes/no)"
- If confirmed, append entry to the appropriate JSON file:
  ```json
  { "id": "GL-001", "rule": "...", "type": "guideline", "confirmed": "YYYY-MM-DD", "source": "user-explicit", "active": true }
  ```
- If listing: read all 3 files, display active rules grouped by type
- If removing: set `"active": false` on the specified rule

### Step 4: Validate
- JSON file is valid after write
- No duplicate rules across files
- Rule is actionable and verifiable by the Guardian
- Confirmation was received before storing
- For JSON operation packets, run
  `bash skills/guardrails-management/scripts/check.sh`.

## Deterministic Assets

- `assets/manifest.json` lists every local asset and consumer.
- `assets/rule-schema.json` defines required rule fields.
- `assets/classification-policy.json` maps user language to rule type and ID
  prefix.
- `assets/confirmation-policy.json` requires explicit confirmation before
  persistence.
- `assets/conflict-policy.json` defines duplicate and conflict checks.
- `assets/storage-map.json` maps each type to its canonical JSON file.
- `assets/report-contract.json` defines operation packet fields enforced by the
  offline validator.

## Quality Criteria

- [ ] User confirmation received before storing any rule
- [ ] Rule stored in correct file (guideline/constraint/guardrail)
- [ ] ID is unique and sequential
- [ ] JSON is valid after write
- [ ] No duplicates across files
- [ ] Evidence tags applied
- [ ] Rule includes scope, source, verifiable check, active flag, and evidence
      tag
- [ ] Unconfirmed proposals are reported but not persisted
- [ ] Removals preserve history by setting `active: false`

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Storing without confirmation | User didn't intend a permanent rule | Always double-confirm |
| Mixing types | "Never" rules in guidelines file | Classify by enforcement level |
| Storing unverifiable rules | Guardian can't check "make it nice" | Rules must be specific and testable |
| Rewriting rule files wholesale | Risky data loss | Append or deactivate one entry at a time |
| Resolving conflicts silently | User loses control of policy | Report conflict and require confirmation |

## Related Skills

- `session-protocol` — Loads guardrails during bootstrap
- `continuous-learning` — Insights may generate new guardrails
- `code-review` — Guardian checks guardrail compliance

## Usage

Example invocations:

- "/guardrails-management" — Run the full guardrails management workflow
- "guardrails management on this project" — Apply to current context


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
| User says "from now on" but no rule is specific | Ask for a verifiable check |
| Duplicate active rule exists | Do not store; return existing ID |
| User asks to remove a rule | Deactivate by ID, keep audit metadata |
