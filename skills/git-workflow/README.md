# Git Workflow

`git-workflow` designs or audits a safe Git operating plan before branch, commit, PR, merge, conflict, or release-tag work. It favors explicit preflight, clean working tree checks, deterministic commands, and clear stop conditions.

## Deterministic Inputs

- Repository state: branch, cleanliness, local/remote alignment, and open PR count.
- Desired operation: feature PR, hotfix, release tag, conflict resolution, or workflow audit.
- Project constraints: branch naming, commit convention, merge method, required checks, and release policy.

## Deterministic Output

The output is a Git workflow plan with:

- repo preflight and decision status;
- branch strategy and branch name;
- ordered command plan with preconditions and rollback notes;
- commit convention and PR policy;
- conflict-resolution policy;
- release-tag policy when relevant;
- validation commands and stop conditions;
- risks and assumptions with evidence tags.

## Offline Contract

The bundled validator checks deterministic JSON workflow-plan fixtures against policy assets:

```bash
bash skills/git-workflow/scripts/check.sh
```
