# Security Pattern Catalog for Plugin Auditing

Human-readable mirror of `assets/scan-policy.json`. The JSON asset is the
source of truth for validators.

## Secret Exposure

| Pattern | Severity | Notes |
|---|---|---|
| `sk-*`, `sk-proj-*` | CRITICAL | Redact full value in prose evidence |
| `AKIA[0-9A-Z]{16}` | CRITICAL | Treat live-looking AWS keys as leaked credentials |
| `ghp_*`, `xox[bsp]-*` | CRITICAL | Treat GitHub and Slack tokens as leaked credentials |
| `<YOUR_TOKEN>`, `${API_KEY}`, `sk-REPLACE_ME` | INFO | Placeholder only when context is docs/examples |
| Private key headers | CRITICAL | Any `BEGIN ... PRIVATE KEY` marker |

## Path Security

| Pattern | Severity | Notes |
|---|---|---|
| `../` in executable hook/script context | CRITICAL | Parent traversal must be blocked |
| `/Users/`, `/home/`, `C:\` in hook paths | WARNING | Replace with plugin-root-relative paths |

## Hook Injection

| Pattern | Severity | Recommendation |
|---|---|---|
| `eval` | CRITICAL | Avoid eval; use arrays or validated arguments |
| Backticks | CRITICAL | Avoid shell substitution in hook commands |
| Unquoted `$VAR` in hook command | CRITICAL | Quote variables or pass structured arguments |
| `curl ... | sh` or `bash` | CRITICAL | Avoid piping remote content to shells |

## Sensitive Files

| Pattern | Severity |
|---|---|
| `.env`, `.env.*` | CRITICAL |
| `credentials.json`, `service-account.json` | CRITICAL |
| `*.pem`, `*.key`, `*.p12`, `*.pfx` | CRITICAL |
| `id_rsa`, `id_ed25519` | CRITICAL |

## Script Safety

| Pattern | Severity | Recommendation |
|---|---|---|
| `curl`/`wget` without checksum or signature verification | CRITICAL | Verify checksum or signature |
| `chmod 777` | WARNING | Use least privilege permissions |
| World-writable script mode | WARNING | Remove `o+w` permissions |

## External Network

| Context | Severity |
|---|---|
| External URL in executable hook or install script | CRITICAL unless verified and expected |
| Metadata homepage/repository URL | INFO |
| Documentation example URL | INFO |
