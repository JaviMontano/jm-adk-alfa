# Session End Cleanup

`session-end-cleanup` closes an agent session with a deterministic handoff:
summary, changes, decisions, tasks, insights, risks, validation evidence, durable
update plan, and guardian decision.

## Triggers

- `session end cleanup`
- `/session-end-cleanup`
- `close this session`
- `prepare the handoff`
- `summarize what changed and what remains`

Do not activate for generic cleanup requests about disk files, code formatting,
or housekeeping unless the request explicitly refers to ending an agent session.

## Required Evidence

- Current objective, active repo/workspace, brand or context rules, and scope.
- Files changed, commands run, validation results, PR/CI/merge state, and
  blockers.
- Decisions, assumptions, insights, open tasks, and durable log authority.

## Resources

- `assets/activation-policy.json` - activation and false-positive boundaries.
- `assets/output-contract.json` - required closeout structure.
- `assets/evidence-policy.json` - evidence tag and source rules.
- `assets/closure-checklist.json` - guardian validation checklist.
- `assets/update-policy.json` - tasklog/changelog write policy.
- `scripts/check.sh` - offline validator for deterministic closeout fixtures.

## Output Format

Return Markdown unless an automation requests JSON. The required Markdown
sections are:

1. Session Summary
2. Changes Completed
3. Decisions And Assumptions
4. Open Tasks
5. Insights Captured
6. Risks And Blockers
7. Validation Evidence
8. Durable Updates
9. Next Handoff
10. Guardian Decision

## Validation

Run the local script contract when maintaining this skill:

```bash
bash skills/session-end-cleanup/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill session-end-cleanup
python3 -B scripts/validate-skill-dod.py --skill session-end-cleanup
```

## Safety Rules

- Never claim validation, CI, PR, merge, or task completion without evidence.
- Never update unrelated tasklog or changelog entries.
- Prefer proposed durable updates when authority or target paths are unclear.
- Pause if unrelated local changes appear before durable writes.
