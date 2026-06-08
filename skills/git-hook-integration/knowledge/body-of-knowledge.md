# Git Hook Integration — Body of Knowledge

## Canon

Git hooks should make repository hygiene repeatable while staying transparent to
contributors. This skill treats hooks as an integration plan first: it renders
the exact hook stages, commands, blocking behavior, and installation guardrails
before any mutation is attempted.

## Required Hook Coverage

| Stage | Responsibility | Minimum Gate |
|-------|----------------|--------------|
| `pre-commit` | Fast local checks before a commit is created | whitespace, forbidden paths, or fast lint |
| `commit-msg` | Commit header policy | Conventional Commit validator |
| `pre-push` | Slower publication checks | component counts, strict skill validation, tests |

Use `assets/hook-stage-model.json` as the stage source of truth. The compiler
fails if any required stage is absent.

## Deterministic Planning Contract

Use `assets/git-hook-integration-schema.json` for structured input. Required
root fields are repository identity, hook manager, install mode, hook directory,
hook list, Conventional Commit policy, validation commands, and evidence.

The supported hook managers are:

- `native-git` for `.githooks` plus `git config core.hooksPath .githooks`.
- `pre-commit` when a Python-oriented hook framework is already desired.
- `husky` when a Node.js project already uses npm lifecycle tooling.
- `lefthook` when cross-language teams need a fast declarative runner.

Default install mode is `plan-only`. Use `dry-run` or `apply-after-review` only
when the user explicitly asks to prepare installation steps.

## Conventional Commit Policy

When Conventional Commits are enabled, the hook plan must include a blocking
`commit-msg` hook. The bundled policy in
`assets/conventional-commit-policy.json` defines allowed types, header length,
examples, and rejection patterns.

## Repository Safety

- Prefer repository-local hook configuration over global Git config.
- Never overwrite existing hook files without backup or explicit confirmation.
- Document bypass policy for `--no-verify` or any `SKIP` variable.
- Keep hook commands project-local and inspectable.
- Treat generated hook plans as reviewable artifacts, not hidden automation.

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Required stage coverage | 100% | `compile-git-hook-integration.py` rejects missing stages |
| Commit policy coverage | 100% when enabled | Commit-msg hook exists and policy fields validate |
| Evidence coverage | 100% | Evidence section contains tagged repository facts |
| Mutation safety | 100% | Output states install mode and non-destructive guardrails |

## References

- `assets/git-hook-integration-schema.json`
- `assets/hook-stage-model.json`
- `assets/conventional-commit-policy.json`
- `assets/install-strategy-model.json`
- `assets/validation-command-catalog.json`
- `scripts/compile-git-hook-integration.py`
