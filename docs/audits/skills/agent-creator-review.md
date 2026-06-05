# Skill Review: agent-creator

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/agent-creator`.
- [CONFIG] Review date: 2026-06-04.
- [CONFIG] Remote ledger row is intentionally deferred; this PR does not modify
  `docs/audits/skill-review-ledger.csv`.

## DoD Evidence

- [CODE] `assets/manifest.json` lists every local asset and validates each
  consumer path.
- [CODE] `assets/agent-spec-schema.json` defines required structured sections
  for custom agent compilation.
- [CODE] `assets/tool-policy.json` rejects wildcard or inherited-all tool
  access and defines least-privilege tiers.
- [CODE] `assets/model-selection-policy.json` maps simple, balanced, and deep
  work to `haiku`, `sonnet`, and `opus`.
- [CODE] `assets/description-trigger-policy.json` forces trigger-focused
  descriptions and negative triggers.
- [CODE] `assets/agent-template.md` defines the canonical Markdown section
  order.
- [CODE] `scripts/compile-agent.py` validates local JSON and renders Markdown
  or stable JSON offline without API, network, MCP, or live registry calls.
- [CODE] `scripts/check.sh` validates one positive compiled agent and negative
  fixtures for built-in name collision, wildcard tools, missing triggers, and
  missing negative boundaries.
- [CODE] `evals/evals.json` includes eight concrete cases with `assets`,
  `deterministic_scripts`, and `quality_criteria` checks.
- [CODE] `examples/example-input.md` and `examples/example-output.md` are
  domain-specific and do not retain scaffold placeholders.
- [CODE] `README.md`, `knowledge/body-of-knowledge.md`, prompts, and role
  files now describe custom-agent generation instead of generic scaffold text.

## Validation Commands

```text
python3 -B scripts/validate-skill-dod.py --skill agent-creator
PASS agent-creator: agent-creator fixtures passed
skills_with_scripts=1 warnings=0 errors=0
skill=agent-creator dod=pass errors=0

python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill agent-creator
PASS agent-creator: agent-creator fixtures passed
skills_with_scripts=1 warnings=0 errors=0

bash skills/agent-creator/scripts/check.sh
agent-creator fixtures passed

python3 -B -m py_compile skills/agent-creator/scripts/*.py
PASS
```

## Residual Limits

- [INFERENCE] Offline validation does not prove live `.claude/agents/`
  registry contents, global permissions, or runtime tool availability.
- [INFERENCE] Runtime installation into project or global agent directories
  still requires explicit user-approved write action.
- [INFERENCE] The compiler validates the agent definition contract; the parent
  orchestrator remains responsible for deciding when to spawn it.

## Ledger Completion 2026-06-05

- [CODE] `bash skills/agent-creator/scripts/check.sh` passed in `codex/complete-script-backed-ledger-20260605` validation.
- [CODE] `python3 -B scripts/validate-skill-dod.py --skill agent-creator` passed with `skill=agent-creator dod=pass errors=0`.
- [CODE] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill agent-creator` passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CONFIG] `docs/audits/skill-review-ledger.csv` now records `agent-creator` as `dod-complete`.
