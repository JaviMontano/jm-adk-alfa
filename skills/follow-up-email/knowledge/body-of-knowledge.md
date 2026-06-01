<!--
generated-by: scripts/scaffold-skill.py
generated-for: follow-up-email
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Follow Up Email Body of Knowledge

## Canon

Follow-up emails convert meeting decisions into private, recipient-specific drafts. Each recipient should receive only the action items assigned to them, plus shared next steps and relevant meeting context.

## Extraction Rules

| Signal | Meaning |
|---|---|
| `ACTION:`, `TODO:`, `- [ ]` | Explicit task marker |
| `Name will...`, `Name se encarga...` | Assignee pattern |
| `by`, `para`, `deadline`, date literal | Deadline candidate |
| `decision`, `agreed`, `se acordo` | Context that may affect tasks |

## Privacy Rules

- Render one recipient at a time.
- Never include another person's action items in the current recipient draft.
- Skip recipients with no action items unless the user requests a summary-only note.
- Never send directly from scripts; scripts produce drafts/previews only.

## Asset Rules

- Use `assets/email-copy-tokens.json` for subject prefix, default sign-off, tone, and send policy.
- Use `assets/email-style.css` for HTML previews.
- Keep `assets/manifest.json` updated when output assets change.

## Quality Signals

| Signal | Target |
|---|---|
| Completeness | Every action item appears in exactly one responsible recipient draft |
| Privacy | No cross-recipient leakage |
| Determinism | Same structured JSON input produces same draft |
| Safety | Send action requires explicit user confirmation outside scripts |
| Tone | Warm, professional, and action-oriented |
