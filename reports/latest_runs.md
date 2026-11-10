# Current run results — 2026-11-09

All jobs in this work block completed locally with bounded threads. Remote SSH timed out;
the owner requested local execution. No server jobs/data transfers or public pushes occurred.

| Run | Result | Saved evidence |
|---|---|---|
| Join audit | All 2,466 missing movement rows explained; 2,496 movement-only keys confirmed in source tracking | `join_attrition.md`, `join_attrition.json` |
| Movement reliability | Historical WR TURN SB=0.546; development/training-reference SB=0.593 [0.373,0.737], 70 WRs | `reliability.md`, `reliability.json`, `study3_turn_reference.json` |
| Route-family measurement | **FAIL**: adjusted SB=0.296 [−0.257,0.606], 41 WRs; frozen gate requires ≥0.40 | `study3_measurement.md`, `.json`, baseline/preprocessing metadata |
| Studies 1–2 audit | All 15 fits converge; **0/9** two-sided Holm-significant original-family tests, **0/3** robust binary sensitivities | `model_audit.md`, `.json`, checkpoints, run log |
| Movement transfer | Corrected PRE+REG WR TURN r=0.279 [0.107,0.445], n=98; DL BURST r=0.443 [0.289,0.584], n=115 | `transfer_audit.md`, `.json`, run log |
| DL size adjustment | Weight-adjusted BURST transfer r=0.203 [0.044,0.376], n=115 | `transfer_audit.md`, `.json` |
| Portable notebook | CSV and Parquet clean-kernel runs match the standalone measurement screen exactly; 6.10/4.45 s | `notebooks/submission.ipynb`, `notebook_execution.json` |
| Statistical checks | Five tests pass: reference leakage, unique-player SDs, equal-family weights/rank, retained groups, negative/degenerate reliability | `tests/test_audit.py` |

Reliability intervals use 10,000 athlete bootstrap resamples; adjusted-transfer intervals
use 2,000 paired athlete resamples with residualisation refitted each time. These are
descriptive measurement/transfer results, distinct from performance prediction.

## Consequence for the research

The frozen Study 3 screen fails before a TURN interaction is fitted. Keep the original
threshold/route grouping; **stop the primary route-performance claim** and proceed with the
planned evidence-map narrative. The contrast interval is wide and the screen is descriptive;
failure does not prove every route-specific effect is zero.

The conventional screen used 3,971 rookie REG development plays from 42 WRs, design rank 65.
41 had sufficient alternating-game halves. All 16 eligible 2025 WRs remain outside new
performance evaluation. Prior 2025 outcome exposure in Studies 1–2 is still disclosed.

The audited earlier association results remain non-significant, including robust binary
sensitivities and unique-player Study 2 scaling. Their historical reports are byte-for-byte
unchanged. Some LMMs report random-effect boundary warnings despite convergence; warnings
and model-based uncertainty limits are saved. No out-of-sample performance gain or
equivalence has been established.

## Draft figures now available

- `figures/study3_measurement.png`: raw/adjusted separation-contrast repeatability.
- `figures/transfer_audited.png`: raw versus size-adjusted movement transfer with intervals.
- `figures/combine_route_trace.png`: actual speed-out paths and lateral acceleration for
  two similar-40 WRs selected using exposures only; rule in `route_trace_selection.json`.
- `figures/study3_support.png`: unique receiver support by cohort.

The notebook independently rebuilds the conventional screen from four competition inputs;
it is still a working version. Full movement-feature/model-audit rebuilding, final results
integration and clean Kaggle execution remain unfinished.

## Exact next work

1. Implement the already preregistered Studies 1–2 baseline-versus-tracking evaluation:
   train-only preprocessing, 2023–24 development, equal-player 2025 scoring, no evaluation
   player intercepts fitted from outcomes; disclose prior cohort exposure.
2. Complete same-sample 3-cone sensitivity and its opt-out/sample limitations.
3. Integrate audited movement/performance results into the portable notebook, evidence
   card and writeup; maintain the November 20 final-claim decision and December deadlines.

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
.venv/bin/python -m unittest discover -s tests -v
```

Run `src.build_measurement_notebook` only when updating embedded screen helper source;
it clears old cell outputs and must be followed by a fresh notebook execution.
