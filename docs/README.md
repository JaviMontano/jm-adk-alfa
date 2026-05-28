# JM-ADK Documentation

## Start Here

- [Getting Started](getting-started.md): clone, validate, create a skill, and keep local state safe.
- [Git Sync Local Safe](git-sync-local-safe.md): update from GitHub without breaking local work.
- [Architecture](../ARCHITECTURE.md): component model and repository boundaries.

## Component Catalog

Run the live counter instead of trusting stale prose:

```bash
python3 scripts/count-components.py
```

Current physical inventory: 524 skills, 256 agents, 260 commands, 256 prompts.

## Maintainer Guides

- [Custom Skills](advanced/custom-skills.md)
- [Custom Agents](advanced/custom-agents.md)
- [MCP Integration](mcp-integration.md)
- [Production Deployment](advanced/production-deployment.md)

## Examples

| # | Example | Shows |
|---|---------|-------|
| 1 | [E-Commerce Analysis](examples/01-ecommerce-analysis.md) | Discovery pipeline |
| 2 | [Task Manager Scaffold](examples/02-task-manager-scaffold.md) | Scaffold to build |
| 3 | [Portfolio on Hostinger](examples/03-portfolio-deploy.md) | Static deployment |

## Quality Gates

```bash
python3 scripts/validate-skills.py --strict
python3 scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
```
