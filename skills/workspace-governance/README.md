# Workspace Governance

Govern the gitignored `workspace/` user interaction layer without polluting the
versioned repository. The skill validates workspace scaffolding, dated session
folders, task bridges, `estandares/`, stale-session review, and `.gitignore`
coverage.

## Triggers

- "workspace governance"
- "scaffold workspace"
- "session folder"
- "task bridge"
- "workspace estandares"
- "keep workspace gitignored"

## Allowed Tools

- Read
- Glob
- Grep
- Bash
- Write

## Deterministic Contract

- `workspace/` must be gitignored.
- Workspace directories must have `README.md`.
- Session folders must match `workspace/YYYY-MM-DD-<slug>/`.
- Task bridge folders must match open tasklog items and use `workspace/tasks/TL-XXX-<slug>/`.
- Sessions older than 30 days are flagged for cleanup review, not deleted automatically.
- Machine-readable governance reports must validate with `scripts/check.sh`.

## Output Format

Markdown or JSON with workspace root, gitignore status, directories, sessions, task bridges, estandares, actions, validation, and risks.
