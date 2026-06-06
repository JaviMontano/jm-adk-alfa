# Session Protocol

`session-protocol` runs the mandatory start-of-session continuity protocol:
load context in a deterministic order, recover recent state, propose pending
closure, and present next steps without starting work prematurely.

## Triggers

- `session protocol`
- `session start`
- `initialize session`
- `context recovery`
- `state recovery`

Do not activate for a generic summary unless the user asks to initialize or
recover session state.

## Resources

- `assets/context-load-order.json` - ordered context source rules.
- `assets/state-recovery-policy.json` - changelog, tasklog, git, and spec checks.
- `assets/closure-policy.json` - close/continue/defer/archive recommendation rules.
- `assets/next-step-policy.json` - next-step ranking and confirmation rules.
- `assets/protocol-report-contract.json` - machine-checkable report shape.
- `scripts/check.sh` - offline report fixture validation.

## Required Output

1. Context Loading
2. State Recovery
3. Pending Closure
4. Next Steps Proposal
5. Confirmation Gate
6. Guardian Decision

## Validation

```bash
bash skills/session-protocol/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill session-protocol
python3 -B scripts/validate-skill-dod.py --skill session-protocol
```

## Safety Rules

- Never auto-close or archive tasks without user confirmation.
- Never start implementation before the confirmation gate.
- Preserve missing files as `[OPEN]` gaps instead of inventing state.
- Use current git status over stale session notes.
