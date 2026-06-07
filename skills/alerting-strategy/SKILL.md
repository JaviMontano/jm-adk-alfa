---
name: alerting-strategy
author: JM Labs (Javier Montaño)
version: 1.0.1
description: >
  Alert fatigue prevention, escalation rules, severity classification. [EXPLICIT]
  Trigger: "alerting strategy"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Alerting Strategy
> "Method over hacks."
## TL;DR
Alert fatigue prevention, escalation rules, severity classification. [EXPLICIT]

## Deterministic Hardening Contract

This skill must produce an alerting strategy that can be checked offline without network, wall-clock, or random dependencies. Use `assets/` as the contract source:

- `assets/alerting-strategy-contract.json`: required report sections and validation checks.
- `assets/severity-policy.json`: allowed severity levels and response targets.
- `assets/rule-policy.json`: alert rule fields and threshold requirements.
- `assets/escalation-policy.json`: ownership, routing, and escalation requirements.
- `assets/fatigue-policy.json`: deduplication, suppression, grouping, and review cadence controls.
- `assets/evidence-policy.json`: allowed evidence tags and provenance rules.

If a JSON alerting strategy is requested or used as handoff, validate it with `scripts/validate_alerting_strategy.py`. The fixture smoke test is `bash skills/alerting-strategy/scripts/check.sh`. [EXPLICIT]
## Procedure
### Step 1: Discover
- Gather context and requirements
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV
### Step 3: Execute
- Implement with evidence tags
### Step 4: Validate
- Verify quality criteria met
## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output

## Usage

Example invocations:

- "/alerting-strategy" — Run the full alerting strategy workflow
- "alerting strategy on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
