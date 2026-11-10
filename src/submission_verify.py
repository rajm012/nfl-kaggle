"""Verify rebuilt headline results and all frozen athlete scores against the review record."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.evaluate import paired_metrics, provenance

ROOT = Path(__file__).resolve().parents[1]


def selected_values(root):
    def read(name):
        return json.loads((root/'reports'/(name+'.json')).read_text())
    validation, audit = read('validation'), read('model_audit')
    measurement, reliability, transfer = read('study3_measurement'), read('reliability'), read('transfer_audit')
    cone = read('cone_sensitivity')
    result = {'counts':{'primary_association_significant':audit['primary_two_sided_holm_significant'],
                         'binary_sensitivity_significant':audit['binary_cluster_sensitivity_holm_significant'],
                         'route_development_players':measurement['development_players'],
                         'route_development_plays':measurement['development_plays']},
              'screen_passes':measurement['screen_passes'], 'prediction':{},'measurement':{},
              'reliability':{},'transfer':{},'association':{},'cone':{}}
    for r in validation['results']:
        result['prediction'][r['id']] = {k:r['metrics'][k] for k in [
            'players','rmse0','rmse1','improvement','improvement_lo','improvement_hi','simultaneous_lo','simultaneous_hi']}
    for r in measurement['diagnostic']:
        result['measurement'][r['contrast']] = {k:r[k] for k in ['n','r','SB','SB_lo','SB_hi']}
    for r in reliability['cross_drill']:
        if r['position']=='WR' and r['feature'] in ['lat','TURN']:
            result['reliability'][r['sample']+'/'+r['feature']] = {k:r[k] for k in ['n','SB','SB_lo','SB_hi']}
    for r in transfer['rows']:
        if r['scope']=='corrected, PRE+REG' and (r['position'],r['trait']) in [('WR','lat'),('DL','burst')]:
            result['transfer'][r['position']+'/'+r['adjustment']] = {k:r[k] for k in ['n','r','lo','hi']}
    for r in audit['models']:
        key = r['id']+'/'+r['method']+'/'+r['model']
        result['association'][key] = {k:r[k] for k in ['players','fitted_plays','beta','lo','hi']}
    for r in cone['comparisons']:
        result['cone'][r['id']] = {'players':r['players']}
        for name in ['baseline_tracking','baseline_cone_tracking']:
            # Names are retained exactly as recorded in the original artifact.
            if name in r['models']:
                interval = r['models'][name]['coefficient_intervals']
                trait = 'A0_z' if r['study']==2 else ('lat_z' if r['id'] in ['W1','O1','D2'] else 'burst_z')
                result['cone'][r['id']][name] = interval[trait]
    return result


def compare(expected, actual, path='', checks=None):
    checks = [] if checks is None else checks
    if isinstance(expected,dict):
        if set(expected)!=set(actual):
            raise AssertionError(f'{path}: different fields')
        for key,value in expected.items():
            compare(value,actual[key],path+'/'+str(key),checks)
    elif isinstance(expected,(float,int)) and not isinstance(expected,bool):
        # Numerical reproduction tolerance only; never a model/claim selection rule.
        if not np.isclose(expected,actual,rtol=2e-4,atol=2e-6):
            raise AssertionError(f'{path}: recorded {expected}, rebuilt {actual}')
        checks.append(path)
    elif expected != actual:
        raise AssertionError(f'{path}: recorded {expected}, rebuilt {actual}')
    return checks


def main():
    expected = json.loads((ROOT/'reports/reference_headlines.json').read_text())
    checks = compare(expected,selected_values(ROOT))
    development = json.loads((ROOT/'reports/evaluation_development.json').read_text())
    validation = json.loads((ROOT/'reports/validation.json').read_text())
    if development['provenance']!=provenance():
        raise AssertionError('Frozen source or rebuilt inputs changed after development')
    if validation['evaluation_players_fitted'] or development['evaluation_players_fitted']:
        raise AssertionError('Evaluation player effects were fitted')
    if development['frozen_utc']>=validation['generated_utc']:
        raise AssertionError('Evaluation preceded development freeze')
    scores = pd.read_parquet(ROOT/'data/interim/evaluation_player_scores.parquet')
    verified = []
    for r in validation['results']:
        model = next(m for m in development['models'] if m['spec']['id']==r['id'])
        subset = scores[scores.test==r['id']]
        if set(subset.nfl_id)&set(model['training_player_ids']):
            raise AssertionError(r['id']+': athlete overlap')
        metrics = paired_metrics(subset,family_size=r['metrics']['family_size'])
        for key in ['rmse0','rmse1','improvement','improvement_lo','improvement_hi']:
            np.testing.assert_allclose(metrics[key],r['metrics'][key],rtol=1e-10,atol=1e-12)
        np.testing.assert_allclose(subset.error0,subset.observed_adjusted-subset.baseline_adjusted,atol=1e-12)
        np.testing.assert_allclose(subset.error1,subset.observed_adjusted-subset.augmented_adjusted,atol=1e-12)
        verified.append(r['id'])
    result = {'headline_numeric_checks':len(checks),'comparisons_verified':verified,
              'raw_input_rebuild':True,'frozen_hashes_match':True,'no_player_overlap':True,
              'no_evaluation_player_effects':True,'reference_results_used_for_fitting':False,
              'relative_tolerance':2e-4,'absolute_tolerance':2e-6}
    (ROOT/'reports/submission_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
