# GitHub Actions CI/CD - Knowledge Graph

## Core Concepts

- [[pipeline-surface]] defines workflows, commands, languages, environments, and
  deploy targets.
- [[trigger-policy]] maps events to safe job execution.
- [[job-graph]] defines jobs, dependencies, runners, and validation commands.
- [[permission-boundary]] limits repository and job permissions.
- [[action-pinning]] protects workflows from mutable third-party code.
- [[cache-contract]] defines deterministic dependency caching.
- [[secret-boundary]] keeps secret names separate from secret values.
- [[deployment-gate]] protects release and production jobs.
- [[validation-evidence]] proves local and CI readiness.

## Flow

- [[pipeline-surface]] -> [[trigger-policy]]
- [[trigger-policy]] -> [[job-graph]]
- [[job-graph]] -> [[permission-boundary]]
- [[job-graph]] -> [[action-pinning]]
- [[job-graph]] -> [[cache-contract]]
- [[secret-boundary]] -> [[deployment-gate]]
- [[deployment-gate]] -> [[validation-evidence]]
- [[job-graph]] -> [[validation-evidence]]
