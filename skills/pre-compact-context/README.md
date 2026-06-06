# Pre Compact Context

`pre-compact-context` prepares a deterministic packet before a conversation is
compacted or handed to another session. It preserves hard rules, active state,
blockers, source paths, validation evidence, and the next action.

## Triggers

- `pre compact context`
- `/pre-compact-context`
- `before compaction`
- `prepare context for compaction`
- `make a rehydration prompt`

Do not activate for ordinary summarization unless the user explicitly wants to
preserve context before compression, compaction, handoff, or thread migration.

## Resources

- `assets/retention-policy.json` - P0/P1/P2/DROP classification rules.
- `assets/output-contract.json` - required packet sections and JSON fields.
- `assets/evidence-policy.json` - evidence tag and source rules.
- `assets/rehydration-checklist.json` - resume-readiness checklist.
- `assets/compaction-risk-policy.json` - loss modes and guardian blockers.
- `scripts/check.sh` - offline fixture validation for context packets.

## Required Output

1. Compaction Trigger
2. Preserve Verbatim
3. Compressed Summary
4. Discard List
5. Open Questions
6. Risks And Blockers
7. Validation Evidence
8. Rehydration Prompt
9. Guardian Decision

## Validation

```bash
bash skills/pre-compact-context/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill pre-compact-context
python3 -B scripts/validate-skill-dod.py --skill pre-compact-context
```

## Safety Rules

- Never drop hard rules, blockers, branch/PR state, or validation failures.
- Never preserve secrets verbatim.
- Never claim a source was read unless the packet cites it.
- Prefer `[OPEN]` over invented task state.
