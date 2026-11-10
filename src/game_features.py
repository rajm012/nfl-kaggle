"""Per player-play movement traits from game tracking (same definitions as the Combine traits).

Run:  .venv/bin/python -m src.game_features
Out:  data/interim/game_play_traits.parquet  one row per (game_id, play_id, nfl_id)

Window (pre-registered amendment 2026-10-29): kinematics on the full track, then frames in
[ball_snap, ball_snap + 3.0 s]. lat = 90th pct |a_lat|, burst = max a_lon, vmax = max speed.
"""
import duckdb
import numpy as np
import polars as pl
from pathlib import Path
import tempfile

from src.kinematics import decompose

INTERIM = "data/interim"
WINDOW_S = 3.0
MIN_FRAMES = 10


def season_traits(con: duckdb.DuckDBPyConnection, season: int,
                  game_ids: list[int] | None = None) -> pl.DataFrame:
    # Batches contain whole games: no player track is split across a boundary.
    game_filter = '' if game_ids is None else (
        ' AND game_id IN (' + ','.join(str(int(g)) for g in game_ids) + ')')
    df = con.sql(f"""
        SELECT game_id, play_id, nfl_id, epoch(time) AS t, x, y, event = 'ball_snap' AS is_snap
        FROM '{INTERIM}/game_tracking.parquet' WHERE season = {season}{game_filter}
        ORDER BY game_id, play_id, nfl_id, time""").pl()
    key = df.select("game_id", "play_id", "nfl_id").to_numpy()
    t, x, y, snap = (df[c].to_numpy() for c in ("t", "x", "y", "is_snap"))
    snap = np.nan_to_num(snap.astype(float)).astype(bool)
    bounds = np.flatnonzero(np.any(key[1:] != key[:-1], axis=1)) + 1
    starts, ends = np.r_[0, bounds], np.r_[bounds, len(df)]

    rows = []
    for s, e in zip(starts, ends):
        snaps = np.flatnonzero(snap[s:e])
        if len(snaps) == 0 or e - s < 15:
            continue
        k = decompose(x[s:e], y[s:e])
        t0 = t[s + snaps[0]]
        w = (t[s:e] >= t0) & (t[s:e] <= t0 + WINDOW_S + 1e-6)
        if w.sum() < MIN_FRAMES:
            continue
        rows.append((*key[s], np.quantile(np.abs(k["a_lat"][w]), 0.9), k["a_lon"][w].max(), k["sp"][w].max(), int(w.sum())))
    return pl.DataFrame(rows, schema=["game_id", "play_id", "nfl_id", "lat", "burst", "vmax", "n_frames"], orient="row")


def main() -> None:
    con = duckdb.connect()
    con.execute("SET memory_limit='256MB'")
    con.execute('SET threads=2')
    # ~120k frames per batch instead of materialising a whole season in RAM.
    with tempfile.TemporaryDirectory(prefix='game_batches_', dir=INTERIM) as temporary:
        pieces = []
        for season in (2023, 2024, 2025):
            games = con.execute(f"SELECT game_id, count(*) FROM '{INTERIM}/game_tracking.parquet' "
                                f"WHERE season={season} GROUP BY game_id ORDER BY game_id").fetchall()
            batches, batch, frames = [], [], 0
            for game, count in games:
                if batch and frames + count > 120000:
                    batches.append(batch)
                    batch, frames = [], 0
                batch.append(game)
                frames += count
            if batch:
                batches.append(batch)
            total = 0
            for index, games_in_batch in enumerate(batches):
                d = season_traits(con, season, games_in_batch).with_columns(season=pl.lit(season))
                target = Path(temporary) / f'{season}_{index:04d}.parquet'
                d.write_parquet(target)
                pieces.append(str(target).replace("'", "''"))
                total += d.height
                if index % 10 == 0:
                    print(f'{season}: batch {index+1}/{len(batches)}, {total:,} player-plays', flush=True)
            print(season, total, 'player-plays', flush=True)
        paths = '[' + ','.join("'" + p + "'" for p in pieces) + ']'
        con.execute(f"COPY (SELECT * FROM read_parquet({paths}) ORDER BY season,game_id,play_id,nfl_id) "
                    f"TO '{INTERIM}/game_play_traits.parquet' (FORMAT parquet, COMPRESSION zstd)")
    con.close()


if __name__ == "__main__":
    main()
