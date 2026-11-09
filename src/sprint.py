"""Sprint-curve fit on Combine 40-yard dash tracking (Study 2 exposure, reports/prereg.md).

Run:  .venv/bin/python -m src.sprint
Out:  data/interim/sprint_attempts.parquet, data/interim/sprint_traits.parquet

Model: v(t) = vmax * (1 - exp(-(t - t0)/tau)), fitted from movement onset (speed >= 0.5 yd/s) to end of run.
A0 = vmax / tau = initial acceleration capacity (yd/s^2).
"""
import numpy as np
import polars as pl
from scipy.optimize import curve_fit

INTERIM = "data/interim"
ONSET_SPEED = 0.5


def model(t, vmax, tau, t0):
    return np.where(t > t0, vmax * (1 - np.exp(-(t - t0) / tau)), 0.0)


def fit_attempt(s: np.ndarray) -> dict | None:
    on = np.flatnonzero(s >= ONSET_SPEED)
    if len(on) == 0:
        return None
    seg = s[on[0]:]
    if len(seg) < 20:
        return None
    t = np.arange(len(seg)) * 0.1
    try:
        (vmax, tau, t0), _ = curve_fit(model, t, seg, p0=(seg.max(), 1.0, 0.0),
                                       bounds=([3, 0.2, -0.3], [14, 4.0, 0.3]), maxfev=5000)
    except RuntimeError:
        return None
    rmse = float(np.sqrt(np.mean((model(t, vmax, tau, t0) - seg) ** 2)))
    return {"vmax": vmax, "tau": tau, "t0": t0, "A0": vmax / tau, "rmse": rmse, "n": len(seg)}


def main() -> None:
    ct = (
        pl.scan_parquet(f"{INTERIM}/combine_tracking.parquet")
        .filter((pl.col("entity_type") == "PLAYER") & (pl.col("drill_type") == "FORTY_YARD_DASH"))
        .sort("event_id", "time").collect()
    )
    rows = []
    for (eid, pid, att), g in ct.group_by(["event_id", "nfl_id", "attempt"], maintain_order=True):
        r = fit_attempt(g["s"].to_numpy())
        if r:
            rows.append({"event_id": eid, "nfl_id": pid, "attempt": att} | r)
    a = pl.DataFrame(rows)
    a.write_parquet(f"{INTERIM}/sprint_attempts.parquet")
    traits = a.group_by("nfl_id").agg(pl.col("A0", "vmax", "tau").mean(), pl.len().alias("n_attempts"))
    traits.write_parquet(f"{INTERIM}/sprint_traits.parquet")
    print(a.select("vmax", "tau", "A0", "rmse").describe())
    print("players:", traits.height)


if __name__ == "__main__":
    main()
