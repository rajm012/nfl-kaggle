"""Replay the originally recorded historical cone solver paths; no coefficient cache.

The source statistical model, rows and inference remain unchanged. On raw rebuilding,
unordered Polars joins can alter the default optimizer's retry path. The recorded
historical W2 Powell and W1 BFGS/L-BFGS paths are replayed from a source-only solver plan.
Canonical W1 row ordering removes numerical permutation effects without changing any row.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import warnings

import numpy as np
from scipy.stats import norm
import statsmodels.api as sm

from src import cone_sensitivity
from src.evaluate import fit_model

ROOT = Path(__file__).resolve().parents[1]


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
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            fit = sm.MixedLM(y,x,groups=groups).fit(method=method)
        if (not fit.converged or not np.isfinite(fit.fe_params).all()
                or not np.isfinite(fit.bse[x.columns]).all() or (fit.bse[x.columns]<=0).any()):
            raise RuntimeError('Recorded historical '+solver+' fit failed numerical checks')
        critical = norm.ppf(.975)
        coefficients = {name:{'beta':float(fit.fe_params[name]),'se':float(fit.bse[name]),
                              'lo':float(fit.fe_params[name]-critical*fit.bse[name]),
                              'hi':float(fit.fe_params[name]+critical*fit.bse[name])} for name in x}
        replayed.append({'id':plan['id'],'model':plan['model'],'solver':solver,
                         'canonical_row_order':plan.get('canonical_row_order', False),
                         'reason':'Replay recorded historical retry, unchanged model/sample'})
        return {'coefficients':fit.fe_params.to_dict(),'coefficient_intervals':coefficients,
                'method':'player random-intercept LMM','player_random_variance':float(fit.cov_re.iloc[0,0]),
                'converged':True,'warnings':sorted(set(str(w.message) for w in caught)),
                'optimizer':solver+' replay of recorded historical retry',
                'initial_diagnostics':[plan['recorded_optimizer']],
                'seconds':round(time.monotonic()-started,3)}

    cone_sensitivity.fit_model = recorded_fit
    cone_sensitivity.main()
    (ROOT/'reports/historical_solver_replay.json').write_text(json.dumps(
        {'generated_utc':datetime.now(timezone.utc).isoformat(),'replayed':replayed,
         'cached_coefficients_used':False,'outcome_model_or_sample_changed':False},indent=2)+'\n')


if __name__=='__main__':
    main()
