# Status log (newest first)

- **2026-11-09 — Joint work started; audit and starter notebook delivered**
  - Owner takes Python/notebook and design/writeup checks; assistant handles football/statistical
    research and internal review. External researchers unavailable; no independent-expert claim.
    Updated allocation and created `START_HERE.md` and `reports/review_notes.md`.
  - Built/ran `src/audit_data.py --tracking-keys`: zero input-integrity failures including full
    22.65M game-frame keys. Raw/Parquet player-play counts both 314,197. Recorded 2,496/2,466
    unmatched game-trait/player-play rows; explanations pending. Study 3 support remains 25/17/16.
  - Created/executed `notebooks/submission.ipynb` on both CSV and Parquet inputs; saved outputs,
    dependency versions and draft `reports/figures/study3_support.png`. No new outcome associations.
    Preserved three historical numerical reports byte-for-byte in `reports/history/2026-11-09/`.
  - Created/tested standard-library `src/system_info.py`. SSH server reached; non-interactive
    authentication rejected, so remote inventory/specifications are not yet verified. Owner can
    run the inventory through their terminal; authentication setup is next for assistant-run jobs.
    Owner confirms password login; prepared a project-specific local SSH key outside Git and
    documented public-key installation in `START_HERE.md`. No remote authorization change yet.
  - Next: owner reviews/reruns notebook; assistant explains join attrition, reproduces movement
    reliability and continues internal research critique before the frozen measurement screen.
- **2026-11-09 — Professor-provided compute and resource priorities**
  - Owner reports remote RTX 5080 (16 GiB VRAM) and strong CPU access. Updated `PLAN.md` with
    local/remote/Kaggle allocation, remote inventory/benchmark steps and checkpointed CPU validation.
    Connection, system RAM, core count, storage, OS and access duration remain unverified.
  - Added `reports/resource_requests.md` with ranked volunteer help, concrete review outputs,
    time estimates and a professor-ready resource request. Football/statistical reviewers are the
    highest-value additions; notebook reproduction and figure/writeup feedback also prioritised.
  - Retained $0 incremental budget, frozen hypotheses, November 20 research cutoff and public
    CPU/Kaggle reproduction. No remote connection, data transfer, model changes or new analyses performed.

- **2026-11-09 — Submission strategy revised at owner's request**
  - Replaced `PLAN.md` with an executable, $0-incremental-budget plan; original preserved in
    `reports/plan_2026-10-08.md`. Final research/story decision Nov 20; notebook ready Dec 14;
    internal owner submission Dec 28. No new hypothesis families after the research cutoff.
  - Checked support before choosing the experiment: only 7 evaluation WRs have ≥10 SLANT and OUT
    plays separately, and only 3 repeat the Combine slant. Revised to existing TURN × pooled
    SLANT/OUT-versus-GO contrast, rookie-season REG: 42 development + 16 evaluation athletes.
  - Added frozen `reports/study3_protocol.md` and appended it to `reports/prereg.md`; support and
    competition verification in `reports/planning_feasibility.md`. No new outcome associations/refits.
    Prior 2025 outcome exposure is explicitly disclosed; this is not a pristine holdout.
  - Plan requires historical-output preservation, robust inference/scaling audit, reproduced supporting
    results, cohort evaluation, six figures/one table and clean Kaggle reproduction. Evidence-map
    submission remains viable if the bounded experiment fails; no prize or payout is guaranteed.
  - Kaggle CLI confirms entry and Jan 6 23:59 UTC deadline; $100k is the total pool. Public overview/rules
    GET returned 404, so precise track/rules verification remains a final UI task.
  - Next: audit keys/season filters, reproduce TURN reliability and build notebook skeleton before new fits.

- **2026-11-09 — Repository orientation and review**
  - Read all current project notes, source modules and reports; checked local Parquet counts/route labels. Saved assessment in `reports/repo_review.md`. No model refits or new outcome analyses.
  - Confirmed general envelope and first-step studies have no Holm-significant results (9 confirmatory tests). Route-matched WR direction is still proposed, with no preregistration or implementation yet.
  - Identified outstanding validation: draft-class holdout, 3-cone subset analysis, robust binary-outcome SE, explicit directional-test documentation and player-level Study 2 standardisation. Supporting exploratory checks also need saved reproduction code before submission.
  - Route labels are not all exact matches: NFL has SLANT/GO/OUT, but no explicit CURL/COMEBACK/POST_CORNER.
  - Corrected memory: Git now exists (initial commit `4a87acf`, 2026-11-09; `main` → `origin/main`). Writeup and figures remain placeholders; submission notebook is not yet present.

- **2026-10-29**
  - Project folder now at `/home/rajm012/Desktop/It's Me/nfl-bdb-2027` (moved by owner). Kaggle launcher fixed (`python -m kaggle`).
  - **All data downloaded** (per-file downloads stalled server-side → new `src/download_zip.sh`). Game tracking = 22.65M frames (data page's 8.8M is wrong; verified no duplicates). Parquet in `data/interim/`.
  - Built: `src/cuts.py` (cut detection), `src/game_features.py` (in-game traits, 314k player-plays), `src/transfer.py`, `src/outcomes.py`, `src/sprint.py` (40-yd sprint-curve fit), `src/study2.py`.
  - Pre-registration written *before* outcome modelling (`reports/prereg.md`), with dated amendments.
  - **Results (honest):**
    - Transfer Combine→game: DL burst r=0.45 (half is body weight), WR turning r=0.28 (size-independent). OL ≈ 0.
    - **Study 1 (6 tests) and Study 2 (3 tests): all null, tight CIs.** Positive control passes (weight/height/pick do predict outcomes), so the pipeline is sound — the tracking traits as defined simply add nothing beyond size, 40 and draft slot.
  - **Decision needed** — the thesis in PLAN.md has failed its own go/no-go. Options:
    - **A (recommended): Route-matched study.** WR Combine route drills share names with NFL routes (slant, curl, comeback, speed-out, post-corner, go). Test whether *how a WR runs a given route at the Combine* predicts separation *on that same route in games* (and whether turning matters only on sharp-break routes). Host lists this exact idea; highly visual. Pre-register one family before looking.
    - **B: "What the Combine can and can't tell you"** — write up the calibrated nulls + the real transfer findings as an evidence map for scouts. Strongest on Data Science score, weaker on "actionable new signal" (Football 30%).
    - **C: Usage angle** — Combine movement → how coaches deploy rookies (route tree, alignment). Very reliable outcome (target 0.74) but "usage" is weaker than "performance" for the hard gate. Plan: proceed with **A**, keeping B as the fallback narrative (all nulls are reportable because pre-registered).

- **2026-10-08 (session 2, cont.)**
  - Combine tracking analysed (`reports/eda.md`). Built `src/kinematics.py` (signed forward/sideways accel from x,y; validated r=0.976 vs provided `a`) and `src/combine_features.py` (drill-normalised player traits).
  - **Key result:** turning + burst traits are reliable for WR/OL/DL (0.55–0.65) and cover ~100% of players, vs the 3-cone's 35%. Braking alone is too noisy → thesis reframed (see `reports/decisions.md`).
  - DB traits weak with generic features → try phase-specific DB features next.
  - Download still running (player_play, then 3 game-tracking files; ~400 KB/s).
  - **Next:** (1) parquet-convert game data when downloaded; (2) detect cuts/turns in game tracking and compute the same traits per player-season (transfer test); (3) inspect `player_play` outcome columns per position (which fields are populated for WR/OL/DL/DB); (4) write `reports/prereg.md` before any outcome modelling.


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

- **2026-10-08** — Read competition overview, data dictionary and rules. Wrote `PLAN.md`. Set up folder + Python env.
