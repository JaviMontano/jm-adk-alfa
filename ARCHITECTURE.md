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
├── user-context/                    # In-kit durable user context repo, scaffold tracked and private content ignored
│   ├── .jm-adk-context.json         # Context repo identity marker
│   ├── _INDICE.md                   # First file to read before loading context
│   ├── context/                     # Durable user background
│   ├── preferences/                 # Stable user preferences
│   ├── memory/                      # User-approved long-lived notes
│   ├── sources/                     # Private source files or source indexes
│   └── schemas/                     # Manifest and context-card schemas
├── .local/                         # Local experiments, ignored
├── references/                     # Ontology and guardrails
├── scripts/                        # Scaffolding, validation, sync, and hooks
├── docs/                           # User and maintainer documentation
└── PRISTINO-INDEX.md               # Generated component index
```

## Upgrade-Safe Boundaries

- Kit core is versioned and reviewable.
- `CLAUDE.md`, `GEMINI.md`, and `AGENTS.md` are homologated runtime mirrors for Claude, Gemini, and Agents families respectively.
- `workspace/` is local session state and must not be committed except `workspace/.gitkeep`.
- `user-context/` is the in-kit durable context repo. Its marker, docs, and schemas are tracked; private user-authored contents are ignored by default.
- `.jm-adk.local.json` is for local configuration and must not be committed.
- `.local/skills/` is for experimental local skills and must not be committed.
- Generated files identify their generator and overwrite policy where practical.
- Scripts that operate on the repo use `git rev-parse --show-toplevel` or an equivalent `git -C` root lookup.

## User Context Layer

`user-context/` is recognized by `user-context/.jm-adk-context.json`, not by the
user files stored inside it. Alfa diagnostics treat it as a context repo as
long as the marker and scaffold contract remain intact.

The layer is separate from `workspace/`: `workspace/` stores task runtime state;
`user-context/` stores durable user-approved context. Agents load `_INDICE.md`
first and then only relevant files.

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

## Sync Model

Use `docs/git-sync-local-safe.md` and `scripts/sync-upstream-safe.sh` for GitHub synchronization. The sync script refuses dirty working trees, fetches remotes, fast-forwards only when safe, and never resets hard.
