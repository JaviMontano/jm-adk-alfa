# Workspace Governance — Body of Knowledge

## Canon

Workspace governance keeps user interaction artifacts in a local gitignored
layer while preserving traceability to tasklog items and session context.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Gitignore coverage | 100% | `workspace/` ignored |
| README coverage | 100% | Every workspace subfolder has README |
| Session format | 100% | `workspace/YYYY-MM-DD-<slug>/` |
| Task bridge match | 100% | Bridge directories map to open tasklog IDs |
| Stale review | 100% | Sessions >30 days flagged, not deleted |

## Directory Types

- root: `workspace/`.
- tasks: `workspace/tasks/`.
- estandares: `workspace/estandares/`.
- session: `workspace/YYYY-MM-DD-<slug>/`.
- task_bridge: `workspace/tasks/TL-XXX-<slug>/`.
