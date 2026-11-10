"""Reproduce movement transfer with explicit season scope and size adjustment.

Run: .venv/bin/python -m src.transfer_audit
Writes reports/transfer_audit.{md,json} and player-season cached traits.
The full-cohort descriptive transfer estimates are not held-out prediction.
"""
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.audit_data import markdown_table
from src.reliability import paired_reliability

ROOT = Path(__file__).resolve().parents[1]
TRAITS = ['lat','burst','vmax']


def game_aggregation(d, by_season=False):
    d = d.copy()
    cell = ['lined_up_position','play_type']
    if by_season:
        cell = ['season']+cell
    for trait in TRAITS:
        groups = d.groupby(cell,dropna=False)[trait]
        d[f'z_{trait}'] = (d[trait]-groups.transform('mean'))/groups.transform('std')
    keys = ['nfl_id','combine_position'] + (['season'] if by_season else [])
    d['half'] = d.groupby(keys).game_id.rank(method='dense').astype(int)%2
    full = d.groupby(keys).agg(n_plays=('nfl_id','size'),
        **{f'g_{t}':(f'z_{t}','mean') for t in TRAITS})
    for half in [0,1]:
        h = d[d.half==half].groupby(keys).agg(
            **{f'g_{t}_{half}':(f'z_{t}','mean') for t in TRAITS})
        full = full.join(h)
    return full[full.n_plays>=30].reset_index()


def adjusted_correlation(d, trait, covariates, n_boot=2000):
    columns = [trait,f'g_{trait}']+covariates
    d = d.dropna(subset=columns)
    values = d[columns].to_numpy(float)
    def estimate(a):
        x,y = a[:,0],a[:,1]
        z = np.column_stack([np.ones(len(a)),a[:,2:]])
        xr = x-z@np.linalg.lstsq(z,x,rcond=None)[0]
        yr = y-z@np.linalg.lstsq(z,y,rcond=None)[0]
        if np.std(xr)<1e-12 or np.std(yr)<1e-12:
            return np.nan
        return float(np.corrcoef(xr,yr)[0,1])
    r = estimate(values)
    rng = np.random.default_rng(20261109)
    rs = np.array([estimate(values[rng.integers(len(values),size=len(values))]) for _ in range(n_boot)])
    rs = rs[np.isfinite(rs)]
    lo,hi = np.quantile(rs,[.025,.975])
    return dict(n=len(d),r=r,lo=float(lo),hi=float(hi),valid_bootstraps=len(rs))


def main():
    path = ROOT/'data/interim'
    pp = pd.read_parquet(path/'player_play.parquet',columns=[
        'game_id','play_id','nfl_id','lined_up_position','route_ran','dropback_duration','sack'])
    gt = pd.read_parquet(path/'game_play_traits.parquet')
    cr = pd.read_parquet(path/'combine_results.parquet')
    games = pd.read_parquet(path/'games.parquet',columns=['game_id','season_type'])
    d = gt.merge(pp,on=['game_id','play_id','nfl_id'],validate='one_to_one').merge(
        cr[['nfl_id','combine_position']],validate='many_to_one').merge(games,validate='many_to_one')
    d['play_type'] = 'ALL'
    receiver = d.combine_position.isin(['WR','TE'])
    d.loc[receiver,'play_type'] = d.loc[receiver,'route_ran'].fillna('NO_ROUTE')
    for pos,field in [('OL','dropback_duration'),('DL','sack')]:
        m = d.combine_position==pos
        d.loc[m,'play_type'] = np.where(d.loc[m,field].notna(),'PASS','RUN')
    ct = pd.read_parquet(path/'combine_traits.parquet',columns=['nfl_id']+TRAITS)
    player = ct.merge(cr[['nfl_id','combine_weight','combine_height','forty']],validate='one_to_one')
    rows = []
    for scope,selected in [('historical, PRE+REG+POST',d),
                           ('corrected, PRE+REG',d[d.season_type.isin(['PRE','REG'])]),
                           ('sensitivity, REG only',d[d.season_type=='REG'])]:
        gp = game_aggregation(selected)
        joined = gp.merge(player,validate='one_to_one')
        if scope.startswith('corrected'):
            gp.to_parquet(path/'game_player_traits_audited.parquet',index=False)
            game_aggregation(selected,by_season=True).to_parquet(
                path/'game_player_season_traits_audited.parquet',index=False)
        for pos in ['WR','OL','DL','TE','DB']:
            p = joined[joined.combine_position==pos].copy()
            p['forty_missing'] = p.forty.isna().astype(int)
            p['forty_f'] = p.forty.fillna(p.forty.median())
            for trait in TRAITS:
                rel = paired_reliability(p[f'g_{trait}_0'],p[f'g_{trait}_1'],n_boot=2000)
                for label,cov in [('raw',[]),('weight-adjusted',['combine_weight']),
                    ('size+forty-adjusted',['combine_weight','combine_height','forty_f','forty_missing'])]:
                    result = adjusted_correlation(p,trait,cov)
                    rows.append(dict(scope=scope,position=pos,trait=trait,adjustment=label,
                                     game_SB=rel['SB'],**result))
    result = dict(generated_utc=datetime.now(timezone.utc).isoformat(),rows=rows,
                  input_joined_plays=len(d),excluded_postseason_plays=int((d.season_type=='POST').sum()),
                  bootstrap_resamples=2000,seed=20261109)
    reports = ROOT/'reports'
    (reports/'transfer_audit.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    headline = [r for r in rows if (r['position'],r['trait']) in [('WR','lat'),('DL','burst')]]
    display = [{k:round(v,3) if isinstance(v,float) else v for k,v in r.items()} for r in headline]
    (reports/'transfer_audit.md').write_text(
        '# Movement transfer audit\n\n'
        f"Generated UTC: {result['generated_utc']}.\n\n"
        + markdown_table(display)
        + '\nEach athlete contributes one pooled-season movement trait (≥30 player-plays). '
        'All seasons are full-cohort descriptive measurements, not development/evaluation '
        'prediction. Historical scope included POST; corrected scope explicitly excludes '
        'POST while retaining PRE+REG, as specified in the measurement preregistration. '
        'REG-only is a season-type sensitivity. Per-season traits with season-specific '
        'normalisation are also cached for later checks; these correlations are pooled.\n\n'
        'Game normalisation retains the original lined-up-position × play-type cells. '
        'Receiver play type uses recorded route, OL uses dropback availability and DL uses '
        'sack availability. No outcome-nullification filter is newly added to historical '
        'movement measurement. Context is available only for the inner-joined source rows.\n\n'
        'Adjusted correlations residualise both Combine and game traits on the stated '
        'covariates plus an intercept, within position. Size+forty uses position-sample '
        'median forty and a missing indicator. 2,000 paired athlete bootstrap resamples '
        'refit residualisation each time; percentile intervals. Adjustment definitions '
        'are explicit and need not match undocumented historical exploratory calculations. '
        'Game SB is alternating-game split-half reliability. Complete position/trait '
        'tables are in JSON, without selecting new performance hypotheses.\n\n'
        f"Joined movement plays: {len(d):,}; POST excluded from corrected scope: "
        f"{result['excluded_postseason_plays']:,}. Historical `transfer.md` is unchanged.\n")
    print(markdown_table(display),flush=True)


if __name__=='__main__':
    main()
