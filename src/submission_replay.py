"""Replay the originally recorded historical cone solver paths; no coefficient cache.

The source statistical model, rows and inference remain unchanged. On raw rebuilding,
unordered Polars joins can alter the default optimizer's retry path. The recorded
historical W2 Powell and W1 BFGS/L-BFGS paths are replayed from a source-only solver plan.
Canonical W1 row ordering removes numerical permutation effects without changing any row.
For that boundary fit only, try identical C then F buffers if strict numerical checks
fail. This fixed retry is based on convergence/covariance, never coefficient direction.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import warnings

import numpy as np
import pandas as pd
import polars as pl
from scipy.stats import norm
import statsmodels.api as sm

from src import cone_sensitivity
from src.evaluate import fit_model

ROOT = Path(__file__).resolve().parents[1]


def canonical_reference_base_table():
    """Original historical table with sorted references before floating reductions.

    Formula, reference athletes, imputation and joins match outcomes.base_table.
    Sorting only the unique-athlete reference removes join-order roundoff from
    the input of the sensitive historical solver; play eligibility is unchanged.
    """
    path = ROOT/'data/interim'
    pp = pl.read_parquet(path/'player_play.parquet')
    games = pl.read_parquet(path/'games.parquet').select('game_id','season','season_type')
    players = pl.read_parquet(path/'players.parquet').select('nfl_id','draft_overall_pick')
    cr = pl.read_parquet(path/'combine_results.parquet').select(
        'nfl_id','combine_position','forty','combine_weight','combine_height')
    tr = pl.read_parquet(path/'combine_traits.parquet').select('nfl_id','lat','burst')
    p = (players.join(cr,on='nfl_id').join(tr,on='nfl_id').sort('nfl_id')
         .with_columns(udfa=pl.col('draft_overall_pick').is_null().cast(pl.Int8),
                       pick=pl.col('draft_overall_pick').fill_null(260),
                       forty_missing=pl.col('forty').is_null().cast(pl.Int8),
                       forty=pl.col('forty').fill_null(pl.col('forty').median().over('combine_position')))
         .with_columns([((pl.col(c)-pl.col(c).mean().over('combine_position'))
                         /pl.col(c).std().over('combine_position')).alias(c+'_z')
                        for c in ['lat','burst','forty','combine_weight','combine_height','pick']]))
    return (pp.join(games,on='game_id')
            .filter((pl.col('season_type')=='REG')&(pl.col('play_nullified_by_penalty')=='N'))
            .join(p,on='nfl_id'))


def main():
    plans = json.loads((ROOT/'reports/historical_solver_plan.json').read_text())
    replayed = []

    def recorded_fit(y,x,groups,binary):
        plan = next((p for p in plans if list(x)==p['columns']),None)
        if binary or plan is None:
            return fit_model(y,x,groups,binary)
        started = time.monotonic()
        method = plan.get('method', 'powell')
        solver = 'Powell' if method == 'powell' else 'BFGS/L-BFGS'
        y, groups = np.asarray(y), np.asarray(groups)
        if plan.get('canonical_row_order', False):
            order = np.lexsort((y, *(x[name].to_numpy() for name in reversed(x.columns)), groups))
            y, x, groups = y[order], x.iloc[order].reset_index(drop=True), groups[order]
            # Identical numbers in C/F buffers can change this boundary fit's
            # convergence flag. Fix buffer layout as well as row order; keep
            # every value, model, solver and numerical acceptance check intact.
            x = pd.DataFrame(np.array(x.to_numpy(), order='C', copy=True), columns=x.columns, copy=False)
            if not x.to_numpy().flags.c_contiguous:
                raise RuntimeError('Canonical historical matrix layout was not preserved')
        numerical_attempts, fit_warnings = [], []
        layouts = ['C', 'F'] if plan.get('canonical_row_order', False) else [None]
        for layout in layouts:
            matrix = x
            if layout is not None:
                matrix = pd.DataFrame(np.array(x.to_numpy(), order=layout, copy=True),
                                      columns=x.columns, copy=False)
                if not np.array_equal(matrix.to_numpy(), x.to_numpy()):
                    raise RuntimeError('Historical layout retry changed matrix values')
                flags = matrix.to_numpy().flags
                if not (flags.c_contiguous if layout == 'C' else flags.f_contiguous):
                    raise RuntimeError('Historical retry matrix layout was not preserved')
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always')
                fit = sm.MixedLM(y,matrix,groups=groups).fit(method=method)
            valid = bool(fit.converged and np.isfinite(fit.fe_params).all()
                         and np.isfinite(fit.bse[x.columns]).all()
                         and (fit.bse[x.columns]>0).all())
            messages = sorted(set(str(w.message) for w in caught))
            fit_warnings.extend(messages)
            numerical_attempts.append({'matrix_layout':layout, 'converged':bool(fit.converged),
                                       'strict_numerical_checks_pass':valid, 'warnings':messages})
            if valid:
                break
        if not valid:
            raise RuntimeError('Recorded historical '+solver+' fit failed numerical checks')
        critical = norm.ppf(.975)
        coefficients = {name:{'beta':float(fit.fe_params[name]),'se':float(fit.bse[name]),
                              'lo':float(fit.fe_params[name]-critical*fit.bse[name]),
                              'hi':float(fit.fe_params[name]+critical*fit.bse[name])} for name in x}
        replayed.append({'id':plan['id'],'model':plan['model'],'solver':solver,
                         'canonical_row_order':plan.get('canonical_row_order', False),
                         'canonical_C_matrix_layout':plan.get('canonical_row_order', False),
                         'accepted_matrix_layout':layout, 'numerical_attempts':numerical_attempts,
                         'reason':'Replay recorded historical retry, unchanged model/sample'})
        return {'coefficients':fit.fe_params.to_dict(),'coefficient_intervals':coefficients,
                'method':'player random-intercept LMM','player_random_variance':float(fit.cov_re.iloc[0,0]),
                'converged':True,'warnings':sorted(set(fit_warnings)),
                'optimizer':solver+' replay of recorded historical retry',
                'initial_diagnostics':[plan['recorded_optimizer']],
                'seconds':round(time.monotonic()-started,3)}

    cone_sensitivity.base_table = canonical_reference_base_table
    cone_sensitivity.fit_model = recorded_fit
    cone_sensitivity.main()
    (ROOT/'reports/historical_solver_replay.json').write_text(json.dumps(
        {'generated_utc':datetime.now(timezone.utc).isoformat(),'replayed':replayed,
         'cached_coefficients_used':False,'outcome_model_or_sample_changed':False},indent=2)+'\n')


if __name__=='__main__':
    main()
