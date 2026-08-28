# AWW Role-XP Calibration Plan

> **For Hermes:** execute this plan task-by-task with the wesnoth-wml-modding skill loaded.
> **Status:** DRAFT — awaiting user decision on calibration philosophy (Task 1).

**Goal:** Rebalance the four non-warrior role-XP channels (scout, tank, leader, buffer) so a unit performing its role levels at approximately the same rate as a warrior relying on native combat XP.

**Architecture:** Two calibration tiers. (a) Derive per-channel values from an explicit accrual model rooted in engine constants (`kill_xp=8*enemy_level`, `combat_xp=1*enemy_level`, awarded once per combat — verified from `src/game_config.cpp` and `src/actions/attack.cpp`). (b) Validate and converge via structured playtest observation, because action frequencies (captures, hits absorbed, supported kills, status applications) are scenario-dependent and cannot be proven by arithmetic alone. Warrior channel stays 0 (native = baseline reference).

**Tech Stack:** Wesnoth 1.18 WML (`[slider]` in `mods/options.cfg`), gates in `macros/status_options.mac.cfg`, `mods/NN_<role>_xp.cfg`, `tools/deploy.sh`, `scripts/verify_wml_chain.py`.

---

### Task 1: Decide calibration philosophy (decision) — RESOLVED

**Decision (2026-08-28):** User approved **Shortfall parity** — scout 8, tank 4, leader 8, buffer 10. Role channel tops up to warrior-native assuming occasional fighting; lowest overleveling risk.

**The tension:** If a role unit ONLY performs its role (never fights), its channel must carry ~9-11 XP/action to match a fighting warrior's ~22.8 XP/scenario. But role units ALSO earn native combat XP when they do fight. Two defensible targets:

- **Shortfall parity (recommended):** role channel tops up to warrior-native, assuming the unit fights occasionally. Derived: scout 8, tank 4, leader 8, buffer 10 (per-action, scenario ~16 turns).
- **Full parity (aggressive):** role-only units match a fighting warrior. Derived: scout 9, tank 5, leader 9, buffer 11.

**Decision inputs:**
- Risk of full parity: role units that DO fight would overlevel badly (channel + native).
- Risk of shortfall: pure-role units (e.g. a scout that only captures) still lag.

**Resolution:** User picks shortfall or full parity (or a middle value). Record choice in CHANGELOG.

---

### Task 2: Update the four slider defaults (work)

**Objective:** Set the four role-XP sliders to the approved values.

**Files:**
- Modify: `C:/src/Advance_Wesnoth_Wars/mods/options.cfg` (lines 165, 176, 187, 198 — scout/tank/leader/buffer `default=`)

**Step 1: Write the failing check**
Confirm current values (scout 4, tank 2, leader 2, buffer 2) are NOT the target:
Run: `grep -n "default=" mods/options.cfg | sed -n '5,8p'`
Expected: current defaults, which will differ from target.

**Step 2: Apply the new defaults**
Patch each slider's `default=` to the approved value. Watch the WML translation-string pitfall: only change the `default=` numeric line, never the `name`/`description` lines. Then update the description text's "Default: N" suffix to match (the warrior one was left stale earlier).

**Step 3: Verify**
Run: `python "C:/Users/Michael Anselmi/AppData/Local/hermes/skills/gaming/wesnoth-wml-modding/scripts/verify_wml_chain.py" "C:/src/Advance_Wesnoth_Wars" 16 20`
Expected: `RESULT: PASS — chain internally consistent`
Also grep that each slider's `default=` now equals the approved value and each description's "Default:" suffix matches.

**Step 4: Deploy + commit**
Run: `bash tools/deploy.sh`
Expected: `OK: repo and deployed tree are identical.`
Then: `git add mods/options.cfg && git commit -m "Rebalance role XP defaults for warrior-native parity"`

---

### Task 3: Structured playtest observation (work + validate)

**Objective:** Measure real per-scenario role-XP accrual to validate the arithmetic model.

**Method (manual, user-driven — the Windows GUI build suppresses headless output):**
1. Launch the game, enable the `[modification]`, play ~3 scenarios of the same map (`4p_Ruvaak_Mirage_Atoll`).
2. For one unit per role (scout, tank, leader, buffer), note XP gained and level-ups across a full scenario.
3. Record in `dev/role_xp_playtest_notes.md` (new file): per-role XP/scenario, action counts, level-ups.

**Acceptance criteria (parity):** each role unit reaches its next level in a comparable number of scenarios to a warrior (~1-2 scenarios for L1 units at the modeled rates).

**Decision gate:** if measured XP deviates >30% from the model, return to Task 2 and re-tune the affected channel(s), then re-test.

---

### Task 4: Regression documentation + skill update (work)

**Objective:** Persist the calibration so it survives future re-tuning.

**Files:**
- Modify: `C:/Users/Michael Anselmi/AppData/Local/hermes/skills/gaming/wesnoth-wml-modding/references/role-xp-channels.md`

**Step 1:** Update the "Balanced default values" section to record the new defaults and the calibration method (engine constants + playtest validation).

**Step 2:** Update `CHANGELOG.md` with the calibration entry.

**Step 3:** Verify the skill reference matches the committed values; commit:
`git add . && git commit -m "docs: record role-XP calibration values and method"`
