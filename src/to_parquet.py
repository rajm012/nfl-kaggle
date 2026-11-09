"""Convert raw CSVs to Parquet (streaming via DuckDB, low memory).

Run from project root:  .venv/bin/python -m src.to_parquet
Outputs: data/interim/<name>.parquet (+ all game tracking seasons in game_tracking.parquet, with a season column).
"""
from pathlib import Path

import duckdb

RAW = Path("data/raw")
OUT = Path("data/interim")


def ready(p: Path) -> bool:
    """Skip files still being downloaded (empty or with a .kaggle-partial marker)."""
    return p.stat().st_size > 0 and not p.with_name(p.name + ".kaggle-partial").exists()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute("SET memory_limit='4GB'; SET preserve_insertion_order=false;")

    for csv in sorted(RAW.glob("*.csv")):
        if csv.stem.startswith("game_tracking_") or not ready(csv):
            continue
        dst = OUT / f"{csv.stem}.parquet"
        con.execute(
            f"COPY (SELECT * FROM read_csv_auto('{csv}', sample_size=-1, nullstr='NA')) "
            f"TO '{dst}' (FORMAT parquet, COMPRESSION zstd)"
        )
        print(f"{csv.name} -> {dst.name}")

    seasons = sorted(RAW.glob("game_tracking_*.csv"))
    if len(seasons) == 3 and all(map(ready, seasons)):
        dst = OUT / "game_tracking.parquet"
        union = " UNION ALL ".join(
            f"SELECT {p.stem[-4:]}::SMALLINT AS season, * FROM read_csv_auto('{p}', nullstr='NA')" for p in seasons
        )
        con.execute(f"COPY ({union}) TO '{dst}' (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 500000)")
        print(f"{[p.name for p in seasons]} -> {dst.name}")

    for pq in sorted(OUT.glob("*.parquet")):
        n = con.execute(f"SELECT count(*) FROM '{pq}'").fetchone()[0]
        print(f"{pq.name:35s} {n:>12,d} rows  {pq.stat().st_size / 2**20:8.1f} MiB")


if __name__ == "__main__":
    main()
