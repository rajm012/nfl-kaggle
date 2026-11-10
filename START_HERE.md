# Start together — 2026-11-09

You handle Python/notebook checks and design/writeup feedback. The assistant handles research,
football interpretation, statistical design and analysis. Research critique is internal;
there is no independent football/statistical reviewer at present.

## First: open the notebook locally

Open `notebooks/submission.ipynb` in your notebook editor with the project `.venv` Python
kernel. Alternatively, from the project root:

```bash
.venv/bin/python -m jupyter lab notebooks/submission.ipynb
```

Restart the kernel and run all cells. The starter has already executed locally on both raw
CSV and cached Parquet paths. It contains counts, key checks, season coverage, eligibility
and the frozen conventional separation-contrast measurement screen. No TURN interaction
or new 2025 performance evaluation was fitted.

Check these numbers:

| Item | Expected |
|---|---:|
| Players | 510 |
| Player-play rows | 314,197 |
| Study 3 eligible WRs: 2023 | 25 |
| Study 3 eligible WRs: 2024 | 17 |
| Study 3 eligible WRs: 2025 | 16 |
| Diagnostic development WRs | 41 |
| Adjusted contrast Spearman–Brown | 0.296 (gate fails below 0.40) |

Your first design review: can the chart clearly explain why only 42 development and 16
evaluation receivers enter this comparison? Suggest changes to labels, colours and wording.
Keep the data and eligibility definition fixed while editing presentation.

Figure: `reports/figures/study3_support.png`. Full audit: `reports/audit.md`.

## Second: remote inventory through SSH (deferred after November 9 local-work request)

Owner supplied `gpu2@192.168.0.104`, but the current workspace cannot reach SSH on that
LAN address. The owner explicitly requested local work. No remote jobs or data transfer
have occurred. Their `ssh-copy-id` output contained a Windows `exec` error, so its final
“key added” message is insufficient to verify access. Resume remote setup only when useful;
the local audited pipeline does not depend on it. Current results: `reports/latest_runs.md`.

The inventory helper is `src/system_info.py`; host RAM/cores/storage/GPU details remain
unverified. A future setup must use the actual remote OS and reachable address, then
verify key login directly. The project key remains outside the repository. Passwords,
private keys and Kaggle credentials do not belong in chat or project files.

## Optional: rerun the complete input audit

```bash
.venv/bin/python -m src.audit_data --tracking-keys
```

This checks all game-frame keys through DuckDB without loading tracking into pandas. Current
run: zero integrity failures; two documented join-attrition notes. There are 2,496 game-trait
rows without a player-play row and 2,466 player-play rows without a game-trait row. Their
source/extraction support is now documented in `reports/join_attrition.md`. CSV and Parquet
player-play row counts agree; the old data
page's 316,338 count differs from the downloaded file, not from conversion.

## What the assistant does next

The join, reliability, model, transfer, cohort prediction and cone checks are complete. The frozen route measurement screen failed, so its primary performance claim stops; none of the nine primary cohort prediction additions has a supported RMSE gain. Small selected cone findings remain secondary. Read `reports/validation_findings.md` and review `reports/figures/cohort_prediction.png` / `reports/evaluation_table.csv`.

The notebook now includes an explicitly labelled saved cohort-result review snapshot; those evaluation models are not yet rebuilt from raw inputs in the notebook. Next is complete notebook/figure/writeup integration. Keep the November 20 final-claim checkpoint. Current work and rerun commands: `reports/latest_runs.md`.
