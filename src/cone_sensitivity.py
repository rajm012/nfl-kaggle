"""Same-row historical 3-cone sensitivity; no invented cone times.

Run after cohort development is frozen: python -m src.cone_sensitivity
Keeps prior all-REG models separate from rookie-only cohort prediction.
"""
from datetime import datetime, timezone
import json

import numpy as np
import pandas as pd
import patsy
import polars as pl

from src.audit_data import markdown_table
from src.evaluate import ROOT, fit_model
from src.outcomes import BASE, TESTS, base_table, prep
from src.route_context import independent_columns
from src.study2 import F_TESTS
from src.validation import study2_player_table


def availability():
    path = ROOT/'data/interim'
    p = pd.read_parquet(path/'combine_results.parquet',columns=[
        'nfl_id','draft_year','combine_position','three_cone','forty','combine_weight','combine_height'])
    p = p.merge(pd.read_parquet(path/'players.parquet',columns=['nfl_id','draft_overall_pick']),
                validate='one_to_one')
    p = p[p.combine_position.isin(['WR','OL','DL'])].copy()
    p['cone_recorded'] = p.three_cone.notna()
    p['draft_status'] = np.where(p.draft_overall_pick.isna(),'UDFA','drafted')
    classes = p.groupby(['combine_position','draft_year']).agg(
        players=('nfl_id','size'),cone_recorded=('cone_recorded','sum')).reset_index()
    status = p.groupby(['combine_position','draft_status']).agg(
        players=('nfl_id','size'),cone_recorded=('cone_recorded','sum')).reset_index()
    profiles = p.groupby(['combine_position','cone_recorded']).agg(
        players=('nfl_id','size'),median_weight=('combine_weight','median'),
        median_forty=('forty','median'),median_pick_drafted=('draft_overall_pick','median'),
        UDFA_fraction=('draft_status',lambda s:(s=='UDFA').mean())).reset_index()
    return p,dict(by_class=classes.to_dict('records'),by_draft_status=status.to_dict('records'),
                  descriptive_profiles=profiles.to_dict('records'))


def fit_comparison(d, formula, trait):
    # Determine all retained rows using the fullest specification first; every
    # nested model shares this row mask, observed cone values and player groups.
    y, full = patsy.dmatrices(formula,d,return_type='dataframe',NA_action='drop')
    retained = d.loc[full.index]
    baseline_cols = [name for name in full if name not in ['cone_z',trait]]
    ordered = full[baseline_cols+['cone_z',trait]]
    reduced,dropped = independent_columns(ordered,np.ones(len(full)))
    if trait not in reduced or 'cone_z' not in reduced:
        raise ValueError('Cone/trait not estimable on same rows')
    candidates = {
        'baseline': [c for c in reduced if c not in [trait,'cone_z']],
        'baseline_tracking': [c for c in reduced if c!='cone_z'],
        'baseline_cone': [c for c in reduced if c!=trait],
        'baseline_cone_tracking': list(reduced),
    }
    outcome = y.columns[0]
    binary = outcome in ['pressure_i','pressure_allowed_i']
    models = {name:fit_model(y.iloc[:,0].to_numpy(float),reduced[columns],retained.nfl_id,binary)
              for name,columns in candidates.items()}
    return dict(candidate_plays=len(d),fitted_plays=len(retained),players=int(retained.nfl_id.nunique()),
        players_by_class=retained.groupby('draft_year').nfl_id.nunique().to_dict(),
        dropped_missing=len(d)-len(retained),dropped_redundant_columns=dropped,
        identical_row_mask=True,models=models,trait_without_cone=models['baseline_tracking']['coefficient_intervals'][trait],
        trait_with_cone=models['baseline_cone_tracking']['coefficient_intervals'][trait],
        cone_with_tracking=models['baseline_cone_tracking']['coefficient_intervals']['cone_z'])


def main():
    # Require a completed development snapshot. No prediction models are tuned
    # using these full-cohort sensitivity fits.
    if not (ROOT/'reports/evaluation_development.json').exists():
        raise RuntimeError('Freeze development before opening full-cohort sensitivity outcomes')
    p,support = availability()
    frame = prep(base_table()).join(pl.from_pandas(p[['nfl_id','draft_year','three_cone']]),on='nfl_id').to_pandas()
    observed = p[p.three_cone.notna()].copy()
    moments = observed.groupby('combine_position').three_cone.agg(['mean','std','count'])
    frame['cone_z'] = ((frame.three_cone-frame.combine_position.map(moments['mean']))
                      / frame.combine_position.map(moments['std']))
    sprint,_ = study2_player_table()
    frame2 = frame.merge(sprint,validate='many_to_one')
    rows = []
    for tid,pos,y,filt,extra,trait,sign in TESTS:
        pl_frame = pl.from_pandas(frame)
        selected = pl_frame.filter((pl.col('combine_position')==pos)&filt&pl.col('three_cone').is_not_null()).to_pandas()
        all_outcome = pl_frame.filter((pl.col('combine_position')==pos)&filt)
        formula = f'{y} ~ {BASE} + {extra} + cone_z + {trait}_z'
        result = fit_comparison(selected,formula,trait+'_z')
        rows.append(dict(id=tid,position=pos,study=1,outcome=y,
            outcome_players_without_cone_restriction=all_outcome['nfl_id'].n_unique(),**result))
        print(f"Cone {tid}: {result['players']} players, {result['fitted_plays']:,} identical rows; "
              f"tracking beta={result['trait_with_cone']['beta']:+.5f}",flush=True)
    for tid,pos,y,filt,extra,sign in F_TESTS:
        all_outcome = frame2[(frame2.combine_position==pos)&frame2[y].notna()]
        selected = all_outcome[all_outcome.three_cone.notna()].copy()
        formula = f'{y} ~ {BASE} + {extra} + ten_f_z + ten_missing + cone_z + A0_z'
        result = fit_comparison(selected,formula,'A0_z')
        rows.append(dict(id=tid,position=pos,study=2,outcome=y,
                         outcome_players_without_cone_restriction=int(all_outcome.nfl_id.nunique()),**result))
        print(f"Cone {tid}: {result['players']} players, {result['fitted_plays']:,} identical rows; "
              f"tracking beta={result['trait_with_cone']['beta']:+.5f}",flush=True)
    result = dict(generated_utc=datetime.now(timezone.utc).isoformat(),comparisons=rows,
                  availability=support,cone_reference=moments.reset_index().to_dict('records'),
                  historical_all_REG=True,cone_times_imputed=False)
    (ROOT/'reports/cone_sensitivity.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    display = []
    for r in rows:
        before,after = r['trait_without_cone'],r['trait_with_cone']
        display.append(dict(test=r['id'],outcome_players=r['outcome_players_without_cone_restriction'],
            cone_players=r['players'],plays=r['fitted_plays'],
            beta_without_cone=round(before['beta'],5),ci_without=f"[{before['lo']:.5f}, {before['hi']:.5f}]",
            beta_with_cone=round(after['beta'],5),ci_with=f"[{after['lo']:.5f}, {after['hi']:.5f}]"))
    text = '# Same-sample 3-cone sensitivity\n\n'
    text += f"Generated UTC: {result['generated_utc']}. Recorded cone times only; no imputation.\n\n"
    text += markdown_table(display)
    text += '\n## Support and selection\n\n'+markdown_table(support['by_class'])+'\n'+markdown_table(support['by_draft_status'])
    text += '\n'+markdown_table(support['descriptive_profiles'])
    text += '\n## Interpretation and method\n\n'
    text += 'These secondary association fits use all available REG non-nullified plays '
    text += 'and include all cohorts, preserving the historical analysis window. They are '
    text += 'separate from the frozen rookie-season cohort prediction models; no prediction '
    text += 'coefficients are changed using these results. Every comparison uses identical '
    text += 'players/plays for baseline, baseline+tracking, baseline+cone and baseline+cone+tracking. '
    text += 'Intervals are two-sided, normal-reference LMM for continuous outcomes and '
    text += 'player-clustered finite-sample t for binary LPM. This is not a new confirmatory family.\n\n'
    text += 'Trait scaling retains the historical player-level definitions and the audited '
    text += 'unique-player Study 2 preprocessing. Cone SD is calculated from unique cone-observed '
    text += 'athletes within position. No missing times are fabricated. Exact retained samples, '
    text += 'rank removals, numerical retry warnings and all nested coefficients are saved in JSON. '
    text += 'Small selected samples can yield wide intervals; no universal incremental ranking '
    text += 'claim follows. Cohort cone-subset prediction appears separately in `validation.md`.\n'
    (ROOT/'reports/cone_sensitivity.md').write_text(text)
    print('Saved reports/cone_sensitivity.md',flush=True)


if __name__=='__main__':
    main()
