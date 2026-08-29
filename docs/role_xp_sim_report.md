# Role XP Parity Simulation Report

Trials: 10,000  
Combat model: 5 combats, kill_prob=45%, enemy_level=1  
Advancement thresholds: L1->L2=50, L2->L3=90

## Warrior baseline

- Mean scenarios to L2: 2.88
- P50 scenarios to L2: 3.0
- Mean scenarios to L3: 7.24
- P50 scenarios to L3: 7.0

## Role summary vs warrior

| Role | Mean L2 | P50 L2 | Mean L3 | P50 L3 | Parity verdict |
| --- | ---: | ---: | ---: | ---: | --- |
| scout | 2.28 | 2.0 | 5.57 | 6.0 | keeps up |
| tank | 2.09 | 2.0 | 5.13 | 5.0 | keeps up |
| leader | 2.26 | 2.0 | 5.54 | 6.0 | keeps up |
| buffer | 2.27 | 2.0 | 5.36 | 5.0 | keeps up |

## Spectrum table (pure-role -> role+full-fighting)

### scout

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 5.01 | 5.0 | 12.58 | 13.0 |
| fight_share=25% | 3.81 | 4.0 | 9.41 | 9.0 |
| fight_share=50% | 3.09 | 3.0 | 7.48 | 8.0 |
| fight_share=75% | 2.52 | 2.0 | 6.38 | 6.0 |
| fight_share=100% | 2.28 | 2.0 | 5.57 | 6.0 |

### tank

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 4.00 | 4.0 | 10.39 | 10.0 |
| fight_share=25% | 3.13 | 3.0 | 8.13 | 8.0 |
| fight_share=50% | 2.78 | 3.0 | 6.66 | 7.0 |
| fight_share=75% | 2.49 | 2.0 | 5.67 | 6.0 |
| fight_share=100% | 2.09 | 2.0 | 5.13 | 5.0 |

### leader

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 5.01 | 5.0 | 12.57 | 13.0 |
| fight_share=25% | 3.81 | 4.0 | 9.39 | 9.0 |
| fight_share=50% | 3.09 | 3.0 | 7.49 | 8.0 |
| fight_share=75% | 2.52 | 2.0 | 6.39 | 6.0 |
| fight_share=100% | 2.26 | 2.0 | 5.54 | 6.0 |

### buffer

| Mix | Mean L2 | P50 L2 | Mean L3 | P50 L3 |
| --- | ---: | ---: | ---: | ---: |
| fight_share=0% | 4.44 | 4.0 | 12.00 | 12.0 |
| fight_share=25% | 3.51 | 3.0 | 9.17 | 9.0 |
| fight_share=50% | 2.90 | 3.0 | 7.31 | 7.0 |
| fight_share=75% | 2.49 | 2.0 | 6.19 | 6.0 |
| fight_share=100% | 2.27 | 2.0 | 5.36 | 5.0 |
