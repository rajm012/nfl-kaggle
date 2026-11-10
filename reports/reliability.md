# Movement reliability reproduction

Generated UTC: 2026-11-09T14:35:44.259548+00:00. Seed 20261109; 10,000 paired athlete bootstrap resamples.

Cross-drill halves use alphabetically ordered canonical drills, alternating within athlete, as in the original pipeline. These measure consistency across different tasks, not same-route test–retest. Spearman–Brown (SB) assumes comparable halves; negative values are retained and intervals describe substantial uncertainty.

| sample | position | feature | n | r | r_lo | r_hi | SB | SB_lo | SB_hi | valid_bootstraps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| historical full cohort | WR | lat | 107 | 0.375 | 0.218 | 0.515 | 0.546 | 0.357 | 0.68 | 10000 |
| historical full cohort | WR | burst | 107 | 0.478 | 0.315 | 0.615 | 0.647 | 0.48 | 0.761 | 10000 |
| historical full cohort | WR | brake | 107 | 0.07 | -0.126 | 0.268 | 0.131 | -0.289 | 0.422 | 10000 |
| historical full cohort | WR | vmax | 107 | 0.37 | 0.189 | 0.533 | 0.541 | 0.318 | 0.696 | 10000 |
| development, training reference | WR | TURN | 70 | 0.421 | 0.229 | 0.583 | 0.593 | 0.373 | 0.737 | 10000 |
| historical full cohort | DB | lat | 122 | 0.141 | -0.053 | 0.317 | 0.247 | -0.111 | 0.482 | 10000 |
| historical full cohort | DB | burst | 122 | 0.06 | -0.136 | 0.248 | 0.114 | -0.316 | 0.398 | 10000 |
| historical full cohort | DB | brake | 122 | 0.185 | 0.01 | 0.351 | 0.312 | 0.019 | 0.52 | 10000 |
| historical full cohort | DB | vmax | 122 | 0.558 | 0.42 | 0.675 | 0.716 | 0.591 | 0.806 | 10000 |
| development, training reference | DB | TURN | 85 | 0.164 | -0.061 | 0.371 | 0.282 | -0.13 | 0.541 | 10000 |
| historical full cohort | OL | lat | 121 | 0.43 | 0.267 | 0.57 | 0.602 | 0.422 | 0.726 | 10000 |
| historical full cohort | OL | burst | 121 | 0.277 | 0.087 | 0.443 | 0.434 | 0.16 | 0.614 | 10000 |
| historical full cohort | OL | brake | 121 | -0.034 | -0.239 | 0.179 | -0.071 | -0.627 | 0.303 | 10000 |
| historical full cohort | OL | vmax | 121 | 0.65 | 0.534 | 0.75 | 0.788 | 0.696 | 0.857 | 10000 |
| development, training reference | OL | TURN | 83 | 0.335 | 0.118 | 0.522 | 0.502 | 0.211 | 0.686 | 10000 |
| historical full cohort | DL | lat | 118 | 0.404 | 0.258 | 0.54 | 0.575 | 0.41 | 0.701 | 10000 |
| historical full cohort | DL | burst | 118 | 0.418 | 0.246 | 0.559 | 0.589 | 0.395 | 0.717 | 10000 |
| historical full cohort | DL | brake | 118 | 0.234 | 0.072 | 0.387 | 0.379 | 0.134 | 0.558 | 10000 |
| historical full cohort | DL | vmax | 118 | 0.745 | 0.659 | 0.814 | 0.854 | 0.794 | 0.898 | 10000 |
| development, training reference | DL | TURN | 74 | 0.339 | 0.149 | 0.506 | 0.506 | 0.259 | 0.672 | 10000 |
| historical full cohort | TE | lat | 42 | 0.057 | -0.293 | 0.397 | 0.109 | -0.828 | 0.568 | 10000 |
| historical full cohort | TE | burst | 42 | 0.454 | 0.2 | 0.705 | 0.625 | 0.333 | 0.827 | 10000 |
| historical full cohort | TE | brake | 42 | 0.163 | -0.078 | 0.453 | 0.281 | -0.168 | 0.624 | 10000 |
| historical full cohort | TE | vmax | 42 | 0.307 | 0.044 | 0.555 | 0.47 | 0.085 | 0.714 | 10000 |
| development, training reference | TE | TURN | 25 | 0.179 | -0.217 | 0.55 | 0.303 | -0.555 | 0.71 | 10000 |

## Same-drill TURN repeats

First two attempts by recorded attempt number (event ID breaks ties). Pearson r is the repeat correlation; SB is a two-attempt composite estimate, not the reliability of a single attempt. Fewer than four pairs return no estimate. No reliability-based feature selection or attempt exclusion. These descriptive repeats include all classes.

| position | drill | n | r | r_lo | r_hi | SB | SB_lo | SB_hi | valid_bootstraps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DB | BACK_PEDAL_AND_90_DEGREE_BREAK_TO_BALL | 2 | None | None | None | None | None | None | 0 |
| DB | BACK_PEDAL_AND_TRANSITION_45_DEGREE_REACTION | 119 | 0.583 | 0.437 | 0.71 | 0.736 | 0.608 | 0.831 | 10000 |
| DB | BOX_DRILL | 3 | None | None | None | None | None | None | 0 |
| DB | GAUNTLET_DRILL | 4 | 0.663 | -1.0 | 1.0 | 0.797 | None | 1.0 | 9857 |
| DB | LINE_DRILL | 99 | 0.215 | 0.039 | 0.402 | 0.353 | 0.075 | 0.574 | 10000 |
| DB | SHORT_SHUTTLE | 8 | 0.159 | -0.563 | 0.868 | 0.274 | -2.572 | 0.929 | 10000 |
| DB | TERYL_AUSTIN_DRILL_1 | 2 | None | None | None | None | None | None | 0 |
| DB | TERYL_AUSTIN_DRILL_2 | 2 | None | None | None | None | None | None | 0 |
| DB | THREE_CONE_DRILL | 7 | 0.484 | -0.755 | 0.964 | 0.653 | -6.147 | 0.982 | 10000 |
| DB | W_DRILL | 3 | None | None | None | None | None | None | 0 |
| DL | BACK_PEDAL_AND_REACT | 3 | None | None | None | None | None | None | 0 |
| DL | BODY_CONTROL_DRILL | 2 | None | None | None | None | None | None | 0 |
| DL | PASS_RUSH_DRILL | 106 | 0.437 | 0.268 | 0.595 | 0.609 | 0.422 | 0.746 | 10000 |
| DL | RUN_AND_CLUB_DRILL | 1 | None | None | None | None | None | None | 0 |
| DL | RUN_THE_HOOP_DRILL | 10 | 0.483 | -0.147 | 0.828 | 0.652 | -0.344 | 0.906 | 10000 |
| DL | SHORT_SHUTTLE | 4 | -0.152 | -1.0 | 1.0 | -0.359 | None | 1.0 | 9857 |
| DL | SHORT_ZONE_BREAKS | 39 | 0.202 | -0.079 | 0.505 | 0.336 | -0.172 | 0.671 | 10000 |
| DL | THREE_CONE_DRILL | 12 | 0.087 | -0.542 | 0.666 | 0.16 | -2.362 | 0.8 | 10000 |
| OL | PASS_RUSH_DROP | 118 | 0.235 | 0.084 | 0.37 | 0.38 | 0.154 | 0.54 | 10000 |
| OL | SCREEN_DRILL | 1 | None | None | None | None | None | None | 0 |
| OL | SHORT_SHUTTLE | 13 | 0.583 | 0.268 | 0.886 | 0.737 | 0.422 | 0.94 | 10000 |
| OL | THREE_CONE_DRILL | 7 | 0.312 | -0.468 | 0.814 | 0.476 | -1.761 | 0.898 | 10000 |
| TE | BLOCK_EXPLOSION | 1 | None | None | None | None | None | None | 0 |
| TE | CORNER_ROUTE | 29 | 0.423 | 0.059 | 0.711 | 0.595 | 0.111 | 0.831 | 10000 |
| TE | END_ZONE_FADE_RIGHT | 7 | 0.703 | -0.406 | 0.995 | 0.826 | -1.365 | 0.998 | 10000 |
| TE | GAUNTLET_DRILL | 40 | 0.539 | 0.206 | 0.755 | 0.701 | 0.342 | 0.86 | 10000 |
| TE | HOOK_ROUTE_RIGHT | 4 | -0.538 | -1.0 | 1.0 | -2.329 | None | 1.0 | 9857 |
| TE | IN_ROUTE_LEFT | 3 | None | None | None | None | None | None | 0 |
| TE | OVER_SHOULDER_ADJUST | 4 | 0.132 | -1.0 | 1.0 | 0.234 | None | 1.0 | 9857 |
| TE | SHORT_SHUTTLE | 11 | 0.399 | -0.341 | 0.814 | 0.571 | -1.037 | 0.897 | 10000 |
| TE | THREE_CONE_DRILL | 7 | 0.587 | -0.314 | 0.997 | 0.74 | -0.918 | 0.999 | 10000 |
| TE | WHEEL_ROUTE_LEFT | 5 | 0.996 | 0.952 | 1.0 | 0.998 | 0.976 | 1.0 | 9982 |
| WR | CIRCUS_ROUTE_LEFT | 6 | 0.756 | -0.891 | 0.998 | 0.861 | -16.34 | 0.999 | 10000 |
| WR | COMEBACK_ROUTE_RIGHT | 12 | 0.534 | 0.043 | 0.963 | 0.697 | 0.082 | 0.981 | 10000 |
| WR | CURL_ROUTE_RIGHT | 7 | -0.391 | -0.927 | 0.681 | -1.285 | -25.429 | 0.81 | 10000 |
| WR | DAGGER_ROUTE_LEFT | 8 | 0.298 | -0.337 | 0.884 | 0.459 | -1.017 | 0.938 | 10000 |
| WR | GAUNTLET_DRILL | 93 | 0.331 | 0.105 | 0.506 | 0.498 | 0.189 | 0.672 | 10000 |
| WR | GO_ROUTE_RIGHT | 7 | 0.074 | -0.775 | 0.911 | 0.138 | -6.88 | 0.953 | 10000 |
| WR | OVER_SHOULDER_ADJUST | 1 | None | None | None | None | None | None | 0 |
| WR | POST_CORNER_ROUTE_LEFT | 10 | 0.495 | -0.276 | 0.909 | 0.662 | -0.762 | 0.952 | 10000 |
| WR | POST_CORNER_ROUTE_RIGHT | 15 | 0.375 | -0.179 | 0.874 | 0.546 | -0.436 | 0.933 | 10000 |
| WR | RED_ZONE_FADE_RIGHT | 13 | 0.511 | -0.065 | 0.859 | 0.676 | -0.138 | 0.924 | 10000 |
| WR | SHORT_SHUTTLE | 6 | -0.651 | -1.0 | 0.492 | -3.727 | -1139604.445 | 0.659 | 10000 |
| WR | SLANT_ROUTE_LEFT | 3 | None | None | None | None | None | None | 0 |
| WR | SLOT_SAIL_ROUTE_RIGHT | 8 | -0.011 | -0.951 | 0.929 | -0.022 | -39.159 | 0.963 | 10000 |
| WR | SLOT_STRIKE_ROUTE_LEFT | 1 | None | None | None | None | None | None | 0 |
| WR | SPEED_OUT_ROUTE_LEFT | 17 | 0.012 | -0.442 | 0.492 | 0.024 | -1.587 | 0.659 | 10000 |
| WR | THREE_CONE_DRILL | 5 | 0.723 | 0.147 | 1.0 | 0.839 | 0.257 | 1.0 | 9982 |

## Exposure QC and training-only reference

| attempts | nonfinite_turn_attempts | nonpositive_duration | nonfinite_coordinates | dropped_attempts | turn_range |
| --- | --- | --- | --- | --- | --- |
| 5517 | 0 | 0 | 0 | 0 | [0.30545849645434453, 7.743827875910975] |

Training-reference means/SDs use unique player/drill means from 2023–24 athletes across positions. The same reference transforms 2025 without using its distribution. Excluded constant/sparse drills: []; unseen drills: ['CIRCUS_ROUTE_LEFT', 'SHORT_ZONE_BREAK_FLAT_WHEEL', 'SHORT_ZONE_BREAK_FORWARD', 'SHORT_ZONE_BREAK_INSIDE']. Metadata: `study3_turn_reference.json`.

This check uses no NFL outcomes. Trace figures and the route-contrast measurement screen are separate requirements. Historical reports remain unchanged.
