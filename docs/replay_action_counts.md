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

## Measured counts
Source: `https://replays.wesnoth.org/1.18/` (verified reachable).

Downloaded 6 MP replays from `2026/08/29/`:
- `4p__Isars_Cross_Turn_8_(7707).bz2`
- `4p_-_Isar's_Blasphemy_(Survival)_Turn_11_(7712).bz2`
- `4p__Underworld_Turn_7_(7610).bz2`
- `4p__Siege_Castles_Turn_1_(7631).bz2`
- `4p__Loris_River_Turn_5_(7593).bz2`
- `4p__Blue_Water_Province_Turn_12_(7573).bz2`

Decompressed with `bunzip2` to WML; parsed `[replay]` blocks. Counted:
- `[attack]` tags (all attacks).
- `[capture_village]` tags.
- Attacks with slow/poison/petrify markers.

Results:
| replay | attacks | captures | buffer-ish attacks |
|---|---|---|---|
| 4p - Isar's Blasphemy | 194 | 0 | 0 |
| 4p Blue Water Province | 103 | 0 | 0 |
| 4p Isar's Cross | 47 | 0 | 0 |
| 4p Loris River | 4 | 0 | 0 |
| 4p Siege Castles | 0 | 0 | 0 |
| 4p Underworld | 36 | 0 | 0 |

Aggregate:
- attacks: mean 64, range 0-194
- captures: mean 0, range 0-0
- buffer attacks: mean 0, range 0-0

Notes:
- `[capture_village]` events were not present in this sampled replay set; these files appear to be partial/turn-based extracts rather than full-game replays.
- slow/poison/petrify markers were not detectable in available replay tags.
- leadership-aura adjacency cannot be inferred from this replay format.

## Honest blocker / remaining work
The current public sample is too incomplete to produce scenario-level role distributions. Next needed step: identify and parse full-completed `.bz2` replays where `[capture_village]` and richer attack metadata are present.
