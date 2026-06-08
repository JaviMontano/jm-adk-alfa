---
name: health-check-automation
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Designs deterministic health checks for services, dependencies, resources,
  alerts, degradation states, and evidence handoff. [EXPLICIT]
  Trigger: "health check automation"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Health Check Automation

> "Method over hacks."

## TL;DR

Use this skill when a project needs a deterministic health-check plan, status
snapshot, dependency monitor, resource threshold policy, or alert handoff.
[EXPLICIT]

The output must separate observed health from inferred risk, name every check,
bind each check to an offline-verifiable threshold where possible, and define
alert routing plus degradation behavior before claiming the system is healthy.
[EXPLICIT]

## Procedure

### Step 1: Inventory Health Surface

- Identify services, dependencies, jobs, storage, queues, credentials,
  scheduled tasks, and resource limits that belong in the health surface.
- Record which signals are observed, synthetic, or unavailable.

### Step 2: Define Deterministic Checks

- Use `assets/health-check-contract.json` for required output fields.
- Use `assets/service-policy.json`, `assets/dependency-policy.json`, and
  `assets/resource-policy.json` to define status, severity, threshold, and
  evidence requirements.
- Avoid live network assumptions unless the caller supplies captured evidence.

### Step 3: Classify Status And Alerts

- Classify each check as `pass`, `warn`, `fail`, or `unknown`.
- Use `assets/alert-policy.json` to map severity, owner, trigger, and handoff.
- Use `assets/degradation-policy.json` when any required check is unavailable,
  stale, or failing.

### Step 4: Validate And Handoff

- Validate structured JSON health reports with
  `scripts/validate_health_check.py` or `scripts/check.sh`.
- Mark overall status `healthy` only when all required checks pass and evidence
  is present.
- Record residual risk for skipped optional checks or stale snapshots.

## Quality Criteria

- [ ] Health surface is explicit and scoped.
- [ ] Required checks have deterministic thresholds.
- [ ] Dependencies include owner, expected status, and failure behavior.
- [ ] Resource checks include units, warning thresholds, critical thresholds,
  and observed values.
- [ ] Alerts include severity, owner, trigger, and handoff evidence.
- [ ] Unknown or stale evidence cannot produce an overall healthy decision.
- [ ] Evidence tags are applied to user-facing factual claims.

## Usage

Example invocations:

- "/health-check-automation" - Build a deterministic health-check plan.
- "Create health checks for this service and its dependencies."
- "Validate this health report JSON before marking the release healthy."
- "Design alerts for resource usage and degraded dependency status."

## Assumptions & Limits

- Assumes access to project artifacts, supplied telemetry, or captured health
  snapshots. [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not perform live monitoring by itself. [EXPLICIT]
- Does not claim production health without provided evidence. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Produce a required evidence list and block healthy status |
| Live system unavailable | Mark unavailable checks `unknown` or `fail` based on evidence |
| Stale snapshot | Block healthy status and request fresh evidence |
| Optional dependency missing | Mark degraded only if policy says optional failure affects service |
| Alert owner missing | Block alert readiness until owner and handoff are defined |
| Conflicting thresholds | Use the stricter threshold and flag the conflict |
