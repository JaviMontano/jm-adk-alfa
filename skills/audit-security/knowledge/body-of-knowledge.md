# Audit Security Body of Knowledge

## Canon

Audit Security is a read-only static audit for plugin artifacts. It reports
observable security risks without executing target code, modifying target files,
or following out-of-scope symlink targets.

## Scan Categories

| Category | Purpose |
|---|---|
| `secret_exposure` | Live-looking credentials, private keys, tokens, and placeholder handling |
| `path_security` | Parent traversal and user-specific absolute paths |
| `hook_injection` | `eval`, backticks, unquoted variables, and shell execution risks in hooks |
| `sensitive_files` | Credential files that should not ship in a plugin bundle |
| `script_safety` | Unsafe permissions, unvalidated downloads, and risky script commands |
| `external_network` | URLs and network operations in executable contexts |

## Evidence Tags

| Tag | Meaning |
|---|---|
| `[CODE]` | Local file content, script content, or command output |
| `[CONFIG]` | Plugin metadata, hooks, manifests, or policy assets |
| `[DOC]` | Documentation-only example or human-readable reference |
| `[INFERENCE]` | Reviewer conclusion from static evidence |

## Invariants

- Every report lists all six categories.
- Finding IDs are stable `SEC-NNN` values.
- Severity counts must match findings exactly.
- Placeholders are INFO with status `placeholder`.
- CRITICAL and WARNING findings require remediation plan entries.
- Security evidence should redact live secrets in prose.

## Anti-Patterns

- Treating placeholder examples as live leaks.
- Marking every match CRITICAL without context.
- Omitting file paths or line numbers.
- Producing a clean report without listing category coverage.
- Executing hook commands during a static audit.
