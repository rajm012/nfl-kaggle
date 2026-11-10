"""Frozen Studies 1–2 cohort prediction; develop and evaluate in separate invocations.

Run: python -m src.evaluate --stage develop
Then: python -m src.evaluate --stage evaluate
See reports/evaluation_protocol.md. Never fits evaluation-player random effects.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import warnings

import duckdb
import numpy as np
import pandas as pd
from scipy.stats import norm, t
import statsmodels.api as sm

from src.audit_data import markdown_table, sql_path
from src.route_context import independent_columns

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261110
KEYS = ['game_id', 'play_id', 'nfl_id']
PLAYER_NUMERIC = ['pick', 'forty', 'combine_weight', 'combine_height']
CONTEXT = {
    'WR': (['season', 'down', 'route_ran', 'team_coverage_man_zone', 'receiver_alignment'],
           ['yards_to_go', 'cushion_f', 'cushion_missing', 'in_motion']),
    'OL': (['season', 'down'], ['yards_to_go', 'dropback_duration', 'pass_rushers_encountered']),
    'DL': (['season', 'down', 'lined_up_position'], ['yards_to_go', 'blitz']),
}


def specifications():
    rows = [
        ('W1', 'WR', 'separation_at_pass_forward', ['lat'], 1),
        ('W2', 'WR', 'separation_at_pass_forward', ['burst'], 1),
        ('O1', 'OL', 'pressure_allowed_i', ['lat'], 1),
        ('O2', 'OL', 'pressure_allowed_i', ['burst'], 1),
        ('D1', 'DL', 'player_get_off', ['burst'], 1),
        ('D2', 'DL', 'pressure_i', ['lat'], 1),
        ('F1', 'DL', 'player_get_off', ['A0'], 2),
        ('F2', 'OL', 'peak_pressure_probability_allowed', ['A0'], 2),
        ('F3', 'WR', 'separation_at_pass_forward', ['A0'], 2),
    ]
    specs = [dict(id=i, position=p, outcome=y, traits=tr, study=s, family='primary',
                  ten_split=s==2, cone=False) for i,p,y,tr,s in rows]
    for original in ['W1', 'O1', 'D1', 'D2']:
        parent = next(r for r in specs if r['id']==original)
        specs.append(dict(parent, id=original+'_joint', traits=['lat', 'burst'], family='joint secondary'))
    for original in ['F1', 'F2', 'F3']:
        parent = next(r for r in specs if r['id']==original)
        specs.append(dict(parent, id=original+'_no10', ten_split=False, family='no-10yd secondary'))
    for parent in list(specs[:9]):
        specs.append(dict(parent, id=parent['id']+'_cone', cone=True, family='cone sensitivity'))
    return specs


def training_traits(attempts, players):
    """Two historical exposures, with drill reference athletes restricted to development."""
    pd_table = attempts.groupby(['nfl_id', 'drill'], as_index=False)[['lat', 'burst']].mean()
    pd_table = pd_table.merge(players[['nfl_id', 'draft_year']], validate='many_to_one')
    train = pd_table[pd_table.draft_year.isin([2023, 2024])]
    references, scored = {}, pd_table[['nfl_id', 'drill']].copy()
    for feature in ['lat', 'burst']:
        ref = train.groupby('drill')[feature].agg(['mean', 'std', 'count'])
        valid = (ref['count']>=2) & np.isfinite(ref['std']) & (ref['std']>0)
        references[feature] = dict(excluded_drills=sorted(set(pd_table.drill)-set(ref.index[valid])),
                                  reference=ref[valid].reset_index().to_dict('records'))
        values = pd_table.merge(ref[valid], left_on='drill', right_index=True, validate='many_to_one')
        values[feature] = (values[feature]-values['mean'])/values['std']
        scored = scored.merge(values[['nfl_id', 'drill', feature]], how='left', validate='one_to_one')
    traits = scored.groupby('nfl_id')[['lat', 'burst']].mean().reset_index()
    return traits, references


def load_players():
    path = ROOT/'data/interim'
    p = pd.read_parquet(path/'combine_results.parquet', columns=[
        'nfl_id', 'draft_year', 'combine_position', 'forty', 'ten_yd_split',
        'combine_weight', 'combine_height', 'three_cone'])
    p = p.merge(pd.read_parquet(path/'players.parquet', columns=['nfl_id', 'draft_overall_pick']),
                validate='one_to_one')
    tr, reference = training_traits(pd.read_parquet(path/'combine_attempts.parquet'), p)
    p = p.merge(tr, validate='one_to_one').merge(pd.read_parquet(
        path/'sprint_traits.parquet', columns=['nfl_id', 'A0']), how='left', validate='one_to_one')
    return p, reference


def load_plays(classes):
    """Development invocation does not materialise 2025 outcome rows."""
    con = duckdb.connect()
    con.execute("SET memory_limit='1GB'")
    con.execute('SET threads=2')
    for name in ['player_play', 'games', 'combine_results']:
        con.execute(f'CREATE VIEW {name} AS SELECT * FROM read_parquet('
                    f'{sql_path(ROOT/"data/interim"/f"{name}.parquet")})')
    years = ','.join(str(int(c)) for c in classes)
    rows = con.sql(f'''SELECT pp.game_id,pp.play_id,pp.nfl_id,g.season,cr.draft_year,
        pp.down,pp.yards_to_go,pp.route_ran,pp.cushion,pp.team_coverage_man_zone,
        pp.receiver_alignment,pp.in_motion_at_ball_snap,pp.dropback_duration,
        pp.pass_rushers_encountered,pp.blitzing,pp.lined_up_position,pp.pressure_allowed,
        pp.sack,pp.time_to_pressure,pp.player_get_off,pp.separation_at_pass_forward,
        pp.peak_pressure_probability_allowed
        FROM player_play pp JOIN games g USING(game_id)
        JOIN combine_results cr USING(nfl_id)
        WHERE cr.draft_year IN ({years}) AND cr.combine_position IN ('WR','OL','DL')
          AND g.season=cr.draft_year AND g.season_type='REG'
          AND pp.play_nullified_by_penalty='N' ORDER BY pp.game_id,pp.play_id,pp.nfl_id''').df()
    con.close()
    if rows[KEYS].isna().any().any() or rows.duplicated(KEYS).any():
        raise ValueError('Null/duplicate prediction keys')
    rows['pressure_allowed_i'] = rows.pressure_allowed.astype(float)
    rows['pressure_i'] = rows.time_to_pressure.notna().astype(int)
    return rows


def select_sample(plays, players, spec):
    d = plays.merge(players.drop(columns='draft_year'), validate='many_to_one')
    d = d[d.combine_position==spec['position']].copy()
    before = len(d)
    if spec['outcome']=='pressure_i':
        d = d[d.sack.notna()].copy()
    d = d[d[spec['outcome']].notna()].copy()
    recorded = len(d)
    required = KEYS + ['down', 'yards_to_go', 'combine_weight', 'combine_height'] + spec['traits']
    if spec['position']=='OL':
        required += ['dropback_duration', 'pass_rushers_encountered']
    if spec['cone']:
        required += ['three_cone']
    d = d.dropna(subset=required).copy().reset_index(drop=True)
    if not np.isfinite(d[spec['outcome']].to_numpy(float)).all():
        raise ValueError('Nonfinite outcome')
    return d, dict(position_rookie_rows=before, outcome_recorded_rows=recorded, fitted_rows=len(d),
                   dropped_required_or_exposure=recorded-len(d), players=int(d.nfl_id.nunique()))


def fit_preprocessing(d, players, spec):
    ref = players[(players.combine_position==spec['position']) & players.draft_year.isin([2023, 2024])].copy()
    if spec['study']==2:
        ref = ref[ref.A0.notna()].copy()
    median = {name:float(ref[name].median()) for name in ['forty', 'ten_yd_split']}
    ref['pick'] = ref.draft_overall_pick.fillna(260)
    ref['forty'] = ref.forty.fillna(median['forty'])
    ref['ten_f'] = ref.ten_yd_split.fillna(median['ten_yd_split'])
    features = PLAYER_NUMERIC + spec['traits'] + (['ten_f'] if spec['ten_split'] else [])
    scalers = {}
    for feature in features:
        mean, sd = float(ref[feature].mean()), float(ref[feature].std(ddof=1))
        if not np.isfinite(mean):
            raise ValueError(f'No training reference for {feature}')
        scalers[feature] = dict(mean=mean, sd=sd if np.isfinite(sd) and sd>0 else 0.)
    if spec['cone']:
        cone = ref.three_cone.dropna()
        if len(cone)<2 or cone.std(ddof=1)<=0:
            raise ValueError('No estimable training cone reference')
        scalers['three_cone'] = dict(mean=float(cone.mean()), sd=float(cone.std(ddof=1)))
    categorical, _ = CONTEXT[spec['position']]
    context, most_frequent = {}, {}
    for column in categorical:
        v = d[column].fillna('UNK').astype(str)
        context[column] = sorted(v.unique().tolist())
        most_frequent[column] = str(v.value_counts().index[0])
    cushion = float(d.cushion.median()) if spec['position']=='WR' else 0.
    if not np.isfinite(cushion):
        raise ValueError('No development cushion median')
    return dict(player_reference_n=len(ref), development_classes=[2023, 2024],
                player_medians=median, player_scalers=scalers, cushion_median=cushion,
                categories=context, most_frequent=most_frequent, latest_season=str(int(d.season.max())))


def transform(d, meta):
    d = d.copy()
    missing = {column:int(d[column].isna().sum()) for column in
               ['forty', 'ten_yd_split', 'cushion', 'in_motion_at_ball_snap', 'blitzing']}
    d['pick'] = d.draft_overall_pick.fillna(260)
    d['udfa'] = d.draft_overall_pick.isna().astype(int)
    d['forty_missing'] = d.forty.isna().astype(int)
    d['ten_missing'] = d.ten_yd_split.isna().astype(int)
    d['forty'] = d.forty.fillna(meta['player_medians']['forty'])
    d['ten_f'] = d.ten_yd_split.fillna(meta['player_medians']['ten_yd_split'])
    d['cushion_missing'] = d.cushion.isna().astype(int)
    d['cushion_f'] = d.cushion.fillna(meta['cushion_median'])
    d['in_motion'] = d.in_motion_at_ball_snap.fillna(False).astype(int)
    d['blitz'] = d.blitzing.fillna(False).astype(int)
    for feature, scaler in meta['player_scalers'].items():
        d[feature+'_z'] = ((d[feature]-scaler['mean'])/scaler['sd']) if scaler['sd'] else 0.
    unknown = {}
    for column, levels in meta['categories'].items():
        values = d[column].fillna('UNK').astype(str)
        unseen = ~values.isin(levels)
        unknown[column] = values[unseen].value_counts().to_dict()
        fallback = meta['latest_season'] if column=='season' else (
            'UNK' if 'UNK' in levels else meta['most_frequent'][column])
        d[column] = values.where(~unseen, fallback)
    return d, dict(missing=missing, unknown_categories=unknown)


def design(d, meta, spec):
    x = pd.DataFrame({'Intercept':np.ones(len(d))}, index=d.index)
    for feature in PLAYER_NUMERIC:
        x[feature+'_z'] = d[feature+'_z']
    for feature in ['udfa', 'forty_missing']:
        x[feature] = d[feature]
    if spec['ten_split']:
        x['ten_f_z'], x['ten_missing'] = d.ten_f_z, d.ten_missing
    if spec['cone']:
        x['three_cone_z'] = d.three_cone_z
    categorical, numeric = CONTEXT[spec['position']]
    for column in categorical:
        for level in meta['categories'][column][1:]:
            x[column+'='+level] = (d[column]==level).astype(float)
    for column in numeric:
        x[column] = d[column].astype(float)
    full = x.copy()
    for feature in spec['traits']:
        full[feature+'_z'] = d[feature+'_z']
    return x, full


def fit_model(y, x, groups, binary):
    started = time.monotonic()
    optimizer = 'OLS' if binary else 'default'
    initial_diagnostics = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        if binary:
            fit = sm.OLS(y,x).fit(cov_type='cluster',
                cov_kwds={'groups':np.asarray(groups),'use_correction':True},use_t=True)
            params = fit.params
            critical = t.ppf(.975, len(np.unique(groups))-1)
            variance, converged = None, True
        else:
            model = sm.MixedLM(y,x,groups=np.asarray(groups))
            try:
                fit = model.fit()
            except np.linalg.LinAlgError as exc:
                fit = None
                initial_diagnostics.append(f'Default optimizer raised {type(exc).__name__}: {exc}')
            initial_diagnostics += sorted(set(str(w.message) for w in caught))
            invalid = (fit is None or not fit.converged or not np.isfinite(fit.fe_params).all()
                       or not np.isfinite(fit.bse[x.columns]).all()
                       or (fit.bse[x.columns]<=0).any()
                       or any('Hessian' in message for message in initial_diagnostics))
            if invalid:
                optimizer = 'Powell after invalid default covariance/convergence'
                fit = model.fit(method='powell')
            if not fit.converged:
                raise RuntimeError('Development MixedLM did not converge')
            params = fit.fe_params
            critical = norm.ppf(.975)
            variance, converged = float(fit.cov_re.iloc[0,0]), bool(fit.converged)
        diagnostics = sorted(set(str(w.message) for w in caught))
    coefficient = {name:dict(beta=float(params[name]), se=float(fit.bse[name]),
                            lo=float(params[name]-critical*fit.bse[name]),
                            hi=float(params[name]+critical*fit.bse[name])) for name in x}
    if (not np.isfinite(np.array(list(params))).all()
            or not np.isfinite(fit.bse[x.columns]).all() or (fit.bse[x.columns]<=0).any()):
        raise ValueError('Invalid fixed coefficient uncertainty after development retry')
    return dict(coefficients=params.to_dict(), coefficient_intervals=coefficient,
                method='player-clustered LPM' if binary else 'player random-intercept LMM',
                player_random_variance=variance, converged=converged, warnings=diagnostics,
                optimizer=optimizer, initial_diagnostics=initial_diagnostics,
                seconds=round(time.monotonic()-started,3))


def freeze_pair(d, players, spec):
    meta = fit_preprocessing(d,players,spec)
    transformed, logs = transform(d,meta)
    x0, x1 = design(transformed,meta,spec)
    x0, dropped0 = independent_columns(x0,np.ones(len(x0)))
    x1, dropped1 = independent_columns(x1,np.ones(len(x1)))
    added = [feature+'_z' for feature in spec['traits']]
    if any(name not in x1 for name in added):
        raise ValueError('Exposure not estimable under ordered rank rule')
    if not set(x0).issubset(x1):
        raise ValueError('Augmented model does not preserve baseline columns')
    binary = spec['outcome'] in ['pressure_i', 'pressure_allowed_i']
    y = d[spec['outcome']].to_numpy(float)
    model0 = fit_model(y,x0,d.nfl_id,binary)
    model1 = fit_model(y,x1,d.nfl_id,binary)
    _, context_numeric = CONTEXT[spec['position']]
    context_columns = [name for name in x0 if '=' in name or name in context_numeric]
    return dict(spec=spec,preprocessing=meta,training_missingness=logs,
                columns0=x0.columns.tolist(),columns1=x1.columns.tolist(),
                dropped0=dropped0,dropped1=dropped1,context_columns=context_columns,
                training_players=int(d.nfl_id.nunique()),training_plays=len(d),
                training_player_ids=sorted(map(int,d.nfl_id.unique())),
                training_outcome_sd=float(np.std(y,ddof=1)),baseline=model0,augmented=model1)


def scores(d, model):
    """Outcome-independent fixed prediction; outcomes enter only the final error calculation."""
    original = d.copy()
    d, logs = transform(d,model['preprocessing'])
    x0,x1 = design(d,model['preprocessing'],model['spec'])
    beta0 = pd.Series(model['baseline']['coefficients'])
    beta1 = pd.Series(model['augmented']['coefficients'])
    p0 = x0[model['columns0']].dot(beta0)
    p1 = x1[model['columns1']].dot(beta1)
    ctx = model['context_columns']
    common_context = x0[ctx].dot(beta0[ctx]) if ctx else pd.Series(0.,index=d.index)
    rows = pd.DataFrame(dict(nfl_id=d.nfl_id, observed=original[model['spec']['outcome']],
                             baseline=p0, augmented=p1, common_context=common_context))
    per_player = rows.groupby('nfl_id').agg(plays=('nfl_id','size'),observed=('observed','mean'),
        baseline=('baseline','mean'),augmented=('augmented','mean'),common_context=('common_context','mean'))
    per_player['observed_adjusted'] = per_player.observed-per_player.common_context
    per_player['baseline_adjusted'] = per_player.baseline-per_player.common_context
    per_player['augmented_adjusted'] = per_player.augmented-per_player.common_context
    per_player['error0'] = per_player.observed-per_player.baseline
    per_player['error1'] = per_player.observed-per_player.augmented
    return per_player.reset_index(), logs


def paired_metrics(table, family_size=1, n_boot=10000):
    if len(table)<2:
        return dict(players=len(table), status='insufficient evaluation players')
    a,b = table.error0.to_numpy(float),table.error1.to_numpy(float)
    rmse0,rmse1 = float(np.sqrt(np.mean(a*a))),float(np.sqrt(np.mean(b*b)))
    mae0,mae1 = float(np.abs(a).mean()),float(np.abs(b).mean())
    rng = np.random.default_rng(SEED)
    samples = rng.integers(len(a),size=(n_boot,len(a)))
    rb = np.sqrt((a[samples]**2).mean(axis=1))
    ra = np.sqrt((b[samples]**2).mean(axis=1))
    gain = rb-ra
    lo,hi = np.quantile(gain,[.025,.975])
    sl,sh = np.quantile(gain,[.025/family_size,1-.025/family_size])
    relative = 100*gain/np.maximum(rb,1e-12)
    rlo,rhi = np.quantile(relative,[.025,.975])
    return dict(players=len(a), status='scored',rmse0=rmse0,rmse1=rmse1,
                improvement=rmse0-rmse1,improvement_lo=float(lo),improvement_hi=float(hi),
                simultaneous_lo=float(sl),simultaneous_hi=float(sh),family_size=family_size,
                mae0=mae0,mae1=mae1,mae_improvement=mae0-mae1,
                relative_improvement_percent=100*(rmse0-rmse1)/rmse0,
                relative_lo=float(rlo),relative_hi=float(rhi),
                min_plays=int(table.plays.min()),median_plays=float(table.plays.median()),
                max_plays=int(table.plays.max()))


def provenance():
    paths = ['src/evaluate.py','src/route_context.py','reports/evaluation_protocol.md',
             'requirements.txt'] + ['data/interim/'+n+'.parquet' for n in
             ['players','combine_results','combine_attempts','sprint_traits','games','player_play']]
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in paths}


def develop():
    players, reference = load_players()
    plays = load_plays([2023,2024])
    assert set(plays.draft_year).issubset({2023,2024})
    models = []
    directory = ROOT/'reports/evaluation_models'
    directory.mkdir(exist_ok=True)
    for spec in specifications():
        d,attrition = select_sample(plays,players,spec)
        if len(d)==0:
            raise ValueError(f"{spec['id']}: empty training sample")
        model = freeze_pair(d,players,spec)
        model['attrition'] = attrition
        (directory/(spec['id']+'.json')).write_text(json.dumps(model,indent=2,allow_nan=False)+'\n')
        models.append(model)
        print(f"Frozen {spec['id']}: {model['training_players']} players, "
              f"{model['training_plays']:,} plays; {len(model['columns0'])}/{len(model['columns1'])} columns",flush=True)
    snapshot = dict(frozen_utc=datetime.now(timezone.utc).isoformat(), models=models,
                    drill_reference=reference, provenance=provenance(),
                    evaluation_outcomes_opened=False, evaluation_players_fitted=False)
    (ROOT/'reports/evaluation_development.json').write_text(json.dumps(snapshot,indent=2,allow_nan=False)+'\n')
    print(f'All {len(models)} development pairs frozen before evaluation.',flush=True)


def write_report(result):
    rows = []
    for entry in result['results']:
        m = entry['metrics']
        rows.append(dict(test=entry['id'],family=entry['family'],train_players=entry['training_players'],
            eval_players=m['players'],eval_plays=entry['evaluation_attrition']['fitted_rows'],
            baseline_RMSE=round(m['rmse0'],5),tracking_RMSE=round(m['rmse1'],5),
            improvement=round(m['improvement'],5),
            ci95=f"[{m['improvement_lo']:.5f}, {m['improvement_hi']:.5f}]",
            family_interval=f"[{m['simultaneous_lo']:.5f}, {m['simultaneous_hi']:.5f}]"))
    main = [r for r in rows if r['family']=='primary']
    extra = [r for r in rows if r['family']!='primary']
    text = '# Studies 1–2 cohort prediction validation\n\n'
    text += f"Generated UTC: {result['generated_utc']}. Frozen development: {result['frozen_utc']}.\n\n"
    text += 'Positive improvement means lower equal-player RMSE with tracking. Units are yards '
    text += 'for WR separation, seconds for DL get-off, and outcome-scale probability/proportion '
    text += 'units for pressure outcomes. This is retrospective conditional prediction on realised NFL context.\n\n'
    text += markdown_table(main)+'\n## Prespecified secondary and cone comparisons\n\n'+markdown_table(extra)
    text += '\n## Validation boundaries\n\n'
    text += 'Rookie REG, non-nullified plays; 2023–24 development and 2025 evaluation. '
    text += 'No evaluation-player effects, imputation moments, context coefficients or recalibration '
    text += 'are fitted from evaluation outcomes. Fixed predictions are averaged within athlete; '
    text += 'a common baseline context adjustment leaves the compared errors unchanged. '
    text += 'All nine original exposures/outcomes are reported, without promoting a winning secondary.\n\n'
    text += '10,000 paired athlete resamples give percentile improvement intervals conditional '
    text += 'on the frozen development fits. Primary family intervals use Bonferroni-adjusted '
    text += 'percentiles within six Study 1 / three Study 2 comparisons; finite bootstrap tails '
    text += 'and small evaluation samples limit precision. Training uncertainty is not included. '
    text += 'The ≥30-play sensitivity, MAE, relative changes and unknown-level counts are in JSON.\n\n'
    text += 'The historical studies already used 2025 outcomes: this is not a pristine holdout. '
    text += 'An unseen 2025 calendar intercept maps to the latest trained season; other unseen '
    text += 'context levels use frozen UNK/modal encodings. Boundary warnings are retained in '
    text += 'development metadata. Binary LPM predictions are not clipped or described as '
    text += 'calibrated probabilities. Small cone subsets are sensitivities, not general scouting validation.\n\n'
    text += 'No Study 3 interaction is fitted; its measurement gate remains failed. Full protocol: '
    text += '`evaluation_protocol.md`; frozen preprocessing/coefficients: `evaluation_development.json`, '
    text += '`evaluation_models/`; per-athlete errors: `data/interim/evaluation_player_scores.parquet`.\n'
    (ROOT/'reports/validation.md').write_text(text)


def evaluate():
    snapshot = json.loads((ROOT/'reports/evaluation_development.json').read_text())
    if snapshot['provenance']!=provenance():
        raise RuntimeError('Frozen source/protocol/inputs changed; regenerate development before evaluation')
    players,_ = load_players()
    plays = load_plays([2025])
    all_scores, results = [], []
    for model in snapshot['models']:
        spec = model['spec']
        d,attrition = select_sample(plays,players,spec)
        if set(d.nfl_id)&set(model['training_player_ids']):
            raise ValueError('Training/evaluation player overlap')
        table,logs = scores(d,model)
        family_size = (6 if spec['study']==1 else 3) if spec['family']=='primary' else 1
        metrics = paired_metrics(table,family_size=family_size)
        if metrics['status']!='scored':
            raise ValueError(f"{spec['id']}: insufficient evaluation support")
        results.append(dict(id=spec['id'],study=spec['study'],family=spec['family'],
            position=spec['position'],outcome=spec['outcome'],training_players=model['training_players'],
            evaluation_attrition=attrition,evaluation_context=logs,metrics=metrics,
            minimum30_sensitivity=paired_metrics(table[table.plays>=30],family_size=family_size)))
        all_scores.append(table.assign(test=spec['id'],family=spec['family']))
        print(f"Scored {spec['id']}: n={metrics['players']}; RMSE gain="
              f"{metrics['improvement']:+.5f} [{metrics['improvement_lo']:+.5f},"
              f"{metrics['improvement_hi']:+.5f}]",flush=True)
    result = dict(generated_utc=datetime.now(timezone.utc).isoformat(),frozen_utc=snapshot['frozen_utc'],
                  results=results,seed=SEED,bootstrap_resamples=10000,
                  prior_2025_exposure=True,evaluation_players_fitted=False,
                  source_provenance=snapshot['provenance'])
    (ROOT/'reports/validation.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    pd.concat(all_scores,ignore_index=True).to_parquet(ROOT/'data/interim/evaluation_player_scores.parquet',index=False)
    write_report(result)
    print('All frozen comparisons scored; report: reports/validation.md',flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=['develop','evaluate'],required=True)
    args = parser.parse_args()
    if args.stage=='develop':
        develop()
    else:
        evaluate()


if __name__=='__main__':
    main()
