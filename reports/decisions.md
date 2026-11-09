# Decision log

- **2026-10-08 — Metric reframed from "Brake-Burst" to acceleration envelope (turning + burst).**
  Evidence: braking alone has low reliability (0.0–0.38); turning (lat) and burst are 0.55–0.65 for WR/OL/DL.
  Lateral accel dominates agility drills. Working name: **"Cornering"/acceleration-envelope traits**; final name TBD.
- **2026-10-08 — Traits are drill-normalised** (z within drill, averaged over drills). Pooled frames failed reliability.
- **2026-10-08 — DB deprioritised for now**: generic traits unreliable (lat 0.25, burst 0.11). Revisit with
  phase-specific DB features (backpedal → plant → drive) before dropping.
- Current front-runners for primary thesis: **WR** (lat/burst reliable, ~independent of 3-cone) and **OL/DL**
  (reliable; DL needs size control). Choose after game-side transfer test (target: go/no-go by 2026-11-02).
- Entering **University track**.
- **2026-10-29 — Per-cut features rejected as player traits.** `src/cuts.py` detects cuts sensibly (shuttle ≈176°,
  3-cone ≈165°, curl ≈105°, slant/out ≈50°), but angle-adjusted, drill-normalised cut features have low split-half
  reliability (Spearman–Brown ≤ 0.48; most < 0.3; DB retain negative). Keep `cuts.py` for *game-side descriptive*
  use only. Frame-quantile traits (lat, burst) remain the measurement.
- **2026-10-29 — DB dropped as primary group.** No reliable DB agility trait (only vmax 0.72). Primary candidates:
  **WR** and **OL/DL** — decide at go/no-go after the game-side transfer test.
- **2026-10-29 — Study 1 (envelope traits) NO-GO.** All 6 pre-registered tests null with tight CIs
  (reports/confirmatory.md). Transfer: DL burst r=0.45 (0.21 net of weight), WR turning r=0.28 (robust to weight/role/40).
- **2026-10-29 — Study 2 (start-of-40 acceleration A0) null.** F1–F3 all null (reports/study2.md). A0 test-retest only 0.40.
- **2026-10-29 — Pipeline validated by positive control:** baseline covariates do predict outcomes (DL weight → slower
  get-off z=4.6; OL height/pick → pressure z=3.0/2.3; WR weight → less separation z=−2.7). Nulls are real, not bugs.
- **2026-10-29 — Exploratory:** tracking traits are barely priced into draft slot (|ρ| ≤ 0.22); preseason in-game movement
  only weakly predicts REG separation (WR turning z=1.7). Outcome reliability: DL get-off 0.80, OL peak pressure prob 0.80,
  WR target 0.74, WR separation 0.57, WR YACOE 0.14 (unusable).
- **OPEN DECISION (needs a direction before more modelling):** see STATUS.md "Decision needed".

- **2026-11-09 — Direction chosen; replaces the open decision above.** Build a scouting evidence
  map and allow one bounded route-context follow-up to strengthen its central finding. Existing
  TURN × SLANT/OUT-versus-GO contrast uses rookie-season REG and conventional-measurable/context
  adjustment. This differs from a drill-specific route-talent score: slant has only 3 repeated
  athletes and exact separate SLANT/OUT evaluation support is only 7 athletes. Pooled family
  support is 42 development + 16 evaluation athletes before final checks.
- **2026-11-09 — Execution constraints.** Incremental cash budget $0; audit and notebook begin
  first; research/story freeze Nov 20. Retain all nulls and report prior 2025 exposure. No new
  hypothesis families after the cutoff. Frozen details in `reports/study3_protocol.md`;
  revised full strategy in `PLAN.md`, original archived in `reports/plan_2026-10-08.md`.
