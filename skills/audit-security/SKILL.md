---
name: audit-security
version: 1.0.1
author: JM Labs (Javier Montaño)
description: >
  Performs a deterministic read-only static security audit for plugin artifacts,
  detecting secret exposure, path security issues, hook injection, sensitive
  files, script safety problems, and external network risks. [EXPLICIT]
  Trigger: audit security, security scan, check for secrets, find vulnerabilities,
  plugin security audit, leaked key scan. [EXPLICIT]
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Audit Security

Performs a read-only static security audit of plugin artifacts. The output is a
severity-classified report with exact file evidence, false-positive handling,
remediation actions, coverage, and validator-backed structure. [EXPLICIT]

## Deterministic Assets

Use these local files before producing or reviewing a security report:

| Path | Use |
|---|---|
| `assets/activation-policy.json` | Activation, clarification, false-positive, and refusal routing |
| `assets/scan-policy.json` | Six scan categories, severities, statuses, and placeholder policy |
| `assets/report-contract.json` | Required report sections and fields |
| `assets/evidence-policy.json` | Evidence and remediation requirements |
| `references/security-patterns.md` | Human-readable security pattern catalog |
| `scripts/validate_security_report.py` | Offline JSON report validator |
| `scripts/check.sh` | Deterministic positive and negative fixture check |

The validator reads only local JSON files. It does not call the network,
current time, random sources, model providers, or MCP tools. [EXPLICIT]

## When To Activate

Activate when the user asks to audit, scan, review, or check a plugin, skill
bundle, hook directory, or explicit file list for security issues. [EXPLICIT]

Do not activate for generic cybersecurity advice, code review, factuality
review, content quality, legal compliance, or non-plugin application security
unless the user supplies a static plugin/file target. [EXPLICIT]

Refuse requests to exploit, weaponize, exfiltrate, or bypass security controls.
[EXPLICIT]

If no target path or file list is supplied, ask for `plugin_root_or_file_list`
instead of inventing a scope. [EXPLICIT]

## Scan Taxonomy

Execute exactly these six categories from `assets/scan-policy.json`:

1. `secret_exposure`
2. `path_security`
3. `hook_injection`
4. `sensitive_files`
5. `script_safety`
6. `external_network`

Every report must list all six categories, even when a category has zero
findings. [EXPLICIT]

## Severity Policy

Use only `CRITICAL`, `WARNING`, and `INFO`.

- `CRITICAL`: live secret exposure, parent-directory traversal in executable
  context, hook command injection, sensitive credential files, or unvalidated
  executable downloads.
- `WARNING`: hardcoded absolute user paths or unsafe script posture that does
  not directly expose credentials or execute untrusted input.
- `INFO`: placeholders, documentation-only examples, metadata URLs, or manual
  review notes.

Placeholder/example secrets such as `<YOUR_TOKEN>`, `${API_KEY}`,
`sk-REPLACE_ME`, and `AKIAEXAMPLE` must be `INFO` with status `placeholder`,
not `CRITICAL`. [EXPLICIT]

## Procedure

1. Confirm activation with `assets/activation-policy.json`.
2. Confirm the target root or explicit file list is inside the requested scope.
3. Execute all six scan categories with static inspection only.
4. For every finding, record stable ID `SEC-NNN`, category, severity, status,
   path, line, pattern, evidence, and remediation.
5. Redact live secrets in prose evidence when needed; preserve enough pattern
   context for remediation.
6. Add remediation plan entries for every `CRITICAL` and `WARNING` finding.
7. Add false-positive notes for placeholders and documentation-only examples.
8. Report coverage: files scanned, files skipped, and scan scope.
9. Validate JSON reports with `scripts/validate_security_report.py` when a
   machine-readable artifact is produced.

## Output Contract

Markdown output must include:

1. `Summary`
2. `Categories Executed`
3. `Findings`
4. `False Positive Notes`
5. `Remediation Plan`
6. `Coverage`
7. `Warnings`

JSON output must match `assets/report-contract.json`. [EXPLICIT]

## Local Validation

Run the skill check:

```bash
bash skills/audit-security/scripts/check.sh
```

Validate a JSON report:

```bash
python3 -B skills/audit-security/scripts/validate_security_report.py \
  --contract skills/audit-security/assets/report-contract.json \
  --scan-policy skills/audit-security/assets/scan-policy.json \
  --evidence-policy skills/audit-security/assets/evidence-policy.json \
  --report <security-report.json>
```

## Quality Gate

- All six categories are executed and reported in canonical order.
- Every finding has exact path, positive line number, pattern, evidence tag, and
  remediation.
- Finding IDs are `SEC-NNN`, unique, ascending, and gapless.
- Severity counts match findings exactly.
- Placeholder/example secrets are never CRITICAL.
- CRITICAL and WARNING findings have remediation plan entries.
- No target files are modified, deleted, quarantined, or executed.

## Assumptions & Limits

- Read-only. This skill never modifies, deletes, quarantines, or executes target
  files. [EXPLICIT]
- Pattern-based static analysis cannot prove absence of obfuscated or split
  secrets. [EXPLICIT]
- Symlink targets outside the supplied root are out of scope and should be
  reported as skipped rather than followed. [EXPLICIT]
- This skill reports plugin static security posture; runtime exploitation tests
  require a separate, explicitly authorized workflow. [EXPLICIT]
