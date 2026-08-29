#!/usr/bin/env python3
"""Monte Carlo XP-parity simulator for AWW role-XP channels."""
from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


DEFAULT_TRIALS = 10_000
DEFAULT_SCENARIO_COMBATS = 5
DEFAULT_SCENARIO_KILLS = 2
DEFAULT_ENEMY_LEVEL = 1
DEFAULT_KILL_XP = 8
DEFAULT_SURVIVE_XP = 1
DEFAULT_THRESHOLD_L1_L2 = 50
DEFAULT_THRESHOLD_L2_L3 = 90
DEFAULT_ROLE_XP: Dict[str, int] = {
    "scout": 8,
    "tank": 4,
    "leader": 8,
    "buffer": 10,
    "warrior": 0,
}
DEFAULT_ACTION_COUNTS: Dict[str, float] = {
    "scout": 2.5,
    "tank": 5,
    "leader": 2.5,
    "buffer": 2,
}


@dataclass
class TrialResult:
    scenarios_to_l2: int
    scenarios_to_l3: int
    reached_l2: bool
    reached_l3: bool


@dataclass
class RoleStats:
    mean_l2: float
    p50_l2: float
    mean_l3: float
    p50_l3: float
    frac_reach_l2: float
    frac_reach_l3: float


def sample_poisson(lam: float, rng: random.Random) -> int:
    # Knuth algorithm for small lambda; bounded cap for safety.
    if lam <= 0:
        return 0
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while True:
        k += 1
        p *= rng.random()
        if p <= L:
            return k - 1
        if k > 10000:
            return k - 1


def xp_per_scenario(
    role: str,
    combats: int,
    kills: int,
    enemy_level: int,
    role_xp_per_action: int,
    action_count: float,
    warrior_mode: bool,
    rng: random.Random,
) -> float:
    combat_xp = kills * (enemy_level * DEFAULT_KILL_XP) + max(0, combats - kills) * (enemy_level * DEFAULT_SURVIVE_XP)
    if warrior_mode:
        return float(combat_xp)
    sampled_actions = max(0.0, rng.gauss(action_count, math.sqrt(max(action_count, 0.5))))
    return float(combat_xp + role_xp_per_action * sampled_actions)


def run_trials(
    role: str,
    combats: int,
    kills: int,
    enemy_level: int,
    role_xp_per_action: int,
    action_count: float,
    threshold_l1_l2: int,
    threshold_l2_l3: int,
    trials: int,
    warrior_mode: bool,
    rng: random.Random,
) -> List[TrialResult]:
    results: List[TrialResult] = []
    for _ in range(trials):
        xp = 0.0
        scenarios = 0
        reached_l2 = False
        reached_l3 = False
        scenarios_to_l2 = 0
        scenarios_to_l3 = 0
        while not reached_l3 and scenarios < 2000:
            xp += xp_per_scenario(
                role=role,
                combats=combats,
                kills=kills,
                enemy_level=enemy_level,
                role_xp_per_action=role_xp_per_action,
                action_count=action_count,
                warrior_mode=warrior_mode,
                rng=rng,
            )
            scenarios += 1
            if not reached_l2 and xp >= threshold_l1_l2:
                reached_l2 = True
                scenarios_to_l2 = scenarios
            if reached_l2 and not reached_l3 and xp >= threshold_l1_l2 + threshold_l2_l3:
                reached_l3 = True
                scenarios_to_l3 = scenarios
        results.append(
            TrialResult(
                scenarios_to_l2=scenarios_to_l2,
                scenarios_to_l3=scenarios_to_l3,
                reached_l2=reached_l2,
                reached_l3=reached_l3,
            )
        )
    return results


def summarize(results: List[TrialResult]) -> RoleStats:
    l2_vals = [r.scenarios_to_l2 for r in results if r.reached_l2]
    l3_vals = [r.scenarios_to_l3 for r in results if r.reached_l3]
    return RoleStats(
        mean_l2=mean(l2_vals),
        p50_l2=quantile(l2_vals, 0.5),
        mean_l3=mean(l3_vals),
        p50_l3=quantile(l3_vals, 0.5),
        frac_reach_l2=sum(1 for r in results if r.reached_l2) / len(results),
        frac_reach_l3=sum(1 for r in results if r.reached_l3) / len(results),
    )


def mean(values: List[int]) -> float:
    return sum(values) / len(values) if values else math.nan


def quantile(values: List[int], q: float) -> float:
    if not values:
        return math.nan
    s = sorted(values)
    idx = (len(s) - 1) * q
    lo = int(math.floor(idx))
    hi = min(lo + 1, len(s) - 1)
    frac = idx - lo
    return s[lo] + frac * (s[hi] - s[lo])


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AWW role XP parity Monte Carlo simulator")
    p.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    p.add_argument("--combats", type=int, default=DEFAULT_SCENARIO_COMBATS)
    p.add_argument("--kills", type=int, default=DEFAULT_SCENARIO_KILLS)
    p.add_argument("--enemy-level", type=int, default=DEFAULT_ENEMY_LEVEL)
    p.add_argument("--role-xp", type=str, default=None, help="JSON object role->xp")
    p.add_argument("--action-counts", type=str, default=None, help="JSON object role->actions per scenario")
    p.add_argument("--threshold-l1-l2", type=int, default=DEFAULT_THRESHOLD_L1_L2)
    p.add_argument("--threshold-l2-l3", type=int, default=DEFAULT_THRESHOLD_L2_L3)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--report", type=str, default="C:/src/Advance_Wesnoth_Wars/docs/role_xp_sim_report.md")
    return p.parse_args()


def run_spectrum(
    role: str,
    base_action: float,
    trials: int,
    combats: int,
    kill_prob: float,
    enemy_level: int,
    role_xp_per_action: int,
    threshold_l1_l2: int,
    threshold_l2_l3: int,
    rng: random.Random,
) -> List[Tuple[str, RoleStats]]:
    out: List[Tuple[str, RoleStats]] = []
    for fight_share in [0.0, 0.25, 0.5, 0.75, 1.0]:
        label = f"fight_share={fight_share:.0%}"
        effective_combats = max(1, round(combats * (0.2 + 0.8 * fight_share)))
        # Use a local RNG child to keep trials independent across spectrum points.
        local_rng = random.Random(rng.randint(0, 2**32 - 1))
        res = run_trials(
            role=role,
            combats=effective_combats,
            kills=0,
            enemy_level=enemy_level,
            role_xp_per_action=role_xp_per_action,
            action_count=base_action,
            threshold_l1_l2=threshold_l1_l2,
            threshold_l2_l3=threshold_l2_l3,
            trials=trials,
            warrior_mode=False,
            rng=local_rng,
        )
        out.append((label, summarize(res)))
    return out


def build_report(
    trials: int,
    combats: int,
    kill_prob: float,
    enemy_level: int,
    role_xp: Dict[str, int],
    action_counts: Dict[str, float],
    threshold_l1_l2: int,
    threshold_l2_l3: int,
    spectrum: Dict[str, List[Tuple[str, RoleStats]]],
    warrior_stats: RoleStats,
) -> str:
    lines: List[str] = []
    lines.append("# Role XP Parity Simulation Report")
    lines.append("")
    lines.append(f"Trials: {trials:,}  \nCombat model: {combats} combats, kill_prob={kill_prob:.0%}, enemy_level={enemy_level}  ")
    lines.append(f"Advancement thresholds: L1->L2={threshold_l1_l2}, L2->L3={threshold_l2_l3}")
    lines.append("")
    lines.append("## Warrior baseline")
    lines.append("")
    lines.append(f"- Mean scenarios to L2: {warrior_stats.mean_l2:.2f}")
    lines.append(f"- P50 scenarios to L2: {warrior_stats.p50_l2:.1f}")
    lines.append(f"- Mean scenarios to L3: {warrior_stats.mean_l3:.2f}")
    lines.append(f"- P50 scenarios to L3: {warrior_stats.p50_l3:.1f}")
    lines.append("")
    lines.append("## Role summary vs warrior")
    lines.append("")
    lines.append("| Role | Mean L2 | P50 L2 | Mean L3 | P50 L3 | Parity verdict |")
    lines.append("| --- | ---: | ---: | ---: | ---: | --- |")
    for role in ["scout", "tank", "leader", "buffer"]:
        stats = spectrum[role][-1][1]
        verdict = parity_verdict(stats, warrior_stats)
        lines.append(
            f"| {role} | {stats.mean_l2:.2f} | {stats.p50_l2:.1f} | {stats.mean_l3:.2f} | {stats.p50_l3:.1f} | {verdict} |"
        )
    lines.append("")
    lines.append("## Spectrum table (pure-role -> role+full-fighting)")
    lines.append("")
    for role in ["scout", "tank", "leader", "buffer"]:
        lines.append(f"### {role}")
        lines.append("")
        lines.append("| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |")
        lines.append("| --- | ---: | ---: | ---: | ---: |")
        for label, stats in spectrum[role]:
            lines.append(
                f"| {label} | {stats.mean_l2:.2f} | {stats.p50_l2:.1f} | {stats.mean_l3:.2f} | {stats.p50_l3:.1f} |"
            )
        lines.append("")
    return "\n".join(lines)


def parity_verdict(role_stats: RoleStats, warrior_stats: RoleStats) -> str:
    diff_l2 = role_stats.mean_l2 - warrior_stats.mean_l2
    diff_l3 = role_stats.mean_l3 - warrior_stats.mean_l3
    if math.isnan(diff_l3):
        return "unknown"
    if diff_l3 <= 1.0:
        return "keeps up"
    if diff_l3 > 3.0:
        return "falls behind"
    return "slightly behind"


def main() -> int:
    args = parse_args()
    rng = random.Random(args.seed)

    role_xp = DEFAULT_ROLE_XP
    if args.role_xp:
        role_xp.update(json.loads(args.role_xp))

    action_counts = DEFAULT_ACTION_COUNTS
    if args.action_counts:
        action_counts.update(json.loads(args.action_counts))

    warrior_results = run_trials(
        role="warrior",
        combats=args.combats,
        kills=0,
        enemy_level=args.enemy_level,
        role_xp_per_action=0,
        action_count=0,
        threshold_l1_l2=args.threshold_l1_l2,
        threshold_l2_l3=args.threshold_l2_l3,
        trials=args.trials,
        warrior_mode=True,
        rng=rng,
    )
    warrior_stats = summarize(warrior_results)

    spectrum: Dict[str, List[Tuple[str, RoleStats]]] = {}
    for role in ["scout", "tank", "leader", "buffer"]:
        spectrum[role] = run_spectrum(
            role=role,
            base_action=action_counts.get(role, 0),
            trials=args.trials,
            combats=args.combats,
            kill_prob=args.kills,
            enemy_level=args.enemy_level,
            threshold_l1_l2=args.threshold_l1_l2,
            threshold_l2_l3=args.threshold_l2_l3,
            rng=rng,
        )

    report = build_report(
        trials=args.trials,
        combats=args.combats,
        kill_prob=args.kills,
        enemy_level=args.enemy_level,
        role_xp=role_xp,
        action_counts=action_counts,
        threshold_l1_l2=args.threshold_l1_l2,
        threshold_l2_l3=args.threshold_l2_l3,
        spectrum=spectrum,
        warrior_stats=warrior_stats,
    )
    Path(args.report).write_text(report, encoding="utf-8")
    print(f"Wrote report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
