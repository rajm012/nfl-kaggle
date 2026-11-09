"""Study 2 confirmatory tests F1-F3 (reports/prereg.md, Study 2, frozen 2026-10-29).

Run:  .venv/bin/python -m src.study2
Out:  reports/study2.md
"""
import warnings

import numpy as np
import polars as pl
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

from src.outcomes import BASE, TESTS, base_table, prep

warnings.filterwarnings("ignore")
INTERIM = "data/interim"
CONTEXT = {t[0]: t[4] for t in TESTS}
F_TESTS = [  # id, position, outcome, filter, context from Study 1 test, expected sign
    ("F1", "DL", "player_get_off", pl.col("player_get_off").is_not_null(), CONTEXT["D1"], -1),
    ("F2", "OL", "peak_pressure_probability_allowed", pl.col("peak_pressure_probability_allowed").is_not_null(), CONTEXT["O1"], -1),
    ("F3", "WR", "separation_at_pass_forward", pl.col("separation_at_pass_forward").is_not_null(), CONTEXT["W1"], +1),
]


def table() -> pl.DataFrame:
    sp = pl.read_parquet(f"{INTERIM}/sprint_traits.parquet").select("nfl_id", "A0")
    ten = pl.read_parquet(f"{INTERIM}/combine_results.parquet").select("nfl_id", "ten_yd_split")
    df = prep(base_table()).join(sp, on="nfl_id").join(ten, on="nfl_id")
    return df.with_columns(
        ten_missing=pl.col("ten_yd_split").is_null().cast(pl.Int8),
        ten_f=pl.col("ten_yd_split").fill_null(pl.col("ten_yd_split").median().over("combine_position")),
    ).with_columns(
        [((pl.col(c) - pl.col(c).mean().over("combine_position")) / pl.col(c).std().over("combine_position")).alias(f"{c}_z")
         for c in ("A0", "ten_f")]
    )


def main() -> None:
    df = table()
    rows = []
    for tid, pos, y, filt, extra, sign in F_TESTS:
        d = df.filter((pl.col("combine_position") == pos) & filt).to_pandas()
        base = BASE
        for ind in ("forty_missing", "udfa"):  # constant within the 40-tracked sample -> collinear with intercept
            if d[ind].nunique() < 2:
                base = base.replace(f" + {ind}", "")
        for label, ten in (("confirmatory (+10yd split)", " + ten_f_z" + (" + ten_missing" if d["ten_missing"].nunique() > 1 else "")), ("secondary (no 10yd split)", "")):
            fit = smf.mixedlm(f"{y} ~ A0_z + {base} + {extra}{ten}", d, groups=d["nfl_id"]).fit()
            assert fit.converged, f"{tid} {label} did not converge"
            b, se, p2 = fit.params["A0_z"], fit.bse["A0_z"], fit.pvalues["A0_z"]
            rows.append(dict(id=tid, model=label, pos=pos, outcome=y, n_plays=len(d), n_players=d["nfl_id"].nunique(),
                             beta=b, lo=b - 1.96 * se, hi=b + 1.96 * se, sd_y=d[y].std(),
                             p_dir=p2 / 2 if np.sign(b) == sign else 1 - p2 / 2))
    res = pl.DataFrame(rows)
    conf = res.filter(pl.col("model").str.starts_with("confirmatory"))
    holm = dict(zip(conf["id"], multipletests(conf["p_dir"].to_numpy(), method="holm")[1]))
    with open("reports/study2.md", "w") as f:
        f.write("# Study 2 — First Step (A0 from 40-yard sprint-curve fit)\n\n")
        f.write("Pre-registered in reports/prereg.md. Holm applies to the 3 confirmatory rows only.\n\n")
        f.write("| id | model | pos | outcome | plays | players | β per SD A0 | 95% CI | β/SD(y) | p_dir | p_holm |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
        for r in res.iter_rows(named=True):
            ph = f"{holm[r['id']]:.4f}" if r["model"].startswith("confirmatory") else "—"
            f.write(f"| {r['id']} | {r['model']} | {r['pos']} | {r['outcome']} | {r['n_plays']} | {r['n_players']} | {r['beta']:.4f} | "
                    f"[{r['lo']:.4f}, {r['hi']:.4f}] | {r['beta'] / r['sd_y']:.3f} | {r['p_dir']:.4f} | {ph} |\n")
    print(open("reports/study2.md").read())


if __name__ == "__main__":
    main()
