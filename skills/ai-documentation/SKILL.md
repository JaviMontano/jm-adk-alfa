---
name: ai-documentation
author: JM Labs (Javier Montaño)
version: 1.0.1
description: >
  Generates and audits source-backed project documentation packets for README,
  API reference, runbooks, architecture notes, changelog drafts, and quickstarts.
  Use this skill when the user asks to "generate docs from code", "write a
  README from this repo", "create API docs", "audit documentation drift", or
  "produce source-backed project documentation". [EXPLICIT]
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# AI Documentation
> "Method over hacks."
## TL;DR
Create documentation only from explicit source evidence, known repository files,
or clearly marked open assumptions. Every output must map generated sections to
source evidence and validation checks. [EXPLICIT]
## Procedure
### Step 1: Source Inventory
- Identify requested documentation type, audience, output path, and required
  source files before drafting. [EXPLICIT]
- Record missing, stale, or conflicting inputs as gaps instead of inventing. [EXPLICIT]
### Step 2: Evidence Map
- Create evidence ids for code, existing docs, API specs, configs, tests, and
  user input. [EXPLICIT]
- Attach evidence ids to every generated section and claim. [EXPLICIT]
### Step 3: Generate Packet
- Produce a deterministic documentation packet using
  `assets/documentation-contract.json`. [EXPLICIT]
- Use closed doc types and source types from local assets. [EXPLICIT]
### Step 4: Validate
- Run `bash skills/ai-documentation/scripts/check.sh` when scripts are present. [EXPLICIT]
- Block delivery if required sections lack evidence, if output paths are unsafe,
  or if validation checks are incomplete. [EXPLICIT]
## Quality Criteria
- [ ] Source inventory covers all requested docs. [EXPLICIT]
- [ ] Generated sections cite evidence ids. [EXPLICIT]
- [ ] Unverified claims are removed or tagged `[OPEN]`. [EXPLICIT]
- [ ] Output paths are relative safe docs paths. [EXPLICIT]
- [ ] Validation packet passes the offline script. [EXPLICIT]

## Usage

Example invocations:

- "Generate a README from this repo" - produce a source-backed README packet.
- "Create API docs from this OpenAPI file" - produce API reference sections.
- "Audit documentation drift" - report stale or missing documentation.

## Deterministic DoD Assets

- `assets/documentation-contract.json` defines the report schema and required checks. [EXPLICIT]
- `assets/source-policy.json` defines allowed source types and source statuses. [EXPLICIT]
- `assets/doc-type-policy.json` defines closed documentation target types and audiences. [EXPLICIT]
- `assets/gap-policy.json` defines severity and blocking-gap behavior. [EXPLICIT]
- `assets/path-policy.json` defines safe relative output path constraints. [EXPLICIT]
- `scripts/validate_ai_documentation_packet.py` validates fixtures offline. [EXPLICIT]


## Assumptions & Limits

- Assumes access to project artifacts such as code, docs, configs, API specs, or user-provided snippets. [EXPLICIT]
- Does not call external documentation services or live APIs during validation. [EXPLICIT]
- Does not invent undocumented behavior; unresolved behavior must be tagged `[OPEN]`. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Produce a gap analysis packet with required sources. |
| Conflicting source files | Record conflict evidence and set validation status to `warn` or `block`. |
| Requested unsafe output path | Block and request a safe relative path under docs, README, or api docs. |
| API docs without API spec | Produce missing-source gap instead of endpoint invention. |
