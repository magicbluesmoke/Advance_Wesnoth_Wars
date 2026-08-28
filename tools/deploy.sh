#!/usr/bin/env bash
# Deploy the Advance Wesnoth Wars source tree to the live game add-ons dir.
# Usage: bash tools/deploy.sh
# The game loads add-ons from the Wesnoth userdata add-ons dir (OneDrive-redirected
# here). C:/src/Advance_Wesnoth_Wars is the source of truth / git repo; this script
# MIRRORS the project files there (copies new/changed, deletes destination orphans)
# so the game sees the current state, then verifies with a full tree diff and exits
# non-zero if anything differs.
#
# Uses only git-bash built-ins (no rsync dependency).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEP="${AWW_DEPLOY_DIR:-C:/Users/Michael Anselmi/OneDrive/Documents/My Games/Wesnoth1.18/data/add-ons/Advance_Wesnoth_Wars}"

if [ ! -d "$DEP" ]; then
  echo "ERROR: deployed dir not found: $DEP" >&2
  exit 1
fi

echo "Deploying $REPO -> $DEP"

EXCLUDED=".git _server.ign *.bak"

# Pass 1: copy every project file from the repo into the deployed tree.
cd "$REPO"
find . -type f \
  ! -path './.git/*' \
  ! -name '.git' \
  ! -name '_server.ign' \
  ! -name '*.bak' \
  -print0 | while IFS= read -r -d '' f; do
    rel="${f#./}"
    mkdir -p "$DEP/$(dirname "$rel")"
    cp -f "$f" "$DEP/$rel"
  done

# Pass 2: delete destination files that are NOT in the repo (mirror semantics),
# skipping the same exclusions so we never remove files the repo intentionally
# does not track.
cd "$DEP"
find . -type f \
  ! -name '.git' \
  ! -name '_server.ign' \
  ! -name '*.bak' \
  -print0 | while IFS= read -r -d '' f; do
    rel="${f#./}"
    if [ ! -e "$REPO/$rel" ]; then
      rm -f "$f"
    fi
  done

echo "Verifying parity..."
if diff -rq --exclude=.git --exclude='_server.ign' --exclude='*.bak' "$REPO" "$DEP" >/dev/null 2>&1; then
  echo "OK: repo and deployed tree are identical."
else
  echo "WARNING: trees differ after deploy. Inspect:" >&2
  diff -rq --exclude=.git --exclude='_server.ign' --exclude='*.bak' "$REPO" "$DEP" 2>&1 | head -20 || true
  exit 2
fi
