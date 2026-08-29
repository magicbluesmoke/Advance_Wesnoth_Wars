# Role XP Parity Simulation Report

Trials: 10,000  
Combat model: 5 combats, 2 kills per scenario, enemy_level=1  
Advancement thresholds: L1->L2=50, L2->L3=90

## Warrior baseline

- Mean scenarios to L2: 3.00
- P50 scenarios to L2: 3.0
- Mean scenarios to L3: 8.00
- P50 scenarios to L3: 8.0

## Role summary vs warrior

| Role | Mean L2 | P50 L2 | Mean L3 | P50 L3 | Parity verdict |
| --- | ---: | ---: | ---: | ---: | --- |
| scout | 2.00 | 2.0 | 4.00 | 4.0 | keeps up |
| tank | 2.00 | 2.0 | 4.00 | 4.0 | keeps up |
| leader | 2.00 | 2.0 | 4.00 | 4.0 | keeps up |
| buffer | 2.00 | 2.0 | 4.00 | 4.0 | keeps up |

## Spectrum table (pure-role -> role+full-fighting)

### scout

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 3.00 | 3.0 | 7.00 | 7.0 |
| fight_share=25% | 3.00 | 3.0 | 7.00 | 7.0 |
| fight_share=50% | 2.00 | 2.0 | 5.00 | 5.0 |
| fight_share=75% | 2.00 | 2.0 | 4.00 | 4.0 |
| fight_share=100% | 2.00 | 2.0 | 4.00 | 4.0 |

### tank

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 3.00 | 3.0 | 7.00 | 7.0 |
| fight_share=25% | 3.00 | 3.0 | 7.00 | 7.0 |
| fight_share=50% | 2.00 | 2.0 | 5.00 | 5.0 |
| fight_share=75% | 2.00 | 2.0 | 4.00 | 4.0 |
| fight_share=100% | 2.00 | 2.0 | 4.00 | 4.0 |

### leader

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 3.00 | 3.0 | 7.00 | 7.0 |
| fight_share=25% | 3.00 | 3.0 | 7.00 | 7.0 |
| fight_share=50% | 2.00 | 2.0 | 5.00 | 5.0 |
| fight_share=75% | 2.00 | 2.0 | 4.00 | 4.0 |
| fight_share=100% | 2.00 | 2.0 | 4.00 | 4.0 |

### buffer

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 3.00 | 3.0 | 7.00 | 7.0 |
| fight_share=25% | 3.00 | 3.0 | 7.00 | 7.0 |
| fight_share=50% | 2.00 | 2.0 | 5.00 | 5.0 |
| fight_share=75% | 2.00 | 2.0 | 4.00 | 4.0 |
| fight_share=100% | 2.00 | 2.0 | 4.00 | 4.0 |
