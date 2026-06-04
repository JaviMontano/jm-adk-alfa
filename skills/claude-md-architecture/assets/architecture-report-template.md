# Claude Md Architecture Report: {repo}

## Summary

- Root: `{rootPath}` with `{rootLineCount}` lines.
- Modules: `{moduleNames}`.
- User scope: `{userScopePath}`.
- Precedence: `{precedenceMode}`.

## Root CLAUDE.md

```markdown
{rootMarkdown}
```

## Module Files

{moduleMarkdown}

## Validation

- Scopes are separated.
- Path-scoped imports are declared by glob.
- Personal preferences stay outside the versioned repo.
- Most-specific subpath precedence is documented.
- Root prefix stays cache-friendly.
