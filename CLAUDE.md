# Project memory — NFL Big Data Bowl 2027 (read this first, every session)

This file is the shared memory for any agent working in this folder. Keep it current: when you learn a durable fact (data quirk, decision, file location), update the relevant section here and add a dated line to `STATUS.md`. Keep this file short — details go in `reports/`.

## Who / what
- Owner: Kaggle user `rajm012` (B.Tech Maths & Computing, undergrad → **University track**).
- Owner handles Python/notebook checks and design/writeup review (confirmed 2026-11-09). Assistant drives football/statistical research and analysis; external expert reviewers are unavailable. Ask owner for account authentication, legal/terms acceptance, team changes and final Kaggle Submit.
- Competition: https://www.kaggle.com/competitions/nfl-big-data-bowl-2027 — judged analytics hackathon. Link 10 Hz **Combine tracking** → **regular-season NFL performance**.
- Deliverable: Kaggle Writeup ≤ 2,000 words, < 10 figures+tables, with a **public Kaggle notebook** attached. Scoring: Football 30 · Data Science 30 · Writeup 20 · Data Viz 20. One submission per team.
- **Hard deadline 2027-01-06 23:59 UTC. Internal deadline 2026-12-28.**

## Where things are
| Path | What |
|---|---|
| `PLAN.md` | Strategy, thesis, stats design, figure plan, timeline. Source of truth for *what* we do. |
| `reports/study3_protocol.md` | Frozen 2026-11-09 route-family follow-up protocol; feasibility counts in `reports/planning_feasibility.md`. |
| `STATUS.md` | Dated progress log, newest first. Read the top before starting; append when you stop. |
| `CLAUDE.md` | This file: durable facts + conventions. `AGENTS.md` points here. |
| `data/raw/` | Original CSVs from Kaggle (git-ignored, never edit). |
| `data/interim/` | Parquet conversions + derived tables (git-ignored, reproducible from `src/`). |
| `src/` | Reusable pipeline code (`python -m src.<module>` from project root). |
| `notebooks/` | Exploration notebooks; final Kaggle notebook is `notebooks/submission.ipynb` (later). |
| `reports/` | Markdown findings: `eda.md`, `data_quirks.md`, `prereg.md`, `decisions.md`; figures in `reports/figures/`. |
| `reports/repo_review.md` | 2026-11-09 code/data review: implemented scope, validation gaps, route-mapping constraints. |
| `reports/latest_runs.md` | Current local-run results, artifacts and exact next work; updated 2026-11-10. |
| `reports/validation_findings.md` | Nov 10 cohort/cone interpretation; full tables in `validation.*` and `cone_sensitivity.*`. |
| `writeup/` | Writeup drafts (`writeup.md`). |

## Environment
- Project root: `/home/rajm012/Desktop/It's Me/nfl-bdb-2027` (Git initial commit 2026-11-09; `main` tracks `origin/main`).
- Python venv: `.venv/` → always use `.venv/bin/python`; call Kaggle as `.venv/bin/python -m kaggle` (the `.venv/bin/kaggle` launcher broke when the folder moved). Packages: polars, duckdb, pandas, statsmodels, pymc, bambi, arviz, lightgbm, scikit-learn, matplotlib, seaborn, plotnine, jupyter.
- Kaggle auth: new-style token at `~/.kaggle/access_token` (Kaggle CLI 2.x). Never print or copy it.
- Machine: 16 GB RAM (often only ~5 GB free), RTX 4050 6 GB. **Never load all game tracking into pandas.** Use parquet + DuckDB/Polars lazy scans, filter columns/rows early.
- Remote resource reported by owner 2026-11-09: professor-provided **RTX 5080, 16 GiB VRAM**, strong CPU. Owner confirms full SSH access. Target supplied Nov 9: `gpu2@192.168.0.104`; SSH times out from this workspace's `172.16.1.x` network. `ssh-copy-id` printed a Windows `exec` error before claiming a key was added, so installation is **unverified**. Dedicated key `~/.ssh/nfl_bdb_2027_ed25519` remains outside the repo. Owner explicitly requested **local execution** after connection trouble. Host RAM/cores/OS/storage/access window remain unverified. Current pipeline is mainly CPU-bound; use remote CPU for planned validation/refits first and preserve CPU/Kaggle reproduction. No extra cash budget.
- Data licence CC BY-NC 4.0: do not commit or upload raw data anywhere except Kaggle.

## Current strategy (details: STATUS.md top entry, reports/decisions.md)
- **Stage as of Nov 10:** requested cohort/cone validation block complete; ready for submission production. Retain the Nov 20 claim-review checkpoint; full raw-input notebook, final figures, writeup and Kaggle/publication checks remain.
- **2026-11-09: PLAN.md rewritten; incremental cash budget $0.** Original plan archived in `reports/plan_2026-10-08.md`.
- Studies 1–2 audited Nov 9: all 15 fits converge; **0/9 two-sided Holm-significant** original-family associations and **0/3** player-clustered binary LPM sensitivities. `src/validation.py` saves separate reports/checkpoints, actual fitted samples and player-table Study 2 SDs. Expected signs were preregistered but one-sided tests were not explicit; conservative two-sided audit is a disclosed correction.
- **Study 3 measurement gate FAILED Nov 9.** Support after checks: 42 development + 16 evaluation WRs; 41 support alternating-game halves. Adjusted contrast SB=0.296 (interval −0.257 to 0.606), below frozen 0.40 gate; raw SB=0.463. `src/route_context.py` fits only the conventional baseline. **No TURN interaction or 2025 performance evaluation fitted. Stop the primary route-performance claim**; proceed with the evidence-map narrative without changing eligibility/route groups to seek a result. Full protocol remains frozen; only 3 slant repeats, no slant-specific talent score.
- **November 20: final narrative decision; no new hypothesis families afterward.** Primary product is a scouting evidence map separating measurement, transfer and added prediction. Promote a signal only if validated.
- Cohort prediction and cone checks completed Nov 10: `src/evaluate.py --stage develop/evaluate` freezes 25 model pairs before evaluation (9 primary, 7 original secondaries, 9 cone sensitivities). Primary rookie-REG evaluation has 20–37 2025 athletes/test; **0/9 marginal intervals support RMSE improvement**, all original-family simultaneous intervals include zero. No evaluation player effects. Prior 2025 exposure disclosed; paired-bootstrap intervals condition on training. Three development models required recorded Powell retries for numerical diagnostics.
- `src/cone_sensitivity.py` completes nine same-row historical all-REG checks (23–43 athletes). Interesting secondary exceptions are retained: DL TURN/pressure association remains positive but cone-subset cohort prediction is uncertain; DL A0 cone cohort gain=0.00755 s [0.00443,0.01080] on only 9 athletes. No cone imputation, universal scouting claim or new hypothesis selection. Final claim/notebook integration remains. Binary robust sensitivity, player-level Study 2 SDs, reliability and adjusted transfer now have saved code. Historical reports are preserved byte-for-byte. Public notebook ready Dec 14, owner submission by Dec 28. Notebook reproduces the frozen conventional measurement screen from four raw CSVs or Parquets with embedded helper source and identical results. Cohort results are an explicitly labelled embedded review snapshot, **not raw-input evaluation rebuilding**; full submission rebuilding remains pending. Draft figures: support, measurement, transfer, exposure-only route trace, `cohort_prediction.png`; `reports/evaluation_table.csv` contains all nine primary comparisons.
- Kaggle CLI verified deadline, entry and $100k total pool on Nov 9. Individual track awards/rules require final UI check.
- Resource priorities and professor/friend requests: `reports/resource_requests.md`; football/statistical review, reliable remote access, independent notebook reproduction and visual/writing feedback precede more hardware.
- Start/handoff: `START_HERE.md`; internal critique in `reports/review_notes.md` is not independent expert validation.
- `python -m src.audit_data --tracking-keys` passes key/count checks; raw player-play CSV=Parquet=314,197. `src/join_audit.py` explains all 2,466 missing trait rows: 1,750 absent tracking keys, 715 no snap, 1 short track. All 2,496 trait rows without player-play exist in supplied tracking; provider omission reasons unknown. Study 3 needs no game-trait join; only 3/5,389 candidate rows lack it. Old numerical reports preserved in `reports/history/2026-11-09/`. `src/system_info.py` runs remotely via stdin.
- `src/reliability.py` reproduces WR cross-drill TURN SB=0.546; training-reference development SB=0.593 (70 WRs; interval 0.373–0.737). `src/transfer_audit.py` reproduces historical correlations and excludes POST for corrected PRE+REG scope: WR TURN r=0.279 (n=98); DL BURST r=0.443, weight-adjusted 0.203 (n=115). These are descriptive movement transfer, not held-out performance prediction. Athlete bootstraps refit adjustment.

## Pipeline (run from project root, in order)
1. `bash src/download_data.sh` → `data/raw/*.csv` (resumable, per file).
2. `.venv/bin/python -m src.to_parquet` → `data/interim/*.parquet` (game tracking merged once all 3 seasons present).
3. `.venv/bin/python -m src.combine_features` → `combine_frames`, `combine_attempts`, `combine_traits` parquet.
4. `-m src.game_features` (~6 min) → `game_play_traits`; `-m src.transfer` → reports/transfer.md.
5. `-m src.outcomes` (Study 1) → reports/confirmatory.md; `-m src.sprint` then `-m src.study2` → reports/study2.md. MixedLM: use default `.fit()` (lbfgs alone silently fails); drop constant indicator columns (singular matrix). Kinematics (signed a_lon / a_lat from x,y) live in `src/kinematics.py` — reuse for game tracking.

Audited path (existing inputs): `-m src.join_audit`, `-m src.reliability`, `-m src.route_context`, `-m src.validation`, `-m src.transfer_audit`, `-m src.audit_figures`. Use bounded threads locally:
`OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 POLARS_MAX_THREADS=2`. Rebuild notebook screen source with
`-m src.build_measurement_notebook` after editing shared helpers; execute notebook afterward.
Prediction: `-m src.evaluate --stage develop` then `--stage evaluate` (refuses changed frozen source, protocol or inputs); `-m src.cone_sensitivity`; `-m src.evaluation_figures`. Protocol is frozen in
`reports/evaluation_protocol.md`; do not edit it or prediction source after evaluation to tune results. Meaningful invariants: `.venv/bin/python -m unittest discover -s tests -v` (11 passed Nov 10).

## Rules of the road (statistical hygiene)
- Write hypotheses/features into `reports/prereg.md` **before** fitting outcome models; don't silently change them.
- Control for draft capital and opportunity; prefer per-play/per-snap outcomes with player random effects.
- Develop on 2023–24 classes; reserve 2025 from further follow-up development. Prior studies already used 2025 outcomes, so disclose exposure and never claim a pristine untouched holdout. Scale/impute on training players.
- Report effect sizes with intervals; label exploratory analyses as such.

## Data facts (verified — add as you learn)
- 9 CSVs, ~2.2 GB. Keys: `nfl_id` (player), `event_id` (combine drill attempt), `game_id`+`play_id` (play).
- Game tracking contains **only the 510 rookie-cohort players**, not teammates/opponents/ball. → No opponent geometry; defender/receiver interaction outcomes must come from `player_play.csv`.
- `combine_tracking.csv` includes BALL rows (`entity_type == 'BALL'`, `nfl_id` null) — filter them out.
- Draft fields null for UDFAs (127/510).
- CSV nulls are the string `NA`. `a` is **unsigned** total-accel magnitude → use `src/kinematics.py`.
- `games.csv` includes **preseason** (PRE) games: outcomes must be REG only; PRE ok for movement signatures.
- Draft pick vs career snaps Spearman −0.72 → never use raw career volume as the outcome.
- NFL `route_ran` has SLANT/GO/OUT but no explicit CURL/COMEBACK/POST_CORNER labels; predeclare any approximate Combine→NFL route mapping. `transfer.py` currently pools games/seasons per player.
- _(more in `reports/data_quirks.md`; findings in `reports/eda.md`)_

## Conventions
- Small, readable scripts in `src/`; each writes outputs to `data/interim/` or `reports/`.
- Figures: colour-blind-safe palette, direct labels, saved as PNG (200 dpi) to `reports/figures/`.
- Git: existing repository on `main`, tracking `origin/main` (verified 2026-11-09); don't push without authorization.
