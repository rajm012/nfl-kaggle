# Repository review — 2026-11-09
Scope: read the project notes, all current `src/` modules and reports; inspect Git state, Parquet row counts and route labels. No models were refitted and no new outcome relationships were examined. Existing numerical findings below are reported results, not independently rerun results.

## What the project is doing
University-track NFL Big Data Bowl 2027 entry: identify a football-relevant signal in 10 Hz Combine tracking that adds information about regular-season performance beyond traditional measurables and draft capital. The intended evidence chain is Combine movement → comparable game movement → performance. Submission requires a short writeup and public Kaggle notebook.

The implemented pipeline converts CSVs to Parquet, derives signed longitudinal and lateral acceleration from smoothed positions, aggregates drill-normalised Combine traits, measures game traits during the first three seconds after the snap, and fits play-level models with player random intercepts. A second study fits 40-yard speed curves to estimate initial acceleration.

## What is established in the current reports
- Braking/cut features were insufficiently reliable as general player traits; turning and burst were retained for WR/OL/DL. DB was dropped as a primary group.
- Some movement traits transfer: WR turning r = 0.28; DL burst r = 0.45. Notes report that the DL association attenuates to 0.21 after controlling for weight.
- None of the six Study 1 or three Study 2 confirmatory tests survives its family's Holm correction. D2 has an unadjusted directional p = 0.039 but adjusted p = 0.234.
- These results support the documented no-go for the tested general traits. They do not establish that all possible Combine tracking features lack value, or that a model can predict unseen players.

## Implementation and validation gaps
1. **Held-out prediction is planned but absent from current scripts/reports.** Neither outcome module splits by draft class or compares held-out baseline versus augmented predictions. Neither implements the pre-specified 3-cone subset analysis. Do not describe 
these checks as complete.

2. **Binary-outcome uncertainty differs from preregistration.** Study 1 uses a linear mixed model for binary outcomes, with model-based standard errors. The preregistration's linear-probability fallback specifies robust standard errors. Resolve or explicitly document this deviation before relying on those intervals as final evidence.

3. **Directional testing needs documentation.** Both outcome modules calculate one-sided p-values; expected signs were predeclared, but the preregistration does not explicitly specify one-sided tests.

4. **Study 2 standardisation weights players by opportunity.** A0 and the 10-yard split are standardised after joining to player-play rows, unlike Study 1's player-table standardisation. Thus one SD in the Study 2 table is a play-weighted SD. Standardise on 
unique players if the intended interpretation is an SD across athletes.

5. **Supporting checks need reproducible artifacts.** Positive-control, weight-adjusted transfer, Combine reliability and outcome reliability numbers appear in notes, but the current scripts do not regenerate dedicated reports for all these checks. Existing `combine_cuts` and `combine_cut_traits` Parquets also lack a saved generator in `src/`.

6. **Player-level exposure limits the independent sample.** Thousands of plays improve estimation of each player's performance; they do not create thousands of independent athletes for testing a single Combine trait. Outcome-model samples are roughly 73–98 players per group.

Positive controls are useful diagnostic evidence, but do not by themselves prove the whole pipeline correct. Conditioning on draft pick and using per-play outcomes address some opportunity confounding; selection into playing time and unmeasured context remain limitations.

## Next study feasibility
The recommended route-matched WR study is proposed, not implemented or pre-registered. Schema inspection confirms Combine `SLANT_ROUTE_LEFT` and `GO_ROUTE_RIGHT` versus NFL `SLANT` and `GO`, and Combine speed-out drills versus NFL `OUT`. NFL labels are: ANGLE, CORNER, CROSS, FLAT, GO, HITCH, IN, OUT, POST, SCREEN, SLANT, WHEEL (plus null). There is no explicit NFL CURL, COMEBACK or POST_CORNER category. Treat any broader mapping as a football assumption that needs a predeclared rationale; matching names alone does not ensure equivalent movement. Choose the mapping, feature and primary test before examining route-specific performance associations. Since earlier studies already used separation outcomes, document this as a subsequent study informed by prior analyses rather than a completely untouched outcome.

## Current artifacts and state
- Verified 510 players; 22,654,290 game frames; 314,197 player-play rows; 314,227 derived game-trait rows; 484 pooled game-trait players; 418 sprint-trait players.
- `transfer.py` pools eligible games/seasons per player. It does not save a player-season trait table or explicitly restrict season type, despite the preregistration's REG + PRE wording.
- `writeup/` and `reports/figures/` contain placeholders; `notebooks/` does not exist yet.
- Git now exists: initial commit `4a87acf` dated 2026-11-09, branch `main` tracking `origin/main`. The working tree was clean before this documentation review.
- `PLAN.md` still presents the original thesis and outdated 8.8M game-frame estimate; use the later status/decision entries to understand the pivot until the strategy document is revised.
