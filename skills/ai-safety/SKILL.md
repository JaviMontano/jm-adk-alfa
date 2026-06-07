---
name: ai-safety
author: JM Labs (Javier Montaño)
version: 1.0.1
description: >
  Designs deterministic AI safety controls for content filters, output
  guardrails, jailbreak prevention, safety evaluation, escalation, and residual
  risk reporting. Use this skill when the user asks for "AI safety",
  "output guardrails", "content filters", "jailbreak prevention", "safety
  evaluation", or "unsafe output mitigation". [EXPLICIT]
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# AI Safety

## TL;DR

Produce a source-backed AI safety report with risk taxonomy, control coverage,
jailbreak tests, evaluation metrics, escalation policy, and residual risks.

## Procedure

### Step 1: Scope The System
- Identify use case, user groups, high-stakes status, and known harm domains. [EXPLICIT]
- Create evidence ids before recommending controls. [EXPLICIT]

### Step 2: Assess Risks
- Classify each risk using `assets/risk-taxonomy.json`. [EXPLICIT]
- Assign severity and scenario text; do not collapse critical risks into generic warnings. [EXPLICIT]

### Step 3: Map Controls
- Map every risk id to at least one control from `assets/control-policy.json`. [EXPLICIT]
- Critical risks cannot use `allow` as the only action. [EXPLICIT]

### Step 4: Test And Evaluate
- Define jailbreak tests from `assets/jailbreak-policy.json`. [EXPLICIT]
- Define evaluation metrics from `assets/evaluation-policy.json`. [EXPLICIT]
- Run `bash skills/ai-safety/scripts/check.sh` when scripts are present. [EXPLICIT]

## Quality Criteria

- [ ] Evidence ids support risks, controls, tests, metrics, and escalation. [EXPLICIT]
- [ ] Every risk has at least one mapped control. [EXPLICIT]
- [ ] Jailbreak coverage exists for jailbreak or prompt-injection risk. [EXPLICIT]
- [ ] Evaluation includes unsafe recall, over-refusal, and jailbreak block rate. [EXPLICIT]
- [ ] Escalation policy has owner, channels, and criteria. [EXPLICIT]

## Deterministic DoD Assets

- `assets/safety-report-contract.json` defines the report schema and required checks. [EXPLICIT]
- `assets/risk-taxonomy.json` defines harm domains and severity values. [EXPLICIT]
- `assets/control-policy.json` defines allowed control types and actions. [EXPLICIT]
- `assets/jailbreak-policy.json` defines allowed attack types and expected actions. [EXPLICIT]
- `assets/evaluation-policy.json` defines required safety metrics. [EXPLICIT]
- `scripts/validate_ai_safety_report.py` validates fixtures offline. [EXPLICIT]

## Limits

- This skill designs and validates safety report packets offline. [EXPLICIT]
- It does not certify a live model as safe. [EXPLICIT]
- Legal, medical, financial, or emergency escalation requires human owner review. [EXPLICIT]
