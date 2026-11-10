"""Reproduce movement reliability without any NFL outcome associations.

Run: .venv/bin/python -m src.reliability
Writes reports/reliability.{md,json} and training-only TURN reference metadata.
"""
from datetime import datetime, timezone
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.audit_data import markdown_table

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261109


def paired_reliability(x, y, n_boot=10000, seed=SEED):
    x, y = np.asarray(x, float), np.asarray(y, float)
    valid = np.isfinite(x) & np.isfinite(y)
    x, y = x[valid], y[valid]
    n = len(x)
    if n < 4 or np.std(x) == 0 or np.std(y) == 0:
        return dict(n=n, r=None, r_lo=None, r_hi=None, SB=None,
                    SB_lo=None, SB_hi=None, valid_bootstraps=0)
    r = float(np.corrcoef(x, y)[0, 1])
    rng = np.random.default_rng(seed)
    draws = rng.integers(n, size=(n_boot, n))
    a, b = x[draws], y[draws]
    a -= a.mean(axis=1, keepdims=True)
    b -= b.mean(axis=1, keepdims=True)
    denom = np.sqrt((a*a).sum(axis=1) * (b*b).sum(axis=1))
    rs = np.divide((a*b).sum(axis=1), denom,
                   out=np.full(n_boot, np.nan), where=denom > 0)
    rs = rs[np.isfinite(rs)]
    lo, hi = np.quantile(rs, [0.025, 0.975])
    # Retain negative estimates; do not turn noise into positive reliability.
    sb = lambda v: float(2*v/(1+v)) if v > -1 else None
    return dict(n=n, r=r, r_lo=float(lo), r_hi=float(hi), SB=sb(r),
                SB_lo=sb(lo), SB_hi=sb(hi), valid_bootstraps=len(rs))


def training_turn(attempts, players):
    """Original TURN definition with 2023/24 drill reference statistics only."""
    pd_table = attempts.groupby(['nfl_id', 'drill'], as_index=False).lat.mean()
    pd_table = pd_table.merge(players[['nfl_id', 'draft_year']], validate='many_to_one')
    train = pd_table[pd_table.draft_year.isin([2023, 2024])]
    ref = train.groupby('drill').lat.agg(['mean', 'std', 'count'])
    keep = (ref['count'] >= 2) & np.isfinite(ref['std']) & (ref['std'] > 0)
    excluded = ref.index[~keep].tolist()
    unseen = sorted(set(pd_table.drill) - set(ref.index))
    ref = ref[keep]
    scored = pd_table.merge(ref, left_on='drill', right_index=True, validate='many_to_one')
    scored['z'] = (scored.lat - scored['mean']) / scored['std']
    scored = scored.sort_values(['nfl_id', 'drill'])
    scored['half'] = scored.groupby('nfl_id').cumcount() % 2
    full = scored.groupby('nfl_id').z.mean().rename('TURN').to_frame()
    half = scored.pivot_table(index='nfl_id', columns='half', values='z', aggfunc='mean')
    full = full.join(half.rename(columns={0: 'TURN_A', 1: 'TURN_B'})).reset_index()
    metadata = dict(reference_classes=[2023, 2024], ddof=1,
                    reference_population='All development-class Combine athletes, across positions',
                    excluded_constant_or_sparse_drills=excluded, unseen_drills=unseen,
                    drill_reference=ref.reset_index().to_dict(orient='records'))
    return full, metadata


def main():
    interim, reports = ROOT/'data/interim', ROOT/'reports'
    players = pd.read_parquet(interim/'combine_results.parquet')
    traits = pd.read_parquet(interim/'combine_traits.parquet').merge(
        players[['nfl_id', 'combine_position', 'draft_year']], validate='one_to_one')
    attempts = pd.read_parquet(interim/'combine_attempts.parquet')
    turn, metadata = training_turn(attempts, players)
    dev = turn.merge(players, validate='one_to_one')
    rows = []
    for pos in ['WR', 'DB', 'OL', 'DL', 'TE']:
        historical = traits[traits.combine_position == pos]
        for feature in ['lat', 'burst', 'brake', 'vmax']:
            rows.append(dict(sample='historical full cohort', position=pos, feature=feature,
                             **paired_reliability(historical[f'{feature}_A'], historical[f'{feature}_B'])))
        d = dev[(dev.combine_position == pos) & dev.draft_year.isin([2023, 2024])]
        rows.append(dict(sample='development, training reference', position=pos, feature='TURN',
                         **paired_reliability(d.TURN_A, d.TURN_B)))

    # Order repeats by explicit attempt number; event ID breaks ties deterministically.
    event_order = pd.read_parquet(interim/'combine_frames.parquet',
                                 columns=['event_id', 'attempt']).drop_duplicates()
    if event_order.event_id.duplicated().any():
        raise ValueError('An event has inconsistent attempt numbers')
    repeat = attempts.merge(event_order, validate='many_to_one').merge(
        players[['nfl_id', 'combine_position', 'draft_year']], validate='many_to_one')
    repeat = repeat.sort_values(['nfl_id', 'drill', 'attempt', 'event_id'])
    repeat['repeat_index'] = repeat.groupby(['nfl_id', 'drill']).cumcount()
    repeat_rows = []
    for (pos, drill), d in repeat.groupby(['combine_position', 'drill']):
        pair = d[d.repeat_index < 2].pivot(index='nfl_id', columns='repeat_index', values='lat')
        n_pair = int(pair.dropna().shape[0]) if 1 in pair else 0
        if n_pair:
            estimate = paired_reliability(pair[0], pair[1])
            repeat_rows.append(dict(position=pos, drill=drill, **estimate))

    qc = dict(attempts=len(attempts), nonfinite_turn_attempts=int((~np.isfinite(attempts.lat)).sum()),
              nonpositive_duration=int((attempts.dur <= 0).sum()),
              nonfinite_coordinates=None,
              dropped_attempts=0,
              turn_range=[float(attempts.lat.min()), float(attempts.lat.max())])
    import duckdb
    con = duckdb.connect()
    con.execute("SET threads=2")
    qc['nonfinite_coordinates'] = con.execute("""SELECT count(*) FROM read_parquet(?)
        WHERE NOT isfinite(x) OR NOT isfinite(y) OR x IS NULL OR y IS NULL""",
        [str(interim/'combine_frames.parquet')]).fetchone()[0]
    con.close()
    if qc['nonfinite_turn_attempts'] or qc['nonfinite_coordinates'] or qc['nonpositive_duration']:
        raise ValueError(f'Exposure QC failed: {qc}')
    turn.to_parquet(interim/'study3_turn.parquet', index=False)
    result = dict(generated_utc=datetime.now(timezone.utc).isoformat(), seed=SEED,
                  bootstrap_resamples=10000, cross_drill=rows, same_drill_turn=repeat_rows,
                  qc=qc, preprocessing=metadata)
    (reports/'reliability.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    (reports/'study3_turn_reference.json').write_text(json.dumps(metadata, indent=2, allow_nan=False)+'\n')
    display = lambda data: [{k: round(v, 3) if isinstance(v, float) else v
                             for k, v in row.items()} for row in data]
    (reports/'reliability.md').write_text(
        '# Movement reliability reproduction\n\n'
        f"Generated UTC: {result['generated_utc']}. Seed {SEED}; 10,000 paired athlete bootstrap resamples.\n\n"
        'Cross-drill halves use alphabetically ordered canonical drills, alternating within athlete, '
        'as in the original pipeline. These measure consistency across different tasks, not '
        'same-route test–retest. Spearman–Brown (SB) assumes comparable halves; negative values '
        'are retained and intervals describe substantial uncertainty.\n\n'
        + markdown_table(display(rows))
        + '\n## Same-drill TURN repeats\n\n'
        'First two attempts by recorded attempt number (event ID breaks ties). Pearson r is the '
        'repeat correlation; SB is a two-attempt composite estimate, not the reliability of a '
        'single attempt. Fewer than four pairs return no estimate. No reliability-based feature '
        'selection or attempt exclusion. These descriptive repeats include all classes.\n\n'
        + markdown_table(display(repeat_rows))
        + '\n## Exposure QC and training-only reference\n\n'
        + markdown_table([qc])
        + '\nTraining-reference means/SDs use unique player/drill means from 2023–24 athletes '
        'across positions. The same reference transforms 2025 without using its distribution. '
        f"Excluded constant/sparse drills: {metadata['excluded_constant_or_sparse_drills']}; "
        f"unseen drills: {metadata['unseen_drills']}. Metadata: `study3_turn_reference.json`.\n\n"
        'This check uses no NFL outcomes. Trace figures and the route-contrast measurement '
        'screen are separate requirements. Historical reports remain unchanged.\n')
    print(markdown_table(display([r for r in rows if r['position'] == 'WR'])), flush=True)


if __name__ == '__main__':
    main()
