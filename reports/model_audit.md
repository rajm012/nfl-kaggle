# Studies 1–2 model audit

Generated UTC: 2026-11-09T14:42:04.246277+00:00. All recorded fits converged. Two-sided Holm-significant original-family rows: 0/9; binary cluster-sensitivity rows: 0/3.

| id | model | method | plays | players | beta | ci95 | p_two | p_two_holm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W1 | original specification | LMM | 31035 | 83 | -0.01499 | [-0.05001, 0.02004] | 0.4016 | 1.0 |
| W2 | original specification | LMM | 31035 | 83 | 0.00081 | [-0.03581, 0.03742] | 0.9655 | 1.0 |
| O1 | original specification | LMM | 48697 | 89 | 0.00137 | [-0.00474, 0.00749] | 0.6604 | 1.0 |
| O1 | original specification | player-clustered LPM sensitivity | 48697 | 89 | 0.00287 | [-0.00365, 0.00939] | 0.3841 | 0.7682 |
| O2 | original specification | LMM | 48697 | 89 | -0.00312 | [-0.00957, 0.00333] | 0.3432 | 1.0 |
| O2 | original specification | player-clustered LPM sensitivity | 48697 | 89 | -0.00259 | [-0.00858, 0.00341] | 0.3936 | 0.7682 |
| D1 | original specification | LMM | 33417 | 98 | 0.00237 | [-0.01381, 0.01854] | 0.7743 | 1.0 |
| D2 | original specification | LMM | 28970 | 98 | 0.00549 | [-0.00061, 0.01160] | 0.078 | 0.4677 |
| D2 | original specification | player-clustered LPM sensitivity | 28970 | 98 | 0.0042 | [-0.00067, 0.00908] | 0.0903 | 0.271 |
| F1 | confirmatory, player SDs | LMM | 25799 | 77 | -0.00119 | [-0.01900, 0.01662] | 0.8961 | 0.8961 |
| F1 | secondary, player SDs | LMM | 25799 | 77 | -0.00154 | [-0.01919, 0.01612] | 0.8646 | — |
| F2 | confirmatory, player SDs | LMM | 37216 | 73 | -0.0042 | [-0.01149, 0.00309] | 0.2591 | 0.7773 |
| F2 | secondary, player SDs | LMM | 37216 | 73 | -0.00399 | [-0.01072, 0.00273] | 0.2444 | — |
| F3 | confirmatory, player SDs | LMM | 26624 | 73 | -0.02029 | [-0.05890, 0.01831] | 0.3029 | 0.7773 |
| F3 | secondary, player SDs | LMM | 26624 | 73 | -0.02123 | [-0.06060, 0.01814] | 0.2905 | — |

## Corrections and limits

Historical reports remain unchanged. Study 1 LMM rows reproduce the original specification and are shown for audit, including its model-based binary SE deviation. Separate binary OLS linear-probability fits use player-clustered sandwich SE, finite-sample correction and t reference with players−1 degrees of freedom. They change the estimator as well as uncertainty and are explicitly sensitivities.

The preregistration stated expected signs but did not explicitly state one-sided testing. Original code used directional p-values. This audit conservatively reports two-sided p-values and Holm across the six Study 1 LMM and three Study 2 confirmatory rows separately. The three cluster sensitivities form a separately labelled Holm family. Historical directional values are saved in JSON, not promoted as new findings.

Study 2 A0 and 10-yard-split imputation/SDs now use unique sprint-tracked athletes within position, before joining to plays. Historical code weighted these moments by opportunity. Baseline Study 1 preprocessing is retained. This is a full-cohort historical audit, not held-out prediction or a pristine 2025 evaluation.

Patsy removes only rows missing required formula fields; model groups follow the actual retained indices. Constant/redundant columns are removed by an ordered rank rule before fitting; actual samples, dropped terms, warnings, covariate estimates and timings are recorded in `model_audit.json` and per-model checkpoints. Normal-reference LMM intervals retain the original continuous-model method. Covariate estimates are descriptive checks, not an additional confirmatory family.

A non-significant result does not establish equivalence or no predictive value. Held-out evaluation and same-sample 3-cone sensitivity remain separate required work.
