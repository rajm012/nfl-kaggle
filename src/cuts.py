"""Cut (change-of-direction) detection and per-cut features, shared by Combine and game tracking.

A cut is a local peak of heading change over a short window, while the player is moving.
For each cut (t = peak frame):
  angle     : |heading(t+W) - heading(t-W)| in degrees (W = 0.5 s)
  v_in      : max speed in the 1.0 s before t
  v_min     : min speed within t +/- 0.5 s
  v_out     : speed 1.0 s after t
  retain    : v_min / v_in   (speed kept through the cut)
  recover_s : time after the v_min frame to regain 90% of v_in (NaN if not within 2 s)
"""
import numpy as np
import polars as pl
from scipy.signal import find_peaks

from src.kinematics import decompose

HZ = 10
W = 5  # frames (0.5 s) half-window for heading change
MIN_ANGLE = 40.0  # degrees
MIN_SPEED_IN = 2.0  # yd/s: ignore direction changes from near-standstill (heading is noise there)


def detect_cuts(x: np.ndarray, y: np.ndarray) -> list[dict]:
    n = len(x)
    if n < 2 * W + HZ + 1:
        return []
    k = decompose(x, y)
    sp, hdg = k["sp"], k["hdg"]
    dh = np.full(n, 0.0)
    dh[W:-W] = np.degrees(np.abs(hdg[2 * W:] - hdg[:-2 * W]))
    peaks, _ = find_peaks(dh, height=MIN_ANGLE, distance=HZ)  # >= 1 s apart
    cuts = []
    for t in peaks:
        lo_in = max(0, t - HZ)
        v_in = sp[lo_in:t + 1].max()
        if v_in < MIN_SPEED_IN:
            continue
        win = slice(max(0, t - W), min(n, t + W + 1))
        i_min = win.start + int(np.argmin(sp[win]))
        v_min = sp[i_min]
        t_out = t + HZ
        v_out = sp[t_out] if t_out < n else np.nan
        after = np.nonzero(sp[i_min:min(n, i_min + 2 * HZ + 1)] >= 0.9 * v_in)[0]
        recover = after[0] / HZ if len(after) else np.nan
        cuts.append({
            "frame": int(t), "angle": float(min(dh[t], 180.0)), "v_in": float(v_in), "v_min": float(v_min),
            "v_out": float(v_out), "retain": float(v_min / v_in), "recover_s": float(recover),
        })
    return cuts


def cuts_table(frames: pl.DataFrame, track_keys: list[str]) -> pl.DataFrame:
    """Run detect_cuts on every track (frames must be time-sorted within track). Returns one row per cut."""
    rows = []
    for key, g in frames.group_by(track_keys, maintain_order=True):
        for c in detect_cuts(g["x"].to_numpy(), g["y"].to_numpy()):
            rows.append(dict(zip(track_keys, key)) | c)
    return pl.DataFrame(rows)
