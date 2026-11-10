"""Whole-game batching must preserve full-track smoothing and post-snap features."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import duckdb
import numpy as np
import pandas as pd
import polars as pl

from src import game_features


class GameBatchTests(unittest.TestCase):
    def test_batching_preserves_whole_track_results(self):
        rows = []
        for game in [100,101,102]:
            for player in [1,2]:
                for frame in range(45):
                    rows.append(dict(season=2023,game_id=game,play_id=7,nfl_id=player,
                                     time=pd.Timestamp('2023-09-01')+pd.Timedelta(seconds=frame*.1),
                                     x=frame*.15,y=player*np.sin(frame/8),
                                     event='ball_snap' if frame==10 else None))
        tracking = pd.DataFrame(rows)
        with tempfile.TemporaryDirectory() as temporary:
            tracking.to_parquet(Path(temporary)/'game_tracking.parquet',index=False)
            con = duckdb.connect()
            with patch.object(game_features,'INTERIM',temporary):
                full = game_features.season_traits(con,2023).sort(['game_id','nfl_id'])
                batched = pl.concat([game_features.season_traits(con,2023,[game])
                                     for game in [102,100,101]]).sort(['game_id','nfl_id'])
            con.close()
            self.assertEqual(full.height,6)
            np.testing.assert_array_equal(full.to_numpy(),batched.to_numpy())


if __name__=='__main__':
    unittest.main()
