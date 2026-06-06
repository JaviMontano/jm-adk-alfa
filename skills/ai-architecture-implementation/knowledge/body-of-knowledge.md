# AI Architecture Implementation Body of Knowledge

Implementation transforms an approved AI architecture or audit roadmap into phased production capability. It does not replace architecture design and does not audit existing systems.

## Required Phases

| id | phase | required output |
|----|-------|-----------------|
| F0 | Foundation | repo, CI skeleton, environments, secrets policy |
| F1 | Data Pipeline | ingestion, quality gates, feature consistency |
| F2 | Model Lifecycle | training, evaluation, registry, staging |
| F3 | Serving | API, auth, fallback, load test |
| F4 | CI/CD | Blue & Gold, canary, validation gates, rollback |
| F5 | Monitoring | infra, app, model, data, drift alerts, runbooks |

## Evidence Rule

Each phase and decision needs evidence or a stated prerequisite. Missing inputs become risks; they must not be invented.

## Production Rule

Production plans require CI/CD, monitoring, rollback, and runbooks. If any are out of scope, validation status must be `warn` or `block`.
