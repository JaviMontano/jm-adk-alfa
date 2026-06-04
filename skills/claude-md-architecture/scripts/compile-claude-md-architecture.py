#!/usr/bin/env python3
"""Compile deterministic CLAUDE.md hierarchy reports from structured JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_DIR = SKILL_DIR / "assets"


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_required_fields(obj: dict[str, Any], fields: list[str], label: str, errors: list[str]) -> None:
    for field in fields:
        require(field in obj and obj[field] not in ("", None), f"{label} missing required field: {field}", errors)


def flatten_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for item in value.values():
            strings.extend(flatten_strings(item))
        return strings
    if isinstance(value, list):
        strings = []
        for item in value:
            strings.extend(flatten_strings(item))
        return strings
    return []


def validate_imports(root: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> set[str]:
    imports = [as_dict(item) for item in as_list(root.get("imports"))]
    scopes: set[str] = set()
    allowed_scopes = set(policy["allowedScopes"])
    for index, item in enumerate(imports, start=1):
        label = f"import {index}"
        validate_required_fields(item, schema["requiredImportFields"], label, errors)
        target = str(item.get("target", ""))
        scope = str(item.get("scope", ""))
        scopes.add(scope)
        require(scope in allowed_scopes, f"{label} scope unsupported", errors)
        require(item.get("stable") is True, f"{label} must be stable", errors)
        if scope == "user":
            prefixes = tuple(policy["imports"]["userTargetPrefixes"])
            require(target.startswith(prefixes), f"{label} user import must target user scope", errors)
        if scope == "module":
            require(target.endswith(policy["imports"]["moduleTargetSuffix"]), f"{label} module import must target CLAUDE.md", errors)
    return scopes


def validate_path_scoped_imports(root: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> set[str]:
    imports = [as_dict(item) for item in as_list(root.get("pathScopedImports"))]
    require(bool(imports), "root.pathScopedImports requires at least one module import", errors)
    globs: set[str] = set()
    for index, item in enumerate(imports, start=1):
        label = f"pathScopedImport {index}"
        validate_required_fields(item, schema["requiredPathScopedImportFields"], label, errors)
        glob = str(item.get("glob", ""))
        target = str(item.get("target", ""))
        require(glob.endswith(policy["module"]["requiredGlobSuffix"]), f"{label} glob must end with /**", errors)
        require(target.endswith(policy["imports"]["moduleTargetSuffix"]), f"{label} target must be a module CLAUDE.md", errors)
        require(nonempty(item.get("reason")), f"{label} reason must be non-empty", errors)
        if glob in globs:
            errors.append(f"duplicate path-scoped glob: {glob}")
        globs.add(glob)
    return globs


def validate_root(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> set[str]:
    root = as_dict(spec.get("root"))
    validate_required_fields(root, schema["requiredRootFields"], "root", errors)
    require(root.get("path") == policy["root"]["teamPath"], "root.path must be CLAUDE.md", errors)
    line_count = root.get("lineCount")
    require(isinstance(line_count, int), "root.lineCount must be integer", errors)
    if isinstance(line_count, int):
        require(line_count <= policy["root"]["maxRecommendedLines"], "root CLAUDE.md exceeds maxRecommendedLines", errors)
    require(bool(as_list(root.get("universalRules"))), "root.universalRules requires at least one rule", errors)
    import_scopes = validate_imports(root, schema, policy, errors)
    globs = validate_path_scoped_imports(root, schema, policy, errors)
    for scope in policy["requiredScopes"]:
        if scope == "team":
            continue
        require(scope in import_scopes or (scope == "module" and bool(globs)), f"missing required scope import: {scope}", errors)
    return globs


def validate_modules(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], root_globs: set[str], errors: list[str]) -> None:
    modules = [as_dict(item) for item in as_list(spec.get("modules"))]
    require(len(modules) >= policy["module"]["minCount"], "modules requires at least one entry", errors)
    seen_paths: set[str] = set()
    seen_globs: set[str] = set()
    for index, module in enumerate(modules, start=1):
        label = f"module {index}"
        validate_required_fields(module, schema["requiredModuleFields"], label, errors)
        path = str(module.get("path", ""))
        glob = str(module.get("glob", ""))
        claude_md = str(module.get("claudeMd", ""))
        rules = as_list(module.get("rules"))
        require(bool(re.match(r"^[a-z0-9][a-z0-9_-]*$", str(module.get("name", "")))), f"{label} name must be slug-like", errors)
        require(glob.endswith(policy["module"]["requiredGlobSuffix"]), f"{label} glob must end with /**", errors)
        require(claude_md.endswith(policy["module"]["claudeMdBasename"]), f"{label} claudeMd must end with CLAUDE.md", errors)
        require(claude_md.startswith(path.rstrip("/") + "/"), f"{label} claudeMd must live under module path", errors)
        require(bool(rules), f"{label} requires rules", errors)
        require(glob in root_globs, f"{label} glob missing from root.pathScopedImports", errors)
        if path in seen_paths:
            errors.append(f"duplicate module path: {path}")
        if glob in seen_globs:
            errors.append(f"duplicate module glob: {glob}")
        seen_paths.add(path)
        seen_globs.add(glob)


def validate_user_scope(spec: dict[str, Any], schema: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    user_scope = as_dict(spec.get("userScope"))
    validate_required_fields(user_scope, schema["requiredUserScopeFields"], "userScope", errors)
    prefixes = tuple(policy["imports"]["userTargetPrefixes"])
    require(str(user_scope.get("path", "")).startswith(prefixes), "userScope.path must be under ~/.claude/", errors)
    require(user_scope.get("versionedInRepo") is False, "userScope.versionedInRepo must be false", errors)
    require(bool(as_list(user_scope.get("preferences"))), "userScope.preferences requires at least one preference or explicit empty rationale", errors)


def validate_precedence(spec: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    precedence = as_dict(spec.get("precedence"))
    require(precedence.get("mode") == policy["precedence"]["requiredMode"], "precedence.mode must be most_specific_subpath_wins", errors)
    levels = [str(item) for item in as_list(precedence.get("levels"))]
    for level in policy["precedence"]["minimumLevels"]:
        require(level in levels, f"precedence.levels missing {level}", errors)
    require(nonempty(precedence.get("conflictResolution")), "precedence.conflictResolution must be non-empty", errors)


def validate_cache_policy(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> None:
    cache = as_dict(spec.get("cachePolicy"))
    validate_required_fields(cache, schema["requiredCachePolicyFields"], "cachePolicy", errors)
    require(cache.get("stablePrefix") is True, "cachePolicy.stablePrefix must be true", errors)
    require(cache.get("noTurnSpecificValues") is True, "cachePolicy.noTurnSpecificValues must be true", errors)
    require(cache.get("rootOnlyUniversalRules") is True, "cachePolicy.rootOnlyUniversalRules must be true", errors)


def validate_validation(spec: dict[str, Any], schema: dict[str, Any], errors: list[str]) -> None:
    validation = as_dict(spec.get("validation"))
    validate_required_fields(validation, schema["requiredValidationFields"], "validation", errors)
    for field in schema["requiredValidationFields"]:
        require(validation.get(field) is True, f"validation.{field} must be true", errors)


def validate_antipatterns(spec: dict[str, Any], policy: dict[str, Any], errors: list[str]) -> None:
    joined = "\n".join(flatten_strings(spec)).lower()
    for token in policy["blockedAntiPatterns"]:
        if token in joined:
            errors.append(f"blocked anti-pattern token present: {token}")


def validate(spec: dict[str, Any]) -> None:
    schema = load_json(ASSET_DIR / "architecture-schema.json")
    policy = load_json(ASSET_DIR / "architecture-policy.json")
    errors: list[str] = []
    validate_required_fields(spec, schema["requiredTopLevel"], "architecture", errors)
    if errors:
        raise ValueError("\n".join(errors))
    require(nonempty(spec.get("repo")), "repo must be non-empty", errors)
    root_globs = validate_root(spec, schema, policy, errors)
    validate_modules(spec, schema, policy, root_globs, errors)
    validate_user_scope(spec, schema, policy, errors)
    validate_precedence(spec, policy, errors)
    validate_cache_policy(spec, schema, errors)
    validate_validation(spec, schema, errors)
    require(bool(as_list(spec.get("risks"))), "risks requires at least one item", errors)
    validate_antipatterns(spec, policy, errors)
    if errors:
        raise ValueError("\n".join(errors))


def bullet_list(items: list[Any]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_root_markdown(spec: dict[str, Any]) -> str:
    root = spec["root"]
    lines = [
        "# CLAUDE.md",
        "",
        "## Imports",
    ]
    for item in root["imports"]:
        lines.append(f"@import {item['target']}")
    lines.extend(["", "## Universal Rules", bullet_list(root["universalRules"]), "", "## Path-Scoped Rules"])
    for item in root["pathScopedImports"]:
        lines.append(f"- apply to: \"{item['glob']}\" -> @import {item['target']} ({item['reason']})")
    precedence = spec["precedence"]
    lines.extend(
        [
            "",
            "## Precedence",
            f"- Mode: `{precedence['mode']}`",
            f"- Order: {' -> '.join(precedence['levels'])}",
            f"- Conflict resolution: {precedence['conflictResolution']}",
        ]
    )
    return "\n".join(lines)


def render_module_markdown(module: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"### {module['claudeMd']}",
            "",
            "```markdown",
            f"# {module['claudeMd']}",
            "",
            f"apply to: \"{module['glob']}\"",
            "",
            "## Module Rules",
            bullet_list(module["rules"]),
            "```",
        ]
    )


def render_report(spec: dict[str, Any]) -> str:
    template = (ASSET_DIR / "architecture-report-template.md").read_text(encoding="utf-8")
    root_markdown = render_root_markdown(spec)
    module_markdown = "\n\n".join(render_module_markdown(item) for item in spec["modules"])
    return template.format(
        repo=spec["repo"],
        rootPath=spec["root"]["path"],
        rootLineCount=spec["root"]["lineCount"],
        moduleNames=", ".join(item["name"] for item in spec["modules"]),
        userScopePath=spec["userScope"]["path"],
        precedenceMode=spec["precedence"]["mode"],
        rootMarkdown=root_markdown,
        moduleMarkdown=module_markdown,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a CLAUDE.md architecture contract")
    parser.add_argument("input", type=Path, help="Path to architecture JSON contract")
    parser.add_argument("--output", type=Path, help="Write generated report")
    args = parser.parse_args()
    try:
        spec = load_json(args.input)
        validate(spec)
        report = render_report(spec)
        if args.output:
            args.output.write_text(report, encoding="utf-8")
        else:
            print(report)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
