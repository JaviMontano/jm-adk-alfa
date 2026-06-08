---
name: post-tool-use-validator
author: JM Labs (Javier Montaño)
version: 1.0.0
description: "Validate tool outputs against exit codes, evidence tags, quality gates, secret exposure policy, scope compliance, and offline post-tool report fixtures. [EXPLICIT]"
triggers:
  - post tool use validator
  - validate tool output
  - evidence tags after command
  - quality gate result check
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Post Tool Use Validator

Validates tool outputs after execution and blocks unsupported success claims. The skill checks command status, evidence, quality gates, secret exposure, and scope compliance before an assistant says work is done.

## Deterministic Contract

- `assets/post-tool-validation-contract.json` defines the JSON report shape.
- `assets/evidence-policy.json` defines evidence requirements.
- `assets/secret-output-policy.json` defines unmasked secret blockers.
- `assets/scope-validation-policy.json` defines write-scope blockers.
- `scripts/validate_post_tool_use_report.py` validates reports offline.
- `scripts/check.sh` runs positive and negative fixtures.

## Procedure

1. Read the tool result: tool name, command, exit code, stdout/stderr excerpts, and touched paths.
2. Verify that declared status matches the actual result.
3. Require evidence for every pass claim.
4. Block unmasked secrets, private data exposure, and writes outside scope.
5. Return `pass`, `warn`, `fail`, or `blocked` with next action.

## Fail-Closed Conditions

- Tool exit code is non-zero but decision says `pass`.
- Evidence tags or command evidence are missing.
- Output includes unmasked token-like secrets.
- Writes occurred outside declared scope.
- A quality gate is failed while the report claims pass.

## Usage

Run the fixture gate:

```bash
bash skills/post-tool-use-validator/scripts/check.sh
```
