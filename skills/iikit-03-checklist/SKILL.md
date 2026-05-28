---
name: iikit-03-checklist
description: >-
  Generate quality checklists that validate requirements completeness, clarity, and consistency — produces scored checklist items linked to specific spec sections (FR-XXX, SC-XXX).
  Use when reviewing a spec for gaps, doing a requirements review, verifying PRD quality, auditing user stories and acceptance criteria, or gating before implementation.
license: MIT
metadata:
  version: "1.6.4"
version: 1.0.0
---

# Intent Integrity Kit Checklist

Generate "Unit Tests for English" — checklists that validate REQUIREMENTS quality, not implementation. [EXPLICIT]

## Core Principle

Every checklist item evaluates the **requirements themselves** for completeness, clarity, consistency, measurability, and coverage. Items MUST NOT test implementation behavior. [EXPLICIT]

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). [EXPLICIT]

## Constitution Loading

Load constitution per [constitution-loading.md](../iikit-core/references/constitution-loading.md) (basic mode). [EXPLICIT]

## Prerequisites Check

1. Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/check-prerequisites.sh --phase 03 --json`
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/check-prerequisites.ps1 -Phase 03 -Json`
2. Parse JSON for `FEATURE_DIR` and `AVAILABLE_DOCS`.
3. If JSON contains `needs_selection: true`: present the `features` array as a numbered table (name and stage columns). Follow the options presentation pattern in [conversation-guide.md](../iikit-core/references/conversation-guide.md). After user selects, run:
   ```bash
   bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/set-active-feature.sh --json <selection>
   ```
   Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/set-active-feature.ps1 -Json <selection>`

   Then re-run the prerequisites check from step 1.

## Execution Steps

### 1. Clarify Intent

Derive up to THREE contextual questions (skip if unambiguous from `$ARGUMENTS`): [EXPLICIT]
- Scope: include integration touchpoints?
- Risk: which areas need mandatory gating?
- Depth: lightweight sanity list or formal release gate?
- Audience: author-only or peer PR review?

### 2. Load Feature Context

Read from FEATURE_DIR: `spec.md` (required), `plan.md` (optional), `tasks.md` (optional). [EXPLICIT]

### 3. Generate Checklist

**Starting point**: `FEATURE_DIR/checklists/requirements.md` already exists (created by `/iikit-01-specify`). Review it, extend it with additional items, and resolve gaps. Do NOT create a duplicate — work with the existing file.

**Additional domain checklists** (optional): if the spec has distinct domains that warrant separate review (e.g., security, performance, accessibility), create additional files as `FEATURE_DIR/checklists/[domain].md`. These supplement `requirements.md`, not replace it.

**Item structure**: question format about requirement quality, with quality dimension tag and spec reference.

Correct: "Are visual hierarchy requirements defined with measurable criteria?" [Clarity, Spec SFR-1]
Wrong: "Verify the button clicks correctly" (this tests implementation) [EXPLICIT]

**Categories**: Requirement Completeness, Clarity, Consistency, Acceptance Criteria Quality, Scenario Coverage, SC-XXX Test Coverage, Edge Case Coverage, Non-Functional Requirements, Dependencies & Assumptions.

**Traceability**: >=80% of items must reference spec sections or use markers: `[Gap]`, `[Ambiguity]`, `[Conflict]`, `[Assumption]`.

See [checklist-examples.md](references/checklist-examples.md) for correct/wrong examples and required patterns. [EXPLICIT]

Use [checklist-template.md](../iikit-core/templates/checklist-template.md) for format structure. [EXPLICIT]

### 4. Gap Resolution (Interactive)

For each `[Gap]` item: follow the gap resolution pattern in [conversation-guide.md](../iikit-core/references/conversation-guide.md). Present missing requirement, explain risk, offer options. On resolution: update spec.md and check item off. Skip if `--no-interactive` or no gaps. [EXPLICIT]

### 5. Remaining Item Validation

After gap resolution, validate ALL unchecked `[ ]` items against spec/plan/constitution: [EXPLICIT]
- If covered: check off with justification
- If genuine gap: convert to `[Gap]` and resolve or defer

Continue until all items are `[x]` or explicitly deferred. [EXPLICIT]

**IMPORTANT**: Checklists are optional — not creating one is fine. But once created, they MUST reach 100% before the skill reports success.

### 6. Report

Output: checklist path, item counts (total/checked/deferred), gap resolution summary, completion percentage. [EXPLICIT]

## Commit

```bash
git add specs/*/checklists/ .specify/context.json
git commit -m "checklist: <feature-short-name> requirements review"
```

## Record Phase Completion

Write a timestamp to `.specify/context.json` so the dashboard knows the checklist phase was run (not just that requirements.md exists from specify): [EXPLICIT]

```bash
CONTEXT_FILE=".specify/context.json" [EXPLICIT]
[[ -f "$CONTEXT_FILE" ]] || echo '{}' > "$CONTEXT_FILE"
jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.checklist_reviewed_at = $ts' "$CONTEXT_FILE" > "$CONTEXT_FILE.tmp" && mv "$CONTEXT_FILE.tmp" "$CONTEXT_FILE"
```

## Dashboard Refresh

Regenerate the dashboard so the pipeline reflects checklist completion: [EXPLICIT]

```bash
bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/generate-dashboard-safe.sh
```

Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/generate-dashboard-safe.ps1` [EXPLICIT]

## Next Steps

Run: `bash .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/bash/next-step.sh --phase 03 --json` [EXPLICIT]
Windows: `pwsh .tessl/tiles/tessl-labs/intent-integrity-kit/skills/iikit-core/scripts/powershell/next-step.ps1 -Phase 03 -Json` [EXPLICIT]

Parse the JSON and present: [EXPLICIT]
1. If `clear_after` is true: suggest `/clear` before proceeding
2. Present `next_step` as the primary recommendation
3. If `alt_steps` non-empty: list as alternatives
4. For `next_step` and each `alt_step`, include the `model_tier` from the JSON so the user knows which model is best for each option. Look up tiers in [model-recommendations.md](../iikit-core/references/model-recommendations.md) for agent-specific switch commands.
5. Append dashboard link

If deferred items remain, warn that downstream skills will flag incomplete checklists. [EXPLICIT]

Format:
```
Checklist complete! [EXPLICIT]
Next: [/clear → ] <next_step> (model: <tier>) [EXPLICIT]
[- <alt_step> — <reason> (model: <tier>)]

- Dashboard: file://$(pwd)/.specify/dashboard.html (resolve the path)
```

## Usage

Example invocations: [EXPLICIT]

- "/iikit-03-checklist" — Run the full iikit 03 checklist workflow
- "iikit 03 checklist on this project" — Apply to current context


## Validation Gate

- [ ] Output follows the defined structure and format [EXPLICIT]
- [ ] All claims are tagged with evidence markers [EXPLICIT]
- [ ] No placeholder content (TBD, TODO) [EXPLICIT]
- [ ] Actionable recommendations with priority levels [EXPLICIT]
- [ ] Assumptions explicitly documented [EXPLICIT]

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
