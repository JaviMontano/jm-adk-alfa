# Guardrails Management Scripts

`check.sh` validates guardrail operation packets offline. It accepts confirmed
store/deactivate and unconfirmed proposal packets, and rejects unconfirmed
persistence, wrong target files, duplicate active rules, missing verifiable
checks, and deletion-based removals.
