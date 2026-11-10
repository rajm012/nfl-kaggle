# NFL Big Data Bowl 2027 — Combine movement evidence map

This University-track project separates movement measurement, Combine-to-game transfer,
and added regular-season performance prediction. The nine primary cohort comparisons
do not establish a supported prediction gain; secondary cone findings remain separate.

- [Writeup](writeup/writeup.md) and [standalone visual preview](writeup/preview.html)
- [Self-contained raw-input notebook](notebooks/submission.ipynb)
- [Notebook reading preview](writeup/notebook_preview.html)
- [Current state](STATUS.md), [project memory](CLAUDE.md) and [submission checklist](reports/submission_checklist.md)
- [Validation interpretation](reports/validation_findings.md) and [production review](reports/submission_review.md)

## Run locally

Use the project `.venv` and place the nine competition CSVs in `data/raw/`.
Open `notebooks/submission.ipynb`, set `BDB_INPUT_ROOT` to that folder,
restart the kernel, and Run All. Every run creates a fresh temporary output directory.
Launch with `BDB_INPUT_ROOT="$PWD/data/raw" .venv/bin/python -m jupyter lab notebooks/submission.ipynb`.
On Kaggle, attach `nfl-big-data-bowl-2027` as a competition source and enable Internet
for installation of the recorded dependencies. CPU is sufficient; no GPU is used.

The notebook stores all required project source in its metadata, with verified hashes.
Its reading view has six figure sections, a formatted table and a collapsible report appendix.
It rebuilds features, measurement and
transfer checks, the historical model audit, all 25 frozen cohort comparisons, cone
sensitivities, six figures and the evaluation table. Reference results are assertions
after fitting, not a substitute for computation. No source module needs downloading.
`src.build_submission_notebook` regenerates the notebook and clears outputs; execute
it again after any intentional source change. Frozen prediction/protocol files must
not be changed to tune evaluation results.

## Attribution and licensing

Code is under the MIT license in [LICENSE](LICENSE). Competition data are supplied by
the NFL through [NFL Big Data Bowl 2027](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/data)
under CC BY-NC 4.0 and remain subject to the competition's access rules. The code license
does not relicense data. Raw files, derived data and credentials are excluded from Git.

Publication and the final owner submission are tracked separately from local verification.
