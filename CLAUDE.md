# Project memory — NFL Big Data Bowl 2027 (read this first, every session)

This file is the shared memory for any agent working in this folder. Keep it current:
when you learn a durable fact (data quirk, decision, file location), update the relevant section here
and add a dated line to `STATUS.md`. Keep this file short — details go in `reports/`.

## Who / what
- Owner: Kaggle user `rajm012` (B.Tech Maths & Computing, undergrad → **University track**).
- Owner is ill and rarely available. **Agents drive the work autonomously.** Only ask the owner for
  things only they can do: clicking Submit on the Kaggle Writeup, legal/terms acceptance, team changes.
- Competition: https://www.kaggle.com/competitions/nfl-big-data-bowl-2027 — judged analytics hackathon.
  Link 10 Hz **Combine tracking** → **regular-season NFL performance**.
- Deliverable: Kaggle Writeup ≤ 2,000 words, < 10 figures+tables, with a **public Kaggle notebook** attached.
  Scoring: Football 30 · Data Science 30 · Writeup 20 · Data Viz 20. One submission per team.
- **Hard deadline 2027-01-06 23:59 UTC. Internal deadline 2026-12-28.**

## Where things are
| Path | What |
|---|---|
| `PLAN.md` | Strategy, thesis, stats design, figure plan, timeline. Source of truth for *what* we do. |
| `STATUS.md` | Dated progress log, newest first. Read the top before starting; append when you stop. |
| `CLAUDE.md` | This file: durable facts + conventions. `AGENTS.md` points here. |
| `data/raw/` | Original CSVs from Kaggle (git-ignored, never edit). |
| `data/interim/` | Parquet conversions + derived tables (git-ignored, reproducible from `src/`). |
| `src/` | Reusable pipeline code (`python -m src.<module>` from project root). |
| `notebooks/` | Exploration notebooks; final Kaggle notebook is `notebooks/submission.ipynb` (later). |
| `reports/` | Markdown findings: `eda.md`, `data_quirks.md`, `prereg.md`, `decisions.md`; figures in `reports/figures/`. |
| `writeup/` | Writeup drafts (`writeup.md`). |

## Environment
- Project root: `/home/rajm012/Desktop/It's Me/nfl-bdb-2027` (moved 2026-10-09; **not a git repo**).
- Python venv: `.venv/` → always use `.venv/bin/python`; call Kaggle as `.venv/bin/python -m kaggle`
  (the `.venv/bin/kaggle` launcher broke when the folder moved). Packages: polars, duckdb,
  pandas, statsmodels, pymc, bambi, arviz, lightgbm, scikit-learn, matplotlib, seaborn, plotnine, jupyter.
- Kaggle auth: new-style token at `~/.kaggle/access_token` (Kaggle CLI 2.x). Never print or copy it.
- Machine: 16 GB RAM (often only ~5 GB free), RTX 4050 6 GB. **Never load all game tracking into pandas.**
  Use parquet + DuckDB/Polars lazy scans, filter columns/rows early.
- Data licence CC BY-NC 4.0: do not commit or upload raw data anywhere except Kaggle.

## Current strategy (details: STATUS.md top entry, reports/decisions.md)
- **2026-10-29: original thesis failed its pre-registered go/no-go.** Envelope traits (turning/burst) and start-of-40
  acceleration do not predict NFL per-play outcomes beyond size/40/draft slot (9/9 tests null, positive control passes).
- Real positive findings so far: Combine→game *transfer* (WR turning r=0.28 size-independent; DL burst r=0.45, half weight);
  tracking traits are not priced into the draft.
- **Next direction (recommended, not yet pre-registered): route-matched WR study (Option A in STATUS.md).** Fallback: write
  the calibrated-null evidence map (Option B). Always pre-register in `reports/prereg.md` BEFORE touching outcomes.

## Pipeline (run from project root, in order)
1. `bash src/download_data.sh` → `data/raw/*.csv` (resumable, per file).
2. `.venv/bin/python -m src.to_parquet` → `data/interim/*.parquet` (game tracking merged once all 3 seasons present).
3. `.venv/bin/python -m src.combine_features` → `combine_frames`, `combine_attempts`, `combine_traits` parquet.
4. `-m src.game_features` (~6 min) → `game_play_traits`; `-m src.transfer` → reports/transfer.md.
5. `-m src.outcomes` (Study 1) → reports/confirmatory.md; `-m src.sprint` then `-m src.study2` → reports/study2.md.
   MixedLM: use default `.fit()` (lbfgs alone silently fails); drop constant indicator columns (singular matrix).
   Kinematics (signed a_lon / a_lat from x,y) live in `src/kinematics.py` — reuse for game tracking.

## Rules of the road (statistical hygiene)
- Write hypotheses/features into `reports/prereg.md` **before** fitting outcome models; don't silently change them.
- Control for draft capital and opportunity; prefer per-play/per-snap outcomes with player random effects.
- Holdout: fit on 2023–24 draft classes, validate on 2025 class.
- Report effect sizes with intervals; label exploratory analyses as such.

## Data facts (verified — add as you learn)
- 9 CSVs, ~2.2 GB. Keys: `nfl_id` (player), `event_id` (combine drill attempt), `game_id`+`play_id` (play).
- Game tracking contains **only the 510 rookie-cohort players**, not teammates/opponents/ball.
  → No opponent geometry; defender/receiver interaction outcomes must come from `player_play.csv`.
- `combine_tracking.csv` includes BALL rows (`entity_type == 'BALL'`, `nfl_id` null) — filter them out.
- Draft fields null for UDFAs (127/510).
- CSV nulls are the string `NA`. `a` is **unsigned** total-accel magnitude → use `src/kinematics.py`.
- `games.csv` includes **preseason** (PRE) games: outcomes must be REG only; PRE ok for movement signatures.
- Draft pick vs career snaps Spearman −0.72 → never use raw career volume as the outcome.
- _(more in `reports/data_quirks.md`; findings in `reports/eda.md`)_

## Conventions
- Small, readable scripts in `src/`; each writes outputs to `data/interim/` or `reports/`.
- Figures: colour-blind-safe palette, direct labels, saved as PNG (200 dpi) to `reports/figures/`.
- Git: project is currently not under version control; don't init/push without the owner's say-so.
