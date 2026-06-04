# Example Output

## Summary

Memoria reestructurada en tres niveles: raíz de equipo lean con `@imports` (universales), `frontend/CLAUDE.md` y `sap/CLAUDE.md` activados por glob, y la preferencia de pnpm movida a user scope fuera del repo.

## Result (GOOD)

```markdown
# CLAUDE.md (team root, stable cacheable prefix)
@import ~/.claude/CLAUDE.md          # user prefs (pnpm), not versioned

## Rules (universal)
- Conventional commits; never push to main directly.

## Path-scoped rules
- apply to: "frontend/**"  ->  @import ./frontend/CLAUDE.md
- apply to: "sap/**"       ->  @import ./sap/CLAUDE.md
```

```markdown
# frontend/CLAUDE.md (loaded only when work touches frontend/**)
- Use design-system tokens; no inline styles.
```

```markdown
# sap/CLAUDE.md (loaded only when work touches sap/**)
- ABAP custom objects use the Z prefix.
```

## Anti-pattern avoided (ANTI)

```markdown
# CLAUDE.md (ANTI: 600 lines, always loaded, cache thrashing)
- Conventional commits.
- Use design-system tokens.   # only frontend
- ABAP objects use Z prefix.  # only sap
- Prefer pnpm over npm.        # personal pref leaked into repo
```

## Validation

- Separación user / team / module en archivos distintos. ✅
- `@imports` estables, sin valores por-turno en el prefijo. ✅
- Reglas de frontend y sap activadas por glob, no copiadas al raíz. ✅
- Precedencia por subpath documentada (más específico gana). ✅
- Preferencia personal (pnpm) movida a user scope, fuera del repo. ✅
