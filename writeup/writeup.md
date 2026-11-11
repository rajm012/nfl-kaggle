# Beyond the Stopwatch: When Should Combine Tracking Change a Scouting Decision?

Receiver A ran an observed 4.54-second 40; Receiver B ran 4.52. Their stopwatch results are close, yet their Combine movement profiles differ. Tracking makes that difference visible. A scouting department must decide what it justifies: a more specific film question, a change in development priorities, or a change on the draft board.

Across nine prescribed receiver and line comparisons, none of the primary 95% intervals supported improved NFL performance prediction from our tracking additions. Some movement carried into games. We therefore propose a practical rule: use movement differences to focus evaluation, and require additional performance evidence before recommending a scouting upgrade.

Our evidence map asks **Can we measure it consistently? Does it carry into games? Does it improve performance prediction beyond conventional measurables?** Each answer changes the confidence a scout can place in the next step. The map is a proposed review aid; its usefulness in actual scouting decisions has not been tested.

![Figure 1: Actual Combine speed-out paths and lateral acceleration for two development receivers with similar 40 times.](../reports/figures/combine_route_trace.png)

*Figure 1. Two development receivers with similar 40 times and different movement profiles. Selection used Combine exposures only: times within 0.03 seconds, largest training-reference TURN difference, deterministic ties. Paths are translated to their starts. No NFL outcome informed selection.*

## What tracking adds to the stopwatch

The supplied competition data contain 510 athletes, 22.65 million game-tracking frames and 314,197 player-play records. We connect player IDs across Combine tracking, conventional test results, draft information, game tracking and supplied performance fields. Key, count and join checks are reproducible in the notebook.

Tracking runs at 10 Hz. We smooth positions and derive acceleration along and perpendicular to travel, distinguishing speeding up from turning. The supplied total-acceleration magnitude combines those components. **TURN** is an attempt's 90th percentile of absolute lateral acceleration; **BURST** is peak longitudinal acceleration. We average attempts within athlete and drill, standardise within drill, then average across non-40 drills. Standardisation puts different drills on comparable scales.

**A0** estimates initial acceleration from a fitted 40-yard speed curve and addresses the separate first-step hypothesis. TURN depends on speed and path shape: a larger value can reflect how a drill was executed. These measurements do not establish intrinsic ability or a causal training effect.

Game movement uses the same decomposition, calculated on complete player tracks before restricting to the first three seconds after the snap. Movement-transfer analyses include preseason and regular season, explicitly excluding postseason. Performance analyses use regular season and exclude nullified plays.

The tracking contains rookie-cohort players rather than a full set of opponents and the ball. We therefore use the supplied performance/context fields and do not reconstruct defender leverage or separation trajectories. Receiver performance is the supplied separation-at-pass-forward field; line outcomes include get-off, pressure allowed, peak pressure probability allowed and an operational pressure flag based on recorded time-to-pressure presence.

![Figure 2: Unique-athlete support in the 2025 evaluation cohort.](../reports/figures/evidence_support.png)

*Figure 2. Exposure and outcome availability determine the evaluation sample. Thousands of plays improve an athlete's outcome estimate; they do not create thousands of independent prospects.*

## How we tested NFL relevance

Historical association models examine all available regular-season observations. Conventional controls include draft slot, undrafted status, body size, 40 time, season and football context. Receiver models account for route, coverage, alignment, cushion and motion; line models use the relevant supplied context. Player intercepts account for repeated observations.

The historical audit covers six movement tests and three first-step tests. It uses two-sided inference and Holm correction within those families because the recorded expected directions did not specify a one-sided threshold. First-step scaling uses unique athletes. Binary outcomes also receive a player-clustered linear-probability sensitivity; the original reports and correction record remain available.

Prediction asks a different question. We train on 2023–24 rookie regular seasons and evaluate 2025 rookie regular seasons. Drill references, player medians, scaling and context encoding are learned from training data. Every baseline and tracking-augmented model uses identical rows; the first-step baseline also includes the 10-yard split. All 25 primary, secondary and cone-subset pairs are frozen before scoring.

Predictions use fixed model components, without evaluation-player intercepts or recalibration. We average outcomes and predictions over each athlete's realised NFL contexts and give each athlete equal weight in root mean squared error (RMSE). Gain is baseline minus tracking RMSE; positive means improvement. Paired athlete bootstraps provide 95% intervals, with simultaneous intervals for the original six/three families. Binary prediction uses an unclipped linear-probability model, not a calibrated probability forecast.

These are retrospective, conditional predictions. They do not forecast a prospect's future route tree or playing opportunity. Earlier studies already used 2025 outcomes, so this is **not a pristine untouched holdout**. Bootstrap intervals condition on fitted training models and omit training-fit uncertainty. We also disclose the assumption that the latest trained calendar intercept persists into 2025.

Equal-athlete scoring limits high-volume starters' influence, while low exposure makes some athlete means noisy. WR TURN athletes have two to 401 valid plays, median 162. We retain the complete primary sample. The separately specified at-least-30-play sensitivity has 17 receivers and an uncertain prediction gain; its threshold was not chosen from results.

## Movement carries over, with limits

For 70 development receivers, training-reference TURN has cross-drill Spearman–Brown consistency of 0.593 [0.373, 0.737]. This is cohort-level agreement across drills; it does not establish reliability for a particular player or route-specific talent score. Only three receivers repeated the tracked slant drill, limiting a slant-specific interpretation.

Receiver turning transfers modestly to game movement: correlation 0.279 [0.107, 0.445], 98 athletes. Defensive-line burst transfer is stronger before adjustment: 0.443 [0.289, 0.584], 115 athletes. After controlling for weight, that DL correlation falls to 0.203 [0.044, 0.376]. Body size explains part of the apparent carryover. Adjustment refits within each athlete bootstrap; the figure also shows size-plus-40 adjustment.

![Figure 3: Movement-transfer correlations with athlete-bootstrap intervals and size adjustment.](../reports/figures/transfer_audited.png)

*Figure 3. These pooled-season movement correlations are descriptive. They establish neither added performance prediction nor a causal benefit from training the trait.*

We also registered a bounded receiver follow-up: whether TURN relates to separation on pooled SLANT/OUT routes relative to GO. Before fitting that interaction, we required the adjusted route-family separation contrast to repeat across alternating games. There were 42 eligible development receivers and 16 evaluation receivers; 41 supported the diagnostic halves.

The adjusted contrast's Spearman–Brown estimate was 0.296 [−0.257, 0.606], below the frozen 0.40 gate. Raw contrast consistency was 0.463. We stopped the primary interaction without weakening the threshold or changing route groups. The wide interval does not prove every route-specific relationship is zero. It means this measurement did not support the planned primary claim. Shared baseline adjustment across halves is an additional limitation.

![Figure 4: Raw and adjusted route-family contrast repeatability against the frozen measurement gate.](../reports/figures/study3_measurement.png)

*Figure 4. BREAK pools SLANT/OUT; panel intervals describe correlations. The gate failed before fitting a TURN interaction. Event-time separation does not measure separation caused specifically by a receiver's break.*

## Added performance prediction remains uncertain

The audited original association families contain zero Holm-significant results among nine tests. The three player-clustered binary sensitivities also contain none. Cohort prediction is consistent with a cautious conclusion: three primary point gains are positive and six negative, but none has a marginal interval supporting improvement. All original-family simultaneous intervals include zero. Primary evaluation samples contain 20–37 athletes.

For WR TURN, baseline separation RMSE is 0.23572 yards versus 0.23577 with tracking, with a gain interval of [−0.00903, 0.01267] yards across 23 receivers. DL TURN has a positive point gain for the recorded pressure proxy, with an interval crossing zero. DL BURST worsens get-off prediction nominally; its family-adjusted and at-least-30-play sensitivity intervals remain uncertain. We retain favourable and adverse results together.

![Figure 5: All nine primary cohort prediction gains and marginal bootstrap intervals.](../reports/figures/cohort_prediction.png)

*Figure 5. Positive is better. Points and intervals show relative RMSE reductions, conditional on training fits. The table supplies absolute errors and units.*

<!-- EVALUATION_TABLE -->

| Comparison | Unit | Athletes | Baseline RMSE | + Tracking RMSE | RMSE gain [95% interval] |
|---|---|---:|---:|---:|---:|
| WR turning / separation | yd | 23 | 0.23572 | 0.23577 | -0.00005 [-0.00903, 0.01267] |
| WR burst / separation | yd | 23 | 0.23572 | 0.23651 | -0.00079 [-0.00641, 0.00416] |
| OL turning / pressure allowed | proportion | 28 | 0.09511 | 0.09446 | +0.00065 [-0.00114, 0.00171] |
| OL burst / pressure allowed | proportion | 28 | 0.09511 | 0.09800 | -0.00290 [-0.00728, 0.00382] |
| DL burst / get-off time | s | 37 | 0.07583 | 0.07981 | -0.00398 [-0.00705, -0.00049] |
| DL turning / pressure generated | proportion | 37 | 0.04370 | 0.04255 | +0.00115 [-0.00008, 0.00231] |
| DL first step / get-off time | s | 23 | 0.09281 | 0.09216 | +0.00065 [-0.00086, 0.00195] |
| OL first step / peak pressure allowed | proportion | 22 | 0.09364 | 0.09373 | -0.00009 [-0.00181, 0.00066] |
| WR first step / separation | yd | 20 | 0.21054 | 0.21062 | -0.00008 [-0.00779, 0.00875] |

*Table 1. Equal-athlete RMSE; positive gain is better. Marginal 95% intervals condition on training fits; all original-family simultaneous intervals include zero.*

<!-- END_EVALUATION_TABLE -->

Cone checks retain selected secondary findings: the historical DL TURN pressure association is positive after adjustment, with uncertain cone-cohort prediction. DL A0 improves get-off RMSE by 0.00755 seconds [0.00443, 0.01080] in **nine athletes**, one of nine cone sensitivities. The broader primary remains uncertain. The notebook retains adverse findings and every comparison; missing cone times are never invented.

Absence of a supported gain does not establish equivalence, negligible effects or that all tracking features are useless. It limits the claims justified by these particular traits, models and samples.

## A concrete scouting conversation

Return to Receivers A and B. Their TURN profiles are −1.78 and +2.53 standard deviations within the development receiver cohort, despite similar 40 times. This pair illustrates what timing alone misses. The values summarise their observed drill profiles; the cross-drill consistency estimate above does not certify either player's individual repeatability.

**Measurement:** inspect the traced attempts and compare repeated, similarly executed drills when available. Ask how entry speed and break shape contribute to the lateral-acceleration difference. This guards against treating drill execution as a universal agility ranking.

**Transfer:** use the observed difference to request targeted film review of comparable out cuts: entry speed, break geometry and reacceleration. Coverage, cushion, motion and throw timing help interpret those situations. Film review is proposed here, not an analysis we performed; player-only coordinates cannot supply the missing opponent geometry.

**Performance:** the receiver prediction comparison does not support an automatic upgrade for the higher-TURN profile. Keep both prospects' movement observations alongside conventional measurables and football evaluation. The specific output of this meeting is a film question and an evidence gap, with draft recommendations requiring further support.

For linemen, the same discipline applies. DL burst transfers into game movement, but its weight-adjusted correlation is smaller and its primary get-off prediction addition lacks a supported gain. Get-off measures crossing the line of scrimmage after the snap, so it combines the initial response and forward movement.

The card can structure a development discussion, but this study establishes neither an individual change threshold nor that increasing TURN creates separation. Repeatable measurements, movement transfer and added performance value remain separate requirements.

![Figure 6: WR turning evidence card separating measurement, transfer and performance evidence.](../reports/figures/scout_evidence_card.png)

*Figure 6. A proposed film/practice-review aid, not a validated prospect-ranking or causal training prescription.*

The remaining limitations are substantial: small evaluation cohorts, selection into NFL playing time and cone participation, missing opponent geometry, observational context, numerical boundary fits and uncertainty conditional on training. The notebook rebuilds features, audits, frozen cohort evaluation, sensitivities and visuals directly from competition CSVs, while preserving the original research record.

The football contribution is a disciplined connection from Combine tracking to regular-season performance: measure movement, test transfer, and require evidence before turning either into a scouting upgrade.

Data source and attribution: [NFL Big Data Bowl 2027 competition data](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/data), NFL; CC BY-NC 4.0. Methods, protocols, exact filters, fit diagnostics and all secondary findings are included in the [attached reproducible notebook](https://www.kaggle.com/code/oppenheimer6th/combine-movement-to-nfl-decisions-an-evidence-map).
