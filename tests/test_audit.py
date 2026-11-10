"""Statistical invariants: reference leakage, row weights, rank and missing groups."""
import unittest

import numpy as np
import pandas as pd

from src.reliability import paired_reliability, training_turn
from src.route_context import baseline_design, independent_columns, preprocess_development
from src.validation import fit_one


class AuditTests(unittest.TestCase):
    def test_evaluation_exposures_cannot_change_training_reference(self):
        players = pd.DataFrame({'nfl_id':[1,2,3,4], 'draft_year':[2023,2024,2023,2025]})
        attempts = pd.DataFrame({'nfl_id':[1,2,3,4,1,2,3,4,4],
            'drill':['A']*4+['B']*4+['UNSEEN'], 'lat':[1,2,4,100,3,7,6,500,800]})
        original,ref = training_turn(attempts,players)
        attempts.loc[attempts.nfl_id==4,'lat'] *= -900
        changed,ref2 = training_turn(attempts,players)
        self.assertEqual(ref,ref2)
        self.assertEqual(ref['unseen_drills'],['UNSEEN'])
        pd.testing.assert_frame_equal(original[original.nfl_id!=4],changed[changed.nfl_id!=4])

    def test_player_scalers_ignore_opportunity_and_evaluation_players(self):
        reference = pd.DataFrame({'nfl_id':[1,2,3,4], 'combine_position':['WR']*4,
            'draft_year':[2023,2024,2024,2025], 'draft_overall_pick':[20,50,np.nan,1],
            'forty':[4.4,np.nan,4.6,9], 'combine_weight':[180,200,220,999],
            'combine_height':[70,72,74,100], 'TURN':[0,1,3,200]})
        dev = reference.iloc[:3].copy()
        dev['cushion'] = [2,4,3]
        dev['in_motion_at_ball_snap'] = False
        dev['route_ran'] = ['GO','OUT','SLANT']
        dev['down'] = 1
        dev['team_coverage_man_zone'] = 'ZONE'
        dev['receiver_alignment'] = 'WIDE'
        _,meta = preprocess_development(dev.copy(),reference.copy())
        duplicate = pd.concat([dev,dev.iloc[[0]*100]],ignore_index=True)
        reference.loc[reference.draft_year==2025,'TURN'] = -99999
        _,meta2 = preprocess_development(duplicate,reference)
        self.assertEqual(meta['player_scalers'],meta2['player_scalers'])
        self.assertAlmostEqual(meta['median_forty'],4.5)
        self.assertEqual(meta['reference_players'],3)

    def test_rank_rule_preserves_predictions_and_equal_family_weights(self):
        d = pd.DataFrame({'nfl_id':[1]*7+[2]*7, 'BREAK':[0]*2+[1]*5+[0]*5+[1]*2})
        d['route_ran'] = np.where(d.BREAK==0,'GO','OUT')
        d['down'] = '1'
        d['team_coverage_man_zone'] = 'ZONE'
        d['receiver_alignment'] = 'WIDE'
        d['yards_to_go'] = np.arange(14)
        for col in ['motion','cushion_f','cushion_missing','weight_z','height_z',
                    'forty_z','pick_z','udfa','forty_missing']:
            d[col] = 0
        meta = {'categories':{k:sorted(d[k].unique()) for k in
            ['route_ran','down','team_coverage_man_zone','receiver_alignment']}}
        x,weights,dropped = baseline_design(d,meta)
        totals = weights.groupby([d.nfl_id,d.BREAK]).sum()
        np.testing.assert_allclose(totals,np.ones(4))
        self.assertIn('udfa:BREAK',dropped)
        original = pd.DataFrame({'Intercept':np.ones(5),'a':np.arange(5),
                                  'redundant':2*np.arange(5),'zero':np.zeros(5)})
        reduced,_ = independent_columns(original,np.ones(5))
        y = np.array([3,4,8,11,12])
        old = original.to_numpy()@np.linalg.lstsq(original,y,rcond=None)[0]
        new = reduced.to_numpy()@np.linalg.lstsq(reduced,y,rcond=None)[0]
        np.testing.assert_allclose(old,new)

    def test_missing_formula_rows_use_retained_player_groups(self):
        rng = np.random.default_rng(8)
        d = pd.DataFrame({'nfl_id':np.repeat(np.arange(12),5), 'x':rng.normal(size=60)})
        d['y'] = .4*d.x+rng.normal(size=60)
        d.loc[[0,8,19],'x'] = np.nan
        spec = dict(id='SYNTH',study=0,model='test',position='WR',outcome='y',
                    coefficient='x',sign=1,filter=np.ones(len(d),bool),formula='y ~ x')
        fit = fit_one(spec,d,'player-clustered LPM sensitivity')
        self.assertEqual(fit['fitted_plays'],57)
        self.assertEqual(fit['players'],12)
        self.assertEqual(fit['cluster_t_df'],11)
        self.assertEqual(fit['dropped_missing_plays'],3)

    def test_bootstrap_keeps_negative_and_degenerate_reliability(self):
        r = paired_reliability(np.arange(8),[7,6,5,4,3,2,1,.2],n_boot=100)
        self.assertLess(r['r'],0)
        self.assertLess(r['SB'],0)
        self.assertIsNone(paired_reliability(np.ones(8),np.arange(8))['r'])


if __name__=='__main__':
    unittest.main()
