#!/usr/bin/env bash
# Download competition files one by one with retries (needs ~/.kaggle/access_token).
set -uo pipefail
cd "$(dirname "$0")/.."
COMP=nfl-big-data-bowl-2027
FILES="players.csv combine_results.csv player_career_successes.csv games.csv combine_tracking.csv player_play.csv game_tracking_2023.csv game_tracking_2024.csv game_tracking_2025.csv"
mkdir -p data/raw
for f in $FILES; do
  [ -s "data/raw/$f" ] && { echo "have $f"; continue; }
  for try in 1 2 3 4 5; do
    .venv/bin/python -m kaggle competitions download -c $COMP -f "$COMP/$f" -p data/raw -q && break
    echo "retry $f ($try)"; sleep 10
  done
  # Kaggle may deliver a zip
  for z in data/raw/*.zip; do [ -e "$z" ] && unzip -o -q "$z" -d data/raw && rm "$z"; done
done
ls -lh data/raw
