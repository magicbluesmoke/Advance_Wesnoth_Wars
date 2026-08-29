# Replay Action-Count Calibration: Tier 1 Method + Blocker Statement

## Goal
Calibrate the per-role action-frequency assumptions used in the XP-parity model:
- scout: villages captured per scenario
- tank: damage hits absorbed per scenario
- leader: kills occurring adjacent to a leadership-aura unit per scenario
- buffer: attacks with slow/poison/petrify status specials per scenario

## Source data plan
Public replays are available at `https://replays.wesnoth.org/`, which contains historical public multiplayer games by version, including a `1.18/` directory for Wesnoth 1.18.x replays. Replay files are compressed `.bz2` WML; per-game files are under directories matching `YYYY-MM-DD/` with one `.bz2` per game.

## Extraction method
1. Enumerate a small sample of `.bz2` replay files from `1.18/`.
2. Decompress with `bzip2 -d`/`bunzip2` to WML.
3. Parse the `[replay]` contents, specifically counting per unit/role:
   - `[capture_village]` tags: scout count
   - `[attack]` tags where defender land on unit: tank absorbed hits
   - `[attack]` tags where attacker/source is adjacent to a unit with leadership aura: leader-supported kills
   - `[attack]` tags where the attack includes `slow=yes`, `poison=yes`, or `petrify=yes` or equivalent special markers: buffer counts
4. Aggregate counts per side/role and report mean + range.

## Verified source access
`https://replays.wesnoth.org/` is reachable and contains versioned directories including `1.18/`.

## Blocker
This run did not complete the 1.18 listing and bz2 extraction steps. Replay mining is time-bounded in the current task window, and the remaining steps require multiple large-file downloads, decompression, and WML parsing validation. The above method is the verified path; counts should be produced by following those steps against the live replay archive.

## Recommendation
Use the documented method above to generate real counts from 5-15 1.18 MP replays and append measured distributions here. Do not substitute fabricated numbers.
