# JM Agentic Development Kit Alfa

Version: 5.2.0
License: MIT
Repository: https://github.com/JaviMontano/jm-adk-alfa

JM-ADK is a local-first agentic development kit for AI-assisted software work. It packages skills, agents, commands, prompts, workspace governance, guardrails, and validation scripts so a developer can scaffold, run, review, and update agentic workflows without mixing versioned kit files with local state.

## Component Inventory

The authoritative counts come from `python3 scripts/count-components.py`.

| Component | Count |
|---|---:|
| Skills | 600 |
| Agents | 261 |
| Commands | 267 |
| Prompts | 256 |
| Total physical components | 1368 |

## Claude Certified Architect Katas

JM-ADK ships the 30 Claude Certified Architect katas as first-class, executable `katas-*` skills (one per kata) across the 5 exam domains:

| Domain | Weight | Katas |
|---|---|---|
| D1 · Agentic Architecture | 27% | deterministic-agent-loop, pretooluse-guardrails, posttooluse-normalization, hub-and-spoke-isolation, headless-code-review, human-handoff-protocol, adaptive-investigation, multiagent-error-propagation |
| D2 · Tool Design & MCP | 18% | defensive-structured-extraction, mcp-structured-errors, tool-description-quality, mcp-server-configuration, builtin-tool-selection |
| D3 · Claude Code Config | 20% | plan-mode-exploration, hierarchical-claude-memory, path-conditional-rules, custom-commands-skills, session-resume-fork |
| D4 · Prompt & Structured Output | 20% | fewshot-edge-calibration, critical-self-correction, message-batch-processing, validation-retry-feedback, independent-reviewer-multipass, confidence-stratified-sampling, false-positive-criteria |
| D5 · Context & Reliability | 15% | prefix-caching, context-dilution-mitigation, multipass-prompt-chaining, persistent-scratchpad, provenance-preservation |

The katas are backed by systemic reliability infrastructure: a policy-driven `PreToolUse` guard (`references/guardrails/tool-policy.json`), reliability references (`references/reliability/`), a structured-annotation schema + headless CI workflow (`.github/workflows/validate.yml`), a Message Batches runner (`scripts/batch/`), and QA suites (`scripts/qa/`). Source inventories live in `docs/katas/`.

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

Declare which runtimes you will drive the kit from (validated against the known
set: `claude-code`, `claude-desktop`, `claude-cowork`, `codex`, `gemini-cli`,
`antigravity`, `cursor`, `windsurf`, `vscode-copilot`):

```bash
python3 scripts/setup-workspace-profile.py \
  --runtime claude-code \
  --runtime-targets claude-code,claude-desktop,codex,antigravity \
  --apply
```

The profile lives in `.jm-adk.local.json` (schema 2, with `preferredRuntime` +
`runtimeTargets`) and must remain untracked.

## Tool Access (MCP)

The kit ships one MCP server, `workspace-mcp` (Gmail + Google Workspace, OAuth2).
It runs on every supported runtime; the config file and snippet differ per runtime.

```bash
python3 scripts/generate-mcp-configs.py --apply   # write references/mcp/*.example
python3 scripts/validate-mcp-config.py            # check wiring is coherent + secret-free
```

Per-tool × per-runtime wiring (Claude Code, Claude Desktop, Codex, Gemini CLI,
Antigravity, Cursor, Windsurf, VS Code): `docs/runtime-tool-access-matrix.md`.
OAuth setup: `docs/google-workspace-mcp-setup.md`.

## User Context Repo

Alfa includes an in-kit context repo at `user-context/`. It is identified by
`user-context/.jm-adk-context.json`, so it remains recognizable as the user
context area regardless of what files the user later adds there.

Use it for durable user background, preferences, memory, curated `resources/`,
and `personal-skills/` that should survive across workspaces. It is separate
from `workspace/`, which is task runtime state.

```bash
python3 scripts/diagnose-user-context.py --dry-run
python3 scripts/diagnose-personal-skills.py --dry-run
python3 scripts/scaffold-user-context.py --dry-run
```

Personal context content is ignored by git by default. Only the scaffold,
marker, schemas, and docs are tracked.

## Local State

Versioned kit files live in the repo. Local runtime state does not.

Tracked:

- `.jm-adk.json`
- `skills/` for SDK skills only
- `agents/`
- `commands/`
- `prompts/`
- `references/`
- `scripts/`
- `docs/`
- `user-context/` scaffold, markers, schemas, and docs only

Ignored:

- `workspace/` except `workspace/.gitkeep`
- private `user-context/` content
- `user-context/resources/*` private resources
- `user-context/personal-skills/skills/*` private personal skills
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

Create a personal skill without writing into the SDK root `skills/`:

```bash
python3 scripts/scaffold-skill.py --name my-personal-skill --description "Personal skill" --personal --dry-run
python3 scripts/scaffold-skill.py --name my-personal-skill --description "Personal skill" --personal
```

Validate and sync personal skills by copy mirror:

```bash
python3 scripts/validate-skills.py --strict --skills-dir user-context/personal-skills/skills
python3 scripts/sync-personal-skills.py --dry-run
python3 scripts/sync-personal-skills.py --apply
```

Create an experimental local skill without tracking it. This is scratch or mirror cache, not durable source:

```bash
python3 scripts/scaffold-skill.py --name my-experiment --description "Local experiment" --local
```

Add a deterministic `scripts/` contract when the skill needs local automation:

```bash
python3 scripts/scaffold-skill.py \
  --name my-skill \
  --description "Short description" \
  --triggers my-skill \
  --allowed-tools Read,Grep,Glob,Bash \
  --with-script-contract \
  --dry-run
```

## Validate

```bash
python3 scripts/validate-skills.py --strict
python3 scripts/validate-skill-scripts.py --strict --run-checks
python3 scripts/validate-skill-dod.py --skill folio-generator
python3 scripts/validate-skill-dod.py --skill follow-up-email
python3 scripts/validate-skill-dod.py --skill font-optimization
python3 scripts/validate-skill-dod.py --skill form-builder
python3 scripts/validate-skill-dod.py --skill form-engineering
python3 scripts/validate-skill-dod.py --skill form-ux-advanced
python3 scripts/validate-skill-dod.py --skill functional-spec
python3 scripts/validate-skill-dod.py --skill functional-toolbelt
python3 scripts/diagnose-user-context.py --dry-run
python3 scripts/diagnose-personal-skills.py --dry-run
python3 scripts/sync-personal-skills.py --dry-run --target /tmp/alfa-personal-skills-target
python3 scripts/validate-runtime-instructions.py
python3 scripts/validate-mcp-config.py
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
