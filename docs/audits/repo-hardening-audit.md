# Repo Hardening Audit

Date: 2026-05-28
Branch: `hardening/skill-scaffold-sync-safe`
Target: `https://github.com/JaviMontano/jm-adk-alfa`

## Architecture Map

- Versioned kit core: root docs, `.jm-adk.json`, `.claude-plugin/`, `.github/`, `scripts/`, `agents/`, `commands/`, `prompts/`, `skills/`, and `references/`.
- Local state: `workspace/` is intended as session state and currently tracked only through `workspace/.gitkeep`.
- Compatibility mirror: `.agent/` contains Antigravity-oriented architecture, 102 mirrored skills, 11 workflows, and a BM25 index/search implementation.
- Governance references: `references/ontology/` contains constitution and orchestration protocols; `references/guardrails/` contains JSON guardrail rules.
- Automation: root `scripts/` contains workspace/session hooks, prompt guards, index generation, skill enrichment, adapters, and canonical sync helpers.

## Real Component Counts

Measured from the clean local clone before implementation:

| Component | Count |
|---|---:|
| Root skills with `SKILL.md` | 524 |
| Root agents in `agents/*.md` | 256 |
| Root commands in `commands/*.md` | 260 |
| Top-level prompt files in `prompts/*/*.md` | 256 |
| `.agent/skills` directories | 102 |
| `.agent/workflows/*.md` | 11 |

## Document Inconsistencies

- `README.md` advertises `264 skills`, `1036 componentes`, and version `v5.1.0`.
- `AGENTS.md`, `GEMINI.md`, and `ARCHITECTURE.md` advertise `264 skills`.
- `CLAUDE.md` and `PRISTINO-INDEX.md` advertise `524 skills`.
- `.claude-plugin/plugin.json` describes `512 skills` and points to `jm-agentic-development-kit-alfa`, while the target repo is `jm-adk-alfa`.
- `.jm-adk.json` uses `version: 4.0.0`, while the plugin manifest uses `5.1.0` and Pristino identifies as `v6.0`.
- `ARCHITECTURE.md` lists `hooks/hooks.json`, `templates/`, `.shared/`, and `settings.json`, but the current tree only confirms `hooks/hooks.json`; `templates/`, `.shared/`, and `settings.json` are absent.

## Generated vs Source Files

- Generated or generated-like: `PRISTINO-INDEX.md`, `.agent/skills_index.json`, workspace runtime files, and scaffold-generated skill support files.
- Source/manual: `SKILL.md`, root docs, command docs, agent docs, ontology, guardrails, and existing skill knowledge/templates.
- Existing generated files do not consistently carry machine-readable generated metadata.

## `.gitignore` State

- Already ignored: `.env`, `.env.local`, `.env.*.local`, logs, `.cache/`, build outputs, Firebase state, and `workspace/*` with `workspace/.gitkeep` preserved.
- Missing or incomplete: `.jm-adk.local.json`, `.codex/`, `.local/`, Python caches, backup files, temp directories, coverage output, and local test artifacts.

## Clone and Repo Boundary Risks

- No nested `.git/` directories were found outside the root during preflight.
- The repo currently has no automated boundary checker to block nested clones, tracked local state, tracked `.env` files, or accidental clone folders inside the kit.
- `workspace/.gitkeep` is tracked intentionally, but every other workspace path should stay local.

## Local Pull and Upgrade Risks

- `workspace/` is correctly treated as local state, but `.jm-adk.local.json` is not yet documented or ignored.
- Existing scripts can create or update files without uniform dry-run and overwrite policy.
- Count drift across docs makes upgrades ambiguous because users cannot tell which generated index is authoritative.
- Manual skill files and generated scaffold files are not consistently distinguished.

## Reusable Scripts

- `scripts/generate-pristino-index.sh` can regenerate the master index but uses shell parsing and direct writes.
- `scripts/enrich-skill.sh` creates partial skill support assets but skips already enriched skills and lacks dry-run/force/local modes.
- `.agent/scripts/generate_index.py` scans skills and creates `.agent/skills_index.json`.
- `.agent/scripts/validate_skills.py` validates basic skill frontmatter and content shape for `.agent` or root skills.
- `scripts/workspace-manager.sh` already centralizes workspace runtime writes.

## Tests and CI

- `.github/workflows/validate.yml` validates selected JSON, component minimum counts, frontmatter basics, internal links, and a lightweight secret pattern scan.
- CI currently checks minimum thresholds instead of exact documented count consistency.
- CI does not run strict skill structure validation, repo boundary checks, or scaffold dry-run tests.
- ShellCheck is not used conditionally.

## Skill Scaffolding Gaps

Measured before migration across 524 root skills:

| Required artifact | Missing |
|---|---:|
| `README.md` | 524 |
| `agents/lead.md` | 22 |
| `agents/support.md` | 22 |
| `agents/guardian.md` | 22 |
| `agents/specialist.md` | 22 |
| `knowledge/body-of-knowledge.md` | 34 |
| `knowledge/knowledge-graph.json` | 524 |
| `prompts/primary.md` | 41 |
| `prompts/meta.md` | 41 |
| `prompts/variations/quick.md` | 41 |
| `prompts/variations/deep.md` | 33 |
| `templates/output.md` | 524 |
| `evals/evals.json` | 35 |
| `examples/example-input.md` | 524 |
| `examples/example-output.md` | 524 |

## Recommended Remediation

- Add a stdlib scaffold generator with dry-run default, force-required overwrite, and local skill mode.
- Add strict validators for required files, frontmatter, JSON validity, duplicate risky triggers, allowed tools, links, counts, and repo boundaries.
- Normalize docs and manifests to current real counts.
- Generate missing-only canonical scaffold files for all existing root skills, preserving existing manual files.
- Add safe upstream sync documentation and script that refuses dirty working trees and only fast-forwards when safe.
