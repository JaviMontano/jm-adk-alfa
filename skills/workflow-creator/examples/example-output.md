# Example Output

## Activation Decision

- expected_activation: true
- reason: [EXPLICIT] User requested workflow YAML with DoD, RACI, KPIs,
  fallback, and escalation.
- missing_inputs: none

## Workflow Spec

```yaml
- id: "skill-hardening-handoff"
  title: "Skill Hardening Handoff"
  objective: "Produce a reviewed skill release packet with local validation evidence."
  trigger: "/jm:harden-skill workflow-creator is invoked for one active skill."
  preconditions:
    - "Git status is clean and main matches origin/main before branch creation."
  inputs:
    - name: "skill_slug"
      type: "string"
      required: true
      description: "Kebab-case skill identifier selected for the hardening iteration."
    - name: "baseline_report"
      type: "object"
      required: true
      description: "Preflight status, current branch, open PR list, and failing gates."
  steps:
    - stepNumber: 1
      title: "Confirm Scope"
      desc: "Coordinator confirms exactly one active skill and creates the working branch from origin/main."
      whyThisMatters: "Without a single active skill, unrelated changes can hide regressions and make PR review ambiguous."
      inputNeeded: "skill_slug:string and baseline_report:object"
      actionInstruction: "Run git status and gh pr list, then record the active skill slug before editing."
      promptToUse: "Confirm the active skill, branch name, and blocking gates. Return JSON with active_skill, branch, and open_prs."
      expectedOutput: "Scope packet with active_skill, branch, open_prs, and baseline_commit fields."
      validationRule: "active_skill equals workflow-creator and open_prs contains no active hardening PR."
      failureSignal: "active_skill missing or open_prs returns another active hardening branch."
      recoveryAction: "Stop and ask for a merge or closure decision before continuing."
      handoffIfNeeded: "coordinator"
    - stepNumber: 2
      title: "Audit Contract"
      desc: "Auditor inspects SKILL.md, evals, examples, assets, and scripts for deterministic gaps."
      whyThisMatters: "Without contract audit, vague scaffold text can pass routing while failing output quality."
      inputNeeded: "skill_slug:string and local file tree"
      actionInstruction: "Read skill files and compare them against validate-skill-dod.py requirements."
      promptToUse: "Audit workflow-creator for scaffold markers, missing assets, weak evals, and uncontrolled dependencies. Return SpokeReport."
      expectedOutput: "SpokeReport with findings, coverage_gaps, recommended_changes, and risk."
      validationRule: "SpokeReport exists and contains at least one finding or explicit no-gap decision."
      failureSignal: "SpokeReport missing findings or returns an empty status."
      recoveryAction: "Retry the audit with narrower file paths and log the missing evidence."
      handoffIfNeeded: "determinism-auditor"
    - stepNumber: 3
      title: "Patch Artifacts"
      desc: "Integrator applies scoped changes to the active skill, review doc, ledger row, and generated indexes."
      whyThisMatters: "Without scoped artifact updates, DoD evidence and catalog metadata drift apart."
      inputNeeded: "HardeningBrief:object and skill files"
      actionInstruction: "Patch only workflow-creator files plus required audit ledger and generated index artifacts."
      promptToUse: "Apply the HardeningBrief. Do not edit any other skill. Preserve existing repo conventions."
      expectedOutput: "Updated assets, evals, examples, scripts, review doc, and ledger row."
      validationRule: "git diff --name-only contains workflow-creator paths and documented audit/index paths only."
      failureSignal: "diff contains another skill path or required workflow-creator artifact missing."
      recoveryAction: "Patch missing artifact or revert only accidental out-of-scope hunks after review."
      handoffIfNeeded: "integrator"
    - stepNumber: 4
      title: "Validate Release"
      desc: "Guardian runs per-skill and repo gates before allowing the PR to open."
      whyThisMatters: "Without independent validation, ledger completion can certify an untested workflow contract."
      inputNeeded: "updated skill tree and review evidence"
      actionInstruction: "Run check.sh, validate-skill-dod.py, validate-skill-scripts.py, and repo gates."
      promptToUse: "Review the evidence and block release if any gate lacks a passing command."
      expectedOutput: "ReleasePacket with commands, results, PR URL, and merge decision."
      validationRule: "ReleasePacket contains local_check passes and dod=pass evidence."
      failureSignal: "Any command returns non-zero exit code or ReleasePacket missing validation evidence."
      recoveryAction: "Stop, patch the failing contract, rerun the failed command, and log the correction."
      handoffIfNeeded: "guardian"
  mainOutput: "ReleasePacket markdown with branch, PR, checks, and merge decision."
  secondaryOutputs:
    - "Updated skill review doc"
    - "Updated skill ledger row"
    - "Validator fixture logs"
  DoD:
    - "Per-skill DoD command passes with dod=pass."
    - "Script contract command passes with warnings=0 errors=0."
    - "Guardian records a release decision with evidence."
  qaChecklist:
    - "All 17 top-level workflow fields are present."
    - "Every step has 12 fields and an observable validation rule."
    - "No other skill directory appears in the implementation diff."
  raci:
    responsible: "integrator"
    accountable: "guardian"
    consulted: "determinism-auditor"
    informed: "coordinator"
  kpis:
    - metric: "local_gate_failures"
      target: "0"
      unit: "count"
      measurement: "Count non-zero exits across required validation commands."
    - metric: "scope_violations"
      target: "0"
      unit: "count"
      measurement: "Count diff paths outside allowed workflow-creator and audit/index files."
  cadence: "per-request"
  errorHandling: "Log the failing command, block ledger completion, and require a corrective patch before PR creation."
  fallbackRoute: "stop-and-ask"
  escalationRoute: "human-maintainer"
```

## Validation Evidence

- [CÓDIGO] Contract: `assets/workflow-definition-contract.json`
- [CÓDIGO] Script: `scripts/validate_workflow_spec.py`
- [CÓDIGO] Local check: `bash skills/workflow-creator/scripts/check.sh`

## Risks And Open Items

- [INFERENCIA] Structural validation does not prove the workflow is strategically
  optimal; it proves the spec is complete, observable, and fail-closed.
