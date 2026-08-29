#!/usr/bin/env python3
"""Sensitivity sweep: does the 'roles lead warriors' finding hold across
kill_prob and action-frequency assumptions?"""
import random, sys
sys.path.insert(0, "C:/src/Advance_Wesnoth_Wars/tools")
from xp_parity_sim import (run_trials, summarize, DEFAULT_ROLE_XP,
                           DEFAULT_ACTION_COUNTS, DEFAULT_THRESHOLD_L1_L2,
                           DEFAULT_THRESHOLD_L2_L3, DEFAULT_SCENARIO_COMBATS)

TRIALS = 5000
TH_L2 = DEFAULT_THRESHOLD_L1_L2
TH_L3 = DEFAULT_THRESHOLD_L2_L3

roles = ["scout", "tank", "leader", "buffer"]

print(f"{'kill_prob':>9} {'act_scale':>9} | {'role':>6} {'meanL2':>7} {'meanL3':>7} {'warL3':>6} {'deltaL3':>7}")
for kill_prob in [0.30, 0.45, 0.60]:
    for act_scale in [0.5, 1.0, 2.0]:
        base = random.Random(12345)
        war = summarize(run_trials("warrior", DEFAULT_SCENARIO_COMBATS, kill_prob, 1,
                                   0, 0, TH_L2, TH_L3, TRIALS, True, base))
        for role in roles:
            rng = random.Random(6789)
            rxp = DEFAULT_ROLE_XP[role]
            acnt = DEFAULT_ACTION_COUNTS[role] * act_scale
            res = summarize(run_trials(role, DEFAULT_SCENARIO_COMBATS, kill_prob, 1,
                                       rxp, acnt, TH_L2, TH_L3, TRIALS, False, rng))
            delta = res.mean_l3 - war.mean_l3
            print(f"{kill_prob:>9.2f} {act_scale:>9.1f} | {role:>6} {res.mean_l2:>7.2f} {res.mean_l3:>7.2f} {war.mean_l3:>6.2f} {delta:>7.2f}")
print("deltaL3 < 0 = role reaches L3 FASTER than warrior (overlevels)")
