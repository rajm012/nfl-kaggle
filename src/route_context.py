"""Frozen Study 3 measurement screen, prior to TURN/outcome associations.

Run: .venv/bin/python -m src.route_context
Fits the conventional baseline on development players only; stops before the
TURN interaction and any 2025 performance evaluation. See study3_protocol.md.
"""
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from src.audit_data import markdown_table
from src.reliability import paired_reliability

ROOT = Path(__file__).resolve().parents[1]
CONVENTIONAL = ['weight_z', 'height_z', 'forty_z', 'pick_z', 'udfa', 'forty_missing']
CATEGORICAL = ['route_ran', 'down', 'team_coverage_man_zone', 'receiver_alignment']


def independent_columns(design, weights):
    """Keep columns in declared order using a scale-aware orthogonal rank rule."""
    a = design.to_numpy(float) * np.sqrt(np.asarray(weights))[:, None]
    basis, keep, dropped = [], [], []
    for j, name in enumerate(design.columns):
        v = a[:, j].copy()
        scale = np.linalg.norm(v)
        if scale:
            for _ in range(2):
                for q in basis:
                    v -= q * np.dot(q, v)
        norm = np.linalg.norm(v)
        if norm <= 1e-10 * max(scale, 1):
            dropped.append(name)
        else:
            keep.append(name)
            basis.append(v/norm)
    return design[keep], dropped


def candidate_table():
    path = ROOT/'data/interim'
    pp = pd.read_parquet(path/'player_play.parquet')
    games = pd.read_parquet(path/'games.parquet', columns=['game_id', 'season', 'season_type'])
    players = pd.read_parquet(path/'players.parquet', columns=['nfl_id', 'draft_overall_pick'])
    cr = pd.read_parquet(path/'combine_results.parquet')
    player_table = cr.merge(players, validate='one_to_one').merge(
        pd.read_parquet(path/'study3_turn.parquet'), validate='one_to_one')
    d = pp.merge(games, validate='many_to_one').merge(player_table, validate='many_to_one')
    d = d[(d.combine_position=='WR') & (d.season_type=='REG') & (d.season==d.draft_year)
          & (d.play_nullified_by_penalty=='N') & d.route_ran.isin(['SLANT', 'OUT', 'GO'])
          & d.separation_at_pass_forward.notna()].copy()
    d['BREAK'] = (d.route_ran!='GO').astype(int)
    counts = d.groupby(['nfl_id', 'BREAK']).size().unstack(fill_value=0)
    eligible = counts.index[(counts[0]>=10) & (counts[1]>=10)]
    d = d[d.nfl_id.isin(eligible)].copy()
    before = d.groupby('draft_year').agg(players=('nfl_id','nunique'), plays=('nfl_id','size'))
    required = ['game_id', 'play_id', 'nfl_id', 'down', 'yards_to_go',
                'TURN', 'combine_weight', 'combine_height']
    d = d.dropna(subset=required).copy()
    # Preserve the frozen support threshold after final usable-row checks.
    counts = d.groupby(['nfl_id','BREAK']).size().unstack(fill_value=0)
    eligible = counts.index[(counts[0]>=10) & (counts[1]>=10)]
    d = d[d.nfl_id.isin(eligible)].copy()
    after = d.groupby('draft_year').agg(players=('nfl_id','nunique'), plays=('nfl_id','size'))
    support = before.join(after, lsuffix='_initial', rsuffix='_fitted').reset_index().to_dict('records')
    dev = d[d.draft_year.isin([2023,2024])].copy()
    eval_count = int(d.loc[d.draft_year==2025, 'nfl_id'].nunique())
    return dev, player_table, support, eval_count


def preprocess_development(dev, player_table, include_turn=True):
    reference = player_table[(player_table.combine_position=='WR')
                             & player_table.draft_year.isin([2023,2024])].copy()
    median_forty = float(reference.forty.median())
    scalers = {}
    for name, d in [('reference', reference), ('development', dev)]:
        d['udfa'] = d.draft_overall_pick.isna().astype(int)
        d['pick'] = d.draft_overall_pick.fillna(260)
        d['forty_missing'] = d.forty.isna().astype(int)
        d['forty'] = d.forty.fillna(median_forty)
        d['weight'], d['height'] = d.combine_weight, d.combine_height
        features = ['weight', 'height', 'forty', 'pick'] + (['TURN'] if include_turn else [])
        for feature in features:
            if name=='reference':
                scalers[feature] = dict(mean=float(d[feature].mean()), sd=float(d[feature].std(ddof=1)))
            s = scalers[feature]
            if not np.isfinite(s['sd']) or s['sd']<=0:
                raise ValueError(f'Invalid training player SD: {feature}')
            d[f'{feature}_z'] = (d[feature]-s['mean'])/s['sd']
    missing = dict(cushion=int(dev.cushion.isna().sum()),
                   motion=int(dev.in_motion_at_ball_snap.isna().sum()),
                   coverage=int(dev.team_coverage_man_zone.isna().sum()),
                   alignment=int(dev.receiver_alignment.isna().sum()))
    cushion_median = float(dev.cushion.median())
    if not np.isfinite(cushion_median):
        raise ValueError('No observed development cushions')
    dev['cushion_missing'] = dev.cushion.isna().astype(int)
    dev['cushion_f'] = dev.cushion.fillna(cushion_median)
    dev['motion'] = dev.in_motion_at_ball_snap.fillna(False).astype(int)
    for category in CATEGORICAL:
        dev[category] = dev[category].fillna('UNK').astype(str)
    levels = {category: sorted(dev[category].unique().tolist()) for category in CATEGORICAL}
    metadata = dict(reference_players=len(reference), reference_classes=[2023,2024],
                    median_forty=median_forty, cushion_median=cushion_median,
                    player_scalers=scalers, categories=levels, development_missing=missing,
                    evaluation_unknown_rule='Unseen levels map to UNK if present, otherwise first training level')
    return dev, metadata


def baseline_design(dev, metadata):
    x = pd.DataFrame({'Intercept': np.ones(len(dev))}, index=dev.index)
    ids = sorted(dev.nfl_id.unique())
    for pid in ids[1:]:
        x[f'player_{pid}'] = (dev.nfl_id==pid).astype(float)
    for cat in CATEGORICAL:
        for level in metadata['categories'][cat][1:]:
            x[f'{cat}={level}'] = (dev[cat]==level).astype(float)
    for feature in ['yards_to_go', 'motion', 'cushion_f', 'cushion_missing']:
        x[feature] = dev[feature].astype(float)
    for feature in CONVENTIONAL:
        x[f'{feature}:BREAK'] = dev[feature] * dev.BREAK
    weights = 1/dev.groupby(['nfl_id','BREAK']).nfl_id.transform('size')
    x, dropped = independent_columns(x, weights)
    return x, weights, dropped


def measurement_screen(dev, x, weights):
    fit = sm.WLS(dev.separation_at_pass_forward, x, weights=weights).fit()
    dev = dev.copy()
    # Player intercepts cancel in the family difference. Subtract all other baseline
    # components, including conventional interactions, as specified by the screen.
    component = [name for name in x if name!='Intercept' and not name.startswith('player_')]
    dev['adjusted'] = dev.separation_at_pass_forward - x[component].dot(fit.params[component])
    game_order = dev[['nfl_id','game_id']].drop_duplicates().sort_values(['nfl_id','game_id'])
    game_order['half'] = game_order.groupby('nfl_id').cumcount()%2
    dev = dev.merge(game_order, validate='many_to_one')
    family = dev.groupby(['nfl_id','half','BREAK']).agg(
        n=('nfl_id','size'), raw=('separation_at_pass_forward','mean'), adjusted=('adjusted','mean'))
    counts = family.n.unstack(['half','BREAK']).reindex(columns=pd.MultiIndex.from_product([[0,1],[0,1]]))
    ids = counts.index[(counts.fillna(0)>=3).all(axis=1)]
    contrasts = pd.DataFrame(index=ids)
    rows = []
    for outcome in ['raw','adjusted']:
        cells = family[outcome].unstack(['half','BREAK'])
        for half in [0,1]:
            contrasts[f'{outcome}_{half}'] = cells.loc[ids, (half,1)]-cells.loc[ids, (half,0)]
        rows.append(dict(contrast=outcome, **paired_reliability(
            contrasts[f'{outcome}_0'], contrasts[f'{outcome}_1'])))
    adjusted = rows[1]
    passes = (len(ids)>=25 and adjusted['SB'] is not None and adjusted['SB']>=0.40)
    return rows, contrasts.reset_index(), fit, passes


def plot_screen(contrasts, rows, target):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1,2,figsize=(9,4.3),layout='constrained')
    for ax, row, color in zip(axes,rows,['#0072B2','#D55E00']):
        kind = row['contrast']
        a, b = contrasts[f'{kind}_0'], contrasts[f'{kind}_1']
        ax.scatter(a,b,color=color,alpha=.75,s=28)
        limits = [min(a.min(),b.min())-.15, max(a.max(),b.max())+.15]
        ax.plot(limits,limits,color='#777777',lw=.8,ls='--')
        ax.axhline(0,color='#BBBBBB',lw=.6); ax.axvline(0,color='#BBBBBB',lw=.6)
        ax.set(xlim=limits,ylim=limits,xlabel='Alternating games: half A (yards)',
               ylabel='Alternating games: half B (yards)')
        if row['r'] is not None:
            ax.set_title(f"{kind.capitalize()} contrast · n={row['n']}\n"
                         f"r={row['r']:.2f} [{row['r_lo']:.2f}, {row['r_hi']:.2f}] · SB={row['SB']:.2f}",fontsize=10)
    fig.suptitle('Does BREAK-minus-GO separation repeat across rookie games?',fontsize=13)
    fig.savefig(target,dpi=200)
    plt.close(fig)


def main():
    reports = ROOT/'reports'
    dev, players, support, evaluation_n = candidate_table()
    if dev.nfl_id.nunique()<35 or evaluation_n<15:
        raise ValueError(f'Frozen support gate fails: {support}')
    dev, metadata = preprocess_development(dev, players)
    x, weights, dropped = baseline_design(dev, metadata)
    rows, contrasts, baseline, passes = measurement_screen(dev,x,weights)
    result = dict(generated_utc=datetime.now(timezone.utc).isoformat(), stage='measurement only',
                  support=support, preprocessing=metadata, dropped_redundant_columns=dropped,
                  design_columns=x.columns.tolist(), model_rank=int(np.linalg.matrix_rank(x.to_numpy())),
                  development_players=int(dev.nfl_id.nunique()), development_plays=len(dev),
                  development_games=int(dev.game_id.nunique()),
                  diagnostic=rows, screen_passes=bool(passes),
                  primary_TURN_association_fitted=False, evaluation_outcomes_opened=False,
                  decision=('Screen passes; freeze before separate development interaction fit' if passes
                            else 'Stop primary route-performance claim: frozen reliability screen fails'))
    (reports/'study3_measurement.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (reports/'study3_preprocessing.json').write_text(json.dumps(metadata,indent=2,allow_nan=False)+'\n')
    contrasts.to_parquet(ROOT/'data/interim/study3_measurement_halves.parquet',index=False)
    # Store the conventional baseline for an auditable screen, without interaction fitting.
    (reports/'study3_baseline.json').write_text(json.dumps(
        dict(coefficients=baseline.params.to_dict(), columns=x.columns.tolist(),
             preprocessing=metadata, dropped_columns=dropped),indent=2,allow_nan=False)+'\n')
    (reports/'figures').mkdir(exist_ok=True)
    plot_screen(contrasts,rows,reports/'figures/study3_measurement.png')
    rounded = [{k:round(v,3) if isinstance(v,float) else v for k,v in r.items()} for r in rows]
    (reports/'study3_measurement.md').write_text(
        '# Study 3 — Frozen measurement screen\n\n'
        f"Generated UTC: {result['generated_utc']}. **{result['decision']}.**\n\n"
        'No TURN–separation association or 2025 performance evaluation was fitted. The '
        'only outcome fit is the frozen conventional baseline on 2023–24 rookie REG plays.\n\n'
        + markdown_table(support)
        + '\n## Alternating-game contrast reliability\n\n'
        + markdown_table(rounded)
        + '\nChronological game IDs are ordered within each athlete and alternated. Each '
        'diagnostic player has ≥3 outcome-recorded BREAK and GO plays in each half. Raw '
        'contrast is mean BREAK separation minus mean GO separation, in yards. Adjusted '
        'contrast removes non-player components of the conventional baseline, including '
        'conventional-measurable family interactions. The halves share estimated adjustments; '
        'this is a descriptive screen, not an independent replication. 10,000 paired player '
        'bootstrap resamples give percentile correlation intervals; negative SB values '
        'are retained.\n\n'
        'Frozen gate: ≥25 diagnostic development players and adjusted SB point estimate '
        '≥0.40. A pass still requires acknowledging its interval; a fail stops the primary '
        'route-performance claim without trying alternate groups or thresholds.\n\n'
        f"Baseline: {len(dev):,} plays, {result['development_players']} players, "
        f"{result['development_games']} games; design rank {result['model_rank']}. "
        'Row weight is 1/n(player,family), giving equal total weight to each player/family. '
        'Player fixed intercepts; separate route/down/coverage/alignment indicators; linear '
        'yards-to-go, motion, cushion/missing indicator; six conventional BREAK interactions. '
        'All player SDs and forty imputation use unique 2023–24 WRs; cushion uses development '
        'plays. No evaluation statistics inform preprocessing.\n\n'
        f"Redundant columns removed in declared order: {dropped}.\n\n"
        'Saved: `study3_measurement.json`, `study3_preprocessing.json`, '
        '`study3_baseline.json`; figure `figures/study3_measurement.png`. '
        'Full-cohort TURN numerical values differ from the training-reference recomputation '
        'by design. Prior 2025 exposure in Studies 1–2 remains disclosed.\n')
    print(result['decision'],flush=True)
    print(markdown_table(rounded),flush=True)


if __name__=='__main__':
    main()
