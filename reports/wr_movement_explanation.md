# Step 2 — What the receiver movement difference means

Descriptive review of the existing pair, using the written [measurement protocol](wr_trace_measurement_protocol.md). Rebuild with `.venv/bin/python -m src.wr_movement`. Values and hashes: [wr_movement_metrics.json](wr_movement_metrics.json).

## The plain-language explanation

TURN measures lateral acceleration: how strongly the direction of movement changes while a player is moving. A faster player on the same curved path has more lateral acceleration. At the same speed, a tighter path also has more lateral acceleration. A larger TURN value therefore does not by itself mean better or more efficient cutting.

For motion above the written speed floor, **absolute lateral acceleration = speed² × absolute path curvature**. This identity describes these same position-derived quantities; it is not independent validation or a causal breakdown of talent. Forty times measure a different task and do not hold these drill speeds constant.

## The two recorded attempts

| Quantity | WR A | WR B |
|---|---:|---:|
| Observed 40 time (s) | 4.540 | 4.520 |
| Across-drill profile (development WR SD) | -1.782 | 2.533 |
| Full-attempt 90th-percentile lateral acceleration (yd/s²) | 6.620 | 7.218 |
| Recorded elapsed span (s) | 4.200 | 4.900 |
| Interior reference peak (s) | 2.700 | 3.000 |
| Speed at reference peak (yd/s) | 5.433 | 5.879 |
| Lateral acceleration at reference peak (yd/s²) | 7.348 | 8.069 |
| Local curvature at reference peak (1/yd) | 0.249 | 0.233 |
| Approximate local radius at reference peak (yd) | 4.017 | 4.284 |

At the separately selected reference peaks, B has higher lateral acceleration (8.07 versus 7.35 yd/s²) and higher speed (5.88 versus 5.43 yd/s). Its local curvature is lower (0.233 versus 0.249 1/yd), corresponding to a slightly wider local radius. This illustrates why larger lateral acceleration cannot be equated with a tighter turn. It does not assign causal credit to speed or identify the better receiver.

These peaks are chosen separately by the same written rule. They are not matched football situations, validated break events, reaction times or a causal comparison. The recorded span is not timed drill completion. The full-attempt percentile and the interior peak summarize different samples.

### Fixed windows around the reference peak

| Athlete | Pre-peak speed | Post-peak speed | Post minus pre | Available samples |
|---|---:|---:|---:|---|
| WR A | 5.600 | 5.662 | 0.062 | 3 / 3 |
| WR B | 6.081 | 5.967 | -0.115 | 3 / 3 |

Speeds are yd/s in fixed 0.3-to-0.1-second windows before/after the peak. These are descriptive local windows, not verified drill-entry/exit phases or a new reacceleration score. Do not read a speed difference as proof that one receiver cuts more efficiently.

## Why one attempt does not explain the headline profile

The headings summarize several non-40 drills, after averaging attempts within each drill and standardizing against the saved development reference. The selected speed-out attempt is only one illustration. A large across-drill gap does not imply the same-sized difference in this one drill.

The athletes have identical available drill sets. Every available referenced drill is retained below; missing drills are not imputed.

### WR A: 13 drills

| Drill | Attempts | Raw percentile mean (yd/s²) | Reference mean | Reference SD | Drill z | Contribution to composite |
|---|---:|---:|---:|---:|---:|---:|
| COMEBACK_ROUTE_RIGHT | 1 | 5.298 | 5.920 | 0.637 | -0.976 | -0.075 |
| CURL_ROUTE_RIGHT | 1 | 4.499 | 5.908 | 0.861 | -1.637 | -0.126 |
| DAGGER_ROUTE_LEFT | 2 | 5.718 | 5.930 | 0.700 | -0.303 | -0.023 |
| GAUNTLET_DRILL | 2 | 5.701 | 5.030 | 0.657 | 1.023 | 0.079 |
| GO_ROUTE_RIGHT | 2 | 1.018 | 1.725 | 0.740 | -0.955 | -0.073 |
| OVER_SHOULDER_ADJUST | 1 | 0.717 | 1.532 | 0.741 | -1.100 | -0.085 |
| POST_CORNER_ROUTE_LEFT | 1 | 5.849 | 6.266 | 0.552 | -0.757 | -0.058 |
| POST_CORNER_ROUTE_RIGHT | 1 | 4.079 | 4.507 | 0.558 | -0.768 | -0.059 |
| RED_ZONE_FADE_RIGHT | 1 | 0.982 | 1.772 | 0.467 | -1.692 | -0.130 |
| SLANT_ROUTE_LEFT | 1 | 4.485 | 4.116 | 0.710 | 0.520 | 0.040 |
| SLOT_SAIL_ROUTE_RIGHT | 1 | 5.906 | 6.465 | 0.611 | -0.916 | -0.070 |
| SLOT_STRIKE_ROUTE_LEFT | 1 | 4.115 | 5.441 | 0.598 | -2.217 | -0.171 |
| SPEED_OUT_ROUTE_LEFT | 1 | 6.620 | 6.665 | 0.435 | -0.102 | -0.008 |

The drill z values average to -0.76011; expressed in development-WR athlete SD units, this is -1.78215, matching the historical heading.

### WR B: 13 drills

| Drill | Attempts | Raw percentile mean (yd/s²) | Reference mean | Reference SD | Drill z | Contribution to composite |
|---|---:|---:|---:|---:|---:|---:|
| COMEBACK_ROUTE_RIGHT | 1 | 7.099 | 5.920 | 0.637 | 1.852 | 0.142 |
| CURL_ROUTE_RIGHT | 1 | 7.302 | 5.908 | 0.861 | 1.619 | 0.125 |
| DAGGER_ROUTE_LEFT | 1 | 7.049 | 5.930 | 0.700 | 1.597 | 0.123 |
| GAUNTLET_DRILL | 2 | 5.512 | 5.030 | 0.657 | 0.735 | 0.057 |
| GO_ROUTE_RIGHT | 1 | 0.653 | 1.725 | 0.740 | -1.449 | -0.111 |
| OVER_SHOULDER_ADJUST | 1 | 2.583 | 1.532 | 0.741 | 1.419 | 0.109 |
| POST_CORNER_ROUTE_LEFT | 2 | 6.242 | 6.266 | 0.552 | -0.043 | -0.003 |
| POST_CORNER_ROUTE_RIGHT | 1 | 5.320 | 4.507 | 0.558 | 1.455 | 0.112 |
| RED_ZONE_FADE_RIGHT | 1 | 2.089 | 1.772 | 0.467 | 0.680 | 0.052 |
| SLANT_ROUTE_LEFT | 1 | 5.817 | 4.116 | 0.710 | 2.397 | 0.184 |
| SLOT_SAIL_ROUTE_RIGHT | 1 | 6.891 | 6.465 | 0.611 | 0.698 | 0.054 |
| SLOT_STRIKE_ROUTE_LEFT | 1 | 6.078 | 5.441 | 0.598 | 1.065 | 0.082 |
| SPEED_OUT_ROUTE_LEFT | 1 | 7.218 | 6.665 | 0.435 | 1.271 | 0.098 |

The drill z values average to 1.02276; expressed in development-WR athlete SD units, this is +2.53314, matching the historical heading.

### Arithmetic contribution to the composite difference

| Drill | B minus A drill z | Contribution to B minus A composite |
|---|---:|---:|
| COMEBACK_ROUTE_RIGHT | +2.828 | +0.218 |
| CURL_ROUTE_RIGHT | +3.257 | +0.251 |
| DAGGER_ROUTE_LEFT | +1.901 | +0.146 |
| GAUNTLET_DRILL | -0.288 | -0.022 |
| GO_ROUTE_RIGHT | -0.493 | -0.038 |
| OVER_SHOULDER_ADJUST | +2.519 | +0.194 |
| POST_CORNER_ROUTE_LEFT | +0.713 | +0.055 |
| POST_CORNER_ROUTE_RIGHT | +2.223 | +0.171 |
| RED_ZONE_FADE_RIGHT | +2.372 | +0.182 |
| SLANT_ROUTE_LEFT | +1.877 | +0.144 |
| SLOT_SAIL_ROUTE_RIGHT | +1.614 | +0.124 |
| SLOT_STRIKE_ROUTE_LEFT | +3.282 | +0.252 |
| SPEED_OUT_ROUTE_LEFT | +1.373 | +0.106 |

The speed-out difference contributes 0.10562 of the 1.78286 raw composite gap (5.9% arithmetically). The across-drill contrast is broader than the single illustrated speed-out. These equal-weight contributions are accounting identities, not causal explanations of talent or performance.

The training drill reference uses 2023–24 athletes across positions; the final display uses development WR mean/SD. Standardizing drills puts values on comparable scales; it does not remove speed dependence or prove that each drill measures the same talent.

## Reliability and size/speed adjustments

The existing same-drill report has 17 WR speed-out repeat pairs: r=0.012 [-0.442, 0.492], two-attempt composite SB=0.024. This wide, uncertain repeat result does not establish an individual speed-out score. The development cross-drill SB of 0.593 is a different measurement across tasks and athletes.

Existing PRE+REG WR movement transfer, raw: r=0.279 [0.107, 0.445], n=98. This is population-level descriptive transfer, not an adjustment for the entry speed of these two attempts or improved separation prediction.

Existing PRE+REG WR movement transfer, weight-adjusted: r=0.281 [0.099, 0.457], n=98. This is population-level descriptive transfer, not an adjustment for the entry speed of these two attempts or improved separation prediction.

Existing PRE+REG WR movement transfer, size+forty-adjusted: r=0.278 [0.092, 0.450], n=98. This is population-level descriptive transfer, not an adjustment for the entry speed of these two attempts or improved separation prediction.

## Candidate Figure 1 and writeup wording

The [candidate replacement figure](figures/combine_route_trace_explained.png) adds the speed curve, reference peak and fixed local windows to the original path/acceleration view. It keeps the original pair, common axes and separately labelled across-drill profile. The existing published Figure 1 remains intact for Step 5 integration; this candidate would replace it, not add a seventh main figure.

**Proposed methods wording:** “TURN summarizes the upper range of lateral acceleration across non-40 drills. Lateral acceleration increases with both speed and path curvature, so a higher profile can reflect drill execution as well as movement ability. The illustrated speed-out attempts show path, speed and acceleration; the headings summarize multiple drills. Neither view establishes cutting efficiency or an individual talent ranking.”

**Proposed caption:** “Same selected receivers, one recorded speed-out attempt each. Headings show their across-drill TURN profiles. Dotted lines/crosses mark an interior lateral-acceleration peak using identical rules; speed-window shading is descriptive and does not identify a verified cut phase. Derivative-edge samples are shaded gray. The pair was selected for an extreme profile contrast, without NFL outcomes.”

## Quality, reproduction and limits

Full-attempt percentiles, composite headings and cached kinematics were checked against the recorded values. Local summaries require 10-Hz cadence, finite values, an interior speed floor and fixed window support. Failures remain unavailable; the saved metrics record each gate. Seven-sample quadratic derivatives span 0.6 seconds between endpoints and can blur brief movements; estimates are not direct measurements of forces.

The four physics checks run with `.venv/bin/python -m unittest discover -s tests -p wr_movement_checks.py -v`. They cover straight motion, circular motion at a known radius, quadratic speed dependence, rigid-coordinate invariance and rejection of irregular cadence. This sidecar check file stays outside the current notebook test bundle. Step 5 must include the new module, descriptive protocol and relevant checks if this figure is integrated into the standalone notebook.

No NFL outcomes enter these new summaries. No new outcome models, efficiency rankings, causal attribution, individual repeatability claims, route-gate changes or fitted-reference changes were made. The next step is the explanation of existing performance uncertainty.
