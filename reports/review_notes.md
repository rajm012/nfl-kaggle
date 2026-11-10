# Internal football/statistical review — 2026-11-09

Owner: assistant. External football/statistical researchers are unavailable; the owner handles
Python execution checks and design/writeup review. This is an internal critique, not independent
expert validation. No new exposure–outcome associations were fitted in this work block.

Sources reviewed: `src/kinematics.py`, `src/outcomes.py`, the frozen `reports/study3_protocol.md`,
local schemas/counts and `reports/audit.md`. Official competition field definitions and any
football-specific external citations must be verified before publication; source names alone
do not prove interpretation.

## Football interpretation

- The observed lateral acceleration depends on speed and path curvature. A high TURN value
  is not automatically proof of greater intrinsic agility or a trainable physiological capacity.
  Inspect standardised-drill traces and use cautious movement language.
- SLANT and OUT contain changes of direction, but break shape, depth and timing vary. Keep
  separate route intercepts and inspect the route components. GO is a comparison context,
  not a guarantee that turning has no relevance to its performance.
- Separation at pass-forward is measured at a shared play event, which may occur before or
  after the receiver's own break. It does not directly measure separation created by that break.
  Confirm the field's official definition and acknowledge throw timing/context.
- Tracking has no opponents/ball. Do not invent defender leverage, coverage transitions or
  separation trajectories from player-only x/y. Use the supplied outcome/context fields.
- Conditional route-family prediction is narrower than pre-draft forecasting, route deployment
  advice or proof that training TURN improves performance. Evidence-card claims must reflect that.

## Statistical review

- Development/evaluation eligibility remains 42/16 athletes before final feature/measurement
  screens. Play counts are not independent exposure sample sizes.
- One route-family interaction is frozen. No redefinition after inspecting significance or
  2025 evaluation. Prior 2025 outcome exposure must be disclosed.
- Player fixed intercepts absorb static player main effects, not trait × route-family
  interactions. Conventional-measurable family interactions help address differential size/speed
  associations; route usage and unmeasured context can still confound interpretation.
- Cluster uncertainty and bootstrap resampling must follow players (and shared games where
  specified), with weighting and rank handling recorded. Check the actual covariance implementation.
- The adjusted contrast-reliability screen shares estimated baseline adjustments across halves.
  Its reliability may differ from a genuinely independent repetition; report the limitation and
  compare raw reliability. Any change to the frozen screen requires a dated amendment before fitting.
- Lack of significance is not equivalence. Practical-size bands are planning choices rather
  than established NFL decision thresholds. Small evaluation n may leave improvement uncertain.

## Completed evidence and open items

- Completed: keys, references, four raw/Parquet row-count checks, draft/season consistency,
  full game-frame key scan and candidate missingness/support counts. No integrity failures.
- Open: explain 2,496/2,466 unmatched derived-trait/outcome-context rows; complete movement
  reliability reproduction and inference/scaling corrections; verify official field semantics.
- Historical `confirmatory.md`, `study2.md`, `transfer.md` preserved byte-for-byte in
  `reports/history/2026-11-09/` before future corrected reruns.

Append dated review findings, sources and resolutions as analysis proceeds.

## 2026-11-09 — Local-run resolutions

- Join attrition is now explained in `join_attrition.md`: all missing movement rows have
  source/extraction reasons; all movement-only keys exist in supplied tracking. The
  provider's player-play context omission remains unknown. No game-trait join is needed
  for Study 3; adding one would remove three otherwise usable candidate rows.
- Cross-drill TURN reliability and explicit size-adjusted transfer reproduce the earlier
  patterns with athlete-bootstrap uncertainty. Corrected movement scope excludes POST;
  REG-only sensitivity is separate. These findings establish neither added prediction
  nor an intrinsic trainable agility capacity.
- The frozen route-family measurement screen failed (adjusted SB=0.296 <0.40). No new
  TURN association/evaluation was opened. Follow the prespecified stopping rule; retain
  wide intervals and the shared-adjustment limitation instead of calling this proof of zero.
- Model audit saves all 15 converged fits and boundary warnings. Unique-player Study 2
  SDs and player-clustered binary LPM sensitivities are now reproducible. Expected signs
  did not explicitly preregister a one-sided test, so the separate audit conservatively
  reports two-sided Holm results (0/9 original-family tests, 0/3 binary sensitivities).
- Exposure-only hero pair: development WRs within 0.03 s in observed forty, greatest
  TURN difference, deterministic ties; first recorded speed-out attempt. Draft traces
  use start-relative translation only and exact cached attempt quantiles. They illustrate
  measurement, not NFL success or a ranking recommendation.
- Remaining material gaps: earlier-study held-out prediction, same-sample 3-cone analysis,
  complete raw-input submission rebuilding, and official field semantics/citations.

## 2026-11-10 — Cohort/cone review

- The earlier prediction/cone gaps are now addressed by separate, versioned analyses. Rookie-only cohort prediction and historical all-REG cone associations are not pooled into one claim. No evaluation-player intercepts are fitted, and training preprocessing uses unique players/development-only drill references. Artifacts verify all 25 scores.
- No primary marginal interval supports an RMSE gain; all original-family intervals cross zero. This does not establish equivalence. Nominal deterioration in DL burst/get-off depends on family/support sensitivity; retain uncertainty rather than asserting harm.
- Cone subset DL TURN/pressure association is positive, but its cohort prediction is not supported. DL A0 improves in a nine-player cone cohort subset. These selected secondary exceptions are disclosed without granting a general scouting ranking recommendation.
- Training-fit uncertainty is not included in paired evaluation bootstraps. Numerical default-optimizer failures were resolved before opening evaluation, using the same-model Powell retry rule with finite fixed-coefficient/SE checks; warnings are retained.
- Remaining gaps for submission: full raw-input notebook rebuilding of validated results, official field semantics/citations, final figure/wording review and clean Kaggle execution. The notebook's embedded evaluation table is explicitly a review snapshot.
