# Status log (newest first)

- **2026-10-29**
  - Project folder now at `/home/rajm012/Desktop/It's Me/nfl-bdb-2027` (moved by owner). Kaggle launcher fixed (`python -m kaggle`).
  - **All data downloaded** (per-file downloads stalled server-side → new `src/download_zip.sh`). Game tracking = 22.65M frames
    (data page's 8.8M is wrong; verified no duplicates). Parquet in `data/interim/`.
  - Built: `src/cuts.py` (cut detection), `src/game_features.py` (in-game traits, 314k player-plays),
    `src/transfer.py`, `src/outcomes.py`, `src/sprint.py` (40-yd sprint-curve fit), `src/study2.py`.
  - Pre-registration written *before* outcome modelling (`reports/prereg.md`), with dated amendments.
  - **Results (honest):**
    - Transfer Combine→game: DL burst r=0.45 (half is body weight), WR turning r=0.28 (size-independent). OL ≈ 0.
    - **Study 1 (6 tests) and Study 2 (3 tests): all null, tight CIs.** Positive control passes (weight/height/pick do predict
      outcomes), so the pipeline is sound — the tracking traits as defined simply add nothing beyond size, 40 and draft slot.
  - **Decision needed** — the thesis in PLAN.md has failed its own go/no-go. Options:
    - **A (recommended): Route-matched study.** WR Combine route drills share names with NFL routes (slant, curl, comeback,
      speed-out, post-corner, go). Test whether *how a WR runs a given route at the Combine* predicts separation *on that same
      route in games* (and whether turning matters only on sharp-break routes). Host lists this exact idea; highly visual.
      Pre-register one family before looking.
    - **B: "What the Combine can and can't tell you"** — write up the calibrated nulls + the real transfer findings as an
      evidence map for scouts. Strongest on Data Science score, weaker on "actionable new signal" (Football 30%).
    - **C: Usage angle** — Combine movement → how coaches deploy rookies (route tree, alignment). Very reliable outcome
      (target 0.74) but "usage" is weaker than "performance" for the hard gate.
    Plan: proceed with **A**, keeping B as the fallback narrative (all nulls are reportable because pre-registered).

- **2026-10-08 (session 2, cont.)**
  - Combine tracking analysed (`reports/eda.md`). Built `src/kinematics.py` (signed forward/sideways accel from x,y;
    validated r=0.976 vs provided `a`) and `src/combine_features.py` (drill-normalised player traits).
  - **Key result:** turning + burst traits are reliable for WR/OL/DL (0.55–0.65) and cover ~100% of players,
    vs the 3-cone's 35%. Braking alone is too noisy → thesis reframed (see `reports/decisions.md`).
  - DB traits weak with generic features → try phase-specific DB features next.
  - Download still running (player_play, then 3 game-tracking files; ~400 KB/s).
  - **Next:** (1) parquet-convert game data when downloaded; (2) detect cuts/turns in game tracking and compute the
    same traits per player-season (transfer test); (3) inspect `player_play` outcome columns per position (which
    fields are populated for WR/OL/DL/DB); (4) write `reports/prereg.md` before any outcome modelling.


- **2026-10-08 (session 2)**
  - Kaggle token installed at `~/.kaggle/access_token` (it is the new `KGAT_` format, not JSON). API works.
  - Entering the **University track** (owner is a B.Tech Maths & Computing undergrad).
  - Added `CLAUDE.md` (shared project memory) + `AGENTS.md` (pointer for non-Claude agents).
  - Data download running via `src/download_data.sh` (file-by-file with retries; link ~400 KB/s → ~1.5 h total).
  - First EDA on small files → `reports/data_quirks.md`. Headline findings:
    - 3-cone missing for 65% of players, shuttle for 61% → tracking-based agility can fill a real scouting gap.
    - Draft pick vs career snaps: Spearman −0.72 → must use per-play outcomes and condition on draft slot.
    - `games.csv` includes preseason games (undocumented) → REG for outcomes, PRE usable for movement signatures.
  - Next: Combine tracking EDA (drill catalogue, attempts per player, cut detection), parquet conversion.

- **2026-10-08** — Read competition overview, data dictionary and rules. Wrote `PLAN.md`.
  Set up folder + Python env.
