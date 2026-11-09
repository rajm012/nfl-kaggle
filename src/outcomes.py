"""Confirmatory outcome tests W1, W2, O1, O2, D1, D2 (reports/prereg.md, frozen 2026-10-29).

Run:  .venv/bin/python -m src.outcomes
Out:  reports/confirmatory.md

Model: play-level linear mixed model, random intercept per player (statsmodels MixedLM).
Binary outcomes use the pre-registered fallback (linear probability). Team-season random effect omitted
(convergence; allowed by prereg "where it converges"). Trait effect = coefficient per 1 SD (z within position).
"""
import numpy as np
import polars as pl
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

INTERIM = "data/interim"


def base_table() -> pl.DataFrame:
    pp = pl.read_parquet(f"{INTERIM}/player_play.parquet")
    games = pl.read_parquet(f"{INTERIM}/games.parquet").select("game_id", "season", "season_type")
    players = pl.read_parquet(f"{INTERIM}/players.parquet").select("nfl_id", "draft_overall_pick")
    cr = pl.read_parquet(f"{INTERIM}/combine_results.parquet").select(
        "nfl_id", "combine_position", "forty", "combine_weight", "combine_height")
    tr = pl.read_parquet(f"{INTERIM}/combine_traits.parquet").select("nfl_id", "lat", "burst")
    p = (
        players.join(cr, on="nfl_id").join(tr, on="nfl_id")
        .with_columns(
            udfa=pl.col("draft_overall_pick").is_null().cast(pl.Int8),
            pick=pl.col("draft_overall_pick").fill_null(260),
            forty_missing=pl.col("forty").is_null().cast(pl.Int8),
            forty=pl.col("forty").fill_null(pl.col("forty").median().over("combine_position")),
        )
        .with_columns(
            [((pl.col(c) - pl.col(c).mean().over("combine_position")) / pl.col(c).std().over("combine_position")).alias(f"{c}_z")
             for c in ("lat", "burst", "forty", "combine_weight", "combine_height", "pick")]
        )
    )
    return (
        pp.join(games, on="game_id").filter((pl.col("season_type") == "REG") & (pl.col("play_nullified_by_penalty") == "N"))
        .join(p, on="nfl_id")
    )


BASE = "pick_z + udfa + forty_z + forty_missing + combine_weight_z + combine_height_z + C(season) + C(down) + yards_to_go"

TESTS = [
    # id, position, outcome expr, row filter, extra covariates, trait, expected sign
    ("W1", "WR", "separation_at_pass_forward", pl.col("separation_at_pass_forward").is_not_null(),
     "C(route_ran) + cushion_f + cushion_missing + C(team_coverage_man_zone) + C(receiver_alignment) + in_motion", "lat", +1),
    ("W2", "WR", "separation_at_pass_forward", pl.col("separation_at_pass_forward").is_not_null(),
     "C(route_ran) + cushion_f + cushion_missing + C(team_coverage_man_zone) + C(receiver_alignment) + in_motion", "burst", +1),
    ("O1", "OL", "pressure_allowed_i", pl.col("pressure_allowed").is_not_null(),
     "dropback_duration + pass_rushers_encountered", "lat", -1),
    ("O2", "OL", "pressure_allowed_i", pl.col("pressure_allowed").is_not_null(),
     "dropback_duration + pass_rushers_encountered", "burst", -1),
    ("D1", "DL", "player_get_off", pl.col("player_get_off").is_not_null(), "blitz + C(lined_up_position)", "burst", -1),
    ("D2", "DL", "pressure_i", pl.col("sack").is_not_null(), "blitz + C(lined_up_position)", "lat", +1),
]


def prep(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        cushion_missing=pl.col("cushion").is_null().cast(pl.Int8),
        cushion_f=pl.col("cushion").fill_null(pl.col("cushion").median()),
        in_motion=pl.col("in_motion_at_ball_snap").fill_null(False).cast(pl.Int8),
        blitz=pl.col("blitzing").fill_null(False).cast(pl.Int8),
        pressure_allowed_i=pl.col("pressure_allowed").cast(pl.Int8),
        pressure_i=pl.col("time_to_pressure").is_not_null().cast(pl.Int8),
        team_coverage_man_zone=pl.col("team_coverage_man_zone").fill_null("UNK"),
        receiver_alignment=pl.col("receiver_alignment").fill_null("UNK"),
        route_ran=pl.col("route_ran").fill_null("UNK"),
        lined_up_position=pl.col("lined_up_position").fill_null("UNK"),
    )


def main() -> None:
    df = prep(base_table())
    rows = []
    for tid, pos, y, filt, extra, trait, sign in TESTS:
        d = df.filter((pl.col("combine_position") == pos) & filt).to_pandas()
        formula = f"{y} ~ {trait}_z + {BASE} + {extra}"
        fit = smf.mixedlm(formula, d, groups=d["nfl_id"]).fit()  # default optimiser chain; lbfgs alone silently failed
        assert fit.converged, f"{tid} did not converge"
        b, se = fit.params[f"{trait}_z"], fit.bse[f"{trait}_z"]
        p_two = fit.pvalues[f"{trait}_z"]
        p_dir = p_two / 2 if np.sign(b) == sign else 1 - p_two / 2  # one-sided in pre-registered direction
        rows.append(dict(id=tid, pos=pos, outcome=y, trait=trait, expected="+" if sign > 0 else "-",
                         n_plays=len(d), n_players=d["nfl_id"].nunique(), beta=b, lo=b - 1.96 * se, hi=b + 1.96 * se,
                         sd_y=d[y].std(), p_dir=p_dir))
        print(tid, f"beta={b:.4f} [{b - 1.96 * se:.4f},{b + 1.96 * se:.4f}] p_dir={p_dir:.4f} n={len(d)}")
    res = pl.DataFrame(rows)
    res = res.with_columns(p_holm=pl.Series(multipletests(res["p_dir"].to_numpy(), method="holm")[1]))
    with open("reports/confirmatory.md", "w") as f:
        f.write("# Confirmatory tests (pre-registered, reports/prereg.md)\n\n")
        f.write("Play-level LMM, random intercept per player; REG season, non-nullified plays. Effect per 1 SD of trait.\n")
        f.write("p_dir = one-sided p in the pre-registered direction; Holm across the 6 tests.\n\n")
        f.write("| id | pos | outcome | trait | exp. | plays | players | β per SD | 95% CI | β / SD(y) | p_dir | p_holm |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|---|\n")
        for r in res.iter_rows(named=True):
            f.write(f"| {r['id']} | {r['pos']} | {r['outcome']} | {r['trait']} | {r['expected']} | {r['n_plays']} | {r['n_players']} | "
                    f"{r['beta']:.4f} | [{r['lo']:.4f}, {r['hi']:.4f}] | {r['beta'] / r['sd_y']:.3f} | {r['p_dir']:.4f} | {r['p_holm']:.4f} |\n")
    print(open("reports/confirmatory.md").read())


if __name__ == "__main__":
    main()
