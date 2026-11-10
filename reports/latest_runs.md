# Current run results — 2026-11-10

All jobs in this work block completed locally with bounded threads. Remote SSH timed out;
the owner requested local execution. No server jobs/data transfers or public pushes occurred.

**Current stage: submission packet, full Kaggle reproduction and notebook publication complete; owner Writeup UI steps remain.**
Retain the evidence-map narrative and November 20 claim-review checkpoint. Complete writeup,
six figures/table, self-contained raw-input notebook, preview and ZIP are available. Owner
review, actual Writeup attachment/rendering and final Submit remain. Handoff:
[submission_handoff.md](submission_handoff.md). Interpretation: [validation_findings.md](validation_findings.md).

| Run | Result | Saved evidence |
|---|---|---|
| Join audit | All 2,466 missing movement rows explained; 2,496 movement-only keys confirmed in source tracking | `join_attrition.md`, `join_attrition.json` |
| Movement reliability | Historical WR TURN SB=0.546; development/training-reference SB=0.593 [0.373,0.737], 70 WRs | `reliability.md`, `reliability.json`, `study3_turn_reference.json` |
| Route-family measurement | **FAIL**: adjusted SB=0.296 [−0.257,0.606], 41 WRs; frozen gate requires ≥0.40 | `study3_measurement.md`, `.json`, baseline/preprocessing metadata |
| Studies 1–2 audit | All 15 fits converge; **0/9** two-sided Holm-significant original-family tests, **0/3** robust binary sensitivities | `model_audit.md`, `.json`, checkpoints, run log |
| Movement transfer | Corrected PRE+REG WR TURN r=0.279 [0.107,0.445], n=98; DL BURST r=0.443 [0.289,0.584], n=115 | `transfer_audit.md`, `.json`, run log |
| DL size adjustment | Weight-adjusted BURST transfer r=0.203 [0.044,0.376], n=115 | `transfer_audit.md`, `.json` |
| Cohort prediction | 25 frozen comparisons scored; **0/9** primary marginal intervals support a gain; all original-family intervals cross zero | `validation.*`, `evaluation_development.json`, `evaluation_models/` |
| Same-sample 3-cone | Nine historical four-model comparisons on identical rows, n=23–43; selected secondary signals retained | `cone_sensitivity.md`, `.json` |
| Portable notebook | Complete nine-raw-CSV clean-kernel rebuild passes in 523.08 s, largest sampled stage RSS 1,183 MiB | `notebooks/submission.ipynb`, `full_notebook_execution.json`, `full_notebook_stages.json` |
| Statistical checks | Twelve tests pass; 402 numeric comparisons and all 25 athlete scores verified, disjoint cohorts and frozen hashes checked | `tests/`, `submission_verification.json` |
| Production packet | 1,900 conservative words; six figures + one table; standalone preview and ZIP | `writeup/`, `submission_packet.json`, `submission_review.md` |
| Official source checks | Rubric/limits, undergraduate Track 7289, awards, deadline and field semantics verified through official API | `official_sources.md`, `official_tracks.json` |
| Kaggle reproduction/publication | 1,421.62 s, sampled largest stage RSS 1,021.4 MiB; all checks pass. Public version 3 has 59 saved outputs and six figures; unchanged-code QUICK_SAVE after full execution version 1 | `kaggle_execution.json`, `kaggle_publication.json` |

Reliability intervals use 10,000 athlete bootstrap resamples; adjusted-transfer intervals
use 2,000 paired athlete resamples with residualisation refitted each time. These are
descriptive measurement/transfer results, distinct from performance prediction.

## Consequence for the research

The frozen Study 3 screen fails before a TURN interaction is fitted. Keep the original
threshold/route grouping; **stop the primary route-performance claim** and proceed with the
planned evidence-map narrative. The contrast interval is wide and the screen is descriptive;
failure does not prove every route-specific effect is zero.

The conventional screen used 3,971 rookie REG development plays from 42 WRs, design rank 65.
41 had sufficient alternating-game halves. No route-family TURN interaction or Study 3 evaluation was fitted. The separate original Studies 1–2 cohort prediction has now scored 2025 rookie outcomes under the frozen protocol. Prior outcome exposure remains disclosed.

The audited earlier association results remain non-significant, including robust binary
sensitivities and unique-player Study 2 scaling. Their historical reports are byte-for-byte
unchanged. Some LMMs report random-effect boundary warnings despite convergence; warnings
and model-based uncertainty limits are saved. No supported primary out-of-sample performance gain or equivalence has been established; favourable selected subsets remain secondary findings.

## Draft figures now available

- `figures/study3_measurement.png`: raw/adjusted separation-contrast repeatability.
- `figures/transfer_audited.png`: raw versus size-adjusted movement transfer with intervals.
- `figures/combine_route_trace.png`: actual speed-out paths and lateral acceleration for two similar-40 WRs selected using exposures only; rule in `route_trace_selection.json`.
- `figures/study3_support.png`: unique receiver support by cohort.
- `figures/cohort_prediction.png`: all nine original primary prediction gains/intervals; `evaluation_table.csv` contains their unit-labelled scores.

The notebook now rebuilds movement features, audits, all 25 frozen cohort comparisons, historical cone checks and every selected figure/table from all nine CSVs. It embeds source, protocols and assertion references, not a fitted-result substitute. The earlier four-input measurement/review snapshot is superseded. Original historical W2+cone Powell retry is replayed using its recorded solver plan; reproduction checks retain the original tolerances.

## Exact next work
1. Owner checks the public notebook in their browser; API confirms public flag, matching code and saved outputs, but direct anonymous web requests return 404 from this workspace.
2. Owner reviews the completed preview/notebook; uploads six figures, pastes the manuscript/table and attaches the public notebook in the Writeup editor, checking its actual rendering.
3. Owner confirms personal undergraduate eligibility/University track and any terms, then final Submit by Dec 28 and saves confirmation. Keep Nov 20 claim review and Dec deadlines.

Do not launch a new route primary model or hypothesis family to bypass the failed gate.

## Rerun commands
Use the existing local environment from the project root:
```bash
export OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 POLARS_MAX_THREADS=2
.venv/bin/python -m src.join_audit
.venv/bin/python -m src.reliability
.venv/bin/python -m src.route_context
.venv/bin/python -m src.validation
.venv/bin/python -m src.transfer_audit
.venv/bin/python -m src.audit_figures
.venv/bin/python -m src.evaluate --stage develop
.venv/bin/python -m src.evaluate --stage evaluate
.venv/bin/python -m src.cone_sensitivity
.venv/bin/python -m src.evaluation_figures
.venv/bin/python -m unittest discover -s tests -v
```

Use `src.build_submission_notebook` for the complete submission; it clears outputs and must be followed by full raw-input execution. `build_measurement_notebook` is a historical skeleton generator and would remove full-submission sections. `src.build_submission_packet` regenerates the manuscript table, preview, ZIP and asset/count manifest.

Prediction source/protocol is frozen and hash-checked. Any later error correction must be documented; no model tuning after the cohort results have been opened. Bootstrap prediction intervals condition on training fits and omit training uncertainty.
