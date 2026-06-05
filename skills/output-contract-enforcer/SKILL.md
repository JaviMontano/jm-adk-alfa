---
name: output-contract-enforcer
description: Validate generated outputs against declared contracts for format, required sections, required fields, evidence tags, naming conventions, machine-readable validation packets, and repair suggestions. Use after a skill produces an output, before gate evaluation, when `/jm:verify` is invoked, or when the user asks to validate an artifact against its output contract. [EXPLICIT]
version: 1.0.0
status: hardened
owner: Javier Montaño
tags: [core, validation, contracts, output]
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Output Contract Enforcer

Post-execution validator for generated artifacts. It checks that an output matches the contract it claims to satisfy, then returns a deterministic pass/fail packet with exact violations and repairs.

## When to Activate

Activate when:

- A skill output needs validation before delivery or gate evaluation.
- The user invokes `/jm:verify`.
- The user asks whether an artifact matches a declared contract, schema, template, required section list, evidence-tag rule, or naming convention.
- An orchestrator needs a post-run blocker before merge, publish, or handoff.

Do not activate when the user only asks to design a JSON schema, format a new response, explain output contracts conceptually, or create a fresh artifact. Route those to the owning creation or design skill unless validation of an existing output is explicitly requested.

## Required Inputs

- Contract source: skill `SKILL.md`, `templates/schema.json`, JSON contract, or explicit required fields.
- Generated output: file path or pasted output.
- Output type: markdown, json, html, docx-report, or unknown.
- Required sections or required fields.
- Evidence policy: whether evidence tags are required and which vocabulary is allowed.
- Naming policy: target file path and expected style when file output is involved.

If a required input is missing, return `status: blocked` and list the missing input. Do not guess a contract.

## Deterministic Contract

- Validate only against declared contract evidence, never against unstated preferences.
- Use one evidence-tag vocabulary: `[CÓDIGO]`, `[CONFIG]`, `[DOC]`, `[INFERENCIA]`, `[SUPUESTO]`.
- Quick mode still enforces mandatory evidence tags.
- Do not auto-rename files. Suggest the corrected name.
- Do not mark pass if any required section, field, evidence tag, format, or naming check fails.
- Report every violation with path, check id, expected value, observed value, and repair.
- For machine-readable validation, use `templates/schema.json`.
- Use `scripts/validate_output_contract.py` for deterministic fixture-backed checks.

## Assets And Scripts

- `assets/output-contract-checklist.md` - validation checklist.
- `assets/contract-rules.json` - canonical checks, statuses, formats, and evidence tags.
- `assets/evidence-tag-policy.json` - allowed evidence tags and failure behavior.
- `assets/markdown-section-contract.json` - default report section contract.
- `templates/schema.json` - validation packet schema.
- `scripts/validate_output_contract.py` - local validator for fixture-backed output checks.

## Validation Process

1. Load the declared contract.
2. Normalize the output type and output path.
3. Run checks in this order: existence, format, required sections or fields, evidence tags, naming, and packet shape.
4. Emit `status: pass` only when every required check passes.
5. Emit `status: fail` when the output exists but violates the contract.
6. Emit `status: blocked` when the contract or output is missing.
7. Include deterministic repairs for each violation.

## Validation Packet

Return a Markdown report or JSON packet with:

```json
{
  "schema": 1,
  "skill": "output-contract-enforcer",
  "status": "pass|fail|blocked",
  "contract_id": "contract identifier",
  "artifact": "path or inline artifact label",
  "checks": [
    {
      "id": "markdown_sections",
      "status": "pass|fail|blocked",
      "expected": "declared expectation",
      "observed": "observed output",
      "repair": "deterministic repair"
    }
  ],
  "violations": [],
  "repair_suggestions": [],
  "evidence": []
}
```

## Required Checks

| Check | Pass Condition | Failure |
|---|---|---|
| `contract_loaded` | Contract source is present and parseable. | `blocked`. |
| `format` | Output type matches declared type. | `fail`. |
| `markdown_sections` | Every required section heading exists exactly once or as allowed by contract. | `fail`. |
| `json_schema` | JSON parses and required fields exist. | `fail`. |
| `evidence_tags` | Required evidence tags are present and use allowed vocabulary. | `fail`. |
| `naming` | File name matches declared convention. | `fail` with suggestion, never rename. |
| `machine_readable_packet` | Packet follows `templates/schema.json`. | `fail`. |

## Output Template

```markdown
# Output Contract Validation

status: pass|fail|blocked
contract_id: <id>
artifact: <path or label>

## Checks

| Check | Status | Expected | Observed | Repair |
|---|---|---|---|---|

## Violations

- None, or exact violation records.

## Evidence

- [CÓDIGO] File and command evidence.

## Repair Suggestions

- Deterministic next edits.
```

## Validation Gate

Before marking pass:

- Contract is loaded from explicit evidence.
- Required sections or fields are checked.
- Evidence-tag policy is enforced.
- Naming policy is checked when an output path exists.
- The verdict is fail when any mandatory check fails.
- Repairs are specific and actionable.
- The validation packet itself matches `templates/schema.json`.
