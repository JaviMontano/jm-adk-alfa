# git-workflow Assets

These assets define deterministic policy for Git workflow plans.

- `workflow-plan-contract.json`: required report fields, decision statuses, evidence tags, and moving-time terms.
- `command-policy.json`: allowed command prefixes and forbidden destructive command patterns.
- `branch-policy.json`: branch types, protected bases, and branch naming pattern.
- `release-policy.json`: release tag strategies and SemVer tag pattern.

The offline validator uses these files with fixtures in `scripts/fixtures/`.
