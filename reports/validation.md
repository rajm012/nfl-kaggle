# Studies 1–2 cohort prediction validation

Generated UTC: 2026-11-10T04:17:42.410875+00:00. Frozen development: 2026-11-10T04:16:55.645605+00:00.

Positive improvement means lower equal-player RMSE with tracking. Units are yards for WR separation, seconds for DL get-off, and outcome-scale probability/proportion units for pressure outcomes. This is retrospective conditional prediction on realised NFL context.

| test | family | train_players | eval_players | eval_plays | baseline_RMSE | tracking_RMSE | improvement | ci95 | family_interval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W1 | primary | 57 | 23 | 3701 | 0.23572 | 0.23577 | -5e-05 | [-0.00903, 0.01267] | [-0.01138, 0.01746] |
| W2 | primary | 57 | 23 | 3701 | 0.23572 | 0.23651 | -0.00079 | [-0.00641, 0.00416] | [-0.00779, 0.00536] |
| O1 | primary | 54 | 28 | 8475 | 0.09511 | 0.09446 | 0.00065 | [-0.00114, 0.00171] | [-0.00156, 0.00198] |
| O2 | primary | 54 | 28 | 8475 | 0.09511 | 0.098 | -0.0029 | [-0.00728, 0.00382] | [-0.00972, 0.00596] |
| D1 | primary | 57 | 37 | 5245 | 0.07583 | 0.07981 | -0.00398 | [-0.00705, -0.00049] | [-0.00791, 0.00064] |
| D2 | primary | 57 | 37 | 4644 | 0.0437 | 0.04255 | 0.00115 | [-0.00008, 0.00231] | [-0.00049, 0.00266] |
| F1 | primary | 50 | 23 | 2589 | 0.09281 | 0.09216 | 0.00065 | [-0.00086, 0.00195] | [-0.00117, 0.00220] |
| F2 | primary | 45 | 22 | 6428 | 0.09364 | 0.09373 | -9e-05 | [-0.00181, 0.00066] | [-0.00217, 0.00085] |
| F3 | primary | 51 | 20 | 3525 | 0.21054 | 0.21062 | -8e-05 | [-0.00779, 0.00875] | [-0.00913, 0.01047] |

## Prespecified secondary and cone comparisons

| test | family | train_players | eval_players | eval_plays | baseline_RMSE | tracking_RMSE | improvement | ci95 | family_interval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W1_joint | joint secondary | 57 | 23 | 3701 | 0.23572 | 0.23593 | -0.00021 | [-0.00857, 0.00870] | [-0.00857, 0.00870] |
| O1_joint | joint secondary | 54 | 28 | 8475 | 0.09511 | 0.09689 | -0.00179 | [-0.00564, 0.00373] | [-0.00564, 0.00373] |
| D1_joint | joint secondary | 57 | 37 | 5245 | 0.07583 | 0.08097 | -0.00514 | [-0.01033, -0.00068] | [-0.01033, -0.00068] |
| D2_joint | joint secondary | 57 | 37 | 4644 | 0.0437 | 0.04302 | 0.00067 | [-0.00117, 0.00243] | [-0.00117, 0.00243] |
| F1_no10 | no-10yd secondary | 50 | 23 | 2589 | 0.09234 | 0.09193 | 0.00041 | [-0.00058, 0.00122] | [-0.00058, 0.00122] |
| F2_no10 | no-10yd secondary | 45 | 22 | 6428 | 0.0931 | 0.0946 | -0.0015 | [-0.00330, -0.00014] | [-0.00330, -0.00014] |
| F3_no10 | no-10yd secondary | 51 | 20 | 3525 | 0.20558 | 0.20494 | 0.00064 | [-0.00559, 0.00761] | [-0.00559, 0.00761] |
| W1_cone | cone sensitivity | 17 | 7 | 1508 | 0.39482 | 0.36205 | 0.03276 | [-0.04748, 0.09115] | [-0.04748, 0.09115] |
| W2_cone | cone sensitivity | 17 | 7 | 1508 | 0.39482 | 0.64975 | -0.25493 | [-0.39734, -0.12727] | [-0.39734, -0.12727] |
| O1_cone | cone sensitivity | 26 | 13 | 3491 | 0.13922 | 0.13969 | -0.00047 | [-0.00116, 0.00075] | [-0.00116, 0.00075] |
| O2_cone | cone sensitivity | 26 | 13 | 3491 | 0.13922 | 0.14207 | -0.00286 | [-0.00523, 0.00038] | [-0.00523, 0.00038] |
| D1_cone | cone sensitivity | 20 | 13 | 1732 | 0.06833 | 0.08501 | -0.01668 | [-0.04755, 0.01432] | [-0.04755, 0.01432] |
| D2_cone | cone sensitivity | 20 | 13 | 1501 | 0.04805 | 0.04836 | -0.00032 | [-0.00598, 0.00569] | [-0.00598, 0.00569] |
| F1_cone | cone sensitivity | 20 | 9 | 979 | 0.0671 | 0.05955 | 0.00755 | [0.00443, 0.01080] | [0.00443, 0.01080] |
| F2_cone | cone sensitivity | 26 | 12 | 3323 | 0.13365 | 0.13377 | -0.00012 | [-0.00140, 0.00040] | [-0.00140, 0.00040] |
| F3_cone | cone sensitivity | 16 | 6 | 1353 | 0.44357 | 0.33364 | 0.10993 | [-0.01557, 0.21656] | [-0.01557, 0.21656] |

## Validation boundaries

Rookie REG, non-nullified plays; 2023–24 development and 2025 evaluation. No evaluation-player effects, imputation moments, context coefficients or recalibration are fitted from evaluation outcomes. Fixed predictions are averaged within athlete; a common baseline context adjustment leaves the compared errors unchanged. All nine original exposures/outcomes are reported, without promoting a winning secondary.

10,000 paired athlete resamples give percentile improvement intervals conditional on the frozen development fits. Primary family intervals use Bonferroni-adjusted percentiles within six Study 1 / three Study 2 comparisons; finite bootstrap tails and small evaluation samples limit precision. Training uncertainty is not included. The ≥30-play sensitivity, MAE, relative changes and unknown-level counts are in JSON.

The historical studies already used 2025 outcomes: this is not a pristine holdout. An unseen 2025 calendar intercept maps to the latest trained season; other unseen context levels use frozen UNK/modal encodings. Boundary warnings are retained in development metadata. Binary LPM predictions are not clipped or described as calibrated probabilities. Small cone subsets are sensitivities, not general scouting validation.

No Study 3 interaction is fitted; its measurement gate remains failed. Full protocol: `evaluation_protocol.md`; frozen preprocessing/coefficients: `evaluation_development.json`, `evaluation_models/`; per-athlete errors: `data/interim/evaluation_player_scores.parquet`.
