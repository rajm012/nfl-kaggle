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
CSV and cached Parquet paths. It currently contains counts, key checks, season coverage and
a draft eligibility chart; no new trait–outcome results.

Check these numbers:

| Item | Expected |
|---|---:|
| Players | 510 |
| Player-play rows | 314,197 |
| Study 3 eligible WRs: 2023 | 25 |
| Study 3 eligible WRs: 2024 | 17 |
| Study 3 eligible WRs: 2025 | 16 |

Your first design review: can the chart clearly explain why only 42 development and 16
evaluation receivers enter this comparison? Suggest changes to labels, colours and wording.
Keep the data and eligibility definition fixed while editing presentation.

Figure: `reports/figures/study3_support.png`. Full audit: `reports/audit.md`.

## Second: remote inventory through SSH

The supplied address is kept out of this document; use your usual SSH connection name in
place of `YOUR_SSH_HOST` below. Run from the local project root:

```bash
ssh YOUR_SSH_HOST 'python3 -' < src/system_info.py
```

This executes a standard-library resource inventory via stdin and prints CPU availability,
RAM, free disk, Python and GPU/driver information. It does not install packages, transfer data,
or modify remote files. Authenticate in your own terminal as usual. Return the JSON output;
there is no need to put a password or private key in chat.

The assistant's initial non-interactive SSH attempt reached the server but authentication
was rejected. The owner confirms password login. Machine specifications remain unverified.
A project-specific SSH key has been prepared locally outside the repository. To enable
assistant-run jobs, install only its public key from your own terminal:

```bash
ssh-copy-id -i ~/.ssh/nfl_bdb_2027_ed25519.pub YOUR_SSH_HOST
```

Enter the server password in that terminal. This adds the project public key to the account's
authorized keys. The private key remains local. After installation, the assistant can check
access with that key and run the resource inventory. Continue notebook review while setup
is pending. Passwords and private keys do not belong in chat or project files.

## Optional: rerun the complete input audit

```bash
.venv/bin/python -m src.audit_data --tracking-keys
```

This checks all game-frame keys through DuckDB without loading tracking into pandas. Current
run: zero integrity failures; two documented join-attrition notes. There are 2,496 game-trait
rows without a player-play row and 2,466 player-play rows without a game-trait row. Their
causes still need investigation. CSV and Parquet player-play row counts agree; the old data
page's 316,338 count differs from the downloaded file, not from conversion.

## What the assistant does next

Explain join attrition and reproduce movement reliability, then run the frozen measurement
screen before any new trait–outcome model. Keep 2025 reserved from further development and
retain the November 20 story decision. Update `STATUS.md` with each completed block.
