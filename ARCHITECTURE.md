# JM-ADK Architecture v5.2.0

> 585 Skills · 260 Agents · 267 Commands · 256 Prompts · 1368 physical components

## Directory Structure

```text
jm-adk-alfa/
├── .claude-plugin/plugin.json      # Plugin manifest
├── .jm-adk.json                    # Shared kit config
├── .jm-adk.local.json              # Local override config, ignored
├── agents/                         # 260 specialist agents
├── commands/                       # 267 user-invocable commands
├── prompts/                        # 256 top-level prompt files
├── skills/                         # 585 skill modules
│   └── {skill}/
│       ├── SKILL.md
│       ├── README.md
│       ├── agents/{lead,support,guardian,specialist}.md
│       ├── knowledge/{body-of-knowledge.md,knowledge-graph.json}
│       ├── prompts/{primary.md,meta.md,variations/}
│       ├── templates/output.md
│       ├── evals/evals.json
│       └── examples/{example-input.md,example-output.md}
├── workspace/                      # Local runtime state, ignored except .gitkeep
├── .local/                         # Local experiments, ignored
├── references/                     # Ontology and guardrails
├── scripts/                        # Scaffolding, validation, sync, and hooks
├── docs/                           # User and maintainer documentation
└── PRISTINO-INDEX.md               # Generated component index
```

## Upgrade-Safe Boundaries

- Kit core is versioned and reviewable.
- `workspace/` is local session state and must not be committed except `workspace/.gitkeep`.
- `.jm-adk.local.json` is for local configuration and must not be committed.
- `.local/skills/` is for experimental local skills and must not be committed.
- Generated files identify their generator and overwrite policy where practical.
- Scripts that operate on the repo use `git rev-parse --show-toplevel` or an equivalent `git -C` root lookup.

## Skill Contract

Every root skill must include:

- `SKILL.md` with `name`, `version`, and `description` frontmatter.
- `README.md`.
- Four role files under `agents/`.
- Body of knowledge and JSON knowledge graph.
- Primary, meta, quick, and deep prompts.
- Output template.
- Eval suite.
- Example input and output.

## First-Use Layer

The post-clone protocol is implemented as docs, agents, skills, commands, scripts, and evals:

- Docs: `docs/FIRST_USE_ONBOARDING.md`, `docs/WORKSPACE_SETUP.md`.
- Agents: `first-use-onboarding-agent`, `workspace-diagnostic-agent`, `runtime-routing-agent`, `task-intake-agent`.
- Skills: `first-use-onboarding`, `workspace-setup`, `runtime-routing`, `prompting-and-meta-prompting`, `safe-scripting-and-bash`.
- Scripts: `diagnose-first-use.py`, `setup-workspace-profile.py`, `validate-onboarding.py`, `check-devkit-readiness.py`.
- Evals: `evals/onboarding/evals.json`.

## Quality Gates

```bash
python3 scripts/scaffold-skill.py --name scaffold-smoke-test --description "Smoke test skill" --triggers smoke-test --allowed-tools Read,Grep --owner "JM Labs" --version 0.1.0 --dry-run
python3 scripts/validate-skills.py --strict
python3 scripts/count-components.py --check-docs
bash scripts/check-repo-boundaries.sh
python3 scripts/validate-onboarding.py
python3 scripts/check-devkit-readiness.py
bash scripts/generate-pristino-index.sh
```

## Architect Katas Layer

The 30 Claude Certified Architect katas ship as `katas-*` skills (one per kata, 5 exam domains) backed by systemic reliability infrastructure:

- Skills: `skills/katas-*` (30 dirs, full 16-file skill contract each).
- Hooks: `scripts/pre-tool-guard.sh` enforces `references/guardrails/tool-policy.json` (hot-reloaded, deterministic deny) — katas 02/03.
- Reliability refs: `references/reliability/{prefix-caching,context-dilution,posttooluse-normalization}.md` — katas 03/10/11.
- Structured output: `references/schemas/annotations.schema.json` + `scripts/post_annotations.py` + `.github/workflows/validate.yml` — katas 05/13.
- Batch: `scripts/batch/batch-runner.py` (Message Batches API + custom_id) — kata 17.
- QA: `scripts/qa/{run-adversarial-tests,run-confidence-fp-tests}.py` — katas 29/30.
- Inventories: `docs/katas/{katas-content.md,practices-inventory.md,skill-inventory.md}`.

## Sync Model

Use `docs/git-sync-local-safe.md` and `scripts/sync-upstream-safe.sh` for GitHub synchronization. The sync script refuses dirty working trees, fetches remotes, fast-forwards only when safe, and never resets hard.
