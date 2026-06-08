---
name: github-actions-ci
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Designs deterministic GitHub Actions CI/CD workflow plans with pinned
  actions, least-privilege permissions, cache keys, matrix strategy, secrets,
  environments, deployment gates, validation, and evidence handoff. [EXPLICIT]
  Trigger: "GitHub Actions", "CI/CD", "CI pipeline", "deploy workflow"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# GitHub Actions CI/CD

> "If it is not automated, it is not reliable."

## TL;DR

Use this skill when creating, reviewing, or hardening GitHub Actions workflows
for lint, test, build, package, deploy, release, or quality gate automation.
[EXPLICIT]

The output must be a verifiable workflow plan, not just YAML prose. It must
define triggers, job graph, permissions, pinned third-party actions, dependency
caching, matrix strategy, secrets, environment protection, concurrency, and
validation evidence before claiming the pipeline is ready. [EXPLICIT]

## Procedure

### Step 1: Discover Pipeline Surface

- Inspect existing `.github/workflows/`, package manifests, lockfiles, test
  commands, build commands, deploy targets, environments, and branch policy.
- Record which facts are observed from files and which are assumptions.

### Step 2: Design Deterministic Workflow

- Use `assets/ci-workflow-contract.json` for required output fields.
- Use `assets/triggers-policy.json`, `assets/permissions-policy.json`,
  `assets/action-pinning-policy.json`, `assets/cache-policy.json`, and
  `assets/matrix-policy.json` to define deterministic workflow behavior.
- Use `assets/secrets-policy.json` and `assets/deployment-policy.json` before
  adding deploy jobs.

### Step 3: Block Unsafe Patterns

- Do not use broad repository permissions unless a job-specific reason is
  recorded.
- Do not use unpinned third-party actions in release or deploy workflows.
- Do not write secrets into workflow YAML.
- Do not deploy from pull_request events or unprotected branches.
- Do not mark CI ready without validation commands and expected checks.

### Step 4: Validate And Handoff

- Validate structured JSON workflow plans with
  `scripts/validate_github_actions_ci.py` or `scripts/check.sh`.
- For YAML implementation, preserve the same contract in the review summary.
- Mark the pipeline ready only when local validation evidence and required
  workflow protections are documented.

## Quality Criteria

- [ ] Trigger policy is explicit for PR, push, manual, schedule, or release.
- [ ] Every job has a purpose, runner, dependency graph, permissions, and
  validation command.
- [ ] Third-party actions are pinned to immutable SHA references when required.
- [ ] Cache keys include dependency lockfile or equivalent invalidation source.
- [ ] Matrix entries are bounded and justified.
- [ ] Secrets are referenced by name only and never embedded as values.
- [ ] Deploy jobs use protected environments, branch gates, and concurrency.
- [ ] Evidence tags are applied to user-facing factual claims.

## Usage

Example invocations:

- "/github-actions-ci" - Build a deterministic CI workflow plan.
- "Review this GitHub Actions workflow for unsafe permissions."
- "Add matrix tests and cache policy to this pipeline."
- "Validate this CI workflow JSON before creating YAML."

## Assumptions & Limits

- Assumes access to project artifacts, workflow YAML, or a supplied pipeline
  plan. [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not create repository secrets or environment approvals by itself.
  [EXPLICIT]
- Does not claim a GitHub-hosted workflow passed without CI evidence. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Produce a missing-evidence report and do not emit ready YAML |
| Deploy requested from PR | Block deploy and require protected branch or manual gate |
| Missing lockfile for cache | Disable cache or require explicit invalidation source |
| Unpinned third-party action | Block release/deploy readiness until pinned |
| Secret value supplied inline | Remove value, reference secret name only, and flag risk |
| Matrix too broad | Bound versions and explain coverage tradeoff |
