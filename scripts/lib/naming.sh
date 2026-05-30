#!/bin/bash
# naming.sh — canonical naming standard (v1.0.0). Single source of truth.
#
# Source it for functions, or run as CLI:
#   bash scripts/lib/naming.sh slugify "Build a landing page for MetodologIA" [maxwords]
#   bash scripts/lib/naming.sh is-kebab "my-slug"            # exit 0/1
#   bash scripts/lib/naming.sh validate-filename "Report.md"  # exit 0/1, prints suggestion
#
# Standard:
#   - kebab-case ^[a-z0-9]+(-[a-z0-9]+)*$, accents transliterated (á→a, ñ→n)
#   - drop ES+EN stopwords + leading filler action-verbs
#   - preserve intent order (mnemonic), dedupe consecutive words
#   - ≤ maxwords (default 5) significant words, ≤ 40 chars
#
# Pure python3 under the hood for determinism. No external deps.

_NAMING_PY() {
python3 - "$@" <<'PY'
import sys, re, unicodedata

STOPWORDS = {
    # EN
    "a","an","the","for","of","to","and","or","in","on","with","that","this",
    "is","are","be","at","by","from","as","it","its",
    # ES
    "el","la","los","las","un","una","unos","unas","de","del","para","por",
    "y","o","en","con","que","al","lo","su","sus","mi","tu",
}
# Leading filler action-verbs (dropped only when not the sole token).
LEAD_VERBS = {
    "build","create","make","do","add","update","fix","setup","set",
    "hacer","crear","construir","generar","armar","montar","poner","agregar",
    "actualizar","arreglar","configurar",
}

def transliterate(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))

def slugify(text: str, maxwords: int = 5) -> str:
    text = transliterate(text).lower()
    tokens = [t for t in re.split(r"[^a-z0-9]+", text) if t]
    tokens = [t for t in tokens if t not in STOPWORDS]
    # Drop leading filler verbs (keep at least one token).
    while len(tokens) > 1 and tokens[0] in LEAD_VERBS:
        tokens.pop(0)
    # Dedupe consecutive duplicates.
    deduped = []
    for t in tokens:
        if not deduped or deduped[-1] != t:
            deduped.append(t)
    deduped = deduped[:maxwords]
    slug = "-".join(deduped)[:40].strip("-")
    return slug or "unnamed"

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Filenames allowed regardless of kebab (governance / conventional).
ALLOW_EXACT = {
    "CLAUDE.md","README.md","SKILL.md","AGENTS.md","GEMINI.md","CODEX.md",
    "ANTIGRAVITY.md","MEMORY.md","TAREAS.md","LICENSE","CHANGELOG.md",
    "CONTRIBUTING.md","SECURITY.md","ARCHITECTURE.md","PRISTINO.md",
    "PRISTINO-INDEX.md","_INDICE.md","_ESTRUCTURA.md","_DASHBOARD.md",
    "INSTRUCCIONES-PROYECTO.md","PROTOCOLO-CIERRE-SESION.md",
}
def allowed_filename(name: str) -> bool:
    if name in ALLOW_EXACT: return True
    if name.startswith("."): return True          # dotfiles
    if name.startswith("_TEMPLATE-"): return True  # templates
    if name.endswith(".gitkeep"): return True
    return False

def is_kebab_filename(name: str) -> bool:
    # Split a single trailing extension; stem must be kebab, ext lowercase alnum.
    if "." in name:
        stem, ext = name.rsplit(".", 1)
        if not re.match(r"^[a-z0-9]+$", ext): return False
    else:
        stem = name
    return bool(KEBAB.match(stem))

cmd = sys.argv[1] if len(sys.argv) > 1 else ""
arg = sys.argv[2] if len(sys.argv) > 2 else ""
extra = sys.argv[3] if len(sys.argv) > 3 else ""

if cmd == "slugify":
    mw = int(extra) if extra.isdigit() else 5
    print(slugify(arg, mw))
elif cmd == "is-kebab":
    sys.exit(0 if KEBAB.match(arg) else 1)
elif cmd == "validate-filename":
    if allowed_filename(arg) or is_kebab_filename(arg):
        sys.exit(0)
    # Suggest a compliant name.
    if "." in arg:
        stem, ext = arg.rsplit(".", 1)
        print("%s.%s" % (slugify(stem), ext.lower()))
    else:
        print(slugify(arg))
    sys.exit(1)
else:
    sys.stderr.write("usage: naming.sh {slugify|is-kebab|validate-filename} <arg> [maxwords]\n")
    sys.exit(2)
PY
}

slugify()           { _NAMING_PY slugify "$1" "${2:-5}"; }
is_kebab()          { _NAMING_PY is-kebab "$1"; }
validate_filename() { _NAMING_PY validate-filename "$1"; }

# CLI dispatch when executed directly.
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  case "${1:-}" in
    slugify)           _NAMING_PY slugify "${2:-}" "${3:-5}";;
    is-kebab)          _NAMING_PY is-kebab "${2:-}";;
    validate-filename) _NAMING_PY validate-filename "${2:-}";;
    *) echo "usage: naming.sh {slugify|is-kebab|validate-filename} <arg> [maxwords]" >&2; exit 2;;
  esac
fi
