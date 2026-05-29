# JM Agentic Development Kit Alfa

Version: 5.2.0
License: MIT
Repository: https://github.com/JaviMontano/jm-adk-alfa

JM-ADK is a local-first agentic development kit for AI-assisted software work. It packages skills, agents, commands, prompts, workspace governance, guardrails, and validation scripts so a developer can scaffold, run, review, and update agentic workflows without mixing versioned kit files with local state.

## Component Inventory

The authoritative counts come from `python3 scripts/count-components.py`.

| Component | Count |
|---|---:|
| Skills | 529 |
| Agents | 260 |
| Commands | 266 |
| Prompts | 256 |
| Total physical components | 1311 |

## Install

```bash
git clone https://github.com/JaviMontano/jm-adk-alfa.git
cd jm-adk-alfa
python3 scripts/count-components.py
python3 scripts/validate-skills.py --strict
```

## After Clone / First Use

Before the first task, diagnose local readiness:

```bash
python3 scripts/diagnose-first-use.py --dry-run
```

If the first user input is only `hola`, `buenas`, `hey`, `hello`, or `empecemos`, Alfa should start `/jm-adk:first-use` instead of beginning technical work. The guided setup asks for goal, project type, stack, preferred runtime, autonomy level, command policy, privacy constraints, workspace area, and output format.

Create local profile state only after review:

```bash
python3 scripts/setup-workspace-profile.py --dry-run
python3 scripts/setup-workspace-profile.py --apply
```

The profile lives in `.jm-adk.local.json` and must remain untracked.

## Local State

Versioned kit files live in the repo. Local runtime state does not.

Tracked:

- `.jm-adk.json`
- `skills/`
- `agents/`
- `commands/`
- `prompts/`
- `references/`
- `scripts/`
- `docs/`

Ignored:

- `workspace/` except `workspace/.gitkeep`
- `.jm-adk.local.json`
- `.local/`
- `.codex/`
- `.env*`
- logs, caches, backups, temp files

## Create a Skill

Dry-run first:

```bash
python3 scripts/scaffold-skill.py \
  --name my-skill \
  --description "Short description" \
  --triggers my-skill,example-trigger \
  --allowed-tools Read,Grep,Glob,Bash \
  --owner "JM Labs" \
  --version 0.1.0 \
  --dry-run
```

Apply after review:

```bash
python3 scripts/scaffold-skill.py \
  --name my-skill \
  --description "Short description" \
  --triggers my-skill,example-trigger \
  --allowed-tools Read,Grep,Glob,Bash \
  --owner "JM Labs" \
  --version 0.1.0
```

Create an experimental local skill without tracking it:

```bash
python3 scripts/scaffold-skill.py --name my-experiment --description "Local experiment" --local
```

## Validate

```bash
python3 scripts/validate-skills.py --strict
python3 scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
python3 scripts/validate-onboarding.py
python3 scripts/check-devkit-readiness.py
python3 scripts/qa/run-adversarial-tests.py
bash scripts/generate-pristino-index.sh
```

If a gate fails, use `docs/TROUBLESHOOTING.md` and report the exact command, output, branch, and files changed before asking an agent to fix it.

## Update Safely from GitHub

Use the guide in `docs/git-sync-local-safe.md`.

Fast-forward only when the tree is clean:

```bash
bash scripts/sync-upstream-safe.sh --remote origin
```

Push only an owned branch explicitly:

```bash
bash scripts/sync-upstream-safe.sh --remote origin --push-branch
```

## Contribute

1. Create a branch; do not push directly to `main`.
2. Keep local overrides in `.jm-adk.local.json` or `.local/`.
3. Run the validation commands above.
4. Regenerate `PRISTINO-INDEX.md` when component metadata changes.
5. Open a pull request with the validation output.
