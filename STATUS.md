# Status log (newest first)

- **2026-11-10 — Kaggle reproduction and notebook publication completed**
  - Private full Kaggle rebuild COMPLETE: 1,421.62 s, largest sampled stage RSS 1,021.4 MiB; all 402 numeric checks, 25 scores and 12 tests pass. Downloaded execution/verification records saved in `kaggle_*` reports. All 146 output files checked: no raw CSVs or intermediate Parquets redistributed.
  - Published under owner-confirmed `oppenheimer6th`: code notebook ID 144187820, public version 3. Publication is a QUICK_SAVE of unchanged tested source and saved outputs; full execution was version 1. API retrieval confirms public flag, matching code, 59 output blocks and six figures. Inline previews reduced to 950px/128 colours for Kaggle's 1 MB source limit; full 200dpi assets retained.
  - Manuscript/standalone HTML/ZIP regenerated with live notebook citation and current asset hashes: 1,900 conservative words, six figures + one table. Final handoff: `reports/submission_handoff.md`; evidence: `kaggle_execution.json`.
  - Owner Writeup upload/attachment/rendering, track/terms confirmation and Submit remain. Anonymous direct HTTP checks returned 404 from this workspace; API confirms public/source access, while owner browser verification remains pending. No final competition submission, legal acceptance, team change or Git push.

- **2026-11-10 — Local submission production completed; Kaggle run in progress**
  - Complete standalone notebook rebuilt from all nine raw CSVs in a fresh directory: 523.08 s, largest sampled stage RSS 1,183 MiB. All 402 numeric comparisons, 25 cohort scores and 12 tests pass; saved notebook has 59 outputs and no error cells.
  - Batched whole-game extraction preserves all 314,227 keyed game-trait values exactly. A historical W2+cone solver-path discrepancy was diagnosed and resolved by replaying its originally recorded Powell retry. No frozen prediction specification/source or sample changed, no cached coefficients, no widened verification tolerance.
  - Six final figures, nine-row evaluation table, 1,900-word conservative manuscript, offline HTML preview, ZIP and owner handoff prepared. API-retrieved rules, data definitions, deadline, undergraduate track and prize allocation verified.
  - Private Kaggle version 1 launched. Owner confirmed **oppenheimer6th** (earlier memory
    said rajm012); canonical metadata corrected. Worker logs show dependencies and raw
    conversion pass; tracking extraction still running. Publication awaits platform
    result verification; owner final Writeup attachment/rendering/Submit remain.
  - No new hypothesis family, route interaction, remote GPU job, Git commit or Git push.

- **2026-11-10 — Repository-position review after validation**
  - Read current memory/plan, latest results, verification artifacts, submission checklist,
    notebook sections and pipeline module inventory. No analysis or tests rerun.
  - Confirmed submission-production stage: cohort/cone validation is complete; notebook
    execution records explicitly show evaluation rebuilding is still absent. Five draft
    figure PNGs and the nine-comparison evaluation CSV exist. `writeup/` contains only
    `.gitkeep`; no writeup draft or Kaggle kernel metadata file exists yet.
  - Next: complete portable raw-input reproduction, select final figures/evidence card
    around the measurement/transfer/prediction findings, draft the writeup, and perform
    owner review plus clean Kaggle execution. Keep Nov 20 claim review, Dec 14 notebook
    readiness and Dec 28 internal submission. Remote access remains optional/deferred.

- **2026-11-10 — Cohort prediction and 3-cone validation completed locally**
  - Froze implementation details before fitting in `reports/evaluation_protocol.md`, appended
    disclosure to prereg. Rookie-season REG prediction, 2023–24 training and 2025 evaluation;
    historical association sensitivity keeps its all-REG window. Prior 2025 exposure disclosed.
  - Built `src/evaluate.py` with separate develop/evaluate stages, training-only drill/player
    preprocessing, frozen context/year encoding, fixed-only predictions and hash enforcement.
    All 25 model pairs freeze before scoring: 9 primary, 7 prespecified joint/no-10-yard
    secondaries, 9 cone subsets. Three development fits required Powell retries under a
    recorded numerical rule; coefficients and uncertainty pass finite/positive checks.
  - **No primary prediction addition has a supported gain:** all 9 marginal gain intervals
    fail to support improvement; all 6/3-family simultaneous intervals include zero. Primary
    evaluation n=20–37 athletes. Three point gains positive, six negative; no equivalence claim.
    DL BURST get-off deteriorates nominally; the family/≥30-play sensitivities remain uncertain.
  - `src/cone_sensitivity.py` completes nine four-model same-row historical comparisons,
    with 23–43 athletes and no fabricated cone times. Secondary DL TURN/pressure association
    remains positive but cone cohort prediction is uncertain; DL A0 cone cohort improves on
    just nine evaluation athletes. Retained all favourable/adverse subset results separately.
  - Saved `validation.*`, `cone_sensitivity.*`, frozen model metadata, player-score Parquet,
    primary `evaluation_table.csv`, `figures/cohort_prediction.png`, run logs and interpretation
    in `validation_findings.md`. Evidence-map narrative retained; Study 3 remains stopped.
  - 11 statistical tests pass. Independent artifact checks recompute all 25 player-weighted
    scores, verify disjoint cohorts, frozen hashes, common-context identities, finite model
    uncertainty and unchanged historical reports. Notebook CSV/Parquet reruns pass (4.95/3.20 s):
    conventional screen rebuild plus an explicitly labelled cohort-result review snapshot.
    Full evaluation/feature rebuilding in the public notebook remains pending.
  - **Next stage: submission production** — complete raw-input notebook integration, final
    evidence-card/figure selection and writeup draft; Nov 20 claim checkpoint and Dec deadlines
    retained. No new hypotheses, remote work or publication actions in this block.

- **2026-11-10 — Plan-position review (no new analysis runs)**
  - Current phase: late audit / early final validation, covering the Nov 10–16 milestones.
    Data/model audits, reliability, the frozen measurement screen and draft notebook/figures
    were completed early. Studies 1–2 cohort prediction and 3-cone sensitivity remain the
    next required work before the Nov 20 final-claim decision. Full writeup, final visuals,
    complete Kaggle reproduction and publication/submission are still pending.

- **2026-11-09 — Local validation runs completed; route-performance measurement gate failed**
  - Owner supplied `gpu2@192.168.0.104`; SSH times out from current network. Their key-copy output
    contains a Windows `exec` error, so key installation is unverified. Owner requested local work;
    no remote data staging/jobs, resource inventory or authentication changes performed.
  - Implemented/ran `src/join_audit.py`: all 2,466 absent movement rows explained (1,750 tracking
    keys missing, 715 snap events missing, 1 track too short). All 2,496 movement-only keys exist
    in supplied tracking; provider context omission remains unknown.
  - `src/reliability.py` reproduces historical WR TURN SB=0.546. Training-only reference gives
    development SB=0.593, 95% bootstrap interval [0.373,0.737], 70 athletes. Metadata and repeat/QC
    tables saved; no outcome-based trace/feature selection.
  - **Frozen Study 3 gate fails:** 42 development + 16 evaluation eligible WRs; 41 diagnostic WRs.
    Raw contrast SB=0.463; baseline-adjusted SB=0.296 [−0.257,0.606], below 0.40. Conventional
    baseline fits 3,971 development plays, rank 65. No TURN interaction or new 2025 performance
    evaluation. Stop primary route-performance claim and follow planned evidence-map path.
  - `src/validation.py`: all 15 LMM/cluster-sensitivity fits converge; no two-sided Holm-significant
    result among 9 original-family tests or 3 player-clustered binary LPM sensitivities. Corrected
    Study 2 scaling on unique players; recorded exact samples, rank, boundary warnings, control
    estimates and model checkpoints. One-sided-test ambiguity documented conservatively.
  - `src/transfer_audit.py`: historical findings reproduced; corrected PRE+REG WR TURN r=0.279
    (n=98), DL BURST r=0.443, weight-adjusted r=0.203 (n=115). Saved athlete-bootstrap intervals
    and pooled/player-season traits with explicit POST exclusion; REG-only sensitivity separate.
  - Notebook now independently reproduces measurement screen from four competition tables;
    clean-kernel Parquet/CSV runs take 4.45/6.10 s and match all screen statistics. Added measurement,
    audited-transfer and actual route-trace draft figures; trace pair chosen only from exposures.
    Five statistical-invariant tests pass. Historical reports verified byte-for-byte unchanged.
  - Current run summary: `reports/latest_runs.md`. Next: held-out Studies 1–2 prediction, same-sample
    3-cone sensitivity, complete notebook rebuilding/integration and evidence-map writing. No new
    route-family primary fit or hypothesis family after the failed screen.

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
