# Changelog Management

`changelog-management` maintains `changelog.md` as a durable continuity log for
decisions, completions, amendments, insights, blockers, and discoveries.

## Triggers

- `changelog-management`
- `changelog`
- `log decision`
- `record change`
- `what happened`
- `session log`
- `record blocker`

## Allowed Tools

- Read
- Write
- Edit
- Glob
- Grep
- Bash

## Deterministic Assets

| Asset | Purpose |
|---|---|
| `assets/changelog-contract.json` | Required report keys and evidence tags. |
| `assets/entry-type-policy.json` | Allowed types and required fields. |
| `assets/ordering-policy.json` | Newest-first date sections and explicit `as_of_date`. |
| `assets/dedupe-policy.json` | Duplicate fingerprint and skip/revise behavior. |
| `assets/evidence-policy.json` | Rationale, principle, and evidence reference requirements. |

## Output Format

Return Markdown with:

- changelog snapshot
- proposed entries
- duplicate review
- ordering review
- write authorization
- Guardian decision

Machine-readable reports should pass:

```bash
bash skills/changelog-management/scripts/check.sh
```

## Safety Rules

- Do not append duplicate entries.
- Do not use hidden system time for entry dates.
- Do not write unsupported event types.
- Do not write entries missing rationale, principle references, or evidence.
- Do not activate for unrelated public release-note requests.
