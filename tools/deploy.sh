#!/usr/bin/env bash
# Deploy the Advance Wesnoth Wars source tree to the live game add-ons dir.
# Usage: bash tools/deploy.sh
# The game loads add-ons from the Wesnoth userdata add-ons dir (OneDrive-redirected
# here). C:/src/Advance_Wesnoth_Wars is the source of truth / git repo; this script
# copies the project files there so the game sees the current state, then verifies
# with a full tree diff and exits non-zero if anything differs.
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

# Copy all project files (tracked + untracked), excluding VCS/backup artifacts.
# First clear the destination of previous stray artifacts, then copy over.
find "$DEP" -type f \
  \( -name '*.bak' -o -name '_server.ign' -o -name '.git' \) -delete 2>/dev/null || true

# Copy every file under the repo (respecting exclusions) into the deployed tree.
cd "$REPO"
find . -type f \
  ! -path './.git/*' \
  ! -name '*.bak' \
  ! -name '_server.ign' \
  ! -name '.git' \
  -print0 | while IFS= read -r -d '' f; do
    rel="${f#./}"
    mkdir -p "$DEP/$(dirname "$rel")"
    cp -f "$f" "$DEP/$rel"
  done

echo "Verifying parity..."
if diff -rq --exclude=.git --exclude='_server.ign' --exclude='*.bak' "$REPO" "$DEP" >/dev/null 2>&1; then
  echo "OK: repo and deployed tree are identical."
else
  echo "WARNING: trees differ after deploy. Inspect:" >&2
  diff -rq --exclude=.git --exclude='_server.ign' --exclude='*.bak' "$REPO" "$DEP" 2>&1 | head -20 || true
  exit 2
fi
