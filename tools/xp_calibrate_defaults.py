#!/usr/bin/env python3
"""Recalibrate role XP at a realistic mid-fighting target (fight_share=0.5,
~3 combats/scenario = 'occasional fighting' per the shortfall-parity intent).
A role unit does its role AND fights occasionally; we set role_xp so it reaches
L3 at warrior pace. Also reports the full-fighting consequence.
"""
import random, sys
sys.path.insert(0, "C:/src/Advance_Wesnoth_Wars/tools")
from xp_parity_sim import (run_trials, summarize, DEFAULT_ACTION_COUNTS,
                           DEFAULT_THRESHOLD_L1_L2, DEFAULT_THRESHOLD_L2_L3,
                           DEFAULT_SCENARIO_COMBATS)

TRIALS = 8000
KILL_PROB = 0.45
TH_L2 = DEFAULT_THRESHOLD_L1_L2
TH_L3 = DEFAULT_THRESHOLD_L2_L3

war = summarize(run_trials("warrior", DEFAULT_SCENARIO_COMBATS, KILL_PROB, 1,
                           0, 0, TH_L2, TH_L3, TRIALS, True, random.Random(424242)))
war_l3 = war.mean_l3
print(f"Warrior baseline mean L3 = {war_l3:.2f}\n")
print(f"{'role':>6} {'act':>4} | {'rxp':>3} {'midFightL3':>10} {'diff':>6} {'fullFightL3':>11} {'pureL3':>7}")
results = {}
for role in ["scout", "tank", "leader", "buffer"]:
    action_count = DEFAULT_ACTION_COUNTS[role]
    best = None
    for rxp in range(0, 13):
        # fight_share=0.5 -> effective combats = round(5*(0.2+0.8*0.5)) = round(5*0.6)=3
        mid = summarize(run_trials(role, 3, KILL_PROB, 1, rxp, action_count,
                                   TH_L2, TH_L3, TRIALS, False, random.Random(2000 + rxp)))
        diff = abs(mid.mean_l3 - war_l3)
        if best is None or diff < best[0]:
            best = (diff, rxp, mid.mean_l3)
    full = summarize(run_trials(role, 5, KILL_PROB, 1, best[1], action_count,
                                TH_L2, TH_L3, TRIALS, False, random.Random(9000 + best[1])))
    pure = summarize(run_trials(role, 1, KILL_PROB, 1, best[1], action_count,
                                TH_L2, TH_L3, TRIALS, False, random.Random(5000 + best[1])))
    results[role] = (best[1], best[2], full.mean_l3, pure.mean_l3)
    print(f"{role:>6} {action_count:>4} | {best[1]:>3} {best[2]:>10.2f} {abs(best[2]-war_l3):>6.2f} {full.mean_l3:>11.2f} {pure.mean_l3:>7.2f}")

print("\nPROPOSED DEFAULT ROLE XP (mid-fight parity):")
for role in ["scout", "tank", "leader", "buffer"]:
    print(f"  {role}: {results[role][0]}")
