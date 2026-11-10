# Study 3 — Frozen measurement screen

Generated UTC: 2026-11-09T14:37:26.305812+00:00. **Stop primary route-performance claim: frozen reliability screen fails.**

No TURN–separation association or 2025 performance evaluation was fitted. The only outcome fit is the frozen conventional baseline on 2023–24 rookie REG plays.

| draft_year | players_initial | plays_initial | players_fitted | plays_fitted |
| --- | --- | --- | --- | --- |
| 2023 | 25 | 2385 | 25 | 2385 |
| 2024 | 17 | 1586 | 17 | 1586 |
| 2025 | 16 | 1179 | 16 | 1179 |

## Alternating-game contrast reliability

| contrast | n | r | r_lo | r_hi | SB | SB_lo | SB_hi | valid_bootstraps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw | 41 | 0.301 | 0.032 | 0.56 | 0.463 | 0.062 | 0.718 | 10000 |
| adjusted | 41 | 0.174 | -0.114 | 0.435 | 0.296 | -0.257 | 0.606 | 10000 |

Chronological game IDs are ordered within each athlete and alternated. Each diagnostic player has ≥3 outcome-recorded BREAK and GO plays in each half. Raw contrast is mean BREAK separation minus mean GO separation, in yards. Adjusted contrast removes non-player components of the conventional baseline, including conventional-measurable family interactions. The halves share estimated adjustments; this is a descriptive screen, not an independent replication. 10,000 paired player bootstrap resamples give percentile correlation intervals; negative SB values are retained.

Frozen gate: ≥25 diagnostic development players and adjusted SB point estimate ≥0.40. A pass still requires acknowledging its interval; a fail stops the primary route-performance claim without trying alternate groups or thresholds.

Baseline: 3,971 plays, 42 players, 384 games; design rank 65. Row weight is 1/n(player,family), giving equal total weight to each player/family. Player fixed intercepts; separate route/down/coverage/alignment indicators; linear yards-to-go, motion, cushion/missing indicator; six conventional BREAK interactions. All player SDs and forty imputation use unique 2023–24 WRs; cushion uses development plays. No evaluation statistics inform preprocessing.

Redundant columns removed in declared order: [].

Saved: `study3_measurement.json`, `study3_preprocessing.json`, `study3_baseline.json`; figure `figures/study3_measurement.png`. Full-cohort TURN numerical values differ from the training-reference recomputation by design. Prior 2025 exposure in Studies 1–2 remains disclosed.
