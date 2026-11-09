# Study 3 — Route-family specificity of Combine turning

Frozen **2026-11-09**, before fitting any new route-family TURN–separation association.
This is a subsequent, predeclared analysis informed by Studies 1–2, not an independent
untouched discovery. The 2025 cohort's outcomes were already included in prior studies.
The current turn to route context and the support inspection are disclosed in `PLAN.md`.
No new outcome association was computed during the planning block.

## Question and one primary test

Does the existing Combine TURN measurement relate to a receiver's separation on SLANT/OUT
relative to GO? A common positive interaction would support route-specific incremental
information that an all-route main effect could miss. It would not establish causality.

- Exposure: TURN, the existing 90th-percentile absolute lateral acceleration per attempt,
  averaged within player/drill, standardised within drill and averaged across non-40 drills.
- Outcome: `separation_at_pass_forward`, in yards.
- Route set: `SLANT`, `OUT`, `GO`; `BREAK=1` for SLANT/OUT and 0 for GO. Retain separate route
  intercepts. The family name is an analytical grouping, not proof every recorded route has
  a sharp or equivalently timed break.
- Primary parameter: coefficient of `TURN_z × BREAK` in the development model below.
  Expected positive; **two-sided alpha=0.05**, 95% interval. One primary coefficient, no
  confirmatory family of route/coverage subtests.
- No new braking, burst, route-score composite or optimised metric weights in this study.

## Sample and evaluation boundary

WR by `combine_position`; join on unique `nfl_id` and unique player-play keys.
Use REG only, `play_nullified_by_penalty == 'N'`, recorded outcome and one of the three
routes. Restrict `season == draft_year` so all classes contribute rookie-season performance.
Require at least **10 outcome-recorded plays in each of BREAK and GO per player** before
modelling; outcome availability, not outcome size, defines eligibility.

Development: 2023/2024 draft classes. Evaluation: 2025. Counts before final joins are
25/17/16 eligible athletes respectively. Require at least **35 development and 15 evaluation
athletes** after feature/key checks. If this fails, do not weaken the threshold after viewing
associations; report feasibility and use the evidence-map narrative.

Do not inspect new 2025 exposure–outcome associations until the development specification,
preprocessing and outputs are saved. Count/label/missingness checks are permitted. Prior
2025 exposure prevents a pristine-holdout claim. No model tuning after evaluation is opened.

## Preprocessing

Rebuild the same TURN definition from `combine_attempts.parquet` with **training-class-only**
drill centring/scaling. Use 2023–24 athletes across positions for the original drill reference
population; average attempts per player/drill before computing reference statistics. Transform
2025 with saved means/SDs; do not compute their own reference distribution. Unseen or constant
drills are excluded by a recorded exposure-only rule for both groups. This is a leakage-aware
recomputation of the existing measurement, not exactly the full-cohort historical numerical trait.

Then scale TURN and conventional numeric player covariates on unique development-class WRs,
not joined plays. Do not weight these SDs by opportunity. Freeze scaler/imputation metadata.

Conventional covariates: weight, height, forty, draft pick (UDFA=260), UDFA indicator and
forty-missing indicator. Impute missing forty with the development WR median. Median-impute
cushion from development plays and add a cushion-missing indicator. Map missing categorical
context to `UNK`, unseen evaluation categories to the saved unknown/reference encoding.
Fill missing motion with false and report the count, retaining the existing pipeline convention.
Drop rows with missing outcome, key, down or yards-to-go; report actual fitted n.
Drop constant/redundant indicator columns by a rank-based rule and record them.

## Measurement screen, before TURN associations

1. Reproduce the existing cross-drill TURN split-half reliability with uncertainty on the
   development cohort. Report the different questions answered by cross-drill consistency
   and same-drill test–retest. Three slant repeats cannot establish a slant-specific trait.
2. For eligible development players, split chronological games into alternating halves.
   In each half compute the mean BREAK separation minus mean GO separation. Require at least
   three recorded plays of each family in each half for this diagnostic.
3. Show raw and baseline-context-adjusted contrast reliability. The latter uses the baseline
   model below, with no TURN. It is a descriptive screen sharing estimated context adjustments;
   report that limitation. Estimate split-half correlation, its interval and Spearman–Brown
   reliability; bootstrap players, not plays.
4. If fewer than 25 development players support the diagnostic, or adjusted contrast
   Spearman–Brown point reliability is below **0.40**, stop a primary route-performance claim.
   Report wide intervals even if the point threshold passes. This prespecified screen does
   not turn marginal reliability into proof of a stable trait.

Record exposure-only trace QC, dropped attempts and all screen results before associations.
Do not select features using the outcome reliability check.

## Development model

Weighted linear model with player fixed intercepts:

`separation ~ player + route + down + yards_to_go + coverage + alignment + motion + cushion + cushion_missing + conventional_covariates:BREAK + TURN_z:BREAK`

`coverage` is `team_coverage_man_zone`; alignment is `receiver_alignment`. Down/route/coverage/
alignment are categorical, other context terms linear. Conventional covariates are the
six numeric/indicator fields defined above. Player-invariant main effects are absorbed by
player intercepts. Their BREAK interactions are necessary because size/speed/draft capital
may themselves be associated with the route-family contrast.

Weight each row by `1 / n(player, family)`, giving equal total weight to each eligible player
and each of their two families. Baseline B0 omits only `TURN_z:BREAK`; B1 adds it. No separate
full-sample search for route, coverage, spline, nonlinear or composite features.

Use two-way player/game cluster-robust uncertainty with finite-sample corrections and a
t reference using the smaller cluster count minus one. Record cluster counts and covariance
implementation. If the two-way estimate is invalid, report player-clustered inference as a
documented fallback plus a game-clustering sensitivity; do not silently substitute model-based SE.

Report coefficient in yards per athlete SD, 95% interval, actual players/plays, model rank,
measurement results and effect plots. A player fixed effect does not identify a general
between-player TURN main effect; this test is explicitly the differential route association.

## Evaluation on 2025

Freeze B0/B1 development coefficients first. For every eligible evaluation player calculate:

- Observed contrast: mean separation on BREAK minus mean separation on GO.
- Predicted contrast: the difference of mean fixed-component predictions on those same plays.
  Unknown player intercepts cancel, so no evaluation player effects are estimated from outcomes.
  Use saved training context encodings and scaler/imputation values.

This tests conditional prediction of the route-family contrast, not absolute separation or
a pre-draft prediction of future context. The mix of SLANT/OUT in BREAK is the player's actual
mix; separate route intercepts handle average differences, not all route-use selection.

Primary evaluation score: **equal-player RMSE** of contrasts. Improvement is RMSE(B0)-RMSE(B1),
positive means better. Report equal-player MAE as secondary and the distribution of paired
athlete errors. Use 10,000 paired player bootstrap resamples for a 95% improvement interval,
explicitly conditional on the fitted development models. Use 200 development-player bootstrap
refits as an additional training-uncertainty sensitivity if feasible; disclose absence/failures.
Do not interpret a wide interval from 16 athletes as strong evidence for or against small gains.

Promote a validated route-context claim only if the development interval is positive and
excludes zero, evaluation improvement is positive with its interval supporting improvement,
and the direction is not dependent on one influential athlete. Otherwise label the new
finding exploratory/uncertain or negative, as appropriate. No new fitting after evaluation.

## Prespecified sensitivities, not new primary tests

- Show SLANT and OUT components separately, without claiming significance from whichever wins.
- Equal-weight SLANT/OUT inside BREAK where both are supported; report the reduced sample.
- Unweighted play-level fit, leave-one-development-player-out influence, and player-only
  versus two-way clustering.
- Same-sample 3-cone-observed analysis, adding cone main/family terms as identifiable;
  report limited n and selection into observed cone times.
- Missingness/eligibility by class, draft status and route; more/less inclusive support
  only as labelled sensitivity, with the original primary result retained.
- All available REG seasons as a secondary follow-up sensitivity, clearly separated from
  the rookie-season analysis and its unequal exposure.

Planning band: **±0.10 yard per SD** for discussing practical scale; show ±0.05/±0.20 bands.
These are not established scouting utility cutoffs. Do not call a null significant test
equivalence; any formal equivalence analysis needs its own clearly labelled method.

## Artifacts and deadline

Planned: `src/route_context.py`, `reports/study3.md`, frozen preprocessing/model metadata,
eligibility table, evaluation table and a notebook figure. These do not exist yet.

Measurement/development done by November 16; evaluate and select final story by **November 20**.
If the screen fails, publish the failure in the research record and build the audited evidence
map. Preserve old outputs and all amendments. Future edits append a dated amendment here.
