"""Meaningful prediction invariants using synthetic athletes and held-out data."""
import unittest

import numpy as np
import pandas as pd

from src.evaluate import (design, fit_preprocessing, paired_metrics, scores,
                          select_sample, training_traits, transform)


def synthetic_players():
    return pd.DataFrame(dict(nfl_id=[1,2,3,4,5],draft_year=[2023,2023,2024,2024,2025],
        combine_position=['OL']*5,forty=[5.1,5.3,np.nan,5.0,12],
        ten_yd_split=[1.7,1.9,1.8,1.6,8],draft_overall_pick=[10,80,np.nan,150,1],
        combine_weight=[290,310,330,300,999],combine_height=[74,76,75,73,100],
        lat=[-.5,.3,.8,-.2,100],burst=[.3,.7,-.2,-.6,-100],A0=[4,5,7,6,80],
        three_cone=[7.4,7.8,np.nan,7.5,np.nan]))


def synthetic_plays(ids=(1,2,3,4),season=None):
    ids = list(ids)
    n = len(ids)*4
    frame = pd.DataFrame(dict(nfl_id=np.repeat(ids,4),game_id=np.arange(n),play_id=np.arange(n),
        draft_year=np.repeat([2023 if i<3 else 2024 if i<5 else 2025 for i in ids],4),
        season=np.repeat([season or (2023 if i<3 else 2024 if i<5 else 2025) for i in ids],4),
        down=np.tile([1,2,1,3],len(ids)),yards_to_go=np.tile([10,3,6,12],len(ids)),
        route_ran=None,cushion=np.nan,team_coverage_man_zone=None,receiver_alignment=None,
        in_motion_at_ball_snap=False,blitzing=False,lined_up_position='G',
        dropback_duration=2.5,pass_rushers_encountered=1,
        pressure_allowed_i=np.tile([0,1,0,0],len(ids)),sack=np.nan))
    return frame


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.spec = dict(position='OL',outcome='pressure_allowed_i',traits=['lat'],
                         study=1,ten_split=False,cone=False)
        self.players = synthetic_players()
        self.d,_ = select_sample(synthetic_plays(),self.players,self.spec)
        self.meta = fit_preprocessing(self.d,self.players,self.spec)

    def test_training_preprocessing_ignores_heldout_extremes_and_play_counts(self):
        changed = self.players.copy()
        changed.loc[changed.draft_year==2025,['forty','lat','combine_weight']] = -9999
        duplicated = pd.concat([self.d,self.d[self.d.nfl_id==1]],ignore_index=True)
        meta2 = fit_preprocessing(duplicated,changed,self.spec)
        self.assertEqual(self.meta['player_medians'],meta2['player_medians'])
        self.assertEqual(self.meta['player_scalers'],meta2['player_scalers'])
        self.assertAlmostEqual(self.meta['player_medians']['forty'],5.1)
        self.assertEqual(self.meta['player_reference_n'],4)

    def test_unknown_calendar_year_uses_frozen_latest_training_level(self):
        held,_ = select_sample(synthetic_plays(ids=[5],season=2025),self.players,self.spec)
        transformed, logs = transform(held,self.meta)
        self.assertEqual(set(transformed.season),{'2024'})
        self.assertEqual(logs['unknown_categories']['season'],{'2025':4})
        x0,x1 = design(transformed,self.meta,self.spec)
        self.assertEqual(len(x0),4)
        self.assertIn('lat_z',x1)

    def test_outcomes_and_unknown_player_id_cannot_affect_fixed_predictions(self):
        held,_ = select_sample(synthetic_plays(ids=[5]),self.players,self.spec)
        transformed,_ = transform(held,self.meta)
        x0,x1 = design(transformed,self.meta,self.spec)
        model = dict(spec=self.spec,preprocessing=self.meta,columns0=list(x0),columns1=list(x1),
            context_columns=['yards_to_go'],
            baseline={'coefficients':{c:(.2 if c=='Intercept' else .01) for c in x0}},
            augmented={'coefficients':{c:(.2 if c=='Intercept' else .01) for c in x1}})
        before,_ = scores(held,model)
        held['pressure_allowed_i'] = 700
        held['nfl_id'] = 99999
        after,_ = scores(held,model)
        np.testing.assert_allclose(before[['baseline','augmented']],after[['baseline','augmented']])
        self.assertNotEqual(before.observed.iloc[0],after.observed.iloc[0])
        np.testing.assert_allclose(before.error0,before.observed_adjusted-before.baseline_adjusted)

    def test_cone_rows_never_impute_missing_times(self):
        cone_spec = dict(self.spec,cone=True)
        subset,attrition = select_sample(synthetic_plays(),self.players,cone_spec)
        self.assertNotIn(3,subset.nfl_id.tolist())
        self.assertEqual(attrition['players'],3)
        self.assertTrue(subset.three_cone.notna().all())

    def test_scoring_has_equal_athlete_weight_and_preserves_gain_sign(self):
        table = pd.DataFrame(dict(error0=[1,3,2],error1=[.5,1.5,1],plays=[1,1000,7]))
        metric = paired_metrics(table,n_boot=200,family_size=6)
        self.assertAlmostEqual(metric['rmse0'],np.sqrt(14/3))
        self.assertGreater(metric['improvement_lo'],0)
        changed = table.assign(plays=[10000,1,1])
        self.assertEqual(metric,paired_metrics(changed,n_boot=200,family_size=6)|
                         {'min_plays':metric['min_plays'],'median_plays':metric['median_plays'],
                          'max_plays':metric['max_plays']})
        self.assertGreaterEqual(metric['improvement_lo'],metric['simultaneous_lo'])

    def test_both_drill_features_ignore_2025_reference_values(self):
        p = self.players[['nfl_id','draft_year']]
        a = pd.DataFrame(dict(nfl_id=[1,2,3,4,5],drill=['A']*5,
                              lat=[1,2,3,4,500],burst=[4,3,2,1,-600]))
        old,ref = training_traits(a,p)
        a.loc[a.nfl_id==5,['lat','burst']] = 99999
        new,ref2 = training_traits(a,p)
        self.assertEqual(ref,ref2)
        pd.testing.assert_frame_equal(old[old.nfl_id!=5],new[new.nfl_id!=5])


if __name__=='__main__':
    unittest.main()
