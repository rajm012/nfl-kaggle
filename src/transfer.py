"""Combine -> game transfer test (pre-registered, reports/prereg.md amendment 2026-10-29).

Run:  .venv/bin/python -m src.transfer
Out:  data/interim/game_player_traits.parquet, reports/transfer.md
"""
import numpy as np
import polars as pl

INTERIM = "data/interim"
TRAITS = ["lat", "burst", "vmax"]
MIN_PLAYS = 30


def game_player_traits() -> pl.DataFrame:
    g = pl.read_parquet(f"{INTERIM}/game_play_traits.parquet")
    pp = pl.read_parquet(f"{INTERIM}/player_play.parquet").select(
        "game_id", "play_id", "nfl_id", "lined_up_position", "route_ran", "dropback_duration", "sack")
    pos = pl.read_parquet(f"{INTERIM}/combine_results.parquet").select("nfl_id", "combine_position")
    d = g.join(pp, on=["game_id", "play_id", "nfl_id"]).join(pos, on="nfl_id")
    play_type = (
        pl.when(pl.col("combine_position").is_in(["WR", "TE"])).then(pl.col("route_ran").fill_null("NO_ROUTE"))
        .when(pl.col("combine_position") == "OL").then(pl.when(pl.col("dropback_duration").is_not_null()).then(pl.lit("PASS")).otherwise(pl.lit("RUN")))
        .when(pl.col("combine_position") == "DL").then(pl.when(pl.col("sack").is_not_null()).then(pl.lit("PASS")).otherwise(pl.lit("RUN")))
        .otherwise(pl.lit("ALL"))
    )
    cell = ["lined_up_position", "play_type"]
    d = d.with_columns(play_type=play_type).with_columns(
        [((pl.col(t) - pl.col(t).mean().over(cell)) / pl.col(t).std().over(cell)).alias(f"z_{t}") for t in TRAITS]
    ).with_columns(half=(pl.col("game_id").rank("dense").over("nfl_id") % 2))
    full = d.group_by("nfl_id", "combine_position").agg([pl.col(f"z_{t}").mean().alias(f"g_{t}") for t in TRAITS] + [pl.len().alias("n_plays")])
    halves = [
        d.filter(pl.col("half") == h).group_by("nfl_id").agg([pl.col(f"z_{t}").mean().alias(f"g_{t}_{h}") for t in TRAITS])
        for h in (0, 1)
    ]
    return full.join(halves[0], on="nfl_id", how="left").join(halves[1], on="nfl_id", how="left").filter(pl.col("n_plays") >= MIN_PLAYS)


def r_ci(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float, int]:
    m = ~(np.isnan(x) | np.isnan(y))
    n = int(m.sum())
    r = float(np.corrcoef(x[m], y[m])[0, 1])
    z, se = np.arctanh(r), 1 / np.sqrt(n - 3)
    return r, float(np.tanh(z - 1.96 * se)), float(np.tanh(z + 1.96 * se)), n


def main() -> None:
    gp = game_player_traits()
    gp.write_parquet(f"{INTERIM}/game_player_traits.parquet")
    ct = pl.read_parquet(f"{INTERIM}/combine_traits.parquet").select("nfl_id", *TRAITS)
    d = gp.join(ct, on="nfl_id")
    rows = []
    for pos in ["WR", "OL", "DL", "TE", "DB"]:
        s = d.filter(pl.col("combine_position") == pos)
        for t in TRAITS:
            r, lo, hi, n = r_ci(s[t].to_numpy(), s[f"g_{t}"].to_numpy())
            rel = s.select(pl.corr(f"g_{t}_0", f"g_{t}_1")).item()
            rows.append({"pos": pos, "trait": t, "n_players": n, "r_combine_game": round(r, 2),
                         "ci95": f"[{lo:.2f}, {hi:.2f}]", "game_split_half_SB": round(2 * rel / (1 + rel), 2)})
    res = pl.DataFrame(rows)
    print(res)
    with open("reports/transfer.md", "w") as f:
        f.write("# Combine → game transfer (pre-registered; see prereg.md amendment 2026-10-29)\n\n")
        f.write("Pearson r between Combine trait and the player's game trait (mean z over plays, ≥30 plays), within position.\n")
        f.write("game_split_half_SB = reliability of the game trait (odd vs even games, Spearman–Brown).\n\n")
        f.write("| pos | trait | n | r | 95% CI | game reliability |\n|---|---|---|---|---|---|\n")
        for x in res.iter_rows(named=True):
            f.write(f"| {x['pos']} | {x['trait']} | {x['n_players']} | {x['r_combine_game']} | {x['ci95']} | {x['game_split_half_SB']} |\n")


if __name__ == "__main__":
    main()
