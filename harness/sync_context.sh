#!/usr/bin/env bash
# Regenerate the SHARED INVARIANTS block in CLAUDE.md (and AGENTS.md if it
# is a regular file, not a symlink) from PROJECT_INVARIANTS.md.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC="PROJECT_INVARIANTS.md"
export BODY="$(awk '/^## /{on=1} on' "$SRC")"
for F in CLAUDE.md AGENTS.md; do
  [[ -L "$F" ]] && continue
  [[ -f "$F" ]] || continue
  awk '
    /<!-- BEGIN SHARED INVARIANTS/ {print; print ENVIRON["BODY"]; skip=1; next}
    /<!-- END SHARED INVARIANTS/ {skip=0}
    !skip {print}' "$F" > "$F.tmp" && mv "$F.tmp" "$F"
  echo "synced: $F"
done
