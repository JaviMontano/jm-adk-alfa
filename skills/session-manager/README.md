# Session Manager

`session-manager` keeps project session state reproducible by reading
`.specify/context.json`, computing the current feature stage from local
artifacts, and writing state only when the evidence and authorization are clear.

## Triggers

- `/jm:status`
- `session-manager`
- `recover session state`
- `compute current feature stage`
- `update context.json after this phase`

## Allowed Tools

- Read
- Write
- Edit
- Bash
- Glob
- Grep

## Deterministic Assets

| Asset | Purpose |
|---|---|
| `assets/state-contract.json` | Required status report shape and allowed context statuses. |
| `assets/stage-policy.json` | Stage order, artifact mapping, and no-skip rule. |
| `assets/priming-policy.json` | Ordered cold-start sources and missing-source behavior. |
| `assets/persistence-policy.json` | Authorized `.specify/**` write targets. |
| `assets/source-boundary-policy.json` | Source boundaries and anti-inference rules. |

## Output Format

Return Markdown with:

- context snapshot
- priming sources
- computed stage
- artifact evidence
- persistence actions
- next action
- Guardian decision

Machine-readable reports should follow `assets/state-contract.json` and pass:

```bash
bash skills/session-manager/scripts/check.sh
```

## Safety Rules

- Do not infer progress from memory or branch names.
- Do not create `.specify/context.json` without authorization.
- Do not advance more than one stage in one pass.
- Do not write outside `.specify/context.json`, `.specify/score-history.json`,
  and `.specify/decisions/`.
