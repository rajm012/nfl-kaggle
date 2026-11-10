"""Audit Studies 1–2 with actual fitted samples and corrected uncertainty/scaling.

Run: .venv/bin/python -m src.validation
Writes separate reports/model_audit.{md,json} and one checkpoint per fitted model.
Historical numerical reports are never overwritten. No new hypothesis family.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import warnings

import numpy as np
import pandas as pd
import patsy
import polars as pl
from scipy.stats import norm, t
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

from src.audit_data import markdown_table
from src.outcomes import BASE, TESTS, base_table, prep
from src.route_context import independent_columns
from src.study2 import F_TESTS

ROOT = Path(__file__).resolve().parents[1]


def study2_player_table():
    path = ROOT/'data/interim'
    p = pd.read_parquet(path/'sprint_traits.parquet', columns=['nfl_id','A0'])
    p = p.merge(pd.read_parquet(path/'combine_results.parquet',
               columns=['nfl_id','combine_position','ten_yd_split']),validate='one_to_one')
    p['ten_missing'] = p.ten_yd_split.isna().astype(int)
    p['ten_f'] = p.ten_yd_split.fillna(p.groupby('combine_position').ten_yd_split.transform('median'))
    metadata = []
    for feature in ['A0','ten_f']:
        stats = p.groupby('combine_position')[feature].agg(['mean','std','count'])
        for pos, row in stats.iterrows():
            metadata.append(dict(position=pos,feature=feature,**row.to_dict()))
        p[f'{feature}_z'] = ((p[feature]-p.groupby('combine_position')[feature].transform('mean'))
                              / p.groupby('combine_position')[feature].transform('std'))
    return p.drop(columns='combine_position'), metadata


def fit_one(spec, frame, method):
    started = time.monotonic()
    d = frame.loc[spec['filter']].copy()
    formula = spec['formula']
    y, x = patsy.dmatrices(formula,d,return_type='dataframe',NA_action='drop')
    fitted = d.loc[x.index]
    x, dropped = independent_columns(x,np.ones(len(x)))
    name = spec['coefficient']
    if name not in x:
        raise ValueError(f"{spec['id']}: exposure is not estimable")
    captured = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        if method=='LMM':
            fit = sm.MixedLM(y.iloc[:,0],x,groups=fitted.nfl_id).fit()
            if not fit.converged:
                raise RuntimeError(f"{spec['id']}: MixedLM failed to converge")
            beta,se = float(fit.params[name]),float(fit.bse[name])
            p_two = float(2*norm.sf(abs(beta/se)))
            critical = norm.ppf(.975)
            df_ref = None
        else:
            fit = sm.OLS(y.iloc[:,0],x).fit(cov_type='cluster',
                cov_kwds={'groups':fitted.nfl_id.to_numpy(),'use_correction':True},use_t=True)
            beta,se = float(fit.params[name]),float(fit.bse[name])
            df_ref = int(fitted.nfl_id.nunique()-1)
            p_two = float(2*t.sf(abs(beta/se),df_ref))
            critical = t.ppf(.975,df_ref)
        captured = sorted(set(str(w.message) for w in caught))
    if not np.isfinite(se) or se<=0:
        raise RuntimeError(f"{spec['id']}: invalid coefficient uncertainty")
    p_dir = p_two/2 if np.sign(beta)==spec['sign'] else 1-p_two/2
    controls = []
    for feature in ['combine_weight_z','combine_height_z','pick_z','forty_z']:
        if feature in x:
            b,s = float(fit.params[feature]),float(fit.bse[feature])
            controls.append(dict(feature=feature,beta=b,lo=float(b-critical*s),hi=float(b+critical*s)))
    return dict(id=spec['id'],study=spec['study'],model=spec['model'],method=method,
                position=spec['position'],outcome=spec['outcome'],coefficient=name,
                candidate_plays=len(d),fitted_plays=len(x),dropped_missing_plays=len(d)-len(x),
                players=int(fitted.nfl_id.nunique()),design_rank=x.shape[1],
                dropped_redundant_columns=dropped,beta=beta,lo=float(beta-critical*se),
                hi=float(beta+critical*se),se=se,p_two=p_two,p_dir_historical=p_dir,
                cluster_t_df=df_ref,converged=True,warnings=captured,controls=controls,
                seconds=round(time.monotonic()-started,2),formula=formula)


def main():
    reports = ROOT/'reports'
    checkpoint = reports/'model_audit_checkpoints'
    checkpoint.mkdir(exist_ok=True)
    frame = prep(base_table()).to_pandas()
    sp, scalers = study2_player_table()
    frame2 = frame.merge(sp,validate='many_to_one')
    specifications = []
    pl_frame = pl.from_pandas(frame)
    for tid,pos,y,filt,extra,trait,sign in TESTS:
        selected = pl_frame.filter((pl.col('combine_position')==pos)&filt)
        # Convert the Polars filter to explicit key membership, avoiding expression duplication.
        selected_keys = pd.MultiIndex.from_frame(selected.select('game_id','play_id','nfl_id').to_pandas())
        mask = pd.MultiIndex.from_frame(frame[['game_id','play_id','nfl_id']]).isin(selected_keys)
        spec = dict(id=tid,study=1,model='original specification',position=pos,outcome=y,
                    coefficient=f'{trait}_z',sign=sign,filter=mask,
                    formula=f'{y} ~ {trait}_z + {BASE} + {extra}')
        specifications.append((spec,frame,'LMM'))
        if tid in ['O1','O2','D2']:
            specifications.append((spec,frame,'player-clustered LPM sensitivity'))
    for tid,pos,y,filt,extra,sign in F_TESTS:
        mask = (frame2.combine_position==pos)&frame2[y].notna()
        for model,ten in [('confirmatory, player SDs',' + ten_f_z + ten_missing'),
                          ('secondary, player SDs','')]:
            spec = dict(id=tid,study=2,model=model,position=pos,outcome=y,
                        coefficient='A0_z',sign=sign,filter=mask,
                        formula=f'{y} ~ A0_z + {BASE} + {extra}{ten}')
            specifications.append((spec,frame2,'LMM'))
    rows = []
    for spec,d,method in specifications:
        # Always refit on invocation. Checkpoints make partial progress reviewable;
        # cached coefficients are not silently accepted after source changes.
        result = fit_one(spec,d,method)
        key = f"{spec['id']}_{'primary' if spec['model'].startswith(('original','confirmatory')) else 'secondary'}_{'lmm' if method=='LMM' else 'cluster'}"
        (checkpoint/f'{key}.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        rows.append(result)
        print(f"{key}: n={result['fitted_plays']:,}/{result['players']} players; "
              f"beta={result['beta']:.5f} [{result['lo']:.5f},{result['hi']:.5f}]; "
              f"p(two)={result['p_two']:.4f}; {result['seconds']}s",flush=True)
    families = [[r for r in rows if r['study']==1 and r['method']=='LMM'],
                [r for r in rows if r['study']==2 and r['model'].startswith('confirmatory')],
                [r for r in rows if r['method']!='LMM']]
    for family in families:
        for r,p in zip(family,multipletests([r['p_two'] for r in family],method='holm')[1]):
            r['p_two_holm'] = float(p)
    result = dict(generated_utc=datetime.now(timezone.utc).isoformat(),models=rows,
                  study2_player_scalers=scalers,all_converged=True,
                  primary_two_sided_holm_significant=sum(
                      r.get('p_two_holm',1)<.05 for r in families[0]+families[1]),
                  binary_cluster_sensitivity_holm_significant=sum(
                      r.get('p_two_holm',1)<.05 for r in families[2]))
    (reports/'model_audit.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    display = []
    for r in rows:
        display.append(dict(id=r['id'],model=r['model'],method=r['method'],plays=r['fitted_plays'],
                            players=r['players'],beta=round(r['beta'],5),
                            ci95=f"[{r['lo']:.5f}, {r['hi']:.5f}]",p_two=round(r['p_two'],4),
                            p_two_holm=round(r['p_two_holm'],4) if 'p_two_holm' in r else '—'))
    (reports/'model_audit.md').write_text(
        '# Studies 1–2 model audit\n\n'
        f"Generated UTC: {result['generated_utc']}. All recorded fits converged. "
        f"Two-sided Holm-significant original-family rows: {result['primary_two_sided_holm_significant']}/9; "
        f"binary cluster-sensitivity rows: {result['binary_cluster_sensitivity_holm_significant']}/3.\n\n"
        + markdown_table(display)
        + '\n## Corrections and limits\n\n'
        'Historical reports remain unchanged. Study 1 LMM rows reproduce the original '
        'specification and are shown for audit, including its model-based binary SE deviation. '
        'Separate binary OLS linear-probability fits use player-clustered sandwich SE, '
        'finite-sample correction and t reference with players−1 degrees of freedom. '
        'They change the estimator as well as uncertainty and are explicitly sensitivities.\n\n'
        'The preregistration stated expected signs but did not explicitly state one-sided '
        'testing. Original code used directional p-values. This audit conservatively reports '
        'two-sided p-values and Holm across the six Study 1 LMM and three Study 2 confirmatory '
        'rows separately. The three cluster sensitivities form a separately labelled Holm '
        'family. Historical directional values are saved in JSON, not promoted as new findings.\n\n'
        'Study 2 A0 and 10-yard-split imputation/SDs now use unique sprint-tracked athletes '
        'within position, before joining to plays. Historical code weighted these moments '
        'by opportunity. Baseline Study 1 preprocessing is retained. This is a full-cohort '
        'historical audit, not held-out prediction or a pristine 2025 evaluation.\n\n'
        'Patsy removes only rows missing required formula fields; model groups follow the '
        'actual retained indices. Constant/redundant columns are removed by an ordered rank '
        'rule before fitting; actual samples, dropped terms, warnings, covariate estimates '
        'and timings are recorded in `model_audit.json` and per-model checkpoints. '
        'Normal-reference LMM intervals retain the original continuous-model method. '
        'Covariate estimates are descriptive checks, not an additional confirmatory family.\n\n'
        'A non-significant result does not establish equivalence or no predictive value. '
        'Held-out evaluation and same-sample 3-cone sensitivity remain separate required work.\n')
    print(f"Audit complete: {result['primary_two_sided_holm_significant']}/9 two-sided Holm-significant original-family tests",flush=True)


if __name__=='__main__':
    main()
