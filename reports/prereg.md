# Pre-registration (frozen 2026-10-29, before any Combine-trait ↔ outcome analysis)

Written before fitting any model that relates Combine traits to NFL outcomes. Changes after this date
must be appended under "Amendments" with a date and reason, never edited in place.

## Traits (exposures) — fixed
From `src/combine_features.py` (drill-normalised, agility + position drills, 40 excluded):
- **TURN** = `lat` (90th pct |lateral accel| per attempt, z within drill, averaged across drills)
- **BURST** = `burst` (max forward accel per attempt, z within drill, averaged across drills)
Both z-scored again within combine_position before modelling. No other trait enters a confirmatory test.

## Confirmatory hypotheses (6 tests, Holm-corrected at family α = 0.05)

| ID | Group | Outcome (REG season, play not nullified) | Expected sign |
|---|---|---|---|
| W1 | WR | `separation_at_pass_forward` on every route with a recorded value | TURN + |
| W2 | WR | same | BURST + |
| O1 | OL | `pressure_allowed` (binary) on pass-block snaps (`pressure_allowed` not null) | TURN − (less pressure) |
| O2 | OL | same | BURST − |
| D1 | DL | `player_get_off` (s, lower = faster) on snaps where recorded | BURST − (faster) |
| D2 | DL | pressure generated (`time_to_pressure` not null) on pass-rush snaps (`sack` not null) | TURN + |

## Models — fixed
Play-level mixed models, random intercept for player (and for team-season where it converges):
- **Baseline covariates (all):** draft slot (`draft_overall_pick`, UDFA = 260, plus UDFA indicator), `forty`
  (missing → position median + missing indicator), `combine_weight`, `combine_height`, season, down, yards_to_go.
- **WR extra context:** `route_ran`, `cushion`, `team_coverage_man_zone`, `receiver_alignment`, `in_motion_at_ball_snap`.
  (`pass_length` excluded: partly a consequence of separation.)
- **OL extra context:** `dropback_duration`, `pass_rushers_encountered`.
- **DL extra context:** `blitzing`, `lined_up_position`.
- Linear mixed model for continuous outcomes; logistic GLMM (or linear probability with robust SE as fallback) for binary.
- Test = trait coefficient (one trait at a time added to baseline; plus both together as secondary).
- Effect reported per 1 SD of trait, with 95% interval.

## Incremental-value test (headline)
For each group: compare baseline vs baseline + trait(s) by (a) the trait coefficient and (b) out-of-sample
prediction of player-level adjusted outcome on the **2025 draft class** after fitting on 2023–24 classes.
Secondary model on the subset with a 3-cone time: does the trait still add over the 3-cone?

## Transfer test (go/no-go; PLAN.md §2)
Same traits computed from game tracking (per player-season, REG + PRE frames, normalised within lined-up position).
Go if Combine↔game trait correlation ≥ 0.3 for the chosen group AND the confirmatory test for that group holds
(Holm-adjusted p < 0.05 or 95% interval excluding 0 in the expected direction).

## Exploratory (labelled as such in the writeup)
Everything else: other traits (brake, vmax, cut features), TE, DB, career outcomes, interactions with route type.

## Amendments
- **2026-10-29 (before computing any transfer correlation):** game-side trait measurement fixed as:
  per player-play, kinematics from `src/kinematics.py` on the full track, then frames in the window
  [ball_snap, ball_snap + 3.0 s] (truncated at track end); lat = 90th pct |a_lat|, burst = max a_lon, vmax = max speed.
  Plays without a ball_snap tag are dropped. Normalisation: z within (lined_up_position × play type), where play type =
  `route_ran` for WR/TE and pass vs run for OL/DL (OL: `dropback_duration` not null; DL: `sack` not null); player-season trait = mean z over plays
  (min 30 plays). Transfer correlation = Pearson r between Combine trait and the player's game trait pooled over seasons.

---

# Study 1 result (2026-10-29)
All six confirmatory tests null (reports/confirmatory.md). Go/no-go rule → **no-go** for the envelope thesis.
Transfer: DL burst r=0.45 (0.21 net of weight); WR lat r=0.28 (unchanged net of weight/role/40) — reports/transfer.md.

# Study 2 pre-registration — "First Step" (frozen 2026-10-29, before computing any 40-yard tracking feature)

Motivation (from outcome-reliability check, which used no Combine traits): DL `player_get_off` and OL
`peak_pressure_probability_allowed` are the most reliable player-level outcomes (split-half SB 0.80 each).
Study 1 used agility-drill burst; the plan's backup (PLAN.md §2) specified **start-of-40 acceleration**, untested so far.

## Exposure (fixed)
From FORTY_YARD_DASH tracking, per attempt: movement onset = first frame with speed ≥ 0.5 yd/s; fit the mono-exponential
sprint model v(t) = vmax·(1 − exp(−(t − t0)/τ)) to speed from onset to the end of the run (least squares, t0 free in
[−0.3, 0.3] s around onset). Derived: **A0 = vmax/τ** (initial acceleration capacity, yd/s²). Player value = mean over attempts;
z-scored within combine_position. One exposure only: **A0**.

## Confirmatory tests (Holm across 3)
| ID | Group | Outcome | Expected |
|---|---|---|---|
| F1 | DL | `player_get_off` (lower = faster) | A0 − |
| F2 | OL | `peak_pressure_probability_allowed` | A0 − |
| F3 | WR | `separation_at_pass_forward` | A0 + |
Model, filters and covariates identical to Study 1 (same BASE + group context; DL F1 uses D1 context, OL F2 uses O1 context,
WR F3 uses W1 context). **Plus** `ten_yd_split` (missing → position median + indicator) as an extra covariate, so the test is
"does tracking-derived A0 add beyond the stopwatch's own acceleration measure?"

## Secondary (pre-specified, not in Holm family)
Same models without `ten_yd_split` (to show what the stopwatch already captures); reliability of A0 (attempt 1 vs 2).
