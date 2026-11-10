# Studies 1–2 cohort evaluation and 3-cone sensitivity

Frozen implementation **2026-11-10**, before new development/evaluation fits in this block.
This implements the 2026-10-29 incremental-value requirement, not a new hypothesis family.
Prior Studies 1–2 already used 2025 outcomes: this is a retrospective cohort split, **not a
pristine untouched holdout**. The Study 3 gate remains failed and its primary claim stopped.

## Scope and preprocessing

- Primary prediction uses rookie-season REG, non-nullified plays. This makes follow-up
  duration comparable across classes; it is a documented prediction specification, distinct
  from the historical association models pooling all available REG seasons.
- Develop on 2023/24 rookie seasons; evaluate on the 2025 rookie season. Preserve the nine
  outcome/exposure definitions W1–D2 and F1–F3 and their original NFL context covariates.
- Require recorded original outcome/filter and nonmissing model keys, down, yards-to-go
  and required OL dropback/pass-rusher context. No minimum-play threshold in the primary
  score; show counts and a separately labelled ≥30-valid-play sensitivity for noisy targets.
- Rebuild TURN/BURST from player/drill attempt means, centring/scaling within drill on
  2023/24 athletes across positions only. Exclude constant/sparse/unseen drills using
  exposure-only rules; transform 2025 with the frozen reference. A0 is the existing mean
  sprint-curve acceleration. Never use game movement or outcomes to construct exposures.
- Player medians/SDs (ddof=1) use unique development-class athletes within position,
  restricted to sprint-tracked athletes for Study 2. UDFA=260 + indicator. Missing forty
  and 10-yard split use development-player medians + indicators. No cone-time imputation.
- Cushion median uses development plays for that specific outcome; missing categorical
  context maps to UNK, motion/blitz nulls to false with counts. Freeze context levels.
  Unseen 2025 levels map to UNK if trained, otherwise the most frequent training level.
- An unseen calendar year cannot have an estimated training coefficient: map evaluation
  season 2025 to the latest development season (2024). This explicitly assumes the latest
  trained calendar intercept persists. Record other unknown-level counts, without tuning.
- Drop only constant/redundant columns by the ordered rank rule, preserving the baseline
  columns before added traits. Save actual players/plays, dropped terms and convergence.

## Prediction models and scores

- Continuous outcomes: original unweighted play-level LMM with player random intercepts;
  prediction uses **fixed components only**. Binary outcomes: separately documented OLS
  linear-probability fallback with player-clustered SE, finite-sample correction and
  players−1 t reference. Do not clip its predictions or call it a calibrated probability.
- For each original test compare identical training/evaluation rows: conventional baseline
  B0 against B1 adding only the prescribed exposure. Study 2 baseline includes 10-yard split.
- Original prespecified secondary comparisons: joint TURN/BURST on each of the four
  distinct Study 1 outcomes, and the three Study 2 comparisons omitting 10-yard split.
  They cannot replace a failed primary comparison or be promoted as a new discovery.
- For each evaluation athlete, compute observed mean outcome and mean fixed prediction
  over those same realised NFL contexts. A common B0 context adjustment can be subtracted
  from observations and both predictions; the errors are unchanged. No evaluation player
  intercepts, recalibration or coefficients are estimated using evaluation outcomes.
- Primary score: equal-athlete RMSE of those mean errors. Improvement is RMSE(B0)−RMSE(B1),
  positive is better; MAE is secondary. These conditional retrospective predictions do not
  establish prospect rankings or forecasts of future NFL role/context/opportunity.
- 10,000 paired evaluation-athlete bootstrap samples give percentile improvement intervals,
  conditional on the trained models. Also report conservative Bonferroni simultaneous
  percentile intervals within the original six/three primary prediction families to avoid
  selecting one of nine apparent gains. These are bootstrap uncertainty intervals, not
  the original coefficient Holm tests. No claim that an uncertain interval proves zero.
- Save all development preprocessing/coefficients and source/protocol hashes before opening
  evaluation. Separate `--stage develop` and `--stage evaluate`; evaluation refuses a changed
  source/protocol. Save per-athlete errors, support/attrition and unknown-level counts.
- The 200 training-bootstrap refits in Study 3 were conditional on its screen passing;
  Study 3 stopped. The present required prediction intervals condition on the training fits;
  explicitly acknowledge they omit training uncertainty rather than imply it was assessed.

## Same-sample 3-cone checks

1. Cohort sensitivity: train cone-observed development athletes and score cone-observed
   2025 athletes. Same rows for B0 + cone versus B0 + cone + the original exposure; same
   frozen player/drill reference as the parent test, and cone SD from unique development
   athletes with observed cone times. No invented times or threshold changes after scoring.
2. Historical association sensitivity: on cone-observed athletes in all available REG
   seasons, compare the original tracking coefficient with and without cone adjustment on
   **identical rows**. Preserve audited player-level Study 2 preprocessing; continuous LMM,
   binary player-clustered LPM. Report two-sided intervals; secondary findings, not a new
   confirmatory family. Report rank/actual samples and estimability failures honestly.
3. Show cone availability and retained athletes by position/class/draft status, including
   those without NFL outcome support. Contrast cone-present/absent conventional profiles
   descriptively. Opt-outs/selection prevent generalising a small subset to all prospects.

## Decision and output

No primary performance-ranking claim without coherent development direction and cohort
improvement supported by uncertainty; account for the nine comparisons and small evaluation
samples. The evidence-map narrative remains the selected path. No Study 3 interaction fit,
new trait or post-evaluation model tuning. Deliver `src/evaluate.py`,
`src/cone_sensitivity.py`, `reports/validation.md`, `reports/cone_sensitivity.md`, frozen
model metadata, evaluation tables and a draft figure. Then update the submission plan/state.

## Numerical-fit rule — added 2026-11-10 before evaluation

Development fitting exposed a singular random-effect covariance/invalid fixed-effect SE
in the no-10-yard secondary baseline. Convergence alone is insufficient. For any continuous
model, require finite fixed coefficients and positive finite fixed-effect SE; retry the
same model with Powell if default fitting fails this check or reports a nonpositive Hessian.
Record both attempts/warnings and fail explicitly if the retry remains invalid. This
numerical rule uses development diagnostics only and changes no exposure, outcome or sample.
