# Same-sample 3-cone sensitivity

Generated UTC: 2026-11-10T04:17:49.997806+00:00. Recorded cone times only; no imputation.

| test | outcome_players | cone_players | plays | beta_without_cone | ci_without | beta_with_cone | ci_with |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W1 | 83 | 25 | 9438 | 0.00549 | [-0.12147, 0.13246] | 0.01139 | [-0.11490, 0.13768] |
| W2 | 83 | 25 | 9438 | -0.02039 | [-0.11930, 0.07851] | -0.02772 | [-0.13337, 0.07793] |
| O1 | 89 | 43 | 20730 | -0.00268 | [-0.00969, 0.00433] | -0.00235 | [-0.00953, 0.00482] |
| O2 | 89 | 43 | 20730 | -0.00146 | [-0.00693, 0.00400] | 0.00042 | [-0.00597, 0.00681] |
| D1 | 98 | 37 | 12470 | -0.01074 | [-0.05166, 0.03018] | -0.01068 | [-0.05361, 0.03226] |
| D2 | 98 | 37 | 10874 | 0.01517 | [0.00621, 0.02413] | 0.01521 | [0.00682, 0.02359] |
| F1 | 77 | 33 | 11717 | -0.02255 | [-0.05177, 0.00666] | -0.0226 | [-0.05251, 0.00731] |
| F2 | 73 | 42 | 19773 | -0.00274 | [-0.01076, 0.00528] | -0.00199 | [-0.00957, 0.00558] |
| F3 | 73 | 23 | 7918 | -0.08269 | [-0.15167, -0.01371] | -0.08328 | [-0.15586, -0.01069] |

## Support and selection

| combine_position | draft_year | players | cone_recorded |
| --- | --- | --- | --- |
| DL | 2023 | 37 | 18 |
| DL | 2024 | 37 | 10 |
| DL | 2025 | 44 | 15 |
| OL | 2023 | 37 | 20 |
| OL | 2024 | 46 | 25 |
| OL | 2025 | 38 | 16 |
| WR | 2023 | 39 | 13 |
| WR | 2024 | 31 | 9 |
| WR | 2025 | 37 | 11 |

| combine_position | draft_status | players | cone_recorded |
| --- | --- | --- | --- |
| DL | UDFA | 29 | 15 |
| DL | drafted | 89 | 28 |
| OL | UDFA | 32 | 18 |
| OL | drafted | 89 | 43 |
| WR | UDFA | 30 | 10 |
| WR | drafted | 77 | 23 |

| combine_position | cone_recorded | players | median_weight | median_forty | median_pick_drafted | UDFA_fraction |
| --- | --- | --- | --- | --- | --- | --- |
| DL | False | 75 | 279.0 | 4.775 | 125.0 | 0.18666666666666668 |
| DL | True | 43 | 279.0 | 4.84 | 103.5 | 0.3488372093023256 |
| OL | False | 60 | 315.0 | 5.1 | 79.0 | 0.23333333333333334 |
| OL | True | 61 | 310.0 | 5.18 | 118.0 | 0.29508196721311475 |
| WR | False | 74 | 201.0 | 4.46 | 129.0 | 0.2702702702702703 |
| WR | True | 33 | 197.0 | 4.46 | 110.0 | 0.30303030303030304 |

## Interpretation and method

These secondary association fits use all available REG non-nullified plays and include all cohorts, preserving the historical analysis window. They are separate from the frozen rookie-season cohort prediction models; no prediction coefficients are changed using these results. Every comparison uses identical players/plays for baseline, baseline+tracking, baseline+cone and baseline+cone+tracking. Intervals are two-sided, normal-reference LMM for continuous outcomes and player-clustered finite-sample t for binary LPM. This is not a new confirmatory family.

Trait scaling retains the historical player-level definitions and the audited unique-player Study 2 preprocessing. Cone SD is calculated from unique cone-observed athletes within position. No missing times are fabricated. Exact retained samples, rank removals, numerical retry warnings and all nested coefficients are saved in JSON. Small selected samples can yield wide intervals; no universal incremental ranking claim follows. Cohort cone-subset prediction appears separately in `validation.md`.
