#!/usr/bin/env bash
# Robust full-data download: Kaggle "download-all" endpoint -> signed GCS URL -> curl with resume.
# Used because per-file downloads of the large game_tracking CSVs stall server-side (2026-10-29).
# Token: ~/.kaggle/access_token (never printed). Curl does not forward the auth header to the GCS redirect host.
set -uo pipefail
cd "$(dirname "$0")/.."
ZIP=data/raw/all.zip
for try in $(seq 1 30); do
  curl -sS -L --fail -C - --retry 3 --speed-limit 10000 --speed-time 120 \
       -H "Authorization: Bearer $(cat ~/.kaggle/access_token)" \
       -o "$ZIP" "https://www.kaggle.com/api/v1/competitions/data/download-all/nfl-big-data-bowl-2027" && break
  echo "attempt $try failed ($(du -h "$ZIP" 2>/dev/null | cut -f1)); retrying"; sleep 15
done
unzip -t -q "$ZIP" && unzip -o -j -q "$ZIP" '*game_tracking_*' -d data/raw/ && rm "$ZIP" && echo "DONE" || echo "ZIP INVALID"
ls -lh data/raw
