# Data quirks log (append as discovered)

- **Nulls are the literal string `NA`** in CSVs → read with `null_values=["NA",""]` (polars) / `nullstr='NA'` (duckdb).
- `combine_results`: opt-outs are common — 3-cone missing 330/510 (65%), short shuttle 309 (61%),
  bench 318, forty 86, ten_yd_split 85, vertical 72, broad 87. NGS production/final score missing for 1.
- `players`: 127/510 UDFAs (draft_round null). Classes: 2023=160, 2024=177, 2025=173.
- `combine_position` counts: DB 122, OL 121, DL 118, WR 107, TE 42.
- `games.csv` contains **PRE (preseason, 49/season)**, REG (272) and POST (13) — docs only mention REG/POST.
  → Outcomes for the writeup must be **REG only** (hard gate is "regular-season performance").
  → PRE frames are still useful for measuring a player's *in-game movement signature* (UDFAs play there).
- **Opportunity ≈ draft capital:** Spearman(draft_overall_pick, career off+def snaps) = −0.72.
  UDFAs: 55–66% have zero career snaps; R1–2: 0%. Career-volume outcomes mostly measure the pick → use
  per-play efficiency outcomes and condition on draft slot.
- **Game tracking is 22,654,290 frames** (2023: 3.67M, 2024: 7.83M, 2025: 11.16M), not the 8.8M on the data page.
  Verified: CSV line counts match, zero duplicate (game, play, nfl_id, time) keys → the docs are wrong, data is fine.
  Players tracked per season: 156 / 318 / 448 (cohort grows as classes enter). ~69 frames (6.9 s) per player-play.
- **2026-11-09 audit:** downloaded `player_play.csv` and Parquet both contain 314,197 rows;
  the data-page 316,338 count differs from the source file, not from conversion (counts checked;
  not a cell-by-cell equality proof). Full game-frame key scan again found zero null/duplicate keys.
- **2026-11-09 join attrition:** 2,496 `game_play_traits` rows lack a `player_play` row; 2,466
  `player_play` rows lack a trait row. Main keys/references are valid; causes remain to be explained
  before reporting transfer/outcome join coverage. See `reports/audit.md`.
- Per-file Kaggle downloads of the big CSVs stall server-side; use `src/download_zip.sh` (download-all zip + curl resume).
