# Step 2 descriptive measurement protocol — 2026-11-11

Written before calculating new trace summaries. This is an exposure-only explanation of
the existing hero pair, not a new NFL outcome hypothesis. The pair/event IDs remain exactly
those in `route_trace_selection.json`; no replacement or favourable-result selection.
Frozen prediction and Study 3 protocols remain in force.

## Inputs and reference

- Read only existing `combine_frames.parquet`, `combine_attempts.parquet`,
  `combine_results.parquet`, `study3_turn.parquet`, `study3_turn_reference.json`, the
  saved selection, reliability and movement-transfer reports. No `player_play`, game
  outcomes or 2025 performance tables enter new calculations.
- Filter frame columns/rows to the two saved event IDs before collecting.
- Use cached `sp`, `a_lon`, `a_lat`, `curv` from the unchanged `src.kinematics` rule:
  10 Hz, seven samples, quadratic Savitzky–Golay derivatives. The seven-sample window
  covers 0.6 seconds between endpoints. Do not tune smoothing or thresholds.
- Recompute the two tracks with that same helper as a preservation check; do not replace
  shared source or historical features. Display original coordinates translated to their
  first recorded position, with common axes and no rotation/rescaling.
- Use the saved 2023–24 player/drill means and SDs to explain composite TURN. Average raw
  attempt lateral-acceleration percentiles within each player/drill, then standardize each
  drill with those references and average available drills. Express the composite in
  development-WR athlete SD units exactly as the original hero figure did. No new reference
  fitting or new player score.

## Fixed summaries

1. **Full-attempt lateral acceleration:** reproduce the existing nearest-rank 90th percentile
   of absolute `a_lat` (Polars' recorded `quantile(0.9)` default). Report yd/s², separately
   from the unitless across-drill profile. Include event frame count and recorded elapsed
   span `(last time − first time)`, not a claimed timed drill completion.
2. **Interior reference peak:** discard the first and last three samples for new local
   summaries to avoid derivative edges. Require speed at least 1 yd/s and finite derived
   quantities. Choose the first maximum absolute lateral acceleration in the remaining
   frames, using time order for ties. Call it the *interior lateral-acceleration peak*,
   not detected cut onset, ideal break, or reaction time.
3. **At that peak:** report elapsed time, speed (yd/s), absolute lateral acceleration
   (yd/s²), absolute curvature (1/yd) and approximate local radius `1/abs(curvature)` (yd).
   Report radius unavailable if absolute curvature is at most 1e-6. Above the speed floor,
   `abs(a_lat) = speed² × abs(curvature)` is a kinematic identity, not causal attribution.
4. **Nearby speed:** take the median speed in `[peak−0.3 s, peak−0.1 s]` and
   `[peak+0.1 s, peak+0.3 s]`, using interior, finite frames above the same speed floor.
   Require three samples in each window. Otherwise mark the window unavailable; do not
   move the peak, extend the window or lower the threshold. Call these *pre/post-peak
   windows*, not validated drill-entry/exit phases. Report their difference, not an
   efficiency score or a validated reacceleration metric.
5. **Across-drill explanation:** retain all available drill rows for each selected athlete,
   their attempt counts, mean raw percentile, saved reference mean/SD, standardized value
   and contribution `z / number of available drills`. Show absent drills as absent, never
   impute. Only decompose B−A into drill contributions if the two drill sets are identical;
   otherwise explain separate composites and their drill-mix limitation.

## Quality gates

- Verify saved player/event IDs, canonical speed-out label, frame counts, unique times,
  strictly increasing 0.1-second cadence (absolute tolerance 1e-6 s), finite coordinates
  and cached quantities, and sufficient interior samples. If cadence fails, local
  physical summaries are unavailable; do not silently resample or repair the frozen track.
- Cached/recomputed kinematics must agree within `rtol=1e-10, atol=1e-10`. Reproduced
  historical percentiles/profile values must agree within `rtol=1e-10, atol=1e-10`.
- Check the identity on the eligible interior frames and preserve all window availability
  failures. Do not treat algebraic reconstruction as independent measurement validation.
- Meaningful synthetic checks cover straight motion, circular motion at known radius,
  speed dependence and translation/rotation invariance. These check physical behavior,
  not agreement with a copied implementation.
- No new cross-athlete outcome associations, athlete rankings, reliability thresholds,
  route-gate changes or training-effect claims. Existing same-drill repeat results may
  be cited with their sample/uncertainty limits, without fitting another reliability model.

## Outputs and interpretation

`src.wr_movement` writes `reports/wr_movement_metrics.json`,
`reports/wr_movement_explanation.md` and a candidate replacement
`reports/figures/combine_route_trace_explained.png`. The original published figure and
packet remain intact until Step 5 integration. The candidate replaces Figure 1 rather
than adding a seventh main figure. It marks the reference peak and fixed windows and
distinguishes the single-attempt data from the across-drill headline.

Report source/protocol hashes and gates. A faster or tighter segment may have larger
lateral acceleration; neither is proof of superior talent, efficient cutting, individual
repeatability, game separation or useful coaching intervention. Size/40-adjusted historical
transfer is population-level evidence, not a control for these attempts' entry speeds.
