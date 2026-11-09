"""Per-player Combine movement-trait features (drill-normalised).

Run:  .venv/bin/python -m src.combine_features
Out:  data/interim/combine_frames.parquet   frame-level kinematics (PLAYER rows only)
      data/interim/combine_attempts.parquet per-attempt raw features
      data/interim/combine_traits.parquet   one row per player: z-scored traits + split-half A/B versions

Why drill-normalised: players run different drill mixes, and pooling raw frames across drills made
split-half reliability ~0 (drill mix swamped the player). Fix: per attempt -> mean per (player, drill)
-> z-score within drill -> average across drills. Raw-pool attempt kept in git history (2026-10-08).

Per-attempt features (straight-line 40 excluded):
  lat   : 90th pct |a_lat|  (turning / cornering capacity)
  burst : max a_lon         (re-acceleration)
  brake : -min a_lon        (peak braking; positive = harder)  -- low reliability, keep as secondary
  vmax  : max speed in drill
  dur   : drill duration (s); lower = quicker completion
"""
import polars as pl

from src.kinematics import add_kinematics

INTERIM = "data/interim"
FEATS = ["lat", "burst", "brake", "vmax", "dur"]

# Canonicalise duplicate drill spellings found in the data.
DRILL_ALIASES = {
    "PASS_PRO-MIRROR_DRILL": "PASS_PRO_MIRROR_DRILL",
    "LINE": "LINE_DRILL",
    "SPEED_OUT_LEFT": "SPEED_OUT_ROUTE_LEFT",
    "OVER_THE_SHOULDER_ADJUST": "OVER_SHOULDER_ADJUST",
}


def player_traits(player_drill: pl.DataFrame) -> pl.DataFrame:
    return player_drill.group_by("nfl_id").agg(
        [pl.col(f"z_{x}").mean().alias(x) for x in FEATS] + [pl.len().alias("n_drills")]
    )


def main() -> None:
    ct = (
        pl.scan_parquet(f"{INTERIM}/combine_tracking.parquet")
        .filter(pl.col("entity_type") == "PLAYER")
        .with_columns(drill=pl.col("drill_name").replace(DRILL_ALIASES))
        .sort("event_id", "time")
        .collect()
    )
    frames = add_kinematics(ct, ["event_id"])
    frames.write_parquet(f"{INTERIM}/combine_frames.parquet")

    att = (
        frames.filter(pl.col("drill_type") != "FORTY_YARD_DASH")
        .group_by("nfl_id", "drill", "event_id")
        .agg(
            lat=pl.col("a_lat").abs().quantile(0.9),
            burst=pl.col("a_lon").max(),
            brake=-pl.col("a_lon").min(),
            vmax=pl.col("sp").max(),
            dur=pl.len() * 0.1,
        )
    )
    att.write_parquet(f"{INTERIM}/combine_attempts.parquet")

    pdz = (
        att.group_by("nfl_id", "drill")
        .agg([pl.col(x).mean() for x in FEATS])
        .with_columns(
            [((pl.col(x) - pl.col(x).mean().over("drill")) / pl.col(x).std().over("drill")).alias(f"z_{x}") for x in FEATS]
        )
        .sort("nfl_id", "drill")
        .with_columns(half=pl.int_range(pl.len()).over("nfl_id") % 2)
    )
    full = player_traits(pdz)
    halves = [
        player_traits(pdz.filter(pl.col("half") == h)).drop("n_drills").rename({x: f"{x}_{s}" for x in FEATS})
        for h, s in [(0, "A"), (1, "B")]
    ]
    out = full.join(halves[0], on="nfl_id", how="left").join(halves[1], on="nfl_id", how="left")
    out.write_parquet(f"{INTERIM}/combine_traits.parquet")
    print(out.describe())


if __name__ == "__main__":
    main()
