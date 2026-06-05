# Example Input

Create a project-local agent named `dependency-auditor`.

It should review package manifests for dependency freshness, known
vulnerabilities, and license risk. It should only read files and run safe
inspection commands. It should produce a compact report with package, current
version, risk, evidence, and recommended action. Use `sonnet` unless you see a
stronger reason.
