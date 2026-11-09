"""Frame-level kinematics shared by Combine and game tracking.

Provided `a` is the *unsigned magnitude* of total acceleration, so we rebuild a signed decomposition
from positions: a_lon (along the direction of travel: + speeding up, - braking) and a_lat (perpendicular:
turning / "cornering"; sign = left/right). Validated on Combine data: |a| from x,y vs provided `a`
r = 0.976; speed from x,y vs `s` r = 0.9995.
"""
import numpy as np
import polars as pl
from scipy.signal import savgol_filter

DT = 0.1  # 10 Hz
WINDOW, ORDER = 7, 2  # Savitzky-Golay: 0.7 s window, quadratic


def decompose(x: np.ndarray, y: np.ndarray) -> dict[str, np.ndarray]:
    """Smoothed speed, longitudinal and lateral acceleration (yd/s, yd/s^2) for one continuous track."""
    w = min(WINDOW, len(x) - (1 - len(x) % 2))  # odd window <= len
    if w <= ORDER:
        nan = np.full(len(x), np.nan)
        return {"sp": nan, "a_lon": nan, "a_lat": nan, "curv": nan, "hdg": nan}
    vx = savgol_filter(x, w, ORDER, deriv=1, delta=DT)
    vy = savgol_filter(y, w, ORDER, deriv=1, delta=DT)
    ax = savgol_filter(x, w, ORDER, deriv=2, delta=DT)
    ay = savgol_filter(y, w, ORDER, deriv=2, delta=DT)
    sp = np.hypot(vx, vy)
    safe = np.maximum(sp, 1e-6)
    a_lon = (vx * ax + vy * ay) / safe
    a_lat = (vx * ay - vy * ax) / safe
    # travel heading (radians, unwrapped so differences are continuous); unreliable when nearly stationary
    hdg = np.unwrap(np.arctan2(vy, vx))
    return {"sp": sp, "a_lon": a_lon, "a_lat": a_lat, "curv": a_lat / np.maximum(safe, 0.5) ** 2, "hdg": hdg}


def add_kinematics(df: pl.DataFrame, track_keys: list[str]) -> pl.DataFrame:
    """Append sp, a_lon, a_lat, curv to a frame table sorted by time within each track."""
    out = []
    for _, g in df.group_by(track_keys, maintain_order=True):
        k = decompose(g["x"].to_numpy(), g["y"].to_numpy())
        out.append(g.with_columns([pl.Series(n, v) for n, v in k.items()]))
    return pl.concat(out)
