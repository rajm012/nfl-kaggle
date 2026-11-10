# Production review — 2026-11-10

This is an internal football/statistical/code review, not independent expert review.

## Completed artifact work

- Replaced the four-input measurement/saved-evaluation snapshot notebook with a standalone
  nine-CSV pipeline. Required source, fixed protocols, solver plan and reference checks are
  embedded. No unpublished helper, precomputed traits or coefficient cache is required.
- Every primary/secondary/cone cohort model is refitted and frozen before evaluation; original
  `evaluate.py`, `route_context.py`, requirements and evaluation protocol are hash-checked
  against the existing frozen specification. No hypotheses, samples or outcome models changed.
- Whole-game batches preserve complete-track smoothing while avoiding a season-wide tracking
  materialisation. Keyed rebuilt game traits match all 314,227 historical rows exactly;
  Combine attempt traits and sprint traits match exactly. Combine player means differ only
  at floating-point rounding (~7e-16). Batch invariance is now a meaningful regression test.
- First full raw rebuild caught a solver-path difference in historical W2 + cone. Original
  run retried Powell; raw rebuilding's unordered join accepted the default solver, changing
  coefficient uncertainty. The portable reproduction now replays **the originally recorded
  Powell solver** using only an embedded solver/column plan, never cached coefficients. All
  other models retain existing numerical rules. No prediction source/model/sample changed.
- After solver replay, **402 numeric comparisons** and all **25 equal-athlete scores** pass
  the original verification tolerance. Disjoint players, frozen hashes and common-context
  error identities pass. Historical reports remain unchanged. Deviations from the first
  attempt are retained in `reproduction_deviations.json` rather than hidden.
- Writeup: 1,900 conservative words including captions, alt text and table, six figures and
  one table. Offline preview embeds all six PNGs. All nine evaluation rows are generated
  directly from `evaluation_table.csv`; source metadata and asset hashes are saved.
- Official requirements, rubric, deadline, data license, track description and award split
  verified from Kaggle API; field definitions reviewed in `official_sources.md`.

## Claim review

| Proposed claim | Evidence and permitted wording |
|---|---|
| WR TURN has cross-drill consistency | Development SB 0.593 [0.373,0.737], 70 athletes; not single-route repeatability |
| Some movement carries into games | WR turning r 0.279, DL burst r 0.443, with intervals and size adjustment; pooled descriptive PRE+REG |
| Primary performance gain remains uncertain | 0/9 primary marginal intervals support RMSE improvement; all family intervals cross zero; not equivalence |
| Route primary stopped appropriately | Adjusted SB 0.296 < frozen 0.40; no TURN interaction fitted |
| Cone subsets merit transparent reporting | DL A0 nine-athlete gain and DL TURN historical association retained alongside adverse/uncertain subset results; no general ranking |
| Scout card supports film/practice questions | Proposed use only; no validated causal training benefit, individual change threshold or draft upgrade |

Main limitations are explicit: prior 2025 exposure, selected small samples, training uncertainty
omitted, realised context, assumed calendar-intercept persistence, numerical boundary fits and
absent opponents/ball. Get-off is LOS-crossing time; pressure generation remains the defined
recorded-time proxy. Internal review is not external endorsement.

## Remaining owner and platform checks

Final clean notebook/Kaggle outcomes are recorded separately, with measured time/memory, rather
than assumed from intermediate runs. Both local and Kaggle clean raw rebuilds pass all checks.
Public version 3 preserves tested source and includes all 59 saved outputs; API public/source
verification passes. Direct anonymous HTTP returned 404, so browser access/rendering still
requires owner confirmation. Owner fresh-kernel/design review, actual public-access
verification, writeup attachment/rendering and final Submit are separate completion conditions.
Do not mark the competition submission complete until its confirmation exists.

## November 10 presentation revision

The owner deleted the first public notebook because its serialized source cell overwhelmed the reading view. Format 2 stores ordinary source files and their hashes in notebook metadata; visible code is at most 1,502 characters. Six numbered figure sections, a formatted table, quiet setup/logs and collapsible complete reports replace the earlier layout. Kaggle raw version 3 passes 402 checks, 25 scores and 12 tests; redesigned public version 4 is verified via API. The source-only W1 historical BFGS/L-BFGS replay uses canonical row ordering to preserve its recorded result, alongside the existing W2 Powell replay. No model formula, sample, frozen prediction source or verification tolerance changed. Updated notebook reading preview is included in the ZIP.
