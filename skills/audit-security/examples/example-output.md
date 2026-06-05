# Example Output

## Summary

| Metric | Value |
|---|---:|
| Target root | `evals/fixtures/security-sample-plugin` |
| Overall status | blocked |
| Total findings | 7 |
| CRITICAL | 5 |
| WARNING | 1 |
| INFO | 1 |
| Categories executed | 6 |

## Categories Executed

1. secret_exposure
2. path_security
3. hook_injection
4. sensitive_files
5. script_safety
6. external_network

## Findings

| ID | Category | Severity | Status | Path | Line | Pattern | Evidence | Remediation |
|---|---|---|---|---|---:|---|---|---|
| SEC-001 | secret_exposure | CRITICAL | confirmed | plugin.json | 6 | sk-proj-* | [CODE] Live-looking OpenAI key appears in plugin metadata. | Remove and rotate the secret, then read it from an environment variable. |
| SEC-002 | secret_exposure | INFO | placeholder | README.md | 4 | `<YOUR_TOKEN>` | [DOC] Placeholder token appears in documentation example. | Keep placeholder syntax and avoid real tokens in examples. |
| SEC-003 | path_security | CRITICAL | confirmed | .claude-plugin/plugin.json | 9 | `../` | [CONFIG] Hook command references a parent directory traversal. | Resolve paths under the plugin root and reject parent directory traversal. |
| SEC-004 | path_security | WARNING | confirmed | hooks/hooks.json | 5 | `/Users/` | [CONFIG] Hook path hardcodes a user-specific absolute path. | Use `${CLAUDE_PLUGIN_ROOT}` or a relative plugin-root path. |
| SEC-005 | hook_injection | CRITICAL | confirmed | hooks/hooks.json | 7 | `eval $USER_INPUT` | [CONFIG] Hook command evaluates unquoted user-controlled input. | Remove eval and pass arguments through a quoted array or validated parser. |
| SEC-006 | sensitive_files | CRITICAL | confirmed | credentials.json | 1 | credentials.json | [CODE] Credential file is present inside the plugin root. | Remove the file from the plugin and load credentials from external secret storage. |
| SEC-007 | script_safety | CRITICAL | confirmed | scripts/install.sh | 3 | curl | [CODE] Script downloads executable content without checksum or signature verification. | Pin the download, verify checksum or signature, and fail closed on mismatch. |

## False Positive Notes

- SEC-002: `<YOUR_TOKEN>` is a documentation placeholder, not a live credential.

## Remediation Plan

| Finding | Priority | Action |
|---|---|---|
| SEC-001 | P0 | Rotate the leaked key and remove it from plugin metadata. |
| SEC-003 | P0 | Replace traversal with plugin-root-bounded path resolution. |
| SEC-004 | P2 | Replace user-specific absolute path with `${CLAUDE_PLUGIN_ROOT}`. |
| SEC-005 | P0 | Remove eval and quote user-controlled arguments. |
| SEC-006 | P0 | Remove credential file from distributed plugin artifacts. |
| SEC-007 | P0 | Add checksum or signature verification for downloads. |

## Coverage

| Files scanned | Files skipped | Scope |
|---:|---:|---|
| 9 | 0 | plugin root only; symlink targets outside root are not followed |

## Warnings

None.
