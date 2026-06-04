# Custom Tooling Extension Plan: {name}

## Summary

- Artifact: `{artifactType}`.
- Trigger: `{trigger}`.
- Scope: `{scopeType}`.
- Path: `{path}`.
- Context fork: `{contextFork}`.
- Mutates: `{mutates}`.

## Interface

- Description: {description}
- Argument hint: `{argumentHint}`

## Security

- Allowed tools: `{allowedTools}`.
- Bash justification: {bashJustification}

## Generated Skeleton

```yaml
{frontmatter}
```

## Validation

- Artifact matches trigger.
- Scope matches replication.
- `context: fork` is present for non-trivial skills.
- `allowed-tools` is minimal and explicit.
- `argument-hint` and `description` are present.
- Permanent conventions stay in `CLAUDE.md`.

## Risks

{risksMarkdown}
