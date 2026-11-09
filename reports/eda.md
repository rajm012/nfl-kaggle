# EDA findings

## Combine tracking (2026-10-08)
- 6,310 drill attempts, 62 drill names (~57 after alias cleanup), 10 Hz exactly (dt = 100 ms always).
- **Coverage:** position drills ~100% of each group (e.g. WR slant 107/107, DB backpedal-90 122/122)
  vs tracked 3-cone 160 players, shuttle 170, 40 418. → tracking agility exists for the ~65% who skip the 3-cone.
- Many drills have 1 attempt/player; some have 2 (WR/TE gauntlet, DB backpedal-45, DL pass-rush, OL pass-rush-drop).
  888 player-drill pairs with ≥2 attempts → test–retest available.
- `SKILL_DRILLS_LB` rows belong to players in combine_position DL (edge/OLB types), only 3–4 players.

## Kinematics
- `a` is **unsigned |total acceleration|** (min 0). Signed braking must be derived.
- Rebuilt from x,y with Savitzky–Golay (7 frames, quadratic): speed r=0.9995 vs `s`; |a| r=0.976 vs `a`.
  Decomposed into a_lon (speed change) and a_lat (turning). See `src/kinematics.py`.
- Lateral (turning) accel reaches ~7 yd/s² in route drills vs braking ~2.5–6 → **turning dominates** agility drills.
- WR route drills: speed often never dips at the break (rounded breaks); 3-cone: near-full stops at cones.

## Reliability of player traits (split-half by drill, Spearman–Brown; within position)
Raw pooled-frame envelope: ≈0 / negative (drill mix confound) → abandoned.
Drill-normalised z-scores (`src/combine_features.py`):

| trait | WR | DB | OL | DL | TE |
|---|---|---|---|---|---|
| lat (turning) | 0.55 | 0.25 | 0.60 | 0.58 | 0.11 |
| burst | 0.65 | 0.11 | 0.43 | 0.59 | 0.62 |
| brake | 0.13 | 0.31 | ≈0 | 0.38 | 0.28 |
| vmax | 0.54 | 0.72 | 0.79 | 0.85 | 0.47 |

Same-drill test–retest (median over drills): lat 0.44, brake 0.38, burst 0.35, vmax 0.61.

Correlation with stopwatch (within position): WR lat vs 3-cone −0.21, burst vs 3-cone −0.32 → largely new info.
DL traits correlate strongly with weight/40 (|r| 0.5–0.8) → for DL must control for size (traits partly = mass).

## Cut-level features (2026-10-29) — see decisions.md
Split-half reliability (Spearman–Brown, angle-adjusted within drill): WR retain 0.14, v_in 0.42, recover 0.25;
OL v_in 0.41; DL v_in 0.48, v_out 0.41; DB all ≤ 0.22 (retain −0.87). → not usable as traits.
