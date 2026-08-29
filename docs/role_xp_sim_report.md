# Role XP Parity Simulation Report

Trials: 10,000  
Combat model: 5 combats, kill_prob=45%, enemy_level=1  
Advancement thresholds: L1->L2=50, L2->L3=90

## Warrior baseline

- Mean scenarios to L2: 2.87
- P50 scenarios to L2: 3.0
- Mean scenarios to L3: 7.23
- P50 scenarios to L3: 7.0

## Role summary vs warrior

| Role | Mean L2 | P50 L2 | Mean L3 | P50 L3 | Parity verdict |
| --- | ---: | ---: | ---: | ---: | --- |
| scout | 1.87 | 2.0 | 3.98 | 4.0 | keeps up |
| tank | 1.87 | 2.0 | 3.98 | 4.0 | keeps up |
| leader | 1.87 | 2.0 | 3.98 | 4.0 | keeps up |
| buffer | 1.87 | 2.0 | 3.98 | 4.0 | keeps up |

## Spectrum table (pure-role -> role+full-fighting)

### scout

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 2.80 | 3.0 | 6.15 | 6.0 |
| fight_share=25% | 2.10 | 2.0 | 5.51 | 6.0 |
| fight_share=50% | 2.03 | 2.0 | 4.78 | 5.0 |
| fight_share=75% | 1.97 | 2.0 | 4.36 | 4.0 |
| fight_share=100% | 1.87 | 2.0 | 3.98 | 4.0 |

### tank

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 2.79 | 3.0 | 6.14 | 6.0 |
| fight_share=25% | 2.09 | 2.0 | 5.50 | 5.0 |
| fight_share=50% | 2.03 | 2.0 | 4.78 | 5.0 |
| fight_share=75% | 1.97 | 2.0 | 4.36 | 4.0 |
| fight_share=100% | 1.87 | 2.0 | 3.98 | 4.0 |

### leader

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 2.80 | 3.0 | 6.15 | 6.0 |
| fight_share=25% | 2.09 | 2.0 | 5.51 | 6.0 |
| fight_share=50% | 2.03 | 2.0 | 4.78 | 5.0 |
| fight_share=75% | 1.97 | 2.0 | 4.35 | 4.0 |
| fight_share=100% | 1.87 | 2.0 | 3.98 | 4.0 |

### buffer

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 2.80 | 3.0 | 6.14 | 6.0 |
| fight_share=25% | 2.10 | 2.0 | 5.50 | 5.0 |
| fight_share=50% | 2.03 | 2.0 | 4.78 | 5.0 |
| fight_share=75% | 1.96 | 2.0 | 4.36 | 4.0 |
| fight_share=100% | 1.87 | 2.0 | 3.98 | 4.0 |
