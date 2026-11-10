# Movement transfer audit

Generated UTC: 2026-11-09T14:41:41.425393+00:00.

| scope | position | trait | adjustment | game_SB | n | r | lo | hi | valid_bootstraps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| historical, PRE+REG+POST | WR | lat | raw | 0.653 | 99 | 0.276 | 0.095 | 0.44 | 2000 |
| historical, PRE+REG+POST | WR | lat | weight-adjusted | 0.653 | 99 | 0.28 | 0.09 | 0.448 | 2000 |
| historical, PRE+REG+POST | WR | lat | size+forty-adjusted | 0.653 | 99 | 0.278 | 0.087 | 0.45 | 2000 |
| historical, PRE+REG+POST | DL | burst | raw | 0.804 | 115 | 0.45 | 0.297 | 0.589 | 2000 |
| historical, PRE+REG+POST | DL | burst | weight-adjusted | 0.804 | 115 | 0.206 | 0.044 | 0.382 | 2000 |
| historical, PRE+REG+POST | DL | burst | size+forty-adjusted | 0.804 | 115 | 0.195 | 0.035 | 0.365 | 2000 |
| corrected, PRE+REG | WR | lat | raw | 0.643 | 98 | 0.279 | 0.107 | 0.445 | 2000 |
| corrected, PRE+REG | WR | lat | weight-adjusted | 0.643 | 98 | 0.281 | 0.099 | 0.457 | 2000 |
| corrected, PRE+REG | WR | lat | size+forty-adjusted | 0.643 | 98 | 0.278 | 0.092 | 0.45 | 2000 |
| corrected, PRE+REG | DL | burst | raw | 0.804 | 115 | 0.443 | 0.289 | 0.584 | 2000 |
| corrected, PRE+REG | DL | burst | weight-adjusted | 0.804 | 115 | 0.203 | 0.044 | 0.376 | 2000 |
| corrected, PRE+REG | DL | burst | size+forty-adjusted | 0.804 | 115 | 0.194 | 0.035 | 0.365 | 2000 |
| sensitivity, REG only | WR | lat | raw | 0.694 | 74 | 0.322 | 0.122 | 0.503 | 2000 |
| sensitivity, REG only | WR | lat | weight-adjusted | 0.694 | 74 | 0.33 | 0.112 | 0.519 | 2000 |
| sensitivity, REG only | WR | lat | size+forty-adjusted | 0.694 | 74 | 0.339 | 0.092 | 0.538 | 2000 |
| sensitivity, REG only | DL | burst | raw | 0.84 | 92 | 0.418 | 0.234 | 0.581 | 2000 |
| sensitivity, REG only | DL | burst | weight-adjusted | 0.84 | 92 | 0.178 | -0.013 | 0.377 | 2000 |
| sensitivity, REG only | DL | burst | size+forty-adjusted | 0.84 | 92 | 0.169 | -0.028 | 0.364 | 2000 |

Each athlete contributes one pooled-season movement trait (≥30 player-plays). All seasons are full-cohort descriptive measurements, not development/evaluation prediction. Historical scope included POST; corrected scope explicitly excludes POST while retaining PRE+REG, as specified in the measurement preregistration. REG-only is a season-type sensitivity. Per-season traits with season-specific normalisation are also cached for later checks; these correlations are pooled.

Game normalisation retains the original lined-up-position × play-type cells. Receiver play type uses recorded route, OL uses dropback availability and DL uses sack availability. No outcome-nullification filter is newly added to historical movement measurement. Context is available only for the inner-joined source rows.

Adjusted correlations residualise both Combine and game traits on the stated covariates plus an intercept, within position. Size+forty uses position-sample median forty and a missing indicator. 2,000 paired athlete bootstrap resamples refit residualisation each time; percentile intervals. Adjustment definitions are explicit and need not match undocumented historical exploratory calculations. Game SB is alternating-game split-half reliability. Complete position/trait tables are in JSON, without selecting new performance hypotheses.

Joined movement plays: 311,731; POST excluded from corrected scope: 12,925. Historical `transfer.md` is unchanged.
