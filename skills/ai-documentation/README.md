# AI Documentation

Generates and audits source-backed project documentation packets for README,
API reference, runbooks, architecture notes, changelog drafts, and quickstarts.

## Triggers

- "generate docs from code"
- "write a README from this repo"
- "create API docs"
- "audit documentation drift"
- "produce source-backed project documentation"

## Contract

The skill produces a JSON-compatible documentation packet with:

- project metadata and target audience
- evidence inventory tied to code, docs, configs, tests, API specs, or user input
- requested documentation targets and output paths
- generated section summaries with source evidence ids
- gap analysis for missing, stale, or conflicting sources
- deterministic validation checks and residual risks

## Offline Validation

Run:

```bash
bash skills/ai-documentation/scripts/check.sh
```

The validator uses only files inside this skill and rejects packets with unknown
doc types, missing evidence, unsafe paths, incomplete validation checks, or
blocking gaps reported as pass.
