# GitHub Actions CI/CD - Body of Knowledge

## Canon

GitHub Actions workflow design is ready only when triggers, jobs, permissions,
actions, caches, secrets, environments, deployment gates, and validation
evidence are explicit. YAML that runs is not automatically safe: broad
permissions, mutable action references, inline secrets, unbounded matrices, and
unguarded deploy jobs can turn CI into a release risk.

## Workflow Surfaces

| Surface | Required Decision |
|---------|-------------------|
| Triggers | PR, push, manual, schedule, release, or workflow_call |
| Jobs | Purpose, runner, steps, dependencies, permissions |
| Actions | Official or third-party, pinned reference, purpose |
| Cache | Key, restore keys, lockfile or invalidation source |
| Matrix | Axis, bounded values, allowed failure policy |
| Secrets | Secret names only, job scope, environment scope |
| Deployment | Branch gate, environment, reviewers, concurrency |
| Evidence | Local commands, expected status checks, CI run evidence |

## Safety Invariants

- Default permissions should be `contents: read`.
- Job permissions should be narrower than repository-wide write permissions.
- Third-party actions used in release or deploy workflows should be pinned to
  immutable SHA references.
- Cache keys should include a lockfile hash or equivalent invalidation source.
- Production deploy jobs should not run from `pull_request` events.
- Secret values should never appear in workflow YAML.
- Ready status requires validation commands and expected checks.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Trigger coverage | 100% | Every workflow event is explicit |
| Permission safety | 100% | Every job declares least privilege |
| Pinning coverage | 100% | Required actions have immutable refs |
| Cache determinism | 100% | Cache keys have invalidation source |
| Deploy protection | 100% | Deploy jobs use branch and environment gates |
| Evidence coverage | 100% | Plans include local and CI validation evidence |

## References

- `assets/ci-workflow-contract.json`
- `assets/triggers-policy.json`
- `assets/permissions-policy.json`
- `assets/action-pinning-policy.json`
- `assets/cache-policy.json`
- `assets/matrix-policy.json`
- `assets/secrets-policy.json`
- `assets/deployment-policy.json`
- `assets/evidence-policy.json`
- `scripts/validate_github_actions_ci.py`
