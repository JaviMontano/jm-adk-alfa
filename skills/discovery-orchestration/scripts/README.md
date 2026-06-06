# Discovery Orchestration Scripts

`check.sh` validates deterministic orchestration packet fixtures offline. It
accepts ready and blocked pipelines with explicit evidence, and rejects missing
gates, dependency cycles, unvalidated ready deliverables, missing owners, and
moving time language.
