# Workflow Definition Packet

## Activation Decision

- expected_activation: {{expected_activation}}
- reason: {{activation_reason}}
- missing_inputs: {{missing_inputs}}

## Workflow Spec

```yaml
- id: "{{id}}"
  title: "{{title}}"
  objective: "{{objective}}"
  trigger: "{{trigger}}"
  preconditions:
    - "{{precondition}}"
  inputs:
    - name: "{{input_name}}"
      type: "{{input_type}}"
      required: true
      description: "{{input_description}}"
  steps:
    - stepNumber: 1
      title: "{{step_title}}"
      desc: "{{step_desc}}"
      whyThisMatters: "{{why_this_matters}}"
      inputNeeded: "{{input_needed}}"
      actionInstruction: "{{action_instruction}}"
      promptToUse: "{{prompt_to_use}}"
      expectedOutput: "{{expected_output}}"
      validationRule: "{{validation_rule}}"
      failureSignal: "{{failure_signal}}"
      recoveryAction: "{{recovery_action}}"
      handoffIfNeeded: "{{handoff}}"
  mainOutput: "{{main_output}}"
  secondaryOutputs:
    - "{{secondary_output}}"
  DoD:
    - "{{dod_item}}"
  qaChecklist:
    - "{{qa_item}}"
  raci:
    responsible: "{{responsible}}"
    accountable: "{{accountable}}"
    consulted: "{{consulted}}"
    informed: "{{informed}}"
  kpis:
    - metric: "{{metric}}"
      target: "{{target}}"
      unit: "{{unit}}"
      measurement: "{{measurement}}"
  cadence: "{{cadence}}"
  errorHandling: "{{error_handling}}"
  fallbackRoute: "{{fallback_route}}"
  escalationRoute: "{{escalation_route}}"
```

## Validation Evidence

- contract: assets/workflow-definition-contract.json
- quality_gates: assets/quality-gates.json
- local_check: {{local_check}}

## Risks And Open Items

- {{risk_or_open_item}}
